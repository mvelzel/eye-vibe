"""Typed cross-glyph eye-track reassociation for the fourteenth horizon."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import random

from eye_mystery.fourteenth_selector import base5_digits, global_relabel
from eye_mystery.practice_cipher4_routes import PatternModel


@dataclass(frozen=True, order=True)
class TrackReassociationSpec:
    component: int
    period: int
    variant: str

    @property
    def name(self) -> str:
        return f"c{self.component}:p{self.period}:{self.variant}"


@dataclass(frozen=True)
class TrackReassociationCandidate:
    spec: TrackReassociationSpec
    train_improvement: float
    heldout_improvement: float
    heldout_valid: bool


@dataclass(frozen=True)
class TrackReassociationAudit:
    selected: TrackReassociationCandidate | None
    valid_training_candidates: int
    controls_run: int
    exceedances: int
    invalid_controls: int
    null_minimum: float
    null_mean: float
    null_maximum: float
    corrected_upper_tail: float
    stopped_after_rejection: bool


def reassociation_specs() -> tuple[TrackReassociationSpec, ...]:
    return tuple(
        TrackReassociationSpec(component, period, variant)
        for component in range(3)
        for period in range(2, 27)
        for variant in ("shift-left", "shift-right", "reverse")
    )


def reassociate_track(
    values: Sequence[int],
    spec: TrackReassociationSpec,
) -> tuple[int, ...] | None:
    """Route one component inside each block, preserving the other two."""

    if spec.component not in range(3):
        raise ValueError("component must lie in 0..2")
    if spec.period < 2:
        raise ValueError("period must be at least two")
    if spec.variant not in ("shift-left", "shift-right", "reverse"):
        raise ValueError(f"unknown reassociation variant: {spec.variant}")

    digits = [list(base5_digits(value)) for value in values]
    output = [row.copy() for row in digits]
    for start in range(0, len(values), spec.period):
        stop = min(start + spec.period, len(values))
        length = stop - start
        if spec.variant == "shift-left":
            sources = tuple(
                start + (index + 1) % length for index in range(length)
            )
        elif spec.variant == "shift-right":
            sources = tuple(
                start + (index - 1) % length for index in range(length)
            )
        else:
            sources = tuple(reversed(range(start, stop)))
        for offset, source in enumerate(sources):
            output[start + offset][spec.component] = digits[source][
                spec.component
            ]

    ranks = tuple(
        25 * row[0] + 5 * row[1] + row[2] for row in output
    )
    if any(rank not in range(83) for rank in ranks):
        return None
    return ranks


def _score(
    streams: Mapping[str, Sequence[int]],
    names: Sequence[str],
    spec: TrackReassociationSpec,
    model: PatternModel,
) -> float | None:
    rendered = []
    for name in names:
        stream = reassociate_track(streams[name], spec)
        if stream is None:
            return None
        rendered.append(stream)
    return model.score(tuple(rendered))


def valid_reassociation_specs(
    streams: Mapping[str, Sequence[int]],
    names: Sequence[str],
    *,
    specs: Sequence[TrackReassociationSpec] | None = None,
) -> tuple[TrackReassociationSpec, ...]:
    catalog = tuple(specs) if specs is not None else reassociation_specs()
    return tuple(
        spec
        for spec in catalog
        if all(
            reassociate_track(streams[name], spec) is not None
            for name in names
        )
    )


def select_reassociation_candidate(
    streams: Mapping[str, Sequence[int]],
    model: PatternModel,
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
    specs: Sequence[TrackReassociationSpec] | None = None,
) -> TrackReassociationCandidate:
    catalog = tuple(specs) if specs is not None else reassociation_specs()
    train_baseline = model.score(tuple(streams[name] for name in train_names))
    train_scores = {
        spec: score
        for spec in catalog
        if (score := _score(streams, train_names, spec, model)) is not None
    }
    if not train_scores:
        raise ValueError("no reassociation candidate stays in range on training")
    selected = min(
        train_scores,
        key=lambda spec: (
            -(train_scores[spec] - train_baseline),
            spec,
        ),
    )
    heldout_baseline = model.score(
        tuple(streams[name] for name in heldout_names)
    )
    heldout_score = _score(streams, heldout_names, selected, model)
    return TrackReassociationCandidate(
        selected,
        train_scores[selected] - train_baseline,
        (
            heldout_score - heldout_baseline
            if heldout_score is not None
            else float("-inf")
        ),
        heldout_score is not None,
    )


def audit_track_reassociation(
    streams: Mapping[str, Sequence[int]],
    model: PatternModel,
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
    controls: int,
    seed: int,
    rejection_exceedances: int = 2,
) -> TrackReassociationAudit:
    if controls < 1:
        raise ValueError("at least one control is required")
    if any(
        value not in range(83)
        for stream in streams.values()
        for value in stream
    ):
        raise ValueError("controls require accepted Eye labels 0..82")

    valid_training = valid_reassociation_specs(streams, train_names)
    if not valid_training:
        return TrackReassociationAudit(
            selected=None,
            valid_training_candidates=0,
            controls_run=0,
            exceedances=0,
            invalid_controls=0,
            null_minimum=float("nan"),
            null_mean=float("nan"),
            null_maximum=float("nan"),
            corrected_upper_tail=1.0,
            stopped_after_rejection=True,
        )
    selected = select_reassociation_candidate(
        streams,
        model,
        train_names=train_names,
        heldout_names=heldout_names,
        specs=valid_training,
    )
    if not selected.heldout_valid:
        return TrackReassociationAudit(
            selected=selected,
            valid_training_candidates=len(valid_training),
            controls_run=0,
            exceedances=0,
            invalid_controls=0,
            null_minimum=float("nan"),
            null_mean=float("nan"),
            null_maximum=float("nan"),
            corrected_upper_tail=1.0,
            stopped_after_rejection=True,
        )

    rng = random.Random(seed)
    null = []
    exceedances = 0
    invalid = 0
    stopped = False
    for _ in range(controls):
        labels = list(range(83))
        rng.shuffle(labels)
        relabeled = global_relabel(streams, labels)
        control = select_reassociation_candidate(
            relabeled,
            model,
            train_names=train_names,
            heldout_names=heldout_names,
        )
        if not control.heldout_valid:
            invalid += 1
            value = float("-inf")
        else:
            value = control.heldout_improvement
        null.append(value)
        exceedances += value >= selected.heldout_improvement
        if exceedances >= rejection_exceedances:
            stopped = len(null) < controls
            break

    denominator = controls + 1 if stopped else len(null) + 1
    finite = tuple(value for value in null if value != float("-inf"))
    return TrackReassociationAudit(
        selected=selected,
        valid_training_candidates=len(valid_training),
        controls_run=len(null),
        exceedances=exceedances,
        invalid_controls=invalid,
        null_minimum=min(finite) if finite else float("-inf"),
        null_mean=sum(finite) / len(finite) if finite else float("-inf"),
        null_maximum=max(finite) if finite else float("-inf"),
        corrected_upper_tail=(1 + exceedances) / denominator,
        stopped_after_rejection=stopped,
    )
