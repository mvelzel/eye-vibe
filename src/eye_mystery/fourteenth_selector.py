"""Five-way raw-eye selector demultiplexing for the fourteenth horizon.

One component of every accepted base-five trigram is treated as a positional
lane tag.  The other two components form an opaque 25-state payload symbol.
The model changes sequence association, so it is not equivalent to a global
permutation of the three eyes.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import permutations
import random

from eye_mystery.practice_cipher4_routes import PatternModel


@dataclass(frozen=True)
class EyeSelectorSpec:
    selector_index: int
    mode: str
    lane_order: tuple[int, ...]
    reversed_mask: int

    @property
    def name(self) -> str:
        order = ",".join(map(str, self.lane_order))
        return (
            f"s{self.selector_index}:{self.mode}:order={order}:"
            f"reverse={self.reversed_mask:05b}"
        )


@dataclass(frozen=True)
class EyeSelectorCandidate:
    spec: EyeSelectorSpec
    train_improvement: float
    heldout_improvement: float


@dataclass(frozen=True)
class EyeSelectorAudit:
    selected: EyeSelectorCandidate
    controls_run: int
    exceedances: int
    null_minimum: float
    null_mean: float
    null_maximum: float
    corrected_upper_tail: float
    stopped_after_rejection: bool


def base5_digits(value: int) -> tuple[int, int, int]:
    if value not in range(125):
        raise ValueError("trigram rank must lie in 0..124")
    return value // 25, value // 5 % 5, value % 5


def selector_coordinates(
    values: Sequence[int], selector_index: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return ordered-pair payloads and selector digits.

    Reversing the two payload fields is a bijection on the 25 pair values.
    The equality-pattern score is label-invariant, so both payload orders are
    provably tied and only the increasing field order is materialized.
    """

    if selector_index not in range(3):
        raise ValueError("selector index must lie in 0..2")
    payload_indexes = tuple(
        index for index in range(3) if index != selector_index
    )
    payload = []
    selectors = []
    for value in values:
        digits = base5_digits(value)
        payload.append(
            5 * digits[payload_indexes[0]] + digits[payload_indexes[1]]
        )
        selectors.append(digits[selector_index])
    return tuple(payload), tuple(selectors)


def selector_specs() -> tuple[EyeSelectorSpec, ...]:
    specs = []
    identity = tuple(range(5))
    for selector_index in range(3):
        specs.extend(
            EyeSelectorSpec(
                selector_index,
                "separate",
                identity,
                mask,
            )
            for mask in range(32)
        )
        specs.extend(
            EyeSelectorSpec(
                selector_index,
                "concatenate",
                tuple(order),
                mask,
            )
            for order in permutations(range(5))
            for mask in range(32)
        )
    return tuple(specs)


def render_selector(
    values: Sequence[int], spec: EyeSelectorSpec
) -> tuple[tuple[int, ...], ...]:
    payload, selectors = selector_coordinates(values, spec.selector_index)
    lanes = [
        tuple(
            value
            for value, selector in zip(payload, selectors, strict=True)
            if selector == lane
        )
        for lane in range(5)
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
                for lane in spec.lane_order
                for value in oriented[lane]
            ),
        )
    raise ValueError(f"unknown selector render mode: {spec.mode}")


def _score(
    streams: Mapping[str, Sequence[int]],
    names: Sequence[str],
    spec: EyeSelectorSpec,
    model: PatternModel,
) -> float:
    return model.score(
        tuple(
            rendered
            for name in names
            for rendered in render_selector(streams[name], spec)
        )
    )


def _baseline(
    streams: Mapping[str, Sequence[int]],
    names: Sequence[str],
    selector_index: int,
    model: PatternModel,
) -> float:
    return model.score(
        tuple(
            selector_coordinates(streams[name], selector_index)[0]
            for name in names
        )
    )


