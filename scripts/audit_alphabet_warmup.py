#!/usr/bin/env python3
"""Audit a discarded A-Z initializer on bounded GAK/deck families."""

from __future__ import annotations

import argparse
import heapq
from collections import Counter
from collections.abc import Callable, Iterator
from dataclasses import dataclass

from eye_mystery.affine_gak import decode_affine_gak_from_state
from eye_mystery.alphabet_warmup import (
    AlphabetWarmup,
    affine_state_after_warmup,
    alphabet_warmups,
    deck_coordinates_after_warmup,
)
from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.deck_base_generic import (
    build_base_orbit_tables,
    decode_base_top_swap_with_tables,
)
from eye_mystery.deck_shuffles import standard_base_candidates
from eye_mystery.metrics import index_of_coincidence
from search_standard_base_decks import mismatch_count
from search_keyword_initial_decks import affine_bases


def audited_warmups() -> tuple[AlphabetWarmup, ...]:
    """Return the canonical reset control followed by the three candidates."""

    return (AlphabetWarmup("no-warmup", ()), *alphabet_warmups())


@dataclass(frozen=True)
class Result:
    family: str
    key: str
    warmup: str
    marker_mode: str
    mismatches: int
    comparisons: int
    unique: int
    ioc: float

    @property
    def quality(self) -> tuple[int, int, float]:
        return self.mismatches, self.unique, -self.ioc


def marker_parts(
    message: tuple[int, ...],
    marker_mode: str,
    previous: int,
) -> tuple[tuple[int, ...], int]:
    if marker_mode == "full":
        return message, previous
    if marker_mode == "skip":
        return message[1:], previous
    if marker_mode == "primer":
        return message[1:], message[0]
    raise ValueError(f"unknown marker mode: {marker_mode}")


def affine_functions() -> Iterator[tuple[str, str, Callable[[int], int]]]:
    for linear in range(83):
        for offset in range(83):
            yield (
                "linear",
                f"{linear},{offset}",
                lambda value, a=linear, b=offset: a * value + b,
            )
    for generator in range(1, 83):
        yield (
            "power",
            str(generator),
            lambda value, g=generator: pow(g, value, 83),
        )
    for exponent in range(1, 82):
        yield (
            "monomial",
            str(exponent),
            lambda value, k=exponent: (
                1 if value == 0 else pow(value, k, 83)
            ),
        )
    for shift in range(83):
        yield (
            "reciprocal",
            str(shift),
            lambda value, s=shift: (
                0
                if (value + s) % 83 == 0
                else pow((value + s) % 83, -1, 83)
            ),
        )


def push_best(
    heap: list[tuple[tuple[float, ...], int, Result]],
    result: Result,
    serial: int,
    limit: int,
) -> None:
    heap_key = tuple(-value for value in result.quality)
    item = (heap_key, serial, result)
    if len(heap) < limit:
        heapq.heappush(heap, item)
    elif item > heap[0]:
        heapq.heapreplace(heap, item)


def audit_affine(
    messages: dict[str, tuple[int, ...]],
    *,
    limit: int,
) -> tuple[list[Result], Counter[tuple[str, str]], int]:
    best: list[tuple[tuple[float, ...], int, Result]] = []
    exact: Counter[tuple[str, str]] = Counter()
    serial = 0
    for family, key, multiplier in affine_functions():
        for warmup in audited_warmups():
            state = affine_state_after_warmup(warmup.plaintext, multiplier)
            if state is None:
                continue
            warm_previous, warm_hidden = state
            for marker_mode in ("full", "skip", "primer"):
                streams = {}
                valid = True
                for name, message in messages.items():
                    body, previous = marker_parts(
                        message,
                        marker_mode,
                        warm_previous,
                    )
                    decoded = decode_affine_gak_from_state(
                        body,
                        multiplier,
                        previous=previous,
                        hidden=warm_hidden,
                    )
                    if decoded is None:
                        valid = False
                        break
                    streams[name] = (
                        decoded
                        if marker_mode == "full"
                        else (None,) + decoded
                    )
                if not valid:
                    continue
                mismatches, comparisons = mismatch_count(streams)
                combined = tuple(
                    value
                    for stream in streams.values()
                    for value in stream
                    if value is not None
                )
                result = Result(
                    f"affine-{family}",
                    key,
                    warmup.name,
                    marker_mode,
                    mismatches,
                    comparisons,
                    len(set(combined)),
                    index_of_coincidence(combined, len(set(combined))),
                )
                if mismatches == 0:
                    exact[(warmup.name, marker_mode)] += 1
                push_best(best, result, serial, limit)
                serial += 1
    return (
        [item[2] for item in sorted(best, key=lambda item: item[2].quality)],
        exact,
        serial,
    )


