"""Reversible deck updates parameterized by the 83 Wall `you*` contexts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from eye_mystery.wall_83_masks import WORLD_VERTICAL_ORDER
from eye_mystery.wall_header_clue import expanded_you_contexts


UPDATE_FAMILIES = (
    "transpose-selected",
    "swap-selected-distance",
    "swap-top-distance",
    "reverse-distance-prefix",
    "rotate-distance-prefix",
    "rotate-full-distance",
)


def _letter_count(word: str) -> int:
    return sum(character.isalpha() for character in word)


def wall_parameter_tables(
    lines_by_id: Mapping[str, Sequence[str]],
) -> tuple[tuple[str, tuple[int, ...]], ...]:
    """Return the ten predeclared raw/zero-based Wall distance tables."""

    contexts = expanded_you_contexts(lines_by_id, WORLD_VERTICAL_ORDER)
    if any(
        context.previous is None or context.following is None
        for context in contexts
    ):
        raise ValueError("a Wall YOU context lacks an adjacent word")
    previous = tuple(_letter_count(context.previous or "") for context in contexts)
    following = tuple(_letter_count(context.following or "") for context in contexts)
    token = tuple(_letter_count(context.token) for context in contexts)
    raw_tables = (
        ("previous-length", previous),
        ("following-length", following),
        ("token-length", token),
        (
            "adjacent-length-sum",
            tuple(left + right for left, right in zip(previous, following, strict=True)),
        ),
        (
            "adjacent-length-difference",
            tuple(abs(left - right) for left, right in zip(previous, following, strict=True)),
        ),
    )
    return tuple(
        item
        for name, values in raw_tables
        for item in (
            (f"{name}/raw", values),
            (f"{name}/zero-based", tuple(max(0, value - 1) for value in values)),
        )
    )


def _apply_update(
    state: list[int],
    *,
    rank: int,
    distance: int,
    family: str,
) -> None:
    size = len(state)
    distance %= size
    if family == "transpose-selected":
        card = state.pop(rank)
        state.insert(max(0, rank - distance), card)
    elif family == "swap-selected-distance":
        state[rank], state[distance] = state[distance], state[rank]
    elif family == "swap-top-distance":
        state[0], state[distance] = state[distance], state[0]
    elif family == "reverse-distance-prefix":
        state[: distance + 1] = reversed(state[: distance + 1])
    elif family == "rotate-distance-prefix":
        prefix = state[: distance + 1]
        state[: distance + 1] = (prefix[-1], *prefix[:-1])
    elif family == "rotate-full-distance":
        state[:] = state[distance:] + state[:distance]
    else:
        raise ValueError(f"unknown Wall deck update: {family}")


def decode_labels(
    ciphertext: Sequence[int],
    initial_deck: Sequence[int],
    parameters: Sequence[int],
    *,
    family: str,
    parameter_index: str = "label",
) -> tuple[int, ...]:
    """Decode emitted labels to ranks and apply the source-driven update."""

    if parameter_index not in {"label", "rank"}:
        raise ValueError("parameter index must be label or rank")
    if len(initial_deck) != len(parameters):
        raise ValueError("deck and parameter table sizes differ")
    state = list(initial_deck)
    plaintext = []
    for label in ciphertext:
        rank = state.index(label)
        plaintext.append(rank)
        index = label if parameter_index == "label" else rank
        _apply_update(
            state,
            rank=rank,
            distance=parameters[index],
            family=family,
        )
    return tuple(plaintext)


def encode_ranks(
    plaintext: Sequence[int],
    initial_deck: Sequence[int],
    parameters: Sequence[int],
    *,
    family: str,
    parameter_index: str = "label",
) -> tuple[int, ...]:
    """Encode rank instructions to labels under the same reversible update."""

    if parameter_index not in {"label", "rank"}:
        raise ValueError("parameter index must be label or rank")
    if len(initial_deck) != len(parameters):
        raise ValueError("deck and parameter table sizes differ")
    state = list(initial_deck)
    ciphertext = []
    for rank in plaintext:
        if not 0 <= rank < len(state):
            raise ValueError("rank instruction is outside the deck")
        label = state[rank]
        ciphertext.append(label)
        index = label if parameter_index == "label" else rank
        _apply_update(
            state,
            rank=rank,
            distance=parameters[index],
            family=family,
        )
    return tuple(ciphertext)
