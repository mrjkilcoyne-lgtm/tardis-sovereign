"""Tests for the dispatch engine."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sovereign_dispatch.config import LocalConfig
from sovereign_dispatch.dispatch import LocalDispatcher, Task


def test_python_hello():
    d = LocalDispatcher(LocalConfig())
    result = d.execute(Task(code="print('hello sovereign')"))
    assert result.ok()
    assert "hello sovereign" in result.stdout


def test_python_error():
    d = LocalDispatcher(LocalConfig())
    result = d.execute(Task(code="raise ValueError('boom')"))
    assert not result.ok()
    assert "boom" in result.stderr


def test_shell_command():
    d = LocalDispatcher(LocalConfig())
    result = d.execute(Task(code="echo 'tardis'", kind="shell"))
    assert result.ok()
    assert "tardis" in result.stdout


def test_timeout():
    d = LocalDispatcher(LocalConfig(timeout_seconds=1))
    result = d.execute(Task(
        code="import time; time.sleep(10)",
        hints={"timeout": 1},
    ))
    assert result.exit_code == 124
    assert "Timeout" in result.stderr


def test_dispatch_env_set():
    d = LocalDispatcher(LocalConfig())
    result = d.execute(Task(
        code="import os; print(os.environ.get('SOVEREIGN_DISPATCH', 'missing'))"
    ))
    assert result.ok()
    assert "1" in result.stdout


def test_payload_small():
    d = LocalDispatcher(LocalConfig())
    result = d.execute(Task(
        code="import os; print(os.environ.get('SOVEREIGN_PAYLOAD', 'none'))",
        payload=b"deadbeef",
    ))
    assert result.ok()
    assert "deadbeef".encode().hex() in result.stdout


def test_content_hash_deterministic():
    t1 = Task(code="print(1)")
    t2 = Task(code="print(1)")
    assert t1.content_hash == t2.content_hash

    t3 = Task(code="print(2)")
    assert t1.content_hash != t3.content_hash
