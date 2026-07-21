#!/usr/bin/env python3
"""Audit the modulo-101 checksum after merging copied body prefixes."""

import argparse
from collections import Counter

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.trie_checksum import (
    affine_f83_relabeling_calibration,
    branch_descendant_checksums,
    random_relabeling_zero_count,
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
    for branch in branch_descendant_checksums(streams, start=1):
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


if __name__ == "__main__":
    main()
