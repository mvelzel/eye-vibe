#!/usr/bin/env python3
"""Test the 1876 Finnish *Lumikki* text as a literal source and skip key.

``Lumikki`` is singled out by a CRC-32/BZIP2 value in the first stored Eye
block.  This script tests the narrow consequences of treating that clue as a
pointer to J. A. Hahnsson's public-domain Finnish translation: exact source
geometry and Cessation-like walks beginning at the story title.
"""

from __future__ import annotations

import heapq
import re
from itertools import permutations
from urllib.request import Request, urlopen

from eye_mystery.corpus import (
    MESSAGE_ORDER,
    MESSAGES,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)
from eye_mystery.ngram import TetragramModel, tetragram_code
from eye_mystery.source_fingerprints import (
    first_family_source_matches,
    normalize_source,
)
from eye_mystery.source_message_tree import SourceEntry, message_tree_matches


SOURCE_URL = "https://www.gutenberg.org/cache/epub/45046/pg45046.txt"


def fetch_source() -> str:
    request = Request(SOURCE_URL, headers={"User-Agent": "Noita-eye-mystery research"})
    return urlopen(request, timeout=60).read().decode("utf-8", errors="ignore")


def extract_lumikki(book: str) -> str:
    start_match = re.search(r"(?m)^Lumikki\.\s*$", book)
    if start_match is None:
        raise ValueError("Lumikki heading not found")
    end_match = re.search(r"(?m)^28\.\s*$", book[start_match.end() :])
    if end_match is None:
        raise ValueError("next story heading not found")
    return book[start_match.start() : start_match.end() + end_match.start()]


def encode_finnish(text: str) -> str:
    return text.translate(
        str.maketrans(
            {"ä": "q", "ö": "x", "å": "z", "Ä": "Q", "Ö": "X", "Å": "Z"}
        )
    )


def letters(text: str) -> str:
    return "".join(character for character in encode_finnish(text).upper() if "A" <= character <= "Z")


def candidate_entries(story: str, mode: str) -> tuple[SourceEntry, ...]:
    fragments = set(story.splitlines())
    fragments.update(re.split(r"(?<=[.!?])\s+", story))
    fragments.update(re.split(r"\n\s*\n", story))
    entries = []
    for index, fragment in enumerate(fragments):
        normalized = normalize_source(
            fragment, mode=mode, transliterate_finnish=True
        ).upper()
        if 90 <= len(normalized) <= 145:
            entries.append(SourceEntry(f"Lumikki fragment {index}", normalized))
    return tuple(entries)


def read_skip_key(
    values: tuple[int, ...],
    key: str,
    *,
    segment_lengths: tuple[int, ...] | None = None,
    reset_value: int | None = None,
) -> str:
    segments = segment_lengths or (len(values),)
    output = []
    start = 0
    for length in segments:
        pointer = -1
        for value in values[start : start + length]:
            if reset_value is not None and value == reset_value:
                pointer = -1
                continue
            if value < 1:
                raise ValueError("skip values must be positive")
            pointer = (pointer + value) % len(key)
            output.append(key[pointer])
        start += length
    if start != len(values):
        raise ValueError("segment lengths do not partition values")
    return "".join(output)


def score_text(model: TetragramModel, text: str) -> tuple[float, int]:
    encoded = letters(text)
    windows = max(0, len(encoded) - 3)
    score = 0.0
    for start in range(windows):
        values = tuple(ord(value) - ord("A") for value in encoded[start : start + 4])
        score += model.log_probabilities[tetragram_code(values)]
    return score, windows


