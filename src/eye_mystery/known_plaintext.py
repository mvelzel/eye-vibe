"""Key-free validation of plaintext candidates for perfectly isomorphic ciphers."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Hashable, Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.isomorphs import pattern


@dataclass(frozen=True)
class PlaintextOccurrence:
    message: str
    position: int
    ciphertext_pattern: str


@dataclass(frozen=True)
class IsomorphismConflict:
    plaintext: tuple[Hashable, ...]
    occurrences: tuple[PlaintextOccurrence, ...]


def first_isomorphism_conflict(
    plaintexts: Mapping[str, Sequence[Hashable]],
    ciphertexts: Mapping[str, Sequence[int]],
    *,
    min_length: int = 2,
    max_length: int | None = None,
) -> IsomorphismConflict | None:
    """Find the shortest repeated plaintext with inconsistent CT patterns.

    In a perfectly isomorphic cipher, every occurrence of the same plaintext
    sequence must produce the same ciphertext equality pattern, regardless of
    its initial state.  A disagreement is therefore a key-independent
    contradiction for the proposed plaintext/cipher pairing.
    """

    if set(plaintexts) != set(ciphertexts):
        raise ValueError("plaintext and ciphertext message names must match")
    if min_length < 1:
        raise ValueError("minimum length must be positive")
    for name in plaintexts:
        if len(plaintexts[name]) != len(ciphertexts[name]):
            raise ValueError(f"length mismatch for {name}")
    longest = max((len(text) for text in plaintexts.values()), default=0)
    stop = longest if max_length is None else min(max_length, longest)

    for length in range(min_length, stop + 1):
        locations: dict[
            tuple[Hashable, ...], list[tuple[str, int]]
        ] = defaultdict(list)
        for name, plaintext in plaintexts.items():
            for position in range(len(plaintext) - length + 1):
                fragment = tuple(plaintext[position : position + length])
                locations[fragment].append((name, position))

        for fragment, occurrences in locations.items():
            if len(occurrences) < 2:
                continue
            annotated = tuple(
                PlaintextOccurrence(
                    message=name,
                    position=position,
                    ciphertext_pattern=pattern(
                        ciphertexts[name][position : position + length]
                    ),
                )
                for name, position in occurrences
            )
            if len(
                {item.ciphertext_pattern for item in annotated}
            ) > 1:
                return IsomorphismConflict(fragment, annotated)
    return None
