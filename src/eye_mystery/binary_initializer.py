"""Verify the compiled Eye-row initializer without decompiler semantics.

The 2025 Windows build writes the low and high halves of its packed ``uint64``
row words to two stack slots.  Zero high halves share one control-flow write,
so the compiled instruction stream contains every low half and only the
nonzero high halves in authored order.
"""

from __future__ import annotations

import struct
from collections.abc import Sequence
from dataclasses import dataclass


LOW_HALF_STORE = b"\xc7\x45\xb4"
HIGH_HALF_STORE = b"\xc7\x45\xb8"


@dataclass(frozen=True)
class EyeCallsiteAudit:
    """Frozen byte-level facts at the one compiled Eye callsite."""

    direct_call_sites: tuple[int, ...]
    callsite_va: int | None
    initializer_argument_signature: bool
    panel_index_loop_signature: bool
    side_filter_signature: bool
    coordinate_argument_signature: bool

    @property
    def exact_interface(self) -> bool:
        return (
            len(self.direct_call_sites) == 1
            and self.initializer_argument_signature
            and self.panel_index_loop_signature
            and self.side_filter_signature
            and self.coordinate_argument_signature
        )


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


def relative_call_sites(
    code: bytes,
    code_va: int,
    target_va: int,
) -> tuple[int, ...]:
    """Find raw ``E8 rel32`` encodings that resolve to one virtual address."""
    sites = []
    for offset in range(len(code) - 4):
        if code[offset] != 0xE8:
            continue
        displacement = struct.unpack_from("<i", code, offset + 1)[0]
        call_va = code_va + offset
        if call_va + 5 + displacement == target_va:
            sites.append(call_va)
    return tuple(sites)


def _has_at(
    code: bytes,
    code_va: int,
    address: int,
    expected: bytes,
) -> bool:
    offset = address - code_va
    return (
        0 <= offset <= len(code) - len(expected)
        and code[offset : offset + len(expected)] == expected
    )


def audit_eye_callsite(
    text: bytes,
    text_va: int,
    initializer_va: int = 0x0061ED60,
) -> EyeCallsiteAudit:
    """Verify the 2025 caller's fixed position/index-only interface.

    The signatures are deliberately exact to the audited executable. They do
    not attempt general x86 decompilation; the planted unit test instead
    verifies address arithmetic and the conjunction of independent windows.
    """
    calls = relative_call_sites(text, text_va, initializer_va)
    if len(calls) != 1:
        return EyeCallsiteAudit(calls, None, False, False, False, False)
    call = calls[0]

    initializer_argument_signature = (
        _has_at(
            text,
            text_va,
            initializer_va + 0x2B,
            b"\x89\x55\x9c\x89\x4d\x98",
        )
        and _has_at(
            text,
            text_va,
            initializer_va + 0x46,
            b"\x8b\x45\x08\xc7\x45\xfc\x00\x00\x00\x00\x85\xc0",
        )
    )
    panel_index_loop_signature = (
        _has_at(text, text_va, call - 0x1CB, b"\x89\x45\xec")
        and _has_at(text, text_va, call - 0x9E, b"\x40\x89\x45\xec\x83\xf8\x09")
        and _has_at(text, text_va, call - 0x74, b"\xff\x75\xec")
    )
    side_filter_signature = (
        _has_at(text, text_va, call - 0x281, b"\x8b\xd9\x89\x5d\xe4")
        and _has_at(
            text,
            text_va,
            call - 0x1C8,
            bytes.fromhex(
                "83 e0 01 75 09 83 fb ff 0f 84 11 01 00 00 "
                "83 f8 01 75 08 3b d8 0f 84 04 01 00 00"
            ),
        )
    )
    coordinate_argument_signature = (
        _has_at(text, text_va, call - 0x18, b"\xf3\x0f\x2c\xd3")
        and _has_at(text, text_va, call - 0x04, b"\xf3\x0f\x2c\xca")
    )
    return EyeCallsiteAudit(
        calls,
        call,
        initializer_argument_signature,
        panel_index_loop_signature,
        side_filter_signature,
        coordinate_argument_signature,
    )
