"""Exact completion facts for a partial permutation.

Repeated plaintext passages in a perfectly isomorphic cipher induce partial
permutations of the ciphertext alphabet.  These helpers quantify what is
forced before choosing arbitrary values for the unobserved edges.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class CompletionStats:
    alphabet_size: int
    observed_edges: int
    observed_fixed_points: int
    path_lengths: tuple[int, ...]
    cycle_lengths: tuple[int, ...]
    minimum_transpositions: int
    minimum_even_transpositions: int | None
    minimum_odd_transpositions: int | None
    minimum_support: int
    even_completion: bool
    odd_completion: bool


def validate_partial_permutation(
    mapping: Mapping[int, int], alphabet_size: int
) -> None:
    """Validate that ``mapping`` is an injection on ``range(alphabet_size)``."""

    if alphabet_size < 1:
        raise ValueError("alphabet size must be positive")
    if any(
        not 0 <= source < alphabet_size or not 0 <= target < alphabet_size
        for source, target in mapping.items()
    ):
        raise ValueError("partial-permutation value is outside the alphabet")
    if len(set(mapping.values())) != len(mapping):
        raise ValueError("partial permutation must be injective")


def _components(
    mapping: Mapping[int, int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return edge lengths of directed paths and vertex lengths of cycles."""

    domain = set(mapping)
    image = set(mapping.values())
    visited: set[int] = set()
    path_lengths: list[int] = []
    cycle_lengths: list[int] = []

    # Every non-cycle component has one vertex with no observed predecessor.
    for start in sorted(domain - image):
        value = start
        edges = 0
        while value in mapping:
            visited.add(value)
            value = mapping[value]
            edges += 1
        visited.add(value)
        path_lengths.append(edges)

    # What remains in the observed domain consists entirely of cycles.
    for start in sorted(domain - visited):
        if start in visited:
            continue
        value = start
        vertices = 0
        while value not in visited:
            visited.add(value)
            value = mapping[value]
            vertices += 1
        cycle_lengths.append(vertices)

    return tuple(sorted(path_lengths, reverse=True)), tuple(
        sorted(cycle_lengths, reverse=True)
    )


def completion_stats(
    mapping: Mapping[int, int], alphabet_size: int
) -> CompletionStats:
    """Return sharp completion bounds and the possible permutation signs.

    A forced path with ``k`` edges can be closed into a ``k + 1`` cycle at a
    cost of ``k`` transpositions.  A forced cycle on ``k`` vertices costs
    ``k - 1``.  Closing paths independently and fixing every unused point is
    optimal, so the reported transposition and support bounds are attainable.

    If at least two source values remain unassigned, two target assignments can
    be exchanged.  This flips the sign of the completion without changing any
    observed edge, proving that both even and odd completions
    exist.
    """

    validate_partial_permutation(mapping, alphabet_size)
    path_lengths, cycle_lengths = _components(mapping)
    observed_fixed_points = sum(
        source == target for source, target in mapping.items()
    )
    minimum_transpositions = sum(path_lengths) + sum(
        length - 1 for length in cycle_lengths
    )
    minimum_support = sum(length + 1 for length in path_lengths) + sum(
        length for length in cycle_lengths if length > 1
    )

    missing = alphabet_size - len(mapping)
    minimum_even = minimum_transpositions % 2 == 0
    if missing >= 2:
        even_completion = True
        odd_completion = True
    else:
        even_completion = minimum_even
        odd_completion = not minimum_even

    minimum_even_transpositions = None
    minimum_odd_transpositions = None
    if even_completion:
        minimum_even_transpositions = minimum_transpositions + (
            minimum_transpositions % 2
        )
    if odd_completion:
        minimum_odd_transpositions = minimum_transpositions + (
            1 - minimum_transpositions % 2
        )

    return CompletionStats(
        alphabet_size=alphabet_size,
        observed_edges=len(mapping),
        observed_fixed_points=observed_fixed_points,
        path_lengths=path_lengths,
        cycle_lengths=cycle_lengths,
        minimum_transpositions=minimum_transpositions,
        minimum_even_transpositions=minimum_even_transpositions,
        minimum_odd_transpositions=minimum_odd_transpositions,
        minimum_support=minimum_support,
        even_completion=even_completion,
        odd_completion=odd_completion,
    )


def permutation_is_even(permutation: Sequence[int]) -> bool:
    """Return the sign of a new-position-to-old-position permutation."""

    validate_partial_permutation(
        dict(enumerate(permutation)), len(permutation)
    )
    cycles = 0
    visited: set[int] = set()
    for start in range(len(permutation)):
        if start in visited:
            continue
        cycles += 1
        value = start
        while value not in visited:
            visited.add(value)
            value = permutation[value]
    return (len(permutation) - cycles) % 2 == 0


def complete_partial_permutation(
    mapping: Mapping[int, int],
    alphabet_size: int,
    *,
    even: bool | None = None,
) -> tuple[int, ...]:
    """Construct a minimum-distance completion, optionally of a given sign."""

    validate_partial_permutation(mapping, alphabet_size)
    result = dict(mapping)
    domain = set(mapping)
    image = set(mapping.values())

    # Close every observed path into its own cycle.
    for start in sorted(domain - image):
        end = start
        while end in mapping:
            end = mapping[end]
        result[end] = start

    # Every wholly unobserved point is fixed in the minimum completion.
    for value in range(alphabet_size):
        result.setdefault(value, value)

    permutation = tuple(result[index] for index in range(alphabet_size))
    if even is None or permutation_is_even(permutation) == even:
        return permutation

    missing_sources = sorted(set(range(alphabet_size)) - domain)
    if len(missing_sources) < 2:
        raise ValueError("the requested completion sign is impossible")
    left, right = missing_sources[:2]
    mutable = list(permutation)
    mutable[left], mutable[right] = mutable[right], mutable[left]
    return tuple(mutable)
