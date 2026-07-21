#!/usr/bin/env python3
"""Audit whether the renderer's u64 chunk divisions carry extra metadata."""

from __future__ import annotations

import random

from eye_mystery.corpus import MESSAGE_ORDER
from eye_mystery.storage_serialization import (
    corpus_packed_words,
    greedy_pack_storage,
    nonfinal_capacity_bits,
    packed_words_sha256,
    storage_stream,
)


def best_printable(bits: tuple[int, ...]) -> tuple[int, int, tuple[int, int, int, int]]:
    """Optimize only reversal, inversion, byte order, and bit offset."""
    best = (-1, -1, (0, 0, 0, 0))
    for reverse in (0, 1):
        ordered = bits[::-1] if reverse else bits
        for invert in (0, 1):
            transformed = tuple(bit ^ invert for bit in ordered)
            for offset in range(8):
                for little_endian in (0, 1):
                    values = []
                    for start in range(offset, len(bits) - 7, 8):
                        byte = transformed[start : start + 8]
                        if little_endian:
                            byte = byte[::-1]
                        values.append(
                            sum(bit << (7 - index) for index, bit in enumerate(byte))
                        )
                    printable = sum(
                        32 <= value < 127 or value in (9, 10, 13)
                        for value in values
                    )
                    candidate = (
                        printable,
                        len(values),
                        (reverse, invert, offset, little_endian),
                    )
                    if candidate > best:
                        best = candidate
    return best


def main() -> None:
    all_lengths = []
    final_lengths = []
    ends_at_newline = 0
    crosses_newline = 0
    for name in MESSAGE_ORDER:
        stream = storage_stream(name)
        _, lengths = greedy_pack_storage(stream)
        all_lengths.extend(lengths[:-1])
        final_lengths.append(lengths[-1])
        cursor = 0
        for length in lengths:
            chunk = stream[cursor : cursor + length]
            ends_at_newline += chunk[-1] == 5
            crosses_newline += 5 in chunk[:-1]
            cursor += length

    words = corpus_packed_words()
    print(f"packed words                 {len(words)}")
    print(f"verified fixture sha256      {packed_words_sha256(words)}")
    print(
        "nonfinal capacity lengths    "
        f"21:{all_lengths.count(21)} 22:{all_lengths.count(22)}"
    )
    print(f"final lengths                {final_lengths}")
    print(f"boundaries ending at newline {ends_at_newline}")
    print(f"chunks crossing newline      {crosses_newline}")

    bits = nonfinal_capacity_bits()
    observed = best_printable(bits)
    randomizer = random.Random(20260721)
    exceed = 0
    trials = 10_000
    for _ in range(trials):
        control = [0] * len(bits)
        for index in randomizer.sample(range(len(bits)), sum(bits)):
            control[index] = 1
        if best_printable(tuple(control))[0] >= observed[0]:
            exceed += 1
    print(
        "best capacity-bit printable "
        f"{observed[0]}/{observed[1]} convention={observed[2]}"
    )
    print(f"fixed-weight null upper tail {(exceed + 1) / (trials + 1):.6f}")


if __name__ == "__main__":
    main()
