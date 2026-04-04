"""Tests for result cache."""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sovereign_dispatch.cache import ResultCache
from sovereign_dispatch.config import CacheConfig
from sovereign_dispatch.dispatch import DispatchResult


def _tmp_cache(**kwargs) -> ResultCache:
    defaults = {
        "enabled": True,
        "db_path": tempfile.mktemp(suffix=".db"),
        "max_size_mb": 1,
        "ttl_seconds": 3600,
    }
    defaults.update(kwargs)
    return ResultCache(CacheConfig(**defaults))


def _result(stdout: str = "ok") -> DispatchResult:
    return DispatchResult(stdout=stdout, stderr="", exit_code=0, elapsed_seconds=0.1)


def test_put_and_get():
    c = _tmp_cache()
    c.put("abc", _result("hello"))
    got = c.get("abc")
    assert got is not None
    assert got.stdout == "hello"
    assert got.cached is True


def test_miss():
    c = _tmp_cache()
    assert c.get("nonexistent") is None


def test_ttl_expiry():
    c = _tmp_cache(ttl_seconds=0)  # instant expiry
    c.put("abc", _result())
    import time
    time.sleep(0.01)
    assert c.get("abc") is None


def test_disabled_cache():
    c = _tmp_cache(enabled=False)
    c.put("abc", _result())
    assert c.get("abc") is None


def test_evict_expired():
    c = _tmp_cache(ttl_seconds=0)
    c.put("a", _result())
    c.put("b", _result())
    import time
    time.sleep(0.01)
    removed = c.evict_expired()
    assert removed >= 2
