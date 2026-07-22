#!/usr/bin/env python3
"""Calibrate the frozen wide S6/body probe family."""

from __future__ import annotations

import argparse
from random import Random

from eye_mystery.factoradic_wide import (
    canonical_streams,
    moving_delimiter_scores,
    wide_scores,
)


def tail(observed: float, controls: list[float], *, lower: bool = False) -> tuple[int, int, float]:
    hits = sum(value <= observed if lower else value >= observed for value in controls)
    return 1 + hits, 1 + len(controls), (1 + hits) / (1 + len(controls))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=2_000)
    parser.add_argument("--seed", type=int, default=20260722)
    args = parser.parse_args()

    streams = canonical_streams()
    identity = list(range(83))
    observed = wide_scores(streams, identity)
    print("observed:", observed)
    print("moving delimiter:")
    for row in moving_delimiter_scores():
        print(" ", row)

    controls = []
    rng = Random(args.seed)
    for _ in range(args.trials):
        mapping = list(range(83))
        rng.shuffle(mapping)
        controls.append(wide_scores(streams, mapping))

    print(
        "A product/header upper:",
        tail(observed.product_header_matches, [row.product_header_matches for row in controls]),
    )
    print(
        "B quotient distinct lower:",
        tail(
            observed.quotients.minimum_distinct,
            [row.quotients.minimum_distinct for row in controls],
            lower=True,
        ),
    )
    print(
        "B quotient visible upper:",
        tail(observed.quotients.maximum_visible, [row.quotients.maximum_visible for row in controls]),
    )
    print(
        "B quotient P-group upper:",
        tail(
            observed.quotients.maximum_in_p_group,
            [row.quotients.maximum_in_p_group for row in controls],
        ),
    )
    print(
        "C running-state distinct lower:",
        tail(
            observed.running_state_distinct,
            [row.running_state_distinct for row in controls],
            lower=True,
        ),
    )
    print(
        "E header-coset matches upper:",
        tail(
            observed.cosets.maximum_header_matches,
            [row.cosets.maximum_header_matches for row in controls],
        ),
    )
    print(
        "E coset self-transition upper:",
        tail(
            observed.cosets.maximum_self_transitions,
            [row.cosets.maximum_self_transitions for row in controls],
        ),
    )
    print(
        "F cycle-type MI upper:",
        tail(observed.cycle_type_mi, [row.cycle_type_mi for row in controls]),
    )


if __name__ == "__main__":
    main()
