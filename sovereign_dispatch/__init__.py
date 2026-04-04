"""Sovereign Dispatch - Local-first code execution with cloud escalation.

Usage:
    from sovereign_dispatch import dispatch

    result = dispatch("print('hello from the TARDIS')")
    print(result.stdout)  # hello from the TARDIS
"""

from __future__ import annotations

from .budget import BudgetExhausted, BudgetTracker
from .cache import ResultCache
from .compress import content_hash
from .config import Config, load_config
from .dispatch import DispatchResult, Task
from .router import route

# Module-level singletons, lazily initialised
_config: Config | None = None
_budget: BudgetTracker | None = None
_cache: ResultCache | None = None


def _ensure_init(config_path: str | None = None):
    global _config, _budget, _cache
    if _config is None or config_path:
        _config = load_config(config_path)
        _budget = BudgetTracker(_config.budget)
        _cache = ResultCache(_config.cache)


def dispatch(
    code: str,
    kind: str = "python",
    hints: dict | None = None,
    payload: bytes | None = None,
    config_path: str | None = None,
) -> DispatchResult:
    """One-call dispatch. Checks cache, routes, executes, records cost.

    Args:
        code: Python code or shell command to run.
        kind: "python" or "shell".
        hints: Optional dict with estimated_seconds, estimated_memory_mb,
               force_cloud, force_local, timeout.
        payload: Optional data blob passed to the task.
        config_path: Optional path to YAML config file.

    Returns:
        DispatchResult with stdout, stderr, exit_code, cost, timing.

    Raises:
        BudgetExhausted: If dispatch would exceed configured budget.
    """
    _ensure_init(config_path)

    task = Task(code=code, kind=kind, hints=hints or {}, payload=payload)

    # 1. Cache check - zero cost if we've seen this before
    cache_key = content_hash(code, payload)
    if _cache and _cache.enabled:
        cached = _cache.get(cache_key)
        if cached is not None:
            return cached

    # 2. Route - picks local or cloud
    dispatcher = route(task, _config, _budget)

    # 3. Execute
    result = dispatcher.execute(task)

    # 4. Record cost
    _budget.record(task.content_hash, result.cost_usd, result.backend)

    # 5. Cache result (only successful runs)
    if result.ok() and _cache and _cache.enabled:
        _cache.put(cache_key, result)

    return result


def get_budget(config_path: str | None = None) -> dict:
    """Get current budget status."""
    _ensure_init(config_path)
    status = _budget.status()
    return {
        "daily_spend": status.daily_spend,
        "monthly_spend": status.monthly_spend,
        "daily_limit": status.daily_limit,
        "monthly_limit": status.monthly_limit,
        "remaining_daily": status.remaining_daily,
        "remaining_monthly": status.remaining_monthly,
        "warn": status.warn,
    }


def clear_cache(config_path: str | None = None) -> int:
    """Evict expired cache entries. Returns count removed."""
    _ensure_init(config_path)
    return _cache.evict_expired()


__all__ = [
    "dispatch",
    "get_budget",
    "clear_cache",
    "Task",
    "DispatchResult",
    "BudgetExhausted",
    "Config",
    "load_config",
]
