#!/usr/bin/env python3
"""Audit the proposed mirror-width structure in giant_dollar.png."""

from __future__ import annotations

import argparse
from pathlib import Path

from eye_mystery.giant_dollar import (
    always_opaque_columns,
    best_comparisons,
    centre_run_widths,
    compare_windows,
    dimensions,
    file_sha256,
    load_alpha_mask,
    scan_windows,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument(
        "--early-image",
        type=Path,
        help="optional historical copy for a byte-level chronology check",
    )
    args = parser.parse_args()

    alpha = load_alpha_mask(args.image)
    left, right = centre_run_widths(alpha)
    print("asset:", args.image)
    print("sha256:", file_sha256(args.image))
    print("dimensions:", dimensions(alpha))
    print("always-opaque columns:", always_opaque_columns(alpha))
    opaque = sum(map(sum, alpha))
    print(
        "opaque/transparent:",
        opaque,
        sum(len(row) for row in alpha) - opaque,
    )

    if args.early_image:
        print("early asset:", args.early_image)
        print("early sha256:", file_sha256(args.early_image))
        print(
            "byte-identical:",
            args.image.read_bytes() == args.early_image.read_bytes(),
        )

    comparisons = scan_windows(left, right, length=43)
    best = best_comparisons(comparisons)
    print("\nall 43-row alignments:", len(comparisons))
    print(
        "best score:",
        f"{best[0].equal_rows}/43 equal,",
        f"absolute difference {best[0].absolute_difference},",
        f"ties {len(best)}",
    )
    print("best (left-start, right-start, reverse, mismatches):")
    for comparison in best:
        print(
            " ",
            comparison.left_start,
            comparison.right_start,
            comparison.right_reversed,
            comparison.mismatches,
        )

    advertised = compare_windows(
        left,
        right,
        left_start=12,
        right_start=15,
        length=43,
        right_reversed=True,
    )
    print("\nadvertised 43-row crop:", advertised)
    if advertised.mismatches:
        index, left_width, right_width = advertised.mismatches[0]
        print(
            "first mismatch, one-based scanline/widths:",
            index + 1,
            left_width,
            right_width,
        )

    sixty = compare_windows(
        left,
        right,
        left_start=5,
        right_start=5,
        length=60,
        right_reversed=True,
    )
    print("60-row containing relation:", sixty)


if __name__ == "__main__":
    main()
