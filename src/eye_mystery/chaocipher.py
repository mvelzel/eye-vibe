"""The historical Chaocipher permutation, generalized to arbitrary size."""

from __future__ import annotations

from collections.abc import Sequence


def _validate(left: Sequence[int], right: Sequence[int]) -> None:
    if len(left) < 4 or len(left) != len(right):
        raise ValueError("alphabets must have the same length of at least four")
    if len(set(left)) != len(left) or set(left) != set(right):
        raise ValueError("alphabets must be permutations of the same symbols")


def permute_left(
    alphabet: Sequence[int], index: int, *, nadir: int | None = None
) -> tuple[int, ...]:
    """Rotate the ciphertext alphabet and move zenith+1 to the nadir."""

    size = len(alphabet)
    if index not in range(size):
        raise ValueError("index outside alphabet")
    nadir = size // 2 if nadir is None else nadir
    if nadir not in range(2, size):
        raise ValueError("nadir must leave room for the Chaocipher insertion")
    rotated = list(alphabet[index:]) + list(alphabet[:index])
    value = rotated.pop(1)
    rotated.insert(nadir, value)
    return tuple(rotated)


def permute_right(
    alphabet: Sequence[int], index: int, *, nadir: int | None = None
) -> tuple[int, ...]:
    """Rotate plaintext to zenith+1 and move the new zenith+2 to nadir."""

    size = len(alphabet)
    if index not in range(size):
        raise ValueError("index outside alphabet")
    nadir = size // 2 if nadir is None else nadir
    if nadir not in range(2, size):
        raise ValueError("nadir must leave room for the Chaocipher insertion")
    rotation = (index + 1) % size
    rotated = list(alphabet[rotation:]) + list(alphabet[:rotation])
    value = rotated.pop(2)
    rotated.insert(nadir, value)
    return tuple(rotated)


def encrypt(
    plaintext: Sequence[int],
    left: Sequence[int],
    right: Sequence[int],
    *,
    nadir: int | None = None,
) -> tuple[int, ...]:
    """Encrypt and reset from the supplied pair of Chaocipher alphabets."""

    _validate(left, right)
    left_state = tuple(left)
    right_state = tuple(right)
    output = []
    for value in plaintext:
        try:
            index = right_state.index(value)
        except ValueError as error:
            raise ValueError("plaintext symbol outside alphabet") from error
        output.append(left_state[index])
        left_state = permute_left(left_state, index, nadir=nadir)
        right_state = permute_right(right_state, index, nadir=nadir)
    return tuple(output)


def decrypt(
    ciphertext: Sequence[int],
    left: Sequence[int],
    right: Sequence[int],
    *,
    nadir: int | None = None,
) -> tuple[int, ...]:
    """Decrypt and reset from the supplied pair of Chaocipher alphabets."""

    _validate(left, right)
    left_state = tuple(left)
    right_state = tuple(right)
    output = []
    for value in ciphertext:
        try:
            index = left_state.index(value)
        except ValueError as error:
            raise ValueError("ciphertext symbol outside alphabet") from error
        output.append(right_state[index])
        left_state = permute_left(left_state, index, nadir=nadir)
        right_state = permute_right(right_state, index, nadir=nadir)
    return tuple(output)
