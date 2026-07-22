"""Independent checks of the proposed six-symbol Eye header interpretation.

The first Eye trigram is already independently exceptional.  This module asks
what happens if its orthodox rank is used as the lexicographic rank of a
permutation of the five renderer eye codes plus the renderer's newline code.
It intentionally implements only the compact, finite core of the July 2026
claim; it does not import the much larger community audit.
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Iterable, Iterator, Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values


SYMBOLS = ("center", "up", "right", "down", "left", "newline")
P_MESSAGES = ("east1", "west1", "east2")
Q_EAST_MESSAGES = ("east3", "east4", "east5")
Q_WEST_MESSAGES = ("west2", "west3", "west4")
Q_MESSAGES = Q_WEST_MESSAGES + Q_EAST_MESSAGES
TARGET_NEWLINE_PREIMAGES = (5, 5, 5, 3, 4, 3, 4, 3, 4)

Permutation = tuple[int, ...]


def header_ranks() -> dict[str, int]:
    """Return the orthodox first-trigram rank of every Eye message."""

    return {name: trigram_values(MESSAGES[name])[0] for name in MESSAGE_ORDER}


def base5_digits(rank: int) -> tuple[int, int, int]:
    return rank // 25, rank // 5 % 5, rank % 5


def lexicographic_unrank(rank: int, size: int = 6) -> Permutation:
    """Unrank one permutation in ordinary lexicographic order."""

    if rank not in range(math.factorial(size)):
        raise ValueError("rank lies outside the permutation space")
    available = list(range(size))
    result = []
    for remaining in range(size, 0, -1):
        index, rank = divmod(rank, math.factorial(remaining - 1))
        result.append(available.pop(index))
    return tuple(result)


def compose(left: Permutation, right: Permutation) -> Permutation:
    """Return ``left`` after ``right`` under one-line notation."""

    return tuple(left[right[index]] for index in range(len(left)))


def inverse(permutation: Permutation) -> Permutation:
    result = [0] * len(permutation)
    for index, value in enumerate(permutation):
        result[value] = index
    return tuple(result)


def permutation_order(permutation: Permutation) -> int:
    identity = tuple(range(len(permutation)))
    value = identity
    for exponent in range(1, math.factorial(len(permutation)) + 1):
        value = compose(permutation, value)
        if value == identity:
            return exponent
    raise AssertionError("permutation order exceeded the group size")


def generated_group(generators: Iterable[Permutation]) -> set[Permutation]:
    generators = tuple(generators)
    if not generators:
        raise ValueError("at least one generator is required")
    identity = tuple(range(len(generators[0])))
    group = {identity}
    pending = [identity]
    while pending:
        value = pending.pop()
        for generator in generators:
            product = compose(generator, value)
            if product not in group:
                group.add(product)
                pending.append(product)
    return group


def fixed_symbols(permutation: Permutation) -> tuple[int, ...]:
    return tuple(index for index, value in enumerate(permutation) if index == value)


def right_coset(permutation: Permutation, group: set[Permutation]) -> frozenset[Permutation]:
    return frozenset(compose(element, permutation) for element in group)


def is_p_d4_event(permutations: Mapping[str, Permutation]) -> bool:
    """Test the named ``r, s, r^-1`` D4 relation used by the P messages."""

    rotation = permutations["east1"]
    reflection = permutations["west1"]
    inverse_rotation = permutations["east2"]
    common_fixed = {
        symbol
        for symbol in range(6)
        if all(permutation[symbol] == symbol for permutation in permutations.values())
    }
    return (
        permutation_order(rotation) == 4
        and permutation_order(reflection) == 2
        and inverse(rotation) == inverse_rotation
        and compose(compose(reflection, rotation), reflection) == inverse_rotation
        and common_fixed == {0, 5}
        and len(generated_group(permutations.values())) == 8
    )


def unique_multiset_permutations(values: Sequence[int]) -> Iterator[tuple[int, ...]]:
    """Yield each distinct permutation without materializing a duplicate-heavy set."""

    counts = Counter(values)
    ordered = tuple(sorted(counts))
    output = [0] * len(values)

    def visit(index: int) -> Iterator[tuple[int, ...]]:
        if index == len(output):
            yield tuple(output)
            return
        for value in ordered:
            if counts[value]:
                counts[value] -= 1
                output[index] = value
                yield from visit(index + 1)
                counts[value] += 1

    yield from visit(0)


@dataclass(frozen=True)
class HeaderSignature:
    ranks: tuple[int, ...]
    permutations: tuple[Permutation, ...]
    p_group_order: int
    p_group_ranks: tuple[int, ...]
    q_group_order: int
    newline_preimages: tuple[int, ...]
    east_q_cosets: int
    west_q_cosets: int


def observed_signature() -> HeaderSignature:
    ranks_by_name = header_ranks()
    ranks = tuple(ranks_by_name[name] for name in MESSAGE_ORDER)
    permutations_by_name = {
        name: lexicographic_unrank(rank) for name, rank in ranks_by_name.items()
    }
    p_group = generated_group(permutations_by_name[name] for name in P_MESSAGES)
    q_group = generated_group(permutations_by_name[name] for name in Q_MESSAGES)
    lookup = {
        lexicographic_unrank(rank): rank for rank in range(math.factorial(6))
    }
    return HeaderSignature(
        ranks=ranks,
        permutations=tuple(permutations_by_name[name] for name in MESSAGE_ORDER),
        p_group_order=len(p_group),
        p_group_ranks=tuple(sorted(lookup[value] for value in p_group)),
        q_group_order=len(q_group),
        newline_preimages=tuple(
            permutations_by_name[name].index(5) for name in MESSAGE_ORDER
        ),
        east_q_cosets=len(
            {
                right_coset(permutations_by_name[name], p_group)
                for name in Q_EAST_MESSAGES
            }
        ),
        west_q_cosets=len(
            {
                right_coset(permutations_by_name[name], p_group)
                for name in Q_WEST_MESSAGES
            }
        ),
    )


@dataclass(frozen=True)
class ConditionalAudit:
    all_assignments: int
    in_range: int
    distinct_ranks: int
    typed: int
    p_d4: int
    q_s5: int
    p_d4_and_q_s5: int
    full: int
    survivors: tuple[tuple[int, ...], ...]


def graph_conditioned_audit() -> ConditionalAudit:
    """Permute only header labels while freezing the known graph coordinates."""

    observed = header_ranks()
    coordinates = {
        name: base5_digits(observed[name])[:2] for name in MESSAGE_ORDER
    }
    labels = tuple(base5_digits(observed[name])[2] for name in MESSAGE_ORDER)
    counts: Counter[str] = Counter()
    survivors = []

    for assignment in unique_multiset_permutations(labels):
        counts["all"] += 1
        ranks = {
            name: 25 * coordinates[name][0] + 5 * coordinates[name][1] + label
            for name, label in zip(MESSAGE_ORDER, assignment, strict=True)
        }
        if max(ranks.values()) > 82:
            continue
        counts["in_range"] += 1
        if len(set(ranks.values())) != 9:
            continue
        counts["distinct"] += 1

        permutations = {
            name: lexicographic_unrank(rank) for name, rank in ranks.items()
        }
        typed = (
            tuple(permutations[name].index(5) for name in MESSAGE_ORDER)
            == TARGET_NEWLINE_PREIMAGES
        )
        p_d4 = is_p_d4_event(
            {name: permutations[name] for name in P_MESSAGES}
        )
        q_values = tuple(permutations[name] for name in Q_MESSAGES)
        q_s5 = all(fixed_symbols(value) == (0,) for value in q_values) and len(
            generated_group(q_values)
        ) == 120
        counts["typed"] += typed
        counts["p_d4"] += p_d4
        counts["q_s5"] += q_s5
        counts["p_d4_q_s5"] += p_d4 and q_s5
        if not (typed and p_d4 and q_s5):
            continue

        p_group = generated_group(permutations[name] for name in P_MESSAGES)
        east_cosets = {
            right_coset(permutations[name], p_group) for name in Q_EAST_MESSAGES
        }
        west_cosets = {
            right_coset(permutations[name], p_group) for name in Q_WEST_MESSAGES
        }
        if len(east_cosets) == 3 and len(west_cosets) == 1:
            counts["full"] += 1
            survivors.append(assignment)

    return ConditionalAudit(
        all_assignments=counts["all"],
        in_range=counts["in_range"],
        distinct_ranks=counts["distinct"],
        typed=counts["typed"],
        p_d4=counts["p_d4"],
        q_s5=counts["q_s5"],
        p_d4_and_q_s5=counts["p_d4_q_s5"],
        full=counts["full"],
        survivors=tuple(survivors),
    )
