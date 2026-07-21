#!/usr/bin/env python3
"""Apply the Meditation Chamber's exact 83x26 blood mask to the eye values."""

from __future__ import annotations

import argparse
import random

from eye_mystery.blood_sieve import pack_chunks
from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, ROW_PAIR_TRIGRAM_LENGTHS


def text_score(data: bytes) -> int:
    """A deliberately simple byte-text score used identically for the null."""
    score = 0
    for byte in data:
        if byte == 32:
            score += 4
        elif 65 <= byte <= 90 or 97 <= byte <= 122:
            score += 3
        elif byte in b".,;:'!?-()\n\r" or 48 <= byte <= 57:
            score += 1
        elif 32 <= byte <= 126:
            score += 0
        else:
            score -= 4
    return score


def mapped_bits(
    value_map: tuple[int, ...], *, mirror_values: bool, reverse_positions: bool
) -> tuple[int, ...]:
    from eye_mystery.blood_sieve import sieve_row_pair, split_row_pair_values

    output: list[int] = []
    for name in MESSAGE_ORDER:
        for row in split_row_pair_values(MESSAGES[name], ROW_PAIR_TRIGRAM_LENGTHS[name]):
            output.extend(
                sieve_row_pair(
                    tuple(value_map[value] for value in row),
                    mirror_values=mirror_values,
                    reverse_positions=reverse_positions,
                )
            )
    return tuple(output)


def ranked_outputs(value_map: tuple[int, ...] = tuple(range(83))):
    rows = []
    for mirror_values in (False, True):
        for reverse_positions in (False, True):
            base = mapped_bits(
                value_map,
                mirror_values=mirror_values,
                reverse_positions=reverse_positions,
            )
            for mask in ("static", "alternating"):
                masked = (
                    base
                    if mask == "static"
                    else tuple(bit ^ (index & 1) for index, bit in enumerate(base))
                )
                for reverse_stream in (False, True):
                    oriented = tuple(reversed(masked)) if reverse_stream else masked
                    for invert in (False, True):
                        bits = tuple(1 - bit for bit in oriented) if invert else oriented
                        for width in (7, 8):
                            for lsb in (False, True):
                                for offset in range(width):
                                    data = bytes(
                                        pack_chunks(
                                            bits,
                                            width=width,
                                            offset=offset,
                                            least_significant_first=lsb,
                                        )
                                    )
                                    raw_score = text_score(data)
                                    rows.append(
                                        (
                                            raw_score / len(data),
                                            raw_score,
                                            mirror_values,
                                            reverse_positions,
                                            mask,
                                            reverse_stream,
                                            invert,
                                            width,
                                            lsb,
                                            offset,
                                            data,
                                        )
                                    )
    return sorted(rows, reverse=True, key=lambda row: (row[0], row[1]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--null-trials", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=8326)
    args = parser.parse_args()

    ranked = ranked_outputs()
    best = ranked[0]
    print("blood pixels: 1114 / 2158 (51.622%)")
    print("eye bits:", sum(len(MESSAGES[name]) // 3 for name in MESSAGE_ORDER))
    print("best normalized text score:", f"{best[0]:.6f}", f"raw={best[1]}")
    print(
        "variant:",
        f"mirror_values={best[2]}",
        f"reverse_positions={best[3]}",
        f"mask={best[4]}",
        f"reverse_stream={best[5]}",
        f"invert={best[6]}",
        f"width={best[7]}",
        f"lsb_first={best[8]}",
        f"offset={best[9]}",
    )
    print("bytes repr:", repr(best[10]))

    rng = random.Random(args.seed)
    null_scores: list[float] = []
    identity = list(range(83))
    for _ in range(args.null_trials):
        rng.shuffle(identity)
        null_scores.append(ranked_outputs(tuple(identity))[0][0])
    exceed = sum(score >= best[0] for score in null_scores)
    p_value = (exceed + 1) / (args.null_trials + 1)
    print(
        "global-alphabet-permutation null:",
        f"exceed={exceed}/{args.null_trials}",
        f"p={p_value:.6f}",
        f"mean_best={sum(null_scores) / len(null_scores):.6f}",
        f"max_best={max(null_scores):.6f}",
    )


if __name__ == "__main__":
    main()
