#!/usr/bin/env python3
"""Report the two marker-derived message orders and their joint null."""

from __future__ import annotations

from math import factorial

from eye_mystery.marker_orders import (
    marker_order_composition_counts,
    marker_order_summary,
)


def main() -> None:
    summary = marker_order_summary()
    print("East-5-first edge trail:", summary["trail_order"])
    print("ascending (third, first, middle):", summary["trie_order"])
    print("all prefix clusters contiguous:", summary["trie_order_is_contiguous"])
    print("sorted third digits:", summary["third_digit_multiset"])
    print()
    counts = marker_order_composition_counts()
    total = factorial(9)
    print("event assignments/9! probability")
    for name, count in counts.items():
        print(f"{name:>22} {count:>7}/{total} {count / total:.10f}")


if __name__ == "__main__":
    main()
