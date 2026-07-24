#!/usr/bin/env python3
"""Run the frozen final-row gap-anchor/header audit."""

from eye_mystery.gap_anchor import (
    FINAL_HEADERS,
    any_broad_gap_match,
    exact_reported_relation,
    gap_anchor_audit,
    planted_gap_streams,
    unique_anchor_values,
)


def main() -> None:
    plant = planted_gap_streams()
    plant_anchors = unique_anchor_values(plant, 11)
    print(
        "plant",
        f"anchors={plant_anchors}",
        f"exact={exact_reported_relation(plant_anchors or ())}",
        f"broad={any_broad_gap_match(plant)}",
    )
    if (
        plant_anchors is None
        or not exact_reported_relation(plant_anchors)
        or any_broad_gap_match(plant) is None
    ):
        raise SystemExit("positive detector control failed")

    audit = gap_anchor_audit()
    print("real")
    print(f"  positions={audit.real_positions}")
    print(f"  anchors={audit.real_anchors}")
    print(f"  headers={FINAL_HEADERS}")
    print(f"  predicted_nonreference={audit.predicted_nonreference}")
    print(
        f"  targeted_structure_controls="
        f"{audit.targeted_structure_controls}/{audit.controls}"
    )
    print(
        f"  targeted_relation_tail="
        f"({1 + audit.targeted_relation_controls}/{1 + audit.controls})"
        f"={audit.targeted_corrected_tail:.9f}"
    )
    print(
        f"  broad_relation_tail="
        f"({1 + audit.broad_relation_controls}/{1 + audit.controls})"
        f"={audit.broad_corrected_tail:.9f}"
    )
    print(f"  passes={audit.passes}")


if __name__ == "__main__":
    main()
