"""GCP auth. Thin wrapper. Caches credentials, handles refresh."""

from __future__ import annotations


class GCPAuth:
    """Lazy-loaded Google Cloud credentials."""

    def __init__(self, project_id: str | None = None):
        self._project_id = project_id
        self._credentials = None

    @property
    def credentials(self):
        if self._credentials is None:
            self._credentials, project = self._load()
            if not self._project_id:
                self._project_id = project
        return self._credentials

    @property
    def project_id(self) -> str:
        if not self._project_id:
            _ = self.credentials  # triggers load
        if not self._project_id:
            raise RuntimeError(
                "No GCP project_id configured. Set cloud.project_id in config "
                "or run: gcloud auth application-default login"
            )
        return self._project_id

    def _load(self):
        try:
            import google.auth
            return google.auth.default(
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        except ImportError:
            raise RuntimeError(
                "GCP dependencies not installed. Run: "
                "pip install sovereign-dispatch[cloud]"
            )
        except Exception as e:
            raise RuntimeError(
                f"GCP auth failed: {e}\n"
                "Run: gcloud auth application-default login"
            )
