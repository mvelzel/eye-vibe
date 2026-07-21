#!/usr/bin/env python3
"""Exhaust natural five-operation walks over the prime field F_83."""

from __future__ import annotations

from itertools import permutations

from eye_mystery.affine_walk import WalkResult, trace_affine_walk
from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER
from eye_mystery.metrics import index_of_coincidence


def main() -> None:
    orders = tuple(permutations(range(3)))
    results = []
    for generator in range(1, 83):
        for translation_pair in ((1, 3), (3, 1), (2, 4), (4, 2)):
            for center_mode in ("identity", "negation", "inversion", "reflection"):
                for up_order in orders:
                    for down_order in orders:
                        streams = [
                            trace_affine_walk(
                                MESSAGES[name],
                                generator,
                                translation_pair,
                                center_mode,
                                up_order,
                                down_order,
                            )
                            for name in MESSAGE_ORDER
                        ]
                        combined = tuple(value for stream in streams for value in stream)
                        unique = len(set(combined))
                        results.append(
                            WalkResult(
                                generator=generator,
                                translation_pair=translation_pair,
                                center_mode=center_mode,
                                up_order=up_order,
                                down_order=down_order,
                                unique=unique,
                                ioc=index_of_coincidence(combined, unique),
                            )
                        )

    print("Five-operation F_83 walks (few symbols, then high IoC):")
    print("gen +/- center     up down unique    IoC")
    for result in sorted(results, key=lambda item: (item.unique, -item.ioc))[:25]:
        print(
            f"{result.generator:>3} {result.translation_pair[0]}/{result.translation_pair[1]} "
            f"{result.center_mode:<10} "
            f"{''.join(str(i + 1) for i in result.up_order)} "
            f"{''.join(str(i + 1) for i in result.down_order)} "
            f"{result.unique:>6} {result.ioc:>6.3f}"
        )


if __name__ == "__main__":
    main()

