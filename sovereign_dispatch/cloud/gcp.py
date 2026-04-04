"""GCP cloud dispatch. Cloud Functions for quick jobs, Cloud Run for heavy."""

from __future__ import annotations

import json
import time
from urllib.request import Request, urlopen

from ..config import CloudConfig
from ..dispatch import DispatchResult, Task
from .auth import GCPAuth


class CloudDispatcher:
    """Dispatches to Google Cloud. Only instantiated when router escalates."""

    def __init__(self, config: CloudConfig):
        self.config = config
        self._auth = GCPAuth(config.project_id)

    def execute(self, task: Task) -> DispatchResult:
        est_seconds = task.hints.get("estimated_seconds", 0)
        if est_seconds > 60:
            return self._run_cloud_run_job(task)
        return self._run_cloud_function(task)

    def _run_cloud_function(self, task: Task) -> DispatchResult:
        """Invoke a Cloud Function synchronously. Fast path."""
        project = self._auth.project_id
        region = self.config.region
        url = (
            f"https://{region}-{project}.cloudfunctions.net/sovereign-dispatch"
        )
        return self._invoke_http(url, task)

    def _run_cloud_run_job(self, task: Task) -> DispatchResult:
        """Submit to Cloud Run Jobs. Polls for completion. Heavy path."""
        project = self._auth.project_id
        region = self.config.region
        url = (
            f"https://{region}-run.googleapis.com/apis/run.googleapis.com/v1/"
            f"namespaces/{project}/jobs/sovereign-dispatch:run"
        )
        return self._invoke_http(url, task)

    def _invoke_http(self, url: str, task: Task) -> DispatchResult:
        """HTTP dispatch with auth token. Minimal payload."""
        t0 = time.monotonic()
        payload = json.dumps({
            "code": task.code,
            "kind": task.kind,
            "hints": task.hints,
        }).encode()

        # Get auth token
        creds = self._auth.credentials
        if hasattr(creds, "token") and creds.token:
            token = creds.token
        else:
            # Refresh to get a token
            from google.auth.transport.requests import Request as AuthRequest
            creds.refresh(AuthRequest())
            token = creds.token

        req = Request(
            url, data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

        try:
            with urlopen(req, timeout=300) as resp:
                body = json.loads(resp.read())
            elapsed = time.monotonic() - t0

            # Estimate cost: Cloud Functions ~$0.0000004/invocation + compute
            est_cost = max(0.001, elapsed * 0.0001)

            return DispatchResult(
                stdout=body.get("stdout", ""),
                stderr=body.get("stderr", ""),
                exit_code=body.get("exit_code", 0),
                elapsed_seconds=elapsed,
                cost_usd=round(est_cost, 6),
                backend="cloud",
            )
        except Exception as e:
            elapsed = time.monotonic() - t0
            return DispatchResult(
                stdout="", stderr=f"Cloud dispatch failed: {e}",
                exit_code=1, elapsed_seconds=elapsed,
                cost_usd=0.0, backend="cloud",
            )