def audit_decks(
    messages: dict[str, tuple[int, ...]],
    *,
    limit: int,
) -> tuple[list[Result], Counter[tuple[str, str]], int, int]:
    best: list[tuple[tuple[float, ...], int, Result]] = []
    exact: Counter[tuple[str, str]] = Counter()
    seen: set[tuple[int, ...]] = set()
    serial = 0
    bases = 0
    for base_name, base in (*affine_bases(), *standard_base_candidates(83)):
        if base in seen:
            continue
        seen.add(base)
        bases += 1
        tables = build_base_orbit_tables(base, max(map(len, messages.values())))
        for warmup in audited_warmups():
            coordinates = deck_coordinates_after_warmup(base, warmup.plaintext)
            for marker_mode in ("full", "skip"):
                if marker_mode == "full":
                    streams = {
                        name: decode_base_top_swap_with_tables(
                            message,
                            tables,
                            coordinates,
                        )
                        for name, message in messages.items()
                    }
                else:
                    streams = {
                        name: (None,)
                        + decode_base_top_swap_with_tables(
                            message[1:],
                            tables,
                            coordinates,
                        )
                        for name, message in messages.items()
                    }
                mismatches, comparisons = mismatch_count(streams)
                combined = tuple(
                    value
                    for stream in streams.values()
                    for value in stream
                    if value is not None
                )
                result = Result(
                    "base-top-swap",
                    base_name,
                    warmup.name,
                    marker_mode,
                    mismatches,
                    comparisons,
                    len(set(combined)),
                    index_of_coincidence(combined, len(set(combined))),
                )
                if mismatches == 0:
                    exact[(warmup.name, marker_mode)] += 1
                push_best(best, result, serial, limit)
                serial += 1
    return (
        [item[2] for item in sorted(best, key=lambda item: item[2].quality)],
        exact,
        serial,
        bases,
    )


def print_results(title: str, best: list[Result], exact, tested: int) -> None:
    print(title)
    print("tested:", tested, "zero-mismatch:", sum(exact.values()))
    print("zero-mismatch by warmup/marker:", dict(exact))
    print("mismatch compare unique ioc warmup marker family key")
    for result in best:
        print(
            f"{result.mismatches:>8} {result.comparisons:>7} "
            f"{result.unique:>6} {result.ioc:>7.4f} "
            f"{result.warmup:<20} {result.marker_mode:<6} "
            f"{result.family:<20} {result.key}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument(
        "--family",
        choices=("affine", "deck", "all"),
        default="all",
    )
    args = parser.parse_args()
    messages = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    if args.family in ("affine", "all"):
        best, exact, tested = audit_affine(messages, limit=args.limit)
        print_results("Affine GAK alphabet warm-up", best, exact, tested)
    if args.family in ("deck", "all"):
        best, exact, tested, bases = audit_decks(messages, limit=args.limit)
        print("\nbase permutations:", bases)
        print_results("Base/top-swap alphabet warm-up", best, exact, tested)


if __name__ == "__main__":
    main()
