#!/usr/bin/env python3
"""Incrementally optimize sdlwdr #3 under a single-cycle progression."""

from __future__ import annotations

import argparse
import math
import random
import json
from pathlib import Path


SIZE = 83
ROOT = Path(__file__).resolve().parents[1]


def load_positions(skip_marker: bool) -> tuple[tuple[int, ...], ...]:
    data = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher3.json").read_text()
    )
    positions = [[] for _ in range(SIZE)]
    skip = int(skip_marker)
    for messages in data.values():
        for message in messages:
            for position, symbol in enumerate(message[skip:]):
                positions[symbol].append(position % SIZE)
    return tuple(tuple(items) for items in positions)


class State:
    def __init__(
        self, coordinates: list[int], positions: tuple[tuple[int, ...], ...]
    ) -> None:
        self.coordinates = coordinates
        self.positions = positions
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
            self._remove_value((coordinate - position) % SIZE)

    def _add_symbol(self, symbol: int) -> None:
        coordinate = self.coordinates[symbol]
        for position in self.positions[symbol]:
            self._add_value((coordinate - position) % SIZE)

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
    iterations: int,
) -> tuple[tuple[int, ...], int, int]:
    tail = list(range(1, SIZE))
    rng.shuffle(tail)
    state = State([0] + tail, positions)
    best = tuple(state.coordinates)
    best_unique = state.unique
    best_collisions = state.collisions
    current_cost = state.cost
    for iteration in range(iterations):
        left, right = rng.sample(range(1, SIZE), 2)
        state.swap(left, right)
        candidate_cost = state.cost
        progress = iteration / max(iterations - 1, 1)
        temperature = 1_500_000 * (250 / 1_500_000) ** progress
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
    parser.add_argument("--iterations", type=int, default=300_000)
    parser.add_argument("--restarts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    positions = load_positions(args.skip_marker)
    rng = random.Random(args.seed)
    overall = None
    overall_key = (SIZE + 1, 0)
    for restart in range(args.restarts):
        coordinates, unique, collisions = anneal(
            rng, positions, args.iterations
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
    print("coordinates=" + ",".join(map(str, overall)))


if __name__ == "__main__":
    main()
