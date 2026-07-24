"""Second lateral batch from the twelfth Eye-cipher novelty horizon."""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations, permutations

from eye_mystery.corpus import (
    MESSAGE_ORDER,
    MESSAGES,
    ROW_PAIR_TRIGRAM_LENGTHS,
)
from eye_mystery.deck_shuffles import interleave, josephus, mongean
from eye_mystery.factoradic_headers import (
    P_MESSAGES,
    Q_EAST_MESSAGES,
    Q_WEST_MESSAGES,
    compose,
)
from eye_mystery.ninth_causal import (
    deepest_leaf_depths,
    three_by_three_partitions,
    transition_edges,
)
from eye_mystery.twelfth_novelty import eye_bodies


NATURAL_PANEL_ROWS = (
    MESSAGE_ORDER[:3],
    MESSAGE_ORDER[3:6],
    MESSAGE_ORDER[6:],
)
HEADER_PARTITION = tuple(
    frozenset(group)
    for group in (P_MESSAGES, Q_WEST_MESSAGES, Q_EAST_MESSAGES)
)


class DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> None:
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return
        if self.rank[left] < self.rank[right]:
            left, right = right, left
        self.parent[right] = left
        if self.rank[left] == self.rank[right]:
            self.rank[left] += 1


@dataclass(frozen=True)
class LineDigraphClosure:
    hidden_states: int
    present_edges: int
    predicted_edges: int
    false_positive_edges: int
    predictions: frozenset[tuple[int, int]]


def line_digraph_closure(
    edges: Iterable[tuple[int, int]], *, alphabet_size: int = 83
) -> LineDigraphClosure:
    """Close constraints ``head(left) == tail(right)`` from visible transitions."""

    present = frozenset(edges)
    dsu = DisjointSet(2 * alphabet_size)
    for left, right in present:
        if (
            left not in range(alphabet_size)
            or right not in range(alphabet_size)
        ):
            raise ValueError("transition lies outside the visible alphabet")
        dsu.union(alphabet_size + left, right)
    roots = {dsu.find(node) for node in range(2 * alphabet_size)}
    predicted = frozenset(
        (left, right)
        for left in range(alphabet_size)
        for right in range(alphabet_size)
        if dsu.find(alphabet_size + left) == dsu.find(right)
    )
    return LineDigraphClosure(
        len(roots),
        len(present),
        len(predicted),
        len(predicted - present),
        predicted,
    )


@dataclass(frozen=True)
class LineDigraphPrediction:
    training: tuple[str, ...]
    hidden_states: int
    novel_predictions: int
    novel_truth: int
    hits: int

    @property
    def precision(self) -> float:
        return self.hits / self.novel_predictions if self.novel_predictions else 0.0

    @property
    def recall(self) -> float:
        return self.hits / self.novel_truth if self.novel_truth else 0.0

    @property
    def f1(self) -> float:
        total = self.precision + self.recall
        return 2 * self.precision * self.recall / total if total else 0.0


def line_digraph_prediction(
    bodies: Mapping[str, Sequence[int]],
    training_names: Sequence[str],
) -> LineDigraphPrediction:
    training_names = tuple(training_names)
    heldout_names = tuple(
        name for name in MESSAGE_ORDER if name not in training_names
    )
    training_edges = transition_edges(
        {name: bodies[name] for name in training_names}
    )
    heldout_edges = transition_edges(
        {name: bodies[name] for name in heldout_names}
    )
    closure = line_digraph_closure(training_edges)
    novel_predictions = closure.predictions - training_edges
    novel_truth = heldout_edges - training_edges
    hits = novel_predictions & novel_truth
    return LineDigraphPrediction(
        training_names,
        closure.hidden_states,
        len(novel_predictions),
        len(novel_truth),
        len(hits),
    )


def all_line_digraph_triples(
    bodies: Mapping[str, Sequence[int]],
) -> tuple[LineDigraphPrediction, ...]:
    return tuple(
        line_digraph_prediction(bodies, training)
        for training in combinations(MESSAGE_ORDER, 3)
    )


