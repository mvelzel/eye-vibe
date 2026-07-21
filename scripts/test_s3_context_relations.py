#!/usr/bin/env python3
"""Test whether the last-row S3 headers act as the strong body transforms."""

from eye_mystery.s3_context import last_family_s3_context_audit


def main() -> None:
    result = last_family_s3_context_audit()
    print("partial context-map sizes:", result.first_size, result.second_size)
    print("first-generator square observations:", result.first_square)
    print("first-generator involution violations:", result.first_square_violations)
    print("second-generator square observations:", result.second_square)
    print("second-generator involution violations:", result.second_square_violations)
    print("first-second-first:", result.braid_left)
    print("second-first-second:", result.braid_right)
    print("braid conflict:", result.braid_conflict)
    print("direct Coxeter assignment survives:", result.coxeter_assignment_survives)


if __name__ == "__main__":
    main()
