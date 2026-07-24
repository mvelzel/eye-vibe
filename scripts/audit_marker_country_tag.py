#!/usr/bin/env python3
"""Run the preregistered Eye marker country-tag audit."""

from __future__ import annotations

from dataclasses import asdict

from eye_mystery.marker_country import marker_country_audit


def main() -> None:
    audit = marker_country_audit()
    for key, value in asdict(audit).items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
