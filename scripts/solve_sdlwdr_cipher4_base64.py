#!/usr/bin/env python3
"""Test substituted, unpadded Base64 as sdlwdr cipher 4's inner codec."""

from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
import random

from eye_mystery.practice_cipher4 import cyclic_differences
from eye_mystery.practice_cipher4_base64 import (
    BASE64_ALPHABET,
    Base64SubstitutionAnnealer,
    ByteNgrams,
    encode_base64_substitution,
    normalize_training_bytes,
)


ROOT = Path(__file__).resolve().parents[1]


def planted_streams(
    corpus: bytes, lengths: tuple[int, ...], seed: int
) -> tuple[tuple[tuple[int, ...], ...], tuple[bytes, ...]]:
    rng = random.Random(seed)
    normalized = normalize_training_bytes(corpus)
    decoded_lengths = tuple((length * 6) // 8 for length in lengths)
    start_limit = len(normalized) - max(decoded_lengths) - 1
    starts = [rng.randrange(start_limit) for _ in lengths]
    plaintexts = tuple(
        normalized[start : start + length]
        for start, length in zip(starts, decoded_lengths, strict=True)
    )
    shuffled = list(BASE64_ALPHABET)
    rng.shuffle(shuffled)
    inverse = {character: index for index, character in enumerate(shuffled)}
    streams = tuple(encode_base64_substitution(text, inverse) for text in plaintexts)
    if tuple(map(len, streams)) != lengths:
        raise AssertionError("planted Base64 lengths do not match the target")
    return streams, plaintexts


def render(data: bytes, limit: int = 500) -> str:
    return "".join(
        chr(value) if value in (9, 10, 13) or 32 <= value <= 126 else f"\\x{value:02x}"
        for value in data[:limit]
    )


def run_restarts(
    streams: tuple[tuple[int, ...], ...],
    model: ByteNgrams,
    expected: bytes,
    *,
    restarts: int,
    iterations: int,
    temperature: float,
    seed: int,
):
    candidates = []
    for restart in range(restarts):
        annealer = Base64SubstitutionAnnealer(
            streams,
            model,
            random.Random(seed + restart),
            expected,
        )
        candidate = annealer.run(iterations, temperature)
        candidates.append(candidate)
        total = sum(map(len, candidate.plaintexts))
        print(
            f"restart={restart} score={candidate.score:.2f} "
            f"printable={candidate.printable}/{total} "
            f"letters-space={candidate.letters_or_spaces}/{total}",
            flush=True,
        )
    return sorted(candidates, key=lambda candidate: candidate.score, reverse=True)


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
    parser.add_argument("--restarts", type=int, default=8)
    parser.add_argument("--iterations", type=int, default=300_000)
    parser.add_argument("--temperature", type=float, default=18.0)
    parser.add_argument("--seed", type=int, default=0x53444C5744520402)
    parser.add_argument("--control", action="store_true")
    args = parser.parse_args()

    corpus = args.corpus.read_bytes()
    model = ByteNgrams.train(corpus)
    expected = base64.b64encode(normalize_training_bytes(corpus))
    messages = json.loads(args.data.read_text())
    streams = tuple(cyclic_differences(message) for message in messages)
    truth = None
    if args.control:
        streams, truth = planted_streams(corpus, tuple(map(len, streams)), args.seed)
    print(
        "stream lengths:", tuple(map(len, streams)),
        "decoded lengths:", tuple((len(stream) * 6) // 8 for stream in streams),
    )
    candidates = run_restarts(
        streams,
        model,
        expected,
        restarts=args.restarts,
        iterations=args.iterations,
        temperature=args.temperature,
        seed=args.seed,
    )
    best = candidates[0]
    print("\nbest mapping", best.mapping)
    for index, plaintext in enumerate(best.plaintexts):
        print(f"\nportion {index + 1}\n{render(plaintext)}")
    if truth is not None:
        recovered = b"".join(best.plaintexts)
        expected_plaintext = b"".join(truth)
        accuracy = sum(
            left == right
            for left, right in zip(recovered, expected_plaintext, strict=True)
        ) / len(expected_plaintext)
        print(f"\ncontrol byte accuracy={accuracy:.6%}")


if __name__ == "__main__":
    main()
