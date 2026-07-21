#!/usr/bin/env python3
"""Recover and replay a deterministic arbitrary-permutation GAK toy."""

from __future__ import annotations

import argparse
import random

from eye_mystery.arbitrary_gak_sat import (
    encrypt_messages,
    recover_known_plaintext_witness,
)


def random_permutation(rng: random.Random, size: int) -> tuple[int, ...]:
    values = list(range(size))
    rng.shuffle(values)
    return tuple(values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deck-size", type=int, default=6)
    parser.add_argument("--messages", type=int, default=3)
    parser.add_argument("--length", type=int, default=18)
    parser.add_argument("--seed", type=int, default=260721)
    parser.add_argument("--timeout-ms", type=int, default=30_000)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    # Identity is a valid canonical reset representative with top card zero.
    initial_deck = tuple(range(args.deck_size))
    operations = tuple(random_permutation(rng, args.deck_size) for _ in range(2))
    plaintexts = tuple(
        tuple(rng.randrange(2) for _ in range(args.length))
        for _ in range(args.messages)
    )
    ciphertexts = encrypt_messages(plaintexts, initial_deck, operations)

    status, witness = recover_known_plaintext_witness(
        plaintexts,
        ciphertexts,
        deck_size=args.deck_size,
        plaintext_alphabet_size=2,
        initial_top_card=0,
        timeout_ms=args.timeout_ms,
    )
    print("status:", status)
    print("deck size:", args.deck_size)
    print("known symbols:", sum(map(len, plaintexts)))
    if witness is None:
        return
    replay = encrypt_messages(plaintexts, witness.initial_deck, witness.operations)
    print("exact replay:", replay == ciphertexts)
    print("initial deck:", witness.initial_deck)
    print("operation 0:", witness.operations[0])
    print("operation 1:", witness.operations[1])


if __name__ == "__main__":
    main()
