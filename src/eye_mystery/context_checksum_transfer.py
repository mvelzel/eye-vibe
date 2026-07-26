"""Transfer the final branch checksum rule to registered isomorph contexts."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import base5_digits, header_ranks
from eye_mystery.ninth_causal import CONTEXT_SPECS, equality_signature
from eye_mystery.novel_branch_machine import (
    DisagreementWindow,
    closed_disagreement_windows,
)


MODULUS = 83
CALIBRATION_CONTEXT = "last-east5"
NONLITERAL_CONTEXTS = CONTEXT_SPECS[6:]


def common_prefix_length(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> int:
    for index, (left_value, right_value) in enumerate(
        zip(left, right, strict=False)
    ):
        if left_value != right_value:
            return index
    return min(len(left), len(right))


def header_scalar(message: str) -> int:
    return base5_digits(header_ranks()[message])[2]


@dataclass(frozen=True)
class ContextChecksumAudit:
    name: str
    left_message: str
    left_start: int
    right_message: str
    right_start: int
    registered_length: int
    actual_common_length: int
    prediction: tuple[int, int]
    windows: tuple[DisagreementWindow, ...]
    observed_checks: tuple[int, ...]
    tested_fields: int
    matching_fields: int
    complete_two_field_match: bool
    reversed_matching_fields: int
    broad_ordered_pair_matches: int
    broad_ordered_pairs: int


def _context_suffixes(
    left_message: str,
    left_start: int,
    right_message: str,
    right_start: int,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    values = {
        name: trigram_values(message)
        for name, message in MESSAGES.items()
    }
    return (
        equality_signature(values[left_message][left_start:]),
        equality_signature(values[right_message][right_start:]),
    )


def _prediction(left_message: str, right_message: str) -> tuple[int, int]:
    return header_scalar(right_message), header_scalar(left_message)


def audit_one_context(
    spec: tuple[str, str, int, str, int, int],
) -> ContextChecksumAudit:
    name, left, left_start, right, right_start, registered_length = spec
    left_signature, right_signature = _context_suffixes(
        left,
        left_start,
        right,
        right_start,
    )
    windows = closed_disagreement_windows(left_signature, right_signature)
    observed = tuple(window.difference_mod83 for window in windows)
    prediction = _prediction(left, right)
    tested = min(2, len(observed))
    matching = sum(
        observed[index] == prediction[index]
        for index in range(tested)
    )
    reversed_matching = sum(
        (-observed[index]) % MODULUS == prediction[index]
        for index in range(tested)
    )

    broad_pairs = tuple(product(MESSAGE_ORDER, repeat=2))
    broad_matches = sum(
        tuple(
            _prediction(candidate_left, candidate_right)[index]
            for index in range(tested)
        )
        == observed[:tested]
        for candidate_left, candidate_right in broad_pairs
    )
    return ContextChecksumAudit(
        name=name,
        left_message=left,
        left_start=left_start,
        right_message=right,
        right_start=right_start,
        registered_length=registered_length,
        actual_common_length=common_prefix_length(
            left_signature,
            right_signature,
        ),
        prediction=prediction,
        windows=windows,
        observed_checks=observed,
        tested_fields=tested,
        matching_fields=matching,
        complete_two_field_match=(
            tested == 2 and matching == 2
        ),
        reversed_matching_fields=reversed_matching,
        broad_ordered_pair_matches=broad_matches,
        broad_ordered_pairs=len(broad_pairs),
    )


@dataclass(frozen=True)
class RegisteredContextTransfer:
    calibration: ContextChecksumAudit
    transfers: tuple[ContextChecksumAudit, ...]
    testable_contexts: int
    tested_fields: int
    matching_fields: int
    complete_two_field_matches: int
    reversed_matching_fields: int


def audit_registered_contexts() -> RegisteredContextTransfer:
    audits = tuple(audit_one_context(spec) for spec in NONLITERAL_CONTEXTS)
    calibration = next(
        audit for audit in audits if audit.name == CALIBRATION_CONTEXT
    )
    transfers = tuple(
        audit for audit in audits if audit.name != CALIBRATION_CONTEXT
    )
    return RegisteredContextTransfer(
        calibration=calibration,
        transfers=transfers,
        testable_contexts=sum(
            audit.tested_fields > 0 for audit in transfers
        ),
        tested_fields=sum(audit.tested_fields for audit in transfers),
        matching_fields=sum(audit.matching_fields for audit in transfers),
        complete_two_field_matches=sum(
            audit.complete_two_field_match for audit in transfers
        ),
        reversed_matching_fields=sum(
            audit.reversed_matching_fields for audit in transfers
        ),
    )


def checksum_plant(
    *,
    left_scalar: int = 2,
    right_scalar: int = 3,
) -> ContextChecksumAudit:
    """Return a synthetic two-record context with reciprocal scalar checks."""

    prefix = tuple(range(11))
    left = prefix + (9, 0, 8, 1)
    right = prefix + (
        9 - right_scalar,
        0,
        8 - left_scalar,
        1,
    )
    windows = closed_disagreement_windows(left, right)
    observed = tuple(window.difference_mod83 for window in windows)
    prediction = (right_scalar, left_scalar)
    return ContextChecksumAudit(
        name="plant",
        left_message="plant-left",
        left_start=0,
        right_message="plant-right",
        right_start=0,
        registered_length=len(prefix),
        actual_common_length=len(prefix),
        prediction=prediction,
        windows=windows,
        observed_checks=observed,
        tested_fields=2,
        matching_fields=sum(
            observed[index] == prediction[index] for index in range(2)
        ),
        complete_two_field_match=observed == prediction,
        reversed_matching_fields=sum(
            (-observed[index]) % MODULUS == prediction[index]
            for index in range(2)
        ),
        broad_ordered_pair_matches=0,
        broad_ordered_pairs=0,
    )
