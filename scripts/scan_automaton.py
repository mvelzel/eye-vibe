#!/usr/bin/env python3
"""Rank periodic readouts of the five-operation gear automaton."""

from __future__ import annotations

from itertools import permutations

from eye_mystery.automaton import ScanResult, readout_pattern, trace
from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER
from eye_mystery.metrics import adjacent_doubles, index_of_coincidence


def main() -> None:
    orders = tuple(permutations(range(3)))
    patterns = {
        "alternating top/bottom": (0, 1),
        "published top/bottom/top": (0, 1, 0),
    }
    results = {name: [] for name in patterns}
    for up_order in orders:
        for down_order in orders:
            traces = {
                name: trace(MESSAGES[name], up_order, down_order)
                for name in MESSAGE_ORDER
            }
            for up_slot in range(25):
                for down_slot in range(25):
                    for pattern_name, pattern in patterns.items():
                        slots = tuple(
                            up_slot if selector == 0 else down_slot
                            for selector in pattern
                        )
                        streams = [
                            readout_pattern(traces[name], slots)
                            for name in MESSAGE_ORDER
                        ]
                        combined = tuple(value for stream in streams for value in stream)
                        results[pattern_name].append(
                            ScanResult(
                                up_order=up_order,
                                down_order=down_order,
                                up_slot=up_slot,
                                down_slot=down_slot,
                                ioc=index_of_coincidence(combined, 25),
                                unique=len(set(combined)),
                                doubles=adjacent_doubles(streams),
                            )
                        )

    print("Top readouts across 36 triangular operation orders")
    print("(normalized IoC: uniform=1, English-like ~=1.7):")
    for pattern_name, pattern_results in results.items():
        print(f"\n{pattern_name}")
        print("up-order down-order up down    IoC unique doubles")
        for result in sorted(pattern_results, key=lambda item: item.ioc, reverse=True)[:20]:
            print(
                f"{''.join(str(i + 1) for i in result.up_order):>8} "
                f"{''.join(str(i + 1) for i in result.down_order):>10} "
                f"{result.up_slot + 1:>2} {result.down_slot + 1:>4}  "
                f"{result.ioc:>6.3f} {result.unique:>6} {result.doubles:>7}"
            )


if __name__ == "__main__":
    main()
