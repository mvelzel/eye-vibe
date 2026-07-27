#!/usr/bin/env python3
"""Audit the Cipher 4 midpoint edit and its literal Eye transfer."""

from __future__ import annotations

from collections import Counter
from difflib import Match, SequenceMatcher
import json
from pathlib import Path

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.edit_diamond import (
    AdditiveDiamond,
    literal_edit_diamonds,
)
from eye_mystery.practice_cipher4 import cyclic_differences


ROOT = Path(__file__).resolve().parents[1]


def action_ranks() -> tuple[tuple[int, ...], ...]:
    messages = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher4.json").read_text()
    )
    return tuple(
        tuple(value - 22 for value in cyclic_differences(message))
        for message in messages
    )


def long_blocks(
    left: tuple[int, ...],
    right: tuple[int, ...],
    *,
    minimum: int = 10,
) -> tuple[Match, ...]:
    return tuple(
        block
        for block in SequenceMatcher(
            None, left, right, autojunk=False
        ).get_matching_blocks()
        if block.size >= minimum
    )


def rejoin_diamonds(
    streams: tuple[tuple[int, ...], ...],
) -> tuple[tuple[str, AdditiveDiamond], ...]:
    results = []
    for left_index in range(len(streams)):
        for right_index in range(left_index + 1, len(streams)):
            blocks = long_blocks(
                streams[left_index],
                streams[right_index],
            )
            for previous, following in zip(blocks, blocks[1:]):
                left_start = previous.a + previous.size
                right_start = previous.b + previous.size
                results.append(
                    (
                        f"P{left_index + 1}/P{right_index + 1} "
                        f"{left_start}:{following.a} "
                        f"{right_start}:{following.b}",
                        AdditiveDiamond(
                            streams[left_index][left_start : following.a],
                            streams[right_index][right_start : following.b],
                        ),
                    )
                )
    return tuple(results)


def midpoint_probability(
    left: tuple[int, ...],
    right: tuple[int, ...],
    *,
    midpoint: int,
) -> float:
    """Exact frequency-matched chance for a two-versus-one frozen branch."""

    left_counts = Counter(left)
    right_counts = Counter(right)
    favorable = 0
    total = 0
    for first, first_count in left_counts.items():
        for second, second_count in left_counts.items():
            ordered_ways = first_count * (
                second_count - int(first == second)
            )
            for third, third_count in right_counts.items():
                ways = ordered_ways * third_count
                total += ways
                favorable += ways * int(first + second - third == midpoint)
    return favorable / total


def normalized_ioc(values: tuple[int, ...], alphabet_size: int) -> float:
    counts = Counter(values)
    total = len(values)
    return (
        alphabet_size
        * sum(count * (count - 1) for count in counts.values())
        / (total * (total - 1))
    )


def main() -> None:
    ranks = action_ranks()
    print("Cipher 4 additive rejoins in Z57")
    for name, diamond in rejoin_diamonds(ranks):
        print(
            f"  {name}: lengths={len(diamond.left)}/{len(diamond.right)} "
            f"solutions={diamond.neutral_solutions(57)} "
            f"sums={sum(diamond.left)}/{sum(diamond.right)}"
        )
    insertion = AdditiveDiamond((18, 22), (12,))
    print(
        "  frozen insertion: "
        f"solutions={insertion.neutral_solutions(57)} "
        f"midpoint_probability={midpoint_probability(ranks[0], ranks[1], midpoint=28):.12f}"
    )
    accumulated = []
    for stream in ranks:
        state = 0
        for rank in stream:
            state = (state + rank - 28) % 57
            accumulated.append(state)
    print(
        "  centered accumulation: "
        f"symbols={len(set(accumulated))}/57 "
        f"normalized_ioc={normalized_ioc(tuple(accumulated), 57):.12f}"
    )

    eyes = {
        name: trigram_values(MESSAGES[name])
        for name in MESSAGE_ORDER
    }
    eye_diamonds = literal_edit_diamonds(
        eyes,
        context_length=4,
        maximum_gap=8,
    )
    midpoint_hits = tuple(
        event
        for event in eye_diamonds
        if 41 in event.additive.neutral_solutions(83)
    )
    print(
        "Eyes literal short-edit transfer: "
        f"diamonds={len(eye_diamonds)} midpoint41={len(midpoint_hits)}"
    )


if __name__ == "__main__":
    main()
