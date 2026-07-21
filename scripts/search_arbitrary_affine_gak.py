#!/usr/bin/env python3
"""Beam-search an unrestricted AGL(1,83) group-autokey plaintext map."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values


@dataclass(frozen=True)
class State:
    multipliers: tuple[int, ...]  # zero means not assigned; valid values are 1..82
    hidden: int
    counts: tuple[int, ...]
    streams: tuple[tuple[int, ...], ...]

    @property
    def unique(self) -> int:
        return sum(count > 0 for count in self.counts)

    @property
    def coincidences(self) -> int:
        return sum(count * (count - 1) for count in self.counts)


def mode_parts(message, mode):
    if mode == "full":
        return 0, 1, message
    if mode == "primer":
        return message[0], 1, message[1:]
    if mode == "skip":
        return 0, 1, message[1:]
    if mode == "indicator-hidden":
        return 0, message[0], message[1:]
    if mode == "indicator-both":
        return message[0], message[0], message[1:]
    raise ValueError(mode)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="skip")
    parser.add_argument("--beam", type=int, default=2_000)
    parser.add_argument("--max-unique", type=int, default=40)
    parser.add_argument(
        "--hidden-order",
        type=int,
        choices=(41, 82),
        default=82,
        help="order of the affine multiplier subgroup",
    )
    args = parser.parse_args()
    messages = tuple(trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER)
    multiplier_choices = tuple(
        pow(2, exponent, 83)
        for exponent in range(0, 82, 82 // args.hidden_order)
    )
    states = [State((0,) * 83, 1, (0,) * 83, ((),) * len(messages))]
    completed = 0
    total = sum(len(mode_parts(message, args.mode)[2]) for message in messages)

    for message_index, message in enumerate(messages):
        previous, initial_hidden, body = mode_parts(message, args.mode)
        states = [
            State(state.multipliers, initial_hidden, state.counts, state.streams)
            for state in states
        ]
        for current in body:
            expanded = []
            for state in states:
                symbol = (current - previous) * state.hidden % 83
                assigned = state.multipliers[symbol]
                choices = (assigned,) if assigned else multiplier_choices
                for multiplier in choices:
                    mapping = state.multipliers
                    if not assigned:
                        mutable = list(mapping)
                        mutable[symbol] = multiplier
                        mapping = tuple(mutable)
                    counts = list(state.counts)
                    counts[symbol] += 1
                    streams = list(state.streams)
                    streams[message_index] += (symbol,)
                    expanded.append(
                        State(
                            mapping,
                            state.hidden * multiplier % 83,
                            tuple(counts),
                            tuple(streams),
                        )
                    )
            expanded = [state for state in expanded if state.unique <= args.max_unique]
            expanded.sort(key=lambda state: (state.unique, -state.coincidences))
            states = expanded[: args.beam]
            completed += 1
            previous = current
            if not states:
                print(f"beam exhausted after {completed}/{total} symbols")
                return
            if completed % 100 == 0:
                print(
                    f"{completed:>4}/{total}: best={states[0].unique} symbols; "
                    f"beam={len(states)}"
                )

    best = states[0]
    print(f"complete: {best.unique} decoded symbols")
    print("plaintext multiplier assignments:")
    for symbol, multiplier in enumerate(best.multipliers):
        if multiplier:
            print(f"  {symbol:>2}: {multiplier:>2}")
    print("streams:")
    for name, stream in zip(MESSAGE_ORDER, best.streams):
        print(f"{name:>5}: {' '.join(map(str, stream))}")


if __name__ == "__main__":
    main()