def cross_phase_values(message: Sequence[int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return the two base-five trigrams crossing accepted glyph boundaries."""

    if len(message) % 3:
        raise ValueError("raw eye stream must contain complete trigrams")
    glyphs = len(message) // 3
    phase_one = []
    phase_two = []
    for glyph in range(glyphs - 1):
        start = 3 * glyph
        phase_one.append(
            25 * message[start + 1] + 5 * message[start + 2] + message[start + 3]
        )
        phase_two.append(
            25 * message[start + 2] + 5 * message[start + 3] + message[start + 4]
        )
    return tuple(phase_one), tuple(phase_two)


def raw_phase_indicators(
    messages: Mapping[str, Sequence[int]],
) -> dict[str, tuple[tuple[int, ...], tuple[int, ...]]]:
    return {
        name: tuple(
            tuple(value >= 83 for value in phase)
            for phase in cross_phase_values(messages[name])
        )
        for name in MESSAGE_ORDER
    }


def raw_phase_selected_positions() -> tuple[dict[str, tuple[int, ...]], dict[str, tuple[int, ...]]]:
    marker_positions = {name: (0,) for name in MESSAGE_ORDER}
    row_positions = {}
    for name in MESSAGE_ORDER:
        cumulative = 0
        positions = []
        for length in ROW_PAIR_TRIGRAM_LENGTHS[name][:-1]:
            cumulative += length
            positions.append(cumulative - 1)
        row_positions[name] = tuple(positions)
    return marker_positions, row_positions


@dataclass(frozen=True)
class RawPhaseScore:
    totals: tuple[int, int]
    marker_hits: tuple[int, int]
    marker_positions: int
    row_hits: tuple[int, int]
    row_positions: int


def raw_phase_score(
    indicators: Mapping[str, tuple[Sequence[int], Sequence[int]]],
) -> RawPhaseScore:
    markers, rows = raw_phase_selected_positions()
    totals = []
    marker_hits = []
    row_hits = []
    for phase in range(2):
        totals.append(
            sum(sum(indicators[name][phase]) for name in MESSAGE_ORDER)
        )
        marker_hits.append(
            sum(
                indicators[name][phase][position]
                for name in MESSAGE_ORDER
                for position in markers[name]
            )
        )
        row_hits.append(
            sum(
                indicators[name][phase][position]
                for name in MESSAGE_ORDER
                for position in rows[name]
            )
        )
    return RawPhaseScore(
        tuple(totals),
        tuple(marker_hits),
        sum(map(len, markers.values())),
        tuple(row_hits),
        sum(map(len, rows.values())),
    )


def rotate_phase_indicators(
    indicators: Mapping[str, tuple[Sequence[int], Sequence[int]]],
    rng: random.Random,
) -> dict[str, tuple[tuple[int, ...], tuple[int, ...]]]:
    output = {}
    for name in MESSAGE_ORDER:
        phases = []
        for values in indicators[name]:
            values = tuple(values)
            offset = rng.randrange(len(values))
            phases.append(values[offset:] + values[:offset])
        output[name] = tuple(phases)
    return output


def shuffle_trigrams_within_row_pairs(
    messages: Mapping[str, Sequence[int]],
    rng: random.Random,
) -> dict[str, tuple[int, ...]]:
    """Shuffle accepted glyphs within each row-pair and triangle parity.

    This preserves every accepted ``0..82`` trigram, each authored row-pair
    multiset, and downward/upward triangle parity.  It breaks only which
    accepted glyphs are adjacent, making it the strict occupancy control for
    crossing phases.
    """

    output = {}
    for name in MESSAGE_ORDER:
        raw = messages[name]
        cursor = 0
        rebuilt: list[int] = []
        for length in ROW_PAIR_TRIGRAM_LENGTHS[name]:
            trigrams = [
                tuple(raw[cursor + 3 * index : cursor + 3 * index + 3])
                for index in range(length)
            ]
            cursor += 3 * length
            lanes = [
                [trigrams[index] for index in range(parity, length, 2)]
                for parity in range(2)
            ]
            for lane in lanes:
                rng.shuffle(lane)
            lane_indices = [0, 0]
            for index in range(length):
                parity = index % 2
                rebuilt.extend(lanes[parity][lane_indices[parity]])
                lane_indices[parity] += 1
        if cursor != len(raw):
            raise ValueError("row-pair lengths do not consume raw message")
        output[name] = tuple(rebuilt)
    return output


GRID_LINE_CLASSES = tuple(
    tuple(
        tuple(
            3 * y + x
            for y in range(3)
            for x in range(3)
            if selector(x, y) == line
        )
        for line in range(3)
    )
    for selector in (
        lambda x, y: y,
        lambda x, y: x,
        lambda x, y: (y - x) % 3,
        lambda x, y: (y + x) % 3,
    )
)


def panel_grid_arrangements() -> tuple[tuple[str, ...], ...]:
    """Enumerate grids preserving the three natural row memberships."""

    arrangements = []
    for row_order in permutations(NATURAL_PANEL_ROWS):
        for first in permutations(row_order[0]):
            for second in permutations(row_order[1]):
                for third in permutations(row_order[2]):
                    arrangements.append((*first, *second, *third))
    return tuple(arrangements)


def line_sum_closures(values: Sequence[int], prime: int) -> int:
    if len(values) != 9:
        raise ValueError("an affine-plane panel requires nine values")
    closures = 0
    for parallel_class in GRID_LINE_CLASSES:
        sums = tuple(
            sum(values[index] for index in line) % prime
            for line in parallel_class
        )
        closures += len(set(sums)) == 1
    return closures


@dataclass(frozen=True)
class AffinePlaneSelection:
    prime: int
    natural_training: int
    natural_heldout: int
    selected_training: int
    selected_heldout: int
    selected_grid: tuple[str, ...]


def affine_plane_selection(
    bodies: Mapping[str, Sequence[int]],
    prime: int,
    *,
    training_start: int = 25,
    training_stop: int = 61,
    heldout_stop: int = 98,
) -> AffinePlaneSelection:
    arrangements = panel_grid_arrangements()

    def score(grid: Sequence[str], start: int, stop: int) -> int:
        return sum(
            line_sum_closures(
                tuple(bodies[name][column] for name in grid), prime
            )
            for column in range(start, stop)
        )

    natural = tuple(MESSAGE_ORDER)
    natural_training = score(natural, training_start, training_stop)
    natural_heldout = score(natural, training_stop, heldout_stop)
    scored = tuple(
        (score(grid, training_start, training_stop), grid)
        for grid in arrangements
    )
    selected_training, selected_grid = max(
        scored,
        key=lambda row: (
            row[0],
            tuple(-MESSAGE_ORDER.index(name) for name in row[1]),
        ),
    )
    return AffinePlaneSelection(
        prime,
        natural_training,
        natural_heldout,
        selected_training,
        score(selected_grid, training_stop, heldout_stop),
        selected_grid,
    )


def shuffle_aligned_panel_values(
    bodies: Mapping[str, Sequence[int]], rng: random.Random
) -> dict[str, tuple[int, ...]]:
    mutable = {name: list(values) for name, values in bodies.items()}
    stop = min(len(values) for values in bodies.values())
    for column in range(stop):
        values = [mutable[name][column] for name in MESSAGE_ORDER]
        rng.shuffle(values)
        for name, value in zip(MESSAGE_ORDER, values, strict=True):
            mutable[name][column] = value
    return {name: tuple(values) for name, values in mutable.items()}


def inverse_permutation(permutation: Sequence[int]) -> tuple[int, ...]:
    output = [0] * len(permutation)
    for index, value in enumerate(permutation):
        output[value] = index
    return tuple(output)


def permutation_power(permutation: Sequence[int], exponent: int) -> tuple[int, ...]:
    if exponent < 0:
        return permutation_power(inverse_permutation(permutation), -exponent)
    value = tuple(range(len(permutation)))
    base = tuple(permutation)
    while exponent:
        if exponent & 1:
            value = compose(base, value)
        base = compose(base, base)
        exponent >>= 1
    return value


def physical_action_candidates(size: int = 83) -> tuple[tuple[str, tuple[int, ...]], ...]:
    """Build the fixed named physical-action dictionary."""

    primitives: list[tuple[str, tuple[int, ...]]] = []
    for cut in range(1, size):
        primitives.append(
            (f"cut-{cut}", tuple(range(cut, size)) + tuple(range(cut)))
        )
    primitives.append(("reverse", tuple(range(size - 1, -1, -1))))
    core = []
    for split in sorted({size // 2, (size + 1) // 2}):
        for right_first in (False, True):
            item = (
                f"interleave-{split}-{'R' if right_first else 'L'}",
                interleave(size, split, right_first=right_first),
            )
            primitives.append(item)
            core.append(item)
    for first_to_top in (False, True):
        for reverse_source in (False, True):
            item = (
                f"monge-{'T' if first_to_top else 'B'}-"
                f"{'rev' if reverse_source else 'fwd'}",
                mongean(
                    size,
                    first_to_top=first_to_top,
                    reverse_source=reverse_source,
                ),
            )
            primitives.append(item)
            core.append(item)
    for step in range(2, size):
        primitives.append((f"josephus-{step}", josephus(size, step)))
    for name, permutation in core:
        for exponent in range(2, 9):
            primitives.append(
                (f"{name}^{exponent}", permutation_power(permutation, exponent))
            )

    expanded = []
    for name, permutation in primitives:
        expanded.append((name, permutation))
        expanded.append((f"{name}^-1", inverse_permutation(permutation)))
    seen: set[tuple[int, ...]] = set()
    output = []
    for name, permutation in expanded:
        if permutation in seen:
            continue
        seen.add(permutation)
        output.append((name, permutation))
    return tuple(output)


@dataclass(frozen=True)
class PhysicalActionScore:
    candidates: int
    common_support: int
    common_action: str
    per_context_supports: tuple[int, ...]
    exact_contexts: int


def physical_action_score(
    mappings: Sequence[Mapping[int, int]],
    candidates: Sequence[tuple[str, Sequence[int]]],
) -> PhysicalActionScore:
    per_candidate = []
    per_context = [0] * len(mappings)
    exact_contexts = [False] * len(mappings)
    for name, permutation in candidates:
        supports = tuple(
            sum(permutation[source] == target for source, target in mapping.items())
            for mapping in mappings
        )
        per_candidate.append((sum(supports), name))
        for index, (support, mapping) in enumerate(
            zip(supports, mappings, strict=True)
        ):
            per_context[index] = max(per_context[index], support)
            exact_contexts[index] |= support == len(mapping)
    common_support, common_action = max(
        per_candidate, key=lambda row: (row[0], row[1])
    )
    return PhysicalActionScore(
        len(candidates),
        common_support,
        common_action,
        tuple(per_context),
        sum(exact_contexts),
    )


def shuffle_mapping_targets(
    mappings: Sequence[Mapping[int, int]], rng: random.Random
) -> tuple[dict[int, int], ...]:
    output = []
    for mapping in mappings:
        sources = tuple(sorted(mapping))
        targets = list(mapping.values())
        rng.shuffle(targets)
        output.append(dict(zip(sources, targets, strict=True)))
    return tuple(output)


@dataclass(frozen=True)
class TransducerScore:
    correct: int
    predictions: int

    @property
    def accuracy(self) -> float:
        return self.correct / self.predictions if self.predictions else 0.0


def raw_suffix_starts(
    bodies: Mapping[str, Sequence[int]] | None = None,
) -> dict[str, int]:
    if bodies is None:
        bodies = eye_bodies()
    depths = deepest_leaf_depths(bodies)
    # Three digits for the marker, three per body glyph, and one complete
    # branch-exit glyph after the deepest shared prefix.
    return {name: 3 * (depths[name] + 2) for name in MESSAGE_ORDER}


def _raw_followers(
    names: Iterable[str],
    messages: Mapping[str, Sequence[int]],
    starts: Mapping[str, int],
) -> tuple[dict[tuple[int, int], Counter[int]], Counter[int]]:
    followers: dict[tuple[int, int], Counter[int]] = {}
    totals: Counter[int] = Counter()
    for name in names:
        stream = messages[name]
        for index in range(max(2, starts[name]), len(stream)):
            context = (stream[index - 2], stream[index - 1])
            followers.setdefault(context, Counter())[stream[index]] += 1
            totals[stream[index]] += 1
    return followers, totals


def _majority(counts: Counter[int]) -> int:
    best = max(counts.values())
    return min(value for value, count in counts.items() if count == best)


def raw_transducer_partition_score(
    partition: Sequence[frozenset[str]],
    messages: Mapping[str, Sequence[int]] = MESSAGES,
    starts: Mapping[str, int] | None = None,
) -> TransducerScore:
    if starts is None:
        starts = raw_suffix_starts()
    correct = predictions = 0
    for group in partition:
        for heldout in group:
            training = tuple(name for name in group if name != heldout)
            followers, totals = _raw_followers(training, messages, starts)
            default = _majority(totals)
            stream = messages[heldout]
            for index in range(max(2, starts[heldout]), len(stream)):
                context = (stream[index - 2], stream[index - 1])
                predicted = (
                    _majority(followers[context])
                    if context in followers
                    else default
                )
                correct += predicted == stream[index]
                predictions += 1
    return TransducerScore(correct, predictions)


def raw_transducer_unconditioned_score(
    messages: Mapping[str, Sequence[int]] = MESSAGES,
    starts: Mapping[str, int] | None = None,
) -> TransducerScore:
    if starts is None:
        starts = raw_suffix_starts()
    correct = predictions = 0
    for heldout in MESSAGE_ORDER:
        followers, totals = _raw_followers(
            (name for name in MESSAGE_ORDER if name != heldout),
            messages,
            starts,
        )
        default = _majority(totals)
        stream = messages[heldout]
        for index in range(max(2, starts[heldout]), len(stream)):
            context = (stream[index - 2], stream[index - 1])
            predicted = (
                _majority(followers[context])
                if context in followers
                else default
            )
            correct += predicted == stream[index]
            predictions += 1
    return TransducerScore(correct, predictions)


def all_transducer_partition_scores(
    messages: Mapping[str, Sequence[int]] = MESSAGES,
) -> tuple[tuple[tuple[frozenset[str], ...], TransducerScore], ...]:
    starts = raw_suffix_starts()
    return tuple(
        (
            partition,
            raw_transducer_partition_score(
                partition, messages=messages, starts=starts
            ),
        )
        for partition in three_by_three_partitions(MESSAGE_ORDER)
    )
