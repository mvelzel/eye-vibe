#!/usr/bin/env python3
"""Audit the modulo-101 checksum after merging copied body prefixes."""

import argparse
from collections import Counter

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.marker_orders import marker_lexicographic_order
from eye_mystery.prefix_hierarchy import serialize_trie_edges
from eye_mystery.trie_checksum import (
    affine_f83_relabeling_calibration,
    branch_descendant_checksums,
    random_relabeling_zero_count,
    signature_preserving_relabeling_calibration,
    signature_preserving_joint_calibration,
    trie_checksum,
    vector_rank_mod,
)


def count_vector(values: tuple[int, ...]) -> tuple[int, ...]:
    counts = Counter(values)
    return tuple(counts[value] for value in range(83))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=200_000)
    args = parser.parse_args()

    streams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    result = trie_checksum(streams, MESSAGE_ORDER, start=1)
    print("distinct body-trie edges:", result.edge_count)
    print("edge-label total:", result.total)
    print("mod 101:", result.residue)
    print("factorization: 37774 = 374 * 101")
    print("branch descendant checksums:")
    branches = branch_descendant_checksums(streams, start=1)
    for branch in branches:
        print(
            branch.cluster.members,
            "depth",
            branch.cluster.length,
            "edges",
            branch.descendant_edge_count,
            "total",
            branch.descendant_total,
            "mod101",
            branch.descendant_residue,
        )
    missing_values = tuple(range(83, 101))
    missing_residue = sum(missing_values) % 101
    print(
        "compressed structural records:",
        len(branches),
        "branch nodes +",
        len(branches) + len(MESSAGE_ORDER) - 1,
        "exits =",
        2 * len(branches) + len(MESSAGE_ORDER) - 1,
    )
    print("missing values:", missing_values, "sum mod101:", missing_residue)

    print("nearby start offsets:")
    for start in range(0, 10):
        shifted = trie_checksum(streams, MESSAGE_ORDER, start=start)
        print(start, shifted.edge_count, shifted.residue)

    reversed_bodies = {
        name: tuple(reversed(stream[1:])) for name, stream in streams.items()
    }
    raw_streams = {name: MESSAGES[name] for name in MESSAGE_ORDER}
    print(
        "suffix-trie control:",
        trie_checksum(reversed_bodies, MESSAGE_ORDER, start=0),
    )
    print(
        "raw-direction trie control:",
        trie_checksum(raw_streams, MESSAGE_ORDER, start=3),
    )

    affine = affine_f83_relabeling_calibration(result.label_multiplicities)
    print("affine F83 zero relabelings:", affine.zero_count, "/", affine.total)
    print("zero additive translations:", affine.zero_translations)
    random_zeros = random_relabeling_zero_count(
        result.label_multiplicities,
        samples=args.samples,
        seed=20_260_721,
    )
    print(
        "arbitrary relabeling zero count:",
        random_zeros,
        "/",
        args.samples,
    )

    message_vectors = tuple(
        count_vector(streams[name]) for name in MESSAGE_ORDER
    )
    print("message count-vector rank:", vector_rank_mod(message_vectors, 101))
    print(
        "rank after adding trie counts:",
        vector_rank_mod(message_vectors + (result.label_multiplicities,), 101),
    )

    diagonal_vectors = tuple(
        count_vector(streams[name]) for name in ("east1", "east3", "east5")
    )
    conditional = signature_preserving_relabeling_calibration(
        result.label_multiplicities,
        diagonal_vectors,
    )
    marker_labels = tuple(streams[name][0] for name in MESSAGE_ORDER)
    marker_fixed = signature_preserving_relabeling_calibration(
        result.label_multiplicities,
        diagonal_vectors,
        fixed_labels=marker_labels,
    )
    joint = signature_preserving_relabeling_calibration(
        result.label_multiplicities,
        diagonal_vectors,
        checksum_modulus=17 * 101,
    )
    joint_marker_fixed = signature_preserving_relabeling_calibration(
        result.label_multiplicities,
        diagonal_vectors,
        fixed_labels=marker_labels,
        checksum_modulus=17 * 101,
    )
    print(
        "exact diagonal-check-preserving zeros:",
        conditional.zero_count,
        "/",
        conditional.total,
        conditional.zero_count / conditional.total,
    )
    print(
        "same with all marker labels fixed:",
        marker_fixed.zero_count,
        "/",
        marker_fixed.total,
        marker_fixed.zero_count / marker_fixed.total,
    )
    print(
        "joint mod-17*101 zeros:",
        joint.zero_count,
        "/",
        joint.total,
        joint.zero_count / joint.total,
    )
    print(
        "same with all marker labels fixed:",
        joint_marker_fixed.zero_count,
        "/",
        joint_marker_fixed.total,
        joint_marker_fixed.zero_count / joint_marker_fixed.total,
    )
    print("joint full-trie zero / branch complement controls:")
    target_branch_residue = (-missing_residue) % 101
    for branch in branches:
        branch_joint = signature_preserving_joint_calibration(
            result.label_multiplicities,
            branch.label_multiplicities,
            diagonal_vectors,
            fixed_labels=marker_labels,
        )
        hits = branch_joint.count(0, target_branch_residue)
        print(
            branch.cluster.length,
            branch.cluster.members,
            hits,
            "/",
            branch_joint.total,
            hits / branch_joint.total,
        )

    orders = {
        "canonical": MESSAGE_ORDER,
        "east5-first trail": MESSAGE_ORDER[-1:] + MESSAGE_ORDER[:-1],
        "marker trie": marker_lexicographic_order(),
        "marker LF": (
            "east5", "west3", "west4", "east3", "east4",
            "west2", "east2", "west1", "east1",
        ),
    }
    print("17-by-54 record controls:")
    for order_name, order in orders.items():
        for breadth_first in (False, True):
            values = serialize_trie_edges(
                streams,
                order,
                start=1,
                breadth_first=breadth_first,
            )
            consecutive = tuple(
                sum(values[offset : offset + 54])
                for offset in range(0, len(values), 54)
            )
            cyclic = tuple(sum(values[lane::17]) for lane in range(17))
            print(
                order_name,
                "BFS" if breadth_first else "DFS",
                "consecutive-equal-2222",
                sum(total == 2222 for total in consecutive),
                "consecutive-zero-mod101",
                sum(total % 101 == 0 for total in consecutive),
                "cyclic-equal-2222",
                sum(total == 2222 for total in cyclic),
                "cyclic-zero-mod101",
                sum(total % 101 == 0 for total in cyclic),
            )


if __name__ == "__main__":
    main()
