"""Exact signed-path model for sdlwdr practice Cipher 3."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from random import Random
from typing import Literal


RAW_SIZE = 83
PLAIN_SIZE = 42
SignedPathMode = Literal["full", "primer"]


@dataclass(frozen=True)
class SignedPathResult:
    status: str
    mode: SignedPathMode
    mapping: tuple[int, ...] | None
    starts: tuple[int, ...] | None
    plaintexts: tuple[tuple[int, ...], ...] | None
    orientation: int | None = None
    offset: int | None = None
    valid_candidates: int = 0


def _validate_messages(messages: Sequence[Sequence[int]]) -> None:
    if not messages:
        raise ValueError("at least one message is required")
    if any(not message for message in messages):
        raise ValueError("messages must be nonempty")
    if any(value not in range(RAW_SIZE) for message in messages for value in message):
        raise ValueError("raw values must lie in 0..82")


def decode_signed_path(
    messages: Sequence[Sequence[int]],
    mapping: Sequence[int],
    mode: SignedPathMode,
    *,
    starts: Sequence[int] | None = None,
) -> tuple[tuple[int, ...], ...] | None:
    """Decode and reject a table as soon as a state leaves ``0..41``."""

    _validate_messages(messages)
    if sorted(mapping) != list(range(-(PLAIN_SIZE - 1), PLAIN_SIZE)):
        raise ValueError("mapping must permute -41..41")
    if mode not in ("full", "primer"):
        raise ValueError(f"unknown mode {mode!r}")
    if mode == "primer":
        if starts is None or len(starts) != len(messages):
            raise ValueError("primer mode needs one start per message")
    elif starts is not None:
        raise ValueError("full mode derives starts from first raw values")

    decoded = []
    for index, message in enumerate(messages):
        if mode == "full":
            state = mapping[message[0]]
            if state not in range(PLAIN_SIZE):
                return None
            plaintext = [state]
            body = message[1:]
        else:
            assert starts is not None
            state = starts[index]
            if state not in range(PLAIN_SIZE):
                return None
            plaintext = []
            body = message[1:]
        for value in body:
            state += mapping[value]
            if state not in range(PLAIN_SIZE):
                return None
            plaintext.append(state)
        decoded.append(tuple(plaintext))
    return tuple(decoded)


def signed_path_catalog() -> tuple[tuple[int, int, tuple[int, ...]], ...]:
    """Return all 83 cuts in both authored-coordinate orientations."""

    return tuple(
        (
            orientation,
            offset,
            tuple(
                ((orientation * value + offset) % RAW_SIZE)
                - (PLAIN_SIZE - 1)
                for value in range(RAW_SIZE)
            ),
        )
        for orientation in (1, -1)
        for offset in range(RAW_SIZE)
    )


def primer_starts(
    messages: Sequence[Sequence[int]],
    mapping: Sequence[int],
) -> tuple[int, ...] | None:
    """Return one legal start per message, if every body fits width 42."""

    starts = []
    for message in messages:
        cumulative = 0
        minimum = 0
        maximum = 0
        for value in message[1:]:
            cumulative += mapping[value]
            minimum = min(minimum, cumulative)
            maximum = max(maximum, cumulative)
        if maximum - minimum >= PLAIN_SIZE:
            return None
        starts.append(-minimum)
    return tuple(starts)


def solve_signed_path(
    messages: Sequence[Sequence[int]],
    mode: SignedPathMode,
) -> SignedPathResult:
    """Exhaust the 166 authored-coordinate signed-path maps."""

    _validate_messages(messages)
    if mode not in ("full", "primer"):
        raise ValueError(f"unknown mode {mode!r}")
    survivors = []
    for orientation, offset, mapping in signed_path_catalog():
        starts = primer_starts(messages, mapping) if mode == "primer" else None
        if mode == "primer" and starts is None:
            continue
        plaintexts = decode_signed_path(messages, mapping, mode, starts=starts)
        if plaintexts is not None:
            survivors.append(
                (orientation, offset, mapping, starts, plaintexts)
            )
    if not survivors:
        return SignedPathResult("unsat", mode, None, None, None)
    orientation, offset, mapping, starts, plaintexts = survivors[0]
    return SignedPathResult(
        "sat",
        mode,
        mapping,
        starts,
        plaintexts,
        orientation,
        offset,
        len(survivors),
    )


def make_signed_path_plant(
    lengths: Sequence[int],
    mode: SignedPathMode,
    *,
    seed: int = 20260727,
    orientation: int = -1,
    offset: int = 17,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[int, ...],
    tuple[int, ...] | None,
]:
    """Build a same-length plant that uses every signed displacement."""

    if mode not in ("full", "primer"):
        raise ValueError(f"unknown mode {mode!r}")
    if not lengths or any(length < 2 for length in lengths):
        raise ValueError("plant lengths must all be at least two")
    needed = RAW_SIZE if mode == "primer" else RAW_SIZE - 1
    carrier = next(
        (index for index, length in enumerate(lengths) if length - 1 >= needed),
        None,
    )
    if carrier is None:
        raise ValueError("one message body must be long enough for full coverage")

    if orientation not in (1, -1) or offset not in range(RAW_SIZE):
        raise ValueError("plant map must be one catalog member")
    rng = Random(seed)
    mapping = list(
        next(
            mapping
            for sign, cut, mapping in signed_path_catalog()
            if (sign, cut) == (orientation, offset)
        )
    )
    raw_for_delta = {delta: raw for raw, delta in enumerate(mapping)}
    messages = []
    starts = []

    for message_index, length in enumerate(lengths):
        if message_index == carrier:
            initial = 0
            forced = [step for size in range(1, PLAIN_SIZE) for step in (size, -size)]
            if mode == "primer":
                forced.insert(0, 0)
        else:
            initial = rng.randrange(PLAIN_SIZE)
            forced = []

        if mode == "full":
            values = [raw_for_delta[initial]]
        else:
            values = [rng.randrange(RAW_SIZE)]
            starts.append(initial)

        state = initial
        for delta in forced:
            if len(values) >= length:
                break
            state += delta
            if state not in range(PLAIN_SIZE):
                raise AssertionError("forced signed path left the state line")
            values.append(raw_for_delta[delta])

        while len(values) < length:
            choices = list(range(-state, PLAIN_SIZE - state))
            delta = rng.choice(choices)
            state += delta
            values.append(raw_for_delta[delta])
        messages.append(tuple(values))

    return (
        tuple(messages),
        tuple(mapping),
        tuple(starts) if mode == "primer" else None,
    )


def flatten_groups(
    groups: Mapping[str, Sequence[Sequence[int]]],
    order: Sequence[str] = ("A", "B", "C"),
) -> tuple[tuple[int, ...], ...]:
    """Flatten author-labelled groups without changing message order."""

    return tuple(
        tuple(message)
        for group in order
        for message in groups[group]
    )
