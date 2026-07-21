"""Five eye directions as noncommutative permutations of F_83."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

MODULUS = 83


def _center(value: int, mode: str) -> int:
    if mode == "identity":
        return value
    if mode == "negation":
        return -value % MODULUS
    if mode == "inversion":
        return 0 if value == 0 else pow(value, -1, MODULUS)
    if mode == "reflection":
        return (1 - value) % MODULUS
    raise ValueError(f"unknown center operation: {mode}")


def trace_affine_walk(
    message: Sequence[int],
    generator: int,
    translation_pair: tuple[int, int],
    center_mode: str,
    up_order: tuple[int, int, int] = (0, 1, 2),
    down_order: tuple[int, int, int] | None = None,
    initial: int = 0,
) -> tuple[int, ...]:
    """Apply each eye as a field permutation and observe after each trigram.

    ``translation_pair`` identifies the directions assigned ``+1`` and ``-1``.
    The remaining opposite pair is assigned multiplication by ``generator`` and
    its inverse.  Valid pairs are ``(1, 3)`` and ``(2, 4)`` (or reversed).
    """
    if generator % MODULUS == 0:
        raise ValueError("generator must be nonzero")
    down_order = up_order if down_order is None else down_order
    positive, negative = translation_pair
    remaining = [eye for eye in (1, 2, 3, 4) if eye not in translation_pair]
    if set(translation_pair) not in ({1, 3}, {2, 4}):
        raise ValueError("translation directions must be an opposite pair")
    multiplier, divider = remaining
    inverse = pow(generator, -1, MODULUS)
    value = initial % MODULUS
    output = []
    for offset in range(0, len(message), 3):
        order = up_order if (offset // 3) % 2 == 0 else down_order
        trigram = message[offset : offset + 3]
        for index in order:
            eye = trigram[index]
            if eye == 0:
                value = _center(value, center_mode)
            elif eye == positive:
                value = (value + 1) % MODULUS
            elif eye == negative:
                value = (value - 1) % MODULUS
            elif eye == multiplier:
                value = generator * value % MODULUS
            elif eye == divider:
                value = inverse * value % MODULUS
        output.append(value)
    return tuple(output)


@dataclass(frozen=True)
class WalkResult:
    generator: int
    translation_pair: tuple[int, int]
    center_mode: str
    up_order: tuple[int, int, int]
    down_order: tuple[int, int, int]
    unique: int
    ioc: float
