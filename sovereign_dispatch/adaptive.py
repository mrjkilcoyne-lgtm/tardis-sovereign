"""Adaptive runtime configuration. Fluid. Quiet. Navigates fashion without following it.

The dispatch system doesn't care what's trendy in code. It detects
what's available, adapts to it, and runs your work in whatever
substrate is at hand. Transformers, venvs, containers, bare metal.
She shifts with the tides but keeps her own counsel.
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RuntimeProfile:
    """What this environment can do right now."""
    python_version: tuple[int, int, int] = (3, 10, 0)
    has_venv: bool = False
    has_docker: bool = False
    has_podman: bool = False
    has_gcloud: bool = False
    has_torch: bool = False
    has_transformers: bool = False
    has_numpy: bool = False
    available_memory_mb: int = 256
    cpu_count: int = 1
    gpu_available: bool = False
    platform: str = "unknown"
    # What runtimes we've seen work here
    proven_backends: list[str] = field(default_factory=list)


def detect_runtime() -> RuntimeProfile:
    """Sniff the environment. Quick and quiet."""
    profile = RuntimeProfile()

    # Python version
    v = sys.version_info
    profile.python_version = (v.major, v.minor, v.micro)

    # Platform
    profile.platform = sys.platform

    # Container runtimes
    profile.has_docker = shutil.which("docker") is not None
    profile.has_podman = shutil.which("podman") is not None

    # Cloud CLI
    profile.has_gcloud = shutil.which("gcloud") is not None

    # venv support
    try:
        import venv
        profile.has_venv = True
    except ImportError:
        pass

    # ML stack - lazy probe, don't import heavy libs
    profile.has_torch = _can_import("torch")
    profile.has_transformers = _can_import("transformers")
    profile.has_numpy = _can_import("numpy")

    # CPU count
    profile.cpu_count = os.cpu_count() or 1

    # Available memory (Linux)
    profile.available_memory_mb = _available_memory_mb()

    # GPU
    profile.gpu_available = _has_gpu()

    # Proven backends
    profile.proven_backends = ["subprocess"]  # always works
    if profile.has_venv:
        profile.proven_backends.append("venv")
    if profile.has_docker:
        profile.proven_backends.append("docker")
    if profile.has_podman:
        profile.proven_backends.append("podman")
    if profile.has_gcloud:
        profile.proven_backends.append("cloud")

    return profile


def _can_import(module: str) -> bool:
    """Check if a module is importable without actually importing it."""
    spec = importlib.util.find_spec(module)
    return spec is not None


def _available_memory_mb() -> int:
    """Best-effort memory detection."""
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) // 1024
    except (OSError, ValueError):
        pass
    # Fallback: assume modest
    return 256


def _has_gpu() -> bool:
    """Check for CUDA GPU. Quick check, no heavy imports."""
    # Check nvidia-smi first (fastest)
    if shutil.which("nvidia-smi") is not None:
        try:
            r = subprocess.run(
                ["nvidia-smi", "-L"], capture_output=True, text=True, timeout=5
            )
            return r.returncode == 0 and "GPU" in r.stdout
        except (subprocess.TimeoutExpired, OSError):
            pass
    return False


class AdaptiveConfig:
    """Wraps the static config and adjusts it based on what's actually here.

    Doesn't override explicit user config. Just fills in the gaps
    and makes sensible choices when the user hasn't specified.
    """

    def __init__(self, profile: RuntimeProfile | None = None):
        self._profile = profile or detect_runtime()
        self._hints_cache: dict[str, str] = {}

    @property
    def profile(self) -> RuntimeProfile:
        return self._profile

    def best_local_backend(self) -> str:
        """Pick the best local execution backend for this environment."""
        # Prefer subprocess - lowest overhead (~13ms)
        # Only use heavier backends when the task needs isolation
        return "subprocess"

    def should_use_gpu(self, task_hints: dict) -> bool:
        """Should this task attempt GPU execution?"""
        if not self._profile.gpu_available:
            return False
        if not self._profile.has_torch:
            return False
        return task_hints.get("gpu", False) or task_hints.get("ml", False)

    def can_run_transformers(self) -> bool:
        """Is the transformers stack available locally?"""
        return self._profile.has_transformers and self._profile.has_torch

    def recommended_concurrency(self) -> int:
        """How many parallel dispatches can this env handle?"""
        cpus = self._profile.cpu_count
        mem = self._profile.available_memory_mb
        # Each dispatch needs ~50MB headroom minimum
        mem_limited = max(1, mem // 50)
        return min(cpus, mem_limited, 8)

    def cloud_available(self) -> bool:
        """Can we escalate to cloud if needed?"""
        return self._profile.has_gcloud

    def adapt_task_hints(self, hints: dict) -> dict:
        """Enrich task hints based on what we know about this environment.

        Fills in estimated_seconds and estimated_memory_mb if not provided,
        based on code heuristics. Quiet. Conservative.
        """
        adapted = dict(hints)

        # If no timeout set and we're memory-constrained, be conservative
        if "timeout" not in adapted:
            if self._profile.available_memory_mb < 512:
                adapted.setdefault("timeout", 15)

        # If ML task but no local GPU, suggest cloud
        if adapted.get("ml") and not self._profile.gpu_available:
            if not adapted.get("force_local"):
                adapted.setdefault("estimated_seconds", 30)
                adapted.setdefault("estimated_memory_mb", 1024)

        # If transformers needed but not installed locally
        if adapted.get("transformers") and not self.can_run_transformers():
            if not adapted.get("force_local"):
                adapted["force_cloud"] = True

        # Safety valve: don't force cloud if cloud isn't available
        if adapted.get("force_cloud") and not self.cloud_available():
            del adapted["force_cloud"]
            adapted["force_local"] = True

        return adapted

    def status(self) -> dict:
        """Quick status for debugging. Doesn't expose anything sensitive."""
        p = self._profile
        return {
            "python": f"{p.python_version[0]}.{p.python_version[1]}.{p.python_version[2]}",
            "platform": p.platform,
            "memory_mb": p.available_memory_mb,
            "cpus": p.cpu_count,
            "gpu": p.gpu_available,
            "backends": p.proven_backends,
            "transformers": p.has_transformers,
            "concurrency": self.recommended_concurrency(),
        }
