"""Result cache. SQLite, content-addressed, LRU eviction. Zero waste."""

from __future__ import annotations

import json
import sqlite3
import time
import zlib
from pathlib import Path

from .config import CacheConfig
from .dispatch import DispatchResult


class ResultCache:
    """Content-addressed result cache. Same code = same result = no re-run."""

    def __init__(self, config: CacheConfig):
        self.config = config
        if not config.enabled:
            self._conn_fn = None
            return
        self._db_path = Path(config.db_path).expanduser()
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._db_path), timeout=5.0)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self):
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    result BLOB NOT NULL,
                    created_at REAL NOT NULL,
                    size_bytes INTEGER NOT NULL
                )
            """)

    @property
    def enabled(self) -> bool:
        return self.config.enabled

    def get(self, key: str) -> DispatchResult | None:
        if not self.enabled:
            return None
        with self._conn() as conn:
            row = conn.execute(
                "SELECT result, created_at FROM cache WHERE key = ?", (key,)
            ).fetchone()
        if not row:
            return None
        blob, created_at = row
        # TTL check
        if time.time() - created_at > self.config.ttl_seconds:
            self._evict_key(key)
            return None
        data = json.loads(zlib.decompress(blob))
        result = DispatchResult.from_dict(data)
        result.cached = True
        return result

    def put(self, key: str, result: DispatchResult):
        if not self.enabled:
            return
        blob = zlib.compress(json.dumps(result.to_dict()).encode())
        with self._conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache (key, result, created_at, size_bytes) VALUES (?, ?, ?, ?)",
                (key, blob, time.time(), len(blob)),
            )
        self._maybe_evict()

    def _evict_key(self, key: str):
        with self._conn() as conn:
            conn.execute("DELETE FROM cache WHERE key = ?", (key,))

    def _maybe_evict(self):
        """Evict oldest entries if over max size."""
        max_bytes = self.config.max_size_mb * 1024 * 1024
        with self._conn() as conn:
            (total,) = conn.execute(
                "SELECT COALESCE(SUM(size_bytes), 0) FROM cache"
            ).fetchone()
            if total <= max_bytes:
                return
            # Delete oldest 25% by creation time
            conn.execute("""
                DELETE FROM cache WHERE key IN (
                    SELECT key FROM cache ORDER BY created_at ASC
                    LIMIT (SELECT COUNT(*) / 4 FROM cache)
                )
            """)

    def evict_expired(self) -> int:
        if not self.enabled:
            return 0
        cutoff = time.time() - self.config.ttl_seconds
        with self._conn() as conn:
            cursor = conn.execute(
                "DELETE FROM cache WHERE created_at < ?", (cutoff,)
            )
            return cursor.rowcount
