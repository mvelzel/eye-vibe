#!/usr/bin/env python3
"""Audit the five-frame Eye glyph atlas in a Noita PE executable."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "src"))

from eye_mystery.compiled_eye_atlas import (  # noqa: E402
    ADD_MASK,
    OBFUSCATED_WORDS,
    XOR_MASK,
    atlas_frames,
    decode_words,
    render_frame,
)


def occurrences(data: bytes, pattern: bytes) -> int:
    count = 0
    start = 0
    while True:
        offset = data.find(pattern, start)
        if offset < 0:
            return count
        count += 1
        start = offset + 1


def binary_signature(data: bytes) -> dict[str, int]:
    """Count the exact immediate signatures from the compiled method."""
    counts: dict[str, int] = {}
    locations = ((b"\xc7\x06", b"\xc7\x46\x04"),) + tuple(
        (b"\xc7\x46" + bytes((offset,)), b"\xc7\x46" + bytes((offset + 4,)))
        for offset in (8, 16, 24, 32)
    )
    for index, word in enumerate(OBFUSCATED_WORDS):
        low = word & 0xFFFFFFFF
        high = word >> 32
        counts[f"word_{index}_low"] = occurrences(
            data, locations[index][0] + low.to_bytes(4, "little")
        )
        counts[f"word_{index}_high"] = occurrences(
            data, locations[index][1] + high.to_bytes(4, "little")
        )
    counts["xor_low"] = occurrences(
        data, b"\x81\x34\xc6" + (XOR_MASK & 0xFFFFFFFF).to_bytes(4, "little")
    )
    counts["xor_high"] = occurrences(
        data, b"\x81\x74\xc6\x04" + (XOR_MASK >> 32).to_bytes(4, "little")
    )
    counts["add_low"] = occurrences(
        data, b"\x81\x06" + (ADD_MASK & 0xFFFFFFFF).to_bytes(4, "little")
    )
    counts["add_high"] = occurrences(
        data, b"\x81\x56\x04" + (ADD_MASK >> 32).to_bytes(4, "little")
    )
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("executable", type=Path)
    args = parser.parse_args()
    data = args.executable.read_bytes()
    counts = binary_signature(data)
    print(f"path={args.executable}")
    print(f"bytes={len(data)} sha256={hashlib.sha256(data).hexdigest()}")
    print("signature_counts=" + " ".join(f"{key}:{value}" for key, value in counts.items()))
    print(f"decoded_words={[f'{word:016x}' for word in decode_words()]}")
    for index, frame in enumerate(atlas_frames()):
        print(f"frame_{index}")
        print(render_frame(frame))
    if not all(value >= 1 for value in counts.values()):
        raise SystemExit("one or more atlas signatures were absent")


if __name__ == "__main__":
    main()
