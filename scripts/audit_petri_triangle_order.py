#!/usr/bin/env python3
"""Run the frozen Petri/Eye triangle-order provenance check."""

from eye_mystery.petri_triangle_order import (
    EYE_ACCEPTED_ORDERS,
    PETRI_SOURCE_ORDERS,
    global_orientation_matches,
    orientation_signature,
)


def main() -> None:
    print("Petri source winding:", dict(orientation_signature(PETRI_SOURCE_ORDERS)))
    print("Accepted Eye winding:", dict(orientation_signature(EYE_ACCEPTED_ORDERS)))
    print("Global symmetry matches:", global_orientation_matches())


if __name__ == "__main__":
    main()
