#!/usr/bin/env python3
"""Audit literal implementations of the public Practice Cipher #5 hints."""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable

from eye_mystery.practice_cipher5 import (
    REVISED_SECTIONS,
    decode_dynamic_substitution,
    interleave_packets,
    recursive_fixed_interleave,
    recursive_increasing_interleaves,
)


Permutation = tuple[int, ...]
Factory = Callable[[int, int], Permutation]


def chunks(deck: Permutation, width: int) -> tuple[Permutation, ...]:
    return tuple(deck[start : start + width] for start in range(0, len(deck), width))


def reverse_chunk_order(size: int, index: int) -> Permutation:
    packets = chunks(tuple(range(size)), index + 1)
    return tuple(value for packet in reversed(packets) for value in packet)


def reverse_each_chunk(size: int, index: int) -> Permutation:
    packets = chunks(tuple(range(size)), index + 1)
    return tuple(value for packet in packets for value in reversed(packet))


def transpose_chunks(size: int, index: int, *, reverse_packets: bool = False) -> Permutation:
    packets = list(chunks(tuple(range(size)), index + 1))
    if reverse_packets:
        packets.reverse()
    return tuple(
        packet[column]
        for column in range(index + 1)
        for packet in packets
        if column < len(packet)
    )


def single_interleave(size: int, index: int, *, right_first: bool) -> Permutation:
    return interleave_packets(
        tuple(range(size)), index + 1, right_first=right_first
    )


def cumulative_layer(
    size: int,
    index: int,
    *,
    transform: str,
    descending: bool,
) -> Permutation:
    deck = tuple(range(size))
    splits = tuple(range(index + 1, size))
    if descending:
        splits = tuple(reversed(splits))
    for split in splits:
        left, right = deck[:split], deck[split:]
        if transform == "cut":
            deck = right + left
        elif transform == "reverse-left":
            deck = tuple(reversed(left)) + right
        elif transform == "reverse-right":
            deck = left + tuple(reversed(right))
        elif transform == "reverse-both":
            deck = tuple(reversed(left)) + tuple(reversed(right))
        elif transform == "swap-reverse":
            deck = tuple(reversed(right)) + tuple(reversed(left))
        else:
            raise ValueError(transform)
    return deck


def factories() -> tuple[tuple[str, Factory], ...]:
    result: list[tuple[str, Factory]] = [
        ("reverse-chunk-order", reverse_chunk_order),
        ("reverse-each-chunk", reverse_each_chunk),
        ("transpose-chunks", transpose_chunks),
        (
            "transpose-reverse-packets",
            lambda size, index: transpose_chunks(
                size, index, reverse_packets=True
            ),
        ),
    ]
    for right_first in (False, True):
        result.append(
            (
                f"single-interleave-{'right' if right_first else 'left'}",
                lambda size, index, rf=right_first: single_interleave(
                    size, index, right_first=rf
                ),
            )
        )
    for transform in (
        "cut",
        "reverse-left",
        "reverse-right",
        "reverse-both",
        "swap-reverse",
    ):
        for descending in (False, True):
            result.append(
                (
                    f"cumulative-{transform}-{'down' if descending else 'up'}",
                    lambda size, index, t=transform, d=descending: cumulative_layer(
                        size, index, transform=t, descending=d
                    ),
                )
            )
    for family_name, family in (
        ("increasing-interleave", recursive_increasing_interleaves),
        ("fixed-interleave", recursive_fixed_interleave),
    ):
        for right_first in (False, True):
            for recurse_first in (False, True):
                result.append(
                    (
                        f"{family_name}-{'right' if right_first else 'left'}-"
                        f"{'unwind' if recurse_first else 'descent'}",
                        lambda size, index, f=family, rf=right_first, rec=recurse_first: f(
                            size,
                            index,
                            one_based=True,
                            right_first=rf,
                            recurse_first=rec,
                        ),
                    )
                )
    return tuple(result)


def normalized_ioc(streams: tuple[tuple[int, ...], ...], size: int = 83) -> float:
    counts = Counter(value for stream in streams for value in stream)
    total = sum(counts.values())
    return (
        sum(count * (count - 1) for count in counts.values())
        / (total * (total - 1) / size)
    )


def main() -> None:
    ciphertexts = tuple(
        tuple(ord(character) - 33 for character in section)
        for section in REVISED_SECTIONS
    )
    results = []
    for name, factory in factories():
        operations = tuple(factory(83, index) for index in range(83))
        if len(set(operations)) != 83:
            continue
        plaintexts = tuple(
            decode_dynamic_substitution(ciphertext, operations)[1:]
            for ciphertext in ciphertexts
        )
        unique = len(set().union(*map(set, plaintexts)))
        ioc = normalized_ioc(plaintexts)
        results.append((unique, -ioc, name, ioc, plaintexts[0][:24]))
    print("unique  norm-IoC family first-body-indexes")
    for unique, _, name, ioc, start in sorted(results):
        print(f"{unique:>6} {ioc:>9.4f} {name:<45} {start}")


if __name__ == "__main__":
    main()
