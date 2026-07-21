#!/usr/bin/env python3
"""Try to read the affine-walk candidate as alternating substitutions."""

from __future__ import annotations

import argparse
import random
from collections import Counter
from pathlib import Path
from urllib.request import Request, urlopen

from eye_mystery.affine_walk import trace_affine_walk
from eye_mystery.alternating_substitution import solve
from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER
from eye_mystery.corpus import trigram_values
from eye_mystery.language_null import prefix_tree_parity_shuffle
from eye_mystery.mono_substitution import solve_mono_substitution
from eye_mystery.ngram import TetragramModel, ascii_letters


def parse_order(value: str) -> tuple[int, int, int]:
    if sorted(value) != ["1", "2", "3"]:
        raise argparse.ArgumentTypeError("order must be a permutation of 123")
    return tuple(int(digit) - 1 for digit in value)  # type: ignore[return-value]


def main() -> None:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--language-corpus", type=Path)
    source.add_argument("--language-corpus-url", action="append")
    finnish = parser.add_mutually_exclusive_group()
    finnish.add_argument("--transliterate-finnish", action="store_true")
    finnish.add_argument(
        "--encode-finnish-diacritics",
        action="store_true",
        help="train with Q/X/Z placeholders for Finnish ä/ö/å",
    )
    parser.add_argument("--generator", type=int, default=1)
    parser.add_argument("--translation-pair", type=int, nargs=2, default=(1, 3))
    parser.add_argument(
        "--center-mode",
        choices=("identity", "negation", "inversion", "reflection"),
        default="negation",
    )
    parser.add_argument("--up-order", type=parse_order, default=parse_order("123"))
    parser.add_argument("--down-order", type=parse_order, default=parse_order("312"))
    parser.add_argument("--monoalphabetic", action="store_true")
    parser.add_argument(
        "--homophonic-output",
        action="store_true",
        help="allow multiple walk states to decode to the same letter",
    )
    parser.add_argument(
        "--frequency-weight",
        type=float,
        default=1.0,
        help="chi-square weight for corpus frequencies in homophonic mode",
    )
    parser.add_argument(
        "--omit-markers",
        action="store_true",
        help="remove the first trigram and reset before tracing each body",
    )
    parser.add_argument("--restarts", type=int, default=12)
    parser.add_argument("--iterations", type=int, default=150_000)
    parser.add_argument("--seed", type=int, default=20260720)
    parser.add_argument("--null-trials", type=int, default=0)
    parser.add_argument("--null-restarts", type=int, default=4)
    parser.add_argument("--null-iterations", type=int, default=60_000)
    parser.add_argument(
        "--null-mode",
        choices=("independent", "prefix-tree"),
        default="prefix-tree",
    )
    args = parser.parse_args()

    if args.language_corpus is not None:
        corpus_text = args.language_corpus.read_text(errors="ignore")
    else:
        corpus_parts = []
        for url in args.language_corpus_url:
            request = Request(
                url,
                headers={"User-Agent": "Noita-eye-mystery research"},
            )
            corpus_parts.append(
                urlopen(request, timeout=60).read().decode(
                    "utf-8", errors="ignore"
                )
            )
        corpus_text = "\n".join(corpus_parts)
    if args.transliterate_finnish:
        corpus_text = corpus_text.translate(
            str.maketrans(
                {
                    "ä": "a",
                    "ö": "o",
                    "å": "a",
                    "Ä": "A",
                    "Ö": "O",
                    "Å": "A",
                }
            )
        )
    elif args.encode_finnish_diacritics:
        corpus_text = corpus_text.translate(
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
    model = TetragramModel.train(corpus_text)
    corpus_letters = ascii_letters(corpus_text)
    letter_counts = Counter(corpus_letters)
    frequency_total = len(corpus_letters) + 26
    target_frequencies = tuple(
        (letter_counts[letter] + 1) / frequency_total
        for letter in range(26)
    )
    streams = tuple(
        trace_affine_walk(
            MESSAGES[name][3:] if args.omit_markers else MESSAGES[name],
            generator=args.generator,
            translation_pair=tuple(args.translation_pair),
            center_mode=args.center_mode,
            up_order=args.up_order,
            down_order=args.down_order,
        )
        for name in MESSAGE_ORDER
    )
    solver = solve_mono_substitution if args.monoalphabetic else solve

    def run_solver(
        input_streams: tuple[tuple[int, ...], ...],
        *,
        restarts: int,
        iterations: int,
        seed: int,
    ):
        return solver(
            input_streams,
            model,
            restarts=restarts,
            iterations=iterations,
            seed=seed,
            injective=not args.homophonic_output,
            target_frequencies=(
                target_frequencies if args.homophonic_output else None
            ),
            frequency_weight=(
                args.frequency_weight if args.homophonic_output else 0.0
            ),
        )

    result = run_solver(
        streams,
        restarts=args.restarts,
        iterations=args.iterations,
        seed=args.seed,
    )
    windows = sum(max(0, len(stream) - 3) for stream in streams)
    reference = ascii_letters(corpus_text)[-sum(map(len, streams)) :]
    reference_score = model.score(reference) / max(1, len(reference) - 3)
    print(f"candidate log score per tetragram: {result.score / windows:.4f}")
    print(f"in-corpus reference score:         {reference_score:.4f}")
    print(f"distinct walk states:              {len(set().union(*map(set, streams)))}")
    print(
        "substitution alphabets:           "
        f"{'one' if args.monoalphabetic else 'alternating'} "
        f"({'homophonic' if args.homophonic_output else 'injective'})"
    )
    print(f"marker handling:                  {'omit/reset' if args.omit_markers else 'full'}")
    print()
    display_table = (
        str.maketrans({"Q": "Ä", "X": "Ö", "Z": "Å"})
        if args.encode_finnish_diacritics
        else None
    )
    for name, plaintext in zip(MESSAGE_ORDER, result.plaintexts):
        if display_table is not None:
            plaintext = plaintext.translate(display_table)
        print(f"{name:>5}: {plaintext}")
    if args.null_trials:
        print()
        print(f"{args.null_mode} parity-shuffle null scores:")
        rng = random.Random(args.seed + 1)
        reference_streams = {
            name: trigram_values(MESSAGES[name])[1 if args.omit_markers else 0 :]
            for name in MESSAGE_ORDER
        }
        for trial in range(args.null_trials):
            if args.null_mode == "prefix-tree":
                shuffled = prefix_tree_parity_shuffle(
                    dict(zip(MESSAGE_ORDER, streams, strict=True)),
                    reference_streams,
                    rng,
                    start=0 if args.omit_markers else 1,
                )
                shuffled_streams = [shuffled[name] for name in MESSAGE_ORDER]
            else:
                shuffled_streams = []
                for stream in streams:
                    shuffled_stream = list(stream)
                    for parity in (0, 1):
                        values = shuffled_stream[parity::2]
                        rng.shuffle(values)
                        shuffled_stream[parity::2] = values
                    shuffled_streams.append(tuple(shuffled_stream))
            null_result = run_solver(
                tuple(shuffled_streams),
                restarts=args.null_restarts,
                iterations=args.null_iterations,
                seed=args.seed + 10_000 + trial,
            )
            print(f"  {trial + 1}: {null_result.score / windows:.4f}")


if __name__ == "__main__":
    main()
