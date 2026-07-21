#!/usr/bin/env python3
"""Anneal unknown initial card labels for structured common-base deck models."""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.deck_base_generic import (
    build_base_orbit_tables,
    decode_base_top_swap_with_tables,
)
from eye_mystery.deck_shuffles import standard_base_candidates
from search_standard_base_decks import mismatch_count


DEFAULT_CANDIDATES = (
    "interleave-s41-L",
    "interleave-s42-R",
    "mongean-B-fwd",
    "mongean-T-fwd",
    "mongean-B-rev",
    "mongean-T-rev",
    "josephus-13",
    "josephus-42",
    "affine-82-fixed82-15-17",
    "affine-84-dummy-25-27",
)


@dataclass(frozen=True)
class OrderScore:
    objective: int
    mismatches: int
    unique: int
    coordinates: tuple[int, ...]


def score_order(
    messages,
    tables,
    coordinates,
    *,
    reset_marker: bool,
    unique_weight: int,
    mismatch_weight: int,
) -> OrderScore:
    if reset_marker:
        streams = {
            name: (None,)
            + decode_base_top_swap_with_tables(
                message[1:], tables, coordinates
            )
            for name, message in messages.items()
        }
    else:
        streams = {
            name: decode_base_top_swap_with_tables(
                message, tables, coordinates
            )
            for name, message in messages.items()
        }
    skipped = tuple(
        value for stream in streams.values() for value in stream[1:]
    )
    unique = len(set(skipped))
    mismatches, _ = mismatch_count(streams)
    return OrderScore(
        unique_weight * unique + mismatch_weight * mismatches,
        mismatches,
        unique,
        tuple(coordinates),
    )


def optimize(
    name,
    base,
    messages,
    *,
    restarts,
    iterations,
    seed,
    unique_weight,
    mismatch_weight,
    reset_marker,
    start_temperature,
    end_temperature,
):
    rng = random.Random(seed)
    tables = build_base_orbit_tables(base, max(map(len, messages.values())))
    overall = None
    for restart in range(restarts):
        coordinates = list(range(83))
        if restart:
            rng.shuffle(coordinates)
        current = score_order(
            messages,
            tables,
            coordinates,
            reset_marker=reset_marker,
            unique_weight=unique_weight,
            mismatch_weight=mismatch_weight,
        )
        best = current
        for iteration in range(iterations):
            left, right = rng.sample(range(83), 2)
            coordinates[left], coordinates[right] = (
                coordinates[right],
                coordinates[left],
            )
            proposal = score_order(
                messages,
                tables,
                coordinates,
                reset_marker=reset_marker,
                unique_weight=unique_weight,
                mismatch_weight=mismatch_weight,
            )
            progress = iteration / max(1, iterations - 1)
            temperature = start_temperature * (
                end_temperature / start_temperature
            ) ** progress
            accept = proposal.objective <= current.objective or rng.random() < math.exp(
                (current.objective - proposal.objective) / temperature
            )
            if accept:
                current = proposal
                if (current.objective, current.unique, current.mismatches) < (
                    best.objective,
                    best.unique,
                    best.mismatches,
                ):
                    best = current
            else:
                coordinates[left], coordinates[right] = (
                    coordinates[right],
                    coordinates[left],
                )
        if overall is None or best.objective < overall.objective:
            overall = best
        print(
            f"{name} restart={restart + 1} objective={best.objective} "
            f"unique={best.unique} mismatches={best.mismatches}",
            flush=True,
        )
    return overall


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", action="append")
    parser.add_argument("--restarts", type=int, default=3)
    parser.add_argument("--iterations", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=20260721)
    parser.add_argument("--unique-weight", type=int, default=8)
    parser.add_argument("--mismatch-weight", type=int, default=1)
    parser.add_argument("--start-temperature", type=float, default=12.0)
    parser.add_argument("--end-temperature", type=float, default=0.05)
    parser.add_argument(
        "--reset-marker",
        action="store_true",
        help="remove the checksum marker before resetting cipher state",
    )
    parser.add_argument(
        "--unique-only",
        action="store_true",
        help="optimize alphabet collapse alone with a calibrated temperature",
    )
    args = parser.parse_args()
    wanted = tuple(args.candidate or DEFAULT_CANDIDATES)
    all_candidates = dict(standard_base_candidates(83))
    missing = set(wanted) - set(all_candidates)
    if missing:
        raise SystemExit(f"unknown candidate names: {sorted(missing)}")
    messages = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    if args.unique_only:
        args.unique_weight = 1
        args.mismatch_weight = 0
        args.start_temperature = 2.0
        args.end_temperature = 0.01
    print(
        f"objective = {args.unique_weight} * distinct instructions after marker "
        f"+ {args.mismatch_weight} * mismatches"
    )
    for index, name in enumerate(wanted):
        result = optimize(
            name,
            all_candidates[name],
            messages,
            restarts=args.restarts,
            iterations=args.iterations,
            seed=args.seed + index,
            unique_weight=args.unique_weight,
            mismatch_weight=args.mismatch_weight,
            reset_marker=args.reset_marker,
            start_temperature=args.start_temperature,
            end_temperature=args.end_temperature,
        )
        assert result is not None
        print(
            f"BEST {name}: objective={result.objective} unique={result.unique} "
            f"mismatches={result.mismatches}"
        )
        print("coordinates:", " ".join(map(str, result.coordinates)))


if __name__ == "__main__":
    main()
