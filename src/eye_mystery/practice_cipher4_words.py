"""Word-constrained search for sdlwdr practice cipher 4's cyclic GAK."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from heapq import nlargest
from math import log
import re

from eye_mystery.practice_cipher4_gak import (
    MODULUS,
    UNSET,
    plaintext_values,
)

NATURAL_42 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .-'?!"


@dataclass(frozen=True)
class SymbolModel:
    """Character n-grams over one explicit plaintext alphabet."""

    alphabet: str
    order: int
    scores: dict[bytes, float]
    floor: float

    @classmethod
    def train(
        cls, text: str, alphabet: str = NATURAL_42, order: int = 6
    ) -> "SymbolModel":
        if len(set(alphabet)) != len(alphabet):
            raise ValueError("alphabet characters must be unique")
        translated = text.upper().translate(
            str.maketrans({"’": "'", "‘": "'", "–": "-", "—": "-"})
        )
        code_by_character = {
            character: code for code, character in enumerate(alphabet)
        }
        space_code = code_by_character.get(" ")
        values: list[int] = []
        previous_space = True
        for character in translated:
            code = code_by_character.get(character)
            if code is not None:
                if character != " " or not previous_space:
                    values.append(code)
                previous_space = character == " "
            elif space_code is not None and not previous_space:
                values.append(space_code)
                previous_space = True
        if values and space_code is not None and values[-1] == space_code:
            values.pop()
        packed = bytes(values)
        counts = Counter(
            packed[index : index + order]
            for index in range(len(packed) - order + 1)
        )
        total = sum(counts.values())
        if not total:
            raise ValueError("training text is too short")
        return cls(
            alphabet,
            order,
            {gram: log(count / total) for gram, count in counts.items()},
            log(0.01 / total),
        )

    def score_extension(self, suffix: bytes, following: int) -> float:
        gram = suffix + bytes((following,))
        if len(gram) < self.order:
            return 0.0
        return self.scores.get(gram[-self.order :], self.floor)


@dataclass(frozen=True)
class WordTrie:
    """A compact uppercase word trie with terminal corpus frequencies."""

    children: tuple[dict[int, int], ...]
    terminal_score: tuple[float | None, ...]

    @classmethod
    def train(
        cls,
        text: str,
        *,
        minimum_count: int = 1,
        maximum_words: int | None = None,
    ) -> "WordTrie":
        if minimum_count < 1:
            raise ValueError("minimum_count must be positive")
        counts = Counter(re.findall(r"[A-Za-z]+", text.upper()))
        selected = [
            (word, count)
            for word, count in counts.most_common(maximum_words)
            if count >= minimum_count
        ]
        if not selected:
            raise ValueError("corpus does not contain any selected words")

        children: list[dict[int, int]] = [{}]
        terminal_counts: list[int] = [0]
        total = sum(count for _, count in selected)
        for word, count in selected:
            node = 0
            for character in word:
                code = ord(character) - ord("A")
                following = children[node].get(code)
                if following is None:
                    following = len(children)
                    children[node][code] = following
                    children.append({})
                    terminal_counts.append(0)
                node = following
            terminal_counts[node] = count
        for character in range(26):
            following = children[0].get(character)
            if following is None:
                following = len(children)
                children[0][character] = following
                children.append({})
                terminal_counts.append(1)
            elif not terminal_counts[following]:
                terminal_counts[following] = 1

        floor = log(0.1 / total)
        terminal_score = tuple(
            log(count / total) if count else None
            for count in terminal_counts
        )
        # The assignment is only to make the intended smoothing explicit in
        # the representation; every stored terminal has a positive count.
        if any(score is not None and score < floor for score in terminal_score):
            raise AssertionError("terminal score fell below the corpus floor")
        return cls(tuple(children), terminal_score)

    def advance(
        self,
        node: int,
        code: int,
        *,
        space_code: int = 26,
        punctuation_codes: Sequence[int] = (),
        digit_codes: Sequence[int] = (),
    ) -> tuple[int, float] | None:
        """Consume one explicit-alphabet symbol.

        Negative node ``-1`` denotes a run of digits. Punctuation terminates a
        complete word and returns to the root; a following space at the root
        is allowed so punctuation-bearing prose remains representable.
        """

        if code == space_code:
            if node == 0:
                return 0, 0.0
            if node == -1:
                return 0, 0.0
            score = self.terminal_score[node]
            if score is None:
                return None
            return 0, score
        if code in digit_codes:
            if node in (0, -1):
                return -1, 0.0
            return None
        if code in punctuation_codes:
            if node == -1:
                return 0, 0.0
            if node < 0:
                return None
            score = self.terminal_score[node]
            if score is None:
                return None
            return 0, score
        if node < 0:
            return None
        following = self.children[node].get(code)
        if following is None:
            return None
        return following, 0.0

    def starts(self) -> tuple[tuple[int, int], ...]:
        return tuple(sorted(self.children[0].items()))


@dataclass(frozen=True)
class WordBeamCandidate:
    score: float
    key: bytes
    trie_node: int
    suffix: bytes
    plaintext: bytes


@dataclass(frozen=True)
class WordBeamResult:
    completed: int
    candidates: tuple[WordBeamCandidate, ...]
    generated_by_step: tuple[int, ...]


def word_constrained_gak_beam(
    differences: Sequence[int],
    trie: WordTrie,
    character_model: SymbolModel,
    *,
    space_position: int,
    beam_width: int,
    ciphertext_sign: int = 1,
    plaintext_sign: int = 1,
    key_on_next: bool = False,
    word_score_weight: float = 0.1,
    plaintext_positions: Sequence[int] | None = None,
    space_code: int = 26,
    punctuation_codes: Sequence[int] = (),
    digit_codes: Sequence[int] = (),
) -> WordBeamResult:
    """Search the arbitrary cyclic-GAK recurrence inside dictionary prose.

    Unlike the character-only beam, candidates must remain prefixes of corpus
    words. This is a hard structural constraint, not another local score.
    """

    if beam_width < 1:
        raise ValueError("beam width must be positive")
    if ciphertext_sign not in (-1, 1) or plaintext_sign not in (-1, 1):
        raise ValueError("signs must be -1 or +1")
    if any(value not in range(MODULUS) for value in differences):
        raise ValueError("differences must lie in Z83")
    if word_score_weight < 0:
        raise ValueError("word_score_weight must be nonnegative")

    actual = tuple(
        plaintext_values(space_position)
        if plaintext_positions is None
        else plaintext_positions
    )
    if len(actual) > UNSET:
        raise ValueError("plaintext alphabet is too large for packed keys")
    if len(set(actual)) != len(actual) or any(
        value not in range(MODULUS) for value in actual
    ):
        raise ValueError("plaintext positions must be distinct values in Z83")
    oriented_to_code = {
        plaintext_sign * value % MODULUS: code
        for code, value in enumerate(actual)
    }
    empty_key = bytes((UNSET,)) * len(actual)
    suffix_size = character_model.order - 1
    beam = [
        WordBeamCandidate(
            0.0,
            empty_key,
            node,
            bytes((code,)),
            bytes((code,)),
        )
        for code, node in trie.starts()
    ]
    generated_by_step: list[int] = []
    completed = 0

    for difference in differences:
        expanded: dict[
            tuple[bytes, int, bytes],
            tuple[float, int, int, bytes, int, bytes],
        ] = {}
        signed_difference = ciphertext_sign * difference
        for parent_index, candidate in enumerate(beam):
            current_code = candidate.plaintext[-1]
            if key_on_next:
                possible_codes = range(len(actual))
            else:
                key_value = candidate.key[current_code]
                if key_value == UNSET:
                    possible_codes = range(len(actual))
                else:
                    following_oriented = (
                        signed_difference + key_value
                    ) % MODULUS
                    following_code = oriented_to_code.get(following_oriented)
                    if following_code is None:
                        continue
                    possible_codes = (following_code,)

            for following_code in possible_codes:
                language_step = trie.advance(
                    candidate.trie_node,
                    following_code,
                    space_code=space_code,
                    punctuation_codes=punctuation_codes,
                    digit_codes=digit_codes,
                )
                if language_step is None:
                    continue
                following_node, word_score = language_step
                following_oriented = (
                    plaintext_sign * actual[following_code] % MODULUS
                )
                required = (
                    following_oriented - signed_difference
                ) % MODULUS
                selector_code = (
                    following_code if key_on_next else current_code
                )
                previous_required = candidate.key[selector_code]
                if previous_required not in (UNSET, required):
                    continue
                if previous_required == UNSET:
                    key = (
                        candidate.key[:selector_code]
                        + bytes((required,))
                        + candidate.key[selector_code + 1 :]
                    )
                else:
                    key = candidate.key

                score = (
                    candidate.score
                    + character_model.score_extension(
                        candidate.suffix, following_code
                    )
                    + word_score_weight * word_score
                )
                suffix = (
                    candidate.suffix + bytes((following_code,))
                )[-suffix_size:]
                identity = (key, following_node, suffix)
                previous = expanded.get(identity)
                if previous is None or score > previous[0]:
                    expanded[identity] = (
                        score,
                        parent_index,
                        following_code,
                        key,
                        following_node,
                        suffix,
                    )

        generated_by_step.append(len(expanded))
        if not expanded:
            break
        selected = nlargest(
            beam_width, expanded.values(), key=lambda item: item[0]
        )
        beam = [
            WordBeamCandidate(
                score,
                key,
                following_node,
                suffix,
                beam[parent_index].plaintext + bytes((following_code,)),
            )
            for (
                score,
                parent_index,
                following_code,
                key,
                following_node,
                suffix,
            ) in selected
        ]
        completed += 1

    return WordBeamResult(
        completed,
        tuple(sorted(beam, key=lambda item: item.score, reverse=True)),
        tuple(generated_by_step),
    )


def encode_word_gak(
    plaintext: Sequence[int],
    key: Sequence[int],
    plaintext_positions: Sequence[int],
    *,
    ciphertext_sign: int = 1,
    plaintext_sign: int = 1,
) -> tuple[int, ...]:
    """Encode a planted current-symbol cyclic-GAK fixture."""

    positions = tuple(plaintext_positions)
    if len(key) != len(positions) or any(
        value not in range(MODULUS) for value in key
    ):
        raise ValueError("key must match the plaintext alphabet")
    if any(value not in range(len(positions)) for value in plaintext):
        raise ValueError("plaintext symbol lies outside the alphabet")
    return tuple(
        ciphertext_sign
        * (
            plaintext_sign * positions[following]
            - key[current]
        )
        % MODULUS
        for current, following in zip(plaintext, plaintext[1:])
    )


def render_symbols(values: Sequence[int], alphabet: str = NATURAL_42) -> str:
    return "".join(alphabet[value] for value in values)
