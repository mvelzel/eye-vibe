"""Projective pair projections and affine 83-to-42 quotients for Cipher 3."""

from __future__ import annotations

import math
import random
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass

from eye_mystery.practice_cipher3_two_sheet import (
    QUOTIENT_SIZE,
    SIZE,
    TwoSheetLanguageModel,
    involution_orbits,
    involution_quotient_table,
)
from eye_mystery.practice_cipher3_wide import normalize_plaintext42


@dataclass(frozen=True, order=True)
class PairRoute:
    stride: int
    start: int

    def __post_init__(self) -> None:
        if (self.stride, self.start) not in {
            (1, 0),
            (1, 1),
            (2, 0),
            (2, 1),
            (2, 2),
        }:
            raise ValueError("route is outside the frozen five-route family")


ROUTES = (
    PairRoute(1, 0),
    PairRoute(1, 1),
    PairRoute(2, 0),
    PairRoute(2, 1),
    PairRoute(2, 2),
)
PROJECTIVE_SLOPES: tuple[int | None, ...] = tuple(range(SIZE)) + (None,)


@dataclass(frozen=True)
class PairArchitecture:
    route: PairRoute
    slope: int | None
    reflection: int

    def __post_init__(self) -> None:
        if self.slope is not None and self.slope not in range(SIZE):
            raise ValueError("finite slope must lie in 0..82")
        if self.reflection not in range(SIZE):
            raise ValueError("reflection must lie in 0..82")

    @property
    def slope_label(self) -> str:
        return "inf" if self.slope is None else str(self.slope)


def architecture_sort_key(
    architecture: PairArchitecture,
) -> tuple[int, int, int, int]:
    return (
        architecture.route.stride,
        architecture.route.start,
        SIZE if architecture.slope is None else architecture.slope,
        architecture.reflection,
    )


def pair_positions(length: int, route: PairRoute) -> tuple[int, ...]:
    """Return left indices of the frozen consecutive-pair route."""
    return tuple(range(route.start, length - 1, route.stride))


def project_linear_pairs(
    stream: Sequence[int],
    route: PairRoute,
    slope: int | None,
) -> tuple[int, ...]:
    """Project consecutive raw pairs to the projective-linear F83 coordinate."""
    output = []
    for left_index in pair_positions(len(stream), route):
        left = stream[left_index]
        right = stream[left_index + 1]
        if left not in range(SIZE) or right not in range(SIZE):
            raise ValueError("raw pair value lies outside 0..82")
        output.append(
            right if slope is None else (left + slope * right) % SIZE
        )
    return tuple(output)


def quotient_pair_streams(
    streams: Sequence[Sequence[int]],
    architecture: PairArchitecture,
) -> tuple[tuple[int, ...], ...]:
    table = involution_quotient_table(architecture.reflection)
    return tuple(
        tuple(
            table[value]
            for value in project_linear_pairs(
                stream,
                architecture.route,
                architecture.slope,
            )
        )
        for stream in streams
    )


def _bell_number(size: int) -> int:
    bell = [[0] * (size + 1) for _ in range(size + 1)]
    bell[0][0] = 1
    for row in range(1, size + 1):
        bell[row][0] = bell[row - 1][row - 1]
        for column in range(1, row + 1):
            bell[row][column] = (
                bell[row - 1][column - 1] + bell[row][column - 1]
            )
    return bell[size][0]


def equality_pattern(values: Sequence[int]) -> tuple[int, ...]:
    labels: dict[int, int] = {}
    return tuple(
        labels.setdefault(value, len(labels))
        for value in values
    )


@dataclass(frozen=True)
class EqualityPatternModel:
    width: int
    log_probabilities: dict[tuple[int, ...], float]
    unseen_log_probability: float

    @classmethod
    def train(
        cls,
        text: str,
        *,
        width: int = 6,
        alpha: float = 0.5,
    ) -> "EqualityPatternModel":
        if width < 2 or alpha <= 0:
            raise ValueError("invalid equality-pattern model parameters")
        values = normalize_plaintext42(text)
        counts = Counter(
            equality_pattern(values[index : index + width])
            for index in range(len(values) - width + 1)
        )
        denominator = sum(counts.values()) + alpha * _bell_number(width)
        unseen = math.log(alpha / denominator)
        return cls(
            width,
            {
                pattern: math.log((count + alpha) / denominator)
                for pattern, count in counts.items()
            },
            unseen,
        )

    def score(
        self,
        streams: Sequence[Sequence[int]],
    ) -> tuple[float, int]:
        """Return log likelihood relative to independent uniform classes."""
        score = 0.0
        windows = 0
        for stream in streams:
            for index in range(len(stream) - self.width + 1):
                pattern = equality_pattern(
                    stream[index : index + self.width]
                )
                language_log_probability = self.log_probabilities.get(
                    pattern,
                    self.unseen_log_probability,
                )
                distinct = len(set(pattern))
                null_log_probability = (
                    sum(
                        math.log(QUOTIENT_SIZE - offset)
                        for offset in range(distinct)
                    )
                    - self.width * math.log(QUOTIENT_SIZE)
                )
                score += language_log_probability - null_log_probability
                windows += 1
        return score, windows


