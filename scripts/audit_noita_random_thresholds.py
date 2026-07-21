#!/usr/bin/env python3
"""Inventory Noita's direct ``Random(0,100)`` Lua thresholds."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from eye_mystery.random_thresholds import (
    RandomThresholdHit,
    scan_directory_thresholds,
    scan_wak_thresholds,
    successful_outcomes,
)
from eye_mystery.wak import WakArchive


def report(label: str, hits: tuple[RandomThresholdHit, ...]) -> None:
    frequencies = Counter((hit.operator, hit.threshold) for hit in hits)
    print(label)
    print("  comparisons:", len(hits))
    print("  distinct operator/threshold pairs:", len(frequencies))
    print("  threshold histogram:")
    for (operator, threshold), count in sorted(
        frequencies.items(), key=lambda item: (item[0][1], item[0][0])
    ):
        print(f"    {operator:>2} {threshold:>3}: {count}")
    selected = tuple(
        hit for hit in hits if hit.operator == "<" and hit.threshold == 83
    )
    print("  exact Random(0,100) < 83 hits:", len(selected))
    for hit in selected:
        print(f"    {hit.path}+0x{hit.offset:x}")
    outcomes = successful_outcomes("<", 83)
    excluded = tuple(value for value in range(101) if value not in outcomes)
    print(
        "  exact outcome set:",
        f"{outcomes[0]}..{outcomes[-1]}",
        f"({len(outcomes)}/101)",
    )
    print(
        "  complementary outcome set:",
        f"{excluded[0]}..{excluded[-1]}",
        f"({len(excluded)}/101)",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path, help="installed Noita data.wak")
    parser.add_argument(
        "--loose-tree",
        type=Path,
        help="optional historical unpacked Noita data directory",
    )
    args = parser.parse_args()

    report("current WAK", scan_wak_thresholds(WakArchive.open(args.archive)))
    if args.loose_tree is not None:
        report("historical loose tree", scan_directory_thresholds(args.loose_tree))


if __name__ == "__main__":
    main()
