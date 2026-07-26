#!/usr/bin/env python3
"""Calibrate and run the exact arbitrary static two-sheet attack."""

from __future__ import annotations

import argparse
import hashlib
import random
from collections import Counter
from pathlib import Path

from eye_mystery.practice_cipher3_arbitrary_two_sheet import (
    decode_streams,
    encode_streams,
    event_accuracy,
    group_streams,
    optimize_key,
    random_key,
    render_streams,
    trigram_score,
)
from eye_mystery.practice_cipher3_wide import (
    TrigramModel42,
    load_cipher3,
    normalize_plaintext42,
)


TRAINING_SHA256 = "922e2a12ccb43a4c9544c260b2166c6ad2097aeb5957faeee113f173bb857cd0"
PLANT_SHA256 = "9a6844ac0703853720010787c7b6c70b0020f1ab1862dcd74452fa46474d1215"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def overlaps(
    interval: tuple[int, int],
    used: list[tuple[int, int]],
) -> bool:
    start, end = interval
    return any(
        start < used_end and used_start < end
        for used_start, used_end in used
    )


def coverage_passages(
    source: tuple[int, ...],
    lengths: tuple[int, ...],
) -> tuple[tuple[tuple[int, ...], ...], list[tuple[int, int]]]:
    """Choose A passages solely to cover every plaintext class twice."""
    counts = Counter()
    used: list[tuple[int, int]] = []
    passages = []
    stride = 11
    for length in lengths:
        best: tuple[int, int, tuple[int, ...]] | None = None
        best_start: int | None = None
        for start in range(0, len(source) - length + 1, stride):
            interval = (start, start + length)
            if overlaps(interval, used):
                continue
            passage = source[start : start + length]
            local = Counter(passage)
            gain = sum(
                min(max(0, 2 - counts[value]), local[value])
                for value in range(42)
            )
            diversity = len(local)
            candidate = (gain, diversity, passage)
            if best is None or candidate[:2] > best[:2]:
                best = candidate
                best_start = start
        if best is None or best_start is None:
            raise RuntimeError("could not select a disjoint coverage passage")
        passage = best[2]
        passages.append(passage)
        counts.update(passage)
        used.append((best_start, best_start + length))
    return tuple(passages), used


def fixed_disjoint_passages(
    source: tuple[int, ...],
    lengths: tuple[int, ...],
    *,
    start: int,
    used: list[tuple[int, int]],
) -> tuple[tuple[int, ...], ...]:
    passages = []
    cursor = start
    for length in lengths:
        while overlaps((cursor, cursor + length), used):
            cursor += length + 97
        if cursor + length > len(source):
            raise RuntimeError("fixed plant passages exceed source")
        passages.append(source[cursor : cursor + length])
        used.append((cursor, cursor + length))
        cursor += length + 137
    return tuple(passages)


def plant_plaintexts(
    source: tuple[int, ...],
    lengths: dict[str, tuple[int, ...]],
) -> dict[str, tuple[tuple[int, ...], ...]]:
    group_a, used = coverage_passages(source, lengths["A"])
    group_b = fixed_disjoint_passages(
        source,
        lengths["B"],
        start=250_000,
        used=used,
    )
    group_c = fixed_disjoint_passages(
        source,
        lengths["C"],
        start=700_000,
        used=used,
    )
    return {"A": group_a, "B": group_b, "C": group_c}


def score_groups(
    streams: dict[str, tuple[tuple[int, ...], ...]],
    key: tuple[int, ...],
    model: TrigramModel42,
) -> tuple[float, float]:
    a_score, a_windows = trigram_score(streams["A"], key, model)
    heldout = streams["B"] + streams["C"]
    heldout_score, heldout_windows = trigram_score(heldout, key, model)
    return a_score / a_windows, heldout_score / heldout_windows


