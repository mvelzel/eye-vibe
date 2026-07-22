#!/usr/bin/env python3
"""Run a bounded quadratic-character projection of the Eye transitions."""

from __future__ import annotations

import argparse
from random import Random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.initials import perfect_successor_rotation
from eye_mystery.marker_bwt import marker_bwt_lf_order
from eye_mystery.marker_orders import MARKER_TRIE_ORDER
from eye_mystery.paley_projection import (
    RepeatContext,
    best_binary_text_fit,
    complement_fit,
    transition_bits,
)


CONTEXTS = (
    RepeatContext(
        "first-six",
        9,
        (
            ("east1", 40),
            ("east1", 68),
            ("west1", 40),
            ("west1", 70),
            ("east2", 45),
            ("east2", 80),
        ),
    ),
    RepeatContext(
        "first-long",
        18,
        (("west1", 34), ("west1", 64), ("east2", 39), ("east2", 74)),
    ),
    RepeatContext(
        "last-three",
        30,
        (("east4", 68), ("west4", 71), ("east5", 69)),
    ),
    RepeatContext(
        "last-nested",
        25,
        (("east4", 73), ("west4", 76), ("east5", 74), ("east3", 64)),
    ),
)


def relabel(
    streams: dict[str, tuple[int, ...]], labels: list[int]
) -> dict[str, tuple[int, ...]]:
    return {
        name: tuple(labels[value] for value in stream)
        for name, stream in streams.items()
    }


def upper_tail(observed: float, controls: list[float]) -> tuple[int, int, float]:
    numerator = 1 + sum(value >= observed for value in controls)
    denominator = len(controls) + 1
    return numerator, denominator, numerator / denominator


def render(values: tuple[int, ...]) -> str:
    return "".join(chr(value) if 32 <= value <= 126 else "." for value in values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=2_000)
    parser.add_argument("--seed", type=int, default=20260722)
    args = parser.parse_args()

    streams = {
        name: trigram_values(MESSAGES[name])
        for name in MESSAGE_ORDER
    }
    trail = perfect_successor_rotation()
    if trail is None:
        raise RuntimeError("initial markers do not define their fixed trail")
    orders = {
        "canonical": MESSAGE_ORDER,
        "marker-trie": MARKER_TRIE_ORDER,
        "marker-trail": trail,
        "marker-lf": marker_bwt_lf_order(),
    }

    bits = tuple(bit for name in MESSAGE_ORDER for bit in transition_bits(streams[name]))
    observed_fit = complement_fit(streams, CONTEXTS)
    observed_text = best_binary_text_fit(streams, orders)
    print("Paley transition bits:", len(bits))
    print("  ones:", sum(bits), f"({sum(bits) / len(bits):.6f})")
    print("  repeat complement fit:", observed_fit)
    print("  best ASCII fit:", observed_text)
    print("  preview:", render(observed_text.values[:160]))

    rng = Random(args.seed)
    complement_controls = []
    ascii_controls = []
    for _ in range(args.trials):
        labels = list(range(83))
        rng.shuffle(labels)
        shuffled = relabel(streams, labels)
        complement_controls.append(complement_fit(shuffled, CONTEXTS).matches)
        ascii_controls.append(best_binary_text_fit(shuffled, orders).rate)

    print(
        "  repeat-fit relabel upper tail:",
        upper_tail(observed_fit.matches, complement_controls),
    )
    print(
        "  ASCII relabel upper tail:",
        upper_tail(observed_text.rate, ascii_controls),
    )


if __name__ == "__main__":
    main()
