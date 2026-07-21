"""A five-operation, 25-position permutation-automaton experiment.

The geometry is a compact 9/7/9 diamond.  Each raw eye direction permutes the
state; after every three transitions, an arbitrary position can be observed.
This tests the hypothesis that eyes are instructions acting on state rather
than literal base-5 digits.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

State = tuple[int, ...]


def _identity() -> State:
    return tuple(range(25))


def _pivot(state: State) -> State:
    result = list(state)
    result[9], result[2], result[11], result[18] = state[2], state[11], state[18], state[9]
    return tuple(result)


def _up(state: State) -> State:
    result = list(state)
    for index in range(9):
        result[16 + index] = state[index]
    for index in range(1, 8):
        result[index] = state[8 + index]
        result[8 + index] = state[16 + index]
    result[0] = state[16]
    result[8] = state[24]
    return tuple(result)


def _right(state: State) -> State:
    result = list(state)
    result[0] = state[8]
    for index in range(1, 9):
        result[index] = state[index - 1]
    result[9] = state[15]
    for index in range(10, 16):
        result[index] = state[index - 1]
    result[16] = state[24]
    for index in range(17, 25):
        result[index] = state[index - 1]
    return tuple(result)


def _down(state: State) -> State:
    result = list(state)
    for index in range(9):
        result[index] = state[24 - index]
        result[24 - index] = state[index]
    for index in range(3):
        result[9 + index] = state[15 - index]
        result[15 - index] = state[9 + index]
    result[12] = state[12]
    return tuple(result)


def _left(state: State) -> State:
    result = list(state)
    for index in range(8):
        result[index] = state[index + 1]
    result[8] = state[0]
    for index in range(9, 15):
        result[index] = state[index + 1]
    result[15] = state[9]
    for index in range(16, 24):
        result[index] = state[index + 1]
    result[24] = state[16]
    return tuple(result)


OPERATIONS: tuple[Callable[[State], State], ...] = (_pivot, _up, _right, _down, _left)


def trace(
    message: Sequence[int],
    up_order: tuple[int, int, int] = (0, 1, 2),
    down_order: tuple[int, int, int] | None = None,
) -> tuple[State, ...]:
    """Return the automaton state after each eye-trigram."""
    if len(message) % 3:
        raise ValueError("eye stream length must be divisible by three")
    down_order = up_order if down_order is None else down_order
    if sorted(up_order) != [0, 1, 2] or sorted(down_order) != [0, 1, 2]:
        raise ValueError("trigram orders must be permutations of (0, 1, 2)")
    state = _identity()
    states = []
    for offset in range(0, len(message), 3):
        order = up_order if (offset // 3) % 2 == 0 else down_order
        trigram = message[offset : offset + 3]
        for index in order:
            state = OPERATIONS[trigram[index]](state)
        states.append(state)
    return tuple(states)


def readout(states: Sequence[State], up_slot: int, down_slot: int | None = None) -> tuple[int, ...]:
    """Read one slot after each trigram, optionally alternating two slots."""
    down_slot = up_slot if down_slot is None else down_slot
    return readout_pattern(states, (up_slot, down_slot))


def readout_pattern(states: Sequence[State], slots: Sequence[int]) -> tuple[int, ...]:
    """Read slots in a repeated pattern after successive trigrams.

    Patrick O'Callahan's published gear-table proposal uses a period-three
    top/bottom/top pattern, whereas the earlier broad scan used a period-two
    top/bottom alternation.  Keeping the pattern explicit lets both claims be
    tested without conflating them.
    """
    if not slots:
        raise ValueError("slot pattern must not be empty")
    if any(not 0 <= slot < 25 for slot in slots):
        raise ValueError("slots must be between 0 and 24")
    return tuple(
        state[slots[index % len(slots)]]
        for index, state in enumerate(states)
    )


@dataclass(frozen=True)
class ScanResult:
    up_order: tuple[int, int, int]
    down_order: tuple[int, int, int]
    up_slot: int
    down_slot: int
    ioc: float
    unique: int
    doubles: int
