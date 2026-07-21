"""Exhaust a low-capacity S3 transducer over the five raw eye directions."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import permutations


Permutation = tuple[int, int, int]
Edge = tuple[int, int]
S3: tuple[Permutation, ...] = tuple(permutations(range(3)))
IDENTITY: Permutation = (0, 1, 2)


def compose(first: Permutation, second: Permutation) -> Permutation:
    """Apply ``first`` and then ``second``."""

    return tuple(second[first[index]] for index in range(3))  # type: ignore[return-value]


def body_product(
    raw_body: Sequence[int],
    direction_operations: Sequence[Permutation],
    eye_order: Sequence[int],
) -> Permutation:
    """Compose one operation per raw direction, with a fixed eye order."""

    if len(raw_body) % 3:
        raise ValueError("raw body length must be divisible by three")
    if len(direction_operations) != 5 or len(set(direction_operations)) != 5:
        raise ValueError("the five directions must name five distinct operations")
    if sorted(eye_order) != [0, 1, 2]:
        raise ValueError("eye order must permute three positions")
    result = IDENTITY
    for offset in range(0, len(raw_body), 3):
        trigram = raw_body[offset : offset + 3]
        for index in eye_order:
            result = compose(result, direction_operations[trigram[index]])
    return result


@dataclass(frozen=True)
class S3TransducerModel:
    direction_operations: tuple[Permutation, ...]
    eye_order: tuple[int, int, int]
    body_outputs: tuple[Permutation, ...]
    edge_matches: int


@dataclass(frozen=True)
class S3TransducerScan:
    match_histogram: tuple[tuple[int, int], ...]
    best_models: tuple[S3TransducerModel, ...]
    all_outputs: tuple[tuple[Permutation, ...], ...]

    @property
    def best_match_count(self) -> int:
        return self.best_models[0].edge_matches


def scan_s3_direction_transducers(
    raw_bodies: Sequence[Sequence[int]], edges: Sequence[Edge]
) -> S3TransducerScan:
    """Exhaust all ``6P5`` injective direction maps and six eye orders."""

    if len(raw_bodies) != len(edges):
        raise ValueError("every body needs one target edge")
    histogram: Counter[int] = Counter()
    best: list[S3TransducerModel] = []
    all_outputs: list[tuple[Permutation, ...]] = []
    best_count = -1
    for direction_operations in permutations(S3, 5):
        for eye_order in permutations(range(3)):
            outputs = tuple(
                body_product(body, direction_operations, eye_order)
                for body in raw_bodies
            )
            matches = sum(
                output[source] == target
                for output, (source, target) in zip(outputs, edges, strict=True)
            )
            histogram[matches] += 1
            all_outputs.append(outputs)
            model = S3TransducerModel(
                direction_operations=direction_operations,
                eye_order=eye_order,
                body_outputs=outputs,
                edge_matches=matches,
            )
            if matches > best_count:
                best_count = matches
                best = [model]
            elif matches == best_count:
                best.append(model)
    return S3TransducerScan(
        match_histogram=tuple(sorted(histogram.items())),
        best_models=tuple(best),
        all_outputs=tuple(all_outputs),
    )


@dataclass(frozen=True)
class BodyAssignmentCalibration:
    below_eight: int
    exactly_eight: int
    all_nine: int

    @property
    def total(self) -> int:
        return self.below_eight + self.exactly_eight + self.all_nine


def calibrate_body_assignments(
    all_outputs: Sequence[Sequence[Permutation]], edges: Sequence[Edge]
) -> BodyAssignmentCalibration:
    """Exhaust body-to-header assignments, preserving each intact body.

    Bit sets represent which transducer models satisfy each header/body pair.
    This makes the exact ``9!`` conditional calibration inexpensive.
    """

    body_count = len(edges)
    if body_count != 9 or any(len(outputs) != body_count for outputs in all_outputs):
        raise ValueError("the exact calibration expects nine headers and bodies")
    model_count = len(all_outputs)
    match_bits = [[0] * body_count for _ in range(body_count)]
    for model_index, outputs in enumerate(all_outputs):
        bit = 1 << model_index
        for header_index, (source, target) in enumerate(edges):
            for body_index, output in enumerate(outputs):
                if output[source] == target:
                    match_bits[header_index][body_index] |= bit

    all_models = (1 << model_count) - 1
    below_eight = exactly_eight = all_nine = 0
    for assignment in permutations(range(body_count)):
        conditions = tuple(
            match_bits[header_index][body_index]
            for header_index, body_index in enumerate(assignment)
        )
        prefix = [all_models]
        for condition in conditions:
            prefix.append(prefix[-1] & condition)
        if prefix[-1]:
            all_nine += 1
            continue
        suffix = [all_models] * (body_count + 1)
        for index in range(body_count - 1, -1, -1):
            suffix[index] = suffix[index + 1] & conditions[index]
        if any(
            prefix[index] & suffix[index + 1]
            for index in range(body_count)
        ):
            exactly_eight += 1
        else:
            below_eight += 1
    return BodyAssignmentCalibration(below_eight, exactly_eight, all_nine)