@dataclass(frozen=True)
class StructuralCandidate:
    architecture: PairArchitecture
    score: float
    windows: int

    @property
    def score_per_window(self) -> float:
        return self.score / self.windows if self.windows else float("-inf")


def screen_structures(
    raw_streams: Sequence[Sequence[int]],
    model: EqualityPatternModel,
) -> tuple[StructuralCandidate, ...]:
    """Score the complete frozen 34,860-member catalog."""
    candidates = []
    quotient_tables = tuple(
        involution_quotient_table(reflection)
        for reflection in range(SIZE)
    )
    for route in ROUTES:
        for slope in PROJECTIVE_SLOPES:
            projected = tuple(
                project_linear_pairs(stream, route, slope)
                for stream in raw_streams
            )
            for reflection, table in enumerate(quotient_tables):
                quotient = tuple(
                    tuple(table[value] for value in stream)
                    for stream in projected
                )
                score, windows = model.score(quotient)
                candidates.append(
                    StructuralCandidate(
                        PairArchitecture(route, slope, reflection),
                        score,
                        windows,
                    )
                )
    return tuple(
        sorted(
            candidates,
            key=lambda result: (
                -result.score_per_window,
                architecture_sort_key(result.architecture),
            ),
        )
    )


def structural_shortlist(
    screened: Sequence[StructuralCandidate],
    per_route: int,
) -> tuple[StructuralCandidate, ...]:
    if per_route < 1:
        raise ValueError("per-route shortlist must be positive")
    selected = []
    for route in ROUTES:
        route_results = [
            result
            for result in screened
            if result.architecture.route == route
        ]
        selected.extend(route_results[:per_route])
    return tuple(selected)


@dataclass(frozen=True)
class PairLanguageResult:
    architecture: PairArchitecture
    score: float
    windows: int
    key: tuple[int, ...]

    @property
    def score_per_window(self) -> float:
        return self.score / self.windows if self.windows else float("-inf")


def optimize_substitution(
    quotient_streams: Sequence[Sequence[int]],
    model: TwoSheetLanguageModel,
    architecture: PairArchitecture,
    *,
    restarts: int,
    iterations: int,
    seed: int,
) -> PairLanguageResult:
    """Optimize one bijective 42-symbol key for fixed quotient streams."""
    if restarts < 1 or iterations < 1:
        raise ValueError("restarts and iterations must be positive")
    windows = tuple(
        tuple(stream[index : index + 3])
        for stream in quotient_streams
        for index in range(len(stream) - 2)
    )
    affected = [set() for _ in range(QUOTIENT_SIZE)]
    for window_index, window in enumerate(windows):
        for value in set(window):
            affected[value].add(window_index)
    counts = Counter(
        value
        for stream in quotient_streams
        for value in stream
    )
    rng = random.Random(seed)
    table = model.trigrams.log_probabilities
    best_score = float("-inf")
    best_key: tuple[int, ...] | None = None

    for restart in range(restarts):
        if restart == 0:
            state_order = sorted(
                range(QUOTIENT_SIZE),
                key=lambda value: (-counts[value], value),
            )
            key = [-1] * QUOTIENT_SIZE
            for state, plaintext in zip(
                state_order,
                model.frequency_order,
                strict=True,
            ):
                key[state] = plaintext
        else:
            key = list(range(QUOTIENT_SIZE))
            rng.shuffle(key)

        def window_score(window_index: int) -> float:
            left, middle, right = windows[window_index]
            return table[
                (QUOTIENT_SIZE * key[left] + key[middle])
                * QUOTIENT_SIZE
                + key[right]
            ]

        scores = [
            window_score(window_index)
            for window_index in range(len(windows))
        ]
        score = sum(scores)
        if score > best_score:
            best_score = score
            best_key = tuple(key)

        for iteration in range(iterations):
            left, right = rng.sample(range(QUOTIENT_SIZE), 2)
            changed = affected[left] | affected[right]
            before = sum(scores[index] for index in changed)
            key[left], key[right] = key[right], key[left]
            replacements = {
                index: window_score(index)
                for index in changed
            }
            delta = sum(replacements.values()) - before
            progress = iteration / max(1, iterations - 1)
            temperature = 18.0 * (0.08 / 18.0) ** progress
            if delta >= 0 or rng.random() < math.exp(delta / temperature):
                score += delta
                for index, replacement in replacements.items():
                    scores[index] = replacement
                if score > best_score:
                    best_score = score
                    best_key = tuple(key)
            else:
                key[left], key[right] = key[right], key[left]

    assert best_key is not None
    return PairLanguageResult(
        architecture,
        best_score,
        len(windows),
        best_key,
    )


