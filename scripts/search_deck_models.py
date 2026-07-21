#!/usr/bin/env python3
"""Test reversible adaptive-deck explanations of the eye messages."""

from __future__ import annotations

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.deck import (
    DeckResult,
    move_to_back_decode,
    move_to_front_decode,
    reverse_prefix_decode,
    ranks_to_labels,
    rotate_to_front_decode,
    swap_with_front_decode,
    transpose_decode,
)
from eye_mystery.metrics import index_of_coincidence


def summarize(family: str, order: str, parameter: int, streams: list[tuple[int, ...]]) -> DeckResult:
    combined = tuple(value for stream in streams for value in stream)
    unique = len(set(combined))
    return DeckResult(
        family=family,
        deck_order=order,
        parameter=parameter,
        unique=unique,
        maximum=max(combined),
        under_26=sum(value < 26 for value in combined) / len(combined),
        ioc=index_of_coincidence(combined, unique),
    )


def main() -> None:
    messages = [trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER]
    orders = {
        "ascending": tuple(range(83)),
        "descending": tuple(reversed(range(83))),
    }
    results = []
    for order_name, deck in orders.items():
        results.append(
            summarize(
                "move-to-front",
                order_name,
                0,
                [move_to_front_decode(message, deck) for message in messages],
            )
        )
        for family, decoder in (
            ("swap-front", swap_with_front_decode),
            ("reverse-prefix", reverse_prefix_decode),
            ("rotate-front", rotate_to_front_decode),
        ):
            results.append(
                summarize(
                    family,
                    order_name,
                    0,
                    [decoder(message, deck) for message in messages],
                )
            )
        results.append(
            summarize(
                "move-to-back",
                order_name,
                0,
                [move_to_back_decode(message, deck) for message in messages],
            )
        )
        for distance in range(1, 83):
            results.append(
                summarize(
                    "transpose",
                    order_name,
                    distance,
                    [transpose_decode(message, deck, distance) for message in messages],
                )
            )

    inverse_results = []
    for order_name, deck in orders.items():
        for family in (
            "move-to-front",
            "move-to-back",
            "swap-front",
            "reverse-prefix",
            "rotate-front",
        ):
            inverse_results.append(
                summarize(
                    family,
                    order_name,
                    0,
                    [ranks_to_labels(message, deck, family) for message in messages],
                )
            )
        for distance in range(1, 83):
            inverse_results.append(
                summarize(
                    "transpose",
                    order_name,
                    distance,
                    [
                        ranks_to_labels(message, deck, "transpose", distance)
                        for message in messages
                    ],
                )
            )

    print("Adaptive deck results (best language-sized collapse first):")
    print("family         order      n unique max   <26%    IoC")
    for result in sorted(
        results,
        key=lambda item: (item.unique, item.maximum, -item.under_26, -item.ioc),
    )[:20]:
        print(
            f"{result.family:<14} {result.deck_order:<10} {result.parameter:>2} "
            f"{result.unique:>6} {result.maximum:>3} "
            f"{100 * result.under_26:>6.2f} {result.ioc:>6.3f}"
        )

    print("\nEye values interpreted as rank instructions (emitted labels):")
    print("family         order      n unique max   <26%    IoC")
    for result in sorted(
        inverse_results,
        key=lambda item: (item.unique, item.maximum, -item.under_26, -item.ioc),
    )[:20]:
        print(
            f"{result.family:<14} {result.deck_order:<10} {result.parameter:>2} "
            f"{result.unique:>6} {result.maximum:>3} "
            f"{100 * result.under_26:>6.2f} {result.ioc:>6.3f}"
        )

    for order_name, deck in orders.items():
        print(f"\nMove-to-front rank prefixes ({order_name} deck):")
        for name, message in zip(MESSAGE_ORDER, messages):
            ranks = move_to_front_decode(message, deck)
            print(f"{name:<5}: {' '.join(f'{value:02d}' for value in ranks[:40])}")


if __name__ == "__main__":
    main()
