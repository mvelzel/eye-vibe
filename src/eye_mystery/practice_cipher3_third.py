"""Wide conformance-vector screens for sdlwdr practice cipher 3."""

from __future__ import annotations

import math
import random
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.practice_cipher3_wide import GROUPS, SIZE, load_cipher3


NamedStreams = tuple[tuple[str, tuple[int, ...]], ...]


def named_streams(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
    *,
    body: bool,
) -> NamedStreams:
    """Return the eighteen streams with stable A0..C5 names."""

    if streams is None:
        streams = load_cipher3()
    return tuple(
        (
            f"{group}{index}",
            tuple(message[1:] if body else message),
        )
        for group in GROUPS
        for index, message in enumerate(streams[group])
    )


@dataclass(frozen=True)
class FactorMatch:
    left: str
    right: str
    left_start: int
    right_start: int
    length: int
    orientation: int
    multiplier: int
    offset: int


def _known_literal_branch(match: FactorMatch) -> bool:
    """Identify every disclosed literal branch in the A prefix tree."""

    if match.orientation != 1 or match.multiplier != 1 or match.offset != 0:
        return False
    if match.left_start != match.right_start or match.left_start < 1:
        return False
    pair = {match.left, match.right}
    if pair == {"A4", "A5"}:
        branch_end = 44
    elif pair in ({"A0", "A4"}, {"A0", "A5"}):
        branch_end = 9
    elif pair == {"A1", "A3"}:
        branch_end = 4
    else:
        return False
    return match.left_start + match.length <= branch_end


def _affine_run(
    left: Sequence[int],
    right: Sequence[int],
    left_start: int,
    right_start: int,
) -> tuple[int, int, int]:
    """Return maximal run and its unique affine map over F83.

    Cipher 3 has no adjacent doubles, so the first two source and target
    values determine a nonzero affine map whenever two symbols remain.
    """

    available = min(len(left) - left_start, len(right) - right_start)
    if available < 2:
        return available, 1, (
            right[right_start] - left[left_start]
        ) % SIZE
    left_delta = (left[left_start + 1] - left[left_start]) % SIZE
    right_delta = (right[right_start + 1] - right[right_start]) % SIZE
    if left_delta == 0:
        raise ValueError("adjacent source double prevents a unique affine map")
    multiplier = right_delta * pow(left_delta, -1, SIZE) % SIZE
    offset = (
        right[right_start] - multiplier * left[left_start]
    ) % SIZE
    length = 2
    while (
        length < available
        and (
            multiplier * left[left_start + length] + offset
        )
        % SIZE
        == right[right_start + length]
    ):
        length += 1
    return length, multiplier, offset


def affine_factor_inventory(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
    *,
    body: bool = False,
    minimum_length: int = 4,
    exclude_known_branch: bool = True,
) -> tuple[FactorMatch, ...]:
    """Enumerate maximal pairwise affine-related factors over F83."""

    if minimum_length < 2:
        raise ValueError("affine factors need at least two values")
    named = named_streams(streams, body=body)
    matches: list[FactorMatch] = []
    for left_index, (left_name, left) in enumerate(named):
        for right_name, raw_right in named[left_index + 1 :]:
            for orientation in (1, -1):
                right = raw_right if orientation == 1 else raw_right[::-1]
                for left_start in range(len(left) - minimum_length + 1):
                    for right_start in range(len(right) - minimum_length + 1):
                        length, multiplier, offset = _affine_run(
                            left,
                            right,
                            left_start,
                            right_start,
                        )
                        if length < minimum_length:
                            continue
                        # Retain only the left-maximal occurrence for this map.
                        if left_start and right_start:
                            if (
                                multiplier * left[left_start - 1] + offset
                            ) % SIZE == right[right_start - 1]:
                                continue
                        match = FactorMatch(
                            left_name,
                            right_name,
                            left_start,
                            right_start,
                            length,
                            orientation,
                            multiplier,
                            offset,
                        )
                        if exclude_known_branch and _known_literal_branch(match):
                            continue
                        matches.append(match)
    return tuple(
        sorted(
            matches,
            key=lambda match: (
                -match.length,
                match.left,
                match.right,
                match.orientation,
                match.left_start,
                match.right_start,
                match.multiplier,
                match.offset,
            ),
        )
    )