def main() -> None:
    book = fetch_source()
    story = extract_lumikki(book)
    key = letters(story)
    model = TetragramModel.train(encode_finnish(book))

    print("source:", SOURCE_URL)
    print("story characters:", len(story), "normalized letters:", len(key))
    for mode in ("letters", "spaces"):
        normalized = normalize_source(
            story, mode=mode, transliterate_finnish=True
        )
        fingerprints = first_family_source_matches({"Lumikki": normalized})
        entries = candidate_entries(story, mode)
        trees = message_tree_matches(entries)
        print(
            f"literal mode={mode}: entries={len(entries)} "
            f"message-trees={len(trees)} first-family-fingerprints={len(fingerprints)}"
        )

    full_raw = {name: MESSAGES[name] for name in MESSAGE_ORDER}
    body_raw = {name: MESSAGES[name][3:] for name in MESSAGE_ORDER}
    full_trigrams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    body_trigrams = {
        name: full_trigrams[name][1:] for name in MESSAGE_ORDER
    }
    best: list[tuple[float, int, str, tuple[str, ...]]] = []
    serial = 0

    def record(
        description: str,
        streams: dict[str, tuple[int, ...]],
        *,
        segments: dict[str, tuple[int, ...]] | None = None,
        reset_value: int | None = None,
        reverse: bool,
    ) -> None:
        nonlocal serial
        source_key = key[::-1] if reverse else key
        texts = tuple(
            read_skip_key(
                streams[name],
                source_key,
                segment_lengths=None if segments is None else segments[name],
                reset_value=reset_value,
            )
            for name in MESSAGE_ORDER
        )
        totals = tuple(score_text(model, text) for text in texts)
        score = sum(total for total, _ in totals) / max(
            1, sum(windows for _, windows in totals)
        )
        item = (score, serial, f"{description} reverse={reverse}", texts)
        serial += 1
        if len(best) < 15:
            heapq.heappush(best, item)
        elif item > best[0]:
            heapq.heapreplace(best, item)

    for reverse in (False, True):
        for marker_mode, raw_streams, trigram_streams in (
            ("full", full_raw, full_trigrams),
            ("body", body_raw, body_trigrams),
        ):
            trigram_segments = {
                name: (
                    ROW_PAIR_TRIGRAM_LENGTHS[name]
                    if marker_mode == "full"
                    else (ROW_PAIR_TRIGRAM_LENGTHS[name][0] - 1,)
                    + ROW_PAIR_TRIGRAM_LENGTHS[name][1:]
                )
                for name in MESSAGE_ORDER
            }
            raw_segments = {
                name: tuple(3 * length for length in trigram_segments[name])
                for name in MESSAGE_ORDER
            }
            raw_sum_plus_one = {
                name: tuple(
                    1 + sum(raw_streams[name][start : start + 3])
                    for start in range(0, len(raw_streams[name]), 3)
                )
                for name in MESSAGE_ORDER
            }
            trigram_plus_one = {
                name: tuple(value + 1 for value in trigram_streams[name])
                for name in MESSAGE_ORDER
            }
            for description, streams, segments in (
                ("raw-sum-plus-one", raw_sum_plus_one, None),
                ("raw-sum-plus-one row-reset", raw_sum_plus_one, trigram_segments),
                ("trigram-plus-one", trigram_plus_one, None),
                ("trigram-plus-one row-reset", trigram_plus_one, trigram_segments),
            ):
                record(
                    f"{description} mode={marker_mode}",
                    streams,
                    segments=segments,
                    reverse=reverse,
                )
            if marker_mode == "full":
                record(
                    "trigram-zero-reset mode=full",
                    trigram_streams,
                    reset_value=0,
                    reverse=reverse,
                )
                record(
                    "trigram-zero-reset mode=full row-reset",
                    trigram_streams,
                    segments=trigram_segments,
                    reset_value=0,
                    reverse=reverse,
                )

            for positive_steps in permutations(range(1, 6)):
                mapped = {
                    name: tuple(positive_steps[value] for value in raw_streams[name])
                    for name in MESSAGE_ORDER
                }
                triple_steps = {
                    name: tuple(
                        sum(mapped[name][start : start + 3])
                        for start in range(0, len(mapped[name]), 3)
                    )
                    for name in MESSAGE_ORDER
                }
                for description, streams, segments in (
                    ("raw-positive", mapped, None),
                    ("raw-positive row-reset", mapped, raw_segments),
                    ("raw-triple-read", triple_steps, None),
                    ("raw-triple-read row-reset", triple_steps, trigram_segments),
                ):
                    record(
                        f"{description} map={positive_steps} mode={marker_mode}",
                        streams,
                        segments=segments,
                        reverse=reverse,
                    )

    reference = key[-1036:]
    reference_total, reference_windows = score_text(model, reference)
    print("skip-key mechanisms:", serial)
    print("held-in Finnish reference:", f"{reference_total / reference_windows:.4f}")
    print("best candidates:")
    display = str.maketrans({"Q": "Ä", "X": "Ö", "Z": "Å"})
    for score, _, description, texts in sorted(best, reverse=True):
        previews = " / ".join(text[:75] for text in texts[:3]).translate(display)
        print(f"  score={score:.4f} {description}")
        print("   ", previews)


if __name__ == "__main__":
    main()
