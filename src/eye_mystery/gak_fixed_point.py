"""Plaintext-word fixed-point certificates for ordinary GAK.

For a known plaintext interval, equal ciphertext cards at its two endpoints
mean that the interval's composite position permutation fixes the top
position.  Different endpoint cards mean that it does not.

The permutations fixing one point form a subgroup.  Therefore, if a repeated
word is a concatenation of two repeated component words, and the whole word
and one component fix the top, the other component must fix it as well.  A
different-card observation on that other component is an exact contradiction.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Hashable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class WordSpan:
    """Updates after ``start`` through ``end``, inclusive of ``end``."""

    start: int
    end: int
    word: tuple[Hashable, ...]
    fixes_top: bool


@dataclass(frozen=True)
class StabilizerContradiction:
    """A fixed concatenation with one fixed and one nonfixed factor."""

    first: WordSpan
    second: WordSpan
    combined: WordSpan

    @property
    def observation_offsets(self) -> tuple[int, ...]:
        return tuple(
            sorted(
                {
                    self.first.start,
                    self.first.end,
                    self.second.start,
                    self.second.end,
                    self.combined.start,
                    self.combined.end,
                }
            )
        )


def word_spans(
    plaintext: Sequence[Hashable],
    ciphertext: Sequence[int],
) -> tuple[WordSpan, ...]:
    """Infer every nonempty word's top-fixing status from its endpoints."""

    if len(plaintext) != len(ciphertext):
        raise ValueError("plaintext and ciphertext lengths differ")
    spans: list[WordSpan] = []
    for start in range(len(plaintext) - 1):
        for end in range(start + 1, len(plaintext)):
            spans.append(
                WordSpan(
                    start=start,
                    end=end,
                    word=tuple(plaintext[start + 1 : end + 1]),
                    fixes_top=ciphertext[start] == ciphertext[end],
                )
            )
    return tuple(spans)


def find_stabilizer_contradictions(
    plaintext: Sequence[Hashable],
    ciphertext: Sequence[int],
) -> tuple[StabilizerContradiction, ...]:
    """Find exact ordinary-GAK contradictions implied by repeated words."""

    spans = word_spans(plaintext, ciphertext)
    by_status: dict[bool, dict[tuple[Hashable, ...], list[WordSpan]]] = {
        True: defaultdict(list),
        False: defaultdict(list),
    }
    for span in spans:
        by_status[span.fixes_top][span.word].append(span)

    contradictions: set[StabilizerContradiction] = set()
    for combined in spans:
        if not combined.fixes_top or len(combined.word) < 2:
            continue
        for split in range(1, len(combined.word)):
            first_word = combined.word[:split]
            second_word = combined.word[split:]
            for fixed_first in by_status[True].get(first_word, ()):
                for nonfixed_second in by_status[False].get(second_word, ()):
                    contradictions.add(
                        StabilizerContradiction(
                            fixed_first,
                            nonfixed_second,
                            combined,
                        )
                    )
            for nonfixed_first in by_status[False].get(first_word, ()):
                for fixed_second in by_status[True].get(second_word, ()):
                    contradictions.add(
                        StabilizerContradiction(
                            nonfixed_first,
                            fixed_second,
                            combined,
                        )
                    )

    return tuple(
        sorted(
            contradictions,
            key=lambda item: (
                len(item.observation_offsets),
                len(item.combined.word),
                item.observation_offsets,
                item.first.start,
                item.second.start,
            ),
        )
    )
