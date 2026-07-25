#!/usr/bin/env python3
"""Reproduce the frozen middle-eye direction-cycle audit."""

from __future__ import annotations

from eye_mystery.middle_eye_cycle import (
    audit_order,
    axis_audits,
    boundary_audit,
)


def main() -> None:
    for audit in axis_audits():
        print(f"axis: {audit}")
    print(f"order: {audit_order()}")
    print(f"boundary: {boundary_audit()}")


if __name__ == "__main__":
    main()
