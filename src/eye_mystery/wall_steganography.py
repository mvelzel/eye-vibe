"""Decoder for Lymm's Wall Messages steganography practice puzzle."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass


WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
PUNCTUATION_RE = re.compile(r"[,.?!]+")

MORSE_TO_TEXT = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    "-----": "0",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
}
TEXT_TO_MORSE = {text: morse for morse, text in MORSE_TO_TEXT.items()}


@dataclass(frozen=True)
class CarrierWord:
    index: int
    text: str
    bit: str


@dataclass(frozen=True)
class MorseGroup:
    words: tuple[CarrierWord, ...]
    code: str
    decoded: str

    @property
    def text(self) -> str:
        return " ".join(word.text for word in self.words)


@dataclass(frozen=True)
class CarrierMismatch:
    group_index: int
    plaintext: str
    word: CarrierWord
    expected_bit: str


def word_bit(word: str) -> str:
    """Map one to three letters to dot, and four or more to dash."""

    letters = sum(character.isalpha() for character in word)
    return "." if letters <= 3 else "-"


def _clause_groups(
    clause: str,
    *,
    first_word_index: int,
) -> tuple[tuple[tuple[CarrierWord, ...], ...], int]:
    words = tuple(match.group() for match in WORD_RE.finditer(clause))
    groups: list[tuple[CarrierWord, ...]] = []
    current: list[CarrierWord] = []
    next_index = first_word_index
    for word in words:
        if current and word[0].isupper():
            groups.append(tuple(current))
            current = []
        current.append(CarrierWord(next_index, word, word_bit(word)))
        next_index += 1
    if current:
        groups.append(tuple(current))
    return tuple(groups), next_index


def carrier_groups(
    text: str,
    *,
    bit_overrides: Mapping[int, str] | None = None,
) -> tuple[MorseGroup, ...]:
    """Split at punctuation runs and unexpected internal capitals."""

    overrides = dict(bit_overrides or {})
    if any(bit not in {".", "-"} for bit in overrides.values()):
        raise ValueError("bit overrides must be dots or dashes")

    word_index = 1
    clause_start = 0
    word_groups: list[tuple[CarrierWord, ...]] = []
    for delimiter in PUNCTUATION_RE.finditer(text):
        clause = text[clause_start : delimiter.start()].strip()
        clause_start = delimiter.end()
        groups, word_index = _clause_groups(
            clause,
            first_word_index=word_index,
        )
        word_groups.extend(groups)
    final_clause = text[clause_start:].strip()
    groups, word_index = _clause_groups(
        final_clause,
        first_word_index=word_index,
    )
    word_groups.extend(groups)

    result: list[MorseGroup] = []
    for words in word_groups:
        code = "".join(overrides.get(word.index, word.bit) for word in words)
        result.append(
            MorseGroup(
                words=words,
                code=code,
                decoded=MORSE_TO_TEXT.get(code, "?"),
            )
        )
    return tuple(result)


def decode_cover(
    text: str,
    *,
    bit_overrides: Mapping[int, str] | None = None,
) -> str:
    """Decode the punctuation/capital groups to a continuous Morse message."""

    return "".join(
        group.decoded
        for group in carrier_groups(text, bit_overrides=bit_overrides)
    )


def mismatches_against_plaintext(
    text: str,
    plaintext: str,
) -> tuple[CarrierMismatch, ...]:
    """Return the exact carrier-bit mismatches for a proposed plaintext.

    Group count and Morse-code lengths must already agree.  This makes a
    minimal repair certificate independent of language scoring.
    """

    groups = carrier_groups(text)
    normalized = "".join(character for character in plaintext.upper() if character.isalnum())
    if len(groups) != len(normalized):
        raise ValueError(
            f"{len(groups)} carrier groups cannot encode "
            f"{len(normalized)} plaintext characters"
        )

    mismatches: list[CarrierMismatch] = []
    for group_index, (group, character) in enumerate(
        zip(groups, normalized, strict=True),
        1,
    ):
        try:
            expected = TEXT_TO_MORSE[character]
        except KeyError as error:
            raise ValueError(f"unsupported plaintext character {character!r}") from error
        if len(group.words) != len(expected):
            raise ValueError(
                f"group {group_index} has {len(group.words)} carrier words "
                f"but {character!r} requires {len(expected)} Morse bits"
            )
        for word, expected_bit in zip(group.words, expected, strict=True):
            if word.bit != expected_bit:
                mismatches.append(
                    CarrierMismatch(
                        group_index=group_index,
                        plaintext=character,
                        word=word,
                        expected_bit=expected_bit,
                    )
                )
    return tuple(mismatches)
