"""Bounded Baconian screens for Noita's 515 Wall Message words."""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from math import isfinite


WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
ENGLISH_FREQUENCIES = (
    0.082,
    0.015,
    0.028,
    0.043,
    0.127,
    0.022,
    0.020,
    0.061,
    0.070,
    0.0015,
    0.0077,
    0.040,
    0.024,
    0.067,
    0.075,
    0.019,
    0.00095,
    0.060,
    0.063,
    0.091,
    0.028,
    0.0098,
    0.024,
    0.0015,
    0.020,
    0.00074,
)


@dataclass(frozen=True)
class WallWord:
    map_id: str
    line_index: int
    raw: str
    normalized: str
    suffix: str


@dataclass(frozen=True)
class BaconianCandidate:
    order_name: str
    rule_name: str
    reverse_bits: bool
    inverted: bool
    values: tuple[int, ...]
    decoded: str
    invalid: int
    monogram_chi_square: float


def tokenize_wall(
    map_id: str,
    lines: Sequence[str],
) -> tuple[WallWord, ...]:
    result = []
    for line_index, line in enumerate(lines):
        matches = tuple(WORD_RE.finditer(line))
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(line)
            suffix = line[match.end() : end]
            result.append(
                WallWord(
                    map_id,
                    line_index,
                    match.group(),
                    match.group().lower(),
                    suffix,
                )
            )
    return tuple(result)


def word_xor(word: WallWord, codebook: Mapping[str, int]) -> int:
    result = 0
    for character in word.raw.upper():
        result ^= codebook[character]
    return result


def word_ink_sum(word: WallWord, codebook: Mapping[str, int]) -> int:
    return sum(codebook[character].bit_count() for character in word.raw.upper())


def candidate_rules(
    codebook: Mapping[str, int],
) -> Mapping[str, Callable[[WallWord], bool]]:
    """Return the predeclared word-level binary features.

    The family is limited to visible typography, word length, and the authored
    4-by-4 rune bitmaps.  It deliberately excludes arbitrary word lists and
    fitted assignments.
    """

    rules: dict[str, Callable[[WallWord], bool]] = {
        "length-parity": lambda word: len(word.normalized.replace("'", "")) % 2 == 1,
        "capitalized": lambda word: word.raw[0].isupper(),
        "apostrophe": lambda word: "'" in word.raw,
        "any-punctuation": lambda word: any(mark in word.suffix for mark in ",.?!"),
        "sentence-punctuation": lambda word: any(mark in word.suffix for mark in ".?!"),
        "question-mark": lambda word: "?" in word.suffix,
        "you-prefix": lambda word: word.normalized.startswith("you"),
        "ink-sum-parity": lambda word: word_ink_sum(word, codebook) % 2 == 1,
        "xor-weight-parity": lambda word: word_xor(word, codebook).bit_count() % 2 == 1,
        "first-weight-parity": lambda word: (
            codebook[word.raw[0].upper()].bit_count() % 2 == 1
        ),
        "last-weight-parity": lambda word: (
            codebook[word.raw[-1].upper()].bit_count() % 2 == 1
        ),
    }
    for threshold in range(2, 10):
        rules[f"length>={threshold}"] = (
            lambda word, threshold=threshold:
            len(word.normalized.replace("'", "")) >= threshold
        )
    for bit in range(16):
        rules[f"xor-pixel-{bit:02}"] = (
            lambda word, bit=bit: bool(word_xor(word, codebook) & (1 << bit))
        )
    return rules


def baconian_values(
    bits: Sequence[bool],
    *,
    reverse_bits: bool = False,
    inverted: bool = False,
) -> tuple[int, ...]:
    if len(bits) % 5:
        raise ValueError("Baconian stream length must be divisible by five")
    result = []
    for start in range(0, len(bits), 5):
        group = bits[start : start + 5]
        if reverse_bits:
            group = tuple(reversed(group))
        value = 0
        for bit in group:
            value = 2 * value + (bool(bit) ^ inverted)
        result.append(value)
    return tuple(result)


def decode_values(values: Sequence[int]) -> str:
    return "".join(chr(ord("A") + value) if value < 26 else "?" for value in values)


def monogram_chi_square(values: Sequence[int]) -> float:
    valid = tuple(value for value in values if value < 26)
    if not valid:
        return float("inf")
    counts = [valid.count(value) for value in range(26)]
    total = len(valid)
    score = sum(
        (count - total * expected) ** 2 / (total * expected)
        for count, expected in zip(counts, ENGLISH_FREQUENCIES, strict=True)
    )
    return score if isfinite(score) else float("inf")


def scan_baconian(
    words_by_id: Mapping[str, Sequence[WallWord]],
    orders: Mapping[str, Sequence[str]],
    codebook: Mapping[str, int],
) -> tuple[BaconianCandidate, ...]:
    rules = candidate_rules(codebook)
    result = []
    for order_name, order in orders.items():
        words = tuple(
            word
            for map_id in order
            for word in words_by_id[map_id]
        )
        if len(words) != 515:
            raise ValueError(f"{order_name}: expected 515 words, got {len(words)}")
        for rule_name, rule in rules.items():
            bits = tuple(rule(word) for word in words)
            for reverse_bits in (False, True):
                for inverted in (False, True):
                    values = baconian_values(
                        bits,
                        reverse_bits=reverse_bits,
                        inverted=inverted,
                    )
                    result.append(
                        BaconianCandidate(
                            order_name,
                            rule_name,
                            reverse_bits,
                            inverted,
                            values,
                            decode_values(values),
                            sum(value >= 26 for value in values),
                            monogram_chi_square(values),
                        )
                    )
    return tuple(result)
