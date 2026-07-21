#!/usr/bin/env python3
"""Test the best 16-state East-diagonal walk as a substitution cipher."""

from __future__ import annotations

import argparse
import glob
import random
from pathlib import Path

from eye_mystery.affine_walk import trace_affine_walk
from eye_mystery.corpus import MESSAGES
from eye_mystery.mono_substitution import solve_mono_substitution
from eye_mystery.ngram import TetragramModel, ascii_letters


NAMES = ("east1", "east3", "east5")
PARAMETERS = {
    "generator": 1,
    "translation_pair": (4, 2),
    "center_mode": "reflection",
    "up_order": (2, 0, 1),
    "down_order": (0, 1, 2),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus", nargs="+")
    parser.add_argument("--restarts", type=int, default=12)
    parser.add_argument("--iterations", type=int, default=150_000)
    parser.add_argument("--seed", type=int, default=20260721)
    parser.add_argument("--encode-finnish-diacritics", action="store_true")
    parser.add_argument("--null-trials", type=int, default=0)
    parser.add_argument("--null-restarts", type=int, default=4)
    parser.add_argument("--null-iterations", type=int, default=60_000)
    args = parser.parse_args()
    paths = [
        Path(value)
        for pattern in args.corpus
        for value in (glob.glob(pattern) if any(c in pattern for c in "*?[") else [pattern])
    ]
    corpus = "\n".join(path.read_text(errors="ignore") for path in paths)
    if args.encode_finnish_diacritics:
        corpus = corpus.translate(
            str.maketrans(
                {
                    "ä": "q",
                    "ö": "x",
                    "å": "z",
                    "Ä": "Q",
                    "Ö": "X",
                    "Å": "Z",
                }
            )
        )
    model = TetragramModel.train(corpus)
    streams = tuple(trace_affine_walk(MESSAGES[name], **PARAMETERS) for name in NAMES)
    result = solve_mono_substitution(
        streams,
        model,
        restarts=args.restarts,
        iterations=args.iterations,
        seed=args.seed,
    )
    windows = sum(max(0, len(stream) - 3) for stream in streams)
    print("states:", len(result.states), result.states)
    print("score per tetragram:", result.score / windows)
    display_table = (
        str.maketrans({"Q": "Ä", "X": "Ö", "Z": "Å"})
        if args.encode_finnish_diacritics
        else None
    )
    for name, plaintext in zip(NAMES, result.plaintexts, strict=True):
        if display_table is not None:
            plaintext = plaintext.translate(display_table)
        print(f"{name}: {plaintext}")

    reference = ascii_letters(corpus)[: sum(map(len, streams))]
    reference_score = model.score(reference)
    print(
        "in-corpus reference score per tetragram:",
        reference_score / max(1, len(reference) - 3),
    )
    if args.null_trials:
        print("within-message shuffle null scores:")
        rng = random.Random(args.seed + 1)
        for trial in range(args.null_trials):
            shuffled_streams = []
            for stream in streams:
                shuffled = list(stream)
                rng.shuffle(shuffled)
                shuffled_streams.append(tuple(shuffled))
            null_result = solve_mono_substitution(
                tuple(shuffled_streams),
                model,
                restarts=args.null_restarts,
                iterations=args.null_iterations,
                seed=args.seed + 10_000 + trial,
            )
            print(f"  {trial + 1}: {null_result.score / windows:.4f}")


if __name__ == "__main__":
    main()
