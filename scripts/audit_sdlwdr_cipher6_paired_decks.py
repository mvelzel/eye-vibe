#!/usr/bin/env python3
"""Run the frozen paired-rotating-deck audit for Practice Cipher #6."""

from __future__ import annotations

from pathlib import Path

from eye_mystery.practice_cipher6 import (
    EXPECTED_PREFIXES,
    paired_deck_audit,
    read_ciphertext,
    render_line,
)


ROOT = Path(__file__).resolve().parents[1]
CIPHERTEXT = ROOT / "artifacts/practice-sdlwdr/cipher6-revised.txt"


def main() -> None:
    lines = read_ciphertext(CIPHERTEXT)
    results = paired_deck_audit(lines)
    passing = [result for result in results if result.prefix_matches == len(EXPECTED_PREFIXES)]

    print(f"candidates={len(results)} prefix-complete={len(passing)}")
    print("prefix low/total fraction distinct max nadir left right")
    for result in results[:20]:
        print(
            f"{result.prefix_matches:>6} "
            f"{result.low_rank_count:>3}/{result.total:<3} "
            f"{result.low_rank_fraction:.6f} "
            f"{result.distinct:>8} {result.maximum:>3} "
            f"{result.nadir:>5} {result.left:<16} {result.right}"
        )
        print("  natural:", render_line(result.decoded[0])[:100])
        print("  altar:  ", render_line(result.decoded[0], altar=True)[:100])


if __name__ == "__main__":
    main()

