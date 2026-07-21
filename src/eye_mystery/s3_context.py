"""Held-out tests of an S3 interpretation of the last-family contexts.

The final header row naturally names the identity and the two adjacent
transpositions of three components.  If those two transpositions also name
the observed East4->East5 and East4->West4 body-context permutations, their
partial maps must obey the Coxeter presentation of S3.  Partial observations
are enough to falsify an identity whenever a known composition moves a label.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from .partial_group import compose_partial, conflict_witness
from .progression_certificate import (
    LAST_CONTEXT_LENGTH,
    LAST_ONE_STEP,
    LAST_REFERENCE,
    LAST_THREE_STEP,
    context_mapping,
)


PartialMap = dict[int, int]


@dataclass(frozen=True)
class S3ContextAudit:
    """Exact consequences of assigning the two context maps to S3 swaps."""

    first_size: int
    second_size: int
    first_square: tuple[tuple[int, int], ...]
    second_square: tuple[tuple[int, int], ...]
    first_square_violations: tuple[tuple[int, int], ...]
    second_square_violations: tuple[tuple[int, int], ...]
    braid_left: tuple[tuple[int, int], ...]
    braid_right: tuple[tuple[int, int], ...]
    braid_conflict: tuple[int, int, int] | None

    @property
    def coxeter_assignment_survives(self) -> bool:
        return not (
            self.first_square_violations
            or self.second_square_violations
            or self.braid_conflict
        )


def identity_violations(mapping: Mapping[int, int]) -> tuple[tuple[int, int], ...]:
    """Known edges that prevent a partial map from being the identity."""

    return tuple(sorted((source, target) for source, target in mapping.items() if source != target))


def last_family_s3_context_audit() -> S3ContextAudit:
    """Test the direct header-generator assignment against independent bodies."""

    reference_name, reference_start = LAST_REFERENCE
    first_name, first_start = LAST_ONE_STEP
    second_name, second_start = LAST_THREE_STEP
    first: PartialMap = context_mapping(
        reference_name,
        reference_start,
        first_name,
        first_start,
        LAST_CONTEXT_LENGTH,
    )
    second: PartialMap = context_mapping(
        reference_name,
        reference_start,
        second_name,
        second_start,
        LAST_CONTEXT_LENGTH,
    )

    first_square = compose_partial(first, first)
    second_square = compose_partial(second, second)
    first_second_first = compose_partial(compose_partial(first, second), first)
    second_first_second = compose_partial(compose_partial(second, first), second)

    return S3ContextAudit(
        first_size=len(first),
        second_size=len(second),
        first_square=tuple(sorted(first_square.items())),
        second_square=tuple(sorted(second_square.items())),
        first_square_violations=identity_violations(first_square),
        second_square_violations=identity_violations(second_square),
        braid_left=tuple(sorted(first_second_first.items())),
        braid_right=tuple(sorted(second_first_second.items())),
        braid_conflict=conflict_witness(first_second_first, second_first_second),
    )
