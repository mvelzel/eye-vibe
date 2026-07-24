"""Finite conditional audit of the Eye marker ``!Fi`` / ``+358`` reading.

Only the third base-five digit is reassigned.  The first two digits, message
coordinates, edge-trail order, BWT primary row, and factoradic predicates are
all held fixed at their independently established values.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from eye_mystery.corpus import MESSAGE_ORDER
from eye_mystery.factoradic_headers import (
    P_MESSAGES,
    Q_EAST_MESSAGES,
    Q_MESSAGES,
    Q_WEST_MESSAGES,
    TARGET_NEWLINE_PREIMAGES,
    base5_digits,
    fixed_symbols,
    generated_group,
    header_ranks,
    is_p_d4_event,
    lexicographic_unrank,
    right_coset,
    unique_multiset_permutations,
)
from eye_mystery.initials import perfect_successor_rotation
from eye_mystery.marker_bwt import (
    base5_trigram_values,
    inverse_cyclic_bwt,
    stable_lf_mapping,
)


Grid = tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]


def marker_grid(assignment: tuple[int, ...]) -> Grid:
    """Lay the nine labels out in canonical three-by-three engine order."""

    if len(assignment) != 9:
        raise ValueError("a marker assignment must contain nine labels")
    return (
        assignment[0:3],
        assignment[3:6],
        assignment[6:9],
    )  # type: ignore[return-value]


def column_sums(grid: Grid) -> tuple[int, int, int]:
    return tuple(sum(grid[row][column] for row in range(3)) for column in range(3))  # type: ignore[return-value]


def rotate_grid(grid: Grid) -> Grid:
    """Rotate a three-by-three grid clockwise."""

    return tuple(
        tuple(grid[2 - column][row] for column in range(3))
        for row in range(3)
    )  # type: ignore[return-value]


def reflect_grid(grid: Grid) -> Grid:
    """Reflect a grid left-to-right."""

    return tuple(tuple(reversed(row)) for row in grid)  # type: ignore[return-value]


def d4_views(grid: Grid) -> tuple[Grid, ...]:
    """Return all distinct rotations/reflections in the square's D4 action."""

    views = []
    current = grid
    for _ in range(4):
        views.append(current)
        current = rotate_grid(current)
    current = reflect_grid(grid)
    for _ in range(4):
        views.append(current)
        current = rotate_grid(current)
    return tuple(dict.fromkeys(views))


def has_country_columns(assignment: tuple[int, ...], *, d4: bool = False) -> bool:
    grid = marker_grid(assignment)
    views = d4_views(grid) if d4 else (grid,)
    return any(column_sums(view) == (3, 5, 8) for view in views)


def assignment_ranks(assignment: tuple[int, ...]) -> dict[str, int]:
    observed = header_ranks()
    coordinates = {
        name: base5_digits(observed[name])[:2] for name in MESSAGE_ORDER
    }
    return {
        name: 25 * coordinates[name][0] + 5 * coordinates[name][1] + label
        for name, label in zip(MESSAGE_ORDER, assignment, strict=True)
    }


@dataclass(frozen=True)
class BwtReading:
    single_cycle: bool
    valid_0_82: bool
    text: str | None

    @property
    def fi_suffix(self) -> bool:
        return self.text is not None and self.text[1:].lower() == "fi"

    @property
    def exact_bang_fi(self) -> bool:
        return self.text == "!Fi"


def assignment_bwt_reading(assignment: tuple[int, ...]) -> BwtReading:
    """Decode one label assignment in the already fixed East-5-first trail."""

    trail = perfect_successor_rotation()
    if trail is None:
        raise ValueError("the marker edge trail is not unique")
    labels = dict(zip(MESSAGE_ORDER, assignment, strict=True))
    last_column = tuple(labels[name] for name in trail)
    lf = stable_lf_mapping(last_column)
    row = 0
    visited = set()
    for _ in last_column:
        visited.add(row)
        row = lf[row]
    single_cycle = len(visited) == len(last_column) and row == 0
    if not single_cycle:
        return BwtReading(False, False, None)
    values = base5_trigram_values(inverse_cyclic_bwt(last_column, 0))
    if any(value > 82 for value in values):
        return BwtReading(True, False, None)
    return BwtReading(True, True, "".join(chr(value + 32) for value in values))


