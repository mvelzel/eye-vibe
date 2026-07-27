"""Exact finite-domain solver for hidden-cycle chord geometry."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from time import monotonic

from eye_mystery.hidden_geometry import (
    MODULUS,
    ChordConstraint,
    chord_classes,
    constraint_holds,
)


@dataclass(frozen=True)
class DomainGeometrySolve:
    outcome: str
    constraints: int
    labels: int
    classes: int
    nodes: int
    backtracks: int
    elapsed_seconds: float
    coordinates: tuple[tuple[int, int], ...] = ()
    reason: str | None = None


class _Timeout(Exception):
    pass


def _rotate(mask: int, shift: int, width: int, full_mask: int) -> int:
    shift %= width
    if not shift:
        return mask
    return ((mask << shift) | (mask >> (width - shift))) & full_mask


def _values(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def _matching_exists(domains: Sequence[int], width: int) -> bool:
    """Return whether coordinate domains admit an injective completion."""

    match_by_position = [-1] * width
    order = sorted(
        range(len(domains)),
        key=lambda index: (domains[index].bit_count(), index),
    )

    def augment(variable: int, seen: list[bool]) -> bool:
        for position in _values(domains[variable]):
            if seen[position]:
                continue
            seen[position] = True
            owner = match_by_position[position]
            if owner < 0 or augment(owner, seen):
                match_by_position[position] = variable
                return True
        return False

    return all(augment(variable, [False] * width) for variable in order)


def solve_hidden_geometry_domain(
    constraints: Sequence[ChordConstraint],
    *,
    modulus: int = MODULUS,
    timeout_ms: int = 180_000,
) -> DomainGeometrySolve:
    """Solve exact chord geometry by bitset arc consistency and search."""

    if modulus < 3 or modulus % 2 == 0:
        raise ValueError("modulus must be an odd integer at least three")
    if timeout_ms < 1:
        raise ValueError("timeout must be positive")
    if not constraints:
        raise ValueError("at least one constraint is required")
    started = monotonic()
    deadline = started + timeout_ms / 1_000
    labels = tuple(
        sorted(
            {
                label
                for constraint in constraints
                for label in constraint.labels
            }
        )
    )
    label_index = {label: index for index, label in enumerate(labels)}
    classes = chord_classes(constraints)
    edges = tuple(
        (label_index[left], label_index[right], class_index)
        for class_index, members in enumerate(classes)
        for left, right in members
    )
    if any(left == right for members in classes for left, right in members):
        raise ValueError("the domain solver expects nonzero chord edges")

    full_coordinates = (1 << modulus) - 1
    half = (modulus - 1) // 2
    full_magnitudes = sum(1 << value for value in range(1, half + 1))
    coordinate_domains = [full_coordinates] * len(labels)
    magnitude_domains = [full_magnitudes] * len(classes)
    coordinate_degree = [0] * len(labels)
    class_degree = [0] * len(classes)
    for left, right, class_index in edges:
        coordinate_degree[left] += 1
        coordinate_degree[right] += 1
        class_degree[class_index] += 1

    anchor_left, anchor_right = next(
        (left, right)
        for constraint in constraints
        for left, right in (
            (constraint.source_left, constraint.source_right),
            (constraint.target_left, constraint.target_right),
        )
        if left != right
    )
    coordinate_domains[label_index[anchor_left]] = 1 << 0
    coordinate_domains[label_index[anchor_right]] = 1 << 1
    nodes = 0
    backtracks = 0

    def check_time() -> None:
        if monotonic() >= deadline:
            raise _Timeout

    def propagate(
        coordinates: list[int],
        magnitudes: list[int],
    ) -> bool:
        changed = True
        while changed:
            check_time()
            changed = False
            singleton_positions = 0
            seen_singletons = 0
            for domain in coordinates:
                if not domain:
                    return False
                if domain & (domain - 1):
                    continue
                if seen_singletons & domain:
                    return False
                seen_singletons |= domain
                singleton_positions |= domain
            for index, domain in enumerate(coordinates):
                if not domain & (domain - 1):
                    continue
                reduced = domain & ~singleton_positions
                if not reduced:
                    return False
                if reduced != domain:
                    coordinates[index] = reduced
                    changed = True

            for left, right, class_index in edges:
                left_domain = coordinates[left]
                right_domain = coordinates[right]
                magnitude_domain = magnitudes[class_index]
                if not magnitude_domain:
                    return False

                left_support = 0
                right_support = 0
                magnitude_support = 0
                for value in _values(magnitude_domain):
                    right_neighbours = _rotate(
                        right_domain,
                        value,
                        modulus,
                        full_coordinates,
                    ) | _rotate(
                        right_domain,
                        -value,
                        modulus,
                        full_coordinates,
                    )
                    if left_domain & right_neighbours:
                        magnitude_support |= 1 << value
                        left_support |= right_neighbours
                    left_neighbours = _rotate(
                        left_domain,
                        value,
                        modulus,
                        full_coordinates,
                    ) | _rotate(
                        left_domain,
                        -value,
                        modulus,
                        full_coordinates,
                    )
                    right_support |= left_neighbours

                new_left = left_domain & left_support
                new_right = right_domain & right_support
                new_magnitude = magnitude_domain & magnitude_support
                if not new_left or not new_right or not new_magnitude:
                    return False
                if new_left != left_domain:
                    coordinates[left] = new_left
                    changed = True
                if new_right != right_domain:
                    coordinates[right] = new_right
                    changed = True
                if new_magnitude != magnitude_domain:
                    magnitudes[class_index] = new_magnitude
                    changed = True

        return _matching_exists(coordinates, modulus)

    def search(
        coordinates: list[int],
        magnitudes: list[int],
    ) -> tuple[list[int], list[int]] | None:
        nonlocal nodes, backtracks
        check_time()
        nodes += 1
        if not propagate(coordinates, magnitudes):
            backtracks += 1
            return None
        candidates = []
        for index, domain in enumerate(coordinates):
            size = domain.bit_count()
            if size > 1:
                candidates.append(
                    (size, -coordinate_degree[index], 0, index, domain)
                )
        for index, domain in enumerate(magnitudes):
            size = domain.bit_count()
            if size > 1:
                candidates.append(
                    (size, -class_degree[index], 1, index, domain)
                )
        if not candidates:
            return coordinates, magnitudes

        _, _, kind, index, domain = min(candidates)
        for value in _values(domain):
            child_coordinates = coordinates.copy()
            child_magnitudes = magnitudes.copy()
            if kind == 0:
                child_coordinates[index] = 1 << value
            else:
                child_magnitudes[index] = 1 << value
            result = search(child_coordinates, child_magnitudes)
            if result is not None:
                return result
        backtracks += 1
        return None

    try:
        resolved = search(coordinate_domains, magnitude_domains)
    except _Timeout:
        return DomainGeometrySolve(
            "unknown",
            len(constraints),
            len(labels),
            len(classes),
            nodes,
            backtracks,
            monotonic() - started,
            reason="timeout",
        )
    elapsed = monotonic() - started
    if resolved is None:
        return DomainGeometrySolve(
            "unsat",
            len(constraints),
            len(labels),
            len(classes),
            nodes,
            backtracks,
            elapsed,
        )

    final_coordinates, _ = resolved
    coordinates = tuple(
        (label, domain.bit_length() - 1)
        for label, domain in zip(labels, final_coordinates, strict=True)
    )
    if len({coordinate for _, coordinate in coordinates}) != len(coordinates):
        raise AssertionError("domain model violates coordinate injection")
    flat = [0] * modulus
    for label, coordinate in coordinates:
        flat[label] = coordinate
    if not all(
        constraint_holds(constraint, flat, modulus=modulus)
        for constraint in constraints
    ):
        raise AssertionError("domain model violates a chord constraint")
    return DomainGeometrySolve(
        "sat",
        len(constraints),
        len(labels),
        len(classes),
        nodes,
        backtracks,
        elapsed,
        coordinates,
    )
