#!/usr/bin/env python3
"""Print the Gate/Veska ``+3`` Eye-marker transfer audit."""

from __future__ import annotations

from eye_mystery.gate_plus3_transfer import (
    audit_conditional,
    audit_observed,
    scan_observed_shifts,
)


def main() -> None:
    observed = audit_observed()
    conditional = audit_conditional()
    print("observed transfers")
    for transfer in observed.transfers:
        print(
            f"  {transfer.source_name} {transfer.source_rank} -> "
            f"{transfer.target_name} {transfer.target_rank}"
        )
        print(f"    left  {transfer.left_quotient}")
        print(f"    right {transfer.right_quotient}")
    print(
        "self",
        observed.self_shift_rank,
        observed.self_shift_target,
    )
    print(
        "shared left",
        observed.shared_left,
        observed.shared_left_cycles,
        observed.shared_left_order,
        observed.shared_left_in_p_d4,
    )
    print(
        "shared right",
        observed.shared_right,
        observed.shared_right_cycles,
        observed.shared_right_order,
        observed.shared_right_in_p_d4,
    )
    print("conditional")
    for field, value in conditional.__dict__.items():
        print(f"  {field}: {value}")
    print("complete observed shift hits")
    for hit in scan_observed_shifts():
        print(
            f"  +{hit.shift}: row{hit.source_row}->row{hit.target_row} "
            f"n={hit.transfer_count} left={hit.shared_left} "
            f"right={hit.shared_right}"
        )


if __name__ == "__main__":
    main()

