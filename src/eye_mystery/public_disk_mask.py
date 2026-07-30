"""Literal replay of Aki's 2024 three-ring Eye disk mask proposal."""

from __future__ import annotations

from collections.abc import Sequence


# data/disk/eyes{1,2,3}.lua in https://git.ignore.pl/noita-eyes, commit
# 0b0e028 (2024-11-02). A zero keeps that eye digit; a one replaces it by 0.
RINGS: tuple[tuple[int, ...], ...] = (
    (0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1),
    (1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0),
    (0,) * 24,
)


def decode(directions: Sequence[int]) -> str:
    """Apply the three periodic source-authored masks and ASCII32 framing."""

    if len(directions) % 3:
        raise ValueError("direction stream must contain complete trigrams")
    output: list[str] = []
    for offset in range(0, len(directions), 3):
        index = offset // 3
        a, b, c = directions[offset : offset + 3]
        values = (
            a if RINGS[0][index % len(RINGS[0])] == 0 else 0,
            b if RINGS[1][index % len(RINGS[1])] == 0 else 0,
            c if RINGS[2][index % len(RINGS[2])] == 0 else 0,
        )
        value = 25 * values[0] + 5 * values[1] + values[2]
        output.append(chr(32 + value))
    return "".join(output)
