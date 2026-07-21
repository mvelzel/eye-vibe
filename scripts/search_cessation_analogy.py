#!/usr/bin/env python3
"""Test direct Cessation-style skip-key readings of the Eye messages."""

from __future__ import annotations

import argparse
import heapq
from itertools import permutations

from eye_mystery.cessation import (
    CESSATION_KEY,
    bits_to_bytes,
    skip_key_bits,
    text_likeness,
)
from eye_mystery.corpus import (
    MESSAGE_ORDER,
    MESSAGES,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)
from eye_mystery.initials import perfect_successor_rotation
from eye_mystery.marker_bwt import (
    marker_bwt_lf_order,
    marker_bwt_plaintext_order,
)
from eye_mystery.prefix_hierarchy import serialize_trie_edges


def message_orders() -> tuple[tuple[str, ...], ...]:
    base = (
        MESSAGE_ORDER,
        perfect_successor_rotation(),
        marker_bwt_lf_order(),
        marker_bwt_plaintext_order(),
    )
    unique = []
    for order in base:
        assert order is not None
        for candidate in (tuple(order), tuple(reversed(order))):
            if candidate not in unique:
                unique.append(candidate)
    return tuple(unique)


def key_variants(
    base_keys: tuple[tuple[str, tuple[int, ...]], ...], *, rotate: bool
) -> tuple[tuple[str, tuple[int, ...]], ...]:
    variants = []
    seen = set()
    for base_name, base_key in base_keys:
        oriented = (
            ("forward", base_key),
            ("reverse", tuple(reversed(base_key))),
            ("complement", tuple(1 - bit for bit in base_key)),
            (
                "reverse-complement",
                tuple(1 - bit for bit in reversed(base_key)),
            ),
        )
        for orientation, key in oriented:
            offsets = range(len(key)) if rotate else (0,)
            for offset in offsets:
                candidate = key[offset:] + key[:offset]
                if candidate in seen:
                    continue
                seen.add(candidate)
                variants.append(
                    (f"{base_name}/{orientation}/rotation={offset}", candidate)
                )
    return tuple(variants)


def parse_key(value: str) -> tuple[str, tuple[int, ...]]:
    try:
        name, bits = value.split("=", 1)
    except ValueError as error:
        raise argparse.ArgumentTypeError("key must be NAME=BITS") from error
    if not name or not bits or any(bit not in "01" for bit in bits):
        raise argparse.ArgumentTypeError("key must have a name and binary digits")
    return name, tuple(map(int, bits))


def candidate_bytes(bits: tuple[int, ...]):
    for offset in range(8):
        for least_significant_first in (False, True):
            data = bits_to_bytes(
                bits,
                offset=offset,
                least_significant_first=least_significant_first,
            )
            yield offset, least_significant_first, data


