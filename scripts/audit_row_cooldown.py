#!/usr/bin/env python3
"""Run the frozen physical-row recurrence cooldown audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from eye_mystery.fifteenth_second import trimmed_eye_words
from eye_mystery.practice_cipher4 import cyclic_differences
from eye_mystery.row_cooldown import (
    PANEL_ORDER,
    CooldownNull,
    audit_cooldowns,
    minimum_recurrence_distance,
    planted_cooldown_words,
    registered_context_fixed_positions,
    run_cooldown_null,
)

ROOT = Path(__file__).resolve().parents[1]


def print_null(label: str, result: CooldownNull) -> None:
    print(label)
    for name in (
        "trials",
        "exact_vector",
        "exact_tail",
        "row_uniform",
        "uniform_tail",
        "row_uniform_distinct",
        "uniform_distinct_tail",
        "split_prediction",
        "split_tail",
    ):
        print(f"  {name}: {getattr(result, name)}")


def practice_inventory() -> None:
    cipher3 = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher3.json").read_text()
    )
    print("practice cipher 3 marker-stripped minima")
    for group in ("A", "B", "C"):
        minima = tuple(
            minimum_recurrence_distance(stream[1:])
            for stream in cipher3[group]
        )
        print(f"  {group}: {minima}")

    cipher4 = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher4.json").read_text()
    )
    print("practice cipher 4 minima")
    print(
        "  raw:",
        tuple(minimum_recurrence_distance(stream) for stream in cipher4),
    )
    print(
        "  cyclic differences:",
        tuple(
            minimum_recurrence_distance(cyclic_differences(stream))
            for stream in cipher4
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=100_000)
    args = parser.parse_args()

    control = audit_cooldowns(planted_cooldown_words())
    print("positive control minima:", control.minima)
    if control.minima != (3, 3, 3, 2, 2, 2, 4, 4, 4):
        raise SystemExit("positive control failed")

    observed = audit_cooldowns()
    print("observed minima:", observed.minima)
    print("row minima:", observed.row_minima)
    print("row uniform:", observed.row_uniform)
    print("row uniform distinct:", observed.row_uniform_distinct)
    print("first-half minima:", observed.first_half_minima)
    print("second-half minima:", observed.second_half_minima)
    print("split thresholds:", observed.split_prediction.thresholds)
    print("split passes:", observed.split_prediction.passes)
    print("lag counts")
    for name, counts in zip(
        PANEL_ORDER,
        observed.lag_counts,
        strict=True,
    ):
        print(f"  {name}: {counts}")

    fixed = registered_context_fixed_positions()
    words = trimmed_eye_words()
    print(
        "registered fixed/free:",
        tuple(
            (name, len(fixed[name]), len(words[name]) - len(fixed[name]))
            for name in PANEL_ORDER
        ),
    )

    null_a = run_cooldown_null(
        trials=args.trials,
        seed=0xC001D04,
        freeze_registered_contexts=False,
    )
    print_null("null A: multiset + no-double", null_a)
    null_b = run_cooldown_null(
        trials=args.trials,
        seed=0xC001D05,
        freeze_registered_contexts=True,
    )
    print_null("null B: registered contexts fixed", null_b)
    practice_inventory()


if __name__ == "__main__":
    main()
