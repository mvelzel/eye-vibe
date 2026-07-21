#!/usr/bin/env python3
"""Test the nine Orb-lore passages as cyclic keys for the nine Eyes."""

from __future__ import annotations

import argparse
import heapq
from itertools import permutations
from pathlib import Path
from urllib.request import Request, urlopen

from eye_mystery.corpus import (
    MESSAGE_ORDER,
    MESSAGES,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)
from eye_mystery.ngram import TetragramModel, tetragram_code
from eye_mystery.noita_lore import ORB_LORE_KEYS


def normalize_finnish(text: str) -> str:
    return text.translate(
        str.maketrans(
            {
                "ä": "q",
                "ö": "x",
                "å": "z",
                "Ä": "Q",
                "Ö": "X",
                "Å": "Z",
            }
        )
    )


def load_corpus(paths: list[Path], urls: list[str]) -> str:
    parts = [path.read_text(errors="ignore") for path in paths]
    for url in urls:
        request = Request(url, headers={"User-Agent": "Noita-eye-mystery research"})
        parts.append(
            urlopen(request, timeout=60).read().decode("utf-8", errors="ignore")
        )
    return normalize_finnish("\n".join(parts))


def read_skip_key(
    values: tuple[int, ...],
    key: str,
    *,
    reset_value: int | None = None,
) -> str:
    pointer = -1
    output = []
    for value in values:
        if reset_value is not None and value == reset_value:
            pointer = -1
            continue
        if value < 1:
            raise ValueError("skip values must be positive")
        pointer = (pointer + value) % len(key)
        output.append(key[pointer])
    return "".join(output)


def read_segmented_skip_key(
    values: tuple[int, ...],
    key: str,
    segment_lengths: tuple[int, ...] | None,
    *,
    reset_value: int | None = None,
) -> str:
    if segment_lengths is None:
        return read_skip_key(values, key, reset_value=reset_value)
    if sum(segment_lengths) != len(values):
        raise ValueError("segment lengths must partition the values")
    output = []
    start = 0
    for length in segment_lengths:
        output.append(
            read_skip_key(
                values[start : start + length],
                key,
                reset_value=reset_value,
            )
        )
        start += length
    return "".join(output)


def score_text(model: TetragramModel, raw_text: str) -> tuple[float, int]:
    text = "".join(
        character
        for character in normalize_finnish(raw_text).upper()
        if "A" <= character <= "Z"
    )
    total = 0.0
    windows = max(0, len(text) - 3)
    for start in range(windows):
        values = tuple(ord(character) - ord("A") for character in text[start : start + 4])
        total += model.log_probabilities[tetragram_code(values)]
    return total, windows


