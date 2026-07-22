#!/usr/bin/env python3
"""Run the frozen case-sensitive bijection attack on sdlwdr cipher 4."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random

from eye_mystery.practice_cipher4_bijection import (
    BijectionAnnealer,
    CaseNgrams,
    encode_substitution,
    normalize_case_text,
)
from eye_mystery.practice_cipher4 import MODULUS


ROOT = Path(__file__).resolve().parents[1]
POOLS = {
    "sentence": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,?!",
    "literary": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,'-",
    "formal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .;:-",
    "prose": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,:;",
}


def action_stream(message: list[int]) -> tuple[int, ...]:
    return (message[0],) + tuple(
        (right - left) % MODULUS for left, right in zip(message, message[1:])
    )


def planted_control(
    corpus: str,
    alphabet: str,
    lengths: tuple[int, ...],
    seed: int,
) -> tuple[tuple[tuple[int, ...], ...], tuple[str, ...]]:
    normalized = normalize_case_text(corpus, alphabet)
    start = 20_000
    required = sum(lengths)
    if len(normalized) < start + required:
        raise ValueError("corpus is too short for the planted control")
    source = normalized[start : start + required]
    plaintexts = []
    cursor = 0
    for length in lengths:
        plaintexts.append(source[cursor : cursor + length])
        cursor += length
    shuffled = list(range(len(alphabet)))
    random.Random(seed).shuffle(shuffled)
    mapping = {
        character: shuffled[index]
        for index, character in enumerate(alphabet)
    }
    return encode_substitution(plaintexts, mapping), tuple(plaintexts)


def accuracy(candidate: tuple[str, ...], expected: tuple[str, ...]) -> float:
    equal = sum(
        left == right
        for candidate_stream, expected_stream in zip(candidate, expected, strict=True)
        for left, right in zip(candidate_stream, expected_stream, strict=True)
    )
    return equal / sum(map(len, expected))


def search(
    streams: tuple[tuple[int, ...], ...],
    model: CaseNgrams,
    alphabet: str,
    *,
    restarts: int,
    iterations: int,
    temperature: float,
    seed: int,
) -> list:
    results = []
    for restart in range(restarts):
        rng = random.Random(seed + restart * 1_000_003)
        annealer = BijectionAnnealer(streams, model, alphabet, rng)
        candidate = annealer.run(iterations, temperature)
        results.append(candidate)
        print(
            f"  restart={restart + 1:>2} score={candidate.score:>12.2f} "
            f"{candidate.plaintexts[0][:100]!r}",
            flush=True,
        )
    return sorted(results, key=lambda item: item.score, reverse=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        type=Path,
        default=ROOT / "artifacts/practice-sdlwdr/cipher4.json",
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        default=Path(
            "/private/tmp/noita-eye-puzzle-scratchpad/"
            "research/data/lang/english-corpus-large.txt"
        ),
    )
    parser.add_argument("--pool", choices=tuple(POOLS) + ("all",), default="all")
    parser.add_argument("--restarts", type=int, default=12)
    parser.add_argument("--iterations", type=int, default=300_000)
    parser.add_argument("--temperature", type=float, default=14.0)
    parser.add_argument("--seed", type=int, default=0x53444C5744520401)
    args = parser.parse_args()

    messages = json.loads(args.data.read_text())
    real_streams = tuple(action_stream(message) for message in messages)
    corpus = args.corpus.read_text(errors="ignore")
    selected = POOLS if args.pool == "all" else {args.pool: POOLS[args.pool]}

    for pool_name, alphabet in selected.items():
        print(f"\nPOOL {pool_name} {alphabet!r}")
        model = CaseNgrams.train(corpus, alphabet)
        control_streams, control_plaintexts = planted_control(
            corpus,
            alphabet,
            tuple(map(len, real_streams)),
            args.seed,
        )
        print("CONTROL")
        controls = search(
            control_streams,
            model,
            alphabet,
            restarts=args.restarts,
            iterations=args.iterations,
            temperature=args.temperature,
            seed=args.seed ^ 0xC0117A01,
        )
        print(
            f"CONTROL BEST score={controls[0].score:.2f} "
            f"accuracy={accuracy(controls[0].plaintexts, control_plaintexts):.6f}"
        )

        print("REAL")
        real = search(
            real_streams,
            model,
            alphabet,
            restarts=args.restarts,
            iterations=args.iterations,
            temperature=args.temperature,
            seed=args.seed,
        )
        print(f"REAL BEST score={real[0].score:.2f}")
        print("MAPPING", real[0].mapping)
        for plaintext in real[0].plaintexts:
            print(plaintext)


if __name__ == "__main__":
    main()
