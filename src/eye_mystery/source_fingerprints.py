"""Exact repeated-plaintext fingerprints for testing candidate source corpora."""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from html.parser import HTMLParser


class _CardBodyParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.card_depth = 0
        self.suppressed_depth = 0
        self.fragments: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = dict(attrs).get("class", "") or ""
        if self.card_depth:
            if tag == "div":
                self.card_depth += 1
            if tag in {"script", "style"}:
                self.suppressed_depth += 1
        elif tag == "div" and "card-body" in classes.split():
            self.card_depth = 1

    def handle_endtag(self, tag: str) -> None:
        if not self.card_depth:
            return
        if tag in {"script", "style"} and self.suppressed_depth:
            self.suppressed_depth -= 1
        if tag == "div":
            self.card_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.card_depth and not self.suppressed_depth:
            self.fragments.append(data)


def extract_card_body(html: str) -> str:
    """Extract visible prose from alchemy-texts.com-style card bodies."""

    parser = _CardBodyParser()
    parser.feed(html)
    return " ".join(parser.fragments)


def normalize_source(
    text: str, mode: str = "letters", *, transliterate_finnish: bool = False
) -> str:
    if transliterate_finnish:
        text = text.translate(
            str.maketrans(
                {
                    "ä": "a",
                    "ö": "o",
                    "å": "a",
                    "Ä": "A",
                    "Ö": "O",
                    "Å": "A",
                }
            )
        )
    if mode == "letters":
        return "".join(re.findall(r"[a-z]", text.lower()))
    if mode == "spaces":
        return " ".join(re.sub(r"[^a-z]+", " ", text.lower()).split())
    raise ValueError("mode must be 'letters' or 'spaces'")


def gap_repeats(text: str, *, length: int, gap: int) -> dict[str, tuple[int, ...]]:
    positions: dict[str, list[int]] = defaultdict(list)
    for start in range(max(0, len(text) - gap - length + 1)):
        block = text[start : start + length]
        if block == text[start + gap : start + gap + length]:
            positions[block].append(start)
    return {block: tuple(values) for block, values in positions.items()}


@dataclass(frozen=True)
class FirstFamilySourceMatch:
    block: str
    gap30: tuple[tuple[str, int], ...]
    gap35: tuple[tuple[str, int], ...]
    inner_gap28: tuple[tuple[str, int], ...]


def first_family_source_matches(
    texts: Mapping[str, str]
) -> tuple[FirstFamilySourceMatch, ...]:
    """Find the exact 18/30, 18/35, nested 9/28 Eye fingerprint."""

    def collect(length: int, gap: int):
        result: dict[str, list[tuple[str, int]]] = defaultdict(list)
        for name, text in texts.items():
            for block, positions in gap_repeats(
                text, length=length, gap=gap
            ).items():
                result[block].extend((name, position) for position in positions)
        return result

    gap30 = collect(18, 30)
    gap35 = collect(18, 35)
    inner_gap28 = collect(9, 28)
    matches = []
    for block in gap30.keys() & gap35.keys():
        inner = block[6:15]
        if inner in inner_gap28:
            matches.append(
                FirstFamilySourceMatch(
                    block,
                    tuple(gap30[block]),
                    tuple(gap35[block]),
                    tuple(inner_gap28[inner]),
                )
            )
    return tuple(sorted(matches, key=lambda match: match.block))


def repeated_blocks(
    texts: Mapping[str, str], *, length: int, minimum_occurrences: int
) -> dict[str, tuple[tuple[str, int], ...]]:
    occurrences: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for name, text in texts.items():
        local: dict[str, list[int]] = defaultdict(list)
        for start in range(max(0, len(text) - length + 1)):
            local[text[start : start + length]].append(start)
        for block, positions in local.items():
            if len(positions) >= 2:
                occurrences[block].extend((name, position) for position in positions)
    return {
        block: tuple(positions)
        for block, positions in occurrences.items()
        if len(positions) >= minimum_occurrences
    }
