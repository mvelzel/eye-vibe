#!/usr/bin/env python3
"""Run the frozen registered-context checksum transfer."""

from eye_mystery.context_checksum_transfer import (
    audit_registered_contexts,
    checksum_plant,
)


def print_context(prefix: str, audit: object) -> None:
    print(prefix, audit)


def main() -> None:
    plant = checksum_plant()
    print_context("plant", plant)
    if not plant.complete_two_field_match:
        raise SystemExit("checksum plant failed")

    result = audit_registered_contexts()
    print_context("calibration", result.calibration)
    for audit in result.transfers:
        print_context("transfer", audit)
    print(
        "summary",
        f"testable={result.testable_contexts}/6",
        f"fields={result.matching_fields}/{result.tested_fields}",
        f"complete={result.complete_two_field_matches}",
        f"reversed={result.reversed_matching_fields}/"
        f"{result.tested_fields}",
    )


if __name__ == "__main__":
    main()