def _isomorphic_run(
    left: Sequence[int],
    right: Sequence[int],
    left_start: int,
    right_start: int,
) -> int:
    left_to_right: dict[int, int] = {}
    right_to_left: dict[int, int] = {}
    length = 0
    available = min(len(left) - left_start, len(right) - right_start)
    while length < available:
        left_value = left[left_start + length]
        right_value = right[right_start + length]
        mapped_right = left_to_right.get(left_value)
        mapped_left = right_to_left.get(right_value)
        if mapped_right is not None and mapped_right != right_value:
            break
        if mapped_left is not None and mapped_left != left_value:
            break
        left_to_right[left_value] = right_value
        right_to_left[right_value] = left_value
        length += 1
    return length


def longest_isomorphic_factor(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
    *,
    body: bool = False,
    exclude_known_branch: bool = True,
) -> FactorMatch:
    """Find the longest cross-stream equality-pattern isomorph."""

    named = named_streams(streams, body=body)
    best: FactorMatch | None = None
    for left_index, (left_name, left) in enumerate(named):
        for right_name, raw_right in named[left_index + 1 :]:
            for orientation in (1, -1):
                right = raw_right if orientation == 1 else raw_right[::-1]
                for left_start in range(len(left)):
                    for right_start in range(len(right)):
                        upper = min(
                            len(left) - left_start,
                            len(right) - right_start,
                        )
                        if best is not None and upper <= best.length:
                            continue
                        length = _isomorphic_run(
                            left,
                            right,
                            left_start,
                            right_start,
                        )
                        match = FactorMatch(
                            left_name,
                            right_name,
                            left_start,
                            right_start,
                            length,
                            orientation,
                            -1,
                            -1,
                        )
                        if (
                            exclude_known_branch
                            and {left_name, right_name} == {"A4", "A5"}
                            and orientation == 1
                            and left_start == right_start
                            and left_start + length <= 45
                        ):
                            continue
                        if best is None or (
                            -length,
                            left_name,
                            right_name,
                            orientation,
                            left_start,
                            right_start,
                        ) < (
                            -best.length,
                            best.left,
                            best.right,
                            best.orientation,
                            best.left_start,
                            best.right_start,
                        ):
                            best = match
    if best is None:
        raise ValueError("at least two nonempty streams are required")
    return best


@dataclass(frozen=True)
class IsomorphicEvidence:
    match: FactorMatch
    distinct_values: int
    repeated_constraints: int