def best_assignment(matrix: tuple[tuple[float, ...], ...]) -> tuple[float, tuple[int, ...]]:
    """Maximum-weight one-to-one message-to-key assignment by subset DP."""

    states = {0: (0.0, ())}
    for row in matrix:
        next_states = {}
        for mask, (score, assignment) in states.items():
            for key_index, value in enumerate(row):
                bit = 1 << key_index
                if mask & bit:
                    continue
                candidate = (score + value, assignment + (key_index,))
                old = next_states.get(mask | bit)
                if old is None or candidate[0] > old[0]:
                    next_states[mask | bit] = candidate
        states = next_states
    return states[(1 << len(matrix)) - 1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language-corpus", type=Path, action="append", default=[])
    parser.add_argument("--language-corpus-url", action="append", default=[])
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args()
    if not args.language_corpus and not args.language_corpus_url:
        raise SystemExit("provide at least one Finnish language corpus")

    corpus = load_corpus(args.language_corpus, args.language_corpus_url)
    model = TetragramModel.train(corpus)
    full_raw = {name: MESSAGES[name] for name in MESSAGE_ORDER}
    body_raw = {name: MESSAGES[name][3:] for name in MESSAGE_ORDER}
    full_trigrams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    body_trigrams = {
        name: full_trigrams[name][1:] for name in MESSAGE_ORDER
    }
    keys = tuple(key for _, key in ORB_LORE_KEYS)

    best = []
    serial = 0

    def record(
        description: str,
        streams: dict[str, tuple[int, ...]],
        reset_value=None,
        segment_lengths: dict[str, tuple[int, ...]] | None = None,
    ):
        nonlocal serial
        texts = tuple(
            tuple(
                read_segmented_skip_key(
                    streams[name],
                    key[::-1] if reverse else key,
                    None if segment_lengths is None else segment_lengths[name],
                    reset_value=reset_value,
                )
                for key in keys
            )
            for name in MESSAGE_ORDER
        )
        scored = tuple(
            tuple(score_text(model, text)[0] for text in row) for row in texts
        )
        score, assignment = best_assignment(scored)
        windows = sum(
            score_text(model, texts[row][key_index])[1]
            for row, key_index in enumerate(assignment)
        )
        item = (
            score / max(1, windows),
            serial,
            f"{description} reverse-keys={reverse}",
            assignment,
            texts,
        )
        serial += 1
        if len(best) < args.top:
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
            sum_plus_one = {
                name: tuple(
                    1 + sum(raw_streams[name][start : start + 3])
                    for start in range(0, len(raw_streams[name]), 3)
                )
                for name in MESSAGE_ORDER
            }
            record(
                f"raw-sum-plus-one mode={marker_mode}",
                sum_plus_one,
            )
            record(
                f"raw-sum-plus-one mode={marker_mode} row-reset",
                sum_plus_one,
                segment_lengths=trigram_segments,
            )
            plus_one = {
                name: tuple(value + 1 for value in trigram_streams[name])
                for name in MESSAGE_ORDER
            }
            record(f"trigram-plus-one mode={marker_mode}", plus_one)
            record(
                f"trigram-plus-one mode={marker_mode} row-reset",
                plus_one,
                segment_lengths=trigram_segments,
            )
            if marker_mode == "full":
                record(
                    "trigram-zero-reset mode=full",
                    trigram_streams,
                    reset_value=0,
                )
                record(
                    "trigram-zero-reset mode=full row-reset",
                    trigram_streams,
                    reset_value=0,
                    segment_lengths=trigram_segments,
                )

        for positive_steps in permutations(range(1, 6)):
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
                mapped = {
                    name: tuple(positive_steps[value] for value in raw_streams[name])
                    for name in MESSAGE_ORDER
                }
                record(
                    f"raw-positive map={positive_steps} mode={marker_mode}",
                    mapped,
                )
                raw_segments = {
                    name: tuple(3 * length for length in trigram_segments[name])
                    for name in MESSAGE_ORDER
                }
                record(
                    f"raw-positive map={positive_steps} mode={marker_mode} row-reset",
                    mapped,
                    segment_lengths=raw_segments,
                )
                triple_steps = {
                    name: tuple(
                        sum(mapped[name][start : start + 3])
                        for start in range(0, len(mapped[name]), 3)
                    )
                    for name in MESSAGE_ORDER
                }
                record(
                    f"raw-triple-read map={positive_steps} mode={marker_mode}",
                    triple_steps,
                )
                record(
                    f"raw-triple-read map={positive_steps} mode={marker_mode} row-reset",
                    triple_steps,
                    segment_lengths=trigram_segments,
                )

    reference = normalize_finnish(corpus)[-1036:]
    reference_total, reference_windows = score_text(model, reference)
    print("Orb lore key lengths:")
    print("  " + ", ".join(f"{name}={len(key)}" for name, key in ORB_LORE_KEYS))
    print("mechanisms/assignments optimized:", serial)
    print("held-in Finnish reference:", f"{reference_total / reference_windows:.4f}")
    print("best candidates:")
    display = str.maketrans({"Q": "Ä", "X": "Ö", "Z": "Å"})
    for score, _, description, assignment, texts in sorted(best, reverse=True):
        print(f"  score={score:.4f} {description}")
        for row, key_index in enumerate(assignment[:3]):
            name = MESSAGE_ORDER[row]
            key_name = ORB_LORE_KEYS[key_index][0]
            preview = texts[row][key_index][:100].translate(display)
            print(f"    {name} <- {key_name}: {preview}")


if __name__ == "__main__":
    main()
