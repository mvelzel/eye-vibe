#!/usr/bin/env python3
"""Run the packed nonlinear-GAK beam on Cipher 4's 200-action common block."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from eye_mystery.practice_cipher4 import cyclic_differences
from eye_mystery.practice_cipher4_gak import (
    CharacterModel,
    encode_nonlinear_gak,
    nonlinear_gak_beam,
    normalize_language,
    render_plaintext,
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
    parser.add_argument("--beam", type=int, default=250_000)
    parser.add_argument("--order", type=int, default=6)
    parser.add_argument(
        "--space-position", type=int, choices=(26, 36), default=36
    )
    parser.add_argument("--ciphertext-sign", type=int, choices=(-1, 1), default=1)
    parser.add_argument("--plaintext-sign", type=int, choices=(-1, 1), default=1)
    parser.add_argument("--key-on-next", action="store_true")
    parser.add_argument(
        "--matched-control",
        action="store_true",
        help="replace the real block by a 201-character natural-English plant",
    )
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    messages = json.loads(args.data.read_text())
    corpus = args.corpus.read_text(errors="ignore")
    target = None
    if args.matched_control:
        target = bytes(normalize_language(corpus)[20_000:20_201])
        differences = encode_nonlinear_gak(
            target,
            tuple((17 * index + 9) % 83 for index in range(27)),
            space_position=args.space_position,
            ciphertext_sign=args.ciphertext_sign,
            plaintext_sign=args.plaintext_sign,
        )
    else:
        differences = cyclic_differences(messages[1])[5:205]
    model = CharacterModel.train(corpus, order=args.order)
    result = nonlinear_gak_beam(
        differences,
        model,
        space_position=args.space_position,
        beam_width=args.beam,
        ciphertext_sign=args.ciphertext_sign,
        plaintext_sign=args.plaintext_sign,
        key_on_next=args.key_on_next,
    )
    print(
        f"completed={result.completed}/{len(differences)} "
        f"survivors={len(result.candidates)}"
    )
    if target is not None:
        target_ranks = [
            index
            for index, candidate in enumerate(result.candidates)
            if candidate.plaintext == target
        ]
        print(f"target_rank={target_ranks[:1]}")
        print(f"target={render_plaintext(target)}")
    for candidate in result.candidates[: args.top]:
        print(f"{candidate.score:12.2f} {render_plaintext(candidate.plaintext)}")
        print("key", tuple(None if value == 255 else value for value in candidate.key))


if __name__ == "__main__":
    main()