def strongest_isomorphic_evidence(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> IsomorphicEvidence:
    """Maximize actual repeat constraints, excluding the disclosed A tree."""

    named = named_streams(streams, body=False)
    best: IsomorphicEvidence | None = None
    for left_index, (left_name, left) in enumerate(named):
        for right_name, raw_right in named[left_index + 1 :]:
            for orientation in (1, -1):
                right = raw_right if orientation == 1 else raw_right[::-1]
                for left_start in range(len(left)):
                    for right_start in range(len(right)):
                        length = _isomorphic_run(
                            left,
                            right,
                            left_start,
                            right_start,
                        )
                        pair = {left_name, right_name}
                        known = (
                            orientation == 1
                            and left_start == right_start
                            and (
                                (
                                    pair == {"A4", "A5"}
                                    and left_start + length <= 45
                                )
                                or (
                                    pair
                                    in ({"A0", "A4"}, {"A0", "A5"})
                                    and left_start >= 1
                                    and left_start + length <= 9
                                )
                                or (
                                    pair == {"A1", "A3"}
                                    and left_start >= 1
                                    and left_start + length <= 4
                                )
                            )
                        )
                        if known:
                            continue
                        distinct = len(
                            set(left[left_start : left_start + length])
                        )
                        evidence = IsomorphicEvidence(
                            FactorMatch(
                                left_name,
                                right_name,
                                left_start,
                                right_start,
                                length,
                                orientation,
                                -1,
                                -1,
                            ),
                            distinct,
                            length - distinct,
                        )
                        if best is None or (
                            -evidence.repeated_constraints,
                            -evidence.match.length,
                            evidence.match.left,
                            evidence.match.right,
                            evidence.match.orientation,
                            evidence.match.left_start,
                            evidence.match.right_start,
                        ) < (
                            -best.repeated_constraints,
                            -best.match.length,
                            best.match.left,
                            best.match.right,
                            best.match.orientation,
                            best.match.left_start,
                            best.match.right_start,
                        ):
                            best = evidence
    if best is None:
        raise ValueError("at least two nonempty streams are required")
    return best


def recurrence_residuals(
    messages: Sequence[Sequence[int]],
    coefficients: Sequence[int],
    *,
    body: bool,
) -> tuple[int, ...]:
    """Return residuals after a homogeneous recurrence over F83."""

    order = len(coefficients)
    if order not in (1, 2):
        raise ValueError("only order-one and order-two screens are frozen")
    residuals: list[int] = []
    for raw_message in messages:
        message = tuple(raw_message[1:] if body else raw_message)
        for index in range(order, len(message)):
            prediction = sum(
                coefficient * message[index - lag - 1]
                for lag, coefficient in enumerate(coefficients)
            )
            residuals.append((message[index] - prediction) % SIZE)
    return tuple(residuals)


@dataclass(frozen=True)
class RecurrenceScreen:
    order: int
    body: bool
    coefficients: tuple[int, ...]
    training_support: int
    validation_support: int
    heldout_support: int
    complete_support: int


def select_recurrence(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
    *,
    order: int,
    body: bool,
) -> RecurrenceScreen:
    """Select minimum residual support on A and transfer to B/C."""

    if streams is None:
        streams = load_cipher3()
    if order == 1:
        candidates = ((a,) for a in range(SIZE))
    elif order == 2:
        candidates = (
            (a, b)
            for a in range(SIZE)
            for b in range(SIZE)
        )
    else:
        raise ValueError("only order one or two is supported")
    selected = min(
        candidates,
        key=lambda coefficients: (
            len(
                set(
                    recurrence_residuals(
                        streams["A"],
                        coefficients,
                        body=body,
                    )
                )
            ),
            coefficients,
        ),
    )
    supports = {
        group: len(
            set(
                recurrence_residuals(
                    streams[group],
                    selected,
                    body=body,
                )
            )
        )
        for group in GROUPS
    }
    complete = len(
        set(
            value
            for group in GROUPS
            for value in recurrence_residuals(
                streams[group],
                selected,
                body=body,
            )
        )
    )
    return RecurrenceScreen(
        order,
        body,
        selected,
        supports["A"],
        supports["B"],
        supports["C"],
        complete,
    )


def berlekamp_massey_complexity(sequence: Sequence[int]) -> int:
    """Return linear complexity over the prime field F83."""

    if not sequence:
        return 0
    connection = [1] + [0] * len(sequence)
    previous = [1] + [0] * len(sequence)
    complexity = 0
    shift = 1
    previous_discrepancy = 1
    for index in range(len(sequence)):
        discrepancy = sequence[index] % SIZE
        for lag in range(1, complexity + 1):
            discrepancy = (
                discrepancy + connection[lag] * sequence[index - lag]
            ) % SIZE
        if discrepancy == 0:
            shift += 1
            continue
        old_connection = connection.copy()
        factor = discrepancy * pow(previous_discrepancy, -1, SIZE) % SIZE
        for position in range(shift, len(connection)):
            connection[position] = (
                connection[position] - factor * previous[position - shift]
            ) % SIZE
        if 2 * complexity <= index:
            complexity = index + 1 - complexity
            previous = old_connection
            previous_discrepancy = discrepancy
            shift = 1
        else:
            shift += 1
    return complexity


def move_to_front_decode(ranks: Sequence[int]) -> tuple[int, ...]:
    """Decode raw values as zero-based MTF ranks with a reset 83-item list."""

    deck = list(range(SIZE))
    decoded: list[int] = []
    for rank in ranks:
        if not 0 <= rank < len(deck):
            raise ValueError("MTF rank outside current alphabet")
        value = deck.pop(rank)
        decoded.append(value)
        deck.insert(0, value)
    return tuple(decoded)


def inverse_bwt(last_column: Sequence[int], primary_index: int) -> tuple[int, ...]:
    """Invert one BWT last column with stable token ordering."""

    length = len(last_column)
    if not 0 <= primary_index < length:
        raise ValueError("primary index outside BWT body")
    occurrence: Counter[int] = Counter()
    tagged_last: list[tuple[int, int]] = []
    for value in last_column:
        tagged_last.append((value, occurrence[value]))
        occurrence[value] += 1
    tagged_first = sorted(tagged_last)
    first_positions = {
        token: index for index, token in enumerate(tagged_first)
    }
    lf = tuple(first_positions[token] for token in tagged_last)
    row = primary_index
    output: list[int] = []
    for _ in range(length):
        output.append(last_column[row])
        row = lf[row]
    output.reverse()
    return tuple(output)


def lz78_phrase_count(sequence: Sequence[int]) -> int:
    """Return a label-invariant LZ78 phrase count."""

    dictionary: set[tuple[int, ...]] = set()
    current: tuple[int, ...] = ()
    phrases = 0
    for value in sequence:
        candidate = current + (value,)
        if candidate in dictionary:
            current = candidate
            continue
        dictionary.add(candidate)
        phrases += 1
        current = ()
    if current:
        phrases += 1
    return phrases


@dataclass(frozen=True)
class CompressionAudit:
    events: int
    entropy_bits: float
    adjacent_doubles: int
    direct_lz78_phrases: int
    inverse_bwt_valid_messages: int
    inverse_bwt_lz78_phrases: int
    mtf_decoded_unique: int
    mtf_message_maximum_unique: int


def compression_audit(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> CompressionAudit:
    """Audit direct MTF/BWT signatures under the first-symbol-header reading."""

    if streams is None:
        streams = load_cipher3()
    messages = [
        tuple(message)
        for group in GROUPS
        for message in streams[group]
    ]
    bodies = [message[1:] for message in messages]
    counts = Counter(value for body in bodies for value in body)
    events = sum(counts.values())
    entropy = -sum(
        count / events * math.log2(count / events)
        for count in counts.values()
    )
    doubles = sum(
        left == right
        for body in bodies
        for left, right in zip(body, body[1:])
    )
    direct_phrases = sum(lz78_phrase_count(body) for body in bodies)
    inverse_bwt_bodies = [
        inverse_bwt(body, message[0])
        for message, body in zip(messages, bodies, strict=True)
        if message[0] < len(body)
    ]
    inverse_phrases = sum(
        lz78_phrase_count(body) for body in inverse_bwt_bodies
    )
    mtf_messages = [move_to_front_decode(body) for body in bodies]
    return CompressionAudit(
        events,
        entropy,
        doubles,
        direct_phrases,
        len(inverse_bwt_bodies),
        inverse_phrases,
        len(set(value for message in mtf_messages for value in message)),
        max(len(set(message)) for message in mtf_messages),
    )


@dataclass(frozen=True)
class ShuffleCompressionControl:
    direct_lz78_phrases: tuple[int, ...]
    inverse_bwt_lz78_phrases: tuple[int, ...]


def compression_shuffle_controls(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
    *,
    controls: int,
    seed: int,
) -> ShuffleCompressionControl:
    """Preserve every header/body multiset while shuffling body order."""

    if controls < 1:
        raise ValueError("at least one control is required")
    if streams is None:
        streams = load_cipher3()
    messages = [
        tuple(message)
        for group in GROUPS
        for message in streams[group]
    ]
    rng = random.Random(seed)
    direct_scores: list[int] = []
    inverse_scores: list[int] = []
    for _ in range(controls):
        shuffled_bodies: list[tuple[int, ...]] = []
        for message in messages:
            body = list(message[1:])
            rng.shuffle(body)
            shuffled_bodies.append(tuple(body))
        direct_scores.append(
            sum(lz78_phrase_count(body) for body in shuffled_bodies)
        )
        inverse_scores.append(
            sum(
                lz78_phrase_count(inverse_bwt(body, message[0]))
                for message, body in zip(
                    messages,
                    shuffled_bodies,
                    strict=True,
                )
                if message[0] < len(body)
            )
        )
    return ShuffleCompressionControl(
        tuple(direct_scores),
        tuple(inverse_scores),
    )
