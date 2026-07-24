"""Typed-coordinate and selector-lane tests for sdlwdr practice cipher 4."""

from __future__ import annotations

import random
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import permutations

from eye_mystery.practice_cipher4_routes import PatternModel


@dataclass(frozen=True)
class Coordinates:
    quotient: tuple[int, ...]
    selector: tuple[int, ...]


@dataclass(frozen=True)
class LaneSpec:
    width: int
    mode: str
    order: tuple[int, ...]
    reversed_mask: int

    @property
    def name(self) -> str:
        order = ",".join(map(str, self.order))
        return (
            f"w{self.width}:{self.mode}:order={order}:"
            f"reverse={self.reversed_mask:0{self.width}b}"
        )


@dataclass(frozen=True)
class LaneCandidate:
    spec: LaneSpec
    train_improvement: float
    heldout_improvement: float


@dataclass(frozen=True)
class LaneAudit:
    selected: LaneCandidate
    controls: int
    null_minimum: float
    null_mean: float
    null_maximum: float
    corrected_upper_tail: float


@dataclass(frozen=True)
class ReassociationSpec:
    width: int
    period: int
    variant: str

    @property
    def name(self) -> str:
        return f"w{self.width}:p{self.period}:{self.variant}"


@dataclass(frozen=True)
class ReassociationCandidate:
    spec: ReassociationSpec
    train_improvement: float
    heldout_improvement: float


@dataclass(frozen=True)
class ReassociationAudit:
    selected: ReassociationCandidate
    controls: int
    null_minimum: float
    null_mean: float
    null_maximum: float
    corrected_upper_tail: float


def split_coordinates(
    ranks: Sequence[int], width: int
) -> Coordinates:
    if width not in (2, 3):
        raise ValueError("only widths two and three are supported")
    if any(rank not in range(57) for rank in ranks):
        raise ValueError("ranks must lie in 0..56")
    pairs = tuple(divmod(rank, width) for rank in ranks)
    return Coordinates(
        tuple(quotient for quotient, _ in pairs),
        tuple(selector for _, selector in pairs),
    )


def lane_specs(width: int) -> tuple[LaneSpec, ...]:
    if width not in (2, 3):
        raise ValueError("only widths two and three are supported")
    specs = [
        LaneSpec(width, "separate", tuple(range(width)), mask)
        for mask in range(1 << width)
    ]
    specs.extend(
        LaneSpec(width, "concatenate", tuple(order), mask)
        for order in permutations(range(width))
        for mask in range(1 << width)
    )
    return tuple(specs)


def render_lanes(
    coordinates: Coordinates, spec: LaneSpec
) -> tuple[tuple[int, ...], ...]:
    if len(coordinates.quotient) != len(coordinates.selector):
        raise ValueError("quotient and selector lengths differ")
    if any(selector not in range(spec.width) for selector in coordinates.selector):
        raise ValueError("selector lies outside the declared width")
    lanes = [
        tuple(
            quotient
            for quotient, selector in zip(
                coordinates.quotient,
                coordinates.selector,
                strict=True,
            )
            if selector == lane
        )
        for lane in range(spec.width)
    ]
    oriented = [
        tuple(reversed(lane)) if spec.reversed_mask & (1 << index) else lane
        for index, lane in enumerate(lanes)
    ]
    if spec.mode == "separate":
        return tuple(oriented)
    if spec.mode == "concatenate":
        return (
            tuple(
                value
                for lane in spec.order
                for value in oriented[lane]
            ),
        )
    raise ValueError(f"unknown lane mode: {spec.mode}")


def _score_portions(
    portions: Sequence[Coordinates],
    spec: LaneSpec,
    model: PatternModel,
) -> float:
    return model.score(
        tuple(
            stream
            for portion in portions
            for stream in render_lanes(portion, spec)
        )
    )


