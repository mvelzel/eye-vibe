"""Screen small adaptive-deck allocators for the late Eye state trace."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass

from eye_mystery.gap_anchor import FINAL_MESSAGES
from eye_mystery.ninth_causal import equality_signature
from eye_mystery.phase_marker_closure import late_signatures
from eye_mystery.synchronizing_bridge import bridge_specs, canonical_streams


MODULUS = 83
TRAINING_LENGTH = 30
POLICIES = (
    "none",
    "front",
    "back",
    "left",
    "right",
    "reverse_prefix",
    "reverse_suffix",
)


def initial_order(sign: int, offset: int) -> list[int]:
    if sign not in (-1, 1):
        raise ValueError("sign must be -1 or 1")
    return [(sign * index + offset) % MODULUS for index in range(MODULUS)]


def update_deck(deck: list[int], index: int, policy: str) -> None:
    if policy == "none":
        return
    if policy == "front":
        deck.insert(0, deck.pop(index))
        return
    if policy == "back":
        deck.append(deck.pop(index))
        return
    if policy == "left":
        if index:
            deck[index - 1], deck[index] = deck[index], deck[index - 1]
        return
    if policy == "right":
        if index + 1 < len(deck):
            deck[index], deck[index + 1] = deck[index + 1], deck[index]
        return
    if policy == "reverse_prefix":
        deck[: index + 1] = reversed(deck[: index + 1])
        return
    if policy == "reverse_suffix":
        deck[index:] = reversed(deck[index:])
        return
    raise ValueError(f"unknown policy: {policy}")


def target_card_trace(
    signature: tuple[int, ...],
    *,
    source_sign: int,
    source_offset: int,
    source_policy: str,
    target_policy: str,
) -> tuple[int, ...]:
    source = initial_order(source_sign, source_offset)
    target = list(range(MODULUS))
    emitted = []
    for class_id in signature:
        index = source.index(class_id)
        emitted.append(target[index])
        update_deck(source, index, source_policy)
        update_deck(target, index, target_policy)
    return tuple(emitted)


def late_values(message: str) -> tuple[int, ...]:
    spec = bridge_specs()[message]
    return tuple(canonical_streams()[message][spec.late_entry_full :])


@dataclass(frozen=True)
class AllocatorWitness:
    source_sign: int
    source_offset: int
    source_policy: str
    target_policy: str
    target_slope: int
    target_offset: int
    training_matches: int
    holdout_matches: int
    holdout_length: int
    first_holdout_prediction: int | None
    first_holdout_actual: int | None


@dataclass(frozen=True)
class PanelAllocatorScreen:
    message: str
    models: int
    maximum_training_matches: int
    cobest_models: int
    cobest_with_perfect_training: int
    maximum_cobest_holdout_matches: int
    witnesses: tuple[AllocatorWitness, ...]


def _with_holdout(
    message: str,
    witness: tuple[int, int, str, str, int, int, int],
) -> AllocatorWitness:
    (
        source_sign,
        source_offset,
        source_policy,
        target_policy,
        slope,
        offset,
        training_matches,
    ) = witness
    signature = late_signatures()[message]
    cards = target_card_trace(
        signature,
        source_sign=source_sign,
        source_offset=source_offset,
        source_policy=source_policy,
        target_policy=target_policy,
    )
    predicted = tuple((slope * card + offset) % MODULUS for card in cards)
    actual = late_values(message)
    held_predicted = predicted[TRAINING_LENGTH:]
    held_actual = actual[TRAINING_LENGTH:]
    return AllocatorWitness(
        source_sign=source_sign,
        source_offset=source_offset,
        source_policy=source_policy,
        target_policy=target_policy,
        target_slope=slope,
        target_offset=offset,
        training_matches=training_matches,
        holdout_matches=sum(
            left == right
            for left, right in zip(held_predicted, held_actual, strict=True)
        ),
        holdout_length=len(held_actual),
        first_holdout_prediction=held_predicted[0] if held_predicted else None,
        first_holdout_actual=held_actual[0] if held_actual else None,
    )


def audit_panel(
    message: str,
    *,
    affine_target: bool,
    representative_limit: int = 24,
) -> PanelAllocatorScreen:
    if message not in FINAL_MESSAGES:
        raise ValueError(f"unknown final message: {message}")
    signature = late_signatures()[message][:TRAINING_LENGTH]
    actual = late_values(message)[:TRAINING_LENGTH]
    slopes = range(1, MODULUS) if affine_target else (1, MODULUS - 1)
    maximum = -1
    cobest = 0
    representatives: list[tuple[int, int, str, str, int, int, int]] = []
    for source_sign in (-1, 1):
        for source_offset in range(MODULUS):
            for source_policy in POLICIES:
                for target_policy in POLICIES:
                    cards = target_card_trace(
                        signature,
                        source_sign=source_sign,
                        source_offset=source_offset,
                        source_policy=source_policy,
                        target_policy=target_policy,
                    )
                    for slope in slopes:
                        offsets = Counter(
                            (value - slope * card) % MODULUS
                            for card, value in zip(cards, actual, strict=True)
                        )
                        local = max(offsets.values())
                        winning_offsets = tuple(
                            offset
                            for offset, count in offsets.items()
                            if count == local
                        )
                        if local > maximum:
                            maximum = local
                            cobest = 0
                            representatives.clear()
                        if local == maximum:
                            cobest += len(winning_offsets)
                            for offset in winning_offsets:
                                if len(representatives) < representative_limit:
                                    representatives.append(
                                        (
                                            source_sign,
                                            source_offset,
                                            source_policy,
                                            target_policy,
                                            slope,
                                            offset,
                                            local,
                                        )
                                    )
    resolved = tuple(_with_holdout(message, item) for item in representatives)
    return PanelAllocatorScreen(
        message=message,
        models=(
            2
            * MODULUS
            * len(POLICIES) ** 2
            * len(tuple(slopes))
            * MODULUS
        ),
        maximum_training_matches=maximum,
        cobest_models=cobest,
        cobest_with_perfect_training=cobest
        if maximum == TRAINING_LENGTH
        else 0,
        maximum_cobest_holdout_matches=max(
            (item.holdout_matches for item in resolved),
            default=0,
        ),
        witnesses=resolved,
    )


@dataclass(frozen=True)
class IdentifiabilityCertificate:
    classes: int
    available_labels: int
    injective_relabelings: int
    information_bits: float


def identifiability_certificate() -> IdentifiabilityCertificate:
    signature = late_signatures()[FINAL_MESSAGES[0]][:TRAINING_LENGTH]
    classes = len(set(signature))
    assignments = math.prod(range(MODULUS - classes + 1, MODULUS + 1))
    return IdentifiabilityCertificate(
        classes=classes,
        available_labels=MODULUS,
        injective_relabelings=assignments,
        information_bits=sum(
            math.log2(MODULUS - index) for index in range(classes)
        ),
    )

