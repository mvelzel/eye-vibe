"""Case-sensitive monoalphabetic attack for sdlwdr practice cipher 4."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from math import exp, log
import random


TRANSLATION = str.maketrans(
    {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
    }
)


def normalize_case_text(text: str, alphabet: str) -> str:
    """Keep case and supported punctuation, collapsing everything else to space."""

    if len(set(alphabet)) != len(alphabet):
        raise ValueError("alphabet characters must be unique")
    supported = set(alphabet)
    result: list[str] = []
    previous_space = True
    for character in text.translate(TRANSLATION):
        if character in supported and not character.isspace():
            result.append(character)
            previous_space = False
        elif " " in supported and not previous_space:
            result.append(" ")
            previous_space = True
    if result and result[-1] == " ":
        result.pop()
    return "".join(result)


@dataclass(frozen=True)
class CaseNgrams:
    order: int
    scores: dict[str, float]
    floor: float
    unigrams: dict[str, float]

    @classmethod
    def train(cls, text: str, alphabet: str, order: int = 4) -> "CaseNgrams":
        normalized = normalize_case_text(text, alphabet)
        counts = Counter(
            normalized[index : index + order]
            for index in range(len(normalized) - order + 1)
        )
        total = sum(counts.values())
        if not total:
            raise ValueError("training text has no n-grams")
        singles = Counter(normalized)
        denominator = len(normalized) + len(alphabet)
        return cls(
            order,
            {gram: log(count / total) for gram, count in counts.items()},
            log(0.01 / total),
            {
                character: (singles[character] + 1) / denominator
                for character in alphabet
            },
        )

    def score(self, text: Sequence[str]) -> float:
        return sum(
            self.scores.get("".join(text[index : index + self.order]), self.floor)
            for index in range(len(text) - self.order + 1)
        )


@dataclass(frozen=True)
class BijectionCandidate:
    score: float
    mapping: dict[int, str]
    plaintexts: tuple[str, ...]


class BijectionAnnealer:
    """Optimize an injective token-to-character map with unused characters."""

    def __init__(
        self,
        streams: Sequence[Sequence[int]],
        model: CaseNgrams,
        alphabet: str,
        rng: random.Random,
    ) -> None:
        observed = sorted({value for stream in streams for value in stream})
        if len(observed) > len(alphabet):
            raise ValueError("alphabet is smaller than the observed token set")
        self.streams = tuple(tuple(stream) for stream in streams)
        self.model = model
        self.alphabet = alphabet
        self.rng = rng
        self.observed = tuple(observed)
        self.slots = self.observed + tuple(
            -(index + 1) for index in range(len(alphabet) - len(observed))
        )
        self.slot_by_token = {
            token: index for index, token in enumerate(self.slots)
        }
        self.frequencies = Counter(
            token for stream in self.streams for token in stream
        )
        self.positions: dict[int, list[tuple[int, int]]] = defaultdict(list)
        for stream_index, stream in enumerate(self.streams):
            for position, token in enumerate(stream):
                self.positions[self.slot_by_token[token]].append(
                    (stream_index, position)
                )

    def initial_key(self) -> list[str]:
        """Frequency-match characters, then perturb for an independent restart."""

        ranked_slots = sorted(
            range(len(self.slots)),
            key=lambda slot: (
                self.frequencies.get(self.slots[slot], 0),
                self.rng.random(),
            ),
            reverse=True,
        )
        ranked_characters = sorted(
            self.alphabet,
            key=lambda character: (
                self.model.unigrams[character],
                self.rng.random(),
            ),
            reverse=True,
        )
        key = [""] * len(self.slots)
        for slot, character in zip(ranked_slots, ranked_characters, strict=True):
            key[slot] = character
        for _ in range(2 * len(key)):
            left, right = self.rng.sample(range(len(key)), 2)
            key[left], key[right] = key[right], key[left]
        return key

    def decode(self, key: Sequence[str]) -> list[list[str]]:
        return [
            [key[self.slot_by_token[token]] for token in stream]
            for stream in self.streams
        ]

    def gram_score(
        self, decoded: Sequence[Sequence[str]], stream: int, start: int
    ) -> float:
        values = decoded[stream]
        if start < 0 or start + self.model.order > len(values):
            return 0.0
        gram = "".join(values[start : start + self.model.order])
        return self.model.scores.get(gram, self.model.floor)

    def total_score(self, decoded: Sequence[Sequence[str]]) -> float:
        return sum(
            self.gram_score(decoded, stream, start)
            for stream, values in enumerate(decoded)
            for start in range(len(values) - self.model.order + 1)
        )

    def affected_starts(self, left: int, right: int) -> set[tuple[int, int]]:
        starts: set[tuple[int, int]] = set()
        for slot in (left, right):
            for stream, position in self.positions.get(slot, ()):  # dummy slots
                for start in range(
                    position - self.model.order + 1, position + 1
                ):
                    if 0 <= start <= len(self.streams[stream]) - self.model.order:
                        starts.add((stream, start))
        return starts

    def run(self, iterations: int, temperature: float) -> BijectionCandidate:
        key = self.initial_key()
        decoded = self.decode(key)
        score = self.total_score(decoded)
        best_score = score
        best_key = key.copy()

        for iteration in range(iterations):
            left, right = self.rng.sample(range(len(key)), 2)
            affected = self.affected_starts(left, right)
            before = sum(
                self.gram_score(decoded, stream, start)
                for stream, start in affected
            )
            key[left], key[right] = key[right], key[left]
            for slot in (left, right):
                for stream, position in self.positions.get(slot, ()):
                    decoded[stream][position] = key[slot]
            after = sum(
                self.gram_score(decoded, stream, start)
                for stream, start in affected
            )
            change = after - before
            progress = iteration / iterations
            current_temperature = temperature * (1.0 - progress) + 0.05
            if change >= 0 or self.rng.random() < exp(change / current_temperature):
                score += change
                if score > best_score:
                    best_score = score
                    best_key = key.copy()
            else:
                key[left], key[right] = key[right], key[left]
                for slot in (left, right):
                    for stream, position in self.positions.get(slot, ()):
                        decoded[stream][position] = key[slot]

        plaintexts = tuple(
            "".join(values) for values in self.decode(best_key)
        )
        return BijectionCandidate(
            best_score,
            {
                token: best_key[self.slot_by_token[token]]
                for token in self.observed
            },
            plaintexts,
        )


def encode_substitution(
    plaintexts: Sequence[str], mapping: dict[str, int]
) -> tuple[tuple[int, ...], ...]:
    """Encode a planted control with a fixed one-to-one substitution."""

    return tuple(
        tuple(mapping[character] for character in plaintext)
        for plaintext in plaintexts
    )
