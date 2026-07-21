"""Deterministic-mask readouts for constant-step cyclic walks.

This is the small, exact mechanism behind a solved community practice puzzle:
adjacent ciphertext symbols walk by ``+step`` or ``-step`` on a cycle, those
directions are XORed with a short deterministic mask, and the resulting bits
are read in fixed-width chunks.
"""

from collections.abc import Sequence


def direction_bits(
    values: Sequence[int], *, modulus: int, step: int = 1
) -> tuple[int, ...] | None:
    """Return 1 for ``+step`` and 0 for ``-step``, or ``None`` on a violation."""
    if modulus < 3:
        raise ValueError("modulus must be at least 3")
    step %= modulus
    if step == 0 or step == -step % modulus:
        raise ValueError("positive and negative steps must be distinct")
    if any(not 0 <= value < modulus for value in values):
        raise ValueError("values must lie inside the cycle")

    bits: list[int] = []
    for left, right in zip(values, values[1:]):
        difference = (right - left) % modulus
        if difference == step:
            bits.append(1)
        elif difference == -step % modulus:
            bits.append(0)
        else:
            return None
    return tuple(bits)


def walk_violations(
    values: Sequence[int], *, modulus: int, step: int = 1
) -> tuple[int, ...]:
    """Return transition indexes that are not either signed constant step."""
    if modulus < 3:
        raise ValueError("modulus must be at least 3")
    step %= modulus
    if step == 0 or step == -step % modulus:
        raise ValueError("positive and negative steps must be distinct")
    return tuple(
        index
        for index, (left, right) in enumerate(zip(values, values[1:]))
        if (right - left) % modulus not in (step, -step % modulus)
    )


def xor_periodic_mask(
    bits: Sequence[int], pattern: Sequence[int]
) -> tuple[int, ...]:
    """XOR a nonempty periodic binary pattern over a bit stream."""
    if not pattern:
        raise ValueError("mask pattern cannot be empty")
    if any(bit not in (0, 1) for bit in (*bits, *pattern)):
        raise ValueError("bits and mask entries must be zero or one")
    return tuple(bit ^ pattern[index % len(pattern)] for index, bit in enumerate(bits))


def chunk_values(
    bits: Sequence[int],
    *,
    width: int,
    offset: int = 0,
    least_significant_first: bool = False,
) -> tuple[int, ...]:
    """Read complete fixed-width chunks after an initial bit offset."""
    if width < 1:
        raise ValueError("width must be positive")
    if not 0 <= offset < width:
        raise ValueError("offset must be smaller than width")
    usable = bits[offset : offset + (len(bits) - offset) // width * width]
    chunks: list[int] = []
    for start in range(0, len(usable), width):
        value = 0
        for index, bit in enumerate(usable[start : start + width]):
            if bit not in (0, 1):
                raise ValueError("bits must be zero or one")
            shift = index if least_significant_first else width - index - 1
            value |= bit << shift
        chunks.append(value)
    return tuple(chunks)
