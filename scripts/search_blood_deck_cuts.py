#!/usr/bin/env python3
"""Test blood-pool row widths/edges as 26 plaintext-selected deck cuts."""

from __future__ import annotations

import argparse
import heapq
from dataclasses import dataclass

from eye_mystery.blood_deck import blood_cut_vectors, cut_letter_map
from eye_mystery.corpus import (
    MESSAGE_ORDER,
    MESSAGES,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)
from eye_mystery.deck_shuffles import standard_base_candidates


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(permutation)
    for position, value in enumerate(permutation):
        result[value] = position
    return tuple(result)


def candidate_bases() -> tuple[tuple[str, tuple[int, ...]], ...]:
    seen: set[tuple[int, ...]] = set()
    result: list[tuple[str, tuple[int, ...]]] = []
    raw = [("identity", tuple(range(83))), *standard_base_candidates(83)]
    for name, base in raw:
        for suffix, candidate in (("", base), ("-inverse", inverse(base))):
            if candidate in seen:
                continue
            seen.add(candidate)
            result.append((name + suffix, candidate))
    return tuple(result)


def decode_prefix(
    ciphertext: tuple[int, ...],
    base: tuple[int, ...],
    letter_for_cut: dict[int, int],
    *,
    base_first: bool,
    descending: bool,
) -> tuple[int, tuple[int, ...]]:
    size = len(base)
    deck = tuple(range(size - 1, -1, -1)) if descending else tuple(range(size))
    plaintext: list[int] = []
    for card in ciphertext:
        if base_first:
            deck = tuple(deck[position] for position in base)
            cut = deck.index(card)
            letter = letter_for_cut.get(cut)
            if letter is None:
                break
            deck = deck[cut:] + deck[:cut]
        else:
            rank = deck.index(card)
            cut = (rank - base[0]) % size
            letter = letter_for_cut.get(cut)
            if letter is None:
                break
            rotated = deck[cut:] + deck[:cut]
            deck = tuple(rotated[position] for position in base)
        plaintext.append(letter)
    return len(plaintext), tuple(plaintext)


def split_message(
    message: tuple[int, ...], lengths: tuple[int, ...]
) -> tuple[tuple[int, ...], ...]:
    result = []
    cursor = 0
    for length in lengths:
        result.append(message[cursor : cursor + length])
        cursor += length
    if cursor != len(message):
        raise ValueError("row-pair lengths do not consume the message")
    return tuple(result)


@dataclass(frozen=True)
class Result:
    matched: int
    possible: int
    min_fraction: float
    vector: str
    reverse_cuts: bool
    base_first: bool
    descending: bool
    marker_mode: str
    base: str
    plaintexts: tuple[tuple[int, ...], ...]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    raw_messages = tuple(
        trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    )
    bases = candidate_bases()
    vectors = blood_cut_vectors()
    best: list[tuple[tuple[float, int], int, Result]] = []
    serial = 0
    tested = 0
    exact: list[Result] = []
    for vector_name in ("end", "span", "count"):
        cuts = vectors[vector_name]
        for reverse_cuts in (False, True):
            letter_for_cut = cut_letter_map(cuts, reverse=reverse_cuts)
            for base_first in (False, True):
                for descending in (False, True):
                    for marker_mode in ("full", "body", "rows", "body-rows"):
                        segmented_messages = []
                        for name, message in zip(
                            MESSAGE_ORDER, raw_messages, strict=True
                        ):
                            if marker_mode == "full":
                                segmented_messages.append((message,))
                            elif marker_mode == "body":
                                segmented_messages.append((message[1:],))
                            else:
                                segments = list(
                                    split_message(
                                        message, ROW_PAIR_TRIGRAM_LENGTHS[name]
                                    )
                                )
                                if marker_mode == "body-rows":
                                    segments[0] = segments[0][1:]
                                segmented_messages.append(tuple(segments))
                        possible = sum(
                            len(segment)
                            for segments in segmented_messages
                            for segment in segments
                        )
                        for base_name, base in bases:
                            decoded_rows = tuple(
                                tuple(
                                    decode_prefix(
                                        segment,
                                        base,
                                        letter_for_cut,
                                        base_first=base_first,
                                        descending=descending,
                                    )
                                    for segment in segments
                                )
                                for segments in segmented_messages
                            )
                            lengths = tuple(
                                sum(length for length, _ in rows)
                                for rows in decoded_rows
                            )
                            message_lengths = tuple(
                                sum(map(len, segments))
                                for segments in segmented_messages
                            )
                            result = Result(
                                matched=sum(lengths),
                                possible=possible,
                                min_fraction=min(
                                    length / message_length
                                    for length, message_length in zip(
                                        lengths, message_lengths, strict=True
                                    )
                                ),
                                vector=vector_name,
                                reverse_cuts=reverse_cuts,
                                base_first=base_first,
                                descending=descending,
                                marker_mode=marker_mode,
                                base=base_name,
                                plaintexts=tuple(
                                    tuple(
                                        value
                                        for _, text in rows
                                        for value in text
                                    )
                                    for rows in decoded_rows
                                ),
                            )
                            if result.matched == possible:
                                exact.append(result)
                            key = (result.min_fraction, result.matched)
                            item = (key, serial, result)
                            serial += 1
                            if len(best) < args.top:
                                heapq.heappush(best, item)
                            elif item > best[0]:
                                heapq.heapreplace(best, item)
                            tested += 1

    print(f"tested: {tested} candidates ({len(bases)} distinct bases)")
    print(f"exact survivors: {len(exact)}")
    print("minfrac matched vector reverse order initial marker base")
    for _, _, result in sorted(best, reverse=True):
        order = "base-cut" if result.base_first else "cut-base"
        initial = "desc" if result.descending else "asc"
        print(
            f"{result.min_fraction:>7.4f} "
            f"{result.matched:>4}/{result.possible:<4} "
            f"{result.vector:<5} {str(result.reverse_cuts):<5} "
            f"{order:<8} {initial:<4} {result.marker_mode:<4} {result.base}"
        )
        if result.matched == result.possible:
            for name, plaintext in zip(
                MESSAGE_ORDER, result.plaintexts, strict=True
            ):
                print(f"  {name}: {''.join(chr(value + 65) for value in plaintext)}")


if __name__ == "__main__":
    main()
