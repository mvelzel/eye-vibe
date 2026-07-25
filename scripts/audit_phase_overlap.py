#!/usr/bin/env python3
"""Run the frozen cross-phase equality-class overlap audit."""

from __future__ import annotations

import argparse

from eye_mystery.phase_overlap import (
    audit_controls,
    ledger_target,
    new_class_positions,
    panel_overlap_profiles,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=50000)
    parser.add_argument("--seed", type=lambda value: int(value, 0), default=0xCACE17)
    args = parser.parse_args()
    target = ledger_target()
    print(f"target: {target}")
    for name, profile in panel_overlap_profiles().items():
        print(f"{name}: {profile}")
        print(
            f"  new target positions: "
            f"{new_class_positions(name, target.new_class)}"
        )
    audit = audit_controls(controls=args.controls, seed=args.seed)
    print(f"observed: {audit.observed}")
    print(
        "exact_east_target_probability: "
        f"{audit.exact_east_target_probability} = "
        f"{float(audit.exact_east_target_probability):.9f}"
    )
    print(
        "exact_east_only_probability: "
        f"{audit.exact_east_only_probability} = "
        f"{float(audit.exact_east_only_probability):.9f}"
    )
    for field in (
        "east_target_exceedances",
        "east_only_exceedances",
        "shared_offset17_exceedances",
        "any_shared_edge_exceedances",
    ):
        exceedances = getattr(audit, field)
        tail = audit.corrected_tail(exceedances, audit.controls)
        print(f"{field}: {exceedances}/{audit.controls} tail={tail:.9f}")


if __name__ == "__main__":
    main()
