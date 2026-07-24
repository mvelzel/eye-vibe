#!/usr/bin/env python3
"""Audit the historical desert-glyph Diamond Readings construction."""

from __future__ import annotations

import argparse
import random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES
from eye_mystery.diamond_reading import (
    COMPONENT_ORDERS,
    X_ORDER,
    Y_ORDER,
    base25_reading,
    collision_pairs,
    index_of_coincidence,
    pair_trigrams,
    shuffled_x_pairs,
    squared_from_pairs,
    squared_reading,
    uniform_pair_baseline,
)


def aggregate_collisions(outputs: tuple[tuple[int, ...], ...]) -> int:
    return sum(collision_pairs(output) for output in outputs)


def relative_order() -> tuple[int, int, int]:
    """Express the document alignment with y components in identity order."""

    return tuple(X_ORDER[Y_ORDER.index(index)] for index in range(3))


def observed_scores() -> tuple[int, tuple[int, ...]]:
    scores = tuple(
        aggregate_collisions(
            tuple(
                squared_from_pairs(
                    pair_trigrams(MESSAGES[name]),
                    relative_order=order,
                )
                for name in MESSAGE_ORDER
            )
        )
        for order in COMPONENT_ORDERS
    )
    return max(scores), scores


def association_control(rng: random.Random) -> tuple[tuple[tuple, ...], ...]:
    result = []
    for name in MESSAGE_ORDER:
        real_x_count = len(MESSAGES[name]) // 6
        order = list(range(real_x_count))
        rng.shuffle(order)
        result.append(shuffled_x_pairs(MESSAGES[name], order))
    return tuple(result)


def cyclic_control(rng: random.Random) -> tuple[tuple[tuple, ...], ...]:
    result = []
    for name in MESSAGE_ORDER:
        pairs = pair_trigrams(MESSAGES[name])
        y_trigrams = tuple(y for y, _ in pairs)
        x_trigrams = tuple(x for _, x in pairs)
        offset = rng.randrange(len(x_trigrams))
        shifted = x_trigrams[offset:] + x_trigrams[:offset]
        result.append(tuple(zip(y_trigrams, shifted, strict=True)))
    return tuple(result)


def max_family_score(pairs_by_message: tuple[tuple[tuple, ...], ...]) -> int:
    return max(
        aggregate_collisions(
            tuple(
                squared_from_pairs(pairs, relative_order=order)
                for pairs in pairs_by_message
            )
        )
        for order in COMPONENT_ORDERS
    )


def tail(
    factory,
    *,
    observed: int,
    controls: int,
    seed: int,
) -> tuple[int, float]:
    rng = random.Random(seed)
    at_least = sum(
        max_family_score(factory(rng)) >= observed for _ in range(controls)
    )
    return at_least, (at_least + 1) / (controls + 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=20_000)
    parser.add_argument("--seed", type=lambda text: int(text, 0), default=0xD1A606)
    args = parser.parse_args()

    print("orders")
    print(f"  y={Y_ORDER} x={X_ORDER} relative={relative_order()}")
    print("uniform-pair IoC baselines")
    print(f"  5x+y  {uniform_pair_baseline('base25'):.8f}")
    print(f"  x^2+y {uniform_pair_baseline('squared'):.8f}")
    print("message IoCs")
    for name in MESSAGE_ORDER:
        first = base25_reading(MESSAGES[name])
        second = squared_reading(MESSAGES[name])
        print(
            f"  {name:5s} n={len(second):3d} "
            f"5x+y={index_of_coincidence(first):.8f} "
            f"x^2+y={index_of_coincidence(second):.8f}"
        )

    observed, geometry_scores = observed_scores()
    tied = sum(score == observed for score in geometry_scores)
    print("squared aggregate ordered-collision geometry family")
    print(f"  scores={geometry_scores}")
    print(f"  document={observed} rank=1/6 tied={tied}")

    association_hits, association_tail = tail(
        association_control,
        observed=observed,
        controls=args.controls,
        seed=args.seed,
    )
    cyclic_hits, cyclic_tail = tail(
        cyclic_control,
        observed=observed,
        controls=args.controls,
        seed=args.seed + 1,
    )
    print("six-alignment max-family controls")
    print(
        f"  association seed=0x{args.seed:x} "
        f"hits={association_hits}/{args.controls} tail={association_tail:.8f}"
    )
    print(
        f"  cyclic seed=0x{args.seed + 1:x} "
        f"hits={cyclic_hits}/{args.controls} tail={cyclic_tail:.8f}"
    )


if __name__ == "__main__":
    main()
