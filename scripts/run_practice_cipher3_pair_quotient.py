#!/usr/bin/env python3
"""Calibrate and run the frozen projective pair-quotient family."""

from __future__ import annotations

import argparse
import hashlib
import random
from collections import Counter
from pathlib import Path

from eye_mystery.practice_cipher3_pair_quotient import (
    ROUTES,
    EqualityPatternModel,
    PairArchitecture,
    PairRoute,
    decode_with_key,
    encode_pair_streams,
    pair_positions,
    quotient_pair_streams,
    search_pair_quotients,
)
from eye_mystery.practice_cipher3_two_sheet import (
    TwoSheetLanguageModel,
    language_score,
    render_plaintext,
)
from eye_mystery.practice_cipher3_wide import (
    load_cipher3,
    normalize_plaintext42,
)


TRAINING_SHA256 = "922e2a12ccb43a4c9544c260b2166c6ad2097aeb5957faeee113f173bb857cd0"
PLANT_SHA256 = "9a6844ac0703853720010787c7b6c70b0020f1ab1862dcd74452fa46474d1215"
CONTROL_ARCHITECTURES = (
    PairArchitecture(PairRoute(1, 1), 37, 19),
    PairArchitecture(PairRoute(2, 1), 29, 51),
)


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
    """Choose training passages solely to cover every class at least twice."""
    counts = Counter()
    used: list[tuple[int, int]] = []
    passages = []
    for length in lengths:
        best: tuple[int, int, tuple[int, ...]] | None = None
        best_start: int | None = None
        for start in range(0, len(source) - length + 1, 11):
            if overlaps((start, start + length), used):
                continue
            passage = source[start : start + length]
            local = Counter(passage)
            gain = sum(
                min(max(0, 2 - counts[value]), local[value])
                for value in range(42)
            )
            candidate = (gain, len(local), passage)
            if best is None or candidate[:2] > best[:2]:
                best = candidate
                best_start = start
        if best is None or best_start is None:
            raise RuntimeError("could not select a coverage passage")
        passages.append(best[2])
        counts.update(best[2])
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


def control_plaintexts(
    source: tuple[int, ...],
    raw_lengths: tuple[int, ...],
    route: PairRoute,
) -> tuple[tuple[int, ...], ...]:
    lengths = tuple(
        len(pair_positions(length, route))
        for length in raw_lengths
    )
    group_a, used = coverage_passages(source, lengths[:6])
    group_b = fixed_disjoint_passages(
        source,
        lengths[6:12],
        start=250_000,
        used=used,
    )
    group_c = fixed_disjoint_passages(
        source,
        lengths[12:],
        start=700_000,
        used=used,
    )
    return group_a + group_b + group_c


def flatten_real() -> tuple[tuple[int, ...], ...]:
    source = load_cipher3()
    return tuple(
        tuple(message)
        for group in ("A", "B", "C")
        for message in source[group]
    )


def format_architecture(architecture: PairArchitecture) -> str:
    return (
        f"route={architecture.route.stride}/{architecture.route.start} "
        f"slope={architecture.slope_label} "
        f"reflection={architecture.reflection}"
    )


def heldout_language_score(
    streams: tuple[tuple[int, ...], ...],
    architecture: PairArchitecture,
    key: tuple[int, ...],
    model: TwoSheetLanguageModel,
) -> float:
    score, windows = language_score(
        quotient_pair_streams(streams, architecture),
        key,
        model,
    )
    return score / windows


def route_aligned_accuracy(
    observed: tuple[tuple[int, ...], ...],
    expected: tuple[tuple[int, ...], ...],
    observed_architecture: PairArchitecture,
    expected_architecture: PairArchitecture,
) -> float:
    if (
        observed_architecture.slope != expected_architecture.slope
        or observed_architecture.reflection != expected_architecture.reflection
        or observed_architecture.route.stride
        != expected_architecture.route.stride
    ):
        return 0.0
    start_delta = (
        observed_architecture.route.start
        - expected_architecture.route.start
    )
    stride = expected_architecture.route.stride
    if start_delta % stride:
        return 0.0
    plaintext_shift = start_delta // stride
    correct = 0
    total = sum(map(len, expected))
    for observed_stream, expected_stream in zip(
        observed,
        expected,
        strict=True,
    ):
        for observed_index, value in enumerate(observed_stream):
            expected_index = observed_index + plaintext_shift
            if (
                expected_index in range(len(expected_stream))
                and value == expected_stream[expected_index]
            ):
                correct += 1
    return correct / total if total else 0.0


