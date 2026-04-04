"""Tests for adaptive runtime detection and config."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sovereign_dispatch.adaptive import AdaptiveConfig, RuntimeProfile, detect_runtime


def test_detect_runtime_runs():
    profile = detect_runtime()
    assert profile.python_version[0] >= 3
    assert profile.cpu_count >= 1
    assert "subprocess" in profile.proven_backends


def test_adaptive_defaults():
    ac = AdaptiveConfig()
    assert ac.best_local_backend() == "subprocess"
    assert ac.recommended_concurrency() >= 1


def test_adapt_hints_passthrough():
    ac = AdaptiveConfig()
    hints = {"timeout": 60, "force_local": True}
    adapted = ac.adapt_task_hints(hints)
    assert adapted["timeout"] == 60
    assert adapted["force_local"] is True


def test_adapt_ml_without_gpu():
    profile = RuntimeProfile(gpu_available=False, has_torch=False)
    ac = AdaptiveConfig(profile)
    hints = {"ml": True}
    adapted = ac.adapt_task_hints(hints)
    # Should suggest cloud-scale estimates since no GPU
    assert adapted.get("estimated_seconds", 0) > 0


def test_adapt_transformers_missing_no_cloud():
    """No transformers, no cloud CLI -> falls back to local gracefully."""
    profile = RuntimeProfile(has_transformers=False, has_torch=False)
    ac = AdaptiveConfig(profile)
    hints = {"transformers": True}
    adapted = ac.adapt_task_hints(hints)
    # Safety valve: no gcloud means force_local, not force_cloud
    assert adapted.get("force_local") is True


def test_adapt_transformers_missing_with_cloud():
    """No transformers but cloud available -> escalates to cloud."""
    profile = RuntimeProfile(has_transformers=False, has_torch=False, has_gcloud=True)
    ac = AdaptiveConfig(profile)
    hints = {"transformers": True}
    adapted = ac.adapt_task_hints(hints)
    assert adapted.get("force_cloud") is True


def test_adapt_transformers_present():
    profile = RuntimeProfile(has_transformers=True, has_torch=True)
    ac = AdaptiveConfig(profile)
    hints = {"transformers": True}
    adapted = ac.adapt_task_hints(hints)
    # Shouldn't force cloud if transformers are local
    assert adapted.get("force_cloud") is not True


def test_status_safe():
    ac = AdaptiveConfig()
    status = ac.status()
    assert "python" in status
    assert "backends" in status
    assert "memory_mb" in status
    # Shouldn't leak anything sensitive
    assert "path" not in str(status).lower()


def test_low_memory_conservative_timeout():
    profile = RuntimeProfile(available_memory_mb=128)
    ac = AdaptiveConfig(profile)
    hints = {}
    adapted = ac.adapt_task_hints(hints)
    assert adapted.get("timeout", 30) <= 15


def test_concurrency_scales_with_resources():
    small = AdaptiveConfig(RuntimeProfile(cpu_count=1, available_memory_mb=128))
    big = AdaptiveConfig(RuntimeProfile(cpu_count=8, available_memory_mb=4096))
    assert small.recommended_concurrency() <= big.recommended_concurrency()
