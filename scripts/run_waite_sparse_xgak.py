#!/usr/bin/env python3
"""Run the frozen sparse-XGAK control and Waite East-2 test."""

from __future__ import annotations

import argparse
import random
import time

from check_waite_m3_suffix import EAST2_RAW_OFFSET, WAITE_M3_SUFFIX

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.sparse_gak_sat import encode_text
from eye_mystery.sparse_xgak_sat import (
    XGAKWitness,
    check_specific_xgak_next_card,
    encrypt_xgak_messages,
    recover_sparse_xgak_witness,
)

DECK_SIZE = 83
CONTROL_SEED = 270728
HELDOUT_OFFSET = 73


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
) -> tuple[str, XGAKWitness | None, float]:
    started = time.monotonic()
    status, witness = recover_sparse_xgak_witness(
        (plaintext,),
        (ciphertext,),
        deck_size=DECK_SIZE,
        plaintext_alphabet_size=alphabet_size,
        distinct_output_positions=True,
        timeout_ms=timeout_ms,
    )
    return status, witness, time.monotonic() - started


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-ms", type=int, default=120_000)
    args = parser.parse_args()

    plaintext, alphabet = encode_text(WAITE_M3_SUFFIX)
    print("plaintext length:", len(plaintext))
    print("literal alphabet size:", len(alphabet))
    print("literal alphabet:", repr("".join(alphabet)))
    print("selector constraint: pairwise distinct")

    rng = random.Random(CONTROL_SEED)
    control_operations = tuple(
        random_permutation(rng, DECK_SIZE) for _ in alphabet
    )
    positions = list(range(DECK_SIZE))
    rng.shuffle(positions)
    control = XGAKWitness(
        control_operations,
        tuple(positions[: len(alphabet)]),
    )
    control_ciphertext = encrypt_xgak_messages((plaintext,), control)[0]
    control_status, control_witness, control_seconds = solve(
        plaintext,
        control_ciphertext,
        alphabet_size=len(alphabet),
        timeout_ms=args.timeout_ms,
    )
    control_replay = (
        control_witness is not None
        and encrypt_xgak_messages((plaintext,), control_witness)[0]
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
        and encrypt_xgak_messages((plaintext,), real_witness)[0]
        == real_ciphertext
    )
    print("real status:", real_status)
    print("real seconds:", f"{real_seconds:.3f}")
    print("real exact replay:", real_replay)
    if real_witness is not None:
        print("real output positions:", real_witness.output_positions)
    if real_status != "sat" or not real_replay:
        print("heldout status: not run; full candidate was not SAT")
        return

    actual = real_ciphertext[HELDOUT_OFFSET]
    alternative = (actual + 1) % DECK_SIZE
    started = time.monotonic()
    heldout = check_specific_xgak_next_card(
        plaintext[:HELDOUT_OFFSET],
        real_ciphertext[:HELDOUT_OFFSET],
        plaintext[HELDOUT_OFFSET],
        actual,
        alternative,
        deck_size=DECK_SIZE,
        plaintext_alphabet_size=len(alphabet),
        distinct_output_positions=True,
        timeout_ms=args.timeout_ms,
    )
    print("heldout prefix length:", HELDOUT_OFFSET)
    print("heldout actual card:", heldout.actual_card)
    print("heldout actual status:", heldout.actual_status)
    print("heldout frozen alternative card:", heldout.alternative_card)
    print("heldout alternative status:", heldout.alternative_status)
    print("heldout non-forcing:", heldout.non_forcing)
    print("heldout seconds:", f"{time.monotonic() - started:.3f}")


if __name__ == "__main__":
    main()
