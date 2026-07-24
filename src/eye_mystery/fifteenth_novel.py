"""Frozen first-batch probes for the fifteenth wide novelty horizon."""

from __future__ import annotations

import random
import zlib
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations, combinations_with_replacement, permutations
from math import log2

from eye_mystery.factoradic_headers import inverse, lexicographic_unrank
from eye_mystery.fourteenth_selector import base5_digits, global_relabel
from eye_mystery.hidden_geometry import (
    FIRST_FAMILY_NAMES,
    LAST_FAMILY_NAMES,
    chord_constraints,
    context_sequences,
)
from eye_mystery.practice_cipher4_routes import PatternModel


BitCode = tuple[int, ...]
TreeShape = tuple[BitCode, ...]
COMPONENT_ORDERS = tuple(permutations(range(3)))
MULTISETS = tuple(combinations_with_replacement(range(5), 3))
MULTISET_INDEX = {value: index for index, value in enumerate(MULTISETS)}


def ordered_prefix_shapes(leaves: int = 6) -> tuple[TreeShape, ...]:
    """Enumerate the Catalan ordered full-binary-tree leaf codes."""

    if leaves < 1:
        raise ValueError("a prefix tree needs at least one leaf")
    if leaves == 1:
        return (((),),)
    shapes = []
    for left_leaves in range(1, leaves):
        right_leaves = leaves - left_leaves
        for left in ordered_prefix_shapes(left_leaves):
            for right in ordered_prefix_shapes(right_leaves):
                shapes.append(
                    tuple((0, *code) for code in left)
                    + tuple((1, *code) for code in right)
                )
    return tuple(shapes)


PREFIX_SHAPES = ordered_prefix_shapes()


@dataclass(frozen=True, order=True)
class PackingSpec:
    width: int
    offset: int
    least_significant_first: bool

    @property
    def name(self) -> str:
        endian = "lsb" if self.least_significant_first else "msb"
        return f"w{self.width}:o{self.offset}:{endian}"


def packing_specs() -> tuple[PackingSpec, ...]:
    return tuple(
        PackingSpec(width, offset, least_significant_first)
        for width in (7, 8)
        for offset in range(width)
        for least_significant_first in (False, True)
    )


@dataclass(frozen=True, order=True)
class PrefixCodeSpec:
    shape_index: int
    route: str

    @property
    def name(self) -> str:
        return f"shape{self.shape_index}:{self.route}"


def prefix_code_specs() -> tuple[PrefixCodeSpec, ...]:
    return tuple(
        PrefixCodeSpec(shape_index, route)
        for shape_index in range(len(PREFIX_SHAPES))
        for route in ("header", "inverse")
    )


def _leaf_order(header: int, route: str) -> tuple[int, ...]:
    order = lexicographic_unrank(header)
    if route == "header":
        return order
    if route == "inverse":
        return inverse(order)
    raise ValueError(f"unknown prefix-code route: {route}")


def prefix_bits(
    tape: Sequence[int],
    header: int,
    spec: PrefixCodeSpec,
) -> tuple[int, ...]:
    if spec.shape_index not in range(len(PREFIX_SHAPES)):
        raise ValueError("prefix-code shape index is outside the catalog")
    if any(symbol not in range(6) for symbol in tape):
        raise ValueError("renderer tape symbols must lie in 0..5")
    shape = PREFIX_SHAPES[spec.shape_index]
    order = _leaf_order(header, spec.route)
    code_for_symbol = {
        symbol: shape[index] for index, symbol in enumerate(order)
    }
    return tuple(bit for symbol in tape for bit in code_for_symbol[symbol])


def pack_complete_bits(
    bits: Sequence[int],
    packing: PackingSpec,
) -> tuple[int, ...]:
    if packing.width not in (7, 8):
        raise ValueError("only frozen 7- and 8-bit packing is supported")
    if packing.offset not in range(packing.width):
        raise ValueError("packing offset lies outside one word")
    output = []
    for start in range(
        packing.offset,
        len(bits) - packing.width + 1,
        packing.width,
    ):
        chunk = tuple(bits[start : start + packing.width])
        if any(bit not in (0, 1) for bit in chunk):
            raise ValueError("bit stream contains a value outside 0/1")
        if packing.least_significant_first:
            chunk = tuple(reversed(chunk))
        value = 0
        for bit in chunk:
            value = 2 * value + bit
        output.append(value)
    return tuple(output)


