#!/usr/bin/env python3
"""Align Hermetic Museum ``THAT WHICH`` pairs to the first Eye family.

The public-domain Internet Archive OCR for Waite's two volumes is supplied by
the caller.  Each source occurrence whose next ``THAT WHICH`` begins at the
observed Eye separation is aligned to the corresponding raw message offset.
The complete source window is then checked against the necessary perfect-
isomorphism condition.

Passing is compatibility, not decryption.  The search is nevertheless stricter
than selecting a sentence after observing one repeated ciphertext window,
because all equal source substrings in the complete aligned message are tested.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
from pathlib import Path
import re

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.isomorphs import pattern

from scripts.check_waite_m3_suffix import repeated_substring_checks


PHRASE = "THAT WHICH"


@dataclass(frozen=True)
class MessageTarget:
    name: str
    first_offset: int
    second_offset: int

    @property
    def gap(self) -> int:
        return self.second_offset - self.first_offset


TARGETS = (
    MessageTarget("east1", 40, 68),
    MessageTarget("west1", 40, 70),
    MessageTarget("east2", 45, 80),
)


@dataclass(frozen=True)
class SourceAlignment:
    source: str
    target: MessageTarget
    phrase_offset: int
    plaintext: str
    check_count: int
    incompatible_count: int
    ciphertext_start: int

    @property
    def compatible(self) -> bool:
        return self.incompatible_count == 0


def normalize_ocr(text: str) -> str:
    """Collapse layout whitespace and undo alphabetic line-wrap hyphens."""

    text = re.sub(r"(?<=[A-Za-z])-\s*\n\s*(?=[A-Za-z])", "", text)
    return re.sub(r"\s+", " ", text).upper().strip()


def phrase_offsets(text: str) -> tuple[int, ...]:
    return tuple(match.start() for match in re.finditer(PHRASE, text))


def align_source(
    source: str,
    text: str,
    target: MessageTarget,
    *,
    ciphertext_start: int = 1,
) -> tuple[SourceAlignment, ...]:
    ciphertext = trigram_values(MESSAGES[target.name])[ciphertext_start:]
    offsets = phrase_offsets(text)
    alignments: list[SourceAlignment] = []
    for first_index, first in enumerate(offsets):
        for second in offsets[first_index + 1 :]:
            if second - first > target.gap:
                break
            if second - first != target.gap:
                continue
            start = first - (target.first_offset - ciphertext_start)
            end = start + len(ciphertext)
            if start < 0 or end > len(text):
                continue
            plaintext = text[start:end]
            checks = repeated_substring_checks(plaintext, ciphertext)
            alignments.append(
                SourceAlignment(
                    source=source,
                    target=target,
                    phrase_offset=first,
                    plaintext=plaintext,
                    check_count=len(checks),
                    incompatible_count=sum(
                        not check.compatible for check in checks
                    ),
                    ciphertext_start=ciphertext_start,
                )
            )
    return tuple(alignments)


def cross_incompatibility_count(
    first_plaintext: str,
    first_ciphertext: tuple[int, ...],
    second_plaintext: str,
    second_ciphertext: tuple[int, ...],
    *,
    min_length: int = 2,
) -> tuple[int, int]:
    """Count maximal equal substrings and incompatible cipher isomorphs."""

    if len(first_plaintext) != len(first_ciphertext):
        raise ValueError("first plaintext and ciphertext lengths differ")
    if len(second_plaintext) != len(second_ciphertext):
        raise ValueError("second plaintext and ciphertext lengths differ")

    total = 0
    incompatible = 0
    for first in range(len(first_plaintext)):
        for second in range(len(second_plaintext)):
            if (
                first
                and second
                and first_plaintext[first - 1] == second_plaintext[second - 1]
            ):
                continue
            length = 0
            while (
                first + length < len(first_plaintext)
                and second + length < len(second_plaintext)
                and first_plaintext[first + length]
                == second_plaintext[second + length]
            ):
                length += 1
            if length < min_length:
                continue
            total += 1
            if pattern(first_ciphertext[first : first + length]) != pattern(
                second_ciphertext[second : second + length]
            ):
                incompatible += 1
    return total, incompatible


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "sources",
        nargs="+",
        type=Path,
        help="plain-text OCR files for the two Hermetic Museum volumes",
    )
    parser.add_argument(
        "--include-marker",
        action="store_true",
        help="treat raw symbol zero as ciphertext rather than a check marker",
    )
    args = parser.parse_args()

    ciphertext_start = 0 if args.include_marker else 1

    alignments: list[SourceAlignment] = []
    for path in args.sources:
        text = normalize_ocr(path.read_text(errors="replace"))
        print(f"source={path} phrase-occurrences={len(phrase_offsets(text))}")
        for target in TARGETS:
            alignments.extend(
                align_source(
                    path.name,
                    text,
                    target,
                    ciphertext_start=ciphertext_start,
                )
            )

    for target in TARGETS:
        candidates = [item for item in alignments if item.target == target]
        compatible = [item for item in candidates if item.compatible]
        print(
            f"{target.name}: gap={target.gap} candidates={len(candidates)} "
            f"compatible={len(compatible)}"
        )
        for item in candidates:
            print(
                f"  {item.source}:{item.phrase_offset} "
                f"checks={item.check_count} "
                f"incompatible={item.incompatible_count} "
                f"plaintext={item.plaintext!r}"
            )

    compatible_by_target = tuple(
        tuple(
            item
            for item in alignments
            if item.target == target and item.compatible
        )
        for target in TARGETS
    )
    joint_count = 0
    rejected_combinations: list[tuple[int, int, str]] = []
    for combination in product(*compatible_by_target):
        cross_checks = 0
        cross_conflicts = 0
        for left_index in range(len(combination)):
            left = combination[left_index]
            left_ciphertext = trigram_values(MESSAGES[left.target.name])[
                ciphertext_start:
            ]
            for right in combination[left_index + 1 :]:
                right_ciphertext = trigram_values(MESSAGES[right.target.name])[
                    ciphertext_start:
                ]
                total, incompatible = cross_incompatibility_count(
                    left.plaintext,
                    left_ciphertext,
                    right.plaintext,
                    right_ciphertext,
                )
                cross_checks += total
                cross_conflicts += incompatible
        locations = ", ".join(
            f"{item.target.name}={item.source}:{item.phrase_offset}"
            for item in combination
        )
        if cross_conflicts:
            rejected_combinations.append(
                (cross_conflicts, cross_checks, locations)
            )
            continue
        joint_count += 1
        print(f"joint-compatible cross-checks={cross_checks}: {locations}")
    print(f"joint-compatible combinations={joint_count}")
    if rejected_combinations:
        print("least-conflicting rejected combinations:")
        for conflicts, checks, locations in sorted(rejected_combinations)[:5]:
            print(
                f"  conflicts={conflicts}/{checks}: {locations}"
            )

    print(
        "verdict: compatible windows survive only a necessary equality-pattern "
        "test; source alignment alone does not recover a cipher key; "
        f"ciphertext-start={ciphertext_start}"
    )


if __name__ == "__main__":
    main()