def _baseline_score(
    portions: Sequence[Coordinates], model: PatternModel
) -> float:
    return model.score(tuple(portion.quotient for portion in portions))


def shuffle_selectors(
    coordinates: Coordinates,
    width: int,
    rng: random.Random,
) -> Coordinates:
    """Shuffle lane tags while retaining the width-2 rank-56 boundary."""

    selectors = list(coordinates.selector)
    movable = [
        index
        for index, quotient in enumerate(coordinates.quotient)
        if width != 2 or quotient < 28
    ]
    values = [selectors[index] for index in movable]
    rng.shuffle(values)
    for index, selector in zip(movable, values, strict=True):
        selectors[index] = selector
    return Coordinates(coordinates.quotient, tuple(selectors))


def select_lane_candidate(
    by_width: dict[int, tuple[Coordinates, ...]],
    model: PatternModel,
    *,
    train_indices: Sequence[int] = (0, 1),
    heldout_index: int = 2,
) -> LaneCandidate:
    candidates = []
    for width in (2, 3):
        portions = by_width[width]
        train = tuple(portions[index] for index in train_indices)
        heldout = (portions[heldout_index],)
        train_baseline = _baseline_score(train, model)
        heldout_baseline = _baseline_score(heldout, model)
        for spec in lane_specs(width):
            candidates.append(
                LaneCandidate(
                    spec,
                    _score_portions(train, spec, model) - train_baseline,
                    _score_portions(heldout, spec, model) - heldout_baseline,
                )
            )
    return max(
        candidates,
        key=lambda item: (
            item.train_improvement,
            item.heldout_improvement,
            item.spec.name,
        ),
    )


def audit_lane_demultiplex(
    ranks: Sequence[Sequence[int]],
    model: PatternModel,
    *,
    controls: int,
    seed: int,
) -> LaneAudit:
    if len(ranks) != 3:
        raise ValueError("the frozen audit requires three portions")
    if controls < 1:
        raise ValueError("at least one control is required")
    observed = {
        width: tuple(split_coordinates(stream, width) for stream in ranks)
        for width in (2, 3)
    }
    selected = select_lane_candidate(observed, model)
    rng = random.Random(seed)
    null = []
    for _ in range(controls):
        shuffled = {
            width: tuple(
                shuffle_selectors(portion, width, rng)
                for portion in observed[width]
            )
            for width in (2, 3)
        }
        null.append(
            select_lane_candidate(shuffled, model).heldout_improvement
        )
    return LaneAudit(
        selected,
        controls,
        min(null),
        sum(null) / len(null),
        max(null),
        (
            1
            + sum(
                value >= selected.heldout_improvement
                for value in null
            )
        )
        / (controls + 1),
    )


def interleave_lanes(
    lanes: Sequence[Sequence[int]],
    selectors: Sequence[int],
) -> tuple[int, ...]:
    """Build width-tagged ranks from explicit payload lanes."""

    width = len(lanes)
    if width not in (2, 3):
        raise ValueError("only widths two and three are supported")
    cursors = [0] * width
    output = []
    for selector in selectors:
        if selector not in range(width):
            raise ValueError("selector lies outside the lane set")
        cursor = cursors[selector]
        if cursor >= len(lanes[selector]):
            raise ValueError("selector over-consumes a lane")
        quotient = lanes[selector][cursor]
        rank = width * quotient + selector
        if rank not in range(57):
            raise ValueError("interleaved rank lies outside 0..56")
        output.append(rank)
        cursors[selector] += 1
    if any(cursor != len(lane) for cursor, lane in zip(cursors, lanes, strict=True)):
        raise ValueError("selectors do not consume every lane value")
    return tuple(output)


def reassociation_specs() -> tuple[ReassociationSpec, ...]:
    return tuple(
        ReassociationSpec(width, period, variant)
        for width in (2, 3)
        for period in range(2, 33)
        for variant in ("shift-left", "shift-right", "reverse")
    )