def normalized_ascii(text: str) -> bytes:
    output = bytearray()
    in_space = True
    for character in text.upper():
        if "A" <= character <= "Z":
            output.append(ord(character))
            in_space = False
        elif not in_space:
            output.append(32)
            in_space = True
    return bytes(output)


@dataclass(frozen=True)
class ByteNgramModel:
    order: int
    scores: dict[tuple[int, ...], float]
    floor: float

    @classmethod
    def train(cls, data: bytes, *, order: int = 4) -> "ByteNgramModel":
        if len(data) < order:
            raise ValueError("byte corpus is shorter than the n-gram order")
        counts = Counter(
            tuple(data[index : index + order])
            for index in range(len(data) - order + 1)
        )
        total = sum(counts.values())
        return cls(
            order,
            {
                gram: log2(count / total)
                for gram, count in counts.items()
            },
            log2(0.05 / total),
        )

    def score(self, streams: Sequence[Sequence[int]]) -> float:
        total = 0.0
        grams = 0
        for stream in streams:
            for index in range(len(stream) - self.order + 1):
                gram = tuple(stream[index : index + self.order])
                total += self.scores.get(gram, self.floor)
                grams += 1
        return total / grams if grams else float("-inf")


@dataclass(frozen=True)
class PrefixCodeCandidate:
    spec: PrefixCodeSpec
    packing: PackingSpec
    train_score: float
    heldout_score: float


def _prefix_score(
    tapes: Mapping[str, Sequence[int]],
    headers: Mapping[str, int],
    names: Sequence[str],
    spec: PrefixCodeSpec,
    packing: PackingSpec,
    model: ByteNgramModel,
) -> float:
    return model.score(
        tuple(
            pack_complete_bits(
                prefix_bits(tapes[name], headers[name], spec),
                packing,
            )
            for name in names
        )
    )


def select_prefix_code(
    tapes: Mapping[str, Sequence[int]],
    headers: Mapping[str, int],
    model: ByteNgramModel,
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
    packings: Sequence[PackingSpec],
) -> PrefixCodeCandidate:
    catalog = tuple(prefix_code_specs())
    packing_catalog = tuple(packings)
    if not packing_catalog:
        raise ValueError("at least one packing convention is required")
    selected_spec, selected_packing = min(
        (
            (spec, packing)
            for spec in catalog
            for packing in packing_catalog
        ),
        key=lambda item: (
            -_prefix_score(
                tapes,
                headers,
                train_names,
                item[0],
                item[1],
                model,
            ),
            item[0],
            item[1],
        ),
    )
    return PrefixCodeCandidate(
        selected_spec,
        selected_packing,
        _prefix_score(
            tapes,
            headers,
            train_names,
            selected_spec,
            selected_packing,
            model,
        ),
        _prefix_score(
            tapes,
            headers,
            heldout_names,
            selected_spec,
            selected_packing,
            model,
        ),
    )


def symbols_from_plain_bits(
    bits: Sequence[int],
    header: int,
    spec: PrefixCodeSpec,
    *,
    maximum_symbols: int,
) -> tuple[int, ...]:
    """Parse plaintext bits with one tree and emit its renderer symbols."""

    if maximum_symbols < 1:
        raise ValueError("maximum_symbols must be positive")
    shape = PREFIX_SHAPES[spec.shape_index]
    order = _leaf_order(header, spec.route)
    leaf_for_code = {
        code: order[index] for index, code in enumerate(shape)
    }
    prefixes = {
        code[:length]
        for code in shape
        for length in range(1, len(code))
    }
    output = []
    current: tuple[int, ...] = ()
    for bit in bits:
        if bit not in (0, 1):
            raise ValueError("plaintext bit stream contains a non-bit")
        current = (*current, bit)
        if current in leaf_for_code:
            output.append(leaf_for_code[current])
            current = ()
            if len(output) == maximum_symbols:
                break
        elif current not in prefixes:
            raise AssertionError("full prefix tree rejected a bit prefix")
    if len(output) != maximum_symbols:
        raise ValueError("plaintext bit stream is too short for the fixture")
    return tuple(output)


