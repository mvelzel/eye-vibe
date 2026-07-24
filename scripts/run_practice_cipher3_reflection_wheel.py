#!/usr/bin/env python3
"""Run the planted and real hidden-reflection-wheel screens for Cipher 3."""

from __future__ import annotations

import argparse
from pathlib import Path
import random

from eye_mystery.practice_cipher3_reflection import (
    ReflectionLanguageModel,
    ReflectionWheelAnnealer,
    encode_reflection_messages,
    recovered_wheel_insertions,
    reciprocal_audit,
    render_plaintext,
    scan_recovered_wheel_insertions,
    wheel_dihedral_match,
)
from eye_mystery.practice_cipher3_wide import (
    GROUPS,
    load_cipher3,
    normalize_plaintext42,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--english-corpus",
        type=Path,
        default=Path("/private/tmp/kalevala-crawford.txt"),
    )
    parser.add_argument("--restarts", type=int, default=8)
    parser.add_argument("--iterations", type=int, default=500_000)
    parser.add_argument("--temperature", type=float, default=60.0)
    parser.add_argument(
        "--skip-joint",
        action="store_true",
        help="run only the requested fixed-coordinate scans",
    )
    parser.add_argument("--seed", type=int, default=0x53444C5744520301)
    parser.add_argument("--control-offset", type=int, default=20_000)
    parser.add_argument(
        "--fixed-scan",
        action="store_true",
        help="exhaust both orientations and all old-wheel J insertions",
    )
    parser.add_argument("--fixed-iterations", type=int, default=5_000)
    parser.add_argument(
        "--standard-scan",
        action="store_true",
        help="hold the displayed 0..82 wheel fixed and optimize only its key",
    )
    parser.add_argument(
        "--mode",
        choices=("control", "real", "both"),
        default="both",
    )
    args = parser.parse_args()

    text = args.english_corpus.read_text(errors="ignore")
    model = ReflectionLanguageModel.train(text)
    real_by_group = load_cipher3()
    real = tuple(
        message
        for group in GROUPS
        for message in real_by_group[group]
    )
    print("one-direction reciprocal audit", reciprocal_audit(real_by_group))

    if args.mode in ("control", "both"):
        normalized = normalize_plaintext42(text)
        lengths = tuple(len(message) - 1 for message in real)
        required = sum(lengths)
        flat = normalized[
            args.control_offset : args.control_offset + required
        ]
        if len(flat) != required:
            raise ValueError("control corpus is too short")
        plaintexts = []
        cursor = 0
        for length in lengths:
            plaintexts.append(tuple(flat[cursor : cursor + length]))
            cursor += length
        used = sorted(set(flat))
        if len(used) > 41:
            raise ValueError("control plaintext uses more than 41 symbols")
        rng = random.Random(args.seed ^ 0xC0117A01)
        wheel = list(range(83))
        rng.shuffle(wheel)
        magnitudes = list(range(1, 42))
        rng.shuffle(magnitudes)
        plaintext_to_magnitude = dict(zip(used, magnitudes, strict=False))
        control = encode_reflection_messages(
            plaintexts,
            wheel,
            plaintext_to_magnitude,
            seed=args.seed ^ 0xD1EEC710,
        )
        expected_coordinates = [0] * 83
        for position, card in enumerate(wheel):
            expected_coordinates[card] = position
        if not args.skip_joint:
            print("planted control")
            result = ReflectionWheelAnnealer(control, model).run(
                restarts=args.restarts,
                iterations=args.iterations,
                seed=args.seed,
                start_temperature=args.temperature,
            )
            correct = sum(
                observed == expected
                for observed_message, expected_message in zip(
                    result.plaintexts,
                    plaintexts,
                    strict=True,
                )
                for observed, expected in zip(
                    observed_message,
                    expected_message,
                    strict=True,
                )
            )
            print(
                f"  score/trigram={result.score_per_trigram:.6f}; "
                f"accuracy={correct / required:.6%}; "
                f"dihedral-wheel={wheel_dihedral_match(result.coordinates, expected_coordinates)}"
            )
            for plaintext in result.plaintexts[:6]:
                print(" ", render_plaintext(plaintext[:120]))
        if args.standard_scan:
            print("standard-wheel planted control")
            standard_control = encode_reflection_messages(
                plaintexts,
                tuple(range(83)),
                plaintext_to_magnitude,
                seed=args.seed ^ 0x57A0D,
            )
            standard = ReflectionWheelAnnealer(
                standard_control,
                model,
            ).run(
                restarts=args.restarts,
                iterations=args.fixed_iterations,
                seed=args.seed ^ 0x57A0D,
                start_temperature=20.0,
                coordinate_move_probability=0.0,
                initial_coordinates=tuple(range(83)),
            )
            correct = sum(
                observed == expected
                for observed_message, expected_message in zip(
                    standard.plaintexts,
                    plaintexts,
                    strict=True,
                )
                for observed, expected in zip(
                    observed_message,
                    expected_message,
                    strict=True,
                )
            )
            print(
                f"  score/trigram={standard.score_per_trigram:.6f}; "
                f"accuracy={correct / required:.6%}"
            )
        if args.fixed_scan:
            print("fixed old-wheel planted control")
            fixed_name, _fixed_coordinates, fixed_wheel = (
                recovered_wheel_insertions()[17]
            )
            fixed_control = encode_reflection_messages(
                plaintexts,
                fixed_wheel,
                plaintext_to_magnitude,
                seed=args.seed ^ 0xF17ED,
            )
            scores = scan_recovered_wheel_insertions(
                fixed_control,
                model,
                iterations=args.fixed_iterations,
                seed=args.seed ^ 0xF17E,
            )
            for score in scores[:10]:
                correct = sum(
                    observed == expected
                    for observed_message, expected_message in zip(
                        score.result.plaintexts,
                        plaintexts,
                        strict=True,
                    )
                    for observed, expected in zip(
                        observed_message,
                        expected_message,
                        strict=True,
                    )
                )
                print(
                    f"  {score.name} "
                    f"{score.result.score_per_trigram:.6f} "
                    f"accuracy={correct / required:.6%}"
                )
            print(f"  planted={fixed_name}")

    if args.mode in ("real", "both"):
        if not args.skip_joint:
            print("real corpus")
            result = ReflectionWheelAnnealer(real, model).run(
                restarts=args.restarts,
                iterations=args.iterations,
                seed=args.seed ^ 0x5EA1,
                start_temperature=args.temperature,
            )
            print(f"  score/trigram={result.score_per_trigram:.6f}")
            for plaintext in result.plaintexts:
                print(" ", render_plaintext(plaintext[:240]))
        if args.standard_scan:
            print("real standard-wheel scan")
            standard = ReflectionWheelAnnealer(real, model).run(
                restarts=args.restarts,
                iterations=args.fixed_iterations,
                seed=args.seed ^ 0x57A0D5EA1,
                start_temperature=20.0,
                coordinate_move_probability=0.0,
                initial_coordinates=tuple(range(83)),
            )
            print(
                f"  score/trigram={standard.score_per_trigram:.6f}"
            )
            for plaintext in standard.plaintexts:
                print(" ", render_plaintext(plaintext[:240]))
        if args.fixed_scan:
            print("real fixed old-wheel scan")
            scores = scan_recovered_wheel_insertions(
                real,
                model,
                iterations=args.fixed_iterations,
                seed=args.seed ^ 0xF17E5EA1,
            )
            for score in scores[:10]:
                print(
                    f"  {score.name} "
                    f"{score.result.score_per_trigram:.6f} "
                    f"{render_plaintext(score.result.plaintexts[0][:120])}"
                )


if __name__ == "__main__":
    main()
