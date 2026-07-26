"""Verify the compiled Eye-row initializer without decompiler semantics.

The 2025 Windows build writes the low and high halves of its packed ``uint64``
row words to two stack slots.  Zero high halves share one control-flow write,
so the compiled instruction stream contains every low half and only the
nonzero high halves in authored order.
"""

from __future__ import annotations

import struct
from collections.abc import Sequence


LOW_HALF_STORE = b"\xc7\x45\xb4"
HIGH_HALF_STORE = b"\xc7\x45\xb8"


def stack_immediates(code: bytes, prefix: bytes) -> tuple[int, ...]:
    """Extract little-endian imm32 values following one fixed store prefix."""
    if len(prefix) != 3:
        raise ValueError("the x86 store prefix must be three bytes")
    return tuple(
        struct.unpack_from("<I", code, offset + len(prefix))[0]
        for offset in range(len(code) - len(prefix) - 3)
        if code[offset : offset + len(prefix)] == prefix
    )


def expected_initializer_halves(
    words: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return all low halves and the emitted nonzero high halves."""
    lows = tuple(word & 0xFFFFFFFF for word in words)
    nonzero_highs = tuple(word >> 32 for word in words if word >> 32)
    return lows, nonzero_highs


def matches_eye_initializer(code: bytes, words: Sequence[int]) -> bool:
    """Test the fixed compiler representation against independently packed rows."""
    lows, nonzero_highs = expected_initializer_halves(words)
    return (
        stack_immediates(code, LOW_HALF_STORE) == lows
        and stack_immediates(code, HIGH_HALF_STORE) == nonzero_highs
    )
