"""Exact constraints for sdlwdr practice cipher 4's cyclic outer group."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass


MODULUS = 83


def cyclic_differences(message: Sequence[int]) -> tuple[int, ...]:
    """Return adjacent differences in the disclosed standard C83 order."""

    return tuple(
        (following - current) % MODULUS
        for current, following in zip(message, message[1:])
    )


def project_action_band(
    values: Sequence[int], projection: str
) -> tuple[int, ...]:
    """Project actions in the exact 22..78 band onto a 3-by-19 grid.

    ``rank-div2``/``rank-mod2`` treat each rank as ``2*q + r``;
    ``rank-div3``/``rank-mod3`` use ``3*q + r``; and the 3-by-19 alternatives
    use divisor 19.  ``raw`` is the identity.
    """

    if projection == "raw":
        return tuple(values)
    ranks = tuple(value - 22 for value in values)
    if any(rank not in range(57) for rank in ranks):
        raise ValueError("projected actions must lie in the 22..78 band")
    for divisor in (2, 3, 19):
        if projection == f"rank-div{divisor}":
            return tuple(rank // divisor for rank in ranks)
        if projection == f"rank-mod{divisor}":
            return tuple(rank % divisor for rank in ranks)
    raise ValueError(f"unknown projection: {projection}")


def consistent_recurrence_prefix(
    plaintext: Sequence[int],
    differences: Sequence[int],
    *,
    ciphertext_sign: int = 1,
    plaintext_sign: int = 1,
    key_on_next: bool = False,
) -> int:
    """Length obeying one arbitrary cyclic-GAK transition function.

    In oriented coordinates, a cyclic GAK has the recurrence

    ``p[i+1] = ciphertext_sign * delta[i] + q[p[i]] (mod 83)``.

    ``q`` is arbitrary but must be a function.  The optional next-symbol
    selector covers the opposite update-timing convention.  A global
    plaintext rotation is immaterial; ``plaintext_sign`` covers reflection.
    """

    return consistent_recurrence_prefix_at(
        plaintext,
        0,
        differences,
        ciphertext_sign=ciphertext_sign,
        plaintext_sign=plaintext_sign,
        key_on_next=key_on_next,
    )


def consistent_recurrence_prefix_at(
    plaintext: Sequence[int],
    start: int,
    differences: Sequence[int],
    *,
    ciphertext_sign: int = 1,
    plaintext_sign: int = 1,
    key_on_next: bool = False,
) -> int:
    """Apply :func:`consistent_recurrence_prefix` at a source offset."""

    if ciphertext_sign not in (-1, 1) or plaintext_sign not in (-1, 1):
        raise ValueError("signs must be -1 or +1")
    if start < 0:
        raise ValueError("start must be nonnegative")
    if len(plaintext) < start + len(differences) + 1:
        raise ValueError("plaintext is shorter than the requested window")
    required_by_symbol: dict[int, int] = {}
    for index, difference in enumerate(differences):
        current = plaintext_sign * plaintext[start + index] % MODULUS
        following = plaintext_sign * plaintext[start + index + 1] % MODULUS
        selector = following if key_on_next else current
        required = (following - ciphertext_sign * difference) % MODULUS
        previous = required_by_symbol.setdefault(selector, required)
        if previous != required:
            return index
    return len(differences)


@dataclass(frozen=True)
class AffineSchedule:
    ciphertext_sign: int
    multiplier: int
    translation: int
    starts: tuple[int, ...]


def decode_affine_schedule(
    differences: Sequence[int],
    start: int,
    *,
    ciphertext_sign: int,
    multiplier: int,
    translation: int,
) -> tuple[int, ...]:
    """Decode ``p' = sign*delta + multiplier*p + translation``."""

    if ciphertext_sign not in (-1, 1):
        raise ValueError("ciphertext_sign must be -1 or +1")
    if not 0 <= start < MODULUS:
        raise ValueError("start must lie in Z83")
    output = [start]
    for difference in differences:
        output.append(
            (
                ciphertext_sign * difference
                + multiplier * output[-1]
                + translation
            )
            % MODULUS
        )
    return tuple(output)


def affine_schedule_survivors(
    differences: Sequence[int], allowed: Iterable[int]
) -> tuple[AffineSchedule, ...]:
    """Exhaust every affine cyclic update whose whole output stays allowed."""

    alphabet = tuple(dict.fromkeys(allowed))
    if not alphabet or any(value not in range(MODULUS) for value in alphabet):
        raise ValueError("allowed values must be a nonempty subset of Z83")
    allowed_set = set(alphabet)
    results = []
    for ciphertext_sign in (1, -1):
        for multiplier in range(MODULUS):
            for translation in range(MODULUS):
                starts = []
                for start in alphabet:
                    value = start
                    for difference in differences:
                        value = (
                            ciphertext_sign * difference
                            + multiplier * value
                            + translation
                        ) % MODULUS
                        if value not in allowed_set:
                            break
                    else:
                        starts.append(start)
                if starts:
                    results.append(
                        AffineSchedule(
                            ciphertext_sign,
                            multiplier,
                            translation,
                            tuple(starts),
                        )
                    )
    return tuple(results)
