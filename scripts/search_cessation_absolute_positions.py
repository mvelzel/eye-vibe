#!/usr/bin/env python3
"""Read Eye trigrams as cursor positions on Cessation-style text rings."""

from __future__ import annotations

import argparse
import heapq
from dataclasses import dataclass
from pathlib import Path
from urllib.request import Request, urlopen

from eye_mystery.cipher_clock import affine_output_positions, wadsworth_decode
from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.ngram import TetragramModel, ascii_letters


RINGS = {
    "noita-keyed-26": "bdmagickefhjlnopqrstuvwxyz",
    "finnish-29": "abcdefghijklmnopqrstuvwxyzåäö",
}


@dataclass(frozen=True)
class Candidate:
    score: float
    ring_name: str
    reversed_ring: bool
    multiplier: int
    offset: int
    omit_markers: bool
    plaintexts: tuple[str, ...]


def normalize_finnish(text: str) -> str:
    return text.translate(
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


def load_corpus(paths: list[Path], urls: list[str]) -> str:
    parts = [path.read_text(errors="ignore") for path in paths]
    for url in urls:
        request = Request(url, headers={"User-Agent": "Noita-eye-mystery research"})
        parts.append(
            urlopen(request, timeout=60).read().decode("utf-8", errors="ignore")
        )
    return "\n".join(parts)


def score_plaintexts(model: TetragramModel, plaintexts: tuple[str, ...]) -> float:
    score = 0.0
    windows = 0
    for plaintext in plaintexts:
        letters = ascii_letters(normalize_finnish(plaintext))
        score += model.score(letters)
        windows += max(0, len(letters) - 3)
    return score / max(1, windows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language-corpus", type=Path, action="append", default=[])
    parser.add_argument("--language-corpus-url", action="append", default=[])
    parser.add_argument("--ring", action="append", choices=tuple(RINGS))
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument(
        "--numeric-only",
        action="store_true",
        help="test only the accepted numeric output order and its rotations",
    )
    args = parser.parse_args()
    if not args.language_corpus and not args.language_corpus_url:
        raise SystemExit("provide at least one Finnish language corpus")

    corpus = normalize_finnish(
        load_corpus(args.language_corpus, args.language_corpus_url)
    )
    model = TetragramModel.train(corpus)
    messages = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    ring_names = tuple(args.ring or RINGS)
    best = []
    serial = 0
    multipliers = (1,) if args.numeric_only else range(1, 83)
    for ring_name in ring_names:
        for reversed_ring in (False, True):
            ring = RINGS[ring_name]
            if reversed_ring:
                ring = ring[::-1]
            for multiplier in multipliers:
                for offset in range(83):
                    try:
                        positions = affine_output_positions(83, multiplier, offset)
                    except ValueError:
                        continue
                    for omit_markers in (False, True):
                        plaintexts = tuple(
                            wadsworth_decode(
                                messages[name][1 if omit_markers else 0 :],
                                ring,
                                positions,
                            )
                            for name in MESSAGE_ORDER
                        )
                        candidate = Candidate(
                            score_plaintexts(model, plaintexts),
                            ring_name,
                            reversed_ring,
                            multiplier,
                            offset,
                            omit_markers,
                            plaintexts,
                        )
                        item = (candidate.score, serial, candidate)
                        serial += 1
                        if len(best) < args.top:
                            heapq.heappush(best, item)
                        elif item > best[0]:
                            heapq.heapreplace(best, item)

    corpus_letters = ascii_letters(corpus)
    reference = corpus_letters[-1036:]
    reference_score = model.score(reference) / max(1, len(reference) - 3)
    print("corpus reference:", f"{reference_score:.4f}")
    print("candidates:", serial)
    display = str.maketrans({"q": "ä", "x": "ö", "z": "å"})
    for _, _, candidate in sorted(best, reverse=True):
        preview = " / ".join(text[:80] for text in candidate.plaintexts[:3])
        print(
            f"score={candidate.score:.4f} ring={candidate.ring_name} "
            f"reverse={candidate.reversed_ring} a={candidate.multiplier} "
            f"b={candidate.offset} mode={'body' if candidate.omit_markers else 'full'}"
        )
        print(" ", preview.translate(display))


if __name__ == "__main__":
    main()
