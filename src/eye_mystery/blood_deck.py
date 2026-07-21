"""Treat the Meditation Chamber blood rows as 26 deck-cut instructions."""

from __future__ import annotations

from collections.abc import Sequence

from .blood_sieve import BLOOD_ROW_RUNS


def blood_cut_vectors() -> dict[str, tuple[int, ...]]:
    """Return the natural one-number summaries of each of the 26 blood rows."""
    starts = tuple(row[0][0] for row in BLOOD_ROW_RUNS)
    ends = tuple(row[-1][1] for row in BLOOD_ROW_RUNS)
    spans = tuple(end - start for start, end in zip(starts, ends, strict=True))
    counts = tuple(
        sum(end - start for start, end in row) for row in BLOOD_ROW_RUNS
    )
    return {
        "start": starts,
        "end": ends,
        "span": spans,
        "count": counts,
    }


def cut_letter_map(
    cuts: Sequence[int], *, deck_size: int = 83, reverse: bool = False
) -> dict[int, int]:
    """Map distinct cut amounts to A1Z26-style letter indexes ``0..25``."""
    normalized = tuple(((-cut if reverse else cut) % deck_size) for cut in cuts)
    if len(set(normalized)) != len(normalized):
        raise ValueError("cut amounts must be distinct modulo the deck size")
    return {cut: index for index, cut in enumerate(normalized)}


def apply_permutation(deck: Sequence[int], permutation: Sequence[int]) -> tuple[int, ...]:
    if len(deck) != len(permutation):
        raise ValueError("deck and permutation must have the same size")
    return tuple(deck[position] for position in permutation)


def decode_base_then_blood_cut(
    ciphertext: Sequence[int],
    base: Sequence[int],
    cuts: Sequence[int],
    *,
    reverse_cuts: bool = False,
    initial_deck: Sequence[int] | None = None,
) -> tuple[int, ...] | None:
    """Apply the common base, infer a blood-row cut, then emit the top card."""
    size = len(base)
    letter_for_cut = cut_letter_map(cuts, deck_size=size, reverse=reverse_cuts)
    deck = tuple(range(size)) if initial_deck is None else tuple(initial_deck)
    plaintext: list[int] = []
    for card in ciphertext:
        deck = apply_permutation(deck, base)
        rank = deck.index(card)
        letter = letter_for_cut.get(rank)
        if letter is None:
            return None
        plaintext.append(letter)
        deck = deck[rank:] + deck[:rank]
    return tuple(plaintext)


def decode_blood_cut_then_base(
    ciphertext: Sequence[int],
    base: Sequence[int],
    cuts: Sequence[int],
    *,
    reverse_cuts: bool = False,
    initial_deck: Sequence[int] | None = None,
) -> tuple[int, ...] | None:
    """Infer a blood-row cut, apply it, then apply the common base shuffle."""
    size = len(base)
    letter_for_cut = cut_letter_map(cuts, deck_size=size, reverse=reverse_cuts)
    deck = tuple(range(size)) if initial_deck is None else tuple(initial_deck)
    plaintext: list[int] = []
    for card in ciphertext:
        rank = deck.index(card)
        cut = (rank - base[0]) % size
        letter = letter_for_cut.get(cut)
        if letter is None:
            return None
        plaintext.append(letter)
        rotated = deck[cut:] + deck[:cut]
        deck = apply_permutation(rotated, base)
    return tuple(plaintext)
