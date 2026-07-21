#!/usr/bin/env python3
"""Calibrate the fixed-coordinate snapshot/delta interpretation."""

from __future__ import annotations

import random
from itertools import combinations

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.snapshot_delta import (
    DEEPEST_EXIT_DEPTHS,
    DEEPEST_SIBLING_TRIOS,
    deepest_equality_geometry,
    deepest_sibling_gap_advantages,
    equality_runs,
)


def main() -> None:
    streams = {
        name: list(trigram_values(MESSAGES[name])[1:]) for name in MESSAGE_ORDER
    }
    observed_parts = deepest_sibling_gap_advantages(streams)
    observed = sum(observed_parts)
    observed_geometry = deepest_equality_geometry(streams)
    print(f"pairwise gap advantages      {observed_parts}")
    print(f"selected total              {observed}")
    for trio in DEEPEST_SIBLING_TRIOS:
        start = DEEPEST_EXIT_DEPTHS[trio[0]]
        for left, right in combinations(trio, 2):
            print(
                f"aligned equality runs {left:>5}/{right:<5} "
                f"{equality_runs(streams[left], streams[right], start=start)}"
            )

    randomizer = random.Random(20260721)
    trials = 2_000
    at_most = 0
    at_least_column_chi = 0
    at_least_edge_ends = 0
    for _ in range(trials):
        control = {name: values[:] for name, values in streams.items()}
        for name, depth in DEEPEST_EXIT_DEPTHS.items():
            # Preserve the complete prefix tree and the first unique exit edge.
            # Only positions after that independently selected edge are shuffled.
            start = depth + 1
            suffix = control[name][start:]
            randomizer.shuffle(suffix)
            control[name][start:] = suffix
        if sum(deepest_sibling_gap_advantages(control)) <= observed:
            at_most += 1
        geometry = deepest_equality_geometry(control)
        at_least_column_chi += geometry[1] >= observed_geometry[1]
        at_least_edge_ends += geometry[3] >= observed_geometry[3]
    print(f"prefix-tree null at most     {at_most}/{trials}")
    print(f"corrected lower tail         {(at_most + 1) / (trials + 1):.9f}")
    print(f"equality geometry            {observed_geometry}")
    print(
        "26-column chi upper tail    "
        f"{(at_least_column_chi + 1) / (trials + 1):.9f}"
    )
    print(
        "row-edge ends upper tail    "
        f"{(at_least_edge_ends + 1) / (trials + 1):.9f}"
    )


if __name__ == "__main__":
    main()