@dataclass(frozen=True)
class PairSearchResult:
    best: PairLanguageResult
    screened: tuple[StructuralCandidate, ...]
    structural_selection: tuple[StructuralCandidate, ...]
    cheap_language: tuple[PairLanguageResult, ...]
    refined: tuple[PairLanguageResult, ...]


def _architecture_seed(architecture: PairArchitecture) -> int:
    route_index = ROUTES.index(architecture.route)
    slope_index = SIZE if architecture.slope is None else architecture.slope
    return (
        1_000_003 * route_index
        + 10_007 * slope_index
        + architecture.reflection
    )


def search_pair_quotients(
    raw_streams: Sequence[Sequence[int]],
    equality_model: EqualityPatternModel,
    language_model: TwoSheetLanguageModel,
    *,
    structural_per_route: int,
    screen_iterations: int,
    refine_shortlist: int,
    refine_restarts: int,
    refine_iterations: int,
    seed: int,
) -> PairSearchResult:
    """Screen every structure, then optimize a frozen bounded shortlist."""
    if refine_shortlist not in range(1, structural_per_route * len(ROUTES) + 1):
        raise ValueError("refine shortlist exceeds structural selection")
    screened = screen_structures(raw_streams, equality_model)
    selected = structural_shortlist(screened, structural_per_route)
    cheap = tuple(
        optimize_substitution(
            quotient_pair_streams(raw_streams, result.architecture),
            language_model,
            result.architecture,
            restarts=1,
            iterations=screen_iterations,
            seed=seed ^ _architecture_seed(result.architecture),
        )
        for result in selected
    )
    refine_architectures = tuple(
        result.architecture
        for result in sorted(
            cheap,
            key=lambda result: (
                -result.score_per_window,
                architecture_sort_key(result.architecture),
            ),
        )[:refine_shortlist]
    )
    refined = tuple(
        optimize_substitution(
            quotient_pair_streams(raw_streams, architecture),
            language_model,
            architecture,
            restarts=refine_restarts,
            iterations=refine_iterations,
            seed=seed ^ 0x5EED0000 ^ _architecture_seed(architecture),
        )
        for architecture in refine_architectures
    )
    best = max(
        refined,
        key=lambda result: (
            result.score_per_window,
            tuple(-value for value in result.key),
        ),
    )
    return PairSearchResult(best, screened, selected, cheap, refined)


def encode_pair_streams(
    plaintexts: Sequence[Sequence[int]],
    raw_lengths: Sequence[int],
    architecture: PairArchitecture,
    key: Sequence[int],
    *,
    seed: int,
) -> tuple[tuple[int, ...], ...]:
    """Encode plaintext through one fixed pair projection and quotient."""
    if sorted(key) != list(range(QUOTIENT_SIZE)):
        raise ValueError("key must permute the 42-symbol plaintext alphabet")
    if len(plaintexts) != len(raw_lengths):
        raise ValueError("plaintext and raw-length counts differ")
    inverse_key = [0] * QUOTIENT_SIZE
    for quotient, plaintext in enumerate(key):
        inverse_key[plaintext] = quotient
    orbits = involution_orbits(architecture.reflection)
    rng = random.Random(seed)
    output = []

    for plaintext, raw_length in zip(
        plaintexts,
        raw_lengths,
        strict=True,
    ):
        positions = pair_positions(raw_length, architecture.route)
        if len(plaintext) != len(positions):
            raise ValueError("plaintext length does not match pair route")
        raw = [rng.randrange(SIZE) for _ in range(raw_length)]
        for left_index, plaintext_value in zip(
            positions,
            plaintext,
            strict=True,
        ):
            if plaintext_value not in range(QUOTIENT_SIZE):
                raise ValueError("plaintext value lies outside 0..41")
            projected = rng.choice(orbits[inverse_key[plaintext_value]])
            right_index = left_index + 1
            if architecture.slope is None:
                raw[right_index] = projected
            elif architecture.slope == 0:
                raw[left_index] = projected
            else:
                raw[right_index] = (
                    (projected - raw[left_index])
                    * pow(architecture.slope, -1, SIZE)
                ) % SIZE
        output.append(tuple(raw))
    return tuple(output)


def decode_with_key(
    quotient_streams: Sequence[Sequence[int]],
    key: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    if sorted(key) != list(range(QUOTIENT_SIZE)):
        raise ValueError("key must permute the 42-symbol plaintext alphabet")
    return tuple(
        tuple(key[value] for value in stream)
        for stream in quotient_streams
    )


def event_accuracy(
    observed: Sequence[Sequence[int]],
    expected: Sequence[Sequence[int]],
) -> float:
    correct = total = 0
    for left_stream, right_stream in zip(
        observed,
        expected,
        strict=True,
    ):
        if len(left_stream) != len(right_stream):
            raise ValueError("stream lengths differ")
        correct += sum(
            left == right
            for left, right in zip(
                left_stream,
                right_stream,
                strict=True,
            )
        )
        total += len(left_stream)
    return correct / total if total else 0.0
