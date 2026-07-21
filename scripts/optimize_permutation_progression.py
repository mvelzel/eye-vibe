#!/usr/bin/env python3
"""Heuristic search for the arbitrary permutation-progression eye model."""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from typing import Sequence

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.permutation_progression import encrypt_progression


@dataclass(frozen=True)
class Score:
    unique: int
    collisions: int

    @property
    def cost(self) -> int:
        # One fewer symbol must always beat any collision improvement.
        return self.unique * 1_000_000 - self.collisions


def cycle_coordinates(permutation: Sequence[int]):
    cycle_for = [()] * len(permutation)
    index_for = [0] * len(permutation)
    seen = [False] * len(permutation)
    for start in range(len(permutation)):
        if seen[start]:
            continue
        cycle = []
        value = start
        while not seen[value]:
            seen[value] = True
            cycle.append(value)
            value = permutation[value]
        cycle_tuple = tuple(cycle)
        for index, value in enumerate(cycle_tuple):
            cycle_for[value] = cycle_tuple
            index_for[value] = index
    return cycle_for, index_for


def score(
    permutation: Sequence[int], occurrences: Sequence[tuple[int, int]]
) -> Score:
    cycle_for, index_for = cycle_coordinates(permutation)
    counts = [0] * len(permutation)
    for position, symbol in occurrences:
        cycle = cycle_for[symbol]
        decoded = cycle[(index_for[symbol] - position) % len(cycle)]
        counts[decoded] += 1
    nonzero = [count for count in counts if count]
    collisions = sum(count * (count - 1) // 2 for count in nonzero)
    return Score(len(nonzero), collisions)


def eye_occurrences(reset_marker: bool) -> tuple[tuple[int, int], ...]:
    skip = 1 if reset_marker else 0
    return tuple(
        (position, symbol)
        for name in MESSAGE_ORDER
        for position, symbol in enumerate(trigram_values(MESSAGES[name])[skip:])
    )


def synthetic_occurrences(
    rng: random.Random,
    permutation: Sequence[int],
    alphabet_size: int,
) -> tuple[tuple[int, int], ...]:
    lengths = [len(trigram_values(MESSAGES[name])) - 1 for name in MESSAGE_ORDER]
    occurrences = []
    for length in lengths:
        plaintext = tuple(rng.randrange(alphabet_size) for _ in range(length))
        ciphertext = encrypt_progression(plaintext, permutation)
        occurrences.extend(enumerate(ciphertext))
    return tuple(occurrences)


def anneal(
    rng: random.Random,
    initial: Sequence[int],
    occurrences: Sequence[tuple[int, int]],
    iterations: int,
    start_temperature: float,
    end_temperature: float,
) -> tuple[tuple[int, ...], Score]:
    current = list(initial)
    current_score = score(current, occurrences)
    best = tuple(current)
    best_score = current_score
    for iteration in range(iterations):
        left, right = rng.sample(range(len(current)), 2)
        current[left], current[right] = current[right], current[left]
        candidate_score = score(current, occurrences)
        progress = iteration / max(1, iterations - 1)
        temperature = start_temperature * (
            end_temperature / start_temperature
        ) ** progress
        delta = candidate_score.cost - current_score.cost
        accept = delta <= 0 or rng.random() < math.exp(
            -min(delta, 10_000_000) / max(temperature, 1e-9)
        )
        if accept:
            current_score = candidate_score
            if candidate_score.cost < best_score.cost:
                best = tuple(current)
                best_score = candidate_score
        else:
            current[left], current[right] = current[right], current[left]
    return best, best_score


def steepest(
    initial: Sequence[int],
    occurrences: Sequence[tuple[int, int]],
    rounds: int,
) -> tuple[tuple[int, ...], Score]:
    current = list(initial)
    current_score = score(current, occurrences)
    for round_number in range(1, rounds + 1):
        best_swap = None
        best_score = current_score
        for left in range(len(current) - 1):
            for right in range(left + 1, len(current)):
                current[left], current[right] = current[right], current[left]
                candidate_score = score(current, occurrences)
                current[left], current[right] = current[right], current[left]
                if candidate_score.cost < best_score.cost:
                    best_score = candidate_score
                    best_swap = (left, right)
        if best_swap is None:
            print(f"steepest round={round_number} local optimum {current_score}")
            break
        left, right = best_swap
        current[left], current[right] = current[right], current[left]
        current_score = best_score
        print(f"steepest round={round_number} score={current_score}")
    return tuple(current), current_score


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--restarts", type=int, default=4)
    parser.add_argument("--iterations", type=int, default=20_000)
    parser.add_argument("--start-temperature", type=float, default=2_000_000.0)
    parser.add_argument("--end-temperature", type=float, default=1_000.0)
    parser.add_argument("--full-marker", action="store_true")
    parser.add_argument("--random-start", action="store_true")
    parser.add_argument("--steepest-rounds", type=int, default=0)
    parser.add_argument("--synthetic-alphabet", type=int, default=0)
    parser.add_argument("--synthetic-swaps", type=int, default=0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)
    planted = list(range(83))
    rng.shuffle(planted)

    if args.synthetic_alphabet:
        occurrences = synthetic_occurrences(
            rng, planted, args.synthetic_alphabet
        )
        initial = planted.copy()
        for _ in range(args.synthetic_swaps):
            left, right = rng.sample(range(83), 2)
            initial[left], initial[right] = initial[right], initial[left]
        print(
            f"synthetic planted={score(planted, occurrences)} "
            f"initial={score(initial, occurrences)} swaps={args.synthetic_swaps}"
        )
    else:
        occurrences = eye_occurrences(not args.full_marker)
        initial = list(range(83))
        print(
            f"eye marker_mode={'full' if args.full_marker else 'reset'} "
            f"identity={score(initial, occurrences)}"
        )

    overall_permutation = tuple(initial)
    overall_score = score(initial, occurrences)
    for restart in range(args.restarts):
        start = initial.copy()
        if args.random_start or restart:
            rng.shuffle(start)
        candidate, candidate_score = anneal(
            rng,
            start,
            occurrences,
            args.iterations,
            args.start_temperature,
            args.end_temperature,
        )
        print(f"restart={restart} score={candidate_score}")
        if candidate_score.cost < overall_score.cost:
            overall_permutation = candidate
            overall_score = candidate_score

    if args.steepest_rounds:
        overall_permutation, overall_score = steepest(
            overall_permutation, occurrences, args.steepest_rounds
        )
    print(f"best={overall_score}")
    print("permutation=" + ",".join(map(str, overall_permutation)))


if __name__ == "__main__":
    main()
