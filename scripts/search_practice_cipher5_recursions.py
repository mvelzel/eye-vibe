#!/usr/bin/env python3
"""Search literal recursive two-packet shuffles for Practice Cipher #5.

The revised puzzle emits ``deck[plaintext_index]`` and then applies the
plaintext-selected permutation.  Long bijective isomorphs in its ciphertext
give a key-free oracle: under the intended plaintext-selected shuffle, the
corresponding decoded spans should be identical.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from eye_mystery.practice_cipher5 import (
    ORIGINAL_SECTIONS,
    REVISED_SECTIONS,
    decode_dynamic_substitution,
)


Packet = tuple[int, ...]
Combiner = Callable[[Packet, Packet], Packet]


# High-confidence maximal bijective isomorphs.  Entries are
# (left section, left offset, right section, right offset, length), zero-based.
ANCHORS = (
    (2, 81, 6, 273, 113),
    (1, 81, 2, 170, 89),
    (1, 119, 3, 208, 51),
    (2, 208, 3, 208, 51),
    (0, 62, 1, 104, 36),
    (0, 62, 2, 193, 36),
    (0, 62, 6, 385, 36),
)


def alternate(left: Packet, right: Packet) -> Packet:
    result: list[int] = []
    for index in range(max(len(left), len(right))):
        if index < len(left):
            result.append(left[index])
        if index < len(right):
            result.append(right[index])
    return tuple(result)


def proportional(left: Packet, right: Packet) -> Packet:
    """Stable merge which spreads both packets as evenly as possible."""
    result: list[int] = []
    li = ri = 0
    while li < len(left) or ri < len(right):
        if li == len(left):
            result.append(right[ri])
            ri += 1
        elif ri == len(right):
            result.append(left[li])
            li += 1
        elif (li + 1) / len(left) <= (ri + 1) / len(right):
            result.append(left[li])
            li += 1
        else:
            result.append(right[ri])
            ri += 1
    return tuple(result)


def combiners() -> tuple[tuple[str, Combiner], ...]:
    result: list[tuple[str, Combiner]] = []
    for reverse_left in (False, True):
        for reverse_right in (False, True):
            for swap in (False, True):
                flags = (
                    f"{'r' if reverse_left else 'f'}"
                    f"{'r' if reverse_right else 'f'}"
                    f"-{'RL' if swap else 'LR'}"
                )

                def packets(
                    left: Packet,
                    right: Packet,
                    rl: bool = reverse_left,
                    rr: bool = reverse_right,
                    sw: bool = swap,
                ) -> tuple[Packet, Packet]:
                    a = tuple(reversed(left)) if rl else left
                    b = tuple(reversed(right)) if rr else right
                    return (b, a) if sw else (a, b)

                result.append(
                    (
                        f"concat-{flags}",
                        lambda left, right, p=packets: p(left, right)[0]
                        + p(left, right)[1],
                    )
                )
                result.append(
                    (
                        f"alternate-{flags}",
                        lambda left, right, p=packets: alternate(*p(left, right)),
                    )
                )
                result.append(
                    (
                        f"proportional-{flags}",
                        lambda left, right, p=packets: proportional(*p(left, right)),
                    )
                )
    return tuple(result)


def peel_unwind(size: int, index: int, combine: Combiner, *, one_based: bool) -> Packet:
    width = index + int(one_based)
    width = max(1, width)

    def recurse(deck: Packet) -> Packet:
        if len(deck) <= width:
            return deck
        return combine(deck[:width], recurse(deck[width:]))

    return recurse(tuple(range(size)))


def peel_descent(size: int, index: int, combine: Combiner, *, one_based: bool) -> Packet:
    width = max(1, index + int(one_based))
    groups = [tuple(range(start, min(start + width, size))) for start in range(0, size, width)]
    deck = groups[-1]
    for packet in reversed(groups[:-1]):
        deck = combine(packet, deck)
    return deck


def doubling_layers(
    size: int,
    index: int,
    combine: Combiner,
    *,
    one_based: bool,
    reverse_layers: bool,
) -> Packet:
    width = max(1, index + int(one_based))
    widths: list[int] = []
    while width < size:
        widths.append(width)
        width *= 2
    if reverse_layers:
        widths.reverse()
    deck = tuple(range(size))
    for width in widths:
        result: list[int] = []
        for start in range(0, size, 2 * width):
            left = deck[start : start + width]
            right = deck[start + width : start + 2 * width]
            result.extend(combine(left, right) if right else left)
        deck = tuple(result)
    return deck


def increasing_splits(
    size: int,
    index: int,
    combine: Combiner,
    *,
    one_based: bool,
    descending: bool,
) -> Packet:
    start = max(1, index + int(one_based))
    splits: Sequence[int] = tuple(range(start, size))
    if descending:
        splits = tuple(reversed(splits))
    deck = tuple(range(size))
    for split in splits:
        deck = combine(deck[:split], deck[split:])
    return deck


def chunk_deal(
    size: int,
    index: int,
    *,
    one_based: bool,
    odd_first: bool,
    reverse_even_order: bool,
    reverse_odd_order: bool,
    reverse_even_packets: bool,
    reverse_odd_packets: bool,
) -> Packet:
    """Deal fixed-width packets into two piles and collect the piles."""
    width = max(1, index + int(one_based))
    packets = [
        tuple(range(start, min(start + width, size)))
        for start in range(0, size, width)
    ]
    even = packets[0::2]
    odd = packets[1::2]
    if reverse_even_order:
        even.reverse()
    if reverse_odd_order:
        odd.reverse()
    if reverse_even_packets:
        even = [tuple(reversed(packet)) for packet in even]
    if reverse_odd_packets:
        odd = [tuple(reversed(packet)) for packet in odd]
    ordered = (odd + even) if odd_first else (even + odd)
    return tuple(value for packet in ordered for value in packet)


@dataclass(frozen=True)
class Result:
    cross_matches: int
    cross_total: int
    matches: int
    total: int
    exact_anchors: int
    unique_plaintext: int
    name: str
    preview: tuple[int, ...]


def inverse(permutation: Packet) -> Packet:
    result = [0] * len(permutation)
    for new_position, old_position in enumerate(permutation):
        result[old_position] = new_position
    return tuple(result)


def decode_top_after_shuffle(
    ciphertext: Sequence[int], operations: tuple[Packet, ...]
) -> tuple[int, ...] | None:
    """Decode the ordinary GAK convention: apply an action, emit the top."""
    deck = tuple(range(len(operations)))
    plaintext: list[int] = []
    for card in ciphertext:
        matches: list[int] = []
        for index, permutation in enumerate(operations):
            if deck[permutation[0]] == card:
                matches.append(index)
        if len(matches) != 1:
            return None
        index = matches[0]
        deck = tuple(deck[position] for position in operations[index])
        plaintext.append(index)
    return tuple(plaintext)


def decode_selected_after_shuffle(
    ciphertext: Sequence[int], operations: tuple[Packet, ...]
) -> tuple[int, ...] | None:
    """Decode the alternate convention: apply an action, emit its own rank."""
    deck = tuple(range(len(operations)))
    plaintext: list[int] = []
    for card in ciphertext:
        matches: list[int] = []
        for index, permutation in enumerate(operations):
            if deck[permutation[index]] == card:
                matches.append(index)
        if len(matches) != 1:
            return None
        index = matches[0]
        deck = tuple(deck[position] for position in operations[index])
        plaintext.append(index)
    return tuple(plaintext)


def evaluate(
    name: str,
    operations: tuple[Packet, ...],
    *,
    mode: str = "rank-before",
) -> Result | None:
    if len(set(operations)) != 83:
        return None
    ciphertexts = tuple(
        tuple(ord(character) - 33 for character in section)
        for section in REVISED_SECTIONS
    )
    if mode == "rank-before":
        plaintexts = tuple(
            decode_dynamic_substitution(ciphertext, operations)
            for ciphertext in ciphertexts
        )
    elif mode == "top-after":
        decoded = tuple(
            decode_top_after_shuffle(ciphertext, operations)
            for ciphertext in ciphertexts
        )
        if any(plaintext is None for plaintext in decoded):
            return None
        plaintexts = decoded  # type: ignore[assignment]
    elif mode == "selected-after":
        decoded = tuple(
            decode_selected_after_shuffle(ciphertext, operations)
            for ciphertext in ciphertexts
        )
        if any(plaintext is None for plaintext in decoded):
            return None
        plaintexts = decoded  # type: ignore[assignment]
    else:
        raise ValueError(mode)
    cross_matches = 0
    if mode == "rank-before":
        old_ciphertexts = tuple(
            tuple(ord(character) - 33 for character in section)
            for section in ORIGINAL_SECTIONS
        )
        old_plaintexts: list[tuple[int, ...]] = []
        for ciphertext in old_ciphertexts:
            # The original post's first symbols fix this initial CTA as rotation
            # by 26.  Its emitted fixed ciphertext label, rather than the recovered
            # plaintext rank, selects the next shuffle.
            deck = tuple((index + 26) % 83 for index in range(83))
            plaintext: list[int] = []
            for card in ciphertext:
                plaintext.append(deck.index(card))
                deck = tuple(deck[position] for position in operations[card])
            old_plaintexts.append(tuple(plaintext))
        cross_matches = sum(
            old == revised
            for old_stream, revised_stream in zip(
                old_plaintexts, plaintexts, strict=True
            )
            for old, revised in zip(old_stream, revised_stream, strict=True)
        )
    cross_total = sum(map(len, plaintexts))
    matches = total = exact = 0
    for left, left_pos, right, right_pos, length in ANCHORS:
        a = plaintexts[left][left_pos : left_pos + length]
        b = plaintexts[right][right_pos : right_pos + length]
        local = sum(x == y for x, y in zip(a, b, strict=True))
        matches += local
        total += length
        exact += local == length
    return Result(
        cross_matches,
        cross_total,
        matches,
        total,
        exact,
        len(set().union(*map(set, plaintexts))),
        name,
        plaintexts[0][:32],
    )


def main() -> None:
    results: list[Result] = []
    seen_operation_sets: set[tuple[Packet, ...]] = set()
    for combine_name, combine in combiners():
        for family_name, family, kwargs in (
            ("peel-unwind", peel_unwind, {}),
            ("peel-descent", peel_descent, {}),
            ("double-up", doubling_layers, {"reverse_layers": False}),
            ("double-down", doubling_layers, {"reverse_layers": True}),
            ("increasing-up", increasing_splits, {"descending": False}),
            ("increasing-down", increasing_splits, {"descending": True}),
        ):
            for one_based in (False, True):
                operations = tuple(
                    family(83, index, combine, one_based=one_based, **kwargs)
                    for index in range(83)
                )
                if operations in seen_operation_sets:
                    continue
                seen_operation_sets.add(operations)
                base_name = (
                    f"{family_name}-{'1b' if one_based else '0b'}-{combine_name}"
                )
                for orientation, operation_set in (
                    ("direct", operations),
                    ("inverse", tuple(map(inverse, operations))),
                ):
                    for mode in ("rank-before", "top-after", "selected-after"):
                        result = evaluate(
                            f"{base_name}-{orientation}-{mode}",
                            operation_set,
                            mode=mode,
                        )
                        if result is not None:
                            results.append(result)
    for odd_first in (False, True):
        for reverse_even_order in (False, True):
            for reverse_odd_order in (False, True):
                for reverse_even_packets in (False, True):
                    for reverse_odd_packets in (False, True):
                        for one_based in (False, True):
                            operations = tuple(
                                chunk_deal(
                                    83,
                                    index,
                                    one_based=one_based,
                                    odd_first=odd_first,
                                    reverse_even_order=reverse_even_order,
                                    reverse_odd_order=reverse_odd_order,
                                    reverse_even_packets=reverse_even_packets,
                                    reverse_odd_packets=reverse_odd_packets,
                                )
                                for index in range(83)
                            )
                            if operations in seen_operation_sets:
                                continue
                            seen_operation_sets.add(operations)
                            flags = (
                                f"{'O' if odd_first else 'E'}-"
                                f"{'R' if reverse_even_order else 'F'}"
                                f"{'R' if reverse_odd_order else 'F'}-"
                                f"{'r' if reverse_even_packets else 'f'}"
                                f"{'r' if reverse_odd_packets else 'f'}"
                            )
                            base_name = (
                                f"chunk-deal-{'1b' if one_based else '0b'}-{flags}"
                            )
                            for orientation, operation_set in (
                                ("direct", operations),
                                ("inverse", tuple(map(inverse, operations))),
                            ):
                                for mode in (
                                    "rank-before",
                                    "top-after",
                                    "selected-after",
                                ):
                                    result = evaluate(
                                        f"{base_name}-{orientation}-{mode}",
                                        operation_set,
                                        mode=mode,
                                    )
                                    if result is not None:
                                        results.append(result)
    print("cross-match anchor-match exact unique family preview")
    for result in sorted(
        results,
        key=lambda item: (
            item.cross_matches,
            item.exact_anchors,
            item.matches,
            -item.unique_plaintext,
        ),
        reverse=True,
    )[:40]:
        print(
            f"{result.cross_matches:>4}/{result.cross_total:<4} "
            f"{result.matches:>3}/{result.total:<3} {result.exact_anchors:>2}/7 "
            f"{result.unique_plaintext:>3} {result.name:<58} {result.preview}"
        )


if __name__ == "__main__":
    main()