def bytes_to_bits(data: bytes) -> tuple[int, ...]:
    return tuple(
        (byte >> shift) & 1
        for byte in data
        for shift in reversed(range(8))
    )


@dataclass(frozen=True)
class PrefixCodeAudit:
    selected: PrefixCodeCandidate
    exact_exceedances: int
    exact_controls: int
    exact_upper_tail: float
    null_minimum: float
    null_mean: float
    null_maximum: float


def permute_renderer_tapes(
    tapes: Mapping[str, Sequence[int]],
    eye_mapping: Sequence[int],
) -> dict[str, tuple[int, ...]]:
    if sorted(eye_mapping) != list(range(5)):
        raise ValueError("eye mapping must permute 0..4")
    return {
        name: tuple(
            eye_mapping[symbol] if symbol < 5 else symbol
            for symbol in tape
        )
        for name, tape in tapes.items()
    }


def audit_prefix_code(
    tapes: Mapping[str, Sequence[int]],
    headers: Mapping[str, int],
    model: ByteNgramModel,
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
    packing: PackingSpec,
) -> PrefixCodeAudit:
    """Enumerate the exact 120 global eye-direction controls."""

    selected = select_prefix_code(
        tapes,
        headers,
        model,
        train_names=train_names,
        heldout_names=heldout_names,
        packings=(packing,),
    )
    null = []
    for mapping in permutations(range(5)):
        control = permute_renderer_tapes(tapes, mapping)
        null.append(
            select_prefix_code(
                control,
                headers,
                model,
                train_names=train_names,
                heldout_names=heldout_names,
                packings=(packing,),
            ).heldout_score
        )
    exceedances = sum(value >= selected.heldout_score for value in null)
    return PrefixCodeAudit(
        selected,
        exceedances,
        len(null),
        exceedances / len(null),
        min(null),
        sum(null) / len(null),
        max(null),
    )


def multiset_order(value: int) -> tuple[int, int]:
    digits = base5_digits(value)
    multiset = tuple(sorted(digits))
    arrangements = tuple(sorted(set(permutations(multiset))))
    return MULTISET_INDEX[multiset], arrangements.index(digits)


def multiset_stream(values: Sequence[int]) -> tuple[int, ...]:
    return tuple(multiset_order(value)[0] for value in values)


def order_stream(values: Sequence[int]) -> tuple[int, ...]:
    return tuple(multiset_order(value)[1] for value in values)


@dataclass(frozen=True)
class OrderTapeScore:
    compressed_bytes: int
    runs: int


def order_tape_score(
    streams: Mapping[str, Sequence[int]],
    names: Sequence[str],
) -> OrderTapeScore:
    data = bytearray()
    runs = 0
    for message_index, name in enumerate(names):
        values = order_stream(streams[name])
        if message_index:
            data.append(255)
        data.extend(values)
        runs += sum(
            index == 0 or value != values[index - 1]
            for index, value in enumerate(values)
        )
    return OrderTapeScore(len(zlib.compress(bytes(data), level=9)), runs)


@dataclass(frozen=True)
class MultisetAudit:
    train_score: float
    heldout_score: float
    train_exceedances: int
    heldout_exceedances: int
    controls: int
    corrected_train_tail: float
    corrected_heldout_tail: float
    order_score: OrderTapeScore
    order_exceedances: int
    corrected_order_tail: float


