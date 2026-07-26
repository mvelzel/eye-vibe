#!/usr/bin/env python3
"""Run a word-constrained cyclic-GAK search on sdlwdr cipher #4."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from eye_mystery.practice_cipher4 import cyclic_differences
from eye_mystery.practice_cipher4_words import (
    NATURAL_42,
    SymbolModel,
    WordTrie,
    encode_word_gak,
    render_symbols,
    word_constrained_gak_beam,
)


ROOT = Path(__file__).resolve().parents[1]


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
    parser.add_argument("--portion", type=int, choices=(1, 2, 3), default=2)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--length", type=int, default=200)
    parser.add_argument("--beam", type=int, default=250_000)
    parser.add_argument("--order", type=int, default=6)
    parser.add_argument(
        "--alphabet",
        choices=("compact27", "natural27", "natural32", "natural42"),
        default="natural32",
    )
    parser.add_argument(
        "--word-list",
        type=Path,
        default=Path("/usr/share/dict/words"),
    )
    parser.add_argument("--ciphertext-sign", type=int, choices=(-1, 1), default=1)
    parser.add_argument("--plaintext-sign", type=int, choices=(-1, 1), default=1)
    parser.add_argument("--key-on-next", action="store_true")
    parser.add_argument("--matched-control", action="store_true")
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    corpus = args.corpus.read_text(errors="ignore")
    if args.alphabet == "compact27":
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
        positions = tuple(range(27))
    elif args.alphabet == "natural27":
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
        positions = tuple(range(26)) + (36,)
    elif args.alphabet == "natural32":
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ .-'?!"
        positions = tuple(range(26)) + tuple(range(36, 42))
    else:
        alphabet = NATURAL_42
        positions = tuple(range(42))
    space_code = alphabet.index(" ")
    punctuation_codes = tuple(
        alphabet.index(character)
        for character in ".-'?!"
        if character in alphabet
    )
    digit_codes = tuple(
        alphabet.index(character)
        for character in "0123456789"
        if character in alphabet
    )
    word_training = corpus
    if args.word_list.exists():
        word_training += "\n" + args.word_list.read_text(errors="ignore")
    target = None
    if args.matched_control:
        if args.alphabet == "natural42":
            sentence = (
                "CODE 0123456789. THE QUICK-BROWN FOX'S PUZZLE IS HARD? YES! "
                "THEN ANOTHER CURIOUS DOG WATCHES FROM THE GARDEN AND RESTS."
            )
        elif args.alphabet == "natural32":
            sentence = (
                "THE QUICK-BROWN FOX'S PUZZLE IS HARD? YES! THEN ANOTHER "
                "CURIOUS DOG WATCHES FROM THE GARDEN AND RESTS."
            )
        else:
            sentence = (
                "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG AND THEN THE QUICK "
                "FOX RESTS WHILE ANOTHER CURIOUS DOG WATCHES FROM THE GARDEN"
            )
        target = bytes(alphabet.index(character) for character in sentence)
        key = tuple((17 * index + 9) % 83 for index in range(len(positions)))
        differences = encode_word_gak(target, key, positions)
        training = corpus + "\n" + (sentence + "\n") * 100
        word_training += "\n" + (sentence + "\n") * 100
    else:
        messages = json.loads(args.data.read_text())
        stream = cyclic_differences(messages[args.portion - 1])
        differences = stream[args.start : args.start + args.length]
        training = corpus

    result = word_constrained_gak_beam(
        differences,
        WordTrie.train(word_training),
        SymbolModel.train(training, alphabet, order=args.order),
        space_position=positions[space_code],
        beam_width=args.beam,
        ciphertext_sign=args.ciphertext_sign,
        plaintext_sign=args.plaintext_sign,
        key_on_next=args.key_on_next,
        plaintext_positions=positions,
        space_code=space_code,
        punctuation_codes=punctuation_codes,
        digit_codes=digit_codes,
    )
    print(
        f"completed={result.completed}/{len(differences)} "
        f"survivors={len(result.candidates)} "
        f"generated_max={max(result.generated_by_step, default=0)}"
    )
    if target is not None:
        target_ranks = [
            index
            for index, candidate in enumerate(result.candidates)
            if candidate.plaintext == target
        ]
        print(f"target_rank={target_ranks[:1]}")
        print(f"target={render_symbols(target, alphabet)}")
    for candidate in result.candidates[: args.top]:
        print(
            f"{candidate.score:12.2f} "
            f"{render_symbols(candidate.plaintext, alphabet)}"
        )
        print(
            "key",
            tuple(
                None if value == 255 else value
                for value in candidate.key
            ),
        )


if __name__ == "__main__":
    main()
