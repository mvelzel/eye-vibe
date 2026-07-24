#!/usr/bin/env python3
"""Run the frozen Earthquake irregular-row mask audit."""

from __future__ import annotations

import argparse
import random
from collections import Counter

from eye_mystery.earthquake_mask import (
    FINAL_STARTS,
    METRIC_NAMES,
    VARIANT_NAMES,
    conditional_anchor_shuffle,
    earthquake_mask_audit,
    metric_maxima,
    planted_mask_streams,
    score_variants,
)
from eye_mystery.gap_anchor import FINAL_MESSAGES, TARGET_GAP, clean_gap_anchors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=50_000)
    parser.add_argument("--seed", type=lambda text: int(text, 0), default=0x21E17)
    args = parser.parse_args()

    plant = planted_mask_streams()
    plant_scores = score_variants(plant)
    forward = plant_scores[0]
    print("plant")
    print(f"  forward-ones={forward}")
    print(f"  maxima={metric_maxima(plant_scores)}")
    if any(value < 1 for value in forward.values()):
        raise SystemExit("positive detector plant failed")

    plant_rng = random.Random(0x21A17)
    for name, start in zip(FINAL_MESSAGES, FINAL_STARTS, strict=True):
        shuffled, attempts = conditional_anchor_shuffle(
            plant[name],
            start=start,
            rng=plant_rng,
        )
        hits = clean_gap_anchors(
            shuffled,
            minimum_gap=TARGET_GAP,
            maximum_gap=TARGET_GAP,
        ).get(TARGET_GAP, ())
        if (
            Counter(shuffled) != Counter(plant[name])
            or any(left == right for left, right in zip(shuffled, shuffled[1:]))
            or len(hits) != 1
            or hits[0].position != start
            or hits[0].value != plant[name][start]
        ):
            raise SystemExit(f"{name} conditional shuffler plant failed")
        print(f"  {name} conditional-shuffle attempts={attempts}")

    audit = earthquake_mask_audit(controls=args.controls, seed=args.seed)
    print("real variants")
    for name, metrics in zip(VARIANT_NAMES, audit.real_variants, strict=True):
        print(f"  {name:13s} {metrics}")
    print("max-family results")
    for name, observed, hits, tail in zip(
        METRIC_NAMES,
        audit.real_maxima,
        audit.control_hits,
        audit.metric_tails,
        strict=True,
    ):
        print(
            f"  {name:31s} observed={observed} "
            f"hits={hits}/{audit.controls} tail={tail:.9f}"
        )
    print(
        f"  conditional_shuffle_attempts={audit.shuffle_attempts} "
        f"mean_per_stream="
        f"{audit.shuffle_attempts / (3 * audit.controls):.6f}"
    )
    print(f"  corrected_tail={audit.corrected_tail:.9f}")
    print(f"  passes={audit.passes}")


if __name__ == "__main__":
    main()
