"""Minimal HTTP API for Sovereign Dispatch.

Zero external dependencies - uses only stdlib http.server.
Keeps the Docker image small and the attack surface minimal.
"""

from __future__ import annotations

import json
import os
import sys
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler

# Add the app directory to path so sovereign_dispatch is importable
sys.path.insert(0, "/app")

from sovereign_dispatch import dispatch, get_budget, get_runtime


class DispatchHandler(BaseHTTPRequestHandler):
    """Handles /dispatch, /budget, /runtime, /healthz endpoints."""

    def do_GET(self):
        if self.path == "/healthz":
            self._json_response(200, {"status": "ok"})
        elif self.path == "/budget":
            try:
                self._json_response(200, get_budget())
            except Exception as e:
                self._json_response(500, {"error": str(e)})
        elif self.path == "/runtime":
            try:
                self._json_response(200, get_runtime())
            except Exception as e:
                self._json_response(500, {"error": str(e)})
        else:
            self._json_response(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/dispatch":
            self._handle_dispatch()
        else:
            self._json_response(404, {"error": "not found"})

    def _handle_dispatch(self):
        # Verify API key if configured
        expected_key = os.environ.get("API_SECRET_KEY")
        if expected_key:
            auth = self.headers.get("Authorization", "")
            if auth != f"Bearer {expected_key}":
                self._json_response(401, {"error": "unauthorized"})
                return

        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}

            code = body.get("code", "")
            kind = body.get("kind", "python")
            hints = body.get("hints")

            if not code:
                self._json_response(400, {"error": "code field required"})
                return

            result = dispatch(code=code, kind=kind, hints=hints)
            self._json_response(200, result.to_dict())

        except Exception as e:
            traceback.print_exc()
            self._json_response(500, {"error": str(e)})

    def _json_response(self, status: int, data: dict):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Structured-ish logging to stderr
        sys.stderr.write(f"[dispatch] {args[0]} {args[1]} {args[2]}\n")


def main():
    port = int(os.environ.get("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), DispatchHandler)
    print(f"Sovereign Dispatch API listening on :{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()


if __name__ == "__main__":
    main()
