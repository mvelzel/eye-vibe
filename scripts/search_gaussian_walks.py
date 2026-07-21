#!/usr/bin/env python3
"""Exhaust natural ``0, ±1, ±i`` walks over ``F_83[i]``."""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from itertools import permutations

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER
from eye_mystery.gaussian_walk import trace_gaussian_walk
from eye_mystery.metrics import index_of_coincidence


@dataclass(frozen=True)
class Result:
    center: str
    observation: str
    initial: tuple[int, int]
    up_order: tuple[int, int, int]
    down_order: tuple[int, int, int]
    marker_mode: str
    mismatches: int
    comparisons: int
    unique: int
    ioc: float

    @property
    def key(self):
        return self.mismatches, self.unique, -self.ioc


def mismatch_count(streams) -> tuple[int, int]:
    comparisons = []

    def compare(anchor_name, anchor_start, other_name, other_start, length):
        comparisons.append(
            (
                streams[anchor_name][anchor_start : anchor_start + length],
                streams[other_name][other_start : other_start + length],
            )
        )

    for anchor, others, length in (
        ("east1", ("west1", "east2"), 24),
        ("west2", ("east3", "west3"), 5),
        ("east4", ("west4", "east5"), 20),
    ):
        for other in others:
            compare(anchor, 1, other, 1, length)
    for other_name, other_start in (
        ("west1", 64),
        ("east2", 39),
        ("east2", 74),
    ):
        compare("west1", 34, other_name, other_start, 18)
    for other_start in (40, 68):
        compare("west1", 40, "east1", other_start, 9)
    for other_name, other_start in (("west4", 71), ("east5", 69)):
        compare("east4", 68, other_name, other_start, 30)
    total = sum(len(left) for left, _ in comparisons)
    mismatches = sum(
        left_value != right_value
        for left, right in comparisons
        for left_value, right_value in zip(left, right, strict=True)
    )
    return mismatches, total


def main() -> None:
    orders = tuple(permutations(range(3)))
    best = []
    serial = 0
    tested = 0
    for center in (
        "identity",
        "negation",
        "conjugation",
        "inversion",
        "rotate-left",
        "rotate-right",
    ):
        for observation in (
            "state",
            "real",
            "imaginary",
            "norm",
            "slope",
            "unit-phase",
        ):
            for initial in ((0, 0), (1, 0), (0, 1), (1, 1)):
                for up_order in orders:
                    for down_order in orders:
                        for reset_marker in (False, True):
                            streams = {}
                            for name in MESSAGE_ORDER:
                                raw = MESSAGES[name]
                                if reset_marker:
                                    streams[name] = (None,) + trace_gaussian_walk(
                                        raw[3:],
                                        center_mode=center,
                                        observation=observation,
                                        up_order=up_order,
                                        down_order=down_order,
                                        initial=initial,
                                    )
                                else:
                                    streams[name] = trace_gaussian_walk(
                                        raw,
                                        center_mode=center,
                                        observation=observation,
                                        up_order=up_order,
                                        down_order=down_order,
                                        initial=initial,
                                    )
                            combined = tuple(
                                value
                                for stream in streams.values()
                                for value in stream[1 if reset_marker else 0 :]
                            )
                            unique = len(set(combined))
                            mismatches, comparisons = mismatch_count(streams)
                            result = Result(
                                center,
                                observation,
                                initial,
                                up_order,
                                down_order,
                                "reset" if reset_marker else "full",
                                mismatches,
                                comparisons,
                                unique,
                                index_of_coincidence(combined, unique),
                            )
                            item = (
                                tuple(-value for value in result.key),
                                serial,
                                result,
                            )
                            serial += 1
                            tested += 1
                            if len(best) < 40:
                                heapq.heappush(best, item)
                            elif item > best[0]:
                                heapq.heapreplace(best, item)

    print(f"tested={tested}")
    print("mismatch unique ioc marker center observation initial up down")
    for _, _, result in sorted(best, key=lambda item: item[2].key):
        print(
            f"{result.mismatches:>8}/{result.comparisons:<3} "
            f"{result.unique:>6} {result.ioc:>6.3f} "
            f"{result.marker_mode:<5} {result.center:<12} "
            f"{result.observation:<10} {result.initial!s:<7} "
            f"{''.join(str(i + 1) for i in result.up_order)} "
            f"{''.join(str(i + 1) for i in result.down_order)}"
        )


if __name__ == "__main__":
    main()
