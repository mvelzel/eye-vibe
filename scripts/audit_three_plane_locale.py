#!/usr/bin/env python3
"""Run the preregistered marker calling-code/locale audit."""

from __future__ import annotations

from dataclasses import asdict

from eye_mystery.locale_checksum import (
    locale_checksum_audit,
    observed_plane_summaries,
)


def main() -> None:
    print("observed planes:")
    for summary in observed_plane_summaries():
        print(
            f"  coordinate {summary.coordinate}: digits={summary.digits} "
            f"code={summary.code} regions={summary.regions}"
        )
    print("conditional audit:")
    for key, value in asdict(locale_checksum_audit()).items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
