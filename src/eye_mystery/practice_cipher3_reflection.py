"""Hidden C83/reflection-quotient attack for sdlwdr practice cipher 3."""

from __future__ import annotations

import math
import random
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.practice_cipher3_wide import (
    EXCEPTIONAL_RAW,
    GROUPS,
    RECOVERED_WHEEL_CARDS,
    SIZE,
    TrigramModel42,
    load_cipher3,
    normalize_plaintext42,
)
from eye_mystery.practice_sdlwdr import PLAINTEXT_ALPHABET


def reflection_magnitude(
    left: int,
    right: int,
    coordinates: Sequence[int],
) -> int:
    """Return the nonzero direction-free distance on one hidden C83 wheel."""

    forward = (coordinates[right] - coordinates[left]) % SIZE
    if forward == 0:
        raise ValueError("a reflection transition cannot be a self-loop")
    return min(forward, SIZE - forward)


def reflection_stream(
    message: Sequence[int],
    coordinates: Sequence[int],
) -> tuple[int, ...]:
    return tuple(
        reflection_magnitude(left, right, coordinates) - 1
        for left, right in zip(message, message[1:])
    )


@dataclass(frozen=True)
class ReciprocalAudit:
    directed_edges: int
    reciprocal_pairs: int
    maximum_reciprocal_degree: int
    maximum_single_direction_degree: int


