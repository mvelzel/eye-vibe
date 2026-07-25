#!/usr/bin/env python3
"""Run the prospective row-2 phase-budget transfer."""

from __future__ import annotations

import argparse

from eye_mystery.row2_phase_transfer import (
    audit_controls,
    predicted_suffixes,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=50000)
    parser.add_argument("--seed", type=lambda value: int(value, 0), default=0xB0D2)
    args = parser.parse_args()
    print(f"predicted_suffixes: {predicted_suffixes()}")
    audit = audit_controls(controls=args.controls, seed=args.seed)
    print(f"observed: {audit.observed}")
    print(f"observed_broad: {audit.observed_broad}")
    for field in (
        "new_common_exceedances",
        "pair_complete_exceedances",
        "pair_switch_exceedances",
        "joint_exceedances",
        "broad_new_common_exceedances",
        "broad_joint_exceedances",
    ):
        exceedances = getattr(audit, field)
        tail = audit.corrected_tail(exceedances, audit.controls)
        print(f"{field}: {exceedances}/{audit.controls} tail={tail:.9f}")


if __name__ == "__main__":
    main()

