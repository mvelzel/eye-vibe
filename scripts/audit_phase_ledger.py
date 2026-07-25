#!/usr/bin/env python3
"""Print the residue-seven header/phase ledger audit."""

from __future__ import annotations

from eye_mystery.phase_ledger import audit_phase_ledger


def main() -> None:
    audit = audit_phase_ledger()
    for field, value in audit.__dict__.items():
        print(f"{field}: {value}")


if __name__ == "__main__":
    main()

