#!/usr/bin/env python3
"""Test whether sdlwdr practice cipher #4 reuses the Eye-message corpus.

The author's cyclic-group hint reduces each Cipher 4 portion to its first
ciphertext value followed by mod-83 adjacent differences.  If the equivalent
cipher alphabet order is standard, this is a fixed renaming of its plaintext
actions.  Equality patterns therefore survive even when that renaming is
unknown.

This script checks the resulting streams against the canonical Eye messages,
their adjacent differences, their raw direction digits, known whole-corpus
orders, and every concatenation of complete Eye messages with the required
length.  Matching is bijective in both directions: two windows match iff one
is obtainable from the other by a one-to-one symbol renaming.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import json
from pathlib import Path
from typing import Hashable, Iterable, Sequence

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.marker_orders import MARKER_TRIE_ORDER


MODULUS = 83
ROOT = Path(__file__).resolve().parents[1]
MARKER_TRAIL_ORDER = (
    "east5",
    "east1",
    "west1",
    "east2",
    "west2",
    "east3",
    "west3",
    "east4",
    "west4",
)
LF_BODY_ORDER = (
    "east5",
    "west3",
    "west4",
    "east3",
    "east4",
    "west2",
    "east2",
    "west1",
    "east1",
)
LF_REVERSE_ORDER = (
    "east1",
    "west1",
    "east2",
    "west2",
    "east4",
    "east3",
    "west4",
    "west3",
    "east5",
)


def adjacent_differences(values: Sequence[int]) -> tuple[int, ...]:
    """Return the identity-state action stream for a cyclic group."""

    if not values:
        return ()
    return (values[0],) + tuple(
        (right - left) % MODULUS for left, right in zip(values, values[1:])
    )


def isomorphic(left: Sequence[Hashable], right: Sequence[Hashable]) -> bool:
    """Return whether two equal-length sequences differ only by a bijection."""

    if len(left) != len(right):
        return False
    forward: dict[Hashable, Hashable] = {}
    reverse: dict[Hashable, Hashable] = {}
    for source, target in zip(left, right, strict=True):
        if source in forward and forward[source] != target:
            return False
        if target in reverse and reverse[target] != source:
            return False
        forward[source] = target
        reverse[target] = source
    return True


@dataclass(frozen=True, order=True)
class Match:
    length: int
    left_start: int
    right_start: int


def longest_isomorphic_substring(
    left: Sequence[Hashable], right: Sequence[Hashable]
) -> Match:
    """Find the longest pair of bijectively equivalent contiguous windows."""

    best = Match(0, 0, 0)
    for left_start in range(len(left)):
        if len(left) - left_start <= best.length:
            break
        for right_start in range(len(right)):
            limit = min(len(left) - left_start, len(right) - right_start)
            if limit <= best.length:
                continue
            forward: dict[Hashable, Hashable] = {}
            reverse: dict[Hashable, Hashable] = {}
            length = 0
            while length < limit:
                source = left[left_start + length]
                target = right[right_start + length]
                if source in forward and forward[source] != target:
                    break
                if target in reverse and reverse[target] != source:
                    break
                forward[source] = target
                reverse[target] = source
                length += 1
            candidate = Match(length, left_start, right_start)
            if candidate > best:
                best = candidate
    return best


def concatenated(
    streams: dict[str, tuple[int, ...]], order: Iterable[str]
) -> tuple[int, ...]:
    return tuple(value for name in order for value in streams[name])


def exact_length_orders(
    lengths: dict[str, int], target: int
) -> Iterable[tuple[str, ...]]:
    """Yield ordered, no-replacement message selections summing to target."""

    minimum = min(lengths.values())
    maximum_count = min(len(lengths), target // minimum)
    for count in range(1, maximum_count + 1):
        for names in product(lengths, repeat=count):
            if len(set(names)) != count:
                continue
            if sum(lengths[name] for name in names) == target:
                yield names


def eye_representations() -> dict[str, dict[str, tuple[int, ...]]]:
    absolute = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    bodies = {name: values[1:] for name, values in absolute.items()}
    differences = {
        name: adjacent_differences(values) for name, values in absolute.items()
    }
    body_differences = {
        name: adjacent_differences(values) for name, values in bodies.items()
    }
    raw = {name: MESSAGES[name] for name in MESSAGE_ORDER}
    return {
        "trigram": absolute,
        "trigram-body": bodies,
        "trigram-difference": differences,
        "trigram-body-difference": body_differences,
        "raw-directions": raw,
    }


def main() -> None:
    cipher_messages = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher4.json").read_text()
    )
    actions = tuple(adjacent_differences(message) for message in cipher_messages)
    representations = eye_representations()
    orders = {
        "canonical": MESSAGE_ORDER,
        "marker-trie": MARKER_TRIE_ORDER,
        "marker-trail": MARKER_TRAIL_ORDER,
        "lf-body": LF_BODY_ORDER,
        "lf-reverse": LF_REVERSE_ORDER,
    }

    print("Cipher 4 action lengths:", tuple(map(len, actions)))
    for representation, streams in representations.items():
        print(f"\n[{representation}]")
        lengths = {name: len(stream) for name, stream in streams.items()}
        for target in map(len, actions):
            candidates = list(exact_length_orders(lengths, target))
            matches = [
                names
                for names in candidates
                if any(
                    isomorphic(action, concatenated(streams, names))
                    for action in actions
                    if len(action) == target
                )
            ]
            print(
                f"length={target}: ordered whole-message candidates={len(candidates)}, "
                f"full isomorphic matches={matches}"
            )

        sources = {
            **{f"message:{name}": stream for name, stream in streams.items()},
            **{
                f"order:{name}": concatenated(streams, order)
                for name, order in orders.items()
            },
        }
        ranked: list[tuple[int, int, str, Match]] = []
        for action_index, action in enumerate(actions):
            for source_name, source in sources.items():
                match = longest_isomorphic_substring(action, source)
                ranked.append((match.length, action_index, source_name, match))
        for _, action_index, source_name, match in sorted(ranked, reverse=True)[:12]:
            print(
                f"portion={action_index} source={source_name} "
                f"longest={match.length} action_start={match.left_start} "
                f"source_start={match.right_start}"
            )


if __name__ == "__main__":
    main()
