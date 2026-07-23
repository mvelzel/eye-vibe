"""Leakage-controlled selector prediction for practice cipher 4."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from math import log2
import random


@dataclass(frozen=True)
class ContextSpec:
    name: str
    phase: int | None = None


def context_specs() -> tuple[ContextSpec, ...]:
    specs = [
        ContextSpec("q"),
        ContextSpec("previous-q"),
        ContextSpec("next-q"),
        ContextSpec("delta-q"),
        ContextSpec("previous-r"),
        ContextSpec("q+previous-r"),
        ContextSpec("previous-q+q"),
        ContextSpec("q+next-q"),
        ContextSpec("previous-q+q+previous-r"),
    ]
    for phase in range(2, 17):
        specs.append(ContextSpec("phase", phase))
        specs.append(ContextSpec("q+phase", phase))
    return tuple(specs)


def _context(
    spec: ContextSpec,
    quotient: Sequence[int],
    selector: Sequence[int],
    index: int,
    payload_modulus: int,
) -> tuple[int, ...] | None:
    if spec.name == "q":
        return (quotient[index],)
    if spec.name == "previous-q":
        return None if index == 0 else (quotient[index - 1],)
    if spec.name == "next-q":
        return None if index + 1 == len(quotient) else (quotient[index + 1],)
    if spec.name == "delta-q":
        if index == 0:
            return None
        return ((quotient[index] - quotient[index - 1]) % payload_modulus,)
    if spec.name == "previous-r":
        return None if index == 0 else (selector[index - 1],)
    if spec.name == "q+previous-r":
        return None if index == 0 else (quotient[index], selector[index - 1])
    if spec.name == "previous-q+q":
        return (
            None
            if index == 0
            else (quotient[index - 1], quotient[index])
        )
    if spec.name == "q+next-q":
        return (
            None
            if index + 1 == len(quotient)
            else (quotient[index], quotient[index + 1])
        )
    if spec.name == "previous-q+q+previous-r":
        return (
            None
            if index == 0
            else (quotient[index - 1], quotient[index], selector[index - 1])
        )
    if spec.name == "phase":
        assert spec.phase is not None
        return (index % spec.phase,)
    if spec.name == "q+phase":
        assert spec.phase is not None
        return (quotient[index], index % spec.phase)
    raise ValueError(f"unknown context: {spec.name}")


def _centered_window(
    values: Sequence[int], index: int, radius: int
) -> tuple[int, ...] | None:
    if index < radius or index + radius >= len(values):
        return None
    return tuple(values[index - radius : index + radius + 1])


@dataclass(frozen=True)
class PredictionScore:
    spec: ContextSpec
    gain_bits_per_symbol: float
    accuracy: float
    baseline_accuracy: float
    evaluated: int


def cross_validated_prediction(
    quotient_streams: Sequence[Sequence[int]],
    selector_streams: Sequence[Sequence[int]],
    *,
    spec: ContextSpec,
    selector_size: int,
    payload_modulus: int,
    radius: int = 4,
    alpha: float = 0.5,
) -> PredictionScore:
    """Leave one portion out and reject copied quotient neighborhoods."""

    if len(quotient_streams) != len(selector_streams):
        raise ValueError("quotient and selector stream counts differ")
    if any(
        len(quotient) != len(selector)
        for quotient, selector in zip(
            quotient_streams, selector_streams, strict=True
        )
    ):
        raise ValueError("quotient and selector stream lengths differ")

    log_gain = 0.0
    correct = 0
    baseline_correct = 0
    evaluated = 0
    scored_windows: set[tuple[int, ...]] = set()

    for held_out in range(len(quotient_streams)):
        context_counts: dict[tuple[int, ...], Counter[int]] = defaultdict(Counter)
        global_counts: Counter[int] = Counter()
        training_windows: set[tuple[int, ...]] = set()
        for stream_index, (quotient, selector) in enumerate(
            zip(quotient_streams, selector_streams, strict=True)
        ):
            if stream_index == held_out:
                continue
            for index, target in enumerate(selector):
                context = _context(
                    spec, quotient, selector, index, payload_modulus
                )
                if context is not None:
                    context_counts[context][target] += 1
                global_counts[target] += 1
                window = _centered_window(quotient, index, radius)
                if window is not None:
                    training_windows.add(window)

        total_global = sum(global_counts.values())
        held_quotient = quotient_streams[held_out]
        held_selector = selector_streams[held_out]
        for index, target in enumerate(held_selector):
            window = _centered_window(held_quotient, index, radius)
            if (
                window is None
                or window in training_windows
                or window in scored_windows
            ):
                continue
            context = _context(
                spec,
                held_quotient,
                held_selector,
                index,
                payload_modulus,
            )
            if context is None:
                continue
            scored_windows.add(window)
            counts = context_counts.get(context)
            baseline_probability = (
                global_counts[target] + alpha
            ) / (total_global + alpha * selector_size)
            if counts:
                model_probability = (counts[target] + alpha) / (
                    sum(counts.values()) + alpha * selector_size
                )
                prediction = max(
                    range(selector_size),
                    key=lambda value: (counts[value], -value),
                )
            else:
                model_probability = baseline_probability
                prediction = max(
                    range(selector_size),
                    key=lambda value: (global_counts[value], -value),
                )
            baseline_prediction = max(
                range(selector_size),
                key=lambda value: (global_counts[value], -value),
            )
            log_gain += log2(model_probability / baseline_probability)
            correct += prediction == target
            baseline_correct += baseline_prediction == target
            evaluated += 1

    return PredictionScore(
        spec,
        log_gain / evaluated if evaluated else 0.0,
        correct / evaluated if evaluated else 0.0,
        baseline_correct / evaluated if evaluated else 0.0,
        evaluated,
    )


@dataclass(frozen=True)
class PredictionAudit:
    scores: tuple[PredictionScore, ...]
    best: PredictionScore
    null_minimum: float
    null_mean: float
    null_maximum: float
    corrected_upper_tail: float


@dataclass(frozen=True)
class PredictionAttribution:
    """Locate whether held-out prediction is only memorized rank reuse."""

    evaluated: int
    seen_context_exact_bigram: int
    correct_seen_context_exact_bigram: int
    seen_context_new_bigram: int
    correct_seen_context_new_bigram: int
    unseen_context: int
    correct_unseen_context: int
    exact_trigram: int
    correct_exact_trigram: int


def attribute_prediction(
    quotient_streams: Sequence[Sequence[int]],
    selector_streams: Sequence[Sequence[int]],
    *,
    spec: ContextSpec,
    selector_size: int,
    payload_modulus: int,
    width: int,
    radius: int = 4,
) -> PredictionAttribution:
    """Partition held-out accuracy by exact rank-bigram reuse."""

    scored_windows: set[tuple[int, ...]] = set()
    totals = Counter[str]()
    for held_out in range(len(quotient_streams)):
        context_counts: dict[tuple[int, ...], Counter[int]] = defaultdict(
            Counter
        )
        global_counts: Counter[int] = Counter()
        training_windows: set[tuple[int, ...]] = set()
        training_bigrams: set[tuple[int, int]] = set()
        training_trigrams: set[tuple[int, int, int]] = set()
        for stream_index, (quotient, selector) in enumerate(
            zip(quotient_streams, selector_streams, strict=True)
        ):
            if stream_index == held_out:
                continue
            ranks = tuple(
                width * q_value + r_value
                for q_value, r_value in zip(
                    quotient, selector, strict=True
                )
            )
            training_bigrams.update(zip(ranks, ranks[1:]))
            training_trigrams.update(
                zip(ranks, ranks[1:], ranks[2:])
            )
            for index, target in enumerate(selector):
                context = _context(
                    spec, quotient, selector, index, payload_modulus
                )
                if context is not None:
                    context_counts[context][target] += 1
                global_counts[target] += 1
                window = _centered_window(quotient, index, radius)
                if window is not None:
                    training_windows.add(window)

        held_quotient = quotient_streams[held_out]
        held_selector = selector_streams[held_out]
        held_ranks = tuple(
            width * q_value + r_value
            for q_value, r_value in zip(
                held_quotient, held_selector, strict=True
            )
        )
        for index, target in enumerate(held_selector):
            window = _centered_window(held_quotient, index, radius)
            if (
                window is None
                or window in training_windows
                or window in scored_windows
            ):
                continue
            context = _context(
                spec,
                held_quotient,
                held_selector,
                index,
                payload_modulus,
            )
            if context is None:
                continue
            scored_windows.add(window)
            counts = context_counts.get(context)
            prediction_counts = counts or global_counts
            prediction = max(
                range(selector_size),
                key=lambda value: (prediction_counts[value], -value),
            )
            correct = prediction == target
            totals["evaluated"] += 1
            if index >= 2 and tuple(held_ranks[index - 2 : index + 1]) in (
                training_trigrams
            ):
                totals["exact_trigram"] += 1
                totals["correct_exact_trigram"] += correct
            if counts is None:
                totals["unseen_context"] += 1
                totals["correct_unseen_context"] += correct
            elif (held_ranks[index - 1], held_ranks[index]) in (
                training_bigrams
            ):
                totals["seen_context_exact_bigram"] += 1
                totals["correct_seen_context_exact_bigram"] += correct
            else:
                totals["seen_context_new_bigram"] += 1
                totals["correct_seen_context_new_bigram"] += correct

    return PredictionAttribution(
        **{
            field: totals[field]
            for field in PredictionAttribution.__dataclass_fields__
        }
    )


def audit_selector_prediction(
    quotient_streams: Sequence[Sequence[int]],
    selector_streams: Sequence[Sequence[int]],
    *,
    selector_size: int,
    payload_modulus: int,
    controls: int,
    seed: int,
    null_mode: str = "selector",
) -> PredictionAudit:
    """Select the best declared context and calibrate the same selection."""

    specs = context_specs()
    scores = tuple(
        cross_validated_prediction(
            quotient_streams,
            selector_streams,
            spec=spec,
            selector_size=selector_size,
            payload_modulus=payload_modulus,
        )
        for spec in specs
    )
    best = max(scores, key=lambda score: score.gain_bits_per_symbol)
    rng = random.Random(seed)
    null = []
    for _ in range(controls):
        shuffled_quotients = [tuple(stream) for stream in quotient_streams]
        shuffled_selectors = []
        if null_mode == "selector":
            for stream in selector_streams:
                values = list(stream)
                rng.shuffle(values)
                shuffled_selectors.append(tuple(values))
        elif null_mode == "within-q":
            for quotient, selector in zip(
                quotient_streams, selector_streams, strict=True
            ):
                values = list(selector)
                positions_by_quotient: dict[int, list[int]] = defaultdict(list)
                for index, value in enumerate(quotient):
                    positions_by_quotient[value].append(index)
                for positions in positions_by_quotient.values():
                    replacements = [values[index] for index in positions]
                    rng.shuffle(replacements)
                    for index, replacement in zip(
                        positions, replacements, strict=True
                    ):
                        values[index] = replacement
                shuffled_selectors.append(tuple(values))
        elif null_mode == "circular-selector":
            for stream in selector_streams:
                offset = rng.randrange(1, len(stream))
                shuffled_selectors.append(
                    tuple(stream[offset:]) + tuple(stream[:offset])
                )
        elif null_mode == "paired-rank":
            shuffled_quotients = []
            for quotient, selector in zip(
                quotient_streams, selector_streams, strict=True
            ):
                pairs = list(zip(quotient, selector, strict=True))
                rng.shuffle(pairs)
                shuffled_quotients.append(
                    tuple(value[0] for value in pairs)
                )
                shuffled_selectors.append(
                    tuple(value[1] for value in pairs)
                )
        else:
            raise ValueError(f"unknown null mode: {null_mode}")
        control_scores = (
            cross_validated_prediction(
                shuffled_quotients,
                shuffled_selectors,
                spec=spec,
                selector_size=selector_size,
                payload_modulus=payload_modulus,
            )
            for spec in specs
        )
        null.append(
            max(score.gain_bits_per_symbol for score in control_scores)
        )
    return PredictionAudit(
        tuple(
            sorted(
                scores,
                key=lambda score: score.gain_bits_per_symbol,
                reverse=True,
            )
        ),
        best,
        min(null),
        sum(null) / len(null),
        max(null),
        (1 + sum(value >= best.gain_bits_per_symbol for value in null))
        / (controls + 1),
    )
