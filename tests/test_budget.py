"""Tests for budget tracking."""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sovereign_dispatch.budget import BudgetExhausted, BudgetTracker
from sovereign_dispatch.config import BudgetConfig


def _tmp_budget(**kwargs) -> BudgetTracker:
    defaults = {
        "max_daily_usd": 1.00,
        "max_monthly_usd": 10.00,
        "warn_at_percent": 80,
        "ledger_path": tempfile.mktemp(suffix=".db"),
    }
    defaults.update(kwargs)
    return BudgetTracker(BudgetConfig(**defaults))


def test_fresh_budget():
    bt = _tmp_budget()
    s = bt.status()
    assert s.daily_spend == 0.0
    assert s.remaining_daily == 1.00
    assert not s.warn


def test_record_and_track():
    bt = _tmp_budget()
    bt.record("task1", 0.50)
    s = bt.status()
    assert s.daily_spend == 0.50
    assert s.remaining_daily == 0.50


def test_would_exceed():
    bt = _tmp_budget(max_daily_usd=1.00)
    bt.record("task1", 0.90)
    assert bt.would_exceed(0.20)  # 0.90 + 0.20 > 1.00
    assert not bt.would_exceed(0.05)  # 0.90 + 0.05 < 1.00


def test_warn_threshold():
    bt = _tmp_budget(max_daily_usd=1.00, warn_at_percent=80)
    bt.record("task1", 0.81)
    s = bt.status()
    assert s.warn


def test_local_dispatch_free():
    bt = _tmp_budget()
    bt.record("task1", 0.0, backend="local")
    s = bt.status()
    assert s.daily_spend == 0.0
