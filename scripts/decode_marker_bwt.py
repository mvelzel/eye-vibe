#!/usr/bin/env python3
"""Decode and calibrate the BWT payload in the initial markers."""

from __future__ import annotations

from eye_mystery.marker_bwt import (
    marker_bwt_multiset_null_counts,
    marker_bwt_summary,
    marker_bwt_trail_assignment_counts,
)


def render(values: object) -> str:
    return "".join(map(str, values))  # type: ignore[arg-type]


def main() -> None:
    summary = marker_bwt_summary()
    print("last column:", render(summary["last_column"]))
    print("first column:", render(summary["first_column"]))
    print("LF mapping:", summary["lf_mapping"])
    print("LF row order:", summary["lf_order"])
    print("restored message order:", summary["plaintext_order"])
    print("inverse digits:", render(summary["restored_digits"]))
    print("base-five trigram values:", summary["values"])
    print("ASCII+32:", repr(summary["ascii32"]))
    print("exact BWT round trip:", summary["round_trip"])
    print()
    print("observed-third-digit-multiset null:")
    for name, count in marker_bwt_multiset_null_counts().items():
        print(f"  {name}: {count}")
    print("observed-marker assignment null:")
    for name, count in marker_bwt_trail_assignment_counts().items():
        print(f"  {name}: {count}")


if __name__ == "__main__":
    main()