def digits_for_trigrams(values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        digit
        for value in values
        for digit in (value // 25, (value // 5) % 5, value % 5)
    )


def segmented_key_bits(
    values: tuple[int, ...],
    lengths: tuple[int, ...],
    key: tuple[int, ...],
    *,
    reset_value: int | None = None,
) -> tuple[int, ...]:
    if sum(lengths) != len(values):
        raise ValueError("segment lengths must partition the values")
    output = []
    start = 0
    for length in lengths:
        output.extend(
            skip_key_bits(
                values[start : start + length],
                key,
                reset_value=reset_value,
            )
        )
        start += length
    return tuple(output)


def push(best, serial, description, bits, *, mirror=None):
    def consider(heap, item):
        if len(heap) < 12:
            heapq.heappush(heap, item)
        elif item > heap[0]:
            heapq.heapreplace(heap, item)

    for offset, lsb, data in candidate_bytes(bits):
        text, printable, negative_controls = text_likeness(data)
        score = (text, printable, negative_controls)
        item = (score, serial, description, offset, lsb, data)
        serial += 1
        consider(best, item)
        if mirror is not None:
            consider(mirror, item)
    return serial


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--key",
        type=parse_key,
        action="append",
        help="binary cyclic key as NAME=BITS; defaults to the Cessation key",
    )
    parser.add_argument(
        "--rotate-keys",
        action="store_true",
        help="test every cyclic starting phase in addition to orientation/complement",
    )
    args = parser.parse_args()
    orders = message_orders()
    base_keys = tuple(args.key or (("cessation-calendar", CESSATION_KEY),))
    keys = key_variants(base_keys, rotate=args.rotate_keys)
    best = []
    best_merged = []
    serial = 0

    # Direct analogy: the five eye directions are the five positive skip
    # distances.  Test every direction-to-distance assignment.
    for steps in permutations(range(1, 6)):
        mapped = {
            name: tuple(steps[value] for value in MESSAGES[name])
            for name in MESSAGE_ORDER
        }
        for order_index, order in enumerate(orders):
            for key_name, key in keys:
                for reset_messages in (False, True):
                    if reset_messages:
                        bits = tuple(
                            bit
                            for name in order
                            for bit in skip_key_bits(mapped[name], key)
                        )
                    else:
                        values = tuple(
                            value for name in order for value in mapped[name]
                        )
                        bits = skip_key_bits(values, key)
                    description = (
                        f"raw-positive map={steps} order={order_index} "
                        f"key={key_name} reset_messages={reset_messages}"
                    )
                    serial = push(best, serial, description, bits)
                    row_bits = tuple(
                        bit
                        for name in order
                        for bit in segmented_key_bits(
                            mapped[name],
                            tuple(
                                3 * length
                                for length in ROW_PAIR_TRIGRAM_LENGTHS[name]
                            ),
                            key,
                        )
                    )
                    serial = push(
                        best,
                        serial,
                        description + " reset_rows=True",
                        row_bits,
                    )

    # Closer syntactic analogy: one direction resets and does not emit, while
    # the other four directions are distances 1..4.
    for reset_direction in range(5):
        other_directions = tuple(
            direction for direction in range(5) if direction != reset_direction
        )
        for positive_steps in permutations(range(1, 5)):
            mapping = {reset_direction: 0}
            mapping.update(zip(other_directions, positive_steps, strict=True))
            mapped = {
                name: tuple(mapping[value] for value in MESSAGES[name])
                for name in MESSAGE_ORDER
            }
            for order_index, order in enumerate(orders):
                for key_name, key in keys:
                    values = tuple(
                        value for name in order for value in mapped[name]
                    )
                    bits = skip_key_bits(values, key, reset_value=0)
                    description = (
                        f"raw-reset reset={reset_direction} steps={positive_steps} "
                        f"order={order_index} key={key_name}"
                    )
                    serial = push(best, serial, description, bits)
                    row_bits = tuple(
                        bit
                        for name in order
                        for bit in segmented_key_bits(
                            mapped[name],
                            tuple(
                                3 * length
                                for length in ROW_PAIR_TRIGRAM_LENGTHS[name]
                            ),
                            key,
                            reset_value=0,
                        )
                    )
                    serial = push(
                        best,
                        serial,
                        description + " reset_rows=True",
                        row_bits,
                    )

    # At the accepted trigram layer, test symbols as positive distances and
    # the Cessation convention where zero resets the pointer.
    trigrams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    for order_index, order in enumerate(orders):
        for key_name, key in keys:
            values = tuple(value for name in order for value in trigrams[name])
            serial = push(
                best,
                serial,
                f"trigram-plus-one order={order_index} key={key_name}",
                skip_key_bits(tuple(value + 1 for value in values), key),
            )
            row_plus_one = tuple(
                bit
                for name in order
                for bit in segmented_key_bits(
                    tuple(value + 1 for value in trigrams[name]),
                    ROW_PAIR_TRIGRAM_LENGTHS[name],
                    key,
                )
            )
            serial = push(
                best,
                serial,
                f"trigram-plus-one order={order_index} key={key_name} reset_rows=True",
                row_plus_one,
            )
            serial = push(
                best,
                serial,
                f"trigram-zero-reset order={order_index} key={key_name}",
                skip_key_bits(values, key, reset_value=0),
            )
            row_zero_reset = tuple(
                bit
                for name in order
                for bit in segmented_key_bits(
                    trigrams[name],
                    ROW_PAIR_TRIGRAM_LENGTHS[name],
                    key,
                    reset_value=0,
                )
            )
            serial = push(
                best,
                serial,
                f"trigram-zero-reset order={order_index} key={key_name} reset_rows=True",
                row_zero_reset,
            )

    # Cessation first merges duplicated fragments.  The Eyes form a branching
    # prefix trie rather than one linear overlap, so serialize every distinct
    # marker-free edge once in both DFS and BFS order, with sibling branches
    # fixed by each independently motivated message order.
    merged_streams = []
    seen_merged = set()
    for order_index, order in enumerate(orders):
        for breadth_first in (False, True):
            values = serialize_trie_edges(
                trigrams,
                order,
                start=1,
                breadth_first=breadth_first,
            )
            if values in seen_merged:
                continue
            seen_merged.add(values)
            merged_streams.append(
                (
                    f"{'bfs' if breadth_first else 'dfs'}-order={order_index}",
                    values,
                )
            )

    for merged_name, values in merged_streams:
        raw_values = digits_for_trigrams(values)
        for key_name, key in keys:
            for steps in permutations(range(1, 6)):
                mapped = tuple(steps[value] for value in raw_values)
                serial = push(
                    best,
                    serial,
                    f"merged-raw-positive {merged_name} map={steps} key={key_name}",
                    skip_key_bits(mapped, key),
                    mirror=best_merged,
                )
            for reset_direction in range(5):
                other_directions = tuple(
                    direction
                    for direction in range(5)
                    if direction != reset_direction
                )
                for positive_steps in permutations(range(1, 5)):
                    mapping = {reset_direction: 0}
                    mapping.update(
                        zip(other_directions, positive_steps, strict=True)
                    )
                    mapped = tuple(mapping[value] for value in raw_values)
                    serial = push(
                        best,
                        serial,
                        f"merged-raw-reset {merged_name} reset={reset_direction} "
                        f"steps={positive_steps} key={key_name}",
                        skip_key_bits(mapped, key, reset_value=0),
                        mirror=best_merged,
                    )
            serial = push(
                best,
                serial,
                f"merged-trigram-plus-one {merged_name} key={key_name}",
                skip_key_bits(tuple(value + 1 for value in values), key),
                mirror=best_merged,
            )
            serial = push(
                best,
                serial,
                f"merged-trigram-zero-reset {merged_name} key={key_name}",
                skip_key_bits(values, key, reset_value=0),
                mirror=best_merged,
            )

    print("base keys:")
    for name, key in base_keys:
        print(f"  {name} ({len(key)}): {''.join(map(str, key))}")
    print("distinct key variants:", len(keys))
    print("distinct merged trie serializations:", len(merged_streams))
    print("byte interpretations tested:", serial)
    print("best candidates:")
    for score, _, description, offset, lsb, data in sorted(best, reverse=True):
        ratio = score[1] / max(1, len(data))
        preview = "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in data[:96])
        print(
            f"  text={score[0]}/{len(data)} printable={score[1]}/{len(data)} "
            f"({ratio:.3f}) offset={offset} lsb={lsb} {description}"
        )
        print("   ", preview)
    print("best merged candidates:")
    for score, _, description, offset, lsb, data in sorted(
        best_merged, reverse=True
    ):
        ratio = score[1] / max(1, len(data))
        preview = "".join(
            chr(byte) if 32 <= byte <= 126 else "." for byte in data[:96]
        )
        print(
            f"  text={score[0]}/{len(data)} printable={score[1]}/{len(data)} "
            f"({ratio:.3f}) offset={offset} lsb={lsb} {description}"
        )
        print("   ", preview)


if __name__ == "__main__":
    main()