def audit_multiset_projection(
    streams: Mapping[str, Sequence[int]],
    model: PatternModel,
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
    controls: int,
    seed: int,
) -> MultisetAudit:
    if controls < 1:
        raise ValueError("at least one multiset control is required")
    train_score = model.score(
        tuple(multiset_stream(streams[name]) for name in train_names)
    )
    heldout_score = model.score(
        tuple(multiset_stream(streams[name]) for name in heldout_names)
    )
    all_names = (*train_names, *heldout_names)
    observed_order = order_tape_score(streams, all_names)
    train_exceedances = heldout_exceedances = order_exceedances = 0
    generator = random.Random(seed)
    for _ in range(controls):
        labels = list(range(83))
        generator.shuffle(labels)
        control = global_relabel(streams, labels)
        control_train = model.score(
            tuple(multiset_stream(control[name]) for name in train_names)
        )
        control_heldout = model.score(
            tuple(multiset_stream(control[name]) for name in heldout_names)
        )
        control_order = order_tape_score(control, all_names)
        train_exceedances += control_train >= train_score
        heldout_exceedances += control_heldout >= heldout_score
        order_exceedances += (
            control_order.compressed_bytes,
            control_order.runs,
        ) <= (
            observed_order.compressed_bytes,
            observed_order.runs,
        )
    denominator = controls + 1
    return MultisetAudit(
        train_score,
        heldout_score,
        train_exceedances,
        heldout_exceedances,
        controls,
        (train_exceedances + 1) / denominator,
        (heldout_exceedances + 1) / denominator,
        observed_order,
        order_exceedances,
        (order_exceedances + 1) / denominator,
    )


def lcp_depth(
    left: int,
    right: int,
    order: Sequence[int],
) -> int:
    if sorted(order) != list(range(3)):
        raise ValueError("component order must permute 0..2")
    left_digits = base5_digits(left)
    right_digits = base5_digits(right)
    depth = 0
    for component in order:
        if left_digits[component] != right_digits[component]:
            break
        depth += 1
    return depth


@dataclass(frozen=True)
class TreeContradiction:
    context: str
    source_pair: tuple[int, int]
    target_pair: tuple[int, int]
    source_depth: int
    target_depth: int


@dataclass(frozen=True)
class TreeIsometryScore:
    order: tuple[int, ...]
    agreements: int
    comparisons: int
    contradiction: TreeContradiction | None

    @property
    def exact(self) -> bool:
        return self.agreements == self.comparisons


def tree_isometry_score(
    contexts: Sequence[tuple[str, Sequence[int], Sequence[int]]],
    order: Sequence[int],
) -> TreeIsometryScore:
    selected_order = tuple(order)
    agreements = comparisons = 0
    first_contradiction = None
    for context, source, target in contexts:
        mapping = {}
        for left, right in zip(source, target, strict=True):
            if left in mapping and mapping[left] != right:
                raise ValueError("context is not a partial function")
            mapping[left] = right
        if len(set(mapping.values())) != len(mapping):
            raise ValueError("context map is not injective")
        for left, right in combinations(sorted(mapping), 2):
            source_depth = lcp_depth(left, right, selected_order)
            target_depth = lcp_depth(
                mapping[left],
                mapping[right],
                selected_order,
            )
            comparisons += 1
            agreements += source_depth == target_depth
            if source_depth != target_depth and first_contradiction is None:
                first_contradiction = TreeContradiction(
                    context,
                    (left, right),
                    (mapping[left], mapping[right]),
                    source_depth,
                    target_depth,
                )
    return TreeIsometryScore(
        selected_order,
        agreements,
        comparisons,
        first_contradiction,
    )


@dataclass(frozen=True)
class TreeIsometryAudit:
    selected_order: tuple[int, ...]
    train: TreeIsometryScore
    heldout: TreeIsometryScore


def audit_tree_isometry(
    contexts: Sequence[tuple[str, Sequence[int], Sequence[int]]],
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
) -> TreeIsometryAudit:
    train_set = frozenset(train_names)
    heldout_set = frozenset(heldout_names)
    train_contexts = tuple(row for row in contexts if row[0] in train_set)
    heldout_contexts = tuple(row for row in contexts if row[0] in heldout_set)
    if {row[0] for row in train_contexts} != train_set:
        raise ValueError("training context selection is incomplete")
    if {row[0] for row in heldout_contexts} != heldout_set:
        raise ValueError("held-out context selection is incomplete")
    train_scores = tuple(
        tree_isometry_score(train_contexts, order)
        for order in COMPONENT_ORDERS
    )
    selected = min(
        train_scores,
        key=lambda score: (-score.agreements, score.order),
    )
    return TreeIsometryAudit(
        selected.order,
        selected,
        tree_isometry_score(heldout_contexts, selected.order),
    )


@dataclass(frozen=True, order=True)
class GraySpec:
    axis_order: tuple[int, ...]
    reflection_mask: int
    metric: str

    @property
    def name(self) -> str:
        axes = "".join(map(str, self.axis_order))
        return f"axes{axes}:r{self.reflection_mask:03b}:{self.metric}"


