#!/usr/bin/env python3
"""Calibrate the BEXIT branch-depth plus outgoing-label identity."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import permutations
from math import factorial
from random import Random

import numpy as np

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.metadata_instruction import (
    branch_exit_records,
    corrected_exit_residues,
)
from eye_mystery.prefix_hierarchy import serialize_trie_edges
from eye_mystery.trie_checksum import vector_rank_mod


def count_vector(values: tuple[int, ...]) -> tuple[int, ...]:
    counts = Counter(values)
    return tuple(counts[value] for value in range(83))


def signature_groups(
    constraints: tuple[tuple[int, ...], ...], fixed_labels: set[int]
) -> tuple[tuple[int, ...], ...]:
    classes: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for label in range(83):
        classes[tuple(vector[label] for vector in constraints)].append(label)
    groups = []
    for labels in classes.values():
        groups.extend((label,) for label in labels if label in fixed_labels)
        free = tuple(label for label in labels if label not in fixed_labels)
        if free:
            groups.append(free)
    return tuple(groups)


def coefficient_vectors(records) -> tuple[tuple[int, ...], ...]:
    vectors = []
    for record in records:
        labels = set(record.exit_labels)
        vectors.append(tuple(int(label in labels) for label in range(83)))
    return (
        tuple(vectors[0][label] - vectors[1][label] for label in range(83)),
        vectors[2],
        tuple(vectors[3][label] - vectors[4][label] for label in range(83)),
    )


def exact_subgroup_distribution(
    coefficients: tuple[tuple[int, ...], ...],
    groups: tuple[tuple[int, ...], ...],
) -> tuple[np.ndarray, tuple[int, int, int], int]:
    """Use cyclic FFT convolution for the three modulo-101 linear forms."""
    spectrum = np.ones((101, 101, 101), dtype=np.complex128)
    fixed = [0, 0, 0]
    expected_total = 1
    for labels in groups:
        if len(labels) == 1:
            label = labels[0]
            for index, vector in enumerate(coefficients):
                fixed[index] = (
                    fixed[index] + vector[label] * label
                ) % 101
            continue
        local = np.zeros((101, 101, 101), dtype=np.float64)
        for replacement in permutations(labels):
            residues = tuple(
                sum(
                    vector[label] * value
                    for label, value in zip(labels, replacement, strict=True)
                )
                % 101
                for vector in coefficients
            )
            local[residues] += 1
        spectrum *= np.fft.fftn(local)
        expected_total *= factorial(len(labels))
    raw = np.fft.ifftn(spectrum).real
    rounded = np.rint(raw).astype(np.int64)
    if float(np.max(np.abs(raw - rounded))) >= 0.001:
        raise ArithmeticError("FFT convolution did not round cleanly")
    if int(rounded.sum()) != expected_total:
        raise ArithmeticError("FFT convolution lost subgroup assignments")
    return rounded, tuple(fixed), expected_total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempts", type=int, default=500_000)
    parser.add_argument("--seed", type=int, default=20260721)
    args = parser.parse_args()

    full_streams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    trail_order = MESSAGE_ORDER[-1:] + MESSAGE_ORDER[:-1]
    bodies = {name: full_streams[name][1:] for name in trail_order}
    records = branch_exit_records(bodies)
    depths = tuple(record.depth for record in records)
    print(f"depths / A1Z26             {depths} / {''.join(chr(64 + x) for x in depths)}")
    print(f"exit labels                 {tuple(record.exit_labels for record in records)}")
    print(f"exit sums                   {tuple(sum(record.exit_labels) for record in records)}")
    print(f"depth-corrected mod101      {corrected_exit_residues(records)}")

    diagonal = tuple(
        count_vector(full_streams[name]) for name in ("east1", "east3", "east5")
    )
    fixed_labels = {full_streams[name][0] for name in MESSAGE_ORDER}
    groups = signature_groups(diagonal, fixed_labels)
    coefficients = coefficient_vectors(records)
    distribution, fixed, total = exact_subgroup_distribution(coefficients, groups)

    coefficient_counts = []
    for depth_coefficient in range(101):
        target = (
            depth_coefficient * (depths[1] - depths[0]) % 101,
            -depth_coefficient * depths[2] % 101,
            depth_coefficient * (depths[4] - depths[3]) % 101,
        )
        adjusted = tuple((target[index] - fixed[index]) % 101 for index in range(3))
        coefficient_counts.append(int(distribution[adjusted]))
    nonzero = tuple(
        (coefficient, count)
        for coefficient, count in enumerate(coefficient_counts)
        if count
    )
    print(f"exact protected subgroup     {total}")
    print(f"nonzero depth coefficients  {nonzero}")
    print(f"exact selected rate         {coefficient_counts[1] / total:.12f}")

    trie_values = serialize_trie_edges(
        full_streams,
        MESSAGE_ORDER,
        start=1,
        breadth_first=False,
    )
    trie_counts = count_vector(trie_values)
    protected_vectors = diagonal + (trie_counts,)
    print(
        "linear ranks base/with exits "
        f"{vector_rank_mod(protected_vectors, 101)}/"
        f"{vector_rank_mod(protected_vectors + coefficients, 101)}"
    )
    target = (3, 77, 11)
    randomizer = Random(args.seed)
    mapping = list(range(83))
    accepted = 0
    hits = 0
    for _ in range(args.attempts):
        for labels in groups:
            if len(labels) > 1:
                replacements = list(labels)
                randomizer.shuffle(replacements)
                for label, replacement in zip(labels, replacements, strict=True):
                    mapping[label] = replacement
        if sum(trie_counts[label] * mapping[label] for label in range(83)) % 101:
            continue
        accepted += 1
        residues = tuple(
            sum(vector[label] * mapping[label] for label in range(83)) % 101
            for vector in coefficients
        )
        hits += residues == target
    print(f"full-trie accepted/attempted {accepted}/{args.attempts}")
    print(f"joint identity hits         {hits}")
    print(f"conditional corrected rate  {(hits + 1) / (accepted + 1):.12f}")


if __name__ == "__main__":
    main()