def run_control(
    raw_lengths: tuple[int, ...],
    plant_values: tuple[int, ...],
    equality_model: EqualityPatternModel,
    language_model: TwoSheetLanguageModel,
    *,
    structural_per_route: int,
    screen_iterations: int,
    refine_shortlist: int,
    refine_restarts: int,
    refine_iterations: int,
    seed: int,
) -> bool:
    passed = True
    for control_index, true_architecture in enumerate(CONTROL_ARCHITECTURES):
        expected = control_plaintexts(
            plant_values,
            raw_lengths,
            true_architecture.route,
        )
        rng = random.Random(seed ^ (0xC0110000 + control_index))
        true_key = list(range(42))
        rng.shuffle(true_key)
        ciphertexts = encode_pair_streams(
            expected,
            raw_lengths,
            true_architecture,
            true_key,
            seed=seed ^ (0xE2C00000 + control_index),
        )
        result = search_pair_quotients(
            ciphertexts[:6],
            equality_model,
            language_model,
            structural_per_route=structural_per_route,
            screen_iterations=screen_iterations,
            refine_shortlist=refine_shortlist,
            refine_restarts=refine_restarts,
            refine_iterations=refine_iterations,
            seed=seed ^ control_index,
        )
        true_global_rank = next(
            index
            for index, candidate in enumerate(result.screened, 1)
            if candidate.architecture == true_architecture
        )
        true_route_rank = next(
            index
            for index, candidate in enumerate(
                (
                    candidate
                    for candidate in result.screened
                    if candidate.architecture.route == true_architecture.route
                ),
                1,
            )
            if candidate.architecture == true_architecture
        )
        structural_retained = any(
            candidate.architecture == true_architecture
            for candidate in result.structural_selection
        )
        selected = result.best
        decoded_a = decode_with_key(
            quotient_pair_streams(ciphertexts[:6], selected.architecture),
            selected.key,
        )
        decoded_bc = decode_with_key(
            quotient_pair_streams(ciphertexts[6:], selected.architecture),
            selected.key,
        )
        a_accuracy = route_aligned_accuracy(
            decoded_a,
            expected[:6],
            selected.architecture,
            true_architecture,
        )
        bc_accuracy = route_aligned_accuracy(
            decoded_bc,
            expected[6:],
            selected.architecture,
            true_architecture,
        )
        bc_score = heldout_language_score(
            ciphertexts[6:],
            selected.architecture,
            selected.key,
            language_model,
        )
        print(f"CONTROL {control_index + 1}")
        print(f"  true     {format_architecture(true_architecture)}")
        print(f"  selected {format_architecture(selected.architecture)}")
        print(
            f"  true structural rank route={true_route_rank} "
            f"global={true_global_rank} retained={structural_retained}"
        )
        print(
            f"  score/window A={selected.score_per_window:.6f} "
            f"B+C={bc_score:.6f}"
        )
        print(
            f"  accuracy A={a_accuracy:.6%} B+C={bc_accuracy:.6%}"
        )
        print(f"  A0={render_plaintext(decoded_a[0])}")
        print(f"  B0={render_plaintext(decoded_bc[0])}")
        passed &= (
            structural_retained
            and a_accuracy >= 0.80
            and bc_accuracy >= 0.60
        )
    return passed


def run_real(
    streams: tuple[tuple[int, ...], ...],
    equality_model: EqualityPatternModel,
    language_model: TwoSheetLanguageModel,
    *,
    structural_per_route: int,
    screen_iterations: int,
    refine_shortlist: int,
    refine_restarts: int,
    refine_iterations: int,
    seed: int,
) -> None:
    result = search_pair_quotients(
        streams[:6],
        equality_model,
        language_model,
        structural_per_route=structural_per_route,
        screen_iterations=screen_iterations,
        refine_shortlist=refine_shortlist,
        refine_restarts=refine_restarts,
        refine_iterations=refine_iterations,
        seed=seed,
    )
    selected = result.best
    decoded = decode_with_key(
        quotient_pair_streams(streams, selected.architecture),
        selected.key,
    )
    bc_score = heldout_language_score(
        streams[6:],
        selected.architecture,
        selected.key,
        language_model,
    )
    print("REAL")
    print(f"  selected {format_architecture(selected.architecture)}")
    print(
        f"  score/window A={selected.score_per_window:.6f} "
        f"B+C={bc_score:.6f}"
    )
    print(
        "  structural top="
        + "; ".join(
            f"{format_architecture(candidate.architecture)}:"
            f"{candidate.score_per_window:.6f}"
            for candidate in result.screened[:5]
        )
    )
    print(f"  A0={render_plaintext(decoded[0])}")
    print(f"  B0={render_plaintext(decoded[6])}")
    print(f"  C0={render_plaintext(decoded[12])}")


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
    parser.add_argument("--pattern-width", type=int, default=6)
    parser.add_argument("--structural-per-route", type=int, default=12)
    parser.add_argument("--screen-iterations", type=int, default=20_000)
    parser.add_argument("--refine-shortlist", type=int, default=8)
    parser.add_argument("--refine-restarts", type=int, default=4)
    parser.add_argument("--refine-iterations", type=int, default=120_000)
    parser.add_argument("--seed", type=int, default=20260727)
    args = parser.parse_args()

    training_hash = file_sha256(args.training)
    plant_hash = file_sha256(args.plant)
    if training_hash != TRAINING_SHA256:
        raise SystemExit(f"unexpected training SHA-256: {training_hash}")
    if plant_hash != PLANT_SHA256:
        raise SystemExit(f"unexpected plant SHA-256: {plant_hash}")
    training_text = args.training.read_text(errors="ignore")
    plant_values = normalize_plaintext42(
        args.plant.read_text(errors="ignore")
    )
    equality_model = EqualityPatternModel.train(
        training_text,
        width=args.pattern_width,
    )
    language_model = TwoSheetLanguageModel.train(training_text)
    streams = flatten_real()
    raw_lengths = tuple(map(len, streams))

    kwargs = {
        "structural_per_route": args.structural_per_route,
        "screen_iterations": args.screen_iterations,
        "refine_shortlist": args.refine_shortlist,
        "refine_restarts": args.refine_restarts,
        "refine_iterations": args.refine_iterations,
        "seed": args.seed,
    }
    if args.phase == "control":
        if not run_control(
            raw_lengths,
            plant_values,
            equality_model,
            language_model,
            **kwargs,
        ):
            raise SystemExit(2)
    else:
        run_real(
            streams,
            equality_model,
            language_model,
            **kwargs,
        )


if __name__ == "__main__":
    main()
