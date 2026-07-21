#!/usr/bin/env python3
"""Scan standard fixed-shuffle/selected-card models for sdlwdr cipher #3."""

from __future__ import annotations

import argparse
import heapq
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from eye_mystery.deck_selected import ACTIONS, selected_action_indices
from eye_mystery.deck_shuffles import standard_base_candidates


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Result:
    unique: int
    maximum: int
    ioc: float
    under_42: float
    action: str
    mode: str
    base: str

    @property
    def key(self) -> tuple[int, int, float, float]:
        return self.unique, self.maximum, -self.ioc, -self.under_42


def action_table(size: int, action: str) -> np.ndarray:
    if action == "swap-front":
        rows = []
        for rank in range(size):
            row = list(range(size))
            row[0], row[rank] = row[rank], row[0]
            rows.append(row)
        return np.asarray(rows, dtype=np.int16)
    return np.asarray(
        [selected_action_indices(size, action, rank) for rank in range(size)],
        dtype=np.int16,
    )


def decode_batch(
    ciphertext: tuple[int, ...], bases: np.ndarray, table: np.ndarray
) -> np.ndarray:
    rows, size = bases.shape
    deck = np.broadcast_to(np.arange(size, dtype=np.int16), (rows, size)).copy()
    decoded = np.empty((rows, len(ciphertext)), dtype=np.uint8)
    for step, card in enumerate(ciphertext):
        deck = np.take_along_axis(deck, bases, axis=1)
        ranks = np.argmax(deck == card, axis=1).astype(np.uint8)
        decoded[:, step] = ranks
        deck = np.take_along_axis(deck, table[ranks], axis=1)
    return decoded


def row_metrics(decoded: np.ndarray) -> tuple[np.ndarray, ...]:
    rows, length = decoded.shape
    counts = np.zeros((rows, 83), dtype=np.int16)
    row_index = np.arange(rows)
    for column in range(length):
        counts[row_index, decoded[:, column]] += 1
    unique = np.count_nonzero(counts, axis=1)
    maximum = np.max(decoded, axis=1)
    pairs = np.sum(counts * (counts - 1), axis=1)
    ioc = pairs / (length * (length - 1))
    under_42 = np.count_nonzero(decoded < 42, axis=1) / length
    return unique, maximum, ioc, under_42


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument(
        "--actions", nargs="+", default=("swap-front",) + ACTIONS
    )
    parser.add_argument("--group", choices=("A", "B", "C"), default="C")
    parser.add_argument("--index", type=int, default=4)
    args = parser.parse_args()

    data = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher3.json").read_text()
    )
    message = tuple(data[args.group][args.index])
    candidates = [("identity", tuple(range(83)))]
    candidates.extend(standard_base_candidates(83))
    names = [name for name, _ in candidates]
    bases = np.asarray([base for _, base in candidates], dtype=np.int16)

    best: list[tuple[tuple[float, ...], int, Result]] = []
    serial = 0
    for action in args.actions:
        table = action_table(83, action)
        for mode, ciphertext in (("full", message), ("body", message[1:])):
            decoded = decode_batch(ciphertext, bases, table)
            unique, maximum, ioc, under_42 = row_metrics(decoded)
            best_row = min(
                range(len(names)),
                key=lambda row: (
                    int(unique[row]),
                    int(maximum[row]),
                    -float(ioc[row]),
                    -float(under_42[row]),
                ),
            )
            print(
                f"{action:<15} {mode:<4} "
                f"best unique={int(unique[best_row]):2} "
                f"max={int(maximum[best_row]):2} "
                f"ioc={float(ioc[best_row]):.4f} "
                f"<42={100 * float(under_42[best_row]):5.1f}% "
                f"base={names[best_row]}",
                flush=True,
            )
            for row, base_name in enumerate(names):
                result = Result(
                    int(unique[row]),
                    int(maximum[row]),
                    float(ioc[row]),
                    float(under_42[row]),
                    action,
                    mode,
                    base_name,
                )
                item = (
                    tuple(-value for value in result.key),
                    serial,
                    result,
                )
                serial += 1
                if len(best) < args.limit:
                    heapq.heappush(best, item)
                elif item > best[0]:
                    heapq.heapreplace(best, item)

    print("\nunique max ioc <42% action mode base")
    for _, _, result in sorted(best, key=lambda item: item[2].key):
        print(
            f"{result.unique:>6} {result.maximum:>3} {result.ioc:>6.4f} "
            f"{100 * result.under_42:>5.1f} {result.action:<15} "
            f"{result.mode:<4} {result.base}"
        )


if __name__ == "__main__":
    main()
