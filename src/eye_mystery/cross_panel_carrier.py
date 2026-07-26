"""Low-capacity cross-panel carriers for the common late state table."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import permutations, product

from eye_mystery.gap_anchor import FINAL_MESSAGES
from eye_mystery.terminal_source_return import class_labels


MODULUS = 83
HOLDOUT_CLASSES = (10, 24)
CLASSES = tuple(range(25))
TRAINING_CLASSES = tuple(
    class_id for class_id in CLASSES if class_id not in HOLDOUT_CLASSES
)
EYE_ORDERS = tuple(permutations(range(3)))


def common_tables() -> dict[str, tuple[int, ...]]:
    return {
        panel: tuple(class_labels(panel)[class_id] for class_id in CLASSES)
        for panel in FINAL_MESSAGES
    }


@dataclass(frozen=True)
class AffineWitness:
    source_panels: tuple[str, str]
    target_panel: str
    a: int
    b: int
    d: int
    c: int
    training_matches: int
    holdout_predictions: tuple[int, int]
    holdout_actual: tuple[int, int]

    @property
    def holdout_matches(self) -> int:
        return sum(
            predicted == actual
            for predicted, actual in zip(
                self.holdout_predictions,
                self.holdout_actual,
                strict=True,
            )
        )


@dataclass(frozen=True)
class AffineScreen:
    target_panel: str
    with_class_term: bool
    models: int
    maximum_training_matches: int
    cobest_models: int
    cobest_predicting_both_holdouts: int
    witnesses: tuple[AffineWitness, ...]


def audit_affine(
    target_panel: str,
    *,
    with_class_term: bool,
    representative_limit: int = 20,
) -> AffineScreen:
    tables = common_tables()
    sources = tuple(
        panel for panel in FINAL_MESSAGES if panel != target_panel
    )
    left = tables[sources[0]]
    right = tables[sources[1]]
    target = tables[target_panel]
    maximum = -1
    cobest = 0
    both = 0
    representatives: list[AffineWitness] = []
    d_values = range(MODULUS) if with_class_term else (0,)
    for a in range(MODULUS):
        for b in range(MODULUS):
            base = tuple(
                (target[class_id] - a * left[class_id] - b * right[class_id])
                % MODULUS
                for class_id in CLASSES
            )
            for d in d_values:
                offsets = Counter(
                    (base[class_id] - d * class_id) % MODULUS
                    for class_id in TRAINING_CLASSES
                )
                local = max(offsets.values())
                winners = tuple(
                    c for c, count in offsets.items() if count == local
                )
                if local > maximum:
                    maximum = local
                    cobest = 0
                    both = 0
                    representatives.clear()
                if local != maximum:
                    continue
                for c in winners:
                    predictions = tuple(
                        (
                            a * left[class_id]
                            + b * right[class_id]
                            + d * class_id
                            + c
                        )
                        % MODULUS
                        for class_id in HOLDOUT_CLASSES
                    )
                    actual = tuple(target[index] for index in HOLDOUT_CLASSES)
                    witness = AffineWitness(
                        source_panels=sources,  # type: ignore[arg-type]
                        target_panel=target_panel,
                        a=a,
                        b=b,
                        d=d,
                        c=c,
                        training_matches=local,
                        holdout_predictions=predictions,  # type: ignore[arg-type]
                        holdout_actual=actual,  # type: ignore[arg-type]
                    )
                    cobest += 1
                    both += witness.holdout_matches == len(HOLDOUT_CLASSES)
                    if len(representatives) < representative_limit:
                        representatives.append(witness)
    coefficient_count = MODULUS ** (3 if with_class_term else 2)
    return AffineScreen(
        target_panel=target_panel,
        with_class_term=with_class_term,
        models=coefficient_count * MODULUS,
        maximum_training_matches=maximum,
        cobest_models=cobest,
        cobest_predicting_both_holdouts=both,
        witnesses=tuple(representatives),
    )


def base5_digits(value: int) -> tuple[int, int, int]:
    return value // 25, (value // 5) % 5, value % 5


@dataclass(frozen=True)
class EyeArithmeticWitness:
    source_panels: tuple[str, str]
    target_panel: str
    source_orders: tuple[tuple[int, int, int], tuple[int, int, int]]
    target_order: tuple[int, int, int]
    a: int
    b: int
    offsets: tuple[int, int, int]
    training_matches: int
    holdout_predictions: tuple[int, int]
    holdout_actual: tuple[int, int]

    @property
    def holdout_matches(self) -> int:
        return sum(
            predicted == actual
            for predicted, actual in zip(
                self.holdout_predictions,
                self.holdout_actual,
                strict=True,
            )
        )


@dataclass(frozen=True)
class EyeArithmeticScreen:
    target_panel: str
    models: int
    maximum_training_matches: int
    cobest_models: int
    cobest_predicting_both_holdouts: int
    witnesses: tuple[EyeArithmeticWitness, ...]


def _eye_prediction(
    left: tuple[int, int, int],
    right: tuple[int, int, int],
    *,
    left_order: tuple[int, int, int],
    right_order: tuple[int, int, int],
    target_order: tuple[int, int, int],
    a: int,
    b: int,
    offsets: tuple[int, int, int],
) -> int:
    target_digits = [0, 0, 0]
    for output_index in range(3):
        target_digits[target_order[output_index]] = (
            a * left[left_order[output_index]]
            + b * right[right_order[output_index]]
            + offsets[output_index]
        ) % 5
    return 25 * target_digits[0] + 5 * target_digits[1] + target_digits[2]


def audit_eye_arithmetic(
    target_panel: str,
    *,
    representative_limit: int = 20,
) -> EyeArithmeticScreen:
    tables = common_tables()
    sources = tuple(
        panel for panel in FINAL_MESSAGES if panel != target_panel
    )
    left = tuple(base5_digits(value) for value in tables[sources[0]])
    right = tuple(base5_digits(value) for value in tables[sources[1]])
    target = tables[target_panel]
    training_mask = sum(1 << index for index in TRAINING_CLASSES)
    holdout_mask = sum(1 << index for index in HOLDOUT_CLASSES)
    maximum = -1
    cobest = 0
    both = 0
    representatives: list[EyeArithmeticWitness] = []
    for left_order, right_order, target_order in product(EYE_ORDERS, repeat=3):
        target_digits = tuple(base5_digits(value) for value in target)
        for a, b in product(range(5), repeat=2):
            masks: list[tuple[int, ...]] = []
            for output_index in range(3):
                digit_masks = []
                for offset in range(5):
                    mask = 0
                    for class_id in CLASSES:
                        predicted = (
                            a * left[class_id][left_order[output_index]]
                            + b * right[class_id][right_order[output_index]]
                            + offset
                        ) % 5
                        if predicted == target_digits[class_id][
                            target_order[output_index]
                        ]:
                            mask |= 1 << class_id
                    digit_masks.append(mask)
                masks.append(tuple(digit_masks))
            for offsets in product(range(5), repeat=3):
                exact_mask = (
                    masks[0][offsets[0]]
                    & masks[1][offsets[1]]
                    & masks[2][offsets[2]]
                )
                local = (exact_mask & training_mask).bit_count()
                if local > maximum:
                    maximum = local
                    cobest = 0
                    both = 0
                    representatives.clear()
                if local != maximum:
                    continue
                predictions = tuple(
                    _eye_prediction(
                        left[class_id],
                        right[class_id],
                        left_order=left_order,  # type: ignore[arg-type]
                        right_order=right_order,  # type: ignore[arg-type]
                        target_order=target_order,  # type: ignore[arg-type]
                        a=a,
                        b=b,
                        offsets=offsets,  # type: ignore[arg-type]
                    )
                    for class_id in HOLDOUT_CLASSES
                )
                actual = tuple(target[index] for index in HOLDOUT_CLASSES)
                witness = EyeArithmeticWitness(
                    source_panels=sources,  # type: ignore[arg-type]
                    target_panel=target_panel,
                    source_orders=(left_order, right_order),  # type: ignore[arg-type]
                    target_order=target_order,  # type: ignore[arg-type]
                    a=a,
                    b=b,
                    offsets=offsets,  # type: ignore[arg-type]
                    training_matches=local,
                    holdout_predictions=predictions,  # type: ignore[arg-type]
                    holdout_actual=actual,  # type: ignore[arg-type]
                )
                cobest += 1
                both += (
                    (exact_mask & holdout_mask).bit_count()
                    == len(HOLDOUT_CLASSES)
                )
                if len(representatives) < representative_limit:
                    representatives.append(witness)
    return EyeArithmeticScreen(
        target_panel=target_panel,
        models=len(EYE_ORDERS) ** 3 * 5**5,
        maximum_training_matches=maximum,
        cobest_models=cobest,
        cobest_predicting_both_holdouts=both,
        witnesses=tuple(representatives),
    )

