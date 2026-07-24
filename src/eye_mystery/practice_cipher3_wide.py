"""Bounded mechanism transfers for sdlwdr practice cipher 3."""

from __future__ import annotations

import json
import math
import random
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from eye_mystery.deck_selected import ACTIONS, selected_action_indices
from eye_mystery.deck_shuffles import standard_base_candidates
from eye_mystery.practice_cipher4_factor import serial_mutual_information
from eye_mystery.practice_cipher5 import (
    decode_dynamic_substitution,
    encode_dynamic_substitution,
    recursive_increasing_chunk_reversal,
)
from eye_mystery.practice_sdlwdr import (
    COMBINED82,
    EXCEPTIONAL_RAW,
    PLAINTEXT_ALPHABET,
    PLAINTEXT_WHEEL,
)


SIZE = 83
GROUPS = ("A", "B", "C")
ROOT = Path(__file__).resolve().parents[2]


def load_cipher3() -> dict[str, tuple[tuple[int, ...], ...]]:
    data = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher3.json").read_text()
    )
    return {
        group: tuple(tuple(message) for message in data[group])
        for group in GROUPS
    }


def recovered_wheel_cards() -> tuple[int, ...]:
    """Return the 82 ordinary raw labels in the recovered cyclic order."""

    cards = tuple(
        0 if character == "~" else ord(character) - 32
        for character in COMBINED82
    )
    if len(cards) != 82 or len(set(cards)) != 82:
        raise AssertionError("the recovered ciphertext wheel must have 82 cards")
    if EXCEPTIONAL_RAW in cards:
        raise AssertionError("the exceptional J must not lie on the wheel")
    return cards


RECOVERED_WHEEL_CARDS = recovered_wheel_cards()
RECOVERED_WHEEL_COORDINATES = {
    card: coordinate
    for coordinate, card in enumerate(RECOVERED_WHEEL_CARDS)
}


def common_prefix_length(
    left: Sequence[int],
    right: Sequence[int],
) -> int:
    """Return the number of literally equal leading values."""

    return next(
        (
            index
            for index, (left_value, right_value) in enumerate(
                zip(left, right, strict=False)
            )
            if left_value != right_value
        ),
        min(len(left), len(right)),
    )


@dataclass(frozen=True)
class PrefixRelation:
    left: str
    right: str
    full_length: int
    body_length: int


