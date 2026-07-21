#!/usr/bin/env python3
"""Exhaust the raw-eye inverse-MTF plus marker-indexed BWT pipeline."""

from eye_mystery.bwt_mtf import raw_eye_bwt_mtf_audit


def main() -> None:
    for key, value in raw_eye_bwt_mtf_audit().items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
