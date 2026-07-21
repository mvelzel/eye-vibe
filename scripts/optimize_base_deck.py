#!/usr/bin/env python3
"""Anneal an unrestricted common base for the top-swap deck model."""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from itertools import combinations

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.deck_base_generic import (
    build_base_orbit_tables,
    decode_base_top_swap_with_tables,
    encrypt_base_top_swap,
)
from eye_mystery.deck_shuffles import standard_base_candidates
from search_standard_base_decks import evaluate, mismatch_count


@dataclass(frozen=True)
class BaseScore:
    objective: int
    mismatches: int
    unique: int
    base: tuple[int, ...]


def score_base(
    base: tuple[int, ...],
    messages: dict[str, tuple[int, ...]],
    *,
    mismatch_weight: int,
    unique_weight: int,
) -> BaseScore:
    tables = build_base_orbit_tables(base, max(map(len, messages.values())))
    streams = {
        name: (None,)
        + decode_base_top_swap_with_tables(message[1:], tables)
        for name, message in messages.items()
    }
    mismatches, _ = mismatch_count(streams)
    unique = len(
        {
            value
            for stream in streams.values()
            for value in stream
            if value is not None
        }
    )
    return BaseScore(
        mismatch_weight * mismatches + unique_weight * unique,
        mismatches,
        unique,
        base,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--start",
        default="affine-82-fixed82-65-4",
        help="standard candidate name, or 'random'",
    )
    parser.add_argument("--restarts", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=20260721)
    parser.add_argument("--mismatch-weight", type=int, default=10)
    parser.add_argument("--unique-weight", type=int, default=1)
    parser.add_argument("--start-temperature", type=float, default=20.0)
    parser.add_argument("--end-temperature", type=float, default=0.05)
    parser.add_argument("--neutral-probability", type=float, default=0.05)
    parser.add_argument(
        "--steepest-rounds",
        type=int,
        default=0,
        help="use exhaustive best-swap descent for this many rounds",
    )
    parser.add_argument(
        "--synthetic-swaps",
        type=int,
        help="calibrate on planted 26-symbol data from this many swaps away",
    )
    args = parser.parse_args()

    rng = random.Random(args.seed)
    candidates = dict(standard_base_candidates(83))
    if args.start != "random" and args.start not in candidates:
        raise SystemExit(f"unknown standard base: {args.start}")
    messages = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    planted: tuple[int, ...] | None = None
    synthetic_start: tuple[int, ...] | None = None
    if args.synthetic_swaps is not None:
        mutable = list(range(83))
        rng.shuffle(mutable)
        planted = tuple(mutable)
        synthetic_start_values = list(planted)
        for _ in range(args.synthetic_swaps):
            left, right = rng.sample(range(83), 2)
            synthetic_start_values[left], synthetic_start_values[right] = (
                synthetic_start_values[right],
                synthetic_start_values[left],
            )
        synthetic_start = tuple(synthetic_start_values)
        messages = {
            name: (rng.randrange(83),)
            + encrypt_base_top_swap(
                tuple(rng.randrange(26) for _ in range(len(message) - 1)),
                planted,
            )
            for name, message in messages.items()
        }
        planted_score = score_base(
            planted,
            messages,
            mismatch_weight=args.mismatch_weight,
            unique_weight=args.unique_weight,
        )
        print(
            f"planted objective={planted_score.objective} "
            f"mismatches={planted_score.mismatches} "
            f"full_unique={planted_score.unique}",
            flush=True,
        )
    overall: BaseScore | None = None
    for restart in range(args.restarts):
        if synthetic_start is not None and restart == 0:
            base = synthetic_start
        elif args.start == "random" or restart:
            mutable = list(range(83))
            rng.shuffle(mutable)
            base = tuple(mutable)
        else:
            base = candidates[args.start]
        current = score_base(
            base,
            messages,
            mismatch_weight=args.mismatch_weight,
            unique_weight=args.unique_weight,
        )
        best = current
        accepted = 0
        if args.steepest_rounds:
            for round_index in range(args.steepest_rounds):
                neighbor = current
                for left, right in combinations(range(83), 2):
                    proposal_base = list(current.base)
                    proposal_base[left], proposal_base[right] = (
                        proposal_base[right],
                        proposal_base[left],
                    )
                    proposal = score_base(
                        tuple(proposal_base),
                        messages,
                        mismatch_weight=args.mismatch_weight,
                        unique_weight=args.unique_weight,
                    )
                    if (
                        proposal.objective,
                        proposal.mismatches,
                        proposal.unique,
                    ) < (
                        neighbor.objective,
                        neighbor.mismatches,
                        neighbor.unique,
                    ):
                        neighbor = proposal
                if neighbor.objective >= current.objective:
                    break
                current = neighbor
                best = current
                accepted += 1
                print(
                    f"round={round_index + 1} objective={best.objective} "
                    f"mismatches={best.mismatches} full_unique={best.unique}",
                    flush=True,
                )
            iteration_range = range(0)
        else:
            iteration_range = range(args.iterations)
        for iteration in iteration_range:
            left, right = rng.sample(range(83), 2)
            proposal_base = list(current.base)
            proposal_base[left], proposal_base[right] = (
                proposal_base[right],
                proposal_base[left],
            )
            proposal = score_base(
                tuple(proposal_base),
                messages,
                mismatch_weight=args.mismatch_weight,
                unique_weight=args.unique_weight,
            )
            progress = iteration / max(1, args.iterations - 1)
            temperature = args.start_temperature * (
                args.end_temperature / args.start_temperature
            ) ** progress
            if proposal.objective < current.objective:
                accept = True
            elif proposal.objective == current.objective:
                accept = rng.random() < args.neutral_probability
            else:
                accept = rng.random() < math.exp(
                    (current.objective - proposal.objective) / temperature
                )
            if accept:
                current = proposal
                accepted += 1
                if (
                    current.objective,
                    current.mismatches,
                    current.unique,
                ) < (best.objective, best.mismatches, best.unique):
                    best = current
        if overall is None or best.objective < overall.objective:
            overall = best
        print(
            f"restart={restart + 1} objective={best.objective} "
            f"mismatches={best.mismatches} full_unique={best.unique} "
            f"accepted={accepted}",
            flush=True,
        )

    assert overall is not None
    full = evaluate("annealed", overall.base, messages, reset_marker=True)
    print(
        f"BEST objective={overall.objective} mismatches={full.mismatches} "
        f"full_unique={full.unique} ioc={full.ioc:.6f}"
    )
    print("base:", " ".join(map(str, overall.base)))


if __name__ == "__main__":
    main()
