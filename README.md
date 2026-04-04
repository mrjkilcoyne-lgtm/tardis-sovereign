# tardis-sovereign

TARDIS Sovereign AI - LGM Server

## Sovereign Dispatch

Local-first code execution that looks remote but isn't. Cloud escalation only when the job demands it.

```python
from sovereign_dispatch import dispatch

result = dispatch("print('hello from the TARDIS')")
# Runs locally in ~13ms. Cached on repeat. $0 cost.

result = dispatch(heavy_ml_code, hints={"estimated_seconds": 60, "estimated_memory_mb": 2048})
# Auto-escalates to Google Cloud. Budget-tracked.
```

### Architecture

- **LocalDispatcher** - subprocess sandbox, resource-limited, ~13ms spin-up
- **CloudDispatcher** - GCP Cloud Functions (quick) / Cloud Run Jobs (heavy)
- **Router** - deterministic local-vs-cloud decision based on task hints
- **BudgetTracker** - SQLite ledger, daily/monthly spend guards
- **ResultCache** - content-addressed, zlib-compressed, LRU eviction
- **Compress** - payload compression, diff-only responses, deduplication

### Install

```bash
pip install -e .              # local only
pip install -e ".[cloud]"     # with GCP support
```

### Config

`config/default.yaml` ships sensible defaults. Override via `SOVEREIGN_CONFIG` env var or per-field with `SOVEREIGN_<SECTION>_<KEY>`.
