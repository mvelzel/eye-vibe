#!/usr/bin/env python3
"""Exact ordinary-GAK extension test for the six ``THAT WHICH`` windows."""

from __future__ import annotations

import argparse

from eye_mystery.arbitrary_state_sparse_gak import (
    recover_arbitrary_state_gak_witness,
)
from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.sparse_gak_sat import encode_text

try:
    from scripts.classify_that_which_windows import WINDOWS
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from classify_that_which_windows import WINDOWS


PHRASE = "THAT WHICH"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-ms", type=int, default=60_000)
    args = parser.parse_args()

    plaintext, alphabet = encode_text(PHRASE)
    ciphertexts = tuple(
        trigram_values(MESSAGES[window.message])[
            window.offset : window.offset + len(PHRASE)
        ]
        for window in WINDOWS
    )
    status, witness = recover_arbitrary_state_gak_witness(
        (plaintext,) * len(ciphertexts),
        ciphertexts,
        deck_size=83,
        plaintext_alphabet_size=len(alphabet),
        timeout_ms=args.timeout_ms,
    )
    print(
        f"traces={len(ciphertexts)} length={len(PHRASE)} "
        f"operations={len(alphabet)} status={status}"
    )
    if witness is not None:
        print("forward replay=exact")
        print(
            "initial tops="
            + ",".join(str(deck[0]) for deck in witness.initial_decks)
        )


if __name__ == "__main__":
    main()
