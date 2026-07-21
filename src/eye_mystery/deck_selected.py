"""Fixed deck shuffles followed by simple selected-card actions.

These models complement :mod:`eye_mystery.deck_base_generic`.  That module
tests a fixed shuffle followed by swapping a plaintext-selected position with
the top.  Here the emitted ciphertext card may instead update the deck with a
cut, an insertion, or a packet reversal--operations common in physical card
handling.
"""

from __future__ import annotations

from collections.abc import Sequence

from eye_mystery.deck_base_generic import validate_permutation


ACTIONS = (
    "move-to-front",
    "move-to-back",
    "cut-to-card",
    "cut-after-card",
    "reverse-prefix",
    "reverse-suffix",
)


def selected_action_indices(size: int, action: str, rank: int) -> tuple[int, ...]:
    """Return new-position-to-old-position indices for one selected-card move."""

    if size <= 0:
        raise ValueError("size must be positive")
    if not 0 <= rank < size:
        raise ValueError("rank is outside the deck")
    if action == "move-to-front":
        return (rank,) + tuple(range(rank)) + tuple(range(rank + 1, size))
    if action == "move-to-back":
        return tuple(range(rank)) + tuple(range(rank + 1, size)) + (rank,)
    if action == "cut-to-card":
        return tuple(range(rank, size)) + tuple(range(rank))
    if action == "cut-after-card":
        cut = (rank + 1) % size
        return tuple(range(cut, size)) + tuple(range(cut))
    if action == "reverse-prefix":
        return tuple(range(rank, -1, -1)) + tuple(range(rank + 1, size))
    if action == "reverse-suffix":
        return tuple(range(rank)) + tuple(range(size - 1, rank - 1, -1))
    raise ValueError(f"unknown selected-card action: {action}")


def decode_base_selected_action(
    ciphertext: Sequence[int], base: Sequence[int], action: str
) -> tuple[int, ...]:
    """Decode ``shuffle; select rank; emit selected card; update by action``."""

    validate_permutation(base)
    size = len(base)
    if any(not 0 <= card < size for card in ciphertext):
        raise ValueError("ciphertext card is outside the deck")
    if action not in ACTIONS:
        raise ValueError(f"unknown selected-card action: {action}")

    deck = list(range(size))
    plaintext = []
    for card in ciphertext:
        deck = [deck[position] for position in base]
        rank = deck.index(card)
        plaintext.append(rank)
        indices = selected_action_indices(size, action, rank)
        deck = [deck[position] for position in indices]
    return tuple(plaintext)
