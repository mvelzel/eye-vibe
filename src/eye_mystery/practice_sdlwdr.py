"""Recovered mechanics for sdlwdr's first two practice ciphers."""

from __future__ import annotations

from collections.abc import Sequence


COMBINED82 = r'''p>9iEZ81q-',D[].6f$0;<jl2Q7_kdP&`BLFng"5R^X:?V@OmG/+re~oUa=3)c\h!4YSKT*N(#HMbCW%IA'''
EXCEPTIONAL_RAW = ord("J") - 32

# Traversing this string corresponds to decreasing coordinates in the
# recovered 42-position plaintext wheel.
PLAINTEXT_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .-’?!"
PLAINTEXT_WHEEL = tuple(
    next(
        character
        for alphabet_index, character in enumerate(PLAINTEXT_ALPHABET)
        if (5 - alphabet_index) % 42 == coordinate
    )
    for coordinate in range(42)
)

# Each section starts with a ciphertext-wheel origin that emits no plaintext.
# The rotations below synchronize the resulting coordinate streams with the
# shared 42-position plaintext wheel.  The exceptional J emits the preceding
# plaintext character and flips the parity convention used for later deltas.
PUZZLE1_SHIFTS = (18, 37, 6, 38, 2, 40, 18, 20, 4, 36, 32, 37, 30, 34, 38, 22, 38)

# Every ordinary section starts in the forward state.  Its first ciphertext
# symbol establishes a ciphertext-wheel origin but emits no recoverable
# plaintext.  These rotations were recovered by synchronizing the common
# plaintext wheel across sections.
PUZZLE2_SHIFTS = (0, 0, 12, 38, 24, 32, 18, 23, 2, 30, None, 3, 28)


def raw_symbol(raw: int) -> str:
    """Render the puzzle's raw 0..82 alphabet (space is displayed as ``~``)."""
    if not 0 <= raw <= 82:
        raise ValueError("raw symbol must lie in 0..82")
    return "~" if raw == 0 else chr(raw + 32)


def ciphertext_coordinate(raw: int) -> int:
    if raw == EXCEPTIONAL_RAW:
        raise ValueError("J is not on the ordinary 82-position wheel")
    return COMBINED82.index(raw_symbol(raw))


def _render_coordinate(value: int, shift: int, direction: int = 1) -> str:
    return PLAINTEXT_WHEEL[(direction * value + shift) % 42]


def decode_puzzle1_section(message: Sequence[int], shift: int) -> str:
    """Decode one section of sdlwdr #1's parity-switching Wadsworth cipher."""
    if len(message) < 2:
        return ""
    previous = ciphertext_coordinate(message[0])
    accumulator = 0
    parity = 0
    result: list[str] = []
    for raw in message[1:]:
        if raw == EXCEPTIONAL_RAW:
            result.append(_render_coordinate(accumulator, shift))
            parity ^= 1
            continue
        current = ciphertext_coordinate(raw)
        distance = (current - previous + 42 * parity) % 82
        accumulator = (accumulator + distance) % 42
        result.append(_render_coordinate(accumulator, shift))
        previous = current
    return "".join(result)


def decode_puzzle1_sections(
    messages: Sequence[Sequence[int]],
) -> tuple[str, ...]:
    if len(messages) != len(PUZZLE1_SHIFTS):
        raise ValueError("puzzle #1 must contain seventeen sections")
    return tuple(
        decode_puzzle1_section(message, shift)
        for message, shift in zip(messages, PUZZLE1_SHIFTS, strict=True)
    )


def decode_puzzle2_ordinary(message: Sequence[int], shift: int) -> str:
    """Decode one forward-traversing section, omitting its unknown first item."""
    if len(message) < 2:
        return ""
    if EXCEPTIONAL_RAW in message:
        raise ValueError("ordinary section unexpectedly contains J")
    previous = ciphertext_coordinate(message[0])
    plaintext_coordinate = 0
    result: list[str] = []
    for raw in message[1:]:
        current = ciphertext_coordinate(raw)
        distance = (current - previous) % 82
        plaintext_coordinate = (plaintext_coordinate + distance) % 42
        result.append(_render_coordinate(plaintext_coordinate, shift))
        previous = current
    return "".join(result)


def decode_puzzle2_reversal(message: Sequence[int]) -> str:
    """Decode section 10, whose J reverses both wheel directions.

    J occurs at zero-based position 90 and supplies the repeated ``L`` in
    ``WILL``.  The post-J accumulator is expressed in the reflected coordinate
    convention, hence its separate origin and mapping direction.
    """
    marker = message.index(EXCEPTIONAL_RAW)
    if marker != 90:
        raise ValueError(f"expected J at index 90, got {marker}")

    previous = ciphertext_coordinate(message[0])
    accumulator = 0
    result: list[str] = []
    for raw in message[1:marker]:
        current = ciphertext_coordinate(raw)
        distance = (current - previous) % 82
        accumulator = (accumulator + distance) % 42
        result.append(_render_coordinate(accumulator, 40))
        previous = current

    result.append(result[-1])
    accumulator = 0
    for raw in message[marker + 1 :]:
        current = ciphertext_coordinate(raw)
        distance = (previous - current) % 82
        accumulator = (accumulator + distance) % 42
        result.append(_render_coordinate(accumulator, 36, direction=-1))
        previous = current
    return "".join(result)


def decode_puzzle2_sections(
    messages: Sequence[Sequence[int]],
) -> tuple[str, ...]:
    if len(messages) != len(PUZZLE2_SHIFTS):
        raise ValueError("puzzle #2 must contain thirteen sections")
    result = []
    for index, (message, shift) in enumerate(zip(messages, PUZZLE2_SHIFTS, strict=True)):
        if index == 10:
            result.append(decode_puzzle2_reversal(message))
        else:
            assert shift is not None
            result.append(decode_puzzle2_ordinary(message, shift))
    return tuple(result)
