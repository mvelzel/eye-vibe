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
    trace: Hashable | None = None

    @property
    def observation_locations(
        self,
    ) -> tuple[tuple[Hashable | None, int], ...]:
        return ((self.trace, self.start), (self.trace, self.end))


@dataclass(frozen=True)
class StabilizerContradiction:
    """Three observed word statuses incompatible with a point stabilizer."""

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

    @property
    def observation_locations(
        self,
    ) -> tuple[tuple[Hashable | None, int], ...]:
        return tuple(
            sorted(
                {
                    *self.first.observation_locations,
                    *self.second.observation_locations,
                    *self.combined.observation_locations,
                },
                key=lambda item: (repr(item[0]), item[1]),
            )
        )


@dataclass(frozen=True)
class WordStatusConflict:
    """The same operation word observed both fixing and not fixing top."""

    fixed: WordSpan
    nonfixed: WordSpan


def word_spans(
    plaintext: Sequence[Hashable],
    ciphertext: Sequence[int],
    *,
    trace: Hashable | None = None,
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
                    trace=trace,
                )
            )
    return tuple(spans)


def find_word_status_conflicts(
    spans: Sequence[WordSpan],
) -> tuple[WordStatusConflict, ...]:
    """Find words observed both inside and outside the top stabilizer."""

    fixed: dict[tuple[Hashable, ...], list[WordSpan]] = defaultdict(list)
    nonfixed: dict[tuple[Hashable, ...], list[WordSpan]] = defaultdict(list)
    for span in spans:
        (fixed if span.fixes_top else nonfixed)[span.word].append(span)
    conflicts = (
        WordStatusConflict(fixed_span, nonfixed_span)
        for word in fixed.keys() & nonfixed.keys()
        for fixed_span in fixed[word]
        for nonfixed_span in nonfixed[word]
    )
    return tuple(
        sorted(
            conflicts,
            key=lambda item: (
                len(item.fixed.word),
                repr(item.fixed.word),
                repr(item.fixed.trace),
                item.fixed.start,
                repr(item.nonfixed.trace),
                item.nonfixed.start,
            ),
        )
    )


def find_stabilizer_contradictions_from_spans(
    spans: Sequence[WordSpan],
) -> tuple[StabilizerContradiction, ...]:
    """Find exact ordinary-GAK contradictions implied by repeated words."""

    by_status: dict[bool, dict[tuple[Hashable, ...], list[WordSpan]]] = {
        True: defaultdict(list),
        False: defaultdict(list),
    }
    for span in spans:
        by_status[span.fixes_top][span.word].append(span)

    contradictions: set[StabilizerContradiction] = set()
    for combined in spans:
        if len(combined.word) < 2:
            continue
        for split in range(1, len(combined.word)):
            first_word = combined.word[:split]
            second_word = combined.word[split:]
            if not combined.fixes_top:
                for fixed_first in by_status[True].get(first_word, ()):
                    for fixed_second in by_status[True].get(second_word, ()):
                        contradictions.add(
                            StabilizerContradiction(
                                fixed_first,
                                fixed_second,
                                combined,
                            )
                        )
                continue
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


def find_stabilizer_contradictions(
    plaintext: Sequence[Hashable],
    ciphertext: Sequence[int],
) -> tuple[StabilizerContradiction, ...]:
    """Find exact ordinary-GAK contradictions in one aligned trace."""

    return find_stabilizer_contradictions_from_spans(
        word_spans(plaintext, ciphertext)
    )


def combined_word_spans(
    plaintexts: Sequence[Sequence[Hashable]],
    ciphertexts: Sequence[Sequence[int]],
    *,
    trace_names: Sequence[Hashable] | None = None,
) -> tuple[WordSpan, ...]:
    """Collect word spans from independent traces without crossing them."""

    if len(plaintexts) != len(ciphertexts):
        raise ValueError("plaintext and ciphertext trace counts differ")
    names: Sequence[Hashable] = (
        tuple(range(len(plaintexts))) if trace_names is None else trace_names
    )
    if len(names) != len(plaintexts):
        raise ValueError("trace name count differs from trace count")
    return tuple(
        span
        for plaintext, ciphertext, name in zip(
            plaintexts,
            ciphertexts,
            names,
            strict=True,
        )
        for span in word_spans(plaintext, ciphertext, trace=name)
    )
