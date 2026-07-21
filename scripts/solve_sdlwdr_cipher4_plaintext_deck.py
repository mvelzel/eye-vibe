#!/usr/bin/env python3
"""Test simple 57-card adaptive plaintext decks for sdlwdr cipher #4.

The standard cyclic ciphertext group turns each portion into its first value
followed by adjacent differences modulo 83.  Every resulting value lies in the
contiguous interval 22..78, so subtracting 22 produces valid ranks in a
57-card deck.  This program tests the common self-organising-list and small
deck-update rules under straightforward 57-character initial alphabets.

The search is deliberately finite and falsifiable.  It enumerates rotations
and reversals of each initial alphabet, decodes every portion from a reset
deck, scores the fixed-length output as English, and reports whether the exact
shared rank blocks also decode alike from their independently reached states.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from difflib import SequenceMatcher
import json
from math import log
from pathlib import Path
import string
from typing import Iterable, Sequence


MODULUS = 83
RANK_OFFSET = 22
DECK_SIZE = 57
ROOT = Path(__file__).resolve().parents[1]


def action_ranks(message: Sequence[int]) -> tuple[int, ...]:
    if not message:
        return ()
    actions = (message[0],) + tuple(
        (right - left) % MODULUS for left, right in zip(message, message[1:])
    )
    ranks = tuple(action - RANK_OFFSET for action in actions)
    if any(not 0 <= rank < DECK_SIZE for rank in ranks):
        raise ValueError("cyclic actions do not fit the observed 57-rank band")
    return ranks


def alphabet_families() -> dict[str, str]:
    punctuation = " .,?!"
    families = {
        "upper-lower": string.ascii_uppercase + string.ascii_lowercase + punctuation,
        "lower-upper": string.ascii_lowercase + string.ascii_uppercase + punctuation,
        "upper-space-lower":
            string.ascii_uppercase + " " + string.ascii_lowercase + ".,?!",
        "lower-space-upper":
            string.ascii_lowercase + " " + string.ascii_uppercase + ".,?!",
        "ascii-space": "".join(chr(value) for value in range(32, 32 + DECK_SIZE)),
        "ascii-bang": "".join(chr(value) for value in range(33, 33 + DECK_SIZE)),
    }
    for name, alphabet in families.items():
        if len(alphabet) != DECK_SIZE or len(set(alphabet)) != DECK_SIZE:
            raise AssertionError(f"invalid alphabet {name}")
    return families


RULES = (
    "identity",
    "move-front",
    "move-back",
    "transpose-left",
    "transpose-right",
    "swap-front",
    "swap-back",
    "reverse-prefix",
    "reverse-suffix",
    "rotate-rank-front",
    "rotate-after-rank-front",
    "rotate-one-left",
    "rotate-one-right",
)


def update(deck: list[str], rank: int, rule: str) -> None:
    """Apply one standard adaptive-list operation in place."""

    if rule == "identity":
        return
    if rule == "move-front":
        deck.insert(0, deck.pop(rank))
    elif rule == "move-back":
        deck.append(deck.pop(rank))
    elif rule == "transpose-left":
        if rank:
            deck[rank - 1], deck[rank] = deck[rank], deck[rank - 1]
    elif rule == "transpose-right":
        if rank + 1 < len(deck):
            deck[rank], deck[rank + 1] = deck[rank + 1], deck[rank]
    elif rule == "swap-front":
        deck[0], deck[rank] = deck[rank], deck[0]
    elif rule == "swap-back":
        deck[-1], deck[rank] = deck[rank], deck[-1]
    elif rule == "reverse-prefix":
        deck[: rank + 1] = reversed(deck[: rank + 1])
    elif rule == "reverse-suffix":
        deck[rank:] = reversed(deck[rank:])
    elif rule == "rotate-rank-front":
        deck[:] = deck[rank:] + deck[:rank]
    elif rule == "rotate-after-rank-front":
        cut = rank + 1
        deck[:] = deck[cut:] + deck[:cut]
    elif rule == "rotate-one-left":
        deck.append(deck.pop(0))
    elif rule == "rotate-one-right":
        deck.insert(0, deck.pop())
    else:
        raise ValueError(f"unknown deck rule: {rule}")


def decode(ranks: Sequence[int], alphabet: str, rule: str) -> str:
    deck = list(alphabet)
    result: list[str] = []
    for rank in ranks:
        result.append(deck[rank])
        update(deck, rank, rule)
    return "".join(result)


def encode(plaintext: str, alphabet: str, rule: str) -> tuple[int, ...]:
    """Inverse of :func:`decode`, used as a positive-control primitive."""

    deck = list(alphabet)
    result: list[int] = []
    for character in plaintext:
        rank = deck.index(character)
        result.append(rank)
        update(deck, rank, rule)
    return tuple(result)


def normalized_fixed(text: str) -> tuple[int, ...]:
    return tuple(
        ord(character.upper()) - ord("A")
        if character.upper() in string.ascii_uppercase
        else 26
        for character in text
    )


@dataclass(frozen=True)
class Tetragrams:
    scores: dict[tuple[int, ...], float]
    floor: float

    @classmethod
    def train(cls, text: str) -> "Tetragrams":
        values = normalized_fixed(text)
        counts = Counter(
            values[index : index + 4] for index in range(len(values) - 3)
        )
        total = sum(counts.values())
        return cls(
            {gram: log(count / total) for gram, count in counts.items()},
            log(0.01 / total),
        )

    def score(self, texts: Iterable[str]) -> float:
        total = 0.0
        for text in texts:
            values = normalized_fixed(text)
            total += sum(
                self.scores.get(values[index : index + 4], self.floor)
                for index in range(len(values) - 3)
            )
            total -= 8.0 * sum(
                character != " " and character.upper() not in string.ascii_uppercase
                for character in text
            )
        return total


def shared_block_agreement(
    ranks: Sequence[Sequence[int]], texts: Sequence[str]
) -> tuple[int, int]:
    """Count equality in all maximal shared rank blocks of length at least 20."""

    equal = 0
    total = 0
    for left in range(len(ranks)):
        for right in range(left + 1, len(ranks)):
            matcher = SequenceMatcher(None, ranks[left], ranks[right], autojunk=False)
            for left_start, right_start, length in matcher.get_matching_blocks():
                if length < 20:
                    continue
                left_text = texts[left][left_start : left_start + length]
                right_text = texts[right][right_start : right_start + length]
                equal += sum(a == b for a, b in zip(left_text, right_text, strict=True))
                total += length
    return equal, total


@dataclass(frozen=True)
class Candidate:
    score: float
    agreement: int
    compared: int
    rule: str
    alphabet_name: str
    reversed_alphabet: bool
    rotation: int
    texts: tuple[str, ...]


def search(
    ranks: tuple[tuple[int, ...], ...], model: Tetragrams, top: int
) -> list[Candidate]:
    candidates: list[Candidate] = []
    for alphabet_name, base in alphabet_families().items():
        for reversed_alphabet in (False, True):
            oriented = base[::-1] if reversed_alphabet else base
            for rotation in range(DECK_SIZE):
                alphabet = oriented[rotation:] + oriented[:rotation]
                for rule in RULES:
                    texts = tuple(decode(stream, alphabet, rule) for stream in ranks)
                    agreement, compared = shared_block_agreement(ranks, texts)
                    candidates.append(
                        Candidate(
                            model.score(texts),
                            agreement,
                            compared,
                            rule,
                            alphabet_name,
                            reversed_alphabet,
                            rotation,
                            texts,
                        )
                    )
    return sorted(candidates, key=lambda candidate: candidate.score, reverse=True)[:top]


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
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    messages = json.loads(args.data.read_text())
    ranks = tuple(action_ranks(message) for message in messages)
    model = Tetragrams.train(args.corpus.read_text(errors="ignore"))
    for candidate in search(ranks, model, args.top):
        print(
            f"score={candidate.score:.2f} "
            f"shared={candidate.agreement}/{candidate.compared} "
            f"rule={candidate.rule} alphabet={candidate.alphabet_name} "
            f"reversed={candidate.reversed_alphabet} rotation={candidate.rotation}"
        )
        for text in candidate.texts:
            print(text[:240])
        print()


if __name__ == "__main__":
    main()
