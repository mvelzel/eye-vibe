#!/usr/bin/env python3
"""Verify the 2025 Noita Eye initializer against the visible corpus.

This is a read-only binary audit.  The virtual-address interval is frozen from
the public candidate-function report and ends immediately before its shared
zero-high-half block.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "src"))

from eye_mystery.binary_initializer import (  # noqa: E402
    HIGH_HALF_STORE,
    LOW_HALF_STORE,
    expected_initializer_halves,
    matches_eye_initializer,
    stack_immediates,
)
from eye_mystery.storage_serialization import (  # noqa: E402
    corpus_packed_words,
    packed_words_sha256,
)

from audit_noita_binary import parse_pe  # noqa: E402


DEFAULT_START_VA = 0x0061ED60
DEFAULT_END_VA = 0x0061FCDC


def va_slice(data: bytes, start_va: int, end_va: int) -> bytes:
    """Return one PE virtual-address interval from its raw section bytes."""
    image = parse_pe(data)
    for section in image.sections:
        section_start = image.image_base + section.virtual_address
        section_end = section_start + section.raw_size
        if section_start <= start_va <= end_va <= section_end:
            raw_start = section.raw_offset + start_va - section_start
            raw_end = section.raw_offset + end_va - section_start
            return data[raw_start:raw_end]
    raise ValueError("virtual-address interval is not contained in one PE section")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("executable", type=Path)
    parser.add_argument("--start-va", type=lambda value: int(value, 0), default=DEFAULT_START_VA)
    parser.add_argument("--end-va", type=lambda value: int(value, 0), default=DEFAULT_END_VA)
    args = parser.parse_args()

    data = args.executable.read_bytes()
    code = va_slice(data, args.start_va, args.end_va)
    shared_zero_store = va_slice(data, args.end_va, args.end_va + 7)
    words = corpus_packed_words()
    expected_lows, expected_highs = expected_initializer_halves(words)
    observed_lows = stack_immediates(code, LOW_HALF_STORE)
    observed_highs = stack_immediates(code, HIGH_HALF_STORE)
    zero_high_words = sum(word >> 32 == 0 for word in words)
    zero_store_exact = shared_zero_store == HIGH_HALF_STORE + b"\0\0\0\0"
    exact = (
        matches_eye_initializer(code, words)
        and zero_high_words == 4
        and zero_store_exact
    )

    print(f"binary_sha256={hashlib.sha256(data).hexdigest()}")
    print(f"va_interval=0x{args.start_va:08x}..0x{args.end_va:08x}")
    print(f"packed_words={len(words)} packed_sha256={packed_words_sha256(words)}")
    print(
        f"low_halves={len(observed_lows)}/{len(expected_lows)} "
        f"exact={observed_lows == expected_lows}"
    )
    print(
        f"nonzero_high_halves={len(observed_highs)}/{len(expected_highs)} "
        f"exact={observed_highs == expected_highs}"
    )
    print(
        f"zero_high_words={zero_high_words} "
        f"shared_zero_store_exact={zero_store_exact}"
    )
    print(f"exact_initializer={exact}")
    if not exact:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
