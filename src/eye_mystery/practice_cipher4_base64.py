"""Base64-under-substitution attack for sdlwdr practice cipher 4.

The cyclic outer layer reduces each ciphertext portion to adjacent differences.
This module tests whether those difference symbols are a monoalphabetic encoding
of an unpadded Base64 stream.  A swap in the candidate alphabet changes only
the Base64 quartets containing either swapped symbol, so language scoring can
be updated locally.
"""

from __future__ import annotations

import base64
from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from math import exp, log
import random


BASE64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def decode_base64_values(values: Sequence[int]) -> bytes:
    """Decode unpadded Base64 values, rejecting an impossible one-symbol tail."""

    if any(value not in range(64) for value in values):
        raise ValueError("Base64 values must lie in 0..63")
    if len(values) % 4 == 1:
        raise ValueError("an unpadded Base64 stream cannot have length 1 mod 4")
    encoded = "".join(BASE64_ALPHABET[value] for value in values)
    encoded += "=" * (-len(encoded) % 4)
    return base64.b64decode(encoded, validate=True)


def normalize_training_bytes(data: bytes) -> bytes:
    """Lower-case printable prose and collapse whitespace for byte n-grams."""

    result = bytearray()
    previous_space = True
    for value in data:
        if 65 <= value <= 90:
            result.append(value + 32)
            previous_space = False
        elif 32 <= value <= 126:
            result.append(value)
            previous_space = value == 32
        elif value in (9, 10, 13) and not previous_space:
            result.append(32)
            previous_space = True
    if result and result[-1] == 32:
        result.pop()
    return bytes(result)


def normalized_byte(value: int) -> int:
    if 65 <= value <= 90:
        return value + 32
    if value in (9, 10, 13):
        return 32
    return value


@dataclass(frozen=True)
class ByteNgrams:
    order: int
    scores: dict[bytes, float]
    floor: float
    printable_reward: float = 6.0
    text_reward: float = 1.5
    nonprintable_penalty: float = 18.0

    @classmethod
    def train(cls, data: bytes, order: int = 4) -> "ByteNgrams":
        normalized = normalize_training_bytes(data)
        counts = Counter(
            normalized[index : index + order]
            for index in range(len(normalized) - order + 1)
        )
        total = sum(counts.values())
        if not total:
            raise ValueError("training data has no byte n-grams")
        return cls(
            order,
            {gram: log(count / total) for gram, count in counts.items()},
            log(0.01 / total),
        )

    def byte_score(self, value: int) -> float:
        if value in (9, 10, 13) or 32 <= value <= 126:
            score = self.printable_reward
            if value == 32 or 65 <= value <= 90 or 97 <= value <= 122:
                score += self.text_reward
            return score
        return -self.nonprintable_penalty

    def gram_score(self, values: Sequence[int], start: int) -> float:
        if start < 0 or start + self.order > len(values):
            return 0.0
        gram = bytes(normalized_byte(value) for value in values[start : start + self.order])
        return self.scores.get(gram, self.floor)


@dataclass(frozen=True)
class Base64Candidate:
    score: float
    printable: int
    letters_or_spaces: int
    mapping: dict[int, str]
    plaintexts: tuple[bytes, ...]


