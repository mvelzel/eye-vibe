"""Deterministic orthographic Finnish syllable-token utilities.

This is intentionally a small, auditable rule system rather than a claim to
resolve every morphological or dialectal ambiguity.  It follows the general
Kielitoimiston rules: a boundary precedes the last consonant before a vowel,
and adjacent vowels split unless they form a long vowel or one of the standard
Finnish diphthongs.  ``ie``, ``uo``, and ``yö`` are treated as diphthongs only
in the first syllable.
"""

from __future__ import annotations

from collections.abc import Sequence
import re
import unicodedata


VOWELS = frozenset("aeiouyäö")
DIPHTHONGS = frozenset(
    (
        "ai",
        "ei",
        "oi",
        "ui",
        "yi",
        "äi",
        "öi",
        "ey",
        "iy",
        "äy",
        "öy",
        "au",
        "eu",
        "iu",
        "ou",
        "ie",
        "uo",
        "yö",
    )
)
FIRST_SYLLABLE_ONLY_DIPHTHONGS = frozenset(("ie", "uo", "yö"))
WORD_PATTERN = re.compile(r"[a-zåäöšž]+", re.IGNORECASE)


def _is_diphthong(pair: str, *, first_syllable: bool) -> bool:
    return pair in DIPHTHONGS and (
        first_syllable or pair not in FIRST_SYLLABLE_ONLY_DIPHTHONGS
    )


def syllabify_word(word: str) -> tuple[str, ...]:
    """Split one Finnish orthographic word using the frozen general rules."""

    normalized = unicodedata.normalize("NFC", word).lower()
    if not normalized or not all(character.isalpha() for character in normalized):
        raise ValueError("word must contain letters only")
    boundaries: list[int] = []
    syllable_start = 0

    for index in range(len(normalized) - 1):
        left = normalized[index]
        right = normalized[index + 1]
        left_vowel = left in VOWELS
        right_vowel = right in VOWELS

        if not left_vowel and right_vowel:
            # In V C...C V, the final consonant begins the next syllable.
            if any(
                character in VOWELS
                for character in normalized[syllable_start:index]
            ):
                boundaries.append(index)
                syllable_start = index
        elif left_vowel and right_vowel:
            pair = left + right
            same_vowel = left == right
            first_syllable = not boundaries
            if not same_vowel and not _is_diphthong(
                pair, first_syllable=first_syllable
            ):
                boundaries.append(index + 1)
                syllable_start = index + 1

    starts = (0, *boundaries)
    stops = (*boundaries, len(normalized))
    return tuple(
        normalized[start:stop]
        for start, stop in zip(starts, stops, strict=True)
        if start < stop
    )


def syllable_tokens(text: str) -> tuple[str, ...]:
    """Tokenize text into words and concatenate their syllables."""

    return tuple(
        syllable
        for word in WORD_PATTERN.findall(unicodedata.normalize("NFC", text))
        for syllable in syllabify_word(word)
    )


def equality_signature(values: Sequence[object]) -> tuple[int, ...]:
    """Canonical first-occurrence labels for a token sequence."""

    labels: dict[object, int] = {}
    signature = []
    for value in values:
        if value not in labels:
            labels[value] = len(labels)
        signature.append(labels[value])
    return tuple(signature)


def aligned_equality_runs(
    left: Sequence[object], right: Sequence[object]
) -> tuple[tuple[bool, int], ...]:
    """Run lengths of literal equality at aligned positions."""

    runs: list[tuple[bool, int]] = []
    for equal in (a == b for a, b in zip(left, right, strict=False)):
        if runs and runs[-1][0] == equal:
            runs[-1] = (equal, runs[-1][1] + 1)
        else:
            runs.append((equal, 1))
    return tuple(runs)
