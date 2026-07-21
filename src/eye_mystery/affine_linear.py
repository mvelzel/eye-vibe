"""Dependency-free finite-field certificates for affine context embeddings."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from collections.abc import Iterator, Sequence

from .affine_embedding import Context, MODULUS


@dataclass(frozen=True)
class FixedMultiplierCase:
    """Result after fixing one multiplier for every affine context map."""

    multipliers: tuple[int, ...]
    status: str
    collisions: tuple[tuple[int, int], ...] = ()
    rank: int = 0
    free_variables: int = 0


def allowed_multipliers(hidden_order: int) -> tuple[int, ...]:
    if hidden_order == 41:
        return tuple(sorted({pow(2, 2 * exponent, MODULUS) for exponent in range(41)}))
    if hidden_order == 82:
        return tuple(range(1, MODULUS))
    raise ValueError("hidden_order must be 41 or 82")


def analyze_fixed_multipliers(
    contexts: Sequence[Context], multipliers: Sequence[int]
) -> FixedMultiplierCase:
    """Reduce an affine embedding to linear algebra over ``F_83``.

    The coordinate of each observed ciphertext label and one translation per
    context are variables.  Two arbitrary distinct label coordinates are
    normalized to 0 and 1.  A case is rejected either because its linear system
    is inconsistent or because every solution identifies distinct labels.
    """
    if not contexts:
        raise ValueError("at least one context is required")
    if len(contexts) != len(multipliers):
        raise ValueError("one multiplier is required per context")
    if any(not 1 <= value < MODULUS for value in multipliers):
        raise ValueError("multipliers must be nonzero elements of F_83")

    labels = tuple(
        dict.fromkeys(
            label
            for context in contexts
            for pair in context.pairs
            for label in pair
        )
    )
    if len(labels) < 2:
        raise ValueError("at least two distinct ciphertext labels are required")
    label_index = {label: index for index, label in enumerate(labels)}
    translation_start = len(labels)
    variable_count = len(labels) + len(contexts)
    rows: list[list[int]] = []

    for context_index, (context, multiplier) in enumerate(
        zip(contexts, multipliers, strict=True)
    ):
        for left, right in context.pairs:
            row = [0] * (variable_count + 1)
            # Accumulate because a fixed-point edge has the same variable on
            # both sides: (1 - multiplier) * x - translation = 0.
            row[label_index[right]] = (row[label_index[right]] + 1) % MODULUS
            row[label_index[left]] = (
                row[label_index[left]] - multiplier
            ) % MODULUS
            row[translation_start + context_index] = -1 % MODULUS
            rows.append(row)
    for label, value in ((labels[0], 0), (labels[1], 1)):
        row = [0] * (variable_count + 1)
        row[label_index[label]] = 1
        row[-1] = value
        rows.append(row)

    rank = 0
    pivots: list[int] = []
    for column in range(variable_count):
        pivot_row = next(
            (
                candidate
                for candidate in range(rank, len(rows))
                if rows[candidate][column] % MODULUS
            ),
            None,
        )
        if pivot_row is None:
            continue
        rows[rank], rows[pivot_row] = rows[pivot_row], rows[rank]
        inverse = pow(rows[rank][column], -1, MODULUS)
        rows[rank] = [(value * inverse) % MODULUS for value in rows[rank]]
        for other in range(len(rows)):
            factor = rows[other][column]
            if other != rank and factor:
                rows[other] = [
                    (left - factor * right) % MODULUS
                    for left, right in zip(rows[other], rows[rank], strict=True)
                ]
        pivots.append(column)
        rank += 1

    if any(
        not any(row[:variable_count]) and row[-1] for row in rows
    ):
        return FixedMultiplierCase(tuple(multipliers), "inconsistent", rank=rank)

    free = tuple(index for index in range(variable_count) if index not in pivots)
    free_index = {variable: index for index, variable in enumerate(free)}
    pivot_rows = {pivot: rows[index] for index, pivot in enumerate(pivots)}
    expressions: list[tuple[int, ...]] = []
    for variable in range(variable_count):
        expression = [0] * (len(free) + 1)
        if variable in free_index:
            expression[free_index[variable]] = 1
        else:
            row = pivot_rows[variable]
            expression[-1] = row[-1]
            for free_variable, index in free_index.items():
                expression[index] = -row[free_variable] % MODULUS
        expressions.append(tuple(expression))

    collisions = tuple(
        (labels[left], labels[right])
        for right in range(len(labels))
        for left in range(right)
        if expressions[left] == expressions[right]
    )
    return FixedMultiplierCase(
        tuple(multipliers),
        "forced_collision" if collisions else "open",
        collisions,
        rank,
        len(free),
    )


def enumerate_multiplier_cases(
    contexts: Sequence[Context], *, hidden_order: int
) -> Iterator[FixedMultiplierCase]:
    values = allowed_multipliers(hidden_order)
    for multipliers in product(values, repeat=len(contexts)):
        yield analyze_fixed_multipliers(contexts, multipliers)
