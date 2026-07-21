#!/usr/bin/env python3
"""Search the progression model in a fixed permutation cycle structure."""

from __future__ import annotations

import argparse
import math
import random
from collections.abc import Sequence

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values

from optimize_permutation_progression import Score, eye_occurrences


def make_cycles(lengths: Sequence[int], labels: Sequence[int]):
    if sum(lengths) != len(labels) or any(length < 1 for length in lengths):
        raise ValueError("cycle lengths must be positive and sum to 83")
    cycles = []
    start = 0
    for length in lengths:
        cycles.append(list(labels[start : start + length]))
        start += length
    return cycles


def score_cycles(
    cycles: Sequence[Sequence[int]],
    occurrences: Sequence[tuple[int, int]],
) -> Score:
    cycle_for = [0] * 83
    index_for = [0] * 83
    for cycle_index, cycle in enumerate(cycles):
        for index, label in enumerate(cycle):
            cycle_for[label] = cycle_index
            index_for[label] = index
    counts: dict[tuple[int, int], int] = {}
    for position, symbol in occurrences:
        cycle_index = cycle_for[symbol]
        residue = (index_for[symbol] - position) % len(cycles[cycle_index])
        key = (cycle_index, residue)
        counts[key] = counts.get(key, 0) + 1
    collisions = sum(count * (count - 1) // 2 for count in counts.values())
    return Score(len(counts), collisions)


def swap_labels(cycles, left, right):
    left_cycle, left_index = left
    right_cycle, right_index = right
    cycles[left_cycle][left_index], cycles[right_cycle][right_index] = (
        cycles[right_cycle][right_index],
        cycles[left_cycle][left_index],
    )


def anneal(
    rng: random.Random,
    initial,
    occurrences,
    iterations: int,
    start_temperature: float,
    end_temperature: float,
):
    cycles = [cycle.copy() for cycle in initial]
    positions = [
        (cycle_index, index)
        for cycle_index, cycle in enumerate(cycles)
        for index in range(len(cycle))
    ]
    current_score = score_cycles(cycles, occurrences)
    best = [cycle.copy() for cycle in cycles]
    best_score = current_score
    for iteration in range(iterations):
        left, right = rng.sample(positions, 2)
        swap_labels(cycles, left, right)
        candidate_score = score_cycles(cycles, occurrences)
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
                best = [cycle.copy() for cycle in cycles]
                best_score = candidate_score
        else:
            swap_labels(cycles, left, right)
    return best, best_score


def steepest(cycles, occurrences, rounds: int):
    current = [cycle.copy() for cycle in cycles]
    positions = [
        (cycle_index, index)
        for cycle_index, cycle in enumerate(current)
        for index in range(len(cycle))
    ]
    current_score = score_cycles(current, occurrences)
    for round_number in range(1, rounds + 1):
        best_swap = None
        best_score = current_score
        for left_index, left in enumerate(positions[:-1]):
            for right in positions[left_index + 1 :]:
                swap_labels(current, left, right)
                candidate_score = score_cycles(current, occurrences)
                swap_labels(current, left, right)
                if candidate_score.cost < best_score.cost:
                    best_score = candidate_score
                    best_swap = (left, right)
        if best_swap is None:
            print(f"steepest round={round_number} local optimum {current_score}")
            break
        swap_labels(current, *best_swap)
        current_score = best_score
        print(f"steepest round={round_number} score={current_score}")
    return current, current_score


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycle-lengths", required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--restarts", type=int, default=4)
    parser.add_argument("--iterations", type=int, default=100_000)
    parser.add_argument("--start-temperature", type=float, default=2_000_000.0)
    parser.add_argument("--end-temperature", type=float, default=1_000.0)
    parser.add_argument("--full-marker", action="store_true")
    parser.add_argument("--synthetic-alphabet", type=int, default=0)
    parser.add_argument("--synthetic-swaps", type=int, default=0)
    parser.add_argument("--steepest-rounds", type=int, default=0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    lengths = tuple(map(int, args.cycle_lengths.split(",")))
    rng = random.Random(args.seed)
    labels = list(range(83))
    rng.shuffle(labels)
    planted = make_cycles(lengths, labels)

    if args.synthetic_alphabet:
        occurrences = []
        plain_labels = [
            (cycle_index, residue)
            for cycle_index, cycle in enumerate(planted)
            for residue in range(len(cycle))
        ][: args.synthetic_alphabet]
        for name in MESSAGE_ORDER:
            length = len(trigram_values(MESSAGES[name])) - 1
            for position in range(length):
                cycle_index, residue = rng.choice(plain_labels)
                cycle = planted[cycle_index]
                symbol = cycle[(residue + position) % len(cycle)]
                occurrences.append((position, symbol))
        occurrences = tuple(occurrences)
        initial = [cycle.copy() for cycle in planted]
        positions = [
            (cycle_index, index)
            for cycle_index, cycle in enumerate(initial)
            for index in range(len(cycle))
        ]
        for _ in range(args.synthetic_swaps):
            swap_labels(initial, *rng.sample(positions, 2))
        print(
            f"synthetic lengths={lengths} "
            f"planted={score_cycles(planted, occurrences)} "
            f"initial={score_cycles(initial, occurrences)}"
        )
    else:
        occurrences = eye_occurrences(not args.full_marker)
        initial = planted
        print(
            f"eye lengths={lengths} "
            f"marker_mode={'full' if args.full_marker else 'reset'} "
            f"initial={score_cycles(initial, occurrences)}"
        )

    overall = [cycle.copy() for cycle in initial]
    overall_score = score_cycles(initial, occurrences)
    for restart in range(args.restarts):
        start_labels = [label for cycle in initial for label in cycle]
        if restart:
            rng.shuffle(start_labels)
        start = make_cycles(lengths, start_labels)
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
            overall = candidate
            overall_score = candidate_score
    if args.steepest_rounds:
        overall, overall_score = steepest(
            overall, occurrences, args.steepest_rounds
        )
    print(f"best={overall_score}")
    print("cycles=" + " | ".join(",".join(map(str, c)) for c in overall))


if __name__ == "__main__":
    main()
