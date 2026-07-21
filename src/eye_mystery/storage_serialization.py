"""Reconstruct the Eye renderer's base-seven storage layer.

The visible direction rows are encoded as digits ``1..6`` (five directions
plus newline), followed by a zero padding digit, and greedily packed into an
unsigned 64-bit integer.  The functions here make that storage convention
independently reproducible from the accepted visible corpus.
"""

from __future__ import annotations

import hashlib
import struct
from collections.abc import Iterable, Sequence

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, ROW_PAIR_TRIGRAM_LENGTHS
from eye_mystery.visual_rows import visual_rows


MAX_U64 = (1 << 64) - 1
MAX_VISIBLE_SYMBOLS = 22


def storage_stream(name: str) -> tuple[int, ...]:
    """Return visual rows with the renderer's newline symbol after each row."""
    result: list[int] = []
    rows = visual_rows(MESSAGES[name], ROW_PAIR_TRIGRAM_LENGTHS[name])
    for row in rows:
        result.extend(row)
        result.append(5)
    return tuple(result)


def encode_storage_chunk(symbols: Sequence[int]) -> int:
    """Encode one nonempty storage-symbol chunk with its trailing zero digit."""
    if not symbols:
        raise ValueError("a storage chunk cannot be empty")
    value = 0
    for symbol in symbols:
        if not 0 <= symbol <= 5:
            raise ValueError("storage symbols must lie in 0..5")
        value = 7 * value + symbol + 1
    value *= 7
    if value > MAX_U64:
        raise OverflowError("storage chunk does not fit in 64 bits")
    return value


def decode_storage_chunk(value: int) -> tuple[int, ...]:
    """Invert one packed word, rejecting absent padding and unused zero digits."""
    if not 0 < value <= MAX_U64 or value % 7:
        raise ValueError("packed storage word must be a positive multiple of seven")
    value //= 7
    reversed_symbols: list[int] = []
    while value:
        digit = value % 7
        if digit == 0:
            raise ValueError("authored chunks do not contain the unused -1 symbol")
        reversed_symbols.append(digit - 1)
        value //= 7
    return tuple(reversed(reversed_symbols))


def greedy_pack_storage(symbols: Sequence[int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Pack the longest available prefix that fits into each 64-bit word."""
    words: list[int] = []
    lengths: list[int] = []
    cursor = 0
    while cursor < len(symbols):
        upper = min(MAX_VISIBLE_SYMBOLS, len(symbols) - cursor)
        for length in range(upper, 0, -1):
            try:
                word = encode_storage_chunk(symbols[cursor : cursor + length])
            except OverflowError:
                continue
            break
        else:  # pragma: no cover - one symbol always fits
            raise AssertionError("failed to pack a storage symbol")
        words.append(word)
        lengths.append(length)
        cursor += length
    return tuple(words), tuple(lengths)


def corpus_packed_words() -> tuple[int, ...]:
    """Derive all 150 engine words from the visible corpus alone."""
    return tuple(
        word
        for name in MESSAGE_ORDER
        for word in greedy_pack_storage(storage_stream(name))[0]
    )


def packed_words_sha256(words: Iterable[int]) -> str:
    """Hash packed words as little-endian u64 values in message order."""
    digest = hashlib.sha256()
    for word in words:
        digest.update(struct.pack("<Q", word))
    return digest.hexdigest()


def nonfinal_capacity_bits() -> tuple[int, ...]:
    """Encode nonfinal chunk lengths as 21=1 and 22=0 in message order."""
    result: list[int] = []
    for name in MESSAGE_ORDER:
        _, lengths = greedy_pack_storage(storage_stream(name))
        if any(length not in (21, 22) for length in lengths[:-1]):
            raise AssertionError("a nonfinal chunk was not capacity-sized")
        result.extend(1 if length == 21 else 0 for length in lengths[:-1])
    return tuple(result)
