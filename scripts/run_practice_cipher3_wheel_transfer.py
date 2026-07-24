#!/usr/bin/env python3
"""Calibrate the solved-C82-wheel transfer against practice cipher 3."""

from __future__ import annotations

import argparse
import random
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from statistics import mean

from eye_mystery.practice_cipher3_wide import (
    GROUPS,
    TrigramModel42,
    decode_recovered_wheel,
    load_cipher3,
    permute_nonexceptional_labels,
    render_wheel_coordinates,
    select_wheel_transfer,
)


WORKER_MODELS = None


def read_corpora(paths: list[Path]) -> str:
    return "\n".join(path.read_text(errors="ignore") for path in paths)


def initialize_worker(models) -> None:
    global WORKER_MODELS
    WORKER_MODELS = models


def score_control(streams) -> float:
    assert WORKER_MODELS is not None
    return select_wheel_transfer(
        streams,
        WORKER_MODELS,
    ).heldout_score_per_trigram


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--english-corpus", type=Path, nargs="+", required=True)
    parser.add_argument("--finnish-corpus", type=Path, nargs="+", required=True)
    parser.add_argument("--controls", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0xC1F3A82)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    streams = load_cipher3()
    models = {
        "english": TrigramModel42.train(read_corpora(args.english_corpus)),
        "finnish": TrigramModel42.train(read_corpora(args.finnish_corpus)),
    }
    observed = select_wheel_transfer(streams, models)
    rng = random.Random(args.seed)
    control_streams = [
        permute_nonexceptional_labels(streams, rng)
        for _ in range(args.controls)
    ]
    if args.workers < 1:
        parser.error("--workers must be positive")
    if args.workers == 1:
        initialize_worker(models)
        controls = list(map(score_control, control_streams))
    else:
        with ProcessPoolExecutor(
            max_workers=args.workers,
            initializer=initialize_worker,
            initargs=(models,),
        ) as executor:
            controls = list(executor.map(score_control, control_streams))
    corrected = (
        sum(score >= observed.heldout_score_per_trigram for score in controls)
        + 1
    ) / (args.controls + 1)
    print("observed:", observed)
    print(
        f"heldout null={min(controls):.6f}..{max(controls):.6f}, "
        f"mean={mean(controls):.6f}; corrected upper tail={corrected:.6f}"
    )

    shifts = dict(observed.shifts)
    print("selected renderings:")
    for group in GROUPS:
        for index, message in enumerate(streams[group]):
            coordinates = decode_recovered_wheel(
                message,
                observed.semantics,
                initial_direction=observed.initial_direction,
                initial_parity=observed.initial_parity,
            )
            text = render_wheel_coordinates(
                coordinates,
                shifts[f"{group}{index}"],
                observed.orientation,
            )
            print(f"  {group}{index}: {text}")


if __name__ == "__main__":
    main()
