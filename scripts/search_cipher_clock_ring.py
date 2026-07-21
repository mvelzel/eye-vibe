#!/usr/bin/env python3
"""Scan affine output disks for Aki's public 114-position input ring."""

from __future__ import annotations

import argparse
import heapq
from dataclasses import dataclass
from pathlib import Path

from eye_mystery.cipher_clock import (
    AKI_DISK_INPUT_RING,
    affine_output_positions,
    wadsworth_decode,
)
from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.ngram import TetragramModel, ascii_letters


@dataclass(frozen=True)
class Candidate:
    score: float
    multiplier: int
    offset: int
    plaintexts: tuple[str, ...]


def normalized_finnish(text: str) -> str:
    return text.translate(
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


def score_plaintexts(
    model: TetragramModel, plaintexts: tuple[str, ...]
) -> float:
    score = 0.0
    windows = 0
    for plaintext in plaintexts:
        letters = ascii_letters(plaintext)
        score += model.score(letters)
        windows += max(0, len(letters) - 3)
    return score / max(1, windows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language-corpus", type=Path, required=True)
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args()

    corpus = normalized_finnish(
        args.language_corpus.read_text(errors="ignore")
    )
    model = TetragramModel.train(corpus)
    corpus_letters = ascii_letters(corpus)
    reference_score = model.score(corpus_letters) / (len(corpus_letters) - 3)
    messages = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    print("input-ring positions:", len(AKI_DISK_INPUT_RING))
    print("input-ring symbols:", len(set(AKI_DISK_INPUT_RING)))
    print("corpus self-score:", f"{reference_score:.4f}")

    for omit_marker in (False, True):
        best: list[tuple[float, int, Candidate]] = []
        serial = 0
        for multiplier in range(1, 83):
            for offset in range(83):
                try:
                    positions = affine_output_positions(
                        83, multiplier, offset
                    )
                except ValueError:
                    continue
                plaintexts = tuple(
                    wadsworth_decode(
                        messages[name][1 if omit_marker else 0 :],
                        AKI_DISK_INPUT_RING,
                        positions,
                    )
                    for name in MESSAGE_ORDER
                )
                candidate = Candidate(
                    score_plaintexts(model, plaintexts),
                    multiplier,
                    offset,
                    plaintexts,
                )
                item = (candidate.score, serial, candidate)
                serial += 1
                if len(best) < args.top:
                    heapq.heappush(best, item)
                elif item > best[0]:
                    heapq.heapreplace(best, item)
        print()
        print("mode:", "body" if omit_marker else "full")
        print("candidates:", serial)
        for _, _, candidate in sorted(best, reverse=True):
            previews = " / ".join(
                plaintext[:60] for plaintext in candidate.plaintexts
            )
            print(
                f"  score={candidate.score:.4f} "
                f"a={candidate.multiplier} b={candidate.offset}: "
                f"{previews}"
            )


if __name__ == "__main__":
    main()
