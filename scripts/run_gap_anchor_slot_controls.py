#!/usr/bin/env python3
"""Run the frozen anchor-record slot/target-rank controls."""

from eye_mystery.gap_anchor import (
    broad_slot_rank_match,
    gap_anchor_slot_audit,
    matching_slot_pairs,
    ordinal_ranks,
    planted_gap_streams,
    unique_anchor_values,
)


def main() -> None:
    plant = planted_gap_streams()
    anchors = unique_anchor_values(plant, 11)
    print(
        "plant",
        f"anchors={anchors}",
        f"ranks={ordinal_ranks(anchors or ())}",
        f"slots={matching_slot_pairs(anchors or ())}",
        f"broad={broad_slot_rank_match(plant)}",
    )
    if (
        anchors is None
        or ordinal_ranks(anchors) != (1, 2, 0)
        or matching_slot_pairs(anchors) != ((0, 2),)
        or broad_slot_rank_match(plant) is None
    ):
        raise SystemExit("slot positive control failed")

    audit = gap_anchor_slot_audit()
    print(
        "target",
        f"structure={audit.target_structure_controls}/{audit.controls}",
        f"rank=({1 + audit.target_rank_controls}/"
        f"{1 + audit.controls})={audit.target_rank_tail:.9f}",
        f"numeric={audit.target_numeric_controls}/{audit.controls}",
        f"joint=({1 + audit.target_joint_controls}/"
        f"{1 + audit.controls})={audit.target_joint_tail:.9f}",
    )
    print(
        "broad",
        f"joint=({1 + audit.broad_joint_controls}/"
        f"{1 + audit.controls})={audit.broad_joint_tail:.9f}",
        f"passes={audit.passes}",
    )


if __name__ == "__main__":
    main()
