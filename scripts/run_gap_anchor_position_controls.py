#!/usr/bin/env python3
"""Run the frozen gap-anchor position/permutation follow-up."""

from eye_mystery.gap_anchor import (
    broad_position_match,
    gap_anchor_position_audit,
    planted_position_streams,
)


def main() -> None:
    plant = planted_position_streams()
    print("plant", broad_position_match(plant))
    if broad_position_match(plant) is None:
        raise SystemExit("position positive control failed")

    audit = gap_anchor_position_audit()
    print(
        "target",
        f"structure={audit.target_structure_controls}/{audit.controls}",
        f"position=({1 + audit.target_position_controls}/"
        f"{1 + audit.controls})={audit.target_position_tail:.9f}",
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
