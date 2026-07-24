#!/usr/bin/env python3
"""Run exact range screens from practice cipher 3's first wide batch."""

from __future__ import annotations

from eye_mystery.practice_cipher3_wide import (
    EXCEPTIONAL_RAW,
    GROUPS,
    load_cipher3,
    physical_transfer_scores,
    recursive_transfer_scores,
    select_fixed_drift,
)


def main() -> None:
    streams = load_cipher3()
    print("input")
    print(
        "  lengths=",
        {
            group: tuple(map(len, streams[group]))
            for group in GROUPS
        },
    )
    print(
        "  J-counts=",
        {
            group: sum(
                symbol == EXCEPTIONAL_RAW
                for message in streams[group]
                for symbol in message
            )
            for group in GROUPS
        },
    )

    print("C. fixed coordinate drift")
    drift = select_fixed_drift(streams)
    print(
        f"  selected-on-A={drift.coordinate_system} "
        f"direction={drift.direction:+d} step={drift.step}; "
        f"unique A/B/C={drift.training_unique}/"
        f"{drift.heldout_b_unique}/{drift.heldout_c_unique}; "
        f"events A/B/C={drift.training_events}/"
        f"{drift.heldout_b_events}/{drift.heldout_c_events}"
    )

    print("D. named physical deck updates")
    physical = physical_transfer_scores(streams)
    for score in physical:
        print(
            f"  {score.action:<15} {score.marker_mode:<4} "
            f"A outside/unique/max={score.training_outside_42}/"
            f"{score.training_unique}/{score.training_maximum}; "
            f"B={score.heldout_b_outside_42}/"
            f"{score.heldout_b_unique}/{score.heldout_b_maximum}; "
            f"C={score.heldout_c_outside_42}/"
            f"{score.heldout_c_unique}/{score.heldout_c_maximum}; "
            f"base={score.base}"
        )
    winner = min(
        physical,
        key=lambda score: (
            score.training_outside_42,
            score.training_unique,
            score.training_maximum,
            score.action,
            score.marker_mode,
            score.base,
        ),
    )
    print("  selected-on-A:", winner)

    print("E. cipher-5 recursive-operation transfer")
    recursive = tuple(
        score for score in recursive_transfer_scores(streams) if score.valid
    )
    for score in sorted(
        recursive,
        key=lambda item: (
            item.training_outside_42,
            item.training_unique,
            item.initial_deck,
            item.marker_mode,
            item.update_timing,
        ),
    )[:8]:
        print(" ", score)
    print(
        f"  valid={len(recursive)}/24; "
        f"exact-range={sum(score.training_outside_42 == 0 and score.heldout_b_outside_42 == 0 and score.heldout_c_outside_42 == 0 for score in recursive)}"
    )


if __name__ == "__main__":
    main()
