#!/usr/bin/env python3
"""Compare the recent crafted syllable pair with East 1 / West 1."""

from __future__ import annotations

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.finnish_syllables import aligned_equality_runs, syllable_tokens


CRAFTED_FIRST = (
    "Paukkovalla paaterella. Mitä itket, impi rukka, Impi rukka, neito nuori; "
    "Maammoko pahon pitävi? Maammoni hyvin pitävi. Immikkö aholla itki,"
)
CRAFTED_SECOND = (
    "Paukkovalla paaterella. Mitä itket, impi rukka, Impi rukka, neito nuori; "
    "Sikkoko pahon pitävi? Sikkoni hyvin pitävi. Immikkö aholla itki,"
)


def main() -> None:
    first = syllable_tokens(CRAFTED_FIRST)
    second = syllable_tokens(CRAFTED_SECOND)
    east = trigram_values(MESSAGES["east1"])[1:]
    west = trigram_values(MESSAGES["west1"])[1:]
    print("crafted first:", first)
    print("crafted second:", second)
    print("crafted equality runs:", aligned_equality_runs(first, second))
    print("Eye equality runs:", aligned_equality_runs(east, west))


if __name__ == "__main__":
    main()
