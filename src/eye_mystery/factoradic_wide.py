"""Breadth-first body probes selected by the six-symbol header structure."""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import (
    P_MESSAGES,
    compose,
    generated_group,
    header_ranks,
    inverse,
    lexicographic_unrank,
    right_coset,
)
from eye_mystery.storage_serialization import storage_stream


IDENTITY = tuple(range(6))
PERMUTATIONS = tuple(lexicographic_unrank(rank) for rank in range(math.factorial(6)))
PERMUTATION_RANK = {permutation: rank for rank, permutation in enumerate(PERMUTATIONS)}


def canonical_streams() -> dict[str, tuple[int, ...]]:
    return {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}


def mapped_bodies(
    streams: Mapping[str, Sequence[int]], mapping: Sequence[int]
) -> dict[str, tuple[int, ...]]:
    """Relabel bodies globally while preserving the independently fixed headers."""

    if sorted(mapping) != list(range(83)):
        raise ValueError("body mapping must permute ranks 0..82")
    return {
        name: tuple(mapping[value] for value in stream[1:])
        for name, stream in streams.items()
    }


def fold_product(values: Sequence[int], *, act_left: bool) -> tuple[int, ...]:
    state = IDENTITY
    for value in values:
        permutation = PERMUTATIONS[value]
        state = compose(permutation, state) if act_left else compose(state, permutation)
    return state


def product_header_score(bodies: Mapping[str, Sequence[int]]) -> int:
    """Best global product convention matching identity/header/inverse-header."""

    headers = header_ranks()
    scores = []
    for act_left in (False, True):
        products = {
            name: fold_product(bodies[name], act_left=act_left)
            for name in MESSAGE_ORDER
        }
        for target in ("identity", "header", "inverse-header"):
            matches = 0
            for name in MESSAGE_ORDER:
                header = PERMUTATIONS[headers[name]]
                expected = (
                    IDENTITY
                    if target == "identity"
                    else header
                    if target == "header"
                    else inverse(header)
                )
                matches += products[name] == expected
            scores.append(matches)
    return max(scores)


def quotient(left: tuple[int, ...], right: tuple[int, ...], route: int) -> tuple[int, ...]:
    """Return one of the four inverse/left-right adjacent quotient conventions."""

    result = (
        compose(inverse(left), right)
        if route % 2 == 0
        else compose(right, inverse(left))
    )
    return inverse(result) if route >= 2 else result


@dataclass(frozen=True)
class QuotientScore:
    minimum_distinct: int
    maximum_visible: int
    maximum_in_p_group: int
    transitions: int


def quotient_score(bodies: Mapping[str, Sequence[int]]) -> QuotientScore:
    headers = header_ranks()
    p_group = generated_group(PERMUTATIONS[headers[name]] for name in P_MESSAGES)
    rows = []
    for route in range(4):
        values = []
        for name in MESSAGE_ORDER:
            permutations = tuple(PERMUTATIONS[value] for value in bodies[name])
            values.extend(
                quotient(left, right, route)
                for left, right in zip(permutations, permutations[1:])
            )
        rows.append(
            (
                len(set(values)),
                sum(PERMUTATION_RANK[value] <= 82 for value in values),
                sum(value in p_group for value in values),
                len(values),
            )
        )
    return QuotientScore(
        minimum_distinct=min(row[0] for row in rows),
        maximum_visible=max(row[1] for row in rows),
        maximum_in_p_group=max(row[2] for row in rows),
        transitions=rows[0][3],
    )


def running_state_score(bodies: Mapping[str, Sequence[int]]) -> int:
    """Smallest summed number of visited S6 states in a declared route family."""

    headers = header_ranks()
    totals = []
    for act_left in (False, True):
        for invert_tokens in (False, True):
            for invert_header in (False, True):
                total = 0
                for name in MESSAGE_ORDER:
                    state = PERMUTATIONS[headers[name]]
                    if invert_header:
                        state = inverse(state)
                    visited = {state}
                    for value in bodies[name]:
                        token = PERMUTATIONS[value]
                        if invert_tokens:
                            token = inverse(token)
                        state = (
                            compose(token, state)
                            if act_left
                            else compose(state, token)
                        )
                        visited.add(state)
                    total += len(visited)
                totals.append(total)
    return min(totals)


@dataclass(frozen=True)
class DelimiterScore:
    direction: str
    rows: int
    empty_rows: int
    rows_at_least_15: int
    maximum_row: int
    payload_modulo_three: tuple[int, ...]


