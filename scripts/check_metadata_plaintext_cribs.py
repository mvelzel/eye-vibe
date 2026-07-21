#!/usr/bin/env python3
"""Check plaintext prefixes suggested by the BEXIT prefix-depth reading."""

from __future__ import annotations

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.known_plaintext import first_isomorphism_conflict


def check(name: str, plaintexts: dict[str, str]) -> None:
    ciphertexts = {
        message_name: trigram_values(MESSAGES[message_name])[1 : 1 + len(text)]
        for message_name, text in plaintexts.items()
    }
    conflict = first_isomorphism_conflict(
        plaintexts,
        ciphertexts,
        min_length=2,
        max_length=max(map(len, plaintexts.values())),
    )
    print(name)
    if conflict is None:
        print("  no perfect-isomorphism conflict")
        return
    print("  conflict:", "".join(conflict.plaintext))
    for occurrence in conflict.occurrences:
        print(
            f"    {occurrence.message}:{occurrence.position} "
            f"{occurrence.ciphertext_pattern}"
        )


def main() -> None:
    check(
        "Emerald Tablet above/below completion",
        {
            "east1": "THATWHICHISABOVEISLIKETO",
            "west1": "THATWHICHISABOVEISLIKETO",
            "east2": "THATWHICHISABOVEISLIKETO",
            "west2": "THATW",
            "east3": "THATWHICH",
            "west3": "THATW",
            "east4": "THATWHICHISBELOWISLI",
            "west4": "THATWHICHISBELOWISLI",
            "east5": "THATWHICHISBELOWISLI",
        },
    )
    check(
        "Corpus Hermeticum VI lower-branch completion",
        {
            "west2": "THERE",
            "east3": "THEREISNO",
            "west3": "THERE",
            "east4": "THEREISNOGOODTHATCAN",
            "west4": "THEREISNOGOODTHATCAN",
            "east5": "THEREISNOGOODTHATCAN",
        },
    )
    check(
        "combined upper/lower Hermetic prefixes",
        {
            "east1": "THATWHICHISABOVEISLIKETO",
            "west1": "THATWHICHISABOVEISLIKETO",
            "east2": "THATWHICHISABOVEISLIKETO",
            "west2": "THERE",
            "east3": "THEREISNO",
            "west3": "THERE",
            "east4": "THEREISNOGOODTHATCAN",
            "west4": "THEREISNOGOODTHATCAN",
            "east5": "THEREISNOGOODTHATCAN",
        },
    )
    cessation = "SEEKINGTRUTHTHEWISEFINDINSTEADITSPROFOUNDABSENCE"
    check(
        "Cessation plaintext as the common Eye prefix",
        {
            "east1": cessation[:24],
            "west1": cessation[:24],
            "east2": cessation[:24],
            "west2": cessation[:5],
            "east3": cessation[:9],
            "west3": cessation[:5],
            "east4": cessation[:20],
            "west4": cessation[:20],
            "east5": cessation[:20],
        },
    )


if __name__ == "__main__":
    main()
