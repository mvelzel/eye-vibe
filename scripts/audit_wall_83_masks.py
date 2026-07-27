#!/usr/bin/env python3
"""Test the exact 83-entry Wall masks against canonical Eye structure."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from eye_mystery.noita_wall_messages import load_wall_message_lines
from eye_mystery.wall_83_masks import (
    THAT_WHICH_WINDOWS,
    hamming_up_to_complement,
    score_mask_on_windows,
    simple_base5_masks,
    wall_masks,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("surface_text", type=Path)
    parser.add_argument("--trials", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=0x83_515)
    args = parser.parse_args()

    lines_by_id = dict(load_wall_message_lines(args.surface_text))
    masks = wall_masks(lines_by_id)
    simple = simple_base5_masks()
    print(f"masks={len(masks)}")
    observed_scores = []
    for mask in masks:
        score = score_mask_on_windows(mask)
        observed_scores.append(score.agreements)
        closest_name, closest_distance = min(
            (
                (name, hamming_up_to_complement(mask.bits, candidate))
                for name, candidate in simple.items()
            ),
            key=lambda item: item[1],
        )
        print(
            f"{mask.name:<44} weight={mask.weight:>2} "
            f"window_agreement={score.agreements:>3}/{score.comparisons} "
            f"common={score.exact_common_tape} "
            f"closest={closest_name}:{closest_distance}"
        )
        for (window_name, _), tape in zip(
            THAT_WHICH_WINDOWS,
            score.tapes,
            strict=True,
        ):
            print(f"  {window_name:<9} {''.join(map(str, tape))}")

    observed_max = max(observed_scores)
    generator = random.Random(args.seed)
    exceed = 0
    for _ in range(args.trials):
        control_scores = []
        for mask in masks:
            shuffled = list(mask.bits)
            generator.shuffle(shuffled)
            control_scores.append(
                score_mask_on_windows(
                    type(mask)(mask.name, tuple(shuffled))
                ).agreements
            )
        exceed += max(control_scores) >= observed_max
    print(
        f"family_max={observed_max} trials={args.trials} "
        f"corrected_tail={(exceed + 1) / (args.trials + 1):.8f}"
    )


if __name__ == "__main__":
    main()
