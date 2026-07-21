"""Reversible adaptive-deck transforms for an S_83 cipher hypothesis."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


def move_to_front_decode(ciphertext: Sequence[int], deck: Sequence[int]) -> tuple[int, ...]:
    """Decode emitted card labels to their current ranks, then move to front."""
    state = list(deck)
    plaintext = []
    for symbol in ciphertext:
        rank = state.index(symbol)
        plaintext.append(rank)
        state.pop(rank)
        state.insert(0, symbol)
    return tuple(plaintext)


def move_to_back_decode(ciphertext: Sequence[int], deck: Sequence[int]) -> tuple[int, ...]:
    """Decode card ranks, moving each emitted card to the back."""
    state = list(deck)
    plaintext = []
    for symbol in ciphertext:
        rank = state.index(symbol)
        plaintext.append(rank)
        state.pop(rank)
        state.append(symbol)
    return tuple(plaintext)


def transpose_decode(
    ciphertext: Sequence[int], deck: Sequence[int], distance: int = 1
) -> tuple[int, ...]:
    """Decode card ranks, moving each emitted card toward the front by N."""
    state = list(deck)
    plaintext = []
    for symbol in ciphertext:
        rank = state.index(symbol)
        plaintext.append(rank)
        target = max(0, rank - distance)
        state.pop(rank)
        state.insert(target, symbol)
    return tuple(plaintext)


def swap_with_front_decode(ciphertext: Sequence[int], deck: Sequence[int]) -> tuple[int, ...]:
    """Decode card ranks, swapping each emitted card with the top card."""
    state = list(deck)
    plaintext = []
    for symbol in ciphertext:
        rank = state.index(symbol)
        plaintext.append(rank)
        state[0], state[rank] = state[rank], state[0]
    return tuple(plaintext)


def reverse_prefix_decode(ciphertext: Sequence[int], deck: Sequence[int]) -> tuple[int, ...]:
    """Decode card ranks, then reverse the prefix ending at that card."""
    state = list(deck)
    plaintext = []
    for symbol in ciphertext:
        rank = state.index(symbol)
        plaintext.append(rank)
        state[: rank + 1] = reversed(state[: rank + 1])
    return tuple(plaintext)


def rotate_to_front_decode(ciphertext: Sequence[int], deck: Sequence[int]) -> tuple[int, ...]:
    """Decode ranks, cyclically rotating the selected card to the front."""
    state = list(deck)
    plaintext = []
    for symbol in ciphertext:
        rank = state.index(symbol)
        plaintext.append(rank)
        state[:] = state[rank:] + state[:rank]
    return tuple(plaintext)


@dataclass(frozen=True)
class DeckResult:
    family: str
    deck_order: str
    parameter: int
    unique: int
    maximum: int
    under_26: float
    ioc: float


def ranks_to_labels(
    ranks: Sequence[int], deck: Sequence[int], family: str, distance: int = 1
) -> tuple[int, ...]:
    """Apply rank instructions and emit the selected card labels.

    This is the inverse direction of the ``*_decode`` functions and tests
    whether the eye values are adaptive ranks rather than emitted labels.
    """
    state = list(deck)
    labels = []
    for rank in ranks:
        symbol = state[rank]
        labels.append(symbol)
        if family == "move-to-front":
            state.pop(rank)
            state.insert(0, symbol)
        elif family == "move-to-back":
            state.pop(rank)
            state.append(symbol)
        elif family == "transpose":
            target = max(0, rank - distance)
            state.pop(rank)
            state.insert(target, symbol)
        elif family == "swap-front":
            state[0], state[rank] = state[rank], state[0]
        elif family == "reverse-prefix":
            state[: rank + 1] = reversed(state[: rank + 1])
        elif family == "rotate-front":
            state[:] = state[rank:] + state[:rank]
        else:
            raise ValueError(f"unknown adaptive deck family: {family}")
    return tuple(labels)
