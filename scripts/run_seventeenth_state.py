#!/usr/bin/env python3
"""Run parameter-free state-reconstruction probes."""

from eye_mystery.seventeenth_state import (
    HankelAudit,
    coarsest_equitable_partition,
    eye_bodies,
    fibration_audit,
    hankel_control_audit,
    partition_is_equitable,
    periodic_hankel_plant,
    planted_regular_cover,
)


def print_hankel(label: str, audit: HankelAudit) -> None:
    print(label)
    for split_label, split in (
        ("P", audit.training),
        ("Q", audit.heldout),
    ):
        print(split_label, f"selected={split.selected_depth}")
        for block in split.blocks:
            print(
                " ",
                block.depth,
                f"shape={block.rows}x{block.columns}",
                f"ranks={block.ranks}",
                f"score={block.score:.9f}",
            )
    print(
        f"tail=({1 + audit.exceedances}/{1 + audit.controls})"
        f"={audit.corrected_upper_tail:.9f}",
        f"rank_excess={audit.heldout_rank_excess}",
        f"control_depths={audit.control_selected_depths}",
        f"passes={audit.passes_rank_gate}",
    )


def main() -> None:
    plant, expected = planted_regular_cover()
    recovered = coarsest_equitable_partition(plant)
    print(
        "plant",
        f"expected={len(expected)}",
        f"recovered={len(recovered)}",
        f"equitable={partition_is_equitable(plant, recovered)}",
        f"exact={recovered == expected}",
    )
    print("real")
    for audit in fibration_audit():
        print(audit)

    plant_hankel = hankel_control_audit(periodic_hankel_plant())
    print_hankel("hankel plant", plant_hankel)
    if not plant_hankel.passes_rank_gate:
        raise SystemExit("Hankel positive control failed; Eye scoring withheld")
    real_hankel = hankel_control_audit(
        eye_bodies(prefix_trimmed=True),
    )
    print_hankel("hankel real", real_hankel)


if __name__ == "__main__":
    main()
