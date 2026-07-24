#!/usr/bin/env python3
"""Run the frozen anchor-record pointer/gauge controls."""

from eye_mystery.gap_anchor import (
    broad_pointer_match,
    exact_pointer_match,
    final_trimmed_bodies,
    gap_anchor_pointer_audit,
    planted_pointer_streams,
)


def main() -> None:
    plant = planted_pointer_streams()
    print(
        "plant",
        f"exact={exact_pointer_match(plant)}",
        f"broad={broad_pointer_match(plant)}",
    )
    if not exact_pointer_match(plant) or broad_pointer_match(plant) is None:
        raise SystemExit("pointer positive control failed")

    real = final_trimmed_bodies()
    print(
        "real",
        f"exact={exact_pointer_match(real)}",
        f"broad={broad_pointer_match(real)}",
    )
    audit = gap_anchor_pointer_audit()
    print(
        "target",
        f"structure={audit.target_structure_controls}/{audit.controls}",
        f"pointer=({1 + audit.target_pointer_controls}/"
        f"{1 + audit.controls})={audit.target_pointer_tail:.9f}",
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
