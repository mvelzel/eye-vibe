"""A compact A-Z tetragram language model for substitution experiments."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import log


ALPHABET_SIZE = 26
TABLE_SIZE = ALPHABET_SIZE**4


def ascii_letters(text: str) -> tuple[int, ...]:
    return tuple(ord(char) - ord("A") for char in text.upper() if "A" <= char <= "Z")


def tetragram_code(values: tuple[int, int, int, int]) -> int:
    a, b, c, d = values
    return ((a * ALPHABET_SIZE + b) * ALPHABET_SIZE + c) * ALPHABET_SIZE + d


@dataclass(frozen=True)
class TetragramModel:
    log_probabilities: tuple[float, ...]

    @classmethod
    def train(cls, text: str) -> "TetragramModel":
        letters = ascii_letters(text)
        if len(letters) < 4:
            raise ValueError("language corpus needs at least four A-Z letters")
        counts = Counter(
            tetragram_code(tuple(letters[index : index + 4]))
            for index in range(len(letters) - 3)
        )
        total = sum(counts.values())
        floor = log(0.05 / total)
        table = [floor] * TABLE_SIZE
        for code, count in counts.items():
            table[code] = log(count / total)
        return cls(tuple(table))

    def score(self, text: tuple[int, ...]) -> float:
        return sum(
            self.log_probabilities[tetragram_code(tuple(text[index : index + 4]))]
            for index in range(len(text) - 3)
        )
