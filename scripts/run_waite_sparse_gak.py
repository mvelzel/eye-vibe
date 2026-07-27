#!/usr/bin/env python3
"""Run the frozen sparse ordinary-GAK control and Waite East-2 test."""

from __future__ import annotations

import argparse
import random
import time

from eye_mystery.arbitrary_gak_sat import encrypt_messages
from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.sparse_gak_sat import (
    canonical_initial_deck,
    check_next_card_forcing,
    encode_text,
    recover_sparse_known_plaintext_witness,
)
from check_waite_m3_suffix import EAST2_RAW_OFFSET, WAITE_M3_SUFFIX


DECK_SIZE = 83
CONTROL_SEED = 270727
CONTROL_TOP_CARD = 17
HELDOUT_PREFIX_LENGTH = 70


def random_permutation(rng: random.Random, size: int) -> tuple[int, ...]:
    values = list(range(size))
    rng.shuffle(values)
    return tuple(values)


def solve(
    plaintext: tuple[int, ...],
    ciphertext: tuple[int, ...],
    *,
    alphabet_size: int,
    timeout_ms: int,
) -> tuple[str, object | None, float]:
    started = time.monotonic()
    status, witness = recover_sparse_known_plaintext_witness(
        (plaintext,),
        (ciphertext,),
        deck_size=DECK_SIZE,
        plaintext_alphabet_size=alphabet_size,
        timeout_ms=timeout_ms,
    )
    return status, witness, time.monotonic() - started


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-ms", type=int, default=60_000)
    args = parser.parse_args()

    plaintext, alphabet = encode_text(WAITE_M3_SUFFIX)
    print("plaintext length:", len(plaintext))
    print("literal alphabet size:", len(alphabet))
    print("literal alphabet:", repr("".join(alphabet)))

    rng = random.Random(CONTROL_SEED)
    control_operations = tuple(
        random_permutation(rng, DECK_SIZE) for _ in alphabet
    )
    control_initial = canonical_initial_deck(DECK_SIZE, CONTROL_TOP_CARD)
    control_ciphertext = encrypt_messages(
        (plaintext,),
        control_initial,
        control_operations,
    )[0]
    control_status, control_witness, control_seconds = solve(
        plaintext,
        control_ciphertext,
        alphabet_size=len(alphabet),
        timeout_ms=args.timeout_ms,
    )
    control_replay = (
        control_witness is not None
        and encrypt_messages(
            (plaintext,),
            control_witness.initial_deck,
            control_witness.operations,
        )[0]
        == control_ciphertext
    )
    print("control status:", control_status)
    print("control seconds:", f"{control_seconds:.3f}")
    print("control exact replay:", control_replay)
    if control_status != "sat" or not control_replay:
        print("real status: not run; Eye-scale positive control did not pass")
        return

    east2 = trigram_values(MESSAGES["east2"])
    real_ciphertext = east2[EAST2_RAW_OFFSET:]
    real_status, real_witness, real_seconds = solve(
        plaintext,
        real_ciphertext,
        alphabet_size=len(alphabet),
        timeout_ms=args.timeout_ms,
    )
    real_replay = (
        real_witness is not None
        and encrypt_messages(
            (plaintext,),
            real_witness.initial_deck,
            real_witness.operations,
        )[0]
        == real_ciphertext
    )
    print("real status:", real_status)
    print("real seconds:", f"{real_seconds:.3f}")
    print("real exact replay:", real_replay)
    if real_status != "sat" or not real_replay:
        print("heldout status: not run; full candidate was not SAT")
        return

    started = time.monotonic()
    heldout = check_next_card_forcing(
        plaintext[:HELDOUT_PREFIX_LENGTH],
        real_ciphertext[:HELDOUT_PREFIX_LENGTH],
        plaintext[HELDOUT_PREFIX_LENGTH],
        real_ciphertext[HELDOUT_PREFIX_LENGTH],
        deck_size=DECK_SIZE,
        plaintext_alphabet_size=len(alphabet),
        timeout_ms=args.timeout_ms,
    )
    print("heldout prefix length:", HELDOUT_PREFIX_LENGTH)
    print("heldout actual card:", real_ciphertext[HELDOUT_PREFIX_LENGTH])
    print("heldout actual status:", heldout.actual_status)
    print("heldout alternative status:", heldout.alternative_status)
    print("heldout alternative card:", heldout.alternative_card)
    print("heldout forced:", heldout.forced)
    print("heldout seconds:", f"{time.monotonic() - started:.3f}")


if __name__ == "__main__":
    main()
