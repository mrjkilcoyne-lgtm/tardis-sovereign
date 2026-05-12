"""Compression, diffing, deduplication. Every byte counts."""

from __future__ import annotations

import difflib
import hashlib
import zlib


def content_hash(code: str, payload: bytes | None = None) -> str:
    """Content-addressed key. Same input = same hash = cache hit."""
    h = hashlib.sha256(code.encode())
    if payload:
        h.update(payload)
    return h.hexdigest()[:16]


def compress(data: bytes, min_bytes: int = 1024) -> tuple[bytes, str]:
    """Compress if worth it. Returns (data, encoding)."""
    if len(data) < min_bytes:
        return data, "raw"
    compressed = zlib.compress(data, level=6)
    if len(compressed) >= len(data):
        return data, "raw"  # compression made it bigger
    return compressed, "zlib"


def decompress(data: bytes, encoding: str) -> bytes:
    if encoding == "zlib":
        return zlib.decompress(data)
    return data


def compute_diff(old: str, new: str) -> str | None:
    """Unified diff. Returns None if identical."""
    if old == new:
        return None
    diff = difflib.unified_diff(
        old.splitlines(keepends=True),
        new.splitlines(keepends=True),
        n=0,  # zero context lines - maximum density
    )
    result = "".join(diff)
    # Only use diff if it's actually smaller
    if len(result) >= len(new):
        return None
    return result


def apply_diff(old: str, diff_text: str) -> str:
    """Apply a unified diff to reconstruct new text.
    Simple line-level patch for our zero-context diffs.
    """
    old_lines = old.splitlines(keepends=True)
    diff_lines = diff_text.splitlines(keepends=True)
    result = list(old_lines)
    offset = 0

    for line in diff_lines:
        if line.startswith("@@"):
            # Parse @@ -start,count +start,count @@
            parts = line.split()
            old_spec = parts[1]  # -start,count
            start = abs(int(old_spec.split(",")[0])) - 1
            offset = start
        elif line.startswith("-") and not line.startswith("---"):
            if offset < len(result):
                result.pop(offset)
        elif line.startswith("+") and not line.startswith("+++"):
            result.insert(offset, line[1:])
            offset += 1

    return "".join(result)
