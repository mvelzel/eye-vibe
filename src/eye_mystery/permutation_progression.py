"""Position-progressive substitution under an arbitrary symbol permutation.

The model is ``cipher_i = P**i(substitution[plain_i])``.  Applying the inverse
power at each position removes the progressive permutation and leaves an
ordinary substitution alphabet.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence


def validate_permutation(permutation: Sequence[int]) -> None:
    if sorted(permutation) != list(range(len(permutation))):
        raise ValueError("permutation must contain every label exactly once")


def inverse_permutation(permutation: Sequence[int]) -> tuple[int, ...]:
    validate_permutation(permutation)
    inverse = [0] * len(permutation)
    for source, target in enumerate(permutation):
        inverse[target] = source
    return tuple(inverse)


def decode_progression(
    message: Sequence[int],
    permutation: Sequence[int],
    *,
    skip: int = 0,
) -> tuple[int, ...]:
    """Remove ``P**position`` from one ciphertext message.

    ``skip`` removes out-of-band leading symbols before the position counter is
    started.  For the Eye messages, ``skip=1`` treats the distinct first
    trigram as metadata and starts position zero at the universal second
    trigram.
    """

    inverse = inverse_permutation(permutation)
    decoded = []
    for position, symbol in enumerate(message[skip:]):
        value = symbol
        for _ in range(position):
            value = inverse[value]
        decoded.append(value)
    return tuple(decoded)


def encrypt_progression(
    plaintext: Sequence[int], permutation: Sequence[int]
) -> tuple[int, ...]:
    """Apply the position-progressive permutation to substituted labels."""

    validate_permutation(permutation)
    encrypted = []
    for position, symbol in enumerate(plaintext):
        value = symbol
        for _ in range(position):
            value = permutation[value]
        encrypted.append(value)
    return tuple(encrypted)


def decoded_alphabet_size(
    messages: Iterable[Sequence[int]],
    permutation: Sequence[int],
    *,
    skip: int = 0,
) -> int:
    return len(
        {
            symbol
            for message in messages
            for symbol in decode_progression(message, permutation, skip=skip)
        }
    )