def run_control(
    training_text: str,
    plant_text: str,
    *,
    mode: str,
    restarts: int,
    iterations: int,
    start_temperature: float,
    end_temperature: float,
    seed: int,
) -> bool:
    real = load_cipher3()
    skip = int(mode == "body")
    lengths = {
        group: tuple(len(message) - skip for message in real[group])
        for group in ("A", "B", "C")
    }
    expected = plant_plaintexts(
        normalize_plaintext42(plant_text),
        lengths,
    )
    true_key = random_key(random.Random(seed ^ 0xC0117A))
    flat_expected = group_streams(expected, ("A", "B", "C"))
    flat_ciphertext = encode_streams(
        flat_expected,
        true_key,
        seed=seed ^ 0xE2C0DE,
    )
    ciphertext = {
        "A": flat_ciphertext[:6],
        "B": flat_ciphertext[6:12],
        "C": flat_ciphertext[12:],
    }
    model = TrigramModel42.train(training_text)
    result = optimize_key(
        ciphertext["A"],
        model,
        training_text,
        restarts=restarts,
        iterations=iterations,
        start_temperature=start_temperature,
        end_temperature=end_temperature,
        seed=seed,
    )
    decoded = {
        group: decode_streams(ciphertext[group], result.key)
        for group in ("A", "B", "C")
    }
    a_accuracy = event_accuracy(decoded["A"], expected["A"])
    heldout_accuracy = event_accuracy(
        decoded["B"] + decoded["C"],
        expected["B"] + expected["C"],
    )
    a_score, heldout_score = score_groups(ciphertext, result.key, model)
    print(
        f"CONTROL mode={mode} A_unique_raw="
        f"{len(set(value for message in ciphertext['A'] for value in message))}"
    )
    print(
        f"  score/window A={a_score:.6f} B+C={heldout_score:.6f}"
    )
    print(
        f"  accuracy A={a_accuracy:.6%} B+C={heldout_accuracy:.6%}"
    )
    print(f"  A0={render_streams(decoded['A'])[0]}")
    print(f"  B0={render_streams(decoded['B'])[0]}")
    return a_accuracy >= 0.80 and heldout_accuracy >= 0.60


def run_real(
    training_text: str,
    *,
    mode: str,
    restarts: int,
    iterations: int,
    start_temperature: float,
    end_temperature: float,
    seed: int,
) -> None:
    source = load_cipher3()
    skip = int(mode == "body")
    streams = {
        group: tuple(tuple(message[skip:]) for message in source[group])
        for group in ("A", "B", "C")
    }
    model = TrigramModel42.train(training_text)
    result = optimize_key(
        streams["A"],
        model,
        training_text,
        restarts=restarts,
        iterations=iterations,
        start_temperature=start_temperature,
        end_temperature=end_temperature,
        seed=seed,
    )
    a_score, heldout_score = score_groups(streams, result.key, model)
    decoded = {
        group: decode_streams(streams[group], result.key)
        for group in ("A", "B", "C")
    }
    print(f"REAL mode={mode}")
    print(
        f"  score/window A={a_score:.6f} B+C={heldout_score:.6f}"
    )
    for group in ("A", "B", "C"):
        print(f"  {group}0={render_streams(decoded[group])[0]}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--training",
        type=Path,
        default=Path("/private/tmp/pg1661.txt"),
    )
    parser.add_argument(
        "--plant",
        type=Path,
        default=Path("/private/tmp/pg2701.txt"),
    )
    parser.add_argument("--phase", choices=("control", "real"), default="control")
    parser.add_argument("--mode", choices=("full", "body", "both"), default="both")
    parser.add_argument("--restarts", type=int, default=4)
    parser.add_argument("--iterations", type=int, default=300_000)
    parser.add_argument("--start-temperature", type=float, default=18.0)
    parser.add_argument("--end-temperature", type=float, default=0.08)
    parser.add_argument("--seed", type=int, default=20260727)
    args = parser.parse_args()

    training_hash = file_sha256(args.training)
    plant_hash = file_sha256(args.plant)
    if training_hash != TRAINING_SHA256:
        raise SystemExit(f"unexpected training SHA-256: {training_hash}")
    if plant_hash != PLANT_SHA256:
        raise SystemExit(f"unexpected plant SHA-256: {plant_hash}")
    training_text = args.training.read_text(errors="ignore")
    plant_text = args.plant.read_text(errors="ignore")
    modes = ("full", "body") if args.mode == "both" else (args.mode,)

    if args.phase == "control":
        passed = []
        for mode in modes:
            passed.append(
                run_control(
                    training_text,
                    plant_text,
                    mode=mode,
                    restarts=args.restarts,
                    iterations=args.iterations,
                    start_temperature=args.start_temperature,
                    end_temperature=args.end_temperature,
                    seed=args.seed ^ (0 if mode == "full" else 0xB0D1),
                )
            )
        if not all(passed):
            raise SystemExit(2)
    else:
        for mode in modes:
            run_real(
                training_text,
                mode=mode,
                restarts=args.restarts,
                iterations=args.iterations,
                start_temperature=args.start_temperature,
                end_temperature=args.end_temperature,
                seed=args.seed ^ (0 if mode == "full" else 0xB0D1),
            )


if __name__ == "__main__":
    main()
