"""Utilities for testing the solved Cessation cipher against the Eyes."""

from __future__ import annotations

from collections.abc import Iterable, Sequence


# The January Void-Liquid calendar key used by the solved Cessation quest.
CESSATION_KEY = tuple(map(int, "1100111101001111001010010101101"))


def skip_key_bits(
    values: Iterable[int],
    key: Sequence[int] = CESSATION_KEY,
    *,
    reset_value: int | None = None,
) -> tuple[int, ...]:
    """Decode forward skip distances through a cyclic binary key.

    The pointer begins immediately before key position zero.  A distance of
    one therefore emits the first bit.  If ``reset_value`` is supplied, that
    value moves the pointer back before position zero and emits no bit.
    """

    if not key or any(bit not in (0, 1) for bit in key):
        raise ValueError("key must be a non-empty binary sequence")
    pointer = -1
    output = []
    for value in values:
        if reset_value is not None and value == reset_value:
            pointer = -1
            continue
        if value < 1:
            raise ValueError("skip distances must be positive")
        pointer = (pointer + value) % len(key)
        output.append(key[pointer])
    return tuple(output)


def trace_trigram_skip_states(
    directions: Sequence[int],
    steps: Sequence[int],
    modulus: int,
    *,
    initial_state: int = 0,
) -> tuple[int, ...]:
    """Apply three direction skips and emit one cyclic state per trigram.

    This is the closest alphabet-ring analogue of the Cessation mechanism for
    the Eyes: each visible direction selects a skip distance, while the
    established three-eye grouping determines when a character is read.
    ``steps`` may be negative to represent walking the ring in reverse.
    """

    if len(directions) % 3:
        raise ValueError("direction count must be divisible by three")
    if len(steps) != 5:
        raise ValueError("steps must contain one value for each eye direction")
    if modulus < 1:
        raise ValueError("modulus must be positive")
    if any(direction not in range(5) for direction in directions):
        raise ValueError("directions must be in 0..4")

    state = initial_state % modulus
    output = []
    for start in range(0, len(directions), 3):
        state = (
            state
            + sum(steps[direction] for direction in directions[start : start + 3])
        ) % modulus
        output.append(state)
    return tuple(output)


def bits_to_bytes(
    bits: Sequence[int], *, offset: int = 0, least_significant_first: bool = False
) -> bytes:
    """Pack complete eight-bit groups after ``offset`` into bytes."""

    if offset not in range(8):
        raise ValueError("bit offset must be in 0..7")
    output = bytearray()
    for start in range(offset, len(bits) - 7, 8):
        chunk = bits[start : start + 8]
        if least_significant_first:
            chunk = tuple(reversed(chunk))
        value = 0
        for bit in chunk:
            if bit not in (0, 1):
                raise ValueError("bits must contain only zero and one")
            value = 2 * value + bit
        output.append(value)
    return bytes(output)


def text_likeness(data: bytes) -> tuple[int, int, int]:
    """Rank byte strings by text characters, printable bytes, and controls."""

    text = sum(
        byte == 32
        or 65 <= byte <= 90
        or 97 <= byte <= 122
        or byte in b".,;:!?'-\n\r"
        for byte in data
    )
    printable = sum(byte in (9, 10, 13) or 32 <= byte <= 126 for byte in data)
    controls = len(data) - printable
    return text, printable, -controls
