#!/usr/bin/env python3
"""Beam search for a deck cipher whose letter shuffles use at most two swaps.

This tests the concrete model ``swap(top, letter_rank); swap(u_l, v_l)``.
The second swap is fixed per plaintext letter and is learned from the data.
The marker can either be treated as an ordinary encrypted symbol (``full``),
which lets its shuffle establish a message-specific hidden state, or discarded
as out-of-band metadata (``reset``).
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values


NO_SWAP = (-1, -1)


@dataclass(frozen=True)
class State:
    swaps: tuple[tuple[int, int], ...]
    decks: tuple[tuple[int, ...], ...]
    counts: tuple[int, ...]
    streams: tuple[tuple[int, ...], ...]
    mismatches: int

    @property
    def unique(self) -> int:
        return sum(count > 0 for count in self.counts)

    @property
    def coincidences(self) -> int:
        return sum(count * (count - 1) for count in self.counts)


def swap(deck: list[int], left: int, right: int) -> None:
    deck[left], deck[right] = deck[right], deck[left]


def advance(
    state: State,
    message_index: int,
    card: int,
    next_card: int | None,
    multiplier: int,
    offset: int,
    comparisons: tuple[tuple[int, int], ...],
) -> list[State]:
    previous = state.decks[message_index]
    deck = [previous[(multiplier * index + offset) % 83] for index in range(83)]
    rank = deck.index(card)
    swap(deck, 0, rank)
    mismatch_delta = sum(
        state.streams[other_message][other_position] != rank
        for other_message, other_position in comparisons
    )
    configured = state.swaps[rank]

    if configured != NO_SWAP:
        swap(deck, *configured)
        candidates = (configured,)
    else:
        candidates_set = {NO_SWAP}
        if next_card is not None:
            next_position = deck.index(next_card)
            # The useful branches are exactly the swaps that make the next
            # decoded rank reuse one already observed. Other arbitrary swaps
            # are indistinguishable from NO_SWAP until one endpoint is seen.
            for target, count in enumerate(state.counts):
                if count and target and next_position and target != next_position:
                    candidates_set.add((next_position, target))
        candidates = tuple(candidates_set)

    results = []
    for secondary in candidates:
        next_deck = deck.copy()
        if secondary != NO_SWAP:
            swap(next_deck, *secondary)
        swaps = list(state.swaps)
        swaps[rank] = secondary
        decks = list(state.decks)
        decks[message_index] = tuple(next_deck)
        counts = list(state.counts)
        counts[rank] += 1
        streams = list(state.streams)
        streams[message_index] += (rank,)
        results.append(
            State(
                tuple(swaps),
                tuple(decks),
                tuple(counts),
                tuple(streams),
                state.mismatches + mismatch_delta,
            )
        )
    return results


def comparison_pairs() -> tuple[
    tuple[tuple[str, int], tuple[str, int]], ...
]:
    """Published strong repeated-plaintext comparisons used by deck scans."""

    pairs: list[tuple[tuple[str, int], tuple[str, int]]] = []

    def add(anchor, anchor_start, other, other_start, length):
        pairs.extend(
            ((anchor, anchor_start + offset), (other, other_start + offset))
            for offset in range(length)
        )

    for anchor, others, length in (
        ("east1", ("west1", "east2"), 24),
        ("west2", ("east3", "west3"), 5),
        ("east4", ("west4", "east5"), 20),
    ):
        for other in others:
            add(anchor, 1, other, 1, length)
    for other_name, other_start in (
        ("west1", 64),
        ("east2", 39),
        ("east2", 74),
    ):
        add("west1", 34, other_name, other_start, 18)
    for other_start in (40, 68):
        add("west1", 40, "east1", other_start, 9)
    for other_name, other_start in (("west4", 71), ("east5", 69)):
        add("east4", 68, other_name, other_start, 30)
    return tuple(pairs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--beam", type=int, default=2_000)
    parser.add_argument("--max-unique", type=int, default=40)
    parser.add_argument("--max-mismatches", type=int, default=230)
    parser.add_argument("--multiplier", type=int, default=1)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument(
        "--marker-mode",
        choices=("full", "reset"),
        default="full",
        help="include the distinct first trigram, or discard it and reset",
    )
    args = parser.parse_args()
    position_shift = 1 if args.marker_mode == "reset" else 0
    messages = tuple(
        trigram_values(MESSAGES[name])[position_shift:]
        for name in MESSAGE_ORDER
    )
    initial_deck = tuple(range(83))
    states = [
        State(
            swaps=(NO_SWAP,) * 83,
            decks=(initial_deck,) * len(messages),
            counts=(0,) * 83,
            streams=((),) * len(messages),
            mismatches=0,
        )
    ]

    events = [
        (message_index, position)
        for position in range(max(map(len, messages)))
        for message_index, message in enumerate(messages)
        if position < len(message)
    ]
    event_order = {event: index for index, event in enumerate(events)}
    name_index = {name: index for index, name in enumerate(MESSAGE_ORDER)}
    comparisons_by_later: dict[
        tuple[int, int], list[tuple[int, int]]
    ] = {}
    for left, right in comparison_pairs():
        left_event = (name_index[left[0]], left[1] - position_shift)
        right_event = (name_index[right[0]], right[1] - position_shift)
        if event_order[left_event] > event_order[right_event]:
            left_event, right_event = right_event, left_event
        comparisons_by_later.setdefault(right_event, []).append(left_event)
    for event_index, (message_index, position) in enumerate(events):
        message = messages[message_index]
        card = message[position]
        next_card = message[position + 1] if position + 1 < len(message) else None
        expanded = []
        for state in states:
            expanded.extend(
                advance(
                    state,
                    message_index,
                    card,
                    next_card,
                    args.multiplier,
                    args.offset,
                    tuple(
                        comparisons_by_later.get(
                            (message_index, position), ()
                        )
                    ),
                )
            )
        expanded = [
            state
            for state in expanded
            if state.unique <= args.max_unique
            and state.mismatches <= args.max_mismatches
        ]
        expanded.sort(
            key=lambda state: (
                state.mismatches,
                state.unique,
                -state.coincidences,
            )
        )
        states = expanded[: args.beam]
        if not states:
            print(f"beam exhausted after {event_index + 1}/{len(events)} symbols")
            return
        if (event_index + 1) % 100 == 0:
            best = states[0]
            print(
                f"{event_index + 1:>4}/{len(events)}: "
                f"best={best.mismatches} mismatches/"
                f"{best.unique} ranks; beam={len(states)}"
            )

    best = states[0]
    print(
        f"complete: {best.mismatches}/230 mismatches; "
        f"{best.unique} decoded ranks"
    )
    print(
        "rank frequencies:",
        Counter({rank: count for rank, count in enumerate(best.counts) if count}).most_common(),
    )
    print("learned secondary swaps:")
    for rank, pair in enumerate(best.swaps):
        if pair != NO_SWAP:
            print(f"  {rank:>2}: {pair[0]:>2} <-> {pair[1]:>2}")
    print("rank streams:")
    for name, stream in zip(MESSAGE_ORDER, best.streams):
        print(f"{name:>5}: {' '.join(map(str, stream))}")


if __name__ == "__main__":
    main()
