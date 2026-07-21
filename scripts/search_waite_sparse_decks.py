#!/usr/bin/env python3
"""Search finite reset-deck families against the Waite East-2 body crib.

The candidate fills the 117-symbol East-2 body with the contiguous Waite text
ending in the proposed ``SUBLIME ... LOWEST.`` sentence.  Every standard
83-card base is tested with a top swap alone and with small, fixed hidden-swap
rules.  A decoded stream fits only if one injective substitution maps its
symbols to all candidate characters.

This is a finite rejection test for these concrete deck families, not a test
of arbitrary GAK or XGAK.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import heapq

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.deck_base_generic import (
    build_base_orbit_tables,
    decode_base_top_swap_hidden_with_tables,
    decode_base_top_swap_with_tables,
)
from eye_mystery.deck_shuffles import standard_base_candidates


WAITE_M3_BODY = (
    "TS AND YOU WILL HAVE WHAT YOU SEEK. SUBLIME THAT WHICH IS THE LOWEST, "
    "AND MAKE THAT WHICH IS THE HIGHEST, THE LOWEST."
)


@dataclass(frozen=True)
class Result:
    conflicts: int
    same_plaintext_conflicts: int
    distinct_plaintext_conflicts: int
    base_name: str
    rule_name: str

    @property
    def key(self) -> tuple[int, int, int, str, str]:
        return (
            self.conflicts,
            self.same_plaintext_conflicts,
            self.distinct_plaintext_conflicts,
            self.base_name,
            self.rule_name,
        )


def _pairs(count: int) -> int:
    return count * (count - 1) // 2


def relation_conflicts(
    plaintext: str,
    decoded: tuple[int, ...],
) -> tuple[int, int, int]:
    """Count equality relations that prevent an injective substitution."""

    if len(plaintext) != len(decoded):
        raise ValueError("plaintext and decoded lengths differ")

    by_plaintext: dict[str, Counter[int]] = defaultdict(Counter)
    by_decoded: dict[int, Counter[str]] = defaultdict(Counter)
    for symbol, value in zip(plaintext, decoded, strict=True):
        by_plaintext[symbol][value] += 1
        by_decoded[value][symbol] += 1

    same_conflicts = sum(
        _pairs(sum(counts.values()))
        - sum(_pairs(count) for count in counts.values())
        for counts in by_plaintext.values()
    )
    distinct_conflicts = sum(
        _pairs(sum(counts.values()))
        - sum(_pairs(count) for count in counts.values())
        for counts in by_decoded.values()
    )
    return (
        same_conflicts + distinct_conflicts,
        same_conflicts,
        distinct_conflicts,
    )


def hidden_rule(kind: str, parameter: int):
    if kind == "anchor":
        return lambda position, size: (1, 1 + position % (size - 1))
    if kind == "ring":
        return lambda position, size: (
            1 + position % (size - 1),
            1 + (position + parameter) % (size - 1),
        )
    if kind == "mirror":
        return lambda position, size: (
            1 + position % (size - 1),
            1 + (-position - parameter) % (size - 1),
        )
    raise ValueError(kind)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-offset", type=int, default=12)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    ciphertext = trigram_values(MESSAGES["east2"])[1:]
    if len(WAITE_M3_BODY) != len(ciphertext):
        raise SystemExit("Waite body and East-2 body lengths differ")

    candidates: list[tuple[str, tuple[int, ...]]] = []
    seen: set[tuple[int, ...]] = set()
    for name, base in (
        ("identity", tuple(range(83))),
        *standard_base_candidates(83),
    ):
        if base in seen:
            continue
        seen.add(base)
        candidates.append((name, base))

    variants = [("top-only", None)] + [
        ("anchor", hidden_rule("anchor", 0))
    ] + [
        (f"{kind}-{offset}", hidden_rule(kind, offset))
        for kind in ("ring", "mirror")
        for offset in range(1, args.max_offset + 1)
    ]

    best: list[tuple[tuple[int, int, int, str, str], Result]] = []
    exact: list[Result] = []
    tested = 0
    for base_name, base in candidates:
        tables = build_base_orbit_tables(base, len(ciphertext))
        for rule_name, rule in variants:
            if rule is None:
                decoded = decode_base_top_swap_with_tables(ciphertext, tables)
            else:
                decoded = decode_base_top_swap_hidden_with_tables(
                    ciphertext, tables, rule
                )
            conflicts, same_conflicts, distinct_conflicts = (
                relation_conflicts(WAITE_M3_BODY, decoded)
            )
            result = Result(
                conflicts,
                same_conflicts,
                distinct_conflicts,
                base_name,
                rule_name,
            )
            tested += 1
            if conflicts == 0:
                exact.append(result)
            reverse_key = (
                -conflicts,
                -same_conflicts,
                -distinct_conflicts,
                base_name,
                rule_name,
            )
            item = (reverse_key, result)
            if len(best) < args.limit:
                heapq.heappush(best, item)
            elif item > best[0]:
                heapq.heapreplace(best, item)

    print(
        f"bases={len(candidates)} variants={len(variants)} "
        f"tested={tested} exact={len(exact)} "
        f"required-same-relations="
        f"{sum(_pairs(count) for count in Counter(WAITE_M3_BODY).values())}"
    )
    print("conflicts same distinct base rule")
    for _, result in sorted(best, key=lambda item: item[1].key):
        print(
            f"{result.conflicts:>9} "
            f"{result.same_plaintext_conflicts:>4} "
            f"{result.distinct_plaintext_conflicts:>8} "
            f"{result.base_name} {result.rule_name}"
        )


if __name__ == "__main__":
    main()
