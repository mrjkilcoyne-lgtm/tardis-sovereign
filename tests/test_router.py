"""Tests for the router."""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from sovereign_dispatch.budget import BudgetExhausted, BudgetTracker
from sovereign_dispatch.config import BudgetConfig, Config
from sovereign_dispatch.dispatch import LocalDispatcher, Task
from sovereign_dispatch.router import route


def _budget(**kwargs) -> BudgetTracker:
    defaults = {
        "max_daily_usd": 10.00,
        "max_monthly_usd": 100.00,
        "warn_at_percent": 80,
        "ledger_path": tempfile.mktemp(suffix=".db"),
    }
    defaults.update(kwargs)
    return BudgetTracker(BudgetConfig(**defaults))


def test_default_routes_local():
    config = Config()
    budget = _budget()
    task = Task(code="print(1)")
    dispatcher = route(task, config, budget)
    assert isinstance(dispatcher, LocalDispatcher)


def test_force_local():
    config = Config()
    budget = _budget()
    task = Task(code="print(1)", hints={"force_local": True})
    dispatcher = route(task, config, budget)
    assert isinstance(dispatcher, LocalDispatcher)


def test_budget_exhausted():
    config = Config()
    budget = _budget(max_daily_usd=0.01)
    budget.record("x", 0.01)
    task = Task(code="print(1)", hints={"force_cloud": True})
    with pytest.raises(BudgetExhausted):
        route(task, config, budget)
