"""Replay Aki's public 25-cell Eye automaton proposal.

The implementation is a literal Python port of ``automaton/init.lua`` and
``machine.lua`` in https://git.ignore.pl/noita-eyes.  It is kept separate from
the project models because this is a screen of an external proposal, not a
promoted decoder.
"""

from __future__ import annotations

from collections.abc import Sequence


SEED = "abcdefghijklm opqrstuvxyz"
# The older graph.lua encoder in the same public repository spells its first
# 13 cells differently.  It is retained as a source-authored variant, not a
# fitted alternative.
GRAPH_SEED = "abcdefghiwklm opqrstuvxyz"


def _clone(state: Sequence[str]) -> list[str]:
    return list(state)


def pivot(state: Sequence[str]) -> list[str]:
    new = _clone(state)
    new[9], new[2], new[11], new[18] = state[2], state[11], state[18], state[9]
    return new


def up(state: Sequence[str]) -> list[str]:
    new = _clone(state)
    for i in range(1, 10):  # Lua i=1..9
        new[15 + i] = state[i - 1]
    for i in range(2, 9):  # Lua i=2..8
        new[i - 1] = state[7 + i]
        new[7 + i] = state[15 + i]
    new[0] = state[16]
    new[8] = state[24]
    return new


def right(state: Sequence[str]) -> list[str]:
    new = _clone(state)
    new[0] = state[8]
    for i in range(2, 10):
        new[i - 1] = state[i - 2]
    new[9] = state[15]
    for i in range(11, 17):
        new[i - 1] = state[i - 2]
    new[16] = state[24]
    for i in range(18, 26):
        new[i - 1] = state[i - 2]
    return new


def down(state: Sequence[str]) -> list[str]:
    new = _clone(state)
    for i in range(1, 10):
        new[i - 1] = state[25 - i]
        new[25 - i] = state[i - 1]
    for i in range(1, 4):
        new[8 + i] = state[16 - i]
        new[16 - i] = state[8 + i]
    new[12] = state[12]
    return new


def left(state: Sequence[str]) -> list[str]:
    new = _clone(state)
    for i in range(1, 9):
        new[i - 1] = state[i]
    new[8] = state[0]
    for i in range(10, 16):
        new[i - 1] = state[i]
    new[15] = state[9]
    for i in range(17, 25):
        new[i - 1] = state[i]
    new[24] = state[16]
    return new


_ACTIONS = (pivot, up, right, down, left)


def decode(directions: Sequence[int], *, seed: str = SEED) -> str:
    """Return the two-slot output of the public automaton for one message."""

    if len(seed) != 25:
        raise ValueError("seed must contain 25 cells")
    if len(directions) % 3:
        raise ValueError("direction stream must contain complete trigrams")
    state = list(seed)
    output: list[str] = []
    for index in range(0, len(directions), 3):
        for eye in directions[index : index + 3]:
            if eye not in range(5):
                raise ValueError("eyes must be directions 0..4")
            state = _ACTIONS[eye](state)
        slot = 18 if (index // 3) % 3 == 1 else 2
        output.append(state[slot])
    return "".join(output)


def decode_all(messages: dict[str, Sequence[int]]) -> dict[str, str]:
    return {name: decode(stream) for name, stream in messages.items()}
