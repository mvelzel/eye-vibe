#!/usr/bin/env python3
"""Run the frozen A-F probes in the sixth wide Eye expansion."""

from __future__ import annotations

import argparse
import random
from functools import cache
from statistics import median

import numpy as np

from eye_mystery.corpus import (
    MESSAGES,
    MESSAGE_ORDER,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)
from eye_mystery.sixth_wide import (
    best_missing_completion,
    best_polynomial_header_rule,
    cancel_direction_word,
    column_collision_score,
    column_label_mutual_information,
    erase_neutral_word,
    literal_affine_context_fit,
    word_inventory,
)
from test_affine_isomorph_embedding import (
    first_three_contexts,
    last_family_contexts,
)


def complete_rows(
    streams: dict[str, tuple[int, ...]],
    *,
    skip_first: bool = False,
) -> tuple[tuple[int, ...], ...]:
    rows = []
    for name in MESSAGE_ORDER:
        cursor = 0
        for row_index, length in enumerate(ROW_PAIR_TRIGRAM_LENGTHS[name]):
            row = streams[name][cursor : cursor + length]
            cursor += length
            if length == 26 and not (skip_first and row_index == 0):
                rows.append(row)
    return tuple(dict.fromkeys(rows))


def complete_rows_by_message(
    streams: dict[str, tuple[int, ...]],
    *,
    skip_first: bool,
) -> dict[str, tuple[tuple[int, ...], ...]]:
    output = {}
    for name in MESSAGE_ORDER:
        rows = []
        cursor = 0
        for row_index, length in enumerate(ROW_PAIR_TRIGRAM_LENGTHS[name]):
            row = streams[name][cursor : cursor + length]
            cursor += length
            if length == 26 and not (skip_first and row_index == 0):
                rows.append(row)
        output[name] = tuple(dict.fromkeys(rows))
    return output


PREFIX_FAMILIES = (
    ("east1", "west1", "east2"),
    ("west2", "east3", "west3"),
    ("east4", "west4", "east5"),
)


def family_heldout_score(
    rows: dict[str, tuple[tuple[int, ...], ...]],
) -> tuple[int, tuple[int, ...]]:
    scores = []
    for family in PREFIX_FAMILIES:
        family_set = set(family)
        training = tuple(
            row
            for name in MESSAGE_ORDER
            if name not in family_set
            for row in rows[name]
        )
        held_out = tuple(row for name in family for row in rows[name])
        scores.append(column_collision_score(training, held_out))
    return sum(scores), tuple(scores)


@cache
def powers(base_count: int, length: int) -> np.ndarray:
    output = np.ones((base_count, length), dtype=np.int64)
    bases = np.arange(base_count, dtype=np.int64)
    for position in range(1, length):
        output[:, position] = output[:, position - 1] * bases % base_count
    return output


def polynomial_score_numpy(
    streams: tuple[np.ndarray, ...], mapping: np.ndarray
) -> int:
    best = 0
    for modulus in (83, 101):
        for reverse in (False, True):
            global_matches = np.zeros((2, modulus), dtype=np.int16)
            root_matches = 0
            for stream in streams:
                header = int(mapping[int(stream[0])])
                body = mapping[stream[1:]]
                if reverse:
                    body = body[::-1]
                table = powers(modulus, len(body))
                hashes = table @ body % modulus
                global_matches[0] += (header - hashes) % modulus == 0
                global_matches[1] += (header + hashes) % modulus == 0
                root_matches += hashes[header % modulus] == 0
            best = max(best, int(global_matches.max()), root_matches)
    return best