def reciprocal_audit(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> ReciprocalAudit:
    """Give the exact obstruction to one contiguous forward half-cycle."""

    if streams is None:
        streams = load_cipher3()
    edges = {
        (left, right)
        for group in GROUPS
        for message in streams[group]
        for left, right in zip(message, message[1:])
    }
    reciprocal = {
        (left, right)
        for left, right in edges
        if left < right and (right, left) in edges
    }
    degrees = Counter(value for edge in reciprocal for value in edge)
    return ReciprocalAudit(
        len(edges),
        len(reciprocal),
        max(degrees.values()),
        2,
    )


@dataclass(frozen=True)
class ReflectionLanguageModel:
    trigrams: TrigramModel42
    frequency_order: tuple[int, ...]

    @classmethod
    def train(cls, text: str) -> "ReflectionLanguageModel":
        values = normalize_plaintext42(text)
        counts = Counter(values)
        return cls(
            TrigramModel42.train(text),
            tuple(
                sorted(
                    range(42),
                    key=lambda value: (-counts[value], value),
                )
            ),
        )


def render_plaintext(values: Sequence[int]) -> str:
    return "".join(PLAINTEXT_ALPHABET[value] for value in values)


def encode_reflection_messages(
    plaintexts: Sequence[Sequence[int]],
    wheel: Sequence[int],
    plaintext_to_magnitude: Mapping[int, int],
    *,
    seed: int,
) -> tuple[tuple[int, ...], ...]:
    """Encode with random directions; the first raw card is a primer."""

    if tuple(sorted(wheel)) != tuple(range(SIZE)):
        raise ValueError("wheel must permute all 83 raw labels")
    if any(
        magnitude not in range(1, 42)
        for magnitude in plaintext_to_magnitude.values()
    ):
        raise ValueError("magnitudes must lie in 1..41")
    if len(set(plaintext_to_magnitude.values())) != len(
        plaintext_to_magnitude
    ):
        raise ValueError("plaintext magnitudes must be injective")
    rng = random.Random(seed)
    coordinate = [0] * SIZE
    for position, card in enumerate(wheel):
        coordinate[card] = position
    output = []
    for plaintext in plaintexts:
        card = rng.randrange(SIZE)
        message = [card]
        position = coordinate[card]
        for value in plaintext:
            magnitude = plaintext_to_magnitude[value]
            direction = rng.choice((-1, 1))
            position = (position + direction * magnitude) % SIZE
            card = wheel[position]
            message.append(card)
        output.append(tuple(message))
    return tuple(output)


@dataclass(frozen=True)
class ReflectionAnnealResult:
    score: float
    coordinates: tuple[int, ...]
    key: tuple[int, ...]
    plaintexts: tuple[tuple[int, ...], ...]

    @property
    def windows(self) -> int:
        return sum(max(0, len(message) - 2) for message in self.plaintexts)

    @property
    def score_per_trigram(self) -> float:
        return self.score / self.windows if self.windows else float("-inf")


class ReflectionWheelAnnealer:
    """Incrementally optimize one raw wheel and one magnitude substitution."""

    def __init__(
        self,
        messages: Sequence[Sequence[int]],
        model: ReflectionLanguageModel,
    ) -> None:
        self.messages = tuple(tuple(message) for message in messages)
        if any(
            left == right
            for message in self.messages
            for left, right in zip(message, message[1:])
        ):
            raise ValueError("reflection messages cannot contain self-loops")
        self.model = model
        self.event_edges: list[tuple[int, int]] = []
        self.message_events: list[tuple[int, ...]] = []
        self.incident_events = [set() for _ in range(SIZE)]
        for message in self.messages:
            identifiers = []
            for left, right in zip(message, message[1:]):
                event = len(self.event_edges)
                self.event_edges.append((left, right))
                identifiers.append(event)
                self.incident_events[left].add(event)
                self.incident_events[right].add(event)
            self.message_events.append(tuple(identifiers))

        self.windows: list[tuple[int, int, int]] = []
        self.windows_by_event = [
            set() for _ in range(len(self.event_edges))
        ]
        for identifiers in self.message_events:
            for index in range(len(identifiers) - 2):
                window = tuple(identifiers[index : index + 3])
                window_id = len(self.windows)
                self.windows.append(window)  # type: ignore[arg-type]
                for event in window:
                    self.windows_by_event[event].add(window_id)

    def _magnitudes(self, coordinates: Sequence[int]) -> list[int]:
        return [
            reflection_magnitude(left, right, coordinates) - 1
            for left, right in self.event_edges
        ]

    def _frequency_key(
        self,
        magnitudes: Sequence[int],
        rng: random.Random,
    ) -> list[int]:
        counts = Counter(magnitudes)
        magnitude_order = sorted(
            range(41),
            key=lambda value: (
                -counts[value],
                rng.random(),
            ),
        )
        key = [-1] * 42
        for magnitude, plaintext in zip(
            magnitude_order,
            self.model.frequency_order[:41],
            strict=True,
        ):
            key[magnitude] = plaintext
        key[41] = self.model.frequency_order[41]
        return key

    def _plaintexts(
        self,
        magnitudes: Sequence[int],
        key: Sequence[int],
    ) -> tuple[tuple[int, ...], ...]:
        return tuple(
            tuple(key[magnitudes[event]] for event in identifiers)
            for identifiers in self.message_events
        )

    def run(
        self,
        *,
        restarts: int,
        iterations: int,
        seed: int,
        start_temperature: float = 60.0,
        end_temperature: float = 0.1,
        coordinate_move_probability: float = 0.55,
        initial_coordinates: Sequence[int] | None = None,
        initial_key: Sequence[int] | None = None,
    ) -> ReflectionAnnealResult:
        if restarts < 1 or iterations < 1:
            raise ValueError("restarts and iterations must be positive")
        if not 0 <= coordinate_move_probability <= 1:
            raise ValueError("invalid coordinate-move probability")
        rng = random.Random(seed)
        table = self.model.trigrams.log_probabilities
        best_score = float("-inf")
        best_coordinates = best_key = best_magnitudes = None

        for restart in range(restarts):
            if initial_coordinates is not None and (
                restart == 0 or coordinate_move_probability == 0
            ):
                coordinates = list(initial_coordinates)
            elif restart == 0:
                coordinates = list(range(SIZE))
            else:
                order = list(range(SIZE))
                rng.shuffle(order)
                coordinates = [0] * SIZE
                for position, card in enumerate(order):
                    coordinates[card] = position
            if sorted(coordinates) != list(range(SIZE)):
                raise ValueError("initial coordinates must be a permutation")

            magnitudes = self._magnitudes(coordinates)
            events_by_magnitude = [set() for _ in range(41)]
            for event, magnitude in enumerate(magnitudes):
                events_by_magnitude[magnitude].add(event)
            if initial_key is not None and restart == 0:
                key = list(initial_key)
                if sorted(key) != list(range(42)):
                    raise ValueError("initial key must be a permutation")
            else:
                key = self._frequency_key(magnitudes, rng)

            def window_score(window_id: int) -> float:
                left, middle, right = self.windows[window_id]
                code = (
                    (
                        42 * key[magnitudes[left]]
                        + key[magnitudes[middle]]
                    )
                    * 42
                    + key[magnitudes[right]]
                )
                return table[code]

            window_scores = [
                window_score(window_id)
                for window_id in range(len(self.windows))
            ]
            score = sum(window_scores)
            if score > best_score:
                best_score = score
                best_coordinates = tuple(coordinates)
                best_key = tuple(key)
                best_magnitudes = tuple(magnitudes)

            for iteration in range(iterations):
                progress = iteration / max(1, iterations - 1)
                temperature = start_temperature * (
                    end_temperature / start_temperature
                ) ** progress
                coordinate_move = (
                    rng.random() < coordinate_move_probability
                )

                if coordinate_move:
                    left_card, right_card = rng.sample(range(SIZE), 2)
                    affected_events = (
                        self.incident_events[left_card]
                        | self.incident_events[right_card]
                    )
                    affected_windows = set().union(
                        *(
                            self.windows_by_event[event]
                            for event in affected_events
                        )
                    )
                    before = sum(
                        window_scores[window]
                        for window in affected_windows
                    )
                    previous_magnitudes = {
                        event: magnitudes[event]
                        for event in affected_events
                    }
                    (
                        coordinates[left_card],
                        coordinates[right_card],
                    ) = (
                        coordinates[right_card],
                        coordinates[left_card],
                    )
                    for event in affected_events:
                        edge_left, edge_right = self.event_edges[event]
                        magnitudes[event] = (
                            reflection_magnitude(
                                edge_left,
                                edge_right,
                                coordinates,
                            )
                            - 1
                        )
                    replacements = {
                        window: window_score(window)
                        for window in affected_windows
                    }
                    delta = sum(replacements.values()) - before
                    accept = delta >= 0 or rng.random() < math.exp(
                        delta / temperature
                    )
                    if accept:
                        score += delta
                        for window, value in replacements.items():
                            window_scores[window] = value
                        for event, old in previous_magnitudes.items():
                            new = magnitudes[event]
                            if new != old:
                                events_by_magnitude[old].remove(event)
                                events_by_magnitude[new].add(event)
                    else:
                        (
                            coordinates[left_card],
                            coordinates[right_card],
                        ) = (
                            coordinates[right_card],
                            coordinates[left_card],
                        )
                        for event, magnitude in previous_magnitudes.items():
                            magnitudes[event] = magnitude
                else:
                    left_slot, right_slot = rng.sample(range(42), 2)
                    affected_events = (
                        (
                            events_by_magnitude[left_slot]
                            if left_slot < 41
                            else set()
                        )
                        | (
                            events_by_magnitude[right_slot]
                            if right_slot < 41
                            else set()
                        )
                    )
                    affected_windows = set().union(
                        *(
                            self.windows_by_event[event]
                            for event in affected_events
                        )
                    )
                    before = sum(
                        window_scores[window]
                        for window in affected_windows
                    )
                    key[left_slot], key[right_slot] = (
                        key[right_slot],
                        key[left_slot],
                    )
                    replacements = {
                        window: window_score(window)
                        for window in affected_windows
                    }
                    delta = sum(replacements.values()) - before
                    accept = delta >= 0 or rng.random() < math.exp(
                        delta / temperature
                    )
                    if accept:
                        score += delta
                        for window, value in replacements.items():
                            window_scores[window] = value
                    else:
                        key[left_slot], key[right_slot] = (
                            key[right_slot],
                            key[left_slot],
                        )

                if score > best_score:
                    best_score = score
                    best_coordinates = tuple(coordinates)
                    best_key = tuple(key)
                    best_magnitudes = tuple(magnitudes)

        assert (
            best_coordinates is not None
            and best_key is not None
            and best_magnitudes is not None
        )
        return ReflectionAnnealResult(
            best_score,
            best_coordinates,
            best_key,
            self._plaintexts(best_magnitudes, best_key),
        )


def wheel_dihedral_match(
    observed_coordinates: Sequence[int],
    expected_coordinates: Sequence[int],
) -> bool:
    """Return whether two coordinates differ only by rotation/reflection."""

    if len(observed_coordinates) != SIZE or len(expected_coordinates) != SIZE:
        raise ValueError("wheel coordinates must contain 83 values")
    for sign in (-1, 1):
        shift = (
            observed_coordinates[0] - sign * expected_coordinates[0]
        ) % SIZE
        if all(
            observed == (sign * expected + shift) % SIZE
            for observed, expected in zip(
                observed_coordinates,
                expected_coordinates,
                strict=True,
            )
        ):
            return True
    return False


def recovered_wheel_insertions(
) -> tuple[tuple[str, tuple[int, ...], tuple[int, ...]], ...]:
    """Return both orientations and all 83 insertions of exceptional ``J``."""

    candidates = []
    for orientation, base in (
        ("forward", RECOVERED_WHEEL_CARDS),
        ("reverse", tuple(reversed(RECOVERED_WHEEL_CARDS))),
    ):
        for position in range(SIZE):
            wheel = (
                base[:position]
                + (EXCEPTIONAL_RAW,)
                + base[position:]
            )
            coordinates = [0] * SIZE
            for coordinate, card in enumerate(wheel):
                coordinates[card] = coordinate
            candidates.append(
                (
                    f"{orientation}-{position}",
                    tuple(coordinates),
                    wheel,
                )
            )
    return tuple(candidates)


@dataclass(frozen=True)
class FixedWheelScore:
    name: str
    result: ReflectionAnnealResult


def scan_recovered_wheel_insertions(
    messages: Sequence[Sequence[int]],
    model: ReflectionLanguageModel,
    *,
    iterations: int,
    seed: int,
) -> tuple[FixedWheelScore, ...]:
    """Exhaust all old-wheel insertions while optimizing only the language key."""

    annealer = ReflectionWheelAnnealer(messages, model)
    scores = []
    for index, (name, coordinates, _wheel) in enumerate(
        recovered_wheel_insertions()
    ):
        result = annealer.run(
            restarts=1,
            iterations=iterations,
            seed=seed + index,
            start_temperature=20.0,
            coordinate_move_probability=0.0,
            initial_coordinates=coordinates,
        )
        scores.append(FixedWheelScore(name, result))
    return tuple(
        sorted(
            scores,
            key=lambda score: (
                -score.result.score_per_trigram,
                score.name,
            ),
        )
    )
