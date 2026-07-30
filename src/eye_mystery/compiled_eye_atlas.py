"""Decode the small five-frame Eye glyph atlas in the 2025 PE build.

The renderer method immediately before the packed message initializer builds
five 11x7 bitmap records.  The compiler stores each 64-bit bitmap word after
an XOR and add/with-carry obfuscation.  This module reproduces that local
representation only; it is not a proposed plaintext decoder.
"""

from __future__ import annotations

from collections.abc import Sequence


WORD_MASK = (1 << 64) - 1

# ``mov [ebp-0x4c], low`` / ``mov [ebp-0x48], high`` at 0x61e880.
OBFUSCATED_WORDS: tuple[int, ...] = (
    0x00C3019AAEFABCB8,
    0x00C3011D4681BCF8,
    0x00C3001AE684BCB8,
    0x00C700DD46F8BCB8,
    0x00C3015D4AFBBCB8,
)

XOR_MASK = 0x00C3250EB6C51DB5
ADD_MASK = 0x003163F62062820B
WIDTH = 11
HEIGHT = 7


def decode_words(words: Sequence[int] = OBFUSCATED_WORDS) -> tuple[int, ...]:
    """Undo the compiled XOR/add transform for each atlas frame."""
    return tuple(((word ^ XOR_MASK) + ADD_MASK) & WORD_MASK for word in words)


def decode_frame(word: int) -> tuple[int, ...]:
    """Return one frame as row-major 0/1 pixels.

    The image buffer is zero-initialized by the allocator.  The compiled
    method sets the three top-row center pixels, then consumes 55 low bits in
    five rows of eleven.  The final row remains transparent.
    """
    if not 0 <= word <= WORD_MASK:
        raise ValueError("frame word must be an unsigned 64-bit value")
    pixels = [0] * (WIDTH * HEIGHT)
    pixels[4:7] = [1, 1, 1]
    remaining = word
    for row in range(1, HEIGHT - 1):
        for column in range(WIDTH):
            pixels[row * WIDTH + column] = remaining & 1
            remaining >>= 1
    return tuple(pixels)


def atlas_frames() -> tuple[tuple[int, ...], ...]:
    """Return all five decoded row-major frames."""
    return tuple(decode_frame(word) for word in decode_words())


def render_frame(pixels: Sequence[int]) -> str:
    """Render one decoded frame as an ASCII diagnostic."""
    if len(pixels) != WIDTH * HEIGHT:
        raise ValueError("unexpected frame length")
    return "\n".join(
        "".join("#" if pixels[row * WIDTH + column] else "." for column in range(WIDTH))
        for row in range(HEIGHT)
    )
