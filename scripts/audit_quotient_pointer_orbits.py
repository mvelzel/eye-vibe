#!/usr/bin/env python3
"""Print the canonical quotient-pointer bridge and its matched null."""

from __future__ import annotations

import argparse

from eye_mystery.quotient_pointer_orbits import (
    canonical_signature,
    common_window_signatures,
    matched_pointer_null,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=500_000)
    parser.add_argument(
        "--seed",
        type=lambda value: int(value, 0),
        default=0x5645534B41,
    )
    args = parser.parse_args()

    observed = canonical_signature()
    print("canonical quotient-seeded orbits")
    for panel in observed.panels:
        orbit = panel.orbit
        print(
            f"{panel.name:>5} q={panel.quotient:2d} r={panel.remainder:2d} "
            f"path={orbit.path} repeat={orbit.repeated_state} "
            f"tail={len(orbit.tail):2d} cycle={len(orbit.cycle):2d}"
        )
    print(
        "all-total / all-union / omitted / closing-tail / closing-cycle / "
        "pure-nonclosing / other-nonclosing:",
        observed.all_orbit_total,
        observed.all_union_size,
        observed.omitted_label_count,
        observed.closing_tail_total,
        observed.closing_cycle_total,
        observed.pure_nonclosing_orbit_sizes,
        observed.other_nonclosing_orbit_total,
    )
    print(
        "closing total / union / cycles / intersections:",
        observed.closing_orbit_total,
        observed.closing_union_size,
        observed.closing_cycle_lengths,
        observed.closing_intersection_sizes,
    )
    print("common 83-window starts with substantive bridge events")
    for start, item in common_window_signatures():
        events = (
            item.objective_gate_event,
            item.predicted_full_partition_event,
            item.phase_event,
            item.ordered_cycle_event,
        )
        if any(events):
            print(
                f"start={start} total={item.all_orbit_total} "
                f"closing={item.closing_orbit_total}/{item.closing_union_size} "
                f"cycles={item.closing_cycle_lengths} events={events}"
            )

    audit = matched_pointer_null(
        args.trials,
        seed=args.seed,
        progress=lambda trial: print(f"completed {trial}/{args.trials}", flush=True),
    )
    print("matched null")
    fields = (
        ("total72", audit.total_72_hits),
        ("typed objective Gate 72|9|8", audit.objective_gate_hits),
        ("broad objective Gate 72|9|8", audit.broad_objective_gate_hits),
        ("typed predicted 12|43|9|8", audit.predicted_full_partition_hits),
        ("broad predicted 12|43|9|8", audit.broad_full_partition_hits),
        ("closing 17|20 phase", audit.phase_hits),
        ("ordered cycles 1|4|7", audit.ordered_cycle_hits),
        ("any ordered +3 cycles", audit.ordered_plus_three_cycle_hits),
        ("header overlap mask", audit.header_overlap_hits),
        ("typed omitted=E4 remainder", audit.typed_sieve_remainder_hits),
        ("omitted=any checksum remainder", audit.any_checksum_remainder_hits),
        ("total72 + typed omitted", audit.total_72_and_typed_sieve_hits),
        ("phase + typed objective", audit.phase_and_objective_hits),
        ("phase + broad objective", audit.phase_and_broad_objective_hits),
        ("phase + typed objective + cycles", audit.full_bridge_hits),
        ("phase + broad objective + cycles", audit.broad_full_bridge_hits),
    )
    for label, hits in fields:
        print(
            f"{label:>29}: {hits}/{audit.trials}; "
            f"corrected={audit.corrected_rate(hits):.12g}"
        )


if __name__ == "__main__":
    main()
