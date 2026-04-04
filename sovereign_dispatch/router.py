"""Router. Decides local vs cloud. No ML, no magic. Deterministic."""

from __future__ import annotations

from .budget import BudgetExhausted, BudgetTracker
from .config import Config
from .dispatch import Dispatcher, LocalDispatcher, Task


def route(task: Task, config: Config, budget: BudgetTracker) -> Dispatcher:
    """Pick the right dispatcher for a task.

    Decision order:
    1. Budget check - refuse if broke
    2. force_local / force_cloud hints
    3. Threshold check - escalate if task is heavy
    4. Default: local (free, fast)
    """
    estimated_cost = _estimate_cost(task, config)

    if budget.would_exceed(estimated_cost):
        status = budget.status()
        raise BudgetExhausted(
            f"Would exceed budget. Daily: ${status.daily_spend:.2f}/${status.daily_limit:.2f}, "
            f"Monthly: ${status.monthly_spend:.2f}/${status.monthly_limit:.2f}"
        )

    # Explicit hints override everything
    if task.hints.get("force_local"):
        return LocalDispatcher(config.local)

    if task.hints.get("force_cloud"):
        return _get_cloud_dispatcher(config)

    # Threshold-based escalation
    est_seconds = task.hints.get("estimated_seconds", 0)
    est_memory = task.hints.get("estimated_memory_mb", 0)

    if (
        est_seconds > config.cloud.escalation_threshold_seconds
        or est_memory > config.cloud.escalation_threshold_memory_mb
    ):
        return _get_cloud_dispatcher(config)

    # Default: local. Free. Fast. Yours.
    return LocalDispatcher(config.local)


def _estimate_cost(task: Task, config: Config) -> float:
    """Rough cost estimate. Local = $0. Cloud = pennies per invocation."""
    est_seconds = task.hints.get("estimated_seconds", 0)
    est_memory = task.hints.get("estimated_memory_mb", 0)

    if task.hints.get("force_local"):
        return 0.0

    if (
        task.hints.get("force_cloud")
        or est_seconds > config.cloud.escalation_threshold_seconds
        or est_memory > config.cloud.escalation_threshold_memory_mb
    ):
        # Cloud Run: ~$0.00002400/vCPU-sec + $0.00000250/GiB-sec
        # Rough estimate: $0.001 per 10 seconds
        return max(0.001, est_seconds * 0.0001)

    return 0.0  # local is free


def _get_cloud_dispatcher(config: Config) -> Dispatcher:
    """Lazy import - only pull in GCP deps when actually needed.
    Falls back to local if cloud deps aren't installed or auth fails.
    """
    try:
        from .cloud.gcp import CloudDispatcher
        d = CloudDispatcher(config.cloud)
        # Probe auth eagerly so we fail fast and fall back
        _ = d._auth.project_id
        return d
    except (ImportError, RuntimeError):
        # Cloud not available. Run local. Quietly.
        return LocalDispatcher(config.local)
