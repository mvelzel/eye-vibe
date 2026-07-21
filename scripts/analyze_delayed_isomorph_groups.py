#!/usr/bin/env python3
"""Look for a systematic two-symbol delayed-isomorphism signature.

All windows with the same informative equality pattern are grouped without a
plaintext guess.  For each group, the script measures how far the group stays
isomorphic before and after trimming one or two leading symbols.  If a rolling
two-plaintext-symbol update explains the Eyes generally, the famous six-window
gain should recur in independent high-confidence groups.

Groups are observational candidates, not proven repeated plaintext.  The scan
therefore reports replication and does not convert its rankings into p-values.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.isomorphs import pattern


@dataclass(frozen=True, order=True)
class Occurrence:
    message: str
    offset: int


@dataclass(frozen=True)
class GroupResult:
    base_length: int
    equality_pattern: str
    repeat_excess: int
    occurrences: tuple[Occurrence, ...]
    common_ends: tuple[int, int, int]

    @property
    def trim_two_gain(self) -> int:
        return self.common_ends[2] - self.common_ends[0]

    @property
    def relative_occurrence_signature(self) -> tuple[tuple[str, int], ...]:
        """Identify shifted views of the same multi-message episode."""

        origin = self.occurrences[0].offset
        return tuple(
            (item.message, item.offset - origin) for item in self.occurrences
        )


def streams() -> dict[str, tuple[int, ...]]:
    return {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }


def common_end(
    occurrences: tuple[Occurrence, ...],
    values: dict[str, tuple[int, ...]],
    *,
    trim: int,
    base_length: int,
) -> int:
    limit = min(
        len(values[item.message]) - item.offset for item in occurrences
    )
    end = base_length
    for candidate in range(base_length + 1, limit + 1):
        patterns = {
            pattern(
                values[item.message][
                    item.offset + trim : item.offset + candidate
                ]
            )
            for item in occurrences
        }
        if len(patterns) != 1:
            break
        end = candidate
    return end


def find_groups(
    *,
    base_length: int,
    minimum_occurrences: int,
    minimum_repeat_excess: int,
) -> tuple[GroupResult, ...]:
    values = streams()
    grouped: dict[str, list[Occurrence]] = defaultdict(list)
    excesses: dict[str, int] = {}
    for name in MESSAGE_ORDER:
        stream = values[name]
        for offset in range(len(stream) - base_length + 1):
            window = stream[offset : offset + base_length]
            excess = len(window) - len(set(window))
            if excess < minimum_repeat_excess:
                continue
            equality = pattern(window)
            grouped[equality].append(Occurrence(name, offset))
            excesses[equality] = excess

    results: list[GroupResult] = []
    for equality, raw_occurrences in grouped.items():
        occurrences = tuple(raw_occurrences)
        if len(occurrences) < minimum_occurrences:
            continue
        ends = (
            common_end(
                occurrences, values, trim=0, base_length=base_length
            ),
            common_end(
                occurrences, values, trim=1, base_length=base_length
            ),
            common_end(
                occurrences, values, trim=2, base_length=base_length
            ),
        )
        results.append(
            GroupResult(
                base_length,
                equality,
                excesses[equality],
                occurrences,
                ends,
            )
        )
    return tuple(results)


def scan_lengths(
    lengths: range,
    *,
    minimum_occurrences: int,
    minimum_repeat_excess: int,
) -> tuple[GroupResult, ...]:
    """Combine scans across seed lengths without hiding nested windows."""

    return tuple(
        result
        for base_length in lengths
        for result in find_groups(
            base_length=base_length,
            minimum_occurrences=minimum_occurrences,
            minimum_repeat_excess=minimum_repeat_excess,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-length", type=int, default=9)
    parser.add_argument("--maximum-base-length", type=int)
    parser.add_argument("--minimum-occurrences", type=int, default=3)
    parser.add_argument("--minimum-repeat-excess", type=int, default=2)
    args = parser.parse_args()

    maximum = args.maximum_base_length or args.base_length
    if maximum < args.base_length:
        raise SystemExit("maximum base length must not precede base length")
    results = scan_lengths(
        range(args.base_length, maximum + 1),
        minimum_occurrences=args.minimum_occurrences,
        minimum_repeat_excess=args.minimum_repeat_excess,
    )
    print(f"groups={len(results)}")
    positive_signatures = {
        item.relative_occurrence_signature
        for item in results
        if item.trim_two_gain > 0
    }
    print(
        "positive-delayed-gain-episodes="
        f"{len(positive_signatures)} (shift-collapsed)"
    )
    for result in sorted(
        results,
        key=lambda item: (
            -item.trim_two_gain,
            -len(item.occurrences),
            -item.repeat_excess,
            item.equality_pattern,
        ),
    ):
        locations = ",".join(
            f"{item.message}:{item.offset}" for item in result.occurrences
        )
        print(
            f"gain2={result.trim_two_gain:>2} "
            f"ends={result.common_ends} occurrences={len(result.occurrences)} "
            f"excess={result.repeat_excess} "
            f"pattern={result.equality_pattern} locations={locations}"
        )


if __name__ == "__main__":
    main()
