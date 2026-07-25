#!/usr/bin/env python3
"""Run the frozen final-row synchronizing-bridge audit."""

from __future__ import annotations

import argparse

from eye_mystery.synchronizing_bridge import (
    audit_controls,
    bridge_segments,
    bridge_specs,
    canonical_streams,
    late_context_profiles,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=50000)
    parser.add_argument("--seed", type=lambda value: int(value, 0), default=0xB1236E)
    args = parser.parse_args()
    streams = canonical_streams()
    specs = bridge_specs()
    segments = bridge_segments(streams)
    for name in specs:
        spec = specs[name]
        print(
            f"{name}: anchor={spec.anchor_value} "
            f"start={spec.anchor_start_trimmed} "
            f"endpoint={spec.endpoint_full} entry={spec.late_entry_full} "
            f"length={spec.length}"
        )
        print(f"  bridge={segments[name]}")
    for name, profile in late_context_profiles(streams).items():
        print(f"{name}: {profile}")

    audit = audit_controls(controls=args.controls, seed=args.seed)
    observed = audit.observed
    broad = audit.observed_broad
    print("observed")
    print(f"  signatures={observed.signatures}")
    print(f"  triple_lcp={observed.triple_lcp}")
    print(f"  east_profile={observed.east_profile}")
    print(f"  east_complete={observed.east_complete}")
    print(f"  east_switch={observed.east_switch}")
    print(f"  joint={observed.joint}")
    print(f"  broad={broad}")
    print("controls")
    for field in (
        "triple_lcp_exceedances",
        "east_complete_exceedances",
        "east_switch_exceedances",
        "joint_exceedances",
        "conditioned_w4_exceedances",
        "broad_lcp_exceedances",
        "broad_pair_exceedances",
        "broad_joint_exceedances",
    ):
        exceedances = getattr(audit, field)
        tail = audit.corrected_tail(exceedances, audit.controls)
        print(f"  {field}={exceedances}/{audit.controls} tail={tail:.9f}")


if __name__ == "__main__":
    main()

