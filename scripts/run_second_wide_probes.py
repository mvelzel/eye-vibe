#!/usr/bin/env python3
"""Run unrelated cheap tests from the second breadth-first architecture map."""

from __future__ import annotations

import argparse
from random import Random

from eye_mystery.corpus import (
    MESSAGE_ORDER,
    MESSAGES,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)
from eye_mystery.initials import perfect_successor_rotation
from eye_mystery.language_null import prefix_tree_parity_shuffle
from eye_mystery.marker_orders import MARKER_TRIE_ORDER
from eye_mystery.metrics import entropy, index_of_coincidence
from eye_mystery.practice_sdlwdr import PLAINTEXT_ALPHABET
from eye_mystery.prefix_hierarchy import serialize_trie_edges
from eye_mystery.wide_complements import (
    best_header_feature_rule,
    best_tape_dependence,
    context_determinism,
    exclusion_ranks,
    reflection_quotient,
    rolling_reflection_quotient,
)


def upper_tail(observed: float, null: list[float]) -> str:
    hits = sum(value >= observed for value in null)
    return f"{hits + 1}/{len(null) + 1} = {(hits + 1)/(len(null) + 1):.6f}"


def flattened(streams: dict[str, tuple[int, ...]]) -> tuple[int, ...]:
    return tuple(value for name in MESSAGE_ORDER for value in streams[name])


def relabel_streams(
    streams: dict[str, tuple[int, ...]], labels: list[int]
) -> dict[str, tuple[int, ...]]:
    return {
        name: tuple(labels[value] for value in stream)
        for name, stream in streams.items()
    }


def maximum_reflection_ioc(streams: dict[str, tuple[int, ...]]) -> tuple[float, int]:
    best = (-1.0, 0)
    for center in range(83):
        values = tuple(
            value
            for name in MESSAGE_ORDER
            for value in reflection_quotient(streams[name], center)
        )
        candidate = index_of_coincidence(values, 42), center
        if candidate > best:
            best = candidate
    return best


def marker_center_ioc(
    streams: dict[str, tuple[int, ...]], bodies: dict[str, tuple[int, ...]]
) -> float:
    values = tuple(
        value
        for name in MESSAGE_ORDER
        for value in reflection_quotient(bodies[name], streams[name][0])
    )
    return index_of_coincidence(values, 42)


def rolling_ioc(streams: dict[str, tuple[int, ...]]) -> float:
    values = tuple(
        value
        for name in MESSAGE_ORDER
        for value in rolling_reflection_quotient(streams[name])
    )
    return index_of_coincidence(values, 41)


