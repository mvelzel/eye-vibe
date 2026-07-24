#!/usr/bin/env python3
"""Run the frozen altar-valued asset-tape cut audit for Cipher #6."""

from __future__ import annotations

from pathlib import Path

from eye_mystery.practice_cipher6 import (
    read_ciphertext,
    render_line,
    tape_value_cut_audit,
)


ROOT = Path(__file__).resolve().parents[1]
CIPHERTEXT = ROOT / "artifacts/practice-sdlwdr/cipher6-revised.txt"


def main() -> None:
    results = tape_value_cut_audit(read_ciphertext(CIPHERTEXT))

    print(f"candidates={len(results)}")
    print("prefix low/total fraction distinct max binary alphabet symbols base cut")
    for result in results:
        symbols = "append" if result.appended_nonletters else "literal"
        base = "one" if result.one_based else "zero"
        print(
            f"{result.prefix_matches:>6} "
            f"{result.low_rank_count:>3}/{result.total:<3} "
            f"{result.low_rank_fraction:.6f} "
            f"{result.distinct:>8} {result.maximum:>3} "
            f"{result.binary_direction:<3} {result.alphabet:<10} "
            f"{symbols:<7} {base:<4} {result.cut_direction}"
        )
        print("  natural:", render_line(result.decoded[0])[:100])
        print("  altar:  ", render_line(result.decoded[0], altar=True)[:100])


if __name__ == "__main__":
    main()
