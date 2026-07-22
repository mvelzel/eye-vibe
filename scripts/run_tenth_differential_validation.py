#!/usr/bin/env python3
"""Run the frozen independent validation of the mod-101 branch anomaly."""

from __future__ import annotations

import argparse
import random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.tenth_wide import (
    NONLITERAL_CONTEXTS,
    context_differential_score,
    context_mappings,
    shuffled_context_mappings_fixed_points,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=0xD1FF)
    args = parser.parse_args()
    if args.controls < 1:
        parser.error("--controls must be positive")

    streams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    mappings = context_mappings(streams, NONLITERAL_CONTEXTS)
    observed = context_differential_score(mappings, modulus=101)
    rng = random.Random(args.seed)
    controls = []
    for _ in range(args.controls):
        control = shuffled_context_mappings_fixed_points(mappings, rng)
        controls.append(
            context_differential_score(control, modulus=101).repeated_mass
        )
    hits = sum(value >= observed.repeated_mass for value in controls)
    print("fixed modulus: 101")
    print("edges:", observed.edges)
    print("per-map supports:", observed.per_map_support)
    print("summed support:", observed.summed_support)
    print("repeated mass:", observed.repeated_mass)
    print("control range:", min(controls), "..", max(controls))
    print(
        "corrected upper tail:",
        f"{hits + 1}/{args.controls + 1} = "
        f"{(hits + 1)/(args.controls + 1):.8f}",
    )


if __name__ == "__main__":
    main()
