#!/usr/bin/env python3
"""Scan standard bases under every continuous cyclic panel ordering."""

from __future__ import annotations

import heapq
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.deck_base_generic import decode_base_top_swap_with_cycles
from eye_mystery.deck_shuffles import is_affine_mod_size, standard_base_candidates
from search_continuous_affine_decks import split_stream
from search_standard_base_decks import mismatch_count


@dataclass(frozen=True)
class Result:
    unique: int
    mismatches: int
    rotation: int
    base_name: str

    @property
    def key(self):
        return self.unique, self.mismatches


def main() -> None:
    messages = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    lengths = {name: len(message) for name, message in messages.items()}
    streams = []
    for rotation in range(len(MESSAGE_ORDER)):
        order = MESSAGE_ORDER[rotation:] + MESSAGE_ORDER[:rotation]
        ciphertext = tuple(
            value for name in order for value in messages[name]
        )
        streams.append((order, ciphertext))

    best: list[tuple[tuple[int, int], int, Result]] = []
    serial = 0
    for base_name, base in standard_base_candidates(83):
        # The complete affine-on-83 family is scanned independently by
        # search_continuous_affine_decks.py.  Keep this count aligned with the
        # 8,430 non-duplicate physical/near-size bases in the reset scan.
        if is_affine_mod_size(base):
            continue
        for rotation, (order, ciphertext) in enumerate(streams):
            decoded = decode_base_top_swap_with_cycles(ciphertext, base)
            split = split_stream(decoded, order, lengths)
            mismatches, _ = mismatch_count(split)
            result = Result(
                len(set(decoded)), mismatches, rotation, base_name
            )
            item = (
                (-result.unique, -result.mismatches),
                serial,
                result,
            )
            serial += 1
            if len(best) < 30:
                heapq.heappush(best, item)
            elif item > best[0]:
                heapq.heapreplace(best, item)

    print(f"tested={serial}")
    print("unique mismatch start base")
    for _, _, result in sorted(best, key=lambda item: item[2].key):
        print(
            f"{result.unique:>6} {result.mismatches:>8} "
            f"{MESSAGE_ORDER[result.rotation]:>5} {result.base_name}"
        )


if __name__ == "__main__":
    main()
