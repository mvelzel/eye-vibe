#!/usr/bin/env python3
"""Test BWT-derived panel orders as one continuous deck-cipher stream."""

from __future__ import annotations

import heapq
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.deck_base import decode_affine_base_swap
from eye_mystery.deck_base_generic import decode_base_top_swap_with_cycles
from eye_mystery.deck_shuffles import (
    is_affine_mod_size,
    standard_base_candidates,
)
from eye_mystery.marker_bwt import (
    marker_bwt_lf_order,
    marker_bwt_plaintext_order,
)
from search_continuous_affine_decks import split_stream
from search_standard_base_decks import mismatch_count


@dataclass(frozen=True)
class Result:
    unique: int
    mismatches: int
    family: str
    order_name: str
    marker_mode: str
    base_name: str

    @property
    def key(self) -> tuple[int, int]:
        return self.unique, self.mismatches


def evaluate(
    decoded: tuple[int, ...],
    order: tuple[str, ...],
    lengths: dict[str, int],
    *,
    omit_markers: bool,
) -> tuple[int, int]:
    streams = split_stream(decoded, order, lengths)
    if omit_markers:
        streams = {name: (None,) + stream for name, stream in streams.items()}
    mismatches, _ = mismatch_count(streams)
    return len(set(decoded)), mismatches


def main() -> None:
    full_messages = {
        name: trigram_values(MESSAGES[name])
        for name in marker_bwt_plaintext_order()
    }
    orders = {
        "bwt-plaintext": marker_bwt_plaintext_order(),
        "bwt-lf": marker_bwt_lf_order(),
    }
    best: list[tuple[tuple[int, int], int, Result]] = []
    serial = 0

    def retain(result: Result) -> None:
        nonlocal serial
        item = ((-result.unique, -result.mismatches), serial, result)
        serial += 1
        if len(best) < 40:
            heapq.heappush(best, item)
        elif item > best[0]:
            heapq.heapreplace(best, item)

    prepared = []
    for order_name, order in orders.items():
        for omit_markers in (False, True):
            messages = {
                name: full_messages[name][1:] if omit_markers else full_messages[name]
                for name in order
            }
            lengths = {name: len(message) for name, message in messages.items()}
            ciphertext = tuple(
                value for name in order for value in messages[name]
            )
            prepared.append(
                (order_name, order, omit_markers, lengths, ciphertext)
            )

    for multiplier in range(1, 83):
        for offset in range(83):
            base_name = f"{multiplier}-{offset}"
            for order_name, order, omit_markers, lengths, ciphertext in prepared:
                decoded = decode_affine_base_swap(
                    ciphertext, multiplier, offset
                )
                unique, mismatches = evaluate(
                    decoded,
                    order,
                    lengths,
                    omit_markers=omit_markers,
                )
                retain(
                    Result(
                        unique,
                        mismatches,
                        "affine",
                        order_name,
                        "body" if omit_markers else "full",
                        base_name,
                    )
                )

    for base_name, base in standard_base_candidates(83):
        if is_affine_mod_size(base):
            continue
        for order_name, order, omit_markers, lengths, ciphertext in prepared:
            decoded = decode_base_top_swap_with_cycles(ciphertext, base)
            unique, mismatches = evaluate(
                decoded,
                order,
                lengths,
                omit_markers=omit_markers,
            )
            retain(
                Result(
                    unique,
                    mismatches,
                    "standard",
                    order_name,
                    "body" if omit_markers else "full",
                    base_name,
                )
            )

    print("tested:", serial)
    print("unique mismatch family order marker base")
    for _, _, result in sorted(best, key=lambda item: item[2].key):
        print(
            f"{result.unique:>6} {result.mismatches:>8} "
            f"{result.family:<8} {result.order_name:<13} "
            f"{result.marker_mode:<4} {result.base_name}"
        )


if __name__ == "__main__":
    main()
