#!/usr/bin/env python3
"""Exhaust simple fixed-shuffle plus selected-card update mechanisms.

The search is vectorized over every standard 83-card base.  It needs NumPy;
the cryptanalytic model and its unit tests remain dependency-free.
"""

from __future__ import annotations

import argparse
import heapq
from dataclasses import dataclass

import numpy as np

from eye_mystery.corpus import (
    MESSAGE_ORDER,
    MESSAGES,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)
from eye_mystery.deck_selected import ACTIONS, selected_action_indices
from eye_mystery.deck_shuffles import standard_base_candidates


@dataclass(frozen=True)
class Result:
    mismatches: int
    unique: int
    action: str
    marker_mode: str
    base: str

    @property
    def key(self) -> tuple[int, int]:
        return self.mismatches, self.unique


COMPARISONS = (
    ("east1", 1, "west1", 1, 24),
    ("east1", 1, "east2", 1, 24),
    ("west2", 1, "east3", 1, 5),
    ("west2", 1, "west3", 1, 5),
    ("east4", 1, "west4", 1, 20),
    ("east4", 1, "east5", 1, 20),
    ("west1", 34, "west1", 64, 18),
    ("west1", 34, "east2", 39, 18),
    ("west1", 34, "east2", 74, 18),
    ("west1", 40, "east1", 40, 9),
    ("west1", 40, "east1", 68, 9),
    ("east4", 68, "west4", 71, 30),
    ("east4", 68, "east5", 69, 30),
)


def action_table(size: int, action: str) -> np.ndarray:
    return np.asarray(
        [selected_action_indices(size, action, rank) for rank in range(size)],
        dtype=np.int16,
    )


def decode_batch(
    ciphertext: tuple[int, ...], bases: np.ndarray, table: np.ndarray
) -> np.ndarray:
    rows, size = bases.shape
    deck = np.broadcast_to(np.arange(size, dtype=np.uint8), (rows, size)).copy()
    decoded = np.empty((rows, len(ciphertext)), dtype=np.uint8)
    for step, card in enumerate(ciphertext):
        deck = np.take_along_axis(deck, bases, axis=1)
        ranks = np.argmax(deck == card, axis=1).astype(np.uint8)
        decoded[:, step] = ranks
        deck = np.take_along_axis(deck, table[ranks], axis=1)
    return decoded


def split_message(message: tuple[int, ...], lengths: tuple[int, ...]):
    start = 0
    for length in lengths:
        yield message[start : start + length]
        start += length
    if start != len(message):
        raise ValueError("row-pair lengths do not cover the message")


def decode_mode(
    message: tuple[int, ...],
    lengths: tuple[int, ...],
    bases: np.ndarray,
    table: np.ndarray,
    mode: str,
) -> np.ndarray:
    if mode == "full":
        return decode_batch(message, bases, table)
    if mode == "reset":
        return decode_batch(message[1:], bases, table)
    segments = tuple(split_message(message, lengths))
    if mode == "rows":
        return np.concatenate(
            tuple(decode_batch(segment, bases, table) for segment in segments),
            axis=1,
        )
    if mode == "body-rows":
        body_segments = (segments[0][1:],) + segments[1:]
        return np.concatenate(
            tuple(decode_batch(segment, bases, table) for segment in body_segments),
            axis=1,
        )
    raise ValueError(f"unknown reset mode: {mode}")


def score(
    streams: dict[str, np.ndarray], *, marker_mode: str
) -> tuple[np.ndarray, np.ndarray]:
    offset = 1 if marker_mode in ("reset", "body-rows") else 0
    rows = next(iter(streams.values())).shape[0]
    mismatches = np.zeros(rows, dtype=np.int16)
    for left, left_start, right, right_start, length in COMPARISONS:
        left_values = streams[left][
            :, left_start - offset : left_start - offset + length
        ]
        right_values = streams[right][
            :, right_start - offset : right_start - offset + length
        ]
        mismatches += np.count_nonzero(left_values != right_values, axis=1)
    combined = np.concatenate(tuple(streams.values()), axis=1)
    ordered = np.sort(combined, axis=1)
    unique = 1 + np.count_nonzero(ordered[:, 1:] != ordered[:, :-1], axis=1)
    return mismatches, unique


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--modes",
        nargs="+",
        choices=("full", "reset", "rows", "body-rows"),
        default=("full", "reset", "rows", "body-rows"),
    )
    args = parser.parse_args()
    candidates = [("identity", tuple(range(83)))]
    candidates.extend(standard_base_candidates(83))
    names = [name for name, _ in candidates]
    bases = np.asarray([base for _, base in candidates], dtype=np.int16)
    messages = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    best: list[tuple[tuple[int, int], int, Result]] = []
    serial = 0
    tested = 0
    for action in ACTIONS:
        table = action_table(83, action)
        for marker_mode in args.modes:
            streams = {
                name: decode_mode(
                    message,
                    ROW_PAIR_TRIGRAM_LENGTHS[name],
                    bases,
                    table,
                    marker_mode,
                )
                for name, message in messages.items()
            }
            mismatches, unique = score(streams, marker_mode=marker_mode)
            for row, base_name in enumerate(names):
                result = Result(
                    int(mismatches[row]),
                    int(unique[row]),
                    action,
                    marker_mode,
                    base_name,
                )
                item = (tuple(-value for value in result.key), serial, result)
                serial += 1
                if len(best) < 30:
                    heapq.heappush(best, item)
                elif item > best[0]:
                    heapq.heapreplace(best, item)
            tested += len(names)
            best_row = min(
                range(len(names)),
                key=lambda row: (int(mismatches[row]), int(unique[row])),
            )
            print(
                f"{action:<15} {marker_mode:<5} "
                f"best={int(mismatches[best_row])}/230 "
                f"unique={int(unique[best_row])} base={names[best_row]}",
                flush=True,
            )

    print(
        f"tested: {tested} "
        f"({len(names)} bases x {len(ACTIONS)} actions x {len(args.modes)} modes)"
    )
    print("mismatch unique action mode base")
    for _, _, result in sorted(best, key=lambda item: item[2].key):
        print(
            f"{result.mismatches:>8} {result.unique:>6} "
            f"{result.action:<15} {result.marker_mode:<5} {result.base}"
        )


if __name__ == "__main__":
    main()
