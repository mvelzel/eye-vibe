#!/usr/bin/env python3
"""Audit header-ordered no-repeat conditional ranks."""

from eye_mystery.header_no_repeat import (
    ROUTES,
    audit_header_no_repeat,
    score_route,
)


def main() -> None:
    print("real conditional-rank route scores:")
    for route in ROUTES:
        score = score_route(route)
        print(
            f"  {route}: magnitude train={score.training_magnitude}/"
            f"{score.training_transitions} holdout={score.holdout_magnitude}/"
            f"{score.holdout_transitions} sheet_xor="
            f"{score.selected_sheet_xor} sheet_holdout="
            f"{score.holdout_sheet_matches}/{score.holdout_transitions} "
            f"full_holdout={score.holdout_full_agreements}/"
            f"{score.holdout_transitions}"
        )
        for context in (*score.training, *score.holdout):
            print(
                f"    {context.name}: magnitude="
                f"{context.magnitude_agreements}/{context.transitions} "
                f"full={context.full_agreements}/{context.transitions} "
                f"sheet_equal={context.sheet_equal}/{context.transitions}"
            )

    audit = audit_header_no_repeat()
    observed = audit.observed
    print(
        f"selected={observed.route} "
        f"train={observed.training_magnitude}/"
        f"{observed.training_transitions} "
        f"holdout={observed.holdout_magnitude}/"
        f"{observed.holdout_transitions}"
    )
    print(
        f"magnitude_tail={audit.magnitude_tail_count}/{audit.control_count}="
        f"{audit.magnitude_tail:.9f} "
        f"control_max={audit.maximum_control_magnitude}"
    )
    print(
        f"full_tail={audit.full_tail_count}/{audit.control_count}="
        f"{audit.full_tail:.9f}"
    )
    print("magnitude histogram:")
    for score, count in audit.magnitude_histogram:
        print(f"  {score}: {count}")


if __name__ == "__main__":
    main()
