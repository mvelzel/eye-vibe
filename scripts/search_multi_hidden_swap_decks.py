#!/usr/bin/env python3
"""Search common bases plus up to three formulaic hidden swaps.

Each plaintext action is ``base; swap(top, rank); hidden_1(rank); ...``.  The
three-stage search first retains bases with a good single-swap rule, then adds
all ordered second rules, and finally adds a third rule to the best pairs.
"""

from __future__ import annotations

import argparse
import heapq
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.deck_base_generic import (
    build_base_orbit_tables,
    decode_base_top_swap_hidden_sequence_with_tables,
)
from eye_mystery.deck_shuffles import standard_base_candidates
from search_hidden_swap_decks import REQUIRED_ENDS, hidden_rule
from search_standard_base_decks import mismatch_count


@dataclass(frozen=True)
class Rule:
    kind: str
    parameter: int

    @property
    def name(self) -> str:
        return f"{self.kind}-{self.parameter}"

    def build(self):
        if self.kind == "none":
            return lambda _position, _size: (1, 1)
        return hidden_rule(self.kind, self.parameter)


@dataclass(frozen=True)
class Result:
    mismatches: int
    unique: int
    base_name: str
    rules: tuple[Rule, ...]

    @property
    def key(self) -> tuple[int, int]:
        return self.mismatches, self.unique

    @property
    def name(self) -> str:
        suffix = "+".join(rule.name for rule in self.rules)
        return f"{self.base_name}+{suffix}"


def retain_best(
    heap: list[tuple[tuple[int, int], int, Result]],
    result: Result,
    limit: int,
    serial: int,
) -> None:
    reverse_key = (-result.mismatches, -result.unique)
    item = (reverse_key, serial, result)
    if len(heap) < limit:
        heapq.heappush(heap, item)
    elif item > heap[0]:
        heapq.heapreplace(heap, item)


def evaluate(base_name, tables, rules, messages) -> Result:
    built = tuple(rule.build() for rule in rules)
    streams = {
        name: (None,)
        + decode_base_top_swap_hidden_sequence_with_tables(
            message[1:], tables, built
        )
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
    return Result(mismatches, unique, base_name, tuple(rules))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-offset", type=int, default=12)
    parser.add_argument("--base-limit", type=int, default=50)
    parser.add_argument("--pair-limit", type=int, default=50)
    parser.add_argument("--output-limit", type=int, default=30)
    parser.add_argument("--stages", type=int, choices=(1, 2, 3), default=3)
    args = parser.parse_args()

    messages = {
        name: trigram_values(MESSAGES[name])[: REQUIRED_ENDS[name]]
        for name in MESSAGE_ORDER
    }
    rules = (Rule("none", 0), Rule("anchor", 0)) + tuple(
        Rule(kind, offset)
        for kind in ("ring", "mirror")
        for offset in range(1, args.max_offset + 1)
    )
    candidates = tuple(standard_base_candidates(83))
    maximum_steps = max(REQUIRED_ENDS.values())
    tables_by_name = {
        name: build_base_orbit_tables(base, maximum_steps)
        for name, base in candidates
    }

    # Keep one winner per base so many base geometries survive into the
    # combinatorial second stage.
    base_winners: list[Result] = []
    exact_base_winners: list[Result] = []
    tested = 0
    for base_name, _ in candidates:
        results = tuple(
            evaluate(
                base_name,
                tables_by_name[base_name],
                (rule,),
                messages,
            )
            for rule in rules
        )
        tested += len(rules)
        base_winners.append(min(results, key=lambda result: result.key))
        exact_base_winners.append(
            min(
                (
                    result
                    for result in results
                    if result.rules[0].kind != "none"
                ),
                key=lambda result: result.key,
            )
        )
    current = sorted(base_winners, key=lambda result: result.key)[
        : args.base_limit
    ]
    exact_current = sorted(
        exact_base_winners, key=lambda result: result.key
    )[: args.base_limit]
    selected_bases = {
        result.base_name for result in current + exact_current
    }
    print(
        f"stage=1 tested={tested} bases={len(selected_bases)} "
        f"best-up-to={current[0].mismatches}/{current[0].unique} "
        f"best-exact={exact_current[0].mismatches}/"
        f"{exact_current[0].unique}",
        flush=True,
    )

    if args.stages >= 2:
        pair_heap: list[tuple[tuple[int, int], int, Result]] = []
        exact_pair_heap: list[tuple[tuple[int, int], int, Result]] = []
        serial = 0
        for base_name in selected_bases:
            tables = tables_by_name[base_name]
            for first in rules:
                for second in rules:
                    result = evaluate(
                        base_name,
                        tables,
                        (first, second),
                        messages,
                    )
                    retain_best(
                        pair_heap, result, args.pair_limit, serial
                    )
                    if (
                        first.kind != "none"
                        and second.kind != "none"
                        and first != second
                    ):
                        retain_best(
                            exact_pair_heap,
                            result,
                            args.pair_limit,
                            serial,
                        )
                    serial += 1
        tested += serial
        current = sorted(
            (item[2] for item in pair_heap), key=lambda result: result.key
        )
        exact_current = sorted(
            (item[2] for item in exact_pair_heap),
            key=lambda result: result.key,
        )
        print(
            f"stage=2 tested={serial} survivors={len(current)} "
            f"best-up-to={current[0].mismatches}/{current[0].unique} "
            f"best-exact={exact_current[0].mismatches}/"
            f"{exact_current[0].unique}",
            flush=True,
        )

    if args.stages >= 3:
        triple_heap: list[tuple[tuple[int, int], int, Result]] = []
        serial = 0
        for seed in current:
            tables = tables_by_name[seed.base_name]
            for third in rules:
                result = evaluate(
                    seed.base_name,
                    tables,
                    seed.rules + (third,),
                    messages,
                )
                retain_best(
                    triple_heap, result, args.output_limit, serial
                )
                serial += 1
        exact_triple_heap: list[
            tuple[tuple[int, int], int, Result]
        ] = []
        for seed in exact_current:
            tables = tables_by_name[seed.base_name]
            for third in rules:
                if third.kind == "none" or third == seed.rules[-1]:
                    continue
                result = evaluate(
                    seed.base_name,
                    tables,
                    seed.rules + (third,),
                    messages,
                )
                retain_best(
                    exact_triple_heap,
                    result,
                    args.output_limit,
                    serial,
                )
                serial += 1
        tested += serial
        current = sorted(
            (item[2] for item in triple_heap),
            key=lambda result: result.key,
        )
        exact_current = sorted(
            (item[2] for item in exact_triple_heap),
            key=lambda result: result.key,
        )
        print(
            f"stage=3 tested={serial} survivors={len(current)} "
            f"best-up-to={current[0].mismatches}/{current[0].unique} "
            f"best-exact={exact_current[0].mismatches}/"
            f"{exact_current[0].unique}",
            flush=True,
        )

    print(f"total tested={tested}")
    print("exact-stage mismatch unique model")
    for result in exact_current[: args.output_limit]:
        print(f"{result.mismatches:>8} {result.unique:>6} {result.name}")
    print("up-to-stage mismatch unique model")
    for result in current[: args.output_limit]:
        print(f"{result.mismatches:>8} {result.unique:>6} {result.name}")


if __name__ == "__main__":
    main()
