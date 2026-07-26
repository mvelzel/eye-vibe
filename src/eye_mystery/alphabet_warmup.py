"""Discarded-alphabet initial states for bounded adaptive ciphers."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from eye_mystery.affine_gak import MODULUS
from eye_mystery.deck_base_generic import validate_permutation
from eye_mystery.ninth_second import TRAILER_ALPHABET

LATIN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


@dataclass(frozen=True)
class AlphabetWarmup:
    """One finite interpretation of an unwritten A-Z encryption pass."""

    name: str
    plaintext: tuple[int, ...]


def alphabet_warmups() -> tuple[AlphabetWarmup, ...]:
    """Return the three literal standard/keyed-alphabet interpretations.

    The community proposal says that A-Z may have been encrypted and its
    outputs discarded, possibly using the Trailer Altar keyed alphabet.
    "Using the keyed alphabet" has two directional readings: encrypt the
    keyed letter order under standard A-Z indices, or encrypt standard A-Z
    under positions in the keyed order.  They are inverse permutations.
    """

    keyed_letters = TRAILER_ALPHABET[:26]
    if len(keyed_letters) != 26 or set(keyed_letters) != set(LATIN_ALPHABET):
        raise ValueError("Trailer alphabet must begin with a permutation of A-Z")
    keyed_ranks = tuple(LATIN_ALPHABET.index(letter) for letter in keyed_letters)
    inverse_keyed_ranks = tuple(
        keyed_letters.index(letter) for letter in LATIN_ALPHABET
    )
    return (
        AlphabetWarmup("standard-az", tuple(range(26))),
        AlphabetWarmup("keyed-letter-order", keyed_ranks),
        AlphabetWarmup("az-in-keyed-slots", inverse_keyed_ranks),
    )


def deck_coordinates_after_warmup(
    base: Sequence[int],
    plaintext: Sequence[int],
) -> tuple[int, ...]:
    """Materialize a base/top-swap warm-up and return card coordinates."""

    validate_permutation(base)
    size = len(base)
    if any(not 0 <= position < size for position in plaintext):
        raise ValueError("warm-up instruction is outside the deck")
    deck = list(range(size))
    for position in plaintext:
        deck = [deck[base[index]] for index in range(size)]
        deck[0], deck[position] = deck[position], deck[0]
    coordinate_of = [0] * size
    for coordinate, card in enumerate(deck):
        coordinate_of[card] = coordinate
    return tuple(coordinate_of)


def affine_state_after_warmup(
    plaintext: Sequence[int],
    multiplier_for_plaintext: Callable[[int], int],
    *,
    previous: int = 0,
    hidden: int = 1,
    modulus: int = MODULUS,
) -> tuple[int, int] | None:
    """Return ``(visible_coordinate, hidden_multiplier)`` after a GAK warm-up."""

    previous %= modulus
    hidden %= modulus
    if hidden == 0:
        return None
    for symbol in plaintext:
        symbol %= modulus
        previous = (previous + symbol * pow(hidden, -1, modulus)) % modulus
        multiplier = multiplier_for_plaintext(symbol) % modulus
        if multiplier == 0:
            return None
        hidden = hidden * multiplier % modulus
    return previous, hidden
