"""Core dispatch engine. Local execution that looks remote but isn't."""

from __future__ import annotations

import hashlib
import json
import os
import resource
import signal
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from .config import Config, LocalConfig


@dataclass
class Task:
    """What to run."""
    code: str
    kind: str = "python"           # "python" | "shell"
    hints: dict = field(default_factory=dict)  # estimated_seconds, estimated_memory_mb, force_cloud, force_local
    payload: bytes | None = None   # optional data blob

    @property
    def content_hash(self) -> str:
        h = hashlib.sha256(self.code.encode())
        if self.payload:
            h.update(self.payload)
        h.update(self.kind.encode())
        return h.hexdigest()[:16]


@dataclass
class DispatchResult:
    """What came back."""
    stdout: str
    stderr: str
    exit_code: int
    elapsed_seconds: float
    cost_usd: float = 0.0
    cached: bool = False
    backend: str = "local"

    def ok(self) -> bool:
        return self.exit_code == 0

    def to_dict(self) -> dict:
        return {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "exit_code": self.exit_code,
            "elapsed": round(self.elapsed_seconds, 3),
            "cost_usd": self.cost_usd,
            "cached": self.cached,
            "backend": self.backend,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, d: dict) -> DispatchResult:
        return cls(
            stdout=d["stdout"],
            stderr=d["stderr"],
            exit_code=d["exit_code"],
            elapsed_seconds=d.get("elapsed", 0.0),
            cost_usd=d.get("cost_usd", 0.0),
            cached=d.get("cached", False),
            backend=d.get("backend", "local"),
        )


class Dispatcher(Protocol):
    def execute(self, task: Task) -> DispatchResult: ...


class LocalDispatcher:
    """Runs code in a subprocess sandbox. Fast. Looks remote. Isn't."""

    def __init__(self, config: LocalConfig):
        self.config = config
        self._python = config.python_path or sys.executable

    def execute(self, task: Task) -> DispatchResult:
        if task.kind == "python":
            return self._run_python(task)
        elif task.kind == "shell":
            return self._run_shell(task)
        else:
            return DispatchResult(
                stdout="", stderr=f"Unknown task kind: {task.kind}",
                exit_code=1, elapsed_seconds=0.0,
            )

    def _run_python(self, task: Task) -> DispatchResult:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, prefix="sov_"
        ) as f:
            f.write(task.code)
            script_path = f.name

        try:
            return self._exec(
                [self._python, "-u", script_path],
                task, env_extra=self._payload_env(task),
            )
        finally:
            os.unlink(script_path)

    def _run_shell(self, task: Task) -> DispatchResult:
        return self._exec(
            ["sh", "-c", task.code],
            task, env_extra=self._payload_env(task),
        )

    def _exec(
        self, cmd: list[str], task: Task,
        env_extra: dict[str, str] | None = None,
    ) -> DispatchResult:
        env = os.environ.copy()
        env["SOVEREIGN_DISPATCH"] = "1"  # so code knows it's dispatched
        if env_extra:
            env.update(env_extra)

        timeout = task.hints.get("timeout", self.config.timeout_seconds)
        mem_mb = task.hints.get("max_memory_mb", self.config.max_memory_mb)

        # Build preexec to set resource limits on Linux
        def _limit():
            if sys.platform != "win32":
                mem_bytes = mem_mb * 1024 * 1024
                try:
                    resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
                except (ValueError, resource.error):
                    pass  # best effort

        t0 = time.monotonic()
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True,
                timeout=timeout, env=env, preexec_fn=_limit,
            )
            elapsed = time.monotonic() - t0
            return DispatchResult(
                stdout=proc.stdout, stderr=proc.stderr,
                exit_code=proc.returncode, elapsed_seconds=elapsed,
            )
        except subprocess.TimeoutExpired:
            elapsed = time.monotonic() - t0
            return DispatchResult(
                stdout="", stderr=f"Timeout after {timeout}s",
                exit_code=124, elapsed_seconds=elapsed,
            )

    @staticmethod
    def _payload_env(task: Task) -> dict[str, str] | None:
        """Pass payload as env var if small, temp file if large."""
        if not task.payload:
            return None
        if len(task.payload) < 32768:  # 32KB inline
            return {"SOVEREIGN_PAYLOAD": task.payload.hex()}
        # Write to temp file, code reads SOVEREIGN_PAYLOAD_FILE
        f = tempfile.NamedTemporaryFile(delete=False, prefix="sov_data_")
        f.write(task.payload)
        f.close()
        return {"SOVEREIGN_PAYLOAD_FILE": f.name}
