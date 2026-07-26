#!/usr/bin/env python3
"""Run the planted and real affine two-sheet Cipher 3 audit."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from eye_mystery.practice_cipher3_two_sheet import (
    TwoSheetLanguageModel,
    decode_with_key,
    encode_two_sheet,
    flatten_groups,
    language_score,
    quotient_streams,
    render_plaintext,
    search_reflections,
)
from eye_mystery.practice_cipher3_wide import (
    load_cipher3,
    normalize_plaintext42,
)


def split_plaintexts(
    values: tuple[int, ...],
    lengths: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    required = sum(lengths)
    if len(values) < required:
        raise ValueError("control corpus is too short")
    output = []
    cursor = 0
    for length in lengths:
        output.append(tuple(values[cursor : cursor + length]))
        cursor += length
    return tuple(output)


def accuracy(
    observed: tuple[tuple[int, ...], ...],
    expected: tuple[tuple[int, ...], ...],
) -> float:
    correct = sum(
        left == right
        for observed_stream, expected_stream in zip(
            observed,
            expected,
            strict=True,
        )
        for left, right in zip(
            observed_stream,
            expected_stream,
            strict=True,
        )
    )
    return correct / sum(map(len, expected))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--language-corpus",
        type=Path,
        default=Path("/private/tmp/cipher3-kalevala-crawford.txt"),
    )
    parser.add_argument("--mode", choices=("full", "body", "both"), default="both")
    parser.add_argument("--screen-iterations", type=int, default=10_000)
    parser.add_argument("--refine-iterations", type=int, default=80_000)
    parser.add_argument("--refine-restarts", type=int, default=4)
    parser.add_argument("--shortlist", type=int, default=6)
    parser.add_argument("--seed", type=int, default=0xC3A2)
    args = parser.parse_args()

    corpus = args.language_corpus.read_text(errors="ignore")
    split = len(corpus) * 2 // 3
    model = TwoSheetLanguageModel.train(corpus[:split])
    control_values = normalize_plaintext42(corpus[split:])
    streams = load_cipher3()
    modes = ("full", "body") if args.mode == "both" else (args.mode,)

    for mode_index, mode in enumerate(modes):
        body = mode == "body"
        real_a = flatten_groups(streams, ("A",), body=body)
        real_bc = flatten_groups(streams, ("B", "C"), body=body)
        all_lengths = tuple(
            map(
                len,
                flatten_groups(streams, ("A", "B", "C"), body=body),
            )
        )
        control_plaintexts = split_plaintexts(control_values, all_lengths)
        control_a = control_plaintexts[:6]
        control_bc = control_plaintexts[6:]
        rng = random.Random(args.seed ^ (0xB0D1 if body else 0xF011))
        planted_reflection = 37
        planted_key = list(range(42))
        rng.shuffle(planted_key)
        control_ciphertexts = encode_two_sheet(
            control_plaintexts,
            planted_reflection,
            planted_key,
            seed=args.seed ^ (0xC011 + mode_index),
        )

        print(f"{mode} planted control")
        control_best, control_screen = search_reflections(
            control_ciphertexts[:6],
            model,
            screen_iterations=args.screen_iterations,
            refine_iterations=args.refine_iterations,
            refine_restarts=args.refine_restarts,
            shortlist=args.shortlist,
            seed=args.seed ^ (0x100000 + mode_index),
        )
        control_decoded_a = decode_with_key(
            quotient_streams(
                control_ciphertexts[:6],
                control_best.reflection,
            ),
            control_best.key,
        )
        control_decoded_bc = decode_with_key(
            quotient_streams(
                control_ciphertexts[6:],
                control_best.reflection,
            ),
            control_best.key,
        )
        control_bc_score, control_bc_windows = language_score(
            quotient_streams(
                control_ciphertexts[6:],
                control_best.reflection,
            ),
            control_best.key,
            model,
        )
        print(
            f"  planted={planted_reflection} selected={control_best.reflection} "
            f"screen-rank="
            f"{next(index for index, result in enumerate(control_screen, 1) if result.reflection == planted_reflection)} "
            f"A-score={control_best.score_per_window:.6f} "
            f"A-accuracy={accuracy(control_decoded_a, control_a):.6%}"
        )
        print(
            f"  BC-score={control_bc_score / control_bc_windows:.6f} "
            f"BC-accuracy={accuracy(control_decoded_bc, control_bc):.6%}"
        )
        print(f"  first={render_plaintext(control_decoded_a[0][:100])}")

        print(f"{mode} real corpus")
        real_best, real_screen = search_reflections(
            real_a,
            model,
            screen_iterations=args.screen_iterations,
            refine_iterations=args.refine_iterations,
            refine_restarts=args.refine_restarts,
            shortlist=args.shortlist,
            seed=args.seed ^ (0x200000 + mode_index),
        )
        real_decoded_a = decode_with_key(
            quotient_streams(real_a, real_best.reflection),
            real_best.key,
        )
        real_decoded_bc = decode_with_key(
            quotient_streams(real_bc, real_best.reflection),
            real_best.key,
        )
        real_bc_score, real_bc_windows = language_score(
            quotient_streams(real_bc, real_best.reflection),
            real_best.key,
            model,
        )
        print(
            f"  selected={real_best.reflection} "
            f"A-score={real_best.score_per_window:.6f} "
            f"screen-next="
            f"{','.join(str(result.reflection) for result in real_screen[:5])}"
        )
        print(f"  BC-score={real_bc_score / real_bc_windows:.6f}")
        print(f"  A-first={render_plaintext(real_decoded_a[0][:100])}")
        print(f"  B-first={render_plaintext(real_decoded_bc[0][:100])}")


if __name__ == "__main__":
    main()
