#!/usr/bin/env python3
"""Audit literal Waite continuations in the three connected Eye segments."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
from pathlib import Path

from eye_mystery.free_group_gak import audit_free_group_gak
from eye_mystery.gak_fixed_point import (
    combined_word_spans,
    find_word_status_conflicts,
)

try:
    from scripts.run_that_which_connected_gap_gak import connected_instances
    from scripts.search_waite_that_which import (
        PHRASE,
        TARGETS,
        normalize_ocr,
        phrase_offsets,
    )
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from run_that_which_connected_gap_gak import connected_instances
    from search_waite_that_which import (
        PHRASE,
        TARGETS,
        normalize_ocr,
        phrase_offsets,
    )


@dataclass(frozen=True)
class SourceSegment:
    """One source-only repeated-phrase interval."""

    source: str
    target: str
    first_offset: int
    text: str
    next_character: str | None

    @property
    def identifier(self) -> str:
        return f"{self.source}:{self.first_offset}"


def source_segments(
    sources: tuple[tuple[str, str], ...],
) -> dict[str, tuple[SourceSegment, ...]]:
    """Enumerate all exact-gap source intervals for each Eye target."""

    by_target: dict[str, list[SourceSegment]] = {
        target.name: [] for target in TARGETS
    }
    for source_name, text in sources:
        offsets = phrase_offsets(text)
        for target in TARGETS:
            for first_index, first in enumerate(offsets):
                for second in offsets[first_index + 1 :]:
                    gap = second - first
                    if gap > target.gap:
                        break
                    if gap != target.gap:
                        continue
                    end = second + len(PHRASE)
                    by_target[target.name].append(
                        SourceSegment(
                            source=source_name,
                            target=target.name,
                            first_offset=first,
                            text=text[first:end],
                            next_character=(
                                text[end] if end < len(text) else None
                            ),
                        )
                    )
    return {
        target: tuple(segments)
        for target, segments in by_target.items()
    }


def encode_shared_characters(
    segments: tuple[SourceSegment, ...],
) -> tuple[tuple[tuple[int, ...], ...], tuple[str, ...]]:
    alphabet = tuple(sorted(set("".join(segment.text for segment in segments))))
    rank = {character: index for index, character in enumerate(alphabet)}
    plaintexts = tuple(
        tuple(rank[character] for character in segment.text)
        for segment in segments
    )
    return plaintexts, alphabet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("sources", nargs="+", type=Path)
    args = parser.parse_args()

    normalized = tuple(
        (path.name, normalize_ocr(path.read_text(errors="replace")))
        for path in args.sources
    )
    candidates = source_segments(normalized)
    patterns, ciphertexts, _ = connected_instances()
    target_order = tuple(target.name for target in TARGETS)
    print(
        "candidate_counts="
        + ",".join(
            f"{target}:{len(candidates[target])}"
            for target in target_order
        )
    )
    for target, pattern in zip(target_order, patterns, strict=True):
        expected_length = len(pattern)
        for index, candidate in enumerate(candidates[target]):
            if len(candidate.text) != expected_length:
                raise AssertionError("source segment has the wrong target length")
            print(
                f"source target={target} index={index} "
                f"id={candidate.identifier} next={candidate.next_character!r} "
                f"text={candidate.text!r}"
            )

    survivors = []
    forced_word_sets: list[set[str]] = []
    first_direct_conflicts = None
    for indices, combination in enumerate(
        product(*(candidates[target] for target in target_order))
    ):
        plaintexts, alphabet = encode_shared_characters(combination)
        audit = audit_free_group_gak(plaintexts, ciphertexts)
        decoded_forced = {
            "".join(alphabet[symbol] for symbol in word)
            for word in audit.forced_nonfix_words
        }
        forced_word_sets.append(decoded_forced)
        if first_direct_conflicts is None:
            first_direct_conflicts = (
                alphabet,
                find_word_status_conflicts(
                    combined_word_spans(
                        plaintexts,
                        ciphertexts,
                        trace_names=target_order,
                    )
                ),
            )
        status = "pass" if not audit.forced_nonfix_words else "reject"
        index_tuple = tuple(
            candidates[target].index(candidate)
            for target, candidate in zip(
                target_order, combination, strict=True
            )
        )
        print(
            f"triple={indices:02d} indices={index_tuple} "
            f"actions={len(alphabet)} core={audit.core_states} "
            f"fixed={audit.fixed_words} nonfixed={audit.nonfixed_words} "
            f"forced={len(audit.forced_nonfix_words)} status={status}"
        )
        if status == "pass":
            survivors.append((indices, index_tuple, len(alphabet), audit.core_states))
    print(f"free_group_survivors={len(survivors)}/40")
    for survivor in survivors:
        print(f"survivor={survivor}")
    universal_forced = set.intersection(*forced_word_sets)
    print(f"universal_forced_words={sorted(universal_forced)!r}")
    assert first_direct_conflicts is not None
    alphabet, direct_conflicts = first_direct_conflicts
    for conflict in direct_conflicts:
        word = "".join(alphabet[symbol] for symbol in conflict.fixed.word)
        if word not in universal_forced:
            continue
        print(
            f"direct_certificate word={word!r} "
            f"fixed={conflict.fixed.trace}:"
            f"{conflict.fixed.start}->{conflict.fixed.end} "
            f"nonfixed={conflict.nonfixed.trace}:"
            f"{conflict.nonfixed.start}->{conflict.nonfixed.end}"
        )


if __name__ == "__main__":
    main()
