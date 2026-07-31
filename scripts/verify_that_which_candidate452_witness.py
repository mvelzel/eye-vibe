#!/usr/bin/env python3
"""Independently replay the frozen connected-gap ordinary-GAK witness."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from eye_mystery.arbitrary_gak_sat import encrypt_messages

from run_that_which_connected_gap_gak import connected_instances


ARTIFACT = (
    Path(__file__).resolve().parents[1]
    / "artifacts"
    / "that-which-connected-gap-gak-witness-2026-07-31.json"
)


def main() -> None:
    payload = json.loads(ARTIFACT.read_text())
    decks = tuple(tuple(row) for row in payload["initial_decks"])
    operations = tuple(tuple(row) for row in payload["operations"])
    plaintexts = tuple(tuple(row) for row in payload["plaintexts"])
    _, expected, _ = connected_instances()

    if any(sorted(row) != list(range(83)) for row in decks):
        raise SystemExit("an initial deck is not a permutation of 0..82")
    if any(sorted(row) != list(range(83)) for row in operations):
        raise SystemExit("an operation is not a permutation of 0..82")
    replay = tuple(
        encrypt_messages((plaintext,), deck, operations)[0]
        for plaintext, deck in zip(plaintexts, decks, strict=True)
    )
    if replay != expected:
        raise SystemExit("witness does not replay the three frozen segments")

    digest = hashlib.sha256(
        repr((decks, operations, plaintexts)).encode()
    ).hexdigest()
    if digest != payload["witness_sha256"]:
        raise SystemExit("witness digest differs from the frozen digest")
    print(
        "exact_replay=yes traces=3 lengths=38,40,45 "
        f"actions=7 deck=83 sha256={digest}"
    )


if __name__ == "__main__":
    main()
