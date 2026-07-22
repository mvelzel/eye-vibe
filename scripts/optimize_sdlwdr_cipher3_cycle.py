#!/usr/bin/env python3
"""Optimize sdlwdr #3 under a specified cycle progression layout."""

from __future__ import annotations

import argparse
import math
import random
import json
from pathlib import Path

from eye_mystery.permutation_progression import CycleLayout


SIZE = 83
ROOT = Path(__file__).resolve().parents[1]


def load_positions(
    skip_marker: bool,
    group_filter: str,
) -> tuple[tuple[tuple[int, ...], ...], dict[str, tuple[int, ...]]]:
    data = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher3.json").read_text()
    )
    positions = [[] for _ in range(SIZE)]
    skip = int(skip_marker)
    streams = {
        f"{group}{index}": tuple(message[skip:])
        for group, messages in data.items()
        if group_filter == "ALL" or group == group_filter
        for index, message in enumerate(messages)
    }
    for message in streams.values():
        for position, symbol in enumerate(message):
            # Raw positions matter when a cycle length does not divide 83.
            positions[symbol].append(position)
    return tuple(tuple(items) for items in positions), streams


class State:
    def __init__(
        self,
        coordinates: list[int],
        positions: tuple[tuple[int, ...], ...],
        layout: CycleLayout,
    ) -> None:
        self.coordinates = coordinates
        self.positions = positions
        self.layout = layout
        self.counts = [0] * SIZE
        self.unique = 0
        self.collisions = 0
        for symbol in range(SIZE):
            self._add_symbol(symbol)

    @property
    def cost(self) -> int:
        return self.unique * 1_000_000 - self.collisions

    def _remove_value(self, value: int) -> None:
        count = self.counts[value]
        self.collisions -= count - 1
        self.counts[value] = count - 1
        if count == 1:
            self.unique -= 1

    def _add_value(self, value: int) -> None:
        count = self.counts[value]
        if count == 0:
            self.unique += 1
        self.collisions += count
        self.counts[value] = count + 1

    def _remove_symbol(self, symbol: int) -> None:
        coordinate = self.coordinates[symbol]
        for position in self.positions[symbol]:
            self._remove_value(self.layout.decode_slot(coordinate, position))

    def _add_symbol(self, symbol: int) -> None:
        coordinate = self.coordinates[symbol]
        for position in self.positions[symbol]:
            self._add_value(self.layout.decode_slot(coordinate, position))

    def swap(self, left: int, right: int) -> None:
        self._remove_symbol(left)
        self._remove_symbol(right)
        self.coordinates[left], self.coordinates[right] = (
            self.coordinates[right],
            self.coordinates[left],
        )
        self._add_symbol(left)
        self._add_symbol(right)


def anneal(
    rng: random.Random,
    positions: tuple[tuple[int, ...], ...],
    layout: CycleLayout,
    iterations: int,
) -> tuple[tuple[int, ...], int, int]:
    coordinates = list(range(SIZE))
    rng.shuffle(coordinates)
    state = State(coordinates, positions, layout)
    best = tuple(state.coordinates)
    best_unique = state.unique
    best_collisions = state.collisions
    current_cost = state.cost
    for iteration in range(iterations):
        left, right = rng.sample(range(SIZE), 2)
        state.swap(left, right)
        candidate_cost = state.cost
        progress = iteration / max(iterations - 1, 1)
        # Until a decoded slot reaches zero, ``unique`` has no local
        # gradient.  The collision term is the deliberately smooth proxy: it
        # rewards concentrating events into fewer slots.  Its swap deltas are
        # normally in the tens/hundreds, so the old million-scale schedule
        # was effectively a random walk for almost the entire run.
        temperature = 2_000 * (0.05 / 2_000) ** progress
        delta = candidate_cost - current_cost
        if delta <= 0 or rng.random() < math.exp(
            -min(delta, 20_000_000) / max(temperature, 1e-9)
        ):
            current_cost = candidate_cost
            if (state.unique, -state.collisions) < (
                best_unique,
                -best_collisions,
            ):
                best = tuple(state.coordinates)
                best_unique = state.unique
                best_collisions = state.collisions
        else:
            state.swap(left, right)
    return best, best_unique, best_collisions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-marker", action="store_true")
    parser.add_argument("--cycle-lengths", default="83")
    parser.add_argument("--group", choices=("ALL", "A", "B", "C"), default="ALL")
    parser.add_argument("--iterations", type=int, default=300_000)
    parser.add_argument("--restarts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    cycle_lengths = tuple(map(int, args.cycle_lengths.split(",")))
    layout = CycleLayout(cycle_lengths)
    if layout.size != SIZE:
        raise SystemExit("cycle lengths must sum to 83")
    positions, streams = load_positions(args.skip_marker, args.group)
    rng = random.Random(args.seed)
    overall = None
    overall_key = (SIZE + 1, 0)
    for restart in range(args.restarts):
        coordinates, unique, collisions = anneal(
            rng, positions, layout, args.iterations
        )
        print(
            f"restart={restart} unique={unique} collisions={collisions}",
            flush=True,
        )
        if (unique, -collisions) < overall_key:
            overall = coordinates
            overall_key = (unique, -collisions)
    assert overall is not None
    print(f"best unique={overall_key[0]} collisions={-overall_key[1]}")
    print(f"cycles={cycle_lengths}")
    print(f"group={args.group}")
    print("coordinates=" + ",".join(map(str, overall)))
    alphabet = sorted(
        {
            layout.decode_slot(overall[symbol], position)
            for stream in streams.values()
            for position, symbol in enumerate(stream)
        }
    )
    print("alphabet=" + ",".join(map(str, alphabet)))
    if len(alphabet) <= 42:
        for name, stream in streams.items():
            decoded = tuple(
                layout.decode_slot(overall[symbol], position)
                for position, symbol in enumerate(stream)
            )
            print(f"{name}: " + " ".join(map(str, decoded)))


if __name__ == "__main__":
    main()