class Base64SubstitutionAnnealer:
    """Search an injective difference-symbol to Base64-value mapping."""

    def __init__(
        self,
        streams: Sequence[Sequence[int]],
        model: ByteNgrams,
        rng: random.Random,
        expected_base64: bytes | None = None,
    ) -> None:
        if any(len(stream) % 4 == 1 for stream in streams):
            raise ValueError("every stream must be valid unpadded Base64 length")
        self.streams = tuple(tuple(stream) for stream in streams)
        self.model = model
        self.rng = rng
        self.observed = tuple(sorted({value for stream in streams for value in stream}))
        if len(self.observed) > 64:
            raise ValueError("more than 64 difference symbols are observed")
        self.slots = self.observed + tuple(
            -(index + 1) for index in range(64 - len(self.observed))
        )
        self.slot_by_token = {token: index for index, token in enumerate(self.slots)}
        self.token_streams = tuple(
            tuple(self.slot_by_token[token] for token in stream) for stream in self.streams
        )
        self.frequencies = Counter(slot for stream in self.token_streams for slot in stream)
        self.quartets_by_slot: dict[int, set[tuple[int, int]]] = defaultdict(set)
        for stream_index, stream in enumerate(self.token_streams):
            for position, slot in enumerate(stream):
                self.quartets_by_slot[slot].add((stream_index, position // 4))

        expected = expected_base64 if expected_base64 is not None else b""
        expected_counts = Counter(expected)
        self.expected_value_frequency = {
            index: expected_counts[ord(character)]
            for index, character in enumerate(BASE64_ALPHABET)
        }

    @staticmethod
    def decode_quartet(values: Sequence[int]) -> tuple[int, ...]:
        if not 2 <= len(values) <= 4:
            raise ValueError("a Base64 quartet must contain two to four values")
        first = (values[0] << 2) | (values[1] >> 4)
        if len(values) == 2:
            return (first,)
        second = ((values[1] & 15) << 4) | (values[2] >> 2)
        if len(values) == 3:
            return (first, second)
        third = ((values[2] & 3) << 6) | values[3]
        return (first, second, third)

    def initial_key(self) -> list[int]:
        ranked_slots = sorted(
            range(64),
            key=lambda slot: (self.frequencies.get(slot, 0), self.rng.random()),
            reverse=True,
        )
        ranked_values = sorted(
            range(64),
            key=lambda value: (self.expected_value_frequency[value], self.rng.random()),
            reverse=True,
        )
        key = [0] * 64
        for slot, value in zip(ranked_slots, ranked_values, strict=True):
            key[slot] = value
        for _ in range(128):
            left, right = self.rng.sample(range(64), 2)
            key[left], key[right] = key[right], key[left]
        return key

    def decode(self, key: Sequence[int]) -> list[list[int]]:
        outputs: list[list[int]] = []
        for stream in self.token_streams:
            output: list[int] = []
            for start in range(0, len(stream), 4):
                output.extend(
                    self.decode_quartet([key[slot] for slot in stream[start : start + 4]])
                )
            outputs.append(output)
        return outputs

    def total_score(self, decoded: Sequence[Sequence[int]]) -> float:
        return sum(
            self.model.byte_score(value)
            for stream in decoded
            for value in stream
        ) + sum(
            self.model.gram_score(stream, start)
            for stream in decoded
            for start in range(len(stream) - self.model.order + 1)
        )

    def _quartet_output_start(self, quartet: int) -> int:
        return quartet * 3

    def _affected_positions(self, left: int, right: int) -> dict[int, set[int]]:
        affected: dict[int, set[int]] = defaultdict(set)
        for slot in (left, right):
            for stream_index, quartet in self.quartets_by_slot.get(slot, ()):
                start = self._quartet_output_start(quartet)
                token_start = quartet * 4
                output_length = len(
                    self.decode_quartet(
                        [0] * min(4, len(self.token_streams[stream_index]) - token_start)
                    )
                )
                affected[stream_index].update(range(start, start + output_length))
        return affected

    def _local_score(
        self, decoded: Sequence[Sequence[int]], affected: dict[int, set[int]]
    ) -> float:
        total = 0.0
        for stream_index, positions in affected.items():
            stream = decoded[stream_index]
            total += sum(self.model.byte_score(stream[position]) for position in positions)
            starts: set[int] = set()
            for position in positions:
                starts.update(
                    range(position - self.model.order + 1, position + 1)
                )
            total += sum(self.model.gram_score(stream, start) for start in starts)
        return total

    def _refresh_quartets(
        self,
        key: Sequence[int],
        decoded: list[list[int]],
        left: int,
        right: int,
    ) -> None:
        quartets = self.quartets_by_slot.get(left, set()) | self.quartets_by_slot.get(right, set())
        for stream_index, quartet in quartets:
            token_start = quartet * 4
            values = [
                key[slot]
                for slot in self.token_streams[stream_index][token_start : token_start + 4]
            ]
            output = self.decode_quartet(values)
            start = self._quartet_output_start(quartet)
            decoded[stream_index][start : start + len(output)] = output

    def run(self, iterations: int, temperature: float) -> Base64Candidate:
        key = self.initial_key()
        decoded = self.decode(key)
        score = self.total_score(decoded)
        best_score = score
        best_key = key.copy()

        for iteration in range(iterations):
            left, right = self.rng.sample(range(64), 2)
            affected = self._affected_positions(left, right)
            before = self._local_score(decoded, affected)
            key[left], key[right] = key[right], key[left]
            self._refresh_quartets(key, decoded, left, right)
            after = self._local_score(decoded, affected)
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
                self._refresh_quartets(key, decoded, left, right)

        plaintexts = tuple(bytes(stream) for stream in self.decode(best_key))
        flattened = b"".join(plaintexts)
        return Base64Candidate(
            best_score,
            sum(value in (9, 10, 13) or 32 <= value <= 126 for value in flattened),
            sum(value == 32 or 65 <= value <= 90 or 97 <= value <= 122 for value in flattened),
            {
                token: BASE64_ALPHABET[best_key[self.slot_by_token[token]]]
                for token in self.observed
            },
            plaintexts,
        )


def encode_base64_substitution(data: bytes, inverse: dict[str, int]) -> tuple[int, ...]:
    """Encode a planted byte string as substituted, unpadded Base64 symbols."""

    encoded = base64.b64encode(data).decode("ascii").rstrip("=")
    return tuple(inverse[character] for character in encoded)
