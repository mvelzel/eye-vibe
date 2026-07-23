"""Bounded route-transposition screen for practice cipher 4."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from math import log2
import random


@dataclass(frozen=True)
class RouteSpec:
    kind: str
    parameter: int = 0
    variant: str = ""

    @property
    def name(self) -> str:
        suffix = f":{self.parameter}" if self.parameter else ""
        variant = f":{self.variant}" if self.variant else ""
        return f"{self.kind}{suffix}{variant}"


def _inverse_order(order: Sequence[int]) -> tuple[int, ...]:
    inverse = [0] * len(order)
    for output, source in enumerate(order):
        inverse[source] = output
    return tuple(inverse)


def _rectangular_order(
    length: int, width: int, variant: str
) -> tuple[int, ...]:
    rows = [
        list(range(start, min(start + width, length)))
        for start in range(0, length, width)
    ]
    if variant == "columns":
        return tuple(
            row[column]
            for column in range(width)
            for row in rows
            if column < len(row)
        )
    if variant == "snake-rows":
        return tuple(
            value
            for row_index, row in enumerate(rows)
            for value in (row if row_index % 2 == 0 else reversed(row))
        )
    if variant == "snake-columns":
        columns = [
            [row[column] for row in rows if column < len(row)]
            for column in range(width)
        ]
        return tuple(
            value
            for column_index, column in enumerate(columns)
            for value in (
                column if column_index % 2 == 0 else reversed(column)
            )
        )
    raise ValueError(f"unknown rectangular variant: {variant}")


def _rail_order(length: int, rails: int) -> tuple[int, ...]:
    period = 2 * rails - 2
    rail_at = tuple(
        min(index % period, period - index % period)
        for index in range(length)
    )
    return tuple(
        index
        for rail in range(rails)
        for index, value in enumerate(rail_at)
        if value == rail
    )


def _block_order(
    length: int, width: int, variant: str
) -> tuple[int, ...]:
    result: list[int] = []
    for start in range(0, length, width):
        block = list(range(start, min(start + width, length)))
        if variant == "even-odd":
            block = block[::2] + block[1::2]
        elif variant == "odd-even":
            block = block[1::2] + block[::2]
        elif variant == "reverse":
            block.reverse()
        elif variant == "alternating":
            if (start // width) % 2:
                block.reverse()
        else:
            raise ValueError(f"unknown block variant: {variant}")
        result.extend(block)
    return tuple(result)


def route_order(length: int, spec: RouteSpec) -> tuple[int, ...]:
    """Return source indexes in candidate plaintext order."""

    if spec.kind == "identity":
        return tuple(range(length))
    if spec.kind == "reverse":
        return tuple(reversed(range(length)))
    if spec.kind == "global-parity":
        inverse = spec.variant.startswith("inverse-")
        variant = spec.variant.removeprefix("inverse-")
        base = (
            tuple(range(0, length, 2)) + tuple(range(1, length, 2))
            if variant == "even-odd"
            else tuple(range(1, length, 2)) + tuple(range(0, length, 2))
        )
        return _inverse_order(base) if inverse else base
    elif spec.kind == "rect":
        inverse = spec.variant.startswith("inverse-")
        variant = spec.variant.removeprefix("inverse-")
        base = _rectangular_order(length, spec.parameter, variant)
        return _inverse_order(base) if inverse else base
    elif spec.kind == "rail":
        base = _rail_order(length, spec.parameter)
    elif spec.kind == "block":
        inverse = spec.variant.startswith("inverse-")
        variant = spec.variant.removeprefix("inverse-")
        base = _block_order(length, spec.parameter, variant)
        return _inverse_order(base) if inverse else base
    else:
        raise ValueError(f"unknown route kind: {spec.kind}")
    return _inverse_order(base) if spec.variant.startswith("inverse-") else base


def apply_route(values: Sequence[int], spec: RouteSpec) -> tuple[int, ...]:
    return tuple(values[index] for index in route_order(len(values), spec))


def route_specs() -> tuple[RouteSpec, ...]:
    """Return the predeclared identity and bounded small-route families."""

    specs = [RouteSpec("identity"), RouteSpec("reverse")]
    for variant in (
        "even-odd",
        "odd-even",
        "inverse-even-odd",
        "inverse-odd-even",
    ):
        specs.append(RouteSpec("global-parity", variant=variant))
    for width in range(2, 33):
        for variant in (
            "columns",
            "inverse-columns",
            "snake-rows",
            "inverse-snake-rows",
            "snake-columns",
            "inverse-snake-columns",
        ):
            specs.append(RouteSpec("rect", width, variant))
    for rails in range(2, 11):
        specs.append(RouteSpec("rail", rails, "encode"))
        specs.append(RouteSpec("rail", rails, "inverse-encode"))
    for width in range(2, 33):
        for variant in (
            "even-odd",
            "inverse-even-odd",
            "odd-even",
            "inverse-odd-even",
            "reverse",
            "alternating",
        ):
            specs.append(RouteSpec("block", width, variant))
    return tuple(specs)


def canonical_pattern(values: Sequence[int]) -> tuple[int, ...]:
    labels: dict[int, int] = {}
    return tuple(
        labels.setdefault(value, len(labels))
        for value in values
    )


@dataclass(frozen=True)
class PatternModel:
    order: int
    scores: dict[tuple[int, ...], float]
    floor: float

    @classmethod
    def train(
        cls, values: Sequence[int], *, order: int = 8
    ) -> "PatternModel":
        counts = Counter(
            canonical_pattern(values[index : index + order])
            for index in range(len(values) - order + 1)
        )
        total = sum(counts.values())
        return cls(
            order,
            {
                pattern: log2(count / total)
                for pattern, count in counts.items()
            },
            log2(0.05 / total),
        )

    def score(self, streams: Sequence[Sequence[int]]) -> float:
        score = 0.0
        grams = 0
        for stream in streams:
            for index in range(len(stream) - self.order + 1):
                pattern = canonical_pattern(
                    stream[index : index + self.order]
                )
                score += self.scores.get(pattern, self.floor)
                grams += 1
        return score / grams if grams else float("-inf")


@dataclass(frozen=True)
class RouteScore:
    spec: RouteSpec
    score_per_gram: float


@dataclass(frozen=True)
class RouteAudit:
    scores: tuple[RouteScore, ...]
    identity: RouteScore
    best_nonidentity: RouteScore
    improvement: float
    null_minimum: float
    null_mean: float
    null_maximum: float
    corrected_upper_tail: float


def score_routes(
    streams: Sequence[Sequence[int]],
    model: PatternModel,
    specs: Sequence[RouteSpec],
) -> tuple[RouteScore, ...]:
    return tuple(
        RouteScore(
            spec,
            model.score(
                tuple(apply_route(stream, spec) for stream in streams)
            ),
        )
        for spec in specs
    )


def audit_routes(
    streams: Sequence[Sequence[int]],
    model: PatternModel,
    *,
    controls: int,
    seed: int,
    specs: Sequence[RouteSpec] | None = None,
) -> RouteAudit:
    """Select routes and calibrate improvement over identity."""

    catalog = tuple(specs or route_specs())
    scores = score_routes(streams, model, catalog)
    identity = next(score for score in scores if score.spec.kind == "identity")
    best_nonidentity = max(
        (score for score in scores if score.spec.kind != "identity"),
        key=lambda score: score.score_per_gram,
    )
    improvement = best_nonidentity.score_per_gram - identity.score_per_gram
    rng = random.Random(seed)
    null = []
    for _ in range(controls):
        shuffled = []
        for stream in streams:
            values = list(stream)
            rng.shuffle(values)
            shuffled.append(tuple(values))
        control_scores = score_routes(shuffled, model, catalog)
        control_identity = next(
            score
            for score in control_scores
            if score.spec.kind == "identity"
        )
        control_best = max(
            score.score_per_gram
            for score in control_scores
            if score.spec.kind != "identity"
        )
        null.append(control_best - control_identity.score_per_gram)
    return RouteAudit(
        tuple(
            sorted(
                scores,
                key=lambda score: score.score_per_gram,
                reverse=True,
            )
        ),
        identity,
        best_nonidentity,
        improvement,
        min(null),
        sum(null) / len(null),
        max(null),
        (1 + sum(value >= improvement for value in null))
        / (controls + 1),
    )