def reassociate_selectors(
    coordinates: Coordinates,
    spec: ReassociationSpec,
) -> tuple[int, ...] | None:
    """Pair each quotient with a routed selector from the same short block."""

    output = []
    for start in range(0, len(coordinates.quotient), spec.period):
        quotients = coordinates.quotient[start : start + spec.period]
        selectors = coordinates.selector[start : start + spec.period]
        length = len(quotients)
        if spec.variant == "shift-left":
            order = tuple((index + 1) % length for index in range(length))
        elif spec.variant == "shift-right":
            order = tuple((index - 1) % length for index in range(length))
        elif spec.variant == "reverse":
            order = tuple(reversed(range(length)))
        else:
            raise ValueError(f"unknown reassociation variant: {spec.variant}")
        for index, quotient in enumerate(quotients):
            rank = spec.width * quotient + selectors[order[index]]
            if rank not in range(57):
                return None
            output.append(rank)
    return tuple(output)


def _reassociation_improvements(
    by_width: dict[int, tuple[Coordinates, ...]],
    model: PatternModel,
    spec: ReassociationSpec,
    *,
    train_indices: Sequence[int],
    heldout_index: int,
) -> tuple[float, float] | None:
    portions = by_width[spec.width]
    rendered = tuple(
        reassociate_selectors(portion, spec) for portion in portions
    )
    if any(stream is None for stream in rendered):
        return None
    resolved = tuple(stream for stream in rendered if stream is not None)
    original = tuple(
        tuple(
            spec.width * quotient + selector
            for quotient, selector in zip(
                portion.quotient, portion.selector, strict=True
            )
        )
        for portion in portions
    )
    train_rendered = tuple(resolved[index] for index in train_indices)
    train_original = tuple(original[index] for index in train_indices)
    heldout_rendered = (resolved[heldout_index],)
    heldout_original = (original[heldout_index],)
    return (
        model.score(train_rendered) - model.score(train_original),
        model.score(heldout_rendered) - model.score(heldout_original),
    )


def select_reassociation_candidate(
    by_width: dict[int, tuple[Coordinates, ...]],
    model: PatternModel,
    *,
    train_indices: Sequence[int] = (0, 1),
    heldout_index: int = 2,
) -> ReassociationCandidate:
    candidates = []
    for spec in reassociation_specs():
        improvements = _reassociation_improvements(
            by_width,
            model,
            spec,
            train_indices=train_indices,
            heldout_index=heldout_index,
        )
        if improvements is None:
            continue
        train, heldout = improvements
        candidates.append(ReassociationCandidate(spec, train, heldout))
    if not candidates:
        raise ValueError("no reassociation is valid for these streams")
    return max(
        candidates,
        key=lambda item: (
            item.train_improvement,
            item.heldout_improvement,
            item.spec.name,
        ),
    )


def audit_reassociation(
    ranks: Sequence[Sequence[int]],
    model: PatternModel,
    *,
    controls: int,
    seed: int,
) -> ReassociationAudit:
    if len(ranks) != 3:
        raise ValueError("the frozen audit requires three portions")
    if controls < 1:
        raise ValueError("at least one control is required")
    observed = {
        width: tuple(split_coordinates(stream, width) for stream in ranks)
        for width in (2, 3)
    }
    selected = select_reassociation_candidate(observed, model)
    rng = random.Random(seed)
    null = []
    for _ in range(controls):
        shuffled = {
            width: tuple(
                shuffle_selectors(portion, width, rng)
                for portion in observed[width]
            )
            for width in (2, 3)
        }
        null.append(
            select_reassociation_candidate(
                shuffled, model
            ).heldout_improvement
        )
    return ReassociationAudit(
        selected,
        controls,
        min(null),
        sum(null) / len(null),
        max(null),
        (
            1
            + sum(
                value >= selected.heldout_improvement
                for value in null
            )
        )
        / (controls + 1),
    )
