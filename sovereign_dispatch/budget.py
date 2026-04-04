"""Budget tracker. SQLite ledger. No dispatch without a cost check."""

from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path

from .config import BudgetConfig


class BudgetExhausted(Exception):
    """Raised when dispatch would exceed budget."""
    pass


@dataclass
class BudgetStatus:
    daily_spend: float
    monthly_spend: float
    daily_limit: float
    monthly_limit: float
    remaining_daily: float
    remaining_monthly: float
    warn: bool  # True if past warn_at_percent


class BudgetTracker:
    """SQLite-backed spend ledger. Thread-safe via WAL mode."""

    def __init__(self, config: BudgetConfig):
        self.config = config
        self._db_path = Path(config.ledger_path).expanduser()
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._db_path), timeout=5.0)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self):
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts REAL NOT NULL,
                    task_hash TEXT NOT NULL,
                    cost_usd REAL NOT NULL,
                    backend TEXT NOT NULL
                )
            """)

    def record(self, task_hash: str, cost_usd: float, backend: str = "local"):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO ledger (ts, task_hash, cost_usd, backend) VALUES (?, ?, ?, ?)",
                (time.time(), task_hash, cost_usd, backend),
            )

    def would_exceed(self, estimated_cost: float) -> bool:
        s = self.status()
        return (
            s.remaining_daily < estimated_cost
            or s.remaining_monthly < estimated_cost
        )

    def status(self) -> BudgetStatus:
        now = time.time()
        day_ago = now - 86400
        month_ago = now - 86400 * 30

        with self._conn() as conn:
            (daily,) = conn.execute(
                "SELECT COALESCE(SUM(cost_usd), 0) FROM ledger WHERE ts > ?",
                (day_ago,),
            ).fetchone()
            (monthly,) = conn.execute(
                "SELECT COALESCE(SUM(cost_usd), 0) FROM ledger WHERE ts > ?",
                (month_ago,),
            ).fetchone()

        remaining_d = max(0.0, self.config.max_daily_usd - daily)
        remaining_m = max(0.0, self.config.max_monthly_usd - monthly)
        warn_threshold = self.config.max_daily_usd * (self.config.warn_at_percent / 100)

        return BudgetStatus(
            daily_spend=round(daily, 4),
            monthly_spend=round(monthly, 4),
            daily_limit=self.config.max_daily_usd,
            monthly_limit=self.config.max_monthly_usd,
            remaining_daily=round(remaining_d, 4),
            remaining_monthly=round(remaining_m, 4),
            warn=daily >= warn_threshold,
        )
