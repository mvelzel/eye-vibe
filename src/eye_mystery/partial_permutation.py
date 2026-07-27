"""Exact completion facts for a partial permutation.

Repeated plaintext passages in a perfectly isomorphic cipher induce partial
permutations of the ciphertext alphabet.  These helpers quantify what is
forced before choosing arbitrary values for the unobserved edges.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import lru_cache


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


@dataclass(frozen=True)
class FiniteOrderCompletion:
    """Exact feasibility of completing a partial map with ``P**m = identity``."""

    exponent: int
    feasible: bool
    path_vertex_lengths: tuple[int, ...]
    cycle_lengths: tuple[int, ...]
    incompatible_cycle_lengths: tuple[int, ...]
    minimum_extra_vertices: int | None
    unobserved_vertices: int


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


def finite_order_completion(
    mapping: Mapping[int, int], alphabet_size: int, exponent: int
) -> FiniteOrderCompletion:
    """Test whether a completion can satisfy ``permutation**exponent = id``.

    Observed cycles must already have divisor lengths.  Observed path
    components can be concatenated and closed into cycles whose lengths divide
    ``exponent``; wholly unobserved vertices may fill the remaining slots.
    A small exact bin-packing dynamic program minimizes that filler.
    """

    validate_partial_permutation(mapping, alphabet_size)
    if exponent < 1:
        raise ValueError("exponent must be positive")

    path_edges, cycle_lengths = _components(mapping)
    path_vertices = tuple(sorted((length + 1 for length in path_edges), reverse=True))
    incompatible_cycles = tuple(
        length for length in cycle_lengths if exponent % length
    )
    observed_vertices = len(set(mapping) | set(mapping.values()))
    unobserved_vertices = alphabet_size - observed_vertices
    if incompatible_cycles or any(length > exponent for length in path_vertices):
        return FiniteOrderCompletion(
            exponent,
            False,
            path_vertices,
            cycle_lengths,
            incompatible_cycles,
            None,
            unobserved_vertices,
        )

    divisors = tuple(
        value for value in range(1, exponent + 1) if exponent % value == 0
    )
    counts = [0] * (exponent + 1)
    for length in path_vertices:
        counts[length] += 1

    @lru_cache(maxsize=None)
    def minimum_filler(state: tuple[int, ...]) -> int:
        if not any(state):
            return 0
        anchor = max(index for index, count in enumerate(state) if count)
        available = list(state)
        available[anchor] -= 1
        best = alphabet_size + exponent + 1

        for capacity in divisors:
            if capacity < anchor:
                continue
            chosen = [0] * len(state)
            chosen[anchor] = 1

            def fill(size: int, used: int) -> None:
                nonlocal best
                if size < 2:
                    next_state = tuple(
                        count - take
                        for count, take in zip(state, chosen, strict=True)
                    )
                    best = min(
                        best,
                        capacity - used + minimum_filler(next_state),
                    )
                    return
                maximum = min(available[size], (capacity - used) // size)
                for take in range(maximum + 1):
                    chosen[size] = take + (1 if size == anchor else 0)
                    fill(size - 1, used + take * size)
                chosen[size] = 1 if size == anchor else 0

            fill(exponent, anchor)

        return best

    extra = minimum_filler(tuple(counts))
    return FiniteOrderCompletion(
        exponent,
        extra <= unobserved_vertices,
        path_vertices,
        cycle_lengths,
        incompatible_cycles,
        extra,
        unobserved_vertices,
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
