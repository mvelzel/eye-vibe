#!/usr/bin/env python3
"""Test the classical Wadsworth/cipher-clock interpretation of the Eyes."""

from __future__ import annotations

from eye_mystery.cipher_clock import (
    reciprocal_digram_witnesses,
    reciprocal_plaintext_ring_lower_bound,
)
from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values


def main() -> None:
    bodies = {
        name: trigram_values(MESSAGES[name])[1:] for name in MESSAGE_ORDER
    }
    witnesses = reciprocal_digram_witnesses(bodies)
    lower_bound = reciprocal_plaintext_ring_lower_bound(bodies, 83)
    print("body reciprocal digram pairs:", len(witnesses))
    print("plaintext-ring lower bound:", lower_bound)
    print("Finnish letters (29) excluded:", lower_bound > 29)
    print("Finnish letters plus space (30) excluded:", lower_bound > 30)
    print()
    for witness in witnesses[:10]:
        forward = ", ".join(
            f"{item.message}:{item.position}"
            for item in witness.forward
        )
        reverse = ", ".join(
            f"{item.message}:{item.position}"
            for item in witness.reverse
        )
        print(
            f"{witness.first}->{witness.second} at {forward}; "
            f"{witness.second}->{witness.first} at {reverse}"
        )


if __name__ == "__main__":
    main()