def select_selector_candidate(
    streams: Mapping[str, Sequence[int]],
    model: PatternModel,
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
    specs: Sequence[EyeSelectorSpec] | None = None,
) -> EyeSelectorCandidate:
    """Select solely on training score and evaluate one fixed held-out model."""

    catalog = tuple(specs) if specs is not None else selector_specs()
    train_baselines = {
        selector_index: _baseline(
            streams, train_names, selector_index, model
        )
        for selector_index in range(3)
    }
    selected_spec = max(
        catalog,
        key=lambda spec: (
            _score(streams, train_names, spec, model)
            - train_baselines[spec.selector_index],
            # Deterministic tie break; held-out data is never consulted.
            tuple(-ord(character) for character in spec.name),
        ),
    )
    heldout_baseline = _baseline(
        streams,
        heldout_names,
        selected_spec.selector_index,
        model,
    )
    return EyeSelectorCandidate(
        selected_spec,
        _score(streams, train_names, selected_spec, model)
        - train_baselines[selected_spec.selector_index],
        _score(streams, heldout_names, selected_spec, model)
        - heldout_baseline,
    )


def global_relabel(
    streams: Mapping[str, Sequence[int]],
    labels: Sequence[int],
) -> dict[str, tuple[int, ...]]:
    if sorted(labels) != list(range(83)):
        raise ValueError("labels must permute the accepted 0..82 alphabet")
    return {
        name: tuple(labels[value] for value in stream)
        for name, stream in streams.items()
    }


def audit_selector_demultiplexing(
    streams: Mapping[str, Sequence[int]],
    model: PatternModel,
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
    controls: int,
    seed: int,
    rejection_exceedances: int = 2,
) -> EyeSelectorAudit:
    """Run global-label controls, optionally stopping once promotion is impossible.

    With a maximum of 200 controls, two null exceedances plus the standard
    pseudocount imply a minimum tail of 3/201, already above the frozen .01
    line. Stopping then reports a conservative lower bound rather than an
    exact Monte Carlo tail.
    """

    if controls < 1:
        raise ValueError("at least one control is required")
    if rejection_exceedances < 1:
        raise ValueError("rejection threshold must be positive")
    if any(
        value not in range(83)
        for stream in streams.values()
        for value in stream
    ):
        raise ValueError("controls require accepted Eye labels 0..82")

    selected = select_selector_candidate(
        streams,
        model,
        train_names=train_names,
        heldout_names=heldout_names,
    )
    rng = random.Random(seed)
    null = []
    exceedances = 0
    stopped = False
    for _ in range(controls):
        labels = list(range(83))
        rng.shuffle(labels)
        relabeled = global_relabel(streams, labels)
        score = select_selector_candidate(
            relabeled,
            model,
            train_names=train_names,
            heldout_names=heldout_names,
        ).heldout_improvement
        null.append(score)
        exceedances += score >= selected.heldout_improvement
        if exceedances >= rejection_exceedances:
            stopped = len(null) < controls
            break

    denominator = controls + 1 if stopped else len(null) + 1
    return EyeSelectorAudit(
        selected,
        len(null),
        exceedances,
        min(null),
        sum(null) / len(null),
        max(null),
        (1 + exceedances) / denominator,
        stopped,
    )


def interleave_selector_lanes(
    lanes: Sequence[Sequence[int]],
    selectors: Sequence[int],
    *,
    selector_index: int = 2,
) -> tuple[int, ...]:
    """Create raw-cube trigram ranks from five payload lanes."""

    if len(lanes) != 5:
        raise ValueError("exactly five lanes are required")
    if selector_index not in range(3):
        raise ValueError("selector index must lie in 0..2")
    payload_indexes = tuple(
        index for index in range(3) if index != selector_index
    )
    cursors = [0] * 5
    output = []
    for selector in selectors:
        if selector not in range(5):
            raise ValueError("selector lies outside 0..4")
        cursor = cursors[selector]
        if cursor >= len(lanes[selector]):
            raise ValueError("selector over-consumes a lane")
        payload = lanes[selector][cursor]
        if payload not in range(25):
            raise ValueError("payload lies outside 0..24")
        digits = [0, 0, 0]
        digits[selector_index] = selector
        digits[payload_indexes[0]], digits[payload_indexes[1]] = divmod(
            payload, 5
        )
        output.append(25 * digits[0] + 5 * digits[1] + digits[2])
        cursors[selector] += 1
    if any(
        cursor != len(lane)
        for cursor, lane in zip(cursors, lanes, strict=True)
    ):
        raise ValueError("selectors do not consume every lane value")
    return tuple(output)