def completion_score_numpy(
    left: np.ndarray,
    right: np.ndarray,
    mapping: np.ndarray,
) -> int:
    mapped_left = mapping[left]
    mapped_right = mapping[right]
    left_digits = np.column_stack(
        (mapped_left // 25, mapped_left // 5 % 5, mapped_left % 5)
    )
    right_digits = np.column_stack(
        (mapped_right // 25, mapped_right // 5 % 5, mapped_right % 5)
    )
    best = 0
    for constant in range(5):
        result = (constant - left_digits - right_digits) % 5
        for order in (
            (0, 1, 2),
            (0, 2, 1),
            (1, 0, 2),
            (1, 2, 0),
            (2, 0, 1),
            (2, 1, 0),
        ):
            values = 25 * result[:, order[0]] + 5 * result[:, order[1]] + result[:, order[2]]
            best = max(best, int(np.count_nonzero(values >= 83)))
    return best


def rotate_row(row: tuple[int, ...], amount: int) -> tuple[int, ...]:
    amount %= len(row)
    return row[amount:] + row[:amount]


def corrected(hits: int, controls: int) -> float:
    return (hits + 1) / (controls + 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=2_000)
    parser.add_argument("--seed", type=int, default=0x51A7)
    args = parser.parse_args()

    whole = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    bodies = {name: whole[name][1:] for name in MESSAGE_ORDER}
    contexts = first_three_contexts() + last_family_contexts()

    f5_fits = tuple(
        literal_affine_context_fit(context, modulus=5, dimension=3)
        for context in contexts
    )
    f3_fits = tuple(
        literal_affine_context_fit(
            context,
            modulus=3,
            dimension=4,
            label_limit=81,
        )
        for context in contexts
    )

    observed_polynomial = best_polynomial_header_rule(
        tuple(whole[name] for name in MESSAGE_ORDER)
    )
    observed_completion = best_missing_completion(
        tuple(bodies[name] for name in MESSAGE_ORDER)
    )

    numpy_streams = tuple(
        np.asarray(whole[name], dtype=np.int16) for name in MESSAGE_ORDER
    )
    left = np.asarray(
        [value for name in MESSAGE_ORDER for value in bodies[name][:-1]],
        dtype=np.int16,
    )
    right = np.asarray(
        [value for name in MESSAGE_ORDER for value in bodies[name][1:]],
        dtype=np.int16,
    )
    identity = np.arange(83, dtype=np.int16)
    assert polynomial_score_numpy(numpy_streams, identity) == observed_polynomial.matches
    assert completion_score_numpy(left, right, identity) == observed_completion.missing

    generator = np.random.default_rng(args.seed)
    polynomial_controls = []
    completion_controls = []
    for _ in range(args.controls):
        mapping = generator.permutation(83).astype(np.int16)
        polynomial_controls.append(polynomial_score_numpy(numpy_streams, mapping))
        completion_controls.append(completion_score_numpy(left, right, mapping))

    neutral = word_inventory(erase_neutral_word)
    cancelling = word_inventory(cancel_direction_word)

    rows = complete_rows(whole)
    suffix_rows = complete_rows(whole, skip_first=True)
    suffix_rows_by_message = complete_rows_by_message(whole, skip_first=True)
    observed_column = column_label_mutual_information(rows)
    observed_suffix_column = column_label_mutual_information(suffix_rows)
    observed_family_score, observed_family_parts = family_heldout_score(
        suffix_rows_by_message
    )
    row_generator = random.Random(args.seed ^ 0x26)
    column_controls = []
    suffix_column_controls = []
    family_controls = []
    for _ in range(args.controls):
        rotated = tuple(
            rotate_row(row, row_generator.randrange(len(row))) for row in rows
        )
        column_controls.append(column_label_mutual_information(rotated))
        suffix_rotated = tuple(
            rotate_row(row, row_generator.randrange(len(row)))
            for row in suffix_rows
        )
        suffix_column_controls.append(
            column_label_mutual_information(suffix_rotated)
        )
        rotated_by_message = {
            name: tuple(
                rotate_row(row, row_generator.randrange(len(row)))
                for row in message_rows
            )
            for name, message_rows in suffix_rows_by_message.items()
        }
        family_controls.append(family_heldout_score(rotated_by_message)[0])

    polynomial_hits = sum(
        score >= observed_polynomial.matches for score in polynomial_controls
    )
    completion_hits = sum(
        score >= observed_completion.missing for score in completion_controls
    )
    column_hits = sum(score >= observed_column for score in column_controls)
    suffix_column_hits = sum(
        score >= observed_suffix_column for score in suffix_column_controls
    )
    family_hits = sum(
        score >= observed_family_score for score in family_controls
    )

    print("A literal affine action on F5^3")
    for fit in f5_fits:
        print(
            f"  {fit.context}: pairs={fit.pairs} "
            f"consistent={fit.consistent}"
        )
    print(f"  exact contexts={sum(fit.consistent for fit in f5_fits)}/{len(f5_fits)}")

    print("B polynomial/check-root headers")
    print(f"  observed={observed_polynomial}")
    print(
        f"  controls median={median(polynomial_controls)}; "
        f"upper tail={(polynomial_hits + 1)}/{args.controls + 1}="
        f"{corrected(polynomial_hits, args.controls):.6f}"
    )

    print("C adjacent quasigroup completion")
    print(f"  observed={observed_completion}")
    print(
        f"  controls median={median(completion_controls)}; "
        f"upper tail={(completion_hits + 1)}/{args.controls + 1}="
        f"{corrected(completion_hits, args.controls):.6f}"
    )

    print("D neutral-eye word quotient")
    print(f"  neutral-only={neutral}")
    print(f"  inverse-cancelling={cancelling}")

    print("E literal affine action on F3^4 plus sentinels")
    for fit in f3_fits:
        print(
            f"  {fit.context}: pairs={fit.pairs} sentinels={fit.sentinel_edges} "
            f"consistent={fit.consistent}"
        )
    print(f"  exact contexts={sum(fit.consistent for fit in f3_fits)}/{len(f3_fits)}")

    print("F twenty-six-column phase")
    print(
        f"  unique complete rows={len(rows)}; observed MI={observed_column:.9f}; "
        f"controls median={median(column_controls):.9f}"
    )
    print(
        f"  upper tail={(column_hits + 1)}/{args.controls + 1}="
        f"{corrected(column_hits, args.controls):.6f}"
    )
    print(
        f"  after dropping every first row: rows={len(suffix_rows)}; "
        f"observed MI={observed_suffix_column:.9f}; "
        f"controls median={median(suffix_column_controls):.9f}"
    )
    print(
        f"  suffix upper tail={(suffix_column_hits + 1)}/{args.controls + 1}="
        f"{corrected(suffix_column_hits, args.controls):.6f}"
    )
    print(
        f"  leave-one-prefix-family-out collision score="
        f"{observed_family_score} parts={observed_family_parts}; "
        f"controls median={median(family_controls)}"
    )
    print(
        f"  family-heldout upper tail={(family_hits + 1)}/{args.controls + 1}="
        f"{corrected(family_hits, args.controls):.6f}"
    )


if __name__ == "__main__":
    main()