def reflected_gray_words(
    dimensions: int = 3,
    radix: int = 5,
) -> tuple[tuple[int, ...], ...]:
    if dimensions < 1 or radix < 2:
        raise ValueError("Gray dimensions/radix are outside the frozen family")
    words: tuple[tuple[int, ...], ...] = ((),)
    for _ in range(dimensions):
        next_words = []
        for digit in range(radix):
            suffixes = words if digit % 2 == 0 else tuple(reversed(words))
            next_words.extend((digit, *suffix) for suffix in suffixes)
        words = tuple(next_words)
    return words


GRAY_WORDS = reflected_gray_words()
GRAY_INDEX = {word: index for index, word in enumerate(GRAY_WORDS)}


def gray_specs() -> tuple[GraySpec, ...]:
    return tuple(
        GraySpec(tuple(order), reflection_mask, metric)
        for order in COMPONENT_ORDERS
        for reflection_mask in range(8)
        for metric in ("linear", "circular")
    )


def gray_position(value: int, spec: GraySpec) -> int:
    digits = base5_digits(value)
    transformed = tuple(
        4 - digits[component]
        if spec.reflection_mask & (1 << output_index)
        else digits[component]
        for output_index, component in enumerate(spec.axis_order)
    )
    return GRAY_INDEX[transformed]


def gray_distance(left: int, right: int, spec: GraySpec) -> int:
    difference = abs(gray_position(left, spec) - gray_position(right, spec))
    if spec.metric == "linear":
        return difference
    if spec.metric == "circular":
        return min(difference, 125 - difference)
    raise ValueError(f"unknown Gray metric: {spec.metric}")


@dataclass(frozen=True)
class GrayContradiction:
    context: str
    index: int
    source_edge: tuple[int, int]
    target_edge: tuple[int, int]
    source_distance: int
    target_distance: int


@dataclass(frozen=True)
class GrayScore:
    spec: GraySpec
    agreements: int
    comparisons: int
    contradiction: GrayContradiction | None

    @property
    def exact(self) -> bool:
        return self.agreements == self.comparisons


def gray_score(
    constraints,
    spec: GraySpec,
) -> GrayScore:
    agreements = 0
    first_contradiction = None
    materialized = tuple(constraints)
    for constraint in materialized:
        source_distance = gray_distance(
            constraint.source_left,
            constraint.source_right,
            spec,
        )
        target_distance = gray_distance(
            constraint.target_left,
            constraint.target_right,
            spec,
        )
        agreements += source_distance == target_distance
        if source_distance != target_distance and first_contradiction is None:
            first_contradiction = GrayContradiction(
                constraint.context,
                constraint.index,
                (constraint.source_left, constraint.source_right),
                (constraint.target_left, constraint.target_right),
                source_distance,
                target_distance,
            )
    return GrayScore(
        spec,
        agreements,
        len(materialized),
        first_contradiction,
    )


@dataclass(frozen=True)
class GrayAudit:
    selected: GraySpec
    train: GrayScore
    heldout: GrayScore


def audit_gray_geometry(
    *,
    train_names: Sequence[str],
    heldout_names: Sequence[str],
) -> GrayAudit:
    train_constraints = chord_constraints(names=train_names)
    heldout_constraints = chord_constraints(names=heldout_names)
    train_scores = tuple(
        gray_score(train_constraints, spec) for spec in gray_specs()
    )
    selected = min(
        train_scores,
        key=lambda score: (-score.agreements, score.spec),
    )
    return GrayAudit(
        selected.spec,
        selected,
        gray_score(heldout_constraints, selected.spec),
    )


def default_tree_isometry_audit() -> TreeIsometryAudit:
    return audit_tree_isometry(
        context_sequences(),
        train_names=tuple(sorted(FIRST_FAMILY_NAMES)),
        heldout_names=tuple(sorted(LAST_FAMILY_NAMES)),
    )


def default_gray_audit() -> GrayAudit:
    return audit_gray_geometry(
        train_names=tuple(sorted(FIRST_FAMILY_NAMES)),
        heldout_names=tuple(sorted(LAST_FAMILY_NAMES)),
    )