def exclusion_summary(streams: dict[str, tuple[int, ...]]) -> tuple[float, float, float]:
    ranks = tuple(
        rank
        for name in MESSAGE_ORDER
        for rank in exclusion_ranks(streams[name])
    )
    adjacent_classes = tuple(rank // 2 for rank in ranks)
    half_classes = tuple(rank % 41 for rank in ranks)
    high_bits = tuple(rank // 41 for rank in ranks)
    return (
        index_of_coincidence(adjacent_classes, 41),
        index_of_coincidence(half_classes, 41),
        sum(high_bits) / len(high_bits),
    )


def render(values: tuple[int, ...]) -> str:
    return "".join(PLAINTEXT_ALPHABET[value] for value in values)


def residue_matrix_summary(
    values: tuple[int, ...], rows: int, columns: int, modulus: int = 101
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if len(values) != rows * columns:
        raise ValueError("matrix dimensions do not consume the stream")
    matrix = tuple(
        values[row * columns : (row + 1) * columns] for row in range(rows)
    )
    row_residues = tuple(sum(row) % modulus for row in matrix)
    column_residues = tuple(
        sum(matrix[row][column] for row in range(rows)) % modulus
        for column in range(columns)
    )
    return row_residues, column_residues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260721)
    parser.add_argument("--relabel-trials", type=int, default=200)
    parser.add_argument("--context-trials", type=int, default=500)
    parser.add_argument("--header-trials", type=int, default=1000)
    args = parser.parse_args()

    streams = {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}
    bodies = {name: stream[1:] for name, stream in streams.items()}
    rng = Random(args.seed)

    print("exact complement arithmetic:")
    print("  raw cube / visible / unused:", 5**3, 83, 5**3 - 83)
    print("  reflection orbits on Z83:", len(set(reflection_quotient(range(83), 0))))
    print("  body length / factorization: 1027 = 13*79")
    trie_edges = serialize_trie_edges(
        bodies, MARKER_TRIE_ORDER, start=0, breadth_first=False
    )
    trie_bfs_edges = serialize_trie_edges(
        bodies, MARKER_TRIE_ORDER, start=0, breadth_first=True
    )
    trail = perfect_successor_rotation()
    assert trail is not None
    factored_body_streams = {
        "canonical-13x79": flattened(bodies),
        "marker-trie-13x79": tuple(
            value for message in MARKER_TRIE_ORDER for value in bodies[message]
        ),
        "marker-trail-13x79": tuple(
            value for message in trail for value in bodies[message]
        ),
    }
    print("  merged edges / factorization:", len(trie_edges), "= 34*27 = 9*102")

    global_ioc, best_center = maximum_reflection_ioc(bodies)
    header_ioc = marker_center_ioc(streams, bodies)
    previous_ioc = rolling_ioc(streams)
    print("reflection quotient:")
    print("  best global-center normalized IoC:", global_ioc, "center", best_center)
    print("  per-message marker-center normalized IoC:", header_ioc)
    print("  rolling previous-center normalized IoC:", previous_ioc)
    preview = reflection_quotient(bodies["east1"], best_center)[:100]
    print("  direct natural-42 preview:", render(preview))

    rank_adjacent_ioc, rank_half_ioc, high_bit_rate = exclusion_summary(streams)
    print("no-repeat enumerative ranks:")
    print("  rank//2 normalized IoC:", rank_adjacent_ioc)
    print("  rank%41 normalized IoC:", rank_half_ioc)
    print("  rank//41 one-rate:", high_bit_rate)

    global_null: list[float] = []
    header_null: list[float] = []
    previous_null: list[float] = []
    rank_null: list[float] = []
    tape_null: list[float] = []
    trie_factor_null: list[float] = []
    body_factor_null: list[float] = []
    tape_observed = best_tape_dependence(tuple(bodies.values()))
    for _ in range(args.relabel_trials):
        labels = list(range(83))
        rng.shuffle(labels)
        relabeled_streams = relabel_streams(streams, labels)
        relabeled_bodies = {name: values[1:] for name, values in relabeled_streams.items()}
        global_null.append(maximum_reflection_ioc(relabeled_bodies)[0])
        header_null.append(marker_center_ioc(relabeled_streams, relabeled_bodies))
        previous_null.append(rolling_ioc(relabeled_streams))
        rank_null.append(max(exclusion_summary(relabeled_streams)[:2]))
        tape_null.append(
            best_tape_dependence(tuple(relabeled_bodies.values())).information
        )
        relabeled_trie_layouts = (
            tuple(labels[value] for value in trie_edges),
            tuple(labels[value] for value in trie_bfs_edges),
        )
        trie_factor_null.append(
            max(
                sum(residues.count(0) for residues in residue_matrix_summary(values, 34, 27))
                for values in relabeled_trie_layouts
            )
        )
        body_factor_null.append(
            max(
                sum(
                    residues.count(0)
                    for residues in residue_matrix_summary(
                        tuple(labels[value] for value in values), 13, 79
                    )
                )
                for values in factored_body_streams.values()
            )
        )
    print("  global-center relabel upper tail:", upper_tail(global_ioc, global_null))
    print("  marker-center relabel upper tail:", upper_tail(header_ioc, header_null))
    print("  rolling-center relabel upper tail:", upper_tail(previous_ioc, previous_null))
    print(
        "  best exclusion-class relabel upper tail:",
        upper_tail(max(rank_adjacent_ioc, rank_half_ioc), rank_null),
    )
    print("delayed three-tape dependence:")
    print("  observed:", tape_observed)
    print(
        "  global-relabel upper tail:",
        upper_tail(tape_observed.information, tape_null),
    )

    print("arbitrary short-context next-symbol rules:")
    observed_contexts = {
        order: context_determinism(tuple(bodies.values()), order)
        for order in range(1, 5)
    }
    context_null = {order: [] for order in observed_contexts}
    for _ in range(args.context_trials):
        shuffled = prefix_tree_parity_shuffle(bodies, bodies, rng, start=0)
        for order in observed_contexts:
            context_null[order].append(
                context_determinism(tuple(shuffled.values()), order).accuracy
            )
    for order, observed in observed_contexts.items():
        print(
            " ",
            observed,
            "upper tail",
            upper_tail(observed.accuracy, context_null[order]),
        )

    features = {
        name: {
            "total_length": len(streams[name]),
            "body_length": len(bodies[name]),
            "row_pairs": len(ROW_PAIR_TRIGRAM_LENGTHS[name]),
            "complete_rows": len(ROW_PAIR_TRIGRAM_LENGTHS[name]) - 1,
            "tail_length": ROW_PAIR_TRIGRAM_LENGTHS[name][-1],
            "visual_rows": 2 * len(ROW_PAIR_TRIGRAM_LENGTHS[name]),
        }
        for name in MESSAGE_ORDER
    }
    header_observed = best_header_feature_rule(streams, features)
    header_feature_null = []
    marker_values = [streams[name][0] for name in MESSAGE_ORDER]
    for _ in range(args.header_trials):
        rng.shuffle(marker_values)
        reassigned = {
            name: (marker_values[index],) + bodies[name]
            for index, name in enumerate(MESSAGE_ORDER)
        }
        header_feature_null.append(
            best_header_feature_rule(reassigned, features).matches
        )
    print("header-versus-shape signed-offset rules:")
    print("  observed:", header_observed)
    print(
        "  marker-permutation upper tail:",
        upper_tail(header_observed.matches, header_feature_null),
    )

    print("post-hoc factored record layouts (row-zero/column-zero counts mod 101):")
    traversals = {
        "trie-dfs-34x27": trie_edges,
        "trie-bfs-34x27": trie_bfs_edges,
    }
    trie_factor_observed = 0
    for name, values in traversals.items():
        row_residues, column_residues = residue_matrix_summary(values, 34, 27)
        trie_factor_observed = max(
            trie_factor_observed,
            row_residues.count(0) + column_residues.count(0),
        )
        print(name, row_residues.count(0), column_residues.count(0))
    print("  34x27 relabel upper tail:", upper_tail(trie_factor_observed, trie_factor_null))
    body_factor_observed = 0
    for name, values in factored_body_streams.items():
        row_residues, column_residues = residue_matrix_summary(values, 13, 79)
        body_factor_observed = max(
            body_factor_observed,
            row_residues.count(0) + column_residues.count(0),
        )
        print(name, row_residues.count(0), column_residues.count(0))
    print("  13x79 relabel upper tail:", upper_tail(body_factor_observed, body_factor_null))

    merged = tuple(trie_edges)
    raw = flattened(bodies)
    print("residual distribution after merging copied prefixes once:")
    print(
        "  raw / merged length, entropy, normalized IoC:",
        (len(raw), entropy(raw), index_of_coincidence(raw, 83)),
        (len(merged), entropy(merged), index_of_coincidence(merged, 83)),
    )


if __name__ == "__main__":
    main()