def prefix_relations(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> tuple[PrefixRelation, ...]:
    """Inventory every nonempty literal prefix shared by two reset streams."""

    if streams is None:
        streams = load_cipher3()
    named = tuple(
        (f"{group}{index}", tuple(message))
        for group in GROUPS
        for index, message in enumerate(streams[group])
    )
    relations = []
    for left_index, (left_name, left) in enumerate(named):
        for right_name, right in named[left_index + 1 :]:
            full = common_prefix_length(left, right)
            body = common_prefix_length(left[1:], right[1:])
            if full or body:
                relations.append(
                    PrefixRelation(left_name, right_name, full, body)
                )
    return tuple(
        sorted(
            relations,
            key=lambda relation: (
                -relation.body_length,
                -relation.full_length,
                relation.left,
                relation.right,
            ),
        )
    )


def shuffled_body_prefix_maxima(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
    *,
    controls: int,
    seed: int,
) -> tuple[int, ...]:
    """Shuffle every body independently and retain its maximum pairwise LCP.

    Each control preserves every message's exact symbol multiset and length.
    Random shuffles that create an adjacent double are retried, preserving the
    observed no-double condition as well.
    """

    if controls < 1:
        raise ValueError("at least one control is required")
    if streams is None:
        streams = load_cipher3()
    bodies = [
        tuple(message[1:])
        for group in GROUPS
        for message in streams[group]
    ]
    rng = random.Random(seed)
    maxima = []
    for _ in range(controls):
        shuffled = []
        for body in bodies:
            candidate = list(body)
            for _attempt in range(10_000):
                rng.shuffle(candidate)
                if all(
                    left != right
                    for left, right in zip(candidate, candidate[1:])
                ):
                    break
            else:
                raise RuntimeError("could not construct a no-double control")
            shuffled.append(tuple(candidate))
        maxima.append(
            max(
                common_prefix_length(left, right)
                for left_index, left in enumerate(shuffled)
                for right in shuffled[left_index + 1 :]
            )
        )
    return tuple(maxima)


@dataclass(frozen=True)
class TransitionGraphAudit:
    events: int
    unique_edges: int
    repeated_events: int
    maximum_multiplicity: int
    maximum_outdegree: int
    maximum_indegree: int
    effective_uniform_choices: float


def _effective_uniform_choices(
    visits: Sequence[int],
    observed_distinct: int,
) -> float:
    """Invert the uniform occupancy expectation for the observed row visits."""

    lower = 1.0
    upper = 10_000.0
    for _ in range(100):
        choices = (lower + upper) / 2
        expected = sum(
            choices * (1 - (1 - 1 / choices) ** count)
            for count in visits
        )
        if expected < observed_distinct:
            lower = choices
        else:
            upper = choices
    return (lower + upper) / 2


def transition_graph_audit(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> TransitionGraphAudit:
    """Summarize the previous-ciphertext directed transition graph."""

    if streams is None:
        streams = load_cipher3()
    transitions = tuple(
        (left, right)
        for group in GROUPS
        for message in streams[group]
        for left, right in zip(message, message[1:])
    )
    multiplicities = Counter(transitions)
    outgoing: dict[int, set[int]] = {
        value: set() for value in range(SIZE)
    }
    incoming: dict[int, set[int]] = {
        value: set() for value in range(SIZE)
    }
    visits = Counter()
    for left, right in multiplicities:
        outgoing[left].add(right)
        incoming[right].add(left)
    for left, _right in transitions:
        visits[left] += 1
    unique_edges = len(multiplicities)
    return TransitionGraphAudit(
        len(transitions),
        unique_edges,
        len(transitions) - unique_edges,
        max(multiplicities.values()),
        max(map(len, outgoing.values())),
        max(map(len, incoming.values())),
        _effective_uniform_choices(
            tuple(visits[value] for value in range(SIZE)),
            unique_edges,
        ),
    )


def standard_action_stream(
    message: Sequence[int],
    transform: str,
) -> tuple[int, ...]:
    """Apply one fixed standard-order C83 path transform."""

    if transform == "raw":
        return tuple(message)
    if transform in ("difference-forward", "difference-backward"):
        sign = 1 if transform == "difference-forward" else -1
        return tuple(
            sign * (right - left) % SIZE
            for left, right in zip(message, message[1:])
        )
    if transform in ("accumulate-forward", "accumulate-backward"):
        sign = 1 if transform == "accumulate-forward" else -1
        value = 0
        output = []
        for symbol in message:
            value = (value + sign * symbol) % SIZE
            output.append(value)
        return tuple(output)
    raise ValueError(f"unknown action transform: {transform}")


@dataclass(frozen=True)
class ActionWidthScore:
    transform: str
    width: int
    coordinate: str
    training_excess: float
    heldout_b_excess: float
    heldout_c_excess: float


def _serial_excess(
    streams: Sequence[Sequence[int]],
    *,
    controls: int,
    rng: random.Random,
) -> float:
    observed = serial_mutual_information(streams)
    null = []
    for _ in range(controls):
        shuffled = []
        for stream in streams:
            values = list(stream)
            rng.shuffle(values)
            shuffled.append(tuple(values))
        null.append(serial_mutual_information(shuffled))
    return observed - sum(null) / len(null)


def action_width_scores(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
    *,
    controls: int,
    seed: int,
) -> tuple[ActionWidthScore, ...]:
    """Screen standard C83 path transforms and contiguous quotient widths."""

    if controls < 1:
        raise ValueError("at least one control is required")
    if streams is None:
        streams = load_cipher3()
    transforms = (
        "raw",
        "difference-forward",
        "difference-backward",
        "accumulate-forward",
        "accumulate-backward",
    )
    rows = []
    rng = random.Random(seed)
    for transform in transforms:
        transformed = {
            group: tuple(
                standard_action_stream(message, transform)
                for message in streams[group]
            )
            for group in GROUPS
        }
        for width in range(2, 43):
            for coordinate in ("quotient", "remainder"):
                projected = {
                    group: tuple(
                        tuple(
                            value // width
                            if coordinate == "quotient"
                            else value % width
                            for value in message
                        )
                        for message in transformed[group]
                    )
                    for group in GROUPS
                }
                rows.append(
                    ActionWidthScore(
                        transform,
                        width,
                        coordinate,
                        _serial_excess(
                            projected["A"],
                            controls=controls,
                            rng=rng,
                        ),
                        _serial_excess(
                            projected["B"],
                            controls=controls,
                            rng=rng,
                        ),
                        _serial_excess(
                            projected["C"],
                            controls=controls,
                            rng=rng,
                        ),
                    )
                )
    return tuple(rows)


@dataclass(frozen=True)
class WheelControlSemantics:
    emit: bool
    toggle_parity: bool
    toggle_direction: bool
    reset_accumulator: bool
    reset_anchor: bool


def wheel_control_semantics() -> tuple[WheelControlSemantics, ...]:
    return tuple(
        WheelControlSemantics(
            bool(bits & 1),
            bool(bits & 2),
            bool(bits & 4),
            bool(bits & 8),
            bool(bits & 16),
        )
        for bits in range(32)
    )


def decode_recovered_wheel(
    message: Sequence[int],
    semantics: WheelControlSemantics,
    *,
    initial_direction: int,
    initial_parity: int,
) -> tuple[int, ...]:
    """Decode accumulator coordinates under one bounded exceptional-J rule."""

    if initial_direction not in (-1, 1):
        raise ValueError("initial direction must be -1 or +1")
    if initial_parity not in (0, 1):
        raise ValueError("initial parity must be zero or one")
    previous: int | None = None
    accumulator = 0
    direction = initial_direction
    parity = initial_parity
    output = []
    for symbol in message:
        if symbol == EXCEPTIONAL_RAW:
            if semantics.emit and previous is not None:
                output.append(accumulator)
            if semantics.toggle_parity:
                parity ^= 1
            if semantics.toggle_direction:
                direction = -direction
            if semantics.reset_accumulator:
                accumulator = 0
            if semantics.reset_anchor:
                previous = None
            continue
        current = RECOVERED_WHEEL_COORDINATES[symbol]
        if previous is None:
            previous = current
            continue
        distance = (direction * (current - previous) + 42 * parity) % 82
        accumulator = (accumulator + distance) % 42
        output.append(accumulator)
        previous = current
    return tuple(output)


def render_wheel_coordinates(
    coordinates: Sequence[int],
    shift: int,
    orientation: int,
) -> str:
    if shift not in range(42) or orientation not in (-1, 1):
        raise ValueError("invalid plaintext-wheel orientation or shift")
    return "".join(
        PLAINTEXT_WHEEL[(orientation * value + shift) % 42]
        for value in coordinates
    )


TRANSLITERATION = str.maketrans(
    {
        "Ä": "A",
        "Å": "A",
        "Ö": "O",
        "'": "’",
        "\n": " ",
        "\r": " ",
        "\t": " ",
    }
)


def normalize_plaintext42(text: str) -> tuple[int, ...]:
    indices = {character: index for index, character in enumerate(PLAINTEXT_ALPHABET)}
    output = []
    in_space = True
    for character in text.upper().translate(TRANSLITERATION):
        if character in indices and character != " ":
            output.append(indices[character])
            in_space = False
        elif not in_space:
            output.append(indices[" "])
            in_space = True
    if output and output[-1] == indices[" "]:
        output.pop()
    return tuple(output)


@dataclass(frozen=True)
class TrigramModel42:
    log_probabilities: tuple[float, ...]

    @classmethod
    def train(cls, text: str) -> "TrigramModel42":
        values = normalize_plaintext42(text)
        if len(values) < 3:
            raise ValueError("training corpus is too short")
        counts = Counter(
            (42 * values[index] + values[index + 1]) * 42
            + values[index + 2]
            for index in range(len(values) - 2)
        )
        total = sum(counts.values())
        floor = math.log(0.05 / total)
        table = [floor] * (42**3)
        for code, count in counts.items():
            table[code] = math.log(count / total)
        return cls(tuple(table))

    def best_rotation(
        self,
        coordinates: Sequence[int],
        orientation: int,
    ) -> tuple[float, int, int]:
        import numpy as np

        coordinates = np.asarray(coordinates, dtype=np.int16)
        if len(coordinates) < 3:
            return 0.0, 0, 0
        wheel_to_plain, table = _numpy_trigram_model(self)
        shifts = np.arange(42, dtype=np.int16)[:, None]
        positions = (orientation * coordinates[None, :] + shifts) % 42
        values = wheel_to_plain[positions]
        codes = (
            (42 * values[:, :-2] + values[:, 1:-1]) * 42
            + values[:, 2:]
        )
        scores = table[codes].sum(axis=1)
        best_shift = int(np.argmax(scores))
        return float(scores[best_shift]), len(coordinates) - 2, best_shift


_NUMPY_TRIGRAM_CACHE: dict[int, tuple[object, object]] = {}


def _numpy_trigram_model(model: TrigramModel42) -> tuple[object, object]:
    import numpy as np

    key = id(model)
    cached = _NUMPY_TRIGRAM_CACHE.get(key)
    if cached is None:
        cached = (
            np.asarray(
                [
                    PLAINTEXT_ALPHABET.index(character)
                    for character in PLAINTEXT_WHEEL
                ],
                dtype=np.int16,
            ),
            np.asarray(model.log_probabilities),
        )
        _NUMPY_TRIGRAM_CACHE[key] = cached
    return cached


@dataclass(frozen=True)
class WheelTransferScore:
    model_name: str
    orientation: int
    initial_direction: int
    initial_parity: int
    semantics: WheelControlSemantics
    training_score_per_trigram: float
    heldout_score_per_trigram: float
    shifts: tuple[tuple[str, int], ...]


def select_wheel_transfer(
    streams: Mapping[str, Sequence[Sequence[int]]],
    models: Mapping[str, TrigramModel42],
) -> WheelTransferScore:
    """Select the complete wheel/control family on A and score B/C once."""

    best_key = None
    best_config = None
    for semantics in wheel_control_semantics():
        for initial_direction in (-1, 1):
            for initial_parity in (0, 1):
                decoded_a = tuple(
                    decode_recovered_wheel(
                        message,
                        semantics,
                        initial_direction=initial_direction,
                        initial_parity=initial_parity,
                    )
                    for message in streams["A"]
                )
                for orientation in (-1, 1):
                    for model_name, model in models.items():
                        total = windows = 0
                        shifts = []
                        for index, coordinates in enumerate(decoded_a):
                            score, count, shift = model.best_rotation(
                                coordinates,
                                orientation,
                            )
                            total += score
                            windows += count
                            shifts.append((f"A{index}", shift))
                        average = total / windows
                        key = (
                            -average,
                            model_name,
                            orientation,
                            initial_direction,
                            initial_parity,
                            semantics.emit,
                            semantics.toggle_parity,
                            semantics.toggle_direction,
                            semantics.reset_accumulator,
                            semantics.reset_anchor,
                        )
                        if best_key is None or key < best_key:
                            best_key = key
                            best_config = (
                                model_name,
                                model,
                                orientation,
                                initial_direction,
                                initial_parity,
                                semantics,
                                average,
                                shifts,
                            )
    assert best_config is not None
    (
        model_name,
        model,
        orientation,
        initial_direction,
        initial_parity,
        semantics,
        training_average,
        shifts,
    ) = best_config

    heldout_total = heldout_windows = 0
    for group in ("B", "C"):
        for index, message in enumerate(streams[group]):
            coordinates = decode_recovered_wheel(
                message,
                semantics,
                initial_direction=initial_direction,
                initial_parity=initial_parity,
            )
            score, count, shift = model.best_rotation(coordinates, orientation)
            heldout_total += score
            heldout_windows += count
            shifts.append((f"{group}{index}", shift))
    return WheelTransferScore(
        model_name,
        orientation,
        initial_direction,
        initial_parity,
        semantics,
        training_average,
        heldout_total / heldout_windows,
        tuple(shifts),
    )


def permute_nonexceptional_labels(
    streams: Mapping[str, Sequence[Sequence[int]]],
    rng: random.Random,
) -> dict[str, tuple[tuple[int, ...], ...]]:
    sources = [value for value in range(SIZE) if value != EXCEPTIONAL_RAW]
    targets = sources.copy()
    rng.shuffle(targets)
    mapping = dict(zip(sources, targets, strict=True))
    mapping[EXCEPTIONAL_RAW] = EXCEPTIONAL_RAW
    return {
        group: tuple(
            tuple(mapping[value] for value in message)
            for message in streams[group]
        )
        for group in GROUPS
    }


@dataclass(frozen=True)
class DriftScore:
    coordinate_system: str
    direction: int
    step: int
    training_unique: int
    heldout_b_unique: int
    heldout_c_unique: int
    training_events: int
    heldout_b_events: int
    heldout_c_events: int


def drift_values(
    message: Sequence[int],
    *,
    coordinate_system: str,
    direction: int,
    step: int,
) -> tuple[int, ...]:
    """Remove one fixed reset-relative linear drift from a stream."""

    if direction not in (-1, 1):
        raise ValueError("direction must be -1 or +1")
    if coordinate_system == "standard83":
        modulus = 83
        coordinate = lambda value: value
    elif coordinate_system == "recovered82":
        modulus = 82
        coordinate = RECOVERED_WHEEL_COORDINATES.get
    else:
        raise ValueError("unknown coordinate system")
    if step not in range(modulus):
        raise ValueError("step lies outside the coordinate modulus")

    output = []
    for position, symbol in enumerate(message):
        value = coordinate(symbol)
        if value is None:
            continue
        output.append((direction * value - step * position) % modulus)
    return tuple(output)


def fixed_drift_score(
    streams: Mapping[str, Sequence[Sequence[int]]],
    coordinate_system: str,
    direction: int,
    step: int,
) -> DriftScore:
    values = {
        group: tuple(
            value
            for message in streams[group]
            for value in drift_values(
                message,
                coordinate_system=coordinate_system,
                direction=direction,
                step=step,
            )
        )
        for group in GROUPS
    }
    return DriftScore(
        coordinate_system,
        direction,
        step,
        len(set(values["A"])),
        len(set(values["B"])),
        len(set(values["C"])),
        len(values["A"]),
        len(values["B"]),
        len(values["C"]),
    )


def select_fixed_drift(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> DriftScore:
    """Select a concrete coordinate drift on A without consulting B or C."""

    if streams is None:
        streams = load_cipher3()
    scores = []
    for coordinate_system, modulus in (("standard83", 83), ("recovered82", 82)):
        for direction in (-1, 1):
            for step in range(modulus):
                scores.append(
                    fixed_drift_score(
                        streams,
                        coordinate_system,
                        direction,
                        step,
                    )
                )
    return min(
        scores,
        key=lambda score: (
            score.training_unique,
            score.coordinate_system,
            score.direction,
            score.step,
        ),
    )


def initial_deck_candidates() -> tuple[tuple[str, tuple[int, ...]], ...]:
    identity = tuple(range(SIZE))
    recovered = RECOVERED_WHEEL_CARDS
    candidates = (
        ("raw-forward", identity),
        ("raw-reverse", tuple(reversed(identity))),
        ("wheel-J-first-forward", (EXCEPTIONAL_RAW,) + recovered),
        ("wheel-J-last-forward", recovered + (EXCEPTIONAL_RAW,)),
        (
            "wheel-J-first-reverse",
            (EXCEPTIONAL_RAW,) + tuple(reversed(recovered)),
        ),
        (
            "wheel-J-last-reverse",
            tuple(reversed(recovered)) + (EXCEPTIONAL_RAW,),
        ),
    )
    if any(tuple(sorted(deck)) != identity for _, deck in candidates):
        raise AssertionError("initial deck candidates must permute all 83 cards")
    return candidates


@dataclass(frozen=True)
class RecursiveTransferScore:
    initial_deck: str
    marker_mode: str
    update_timing: str
    valid: bool
    training_outside_42: int
    training_unique: int
    heldout_b_outside_42: int
    heldout_b_unique: int
    heldout_c_outside_42: int
    heldout_c_unique: int
    replay_exact: bool


def _rank_metrics(values: Sequence[int]) -> tuple[int, int]:
    return sum(value >= 42 for value in values), len(set(values))


def recursive_transfer_score(
    streams: Mapping[str, Sequence[Sequence[int]]],
    initial_name: str,
    initial_deck: Sequence[int],
    marker_mode: str,
    update_before_output: bool,
) -> RecursiveTransferScore:
    operations = tuple(
        recursive_increasing_chunk_reversal(SIZE, index)
        for index in range(SIZE)
    )
    skip = marker_mode == "body"
    decoded: dict[str, list[int]] = {group: [] for group in GROUPS}
    replay_exact = True
    try:
        for group in GROUPS:
            for message in streams[group]:
                ciphertext = tuple(message[int(skip) :])
                plaintext = decode_dynamic_substitution(
                    ciphertext,
                    operations,
                    initial_deck=initial_deck,
                    update_before_output=update_before_output,
                )
                decoded[group].extend(plaintext)
                if not update_before_output:
                    replay_exact &= (
                        encode_dynamic_substitution(
                            plaintext,
                            operations,
                            initial_deck=initial_deck,
                        )
                        == ciphertext
                    )
    except ValueError:
        return RecursiveTransferScore(
            initial_name,
            marker_mode,
            "before" if update_before_output else "after",
            False,
            10**9,
            SIZE,
            10**9,
            SIZE,
            10**9,
            SIZE,
            False,
        )

    training = _rank_metrics(decoded["A"])
    heldout_b = _rank_metrics(decoded["B"])
    heldout_c = _rank_metrics(decoded["C"])
    return RecursiveTransferScore(
        initial_name,
        marker_mode,
        "before" if update_before_output else "after",
        True,
        training[0],
        training[1],
        heldout_b[0],
        heldout_b[1],
        heldout_c[0],
        heldout_c[1],
        replay_exact,
    )


def recursive_transfer_scores(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> tuple[RecursiveTransferScore, ...]:
    if streams is None:
        streams = load_cipher3()
    return tuple(
        recursive_transfer_score(
            streams,
            name,
            deck,
            marker_mode,
            update_before_output,
        )
        for name, deck in initial_deck_candidates()
        for marker_mode in ("full", "body")
        for update_before_output in (False, True)
    )


def select_recursive_transfer(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> RecursiveTransferScore:
    return min(
        recursive_transfer_scores(streams),
        key=lambda score: (
            not score.valid,
            score.training_outside_42,
            score.training_unique,
            score.initial_deck,
            score.marker_mode,
            score.update_timing,
        ),
    )


def selected_action_table(size: int, action: str) -> tuple[tuple[int, ...], ...]:
    if action == "swap-front":
        rows = []
        for rank in range(size):
            row = list(range(size))
            row[0], row[rank] = row[rank], row[0]
            rows.append(tuple(row))
        return tuple(rows)
    if action not in ACTIONS:
        raise ValueError("unknown selected-card action")
    return tuple(
        selected_action_indices(size, action, rank)
        for rank in range(size)
    )


def decode_fixed_base_selected_action(
    ciphertext: Sequence[int],
    base: Sequence[int],
    action: str,
) -> tuple[int, ...]:
    """Decode one reset stream under ``base; emit rank; selected update``."""

    size = len(base)
    if tuple(sorted(base)) != tuple(range(size)):
        raise ValueError("base must be a permutation")
    table = selected_action_table(size, action)
    deck = list(range(size))
    output = []
    for card in ciphertext:
        deck = [deck[position] for position in base]
        rank = deck.index(card)
        output.append(rank)
        deck = [deck[position] for position in table[rank]]
    return tuple(output)


@dataclass(frozen=True)
class PhysicalTransferScore:
    base: str
    action: str
    marker_mode: str
    training_outside_42: int
    training_unique: int
    training_maximum: int
    heldout_b_outside_42: int
    heldout_b_unique: int
    heldout_b_maximum: int
    heldout_c_outside_42: int
    heldout_c_unique: int
    heldout_c_maximum: int


def _physical_metrics(
    messages: Sequence[Sequence[int]],
    base: Sequence[int],
    action: str,
    *,
    skip: int,
) -> tuple[int, int, int]:
    values = tuple(
        value
        for message in messages
        for value in decode_fixed_base_selected_action(
            message[skip:],
            base,
            action,
        )
    )
    return sum(value >= 42 for value in values), len(set(values)), max(values)


def physical_transfer_scores(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> tuple[PhysicalTransferScore, ...]:
    """Select one named base inside each action/mode using group A only."""

    import numpy as np

    if streams is None:
        streams = load_cipher3()
    candidates = [("identity", tuple(range(SIZE)))]
    seen = {candidates[0][1]}
    for name, base in standard_base_candidates(SIZE):
        if base in seen:
            continue
        seen.add(base)
        candidates.append((name, base))
    names = tuple(name for name, _ in candidates)
    bases = np.asarray([base for _, base in candidates], dtype=np.int16)
    rows = len(candidates)
    row_indices = np.arange(rows)
    results = []

    for action in ("swap-front",) + ACTIONS:
        table = np.asarray(
            selected_action_table(SIZE, action),
            dtype=np.int16,
        )
        for marker_mode, skip in (("full", 0), ("body", 1)):
            counts = np.zeros((rows, SIZE), dtype=np.int16)
            for message in streams["A"]:
                deck = np.broadcast_to(
                    np.arange(SIZE, dtype=np.int16),
                    (rows, SIZE),
                ).copy()
                for card in message[skip:]:
                    deck = np.take_along_axis(deck, bases, axis=1)
                    ranks = np.argmax(deck == card, axis=1)
                    counts[row_indices, ranks] += 1
                    deck = np.take_along_axis(deck, table[ranks], axis=1)

            outside = counts[:, 42:].sum(axis=1)
            unique = np.count_nonzero(counts, axis=1)
            maximum = np.max(
                np.where(counts > 0, np.arange(SIZE), -1),
                axis=1,
            )
            selected = min(
                range(rows),
                key=lambda row: (
                    int(outside[row]),
                    int(unique[row]),
                    int(maximum[row]),
                    names[row],
                ),
            )
            base_name, base = candidates[selected]
            heldout_b = _physical_metrics(
                streams["B"],
                base,
                action,
                skip=skip,
            )
            heldout_c = _physical_metrics(
                streams["C"],
                base,
                action,
                skip=skip,
            )
            results.append(
                PhysicalTransferScore(
                    base_name,
                    action,
                    marker_mode,
                    int(outside[selected]),
                    int(unique[selected]),
                    int(maximum[selected]),
                    *heldout_b,
                    *heldout_c,
                )
            )
    return tuple(results)


def select_physical_transfer(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> PhysicalTransferScore:
    return min(
        physical_transfer_scores(streams),
        key=lambda score: (
            score.training_outside_42,
            score.training_unique,
            score.training_maximum,
            score.action,
            score.marker_mode,
            score.base,
        ),
    )
