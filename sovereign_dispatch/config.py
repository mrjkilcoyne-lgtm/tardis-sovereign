"""Config loader. YAML + env overrides, frozen dataclass output."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

_DEFAULTS_PATH = Path(__file__).resolve().parent.parent / "config" / "default.yaml"


@dataclass(frozen=True)
class LocalConfig:
    timeout_seconds: int = 30
    max_memory_mb: int = 256
    max_concurrent: int = 4
    python_path: str | None = None


@dataclass(frozen=True)
class CloudConfig:
    provider: str = "gcp"
    project_id: str | None = None
    region: str = "us-central1"
    escalation_threshold_seconds: int = 10
    escalation_threshold_memory_mb: int = 512


@dataclass(frozen=True)
class BudgetConfig:
    max_daily_usd: float = 5.00
    max_monthly_usd: float = 50.00
    warn_at_percent: int = 80
    ledger_path: str = "~/.sovereign/ledger.db"


@dataclass(frozen=True)
class CacheConfig:
    enabled: bool = True
    db_path: str = "~/.sovereign/cache.db"
    max_size_mb: int = 256
    ttl_seconds: int = 3600


@dataclass(frozen=True)
class CompressConfig:
    diff_only: bool = True
    min_compress_bytes: int = 1024


@dataclass(frozen=True)
class Config:
    local: LocalConfig = field(default_factory=LocalConfig)
    cloud: CloudConfig = field(default_factory=CloudConfig)
    budget: BudgetConfig = field(default_factory=BudgetConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    compress: CompressConfig = field(default_factory=CompressConfig)


_SECTION_MAP = {
    "local": LocalConfig,
    "cloud": CloudConfig,
    "budget": BudgetConfig,
    "cache": CacheConfig,
    "compress": CompressConfig,
}


def _apply_env_overrides(raw: dict) -> dict:
    """SOVEREIGN_LOCAL_TIMEOUT_SECONDS=60 -> raw['local']['timeout_seconds']=60."""
    prefix = "SOVEREIGN_"
    for key, val in os.environ.items():
        if not key.startswith(prefix):
            continue
        parts = key[len(prefix):].lower().split("_", 1)
        if len(parts) != 2 or parts[0] not in raw:
            continue
        section, field_name = parts
        raw.setdefault(section, {})[field_name] = val
    return raw


def _coerce(cls, raw_section: dict) -> object:
    """Build a frozen dataclass, coercing string env values to proper types."""
    hints = cls.__dataclass_fields__
    coerced = {}
    for k, v in raw_section.items():
        if k not in hints:
            continue
        target = hints[k].type
        if isinstance(v, str):
            if target in ("int", int):
                v = int(v)
            elif target in ("float", float):
                v = float(v)
            elif target in ("bool", bool):
                v = v.lower() in ("true", "1", "yes")
        coerced[k] = v
    return cls(**coerced)


def load_config(config_path: str | None = None) -> Config:
    """Load config: defaults -> user YAML -> env overrides."""
    raw: dict = {}

    # 1. Baked-in defaults
    if _DEFAULTS_PATH.exists():
        with open(_DEFAULTS_PATH) as f:
            raw = yaml.safe_load(f) or {}

    # 2. User override file
    user_path = config_path or os.environ.get("SOVEREIGN_CONFIG")
    if user_path:
        p = Path(user_path).expanduser()
        if p.exists():
            with open(p) as f:
                user_raw = yaml.safe_load(f) or {}
            for section, vals in user_raw.items():
                if isinstance(vals, dict):
                    raw.setdefault(section, {}).update(vals)

    # 3. Environment variable overrides
    raw = _apply_env_overrides(raw)

    # 4. Build frozen config
    sections = {}
    for name, cls in _SECTION_MAP.items():
        sections[name] = _coerce(cls, raw.get(name, {}))
    return Config(**sections)
