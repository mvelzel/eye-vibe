"""Audit natural Eye-label readings of Noita's 83-entry ``gun_names`` table."""

from __future__ import annotations

import random
from collections.abc import Callable, Mapping, Sequence

from .ngram import TetragramModel


NameFeature = Callable[[int, str], int]


def _letters(name: str) -> str:
    return "".join(character for character in name.upper() if character.isalpha())


def first_letter(_: int, name: str) -> int:
    return ord(name[0].upper()) - ord("A")


def last_letter(_: int, name: str) -> int:
    return ord(name[-1].upper()) - ord("A")


def middle_left(_: int, name: str) -> int:
    letters = _letters(name)
    return ord(letters[(len(letters) - 1) // 2]) - ord("A")


def middle_right(_: int, name: str) -> int:
    letters = _letters(name)
    return ord(letters[len(letters) // 2]) - ord("A")


def a1z26_length(_: int, name: str) -> int:
    """Map a word of length one to A, length two to B, and so on."""
    return (sum(character.isalpha() for character in name) - 1) % 26


def _base5_digits(index: int) -> tuple[int, int, int]:
    return index // 25, (index // 5) % 5, index % 5


def indexed_letter(digit: int, *, from_end: bool = False) -> NameFeature:
    def feature(index: int, name: str) -> int:
        letters = _letters(name)
        position = _base5_digits(index)[digit] % len(letters)
        if from_end:
            position = len(letters) - 1 - position
        return ord(letters[position]) - ord("A")

    return feature


def digit_sum_letter(index: int, name: str, *, from_end: bool = False) -> int:
    letters = _letters(name)
    position = sum(_base5_digits(index)) % len(letters)
    if from_end:
        position = len(letters) - 1 - position
    return ord(letters[position]) - ord("A")


def label_mod_letter(index: int, name: str, *, from_end: bool = False) -> int:
    letters = _letters(name)
    position = index % len(letters)
    if from_end:
        position = len(letters) - 1 - position
    return ord(letters[position]) - ord("A")


FEATURES: tuple[tuple[str, NameFeature], ...] = (
    ("first-letter", first_letter),
    ("last-letter", last_letter),
    ("middle-left", middle_left),
    ("middle-right", middle_right),
    ("A1Z26-length", a1z26_length),
    ("eye-a-from-start", indexed_letter(0)),
    ("eye-b-from-start", indexed_letter(1)),
    ("eye-c-from-start", indexed_letter(2)),
    ("eye-a-from-end", indexed_letter(0, from_end=True)),
    ("eye-b-from-end", indexed_letter(1, from_end=True)),
    ("eye-c-from-end", indexed_letter(2, from_end=True)),
    ("eye-digit-sum-from-start", digit_sum_letter),
    (
        "eye-digit-sum-from-end",
        lambda index, name: digit_sum_letter(index, name, from_end=True),
    ),
    ("label-mod-from-start", label_mod_letter),
    (
        "label-mod-from-end",
        lambda index, name: label_mod_letter(index, name, from_end=True),
    ),
)


def feature_map(names: Sequence[str], feature: NameFeature) -> tuple[int, ...]:
    if len(names) != 83:
        raise ValueError("the selector must contain exactly 83 names")
    values = tuple(feature(index, name) for index, name in enumerate(names))
    if any(not 0 <= value < 26 for value in values):
        raise ValueError("name feature is outside A-Z")
    return values


def alphabetical_deck(
    names: Sequence[str], *, reverse: bool = False
) -> tuple[int, ...]:
    """Order the 83 Eye-label cards by their assigned adjective."""
    if len(names) != 83:
        raise ValueError("the selector must contain exactly 83 names")
    if len(set(names)) != len(names):
        raise ValueError("name-based deck order requires unique names")
    return tuple(
        sorted(range(83), key=lambda index: names[index].casefold(), reverse=reverse)
    )


def map_messages(
    messages: Mapping[str, Sequence[int]],
    mapping: Sequence[int],
    *,
    omit_marker: bool,
) -> dict[str, tuple[int, ...]]:
    start = 1 if omit_marker else 0
    return {
        name: tuple(mapping[value] for value in message[start:])
        for name, message in messages.items()
    }


def score_messages(
    model: TetragramModel, messages: Mapping[str, Sequence[int]]
) -> tuple[float, int]:
    windows = sum(max(0, len(message) - 3) for message in messages.values())
    if not windows:
        raise ValueError("messages contain no tetragram windows")
    return sum(model.score(tuple(message)) for message in messages.values()), windows


def best_natural_score(
    names: Sequence[str],
    messages: Mapping[str, Sequence[int]],
    model: TetragramModel,
) -> tuple[float, str, bool]:
    best = (-float("inf"), "", False)
    for feature_name, feature in FEATURES:
        mapping = feature_map(names, feature)
        for omit_marker in (False, True):
            score, _ = score_messages(
                model,
                map_messages(messages, mapping, omit_marker=omit_marker),
            )
            candidate = (score, feature_name, omit_marker)
            if candidate[0] > best[0]:
                best = candidate
    return best


def permutation_control(
    names: Sequence[str],
    messages: Mapping[str, Sequence[int]],
    model: TetragramModel,
    *,
    controls: int,
    seed: int,
) -> tuple[float, int, int]:
    """Correct over all predeclared readings using shuffled assignments."""
    observed, _, _ = best_natural_score(names, messages, model)
    generator = random.Random(seed)
    at_least = 0
    shuffled = list(names)
    for _ in range(controls):
        generator.shuffle(shuffled)
        score, _, _ = best_natural_score(shuffled, messages, model)
        at_least += score >= observed
    return observed, at_least, controls
