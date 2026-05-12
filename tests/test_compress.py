"""Tests for compression and diffing."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sovereign_dispatch.compress import (
    compress,
    content_hash,
    decompress,
)


def test_content_hash_stable():
    h1 = content_hash("print(1)")
    h2 = content_hash("print(1)")
    assert h1 == h2
    assert len(h1) == 16


def test_content_hash_with_payload():
    h1 = content_hash("x", b"data1")
    h2 = content_hash("x", b"data2")
    assert h1 != h2


def test_compress_small_passthrough():
    data = b"tiny"
    out, enc = compress(data, min_bytes=1024)
    assert enc == "raw"
    assert out == data


def test_compress_large():
    data = b"x" * 10000
    out, enc = compress(data, min_bytes=100)
    assert enc == "zlib"
    assert len(out) < len(data)


def test_roundtrip():
    data = b"hello world " * 1000
    compressed, enc = compress(data, min_bytes=100)
    restored = decompress(compressed, enc)
    assert restored == data
