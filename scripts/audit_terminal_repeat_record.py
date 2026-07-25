#!/usr/bin/env python3
"""Reproduce the frozen terminal-repeat marker audit."""

from __future__ import annotations

from eye_mystery.terminal_repeat_record import (
    audit_terminal_record,
    common_late_signature,
    observed_event_hits,
    record_values,
    repeat_events,
    terminal_event,
)


def ratio(numerator: int, denominator: int) -> str:
    return f"{numerator}/{denominator} = {numerator / denominator:.9f}"


def main() -> None:
    audit = audit_terminal_record()
    print(f"signature: {common_late_signature()}")
    print(f"repeat_events: {repeat_events()}")
    print(f"terminal_event: {terminal_event()}")
    print(f"record_values: {record_values()}")
    for field in (
        "boundary",
        "position",
        "record",
        "record_and_full_closure",
        "record_and_source_delta",
        "record_and_topology",
        "broad_row2",
        "broad_any_row",
        "broad_signed",
    ):
        print(
            f"{field}: "
            f"{ratio(getattr(audit, field), audit.assignments)}"
        )
    print(
        "factoradic_survivors: "
        f"{audit.factoradic_survivors}; record="
        f"{audit.record_factoradic_survivors}; joint="
        f"{audit.record_and_closure_factoradic_survivors}"
    )
    print(
        "observed_unsigned_hits: "
        f"{observed_event_hits(signed=False)}"
    )
    print(
        "observed_signed_hits: "
        f"{observed_event_hits(signed=True)}"
    )


if __name__ == "__main__":
    main()