def _split_rows(tape: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    rows = []
    current = []
    for symbol in tape:
        if symbol == 5:
            rows.append(tuple(current))
            current = []
        else:
            current.append(symbol)
    if current:
        rows.append(tuple(current))
    return tuple(rows)


def moving_delimiter_scores() -> tuple[DelimiterScore, ...]:
    """Apply each Q/P header to the actual visual tape, including row breaks."""

    headers = header_ranks()
    results = []
    for direction in ("forward", "inverse"):
        transformed_by_name = {}
        for name in MESSAGE_ORDER:
            operation = PERMUTATIONS[headers[name]]
            if direction == "inverse":
                operation = inverse(operation)
            transformed_by_name[name] = tuple(
                operation[symbol] for symbol in storage_stream(name)
            )
        rows = tuple(
            row
            for name in MESSAGE_ORDER
            for row in _split_rows(transformed_by_name[name])
        )
        results.append(
            DelimiterScore(
                direction=direction,
                rows=len(rows),
                empty_rows=sum(not row for row in rows),
                rows_at_least_15=sum(len(row) >= 15 for row in rows),
                maximum_row=max(map(len, rows)),
                payload_modulo_three=tuple(
                    sum(symbol != 5 for symbol in transformed_by_name[name]) % 3
                    for name in MESSAGE_ORDER
                ),
            )
        )
    return tuple(results)


@dataclass(frozen=True)
class CosetScore:
    maximum_header_matches: int
    maximum_self_transitions: int
    transitions: int


def coset_score(bodies: Mapping[str, Sequence[int]]) -> CosetScore:
    headers = header_ranks()
    p_group = generated_group(PERMUTATIONS[headers[name]] for name in P_MESSAGES)
    rows = []
    for side in ("right", "left"):
        def coset(permutation: tuple[int, ...]) -> frozenset[tuple[int, ...]]:
            if side == "right":
                return right_coset(permutation, p_group)
            return frozenset(compose(permutation, element) for element in p_group)

        matches = self_transitions = transitions = 0
        for name in MESSAGE_ORDER:
            header_coset = coset(PERMUTATIONS[headers[name]])
            body_cosets = tuple(coset(PERMUTATIONS[value]) for value in bodies[name])
            matches += sum(value == header_coset for value in body_cosets)
            self_transitions += sum(
                left == right for left, right in zip(body_cosets, body_cosets[1:])
            )
            transitions += max(0, len(body_cosets) - 1)
        rows.append((matches, self_transitions, transitions))
    return CosetScore(
        maximum_header_matches=max(row[0] for row in rows),
        maximum_self_transitions=max(row[1] for row in rows),
        transitions=rows[0][2],
    )


def cycle_type(permutation: tuple[int, ...]) -> tuple[int, ...]:
    seen = set()
    lengths = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        value = start
        length = 0
        while value not in seen:
            seen.add(value)
            value = permutation[value]
            length += 1
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def mutual_information(pairs: Sequence[tuple[object, object]]) -> float:
    if not pairs:
        return 0.0
    joint = Counter(pairs)
    left = Counter(value[0] for value in pairs)
    right = Counter(value[1] for value in pairs)
    total = len(pairs)
    return sum(
        count / total
        * math.log2(count * total / (left[first] * right[second]))
        for (first, second), count in joint.items()
    )


def maximum_cycle_type_mi(bodies: Mapping[str, Sequence[int]]) -> float:
    """Select absolute and adjacent-quotient cycle-type transition channels."""

    channels = []
    absolute_pairs = []
    for name in MESSAGE_ORDER:
        types = tuple(cycle_type(PERMUTATIONS[value]) for value in bodies[name])
        absolute_pairs.extend(zip(types, types[1:]))
    channels.append(mutual_information(absolute_pairs))
    for route in range(4):
        quotient_pairs = []
        for name in MESSAGE_ORDER:
            permutations = tuple(PERMUTATIONS[value] for value in bodies[name])
            types = tuple(
                cycle_type(quotient(left, right, route))
                for left, right in zip(permutations, permutations[1:])
            )
            quotient_pairs.extend(zip(types, types[1:]))
        channels.append(mutual_information(quotient_pairs))
    return max(channels)


@dataclass(frozen=True)
class WideScores:
    product_header_matches: int
    quotients: QuotientScore
    running_state_distinct: int
    cosets: CosetScore
    cycle_type_mi: float


def wide_scores(
    streams: Mapping[str, Sequence[int]], mapping: Sequence[int]
) -> WideScores:
    bodies = mapped_bodies(streams, mapping)
    return WideScores(
        product_header_matches=product_header_score(bodies),
        quotients=quotient_score(bodies),
        running_state_distinct=running_state_score(bodies),
        cosets=coset_score(bodies),
        cycle_type_mi=maximum_cycle_type_mi(bodies),
    )
