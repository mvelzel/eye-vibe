#!/usr/bin/env python3
"""Calibrate a static 83-to-27 homophonic reading of Cipher 3."""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import product
import json
from math import log
from pathlib import Path
import random

from eye_mystery.practice_cipher3_wide import normalize_plaintext42
from scan_sdlwdr_cipher4_homophonic_sources import repeat_constraints
from solve_sdlwdr_cipher4_homophones import (
    Annealer,
    Ngrams,
    normalize,
    planted_control,
    render,
)


ROOT = Path(__file__).resolve().parents[1]


def dense_trigram_model(text: str, alpha: float = 0.2) -> Ngrams:
    values = normalize(text)
    counts = Counter(
        values[index : index + 3]
        for index in range(len(values) - 2)
    )
    possibilities = 27**3
    denominator = sum(counts.values()) + alpha * possibilities
    scores = {
        gram: log((counts.get(gram, 0) + alpha) / denominator)
        for gram in product(range(27), repeat=3)
    }
    singles = Counter(values)
    return Ngrams(
        3,
        scores,
        min(scores.values()),
        tuple(
            (singles[value] + 1) / (len(values) + 27)
            for value in range(27)
        ),
    )


def best_anneal(
    streams: tuple[tuple[int, ...], ...],
    model: Ngrams,
    *,
    restarts: int,
    iterations: int,
    temperature: float,
    seed: int,
) -> tuple[float, list[int], Annealer]:
    annealer = Annealer(
        streams,
        model,
        random.Random(seed),
        "frequency",
    )
    best_score = float("-inf")
    best_key: list[int] | None = None
    for restart in range(restarts):
        score, key = annealer.run(iterations, temperature)
        if score > best_score:
            best_score = score
            best_key = key
        print(
            f"  restart={restart + 1} score={score:.2f} "
            f"best={best_score:.2f}",
            flush=True,
        )
    assert best_key is not None
    return best_score, best_key, annealer


def source_matches(target: tuple[int, ...], source: tuple[int, ...]) -> int:
    constraints = repeat_constraints(target)
    return sum(
        all(
            source[start + left] == source[start + right]
            for left, right in constraints
        )
        for start in range(len(source) - len(target) + 1)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--english-corpus",
        type=Path,
        default=Path("/private/tmp/sherlock-holmes.txt"),
    )
    parser.add_argument(
        "--source-corpora",
        nargs="*",
        type=Path,
        default=(),
    )
    parser.add_argument("--restarts", type=int, default=8)
    parser.add_argument("--iterations", type=int, default=300_000)
    parser.add_argument("--temperature", type=float, default=8.0)
    parser.add_argument("--control-offset", type=int, default=20_000)
    args = parser.parse_args()

    data = json.loads(
        (ROOT / "artifacts/practice-sdlwdr/cipher3.json").read_text()
    )
    streams = tuple(
        tuple(message)
        for group in ("A", "B", "C")
        for message in data[group]
    )
    lengths = tuple(map(len, streams))
    corpus = args.english_corpus.read_text(errors="ignore")
    normalized = normalize(corpus)
    model = dense_trigram_model(corpus)

    allocation_probe = Annealer(
        (tuple(range(83)),),
        model,
        random.Random(1),
        "frequency",
    )
    required = sum(lengths)
    expected = normalized[
        args.control_offset : args.control_offset + required
    ]
    if len(expected) != required:
        raise ValueError("the control corpus is too short")
    control = planted_control(
        expected,
        lengths,
        allocation_probe.slot_counts,
        random.Random(99),
    )

    print("planted matched-length control")
    control_score, control_key, control_annealer = best_anneal(
        control,
        model,
        restarts=args.restarts,
        iterations=args.iterations,
        temperature=args.temperature,
        seed=123,
    )
    control_decoded = control_annealer.decode(control_key)
    cursor = 0
    correct = 0
    for decoded, length in zip(control_decoded, lengths, strict=True):
        correct += sum(
            observed == truth
            for observed, truth in zip(
                decoded,
                expected[cursor : cursor + length],
                strict=True,
            )
        )
        cursor += length
    print(f"  accuracy={correct / required:.6%}")
    print(f"  first={render(control_decoded[0])}")

    print("real raw-symbol corpus")
    real_score, real_key, real_annealer = best_anneal(
        streams,
        model,
        restarts=args.restarts,
        iterations=args.iterations,
        temperature=args.temperature,
        seed=0xC3F,
    )
    real_decoded = real_annealer.decode(real_key)
    print(f"  control-real score gap={control_score - real_score:.2f}")
    print(f"  first={render(real_decoded[0])}")

    if args.source_corpora:
        print("one-way static-homophone source fingerprints")
        targets = {
            "raw": tuple(data["C"][4]),
            "body": tuple(data["C"][4][1:]),
            "difference-forward": tuple(
                (right - left) % 83
                for left, right in zip(
                    data["C"][4],
                    data["C"][4][1:],
                )
            ),
            "difference-backward": tuple(
                (left - right) % 83
                for left, right in zip(
                    data["C"][4],
                    data["C"][4][1:],
                )
            ),
        }
        for path in args.source_corpora:
            source = normalize_plaintext42(
                path.read_text(errors="ignore")
            )
            for name, target in targets.items():
                print(
                    f"  {path.name} {name}: "
                    f"{source_matches(target, source)}"
                )


if __name__ == "__main__":
    main()