def is_full_factoradic_event(ranks: Mapping[str, int]) -> bool:
    """Apply the previously published full header predicate without changes."""

    permutations = {
        name: lexicographic_unrank(rank) for name, rank in ranks.items()
    }
    if (
        tuple(permutations[name].index(5) for name in MESSAGE_ORDER)
        != TARGET_NEWLINE_PREIMAGES
    ):
        return False
    if not is_p_d4_event({name: permutations[name] for name in P_MESSAGES}):
        return False
    q_values = tuple(permutations[name] for name in Q_MESSAGES)
    if not (
        all(fixed_symbols(value) == (0,) for value in q_values)
        and len(generated_group(q_values)) == 120
    ):
        return False
    p_group = generated_group(permutations[name] for name in P_MESSAGES)
    east_cosets = {
        right_coset(permutations[name], p_group) for name in Q_EAST_MESSAGES
    }
    west_cosets = {
        right_coset(permutations[name], p_group) for name in Q_WEST_MESSAGES
    }
    return len(east_cosets) == 3 and len(west_cosets) == 1


@dataclass(frozen=True)
class FactoradicSurvivor:
    assignment: tuple[int, ...]
    columns: tuple[int, int, int]
    d4_country: bool
    bwt_text: str | None


@dataclass(frozen=True)
class MarkerCountryAudit:
    all_assignments: int
    in_range: int
    distinct_ranks: int
    exact_country: int
    d4_country: int
    bwt_single_cycle: int
    bwt_valid_0_82: int
    bwt_fi_suffix: int
    bwt_exact_bang_fi: int
    exact_country_and_fi_suffix: int
    exact_country_and_exact_bang_fi: int
    d4_country_and_fi_suffix: int
    d4_country_and_exact_bang_fi: int
    full_factoradic: int
    full_exact_country: int
    full_d4_country: int
    survivors: tuple[FactoradicSurvivor, ...]


def marker_country_audit() -> MarkerCountryAudit:
    """Enumerate the frozen conditional universe from the twenty-fifth pass."""

    labels = tuple(base5_digits(header_ranks()[name])[2] for name in MESSAGE_ORDER)
    counts = {
        "all": 0,
        "in_range": 0,
        "distinct": 0,
        "exact_country": 0,
        "d4_country": 0,
        "single_cycle": 0,
        "valid": 0,
        "fi_suffix": 0,
        "bang_fi": 0,
        "exact_fi": 0,
        "exact_bang": 0,
        "d4_fi": 0,
        "d4_bang": 0,
        "full": 0,
        "full_exact": 0,
        "full_d4": 0,
    }
    survivors = []

    for assignment in unique_multiset_permutations(labels):
        counts["all"] += 1
        ranks = assignment_ranks(assignment)
        if max(ranks.values()) > 82:
            continue
        counts["in_range"] += 1
        if len(set(ranks.values())) != 9:
            continue
        counts["distinct"] += 1

        exact_country = has_country_columns(assignment)
        d4_country = has_country_columns(assignment, d4=True)
        reading = assignment_bwt_reading(assignment)
        counts["exact_country"] += exact_country
        counts["d4_country"] += d4_country
        counts["single_cycle"] += reading.single_cycle
        counts["valid"] += reading.valid_0_82
        counts["fi_suffix"] += reading.fi_suffix
        counts["bang_fi"] += reading.exact_bang_fi
        counts["exact_fi"] += exact_country and reading.fi_suffix
        counts["exact_bang"] += exact_country and reading.exact_bang_fi
        counts["d4_fi"] += d4_country and reading.fi_suffix
        counts["d4_bang"] += d4_country and reading.exact_bang_fi

        if not is_full_factoradic_event(ranks):
            continue
        counts["full"] += 1
        counts["full_exact"] += exact_country
        counts["full_d4"] += d4_country
        survivors.append(
            FactoradicSurvivor(
                assignment=assignment,
                columns=column_sums(marker_grid(assignment)),
                d4_country=d4_country,
                bwt_text=reading.text,
            )
        )

    return MarkerCountryAudit(
        all_assignments=counts["all"],
        in_range=counts["in_range"],
        distinct_ranks=counts["distinct"],
        exact_country=counts["exact_country"],
        d4_country=counts["d4_country"],
        bwt_single_cycle=counts["single_cycle"],
        bwt_valid_0_82=counts["valid"],
        bwt_fi_suffix=counts["fi_suffix"],
        bwt_exact_bang_fi=counts["bang_fi"],
        exact_country_and_fi_suffix=counts["exact_fi"],
        exact_country_and_exact_bang_fi=counts["exact_bang"],
        d4_country_and_fi_suffix=counts["d4_fi"],
        d4_country_and_exact_bang_fi=counts["d4_bang"],
        full_factoradic=counts["full"],
        full_exact_country=counts["full_exact"],
        full_d4_country=counts["full_d4"],
        survivors=tuple(survivors),
    )
