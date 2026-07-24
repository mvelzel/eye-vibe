#!/usr/bin/env python3
"""Run the frozen circle-authored base-permutation audit for Cipher #6."""

from __future__ import annotations

from pathlib import Path

from eye_mystery.practice_cipher6 import (
    circle_base_permutation_audit,
    circle_base_permutations,
    read_ciphertext,
    render_line,
)


ROOT = Path(__file__).resolve().parents[1]
CIPHERTEXT = ROOT / "artifacts/practice-sdlwdr/cipher6-revised.txt"


def main() -> None:
    lines = read_ciphertext(CIPHERTEXT)
    bases = circle_base_permutations()
    results = circle_base_permutation_audit(lines)

    print(f"unique-bases={len(bases)} candidates={len(results)}")
    print("prefix low/total fraction distinct max mode base")
    for result in results[:20]:
        print(
            f"{result.prefix_matches:>6} "
            f"{result.low_rank_count:>3}/{result.total:<3} "
            f"{result.low_rank_fraction:.6f} "
            f"{result.distinct:>8} {result.maximum:>3} "
            f"{result.exponent_mode:<6} {result.base}"
        )
        print("  natural:", render_line(result.decoded[0])[:100])
        print("  altar:  ", render_line(result.decoded[0], altar=True)[:100])


if __name__ == "__main__":
    main()
