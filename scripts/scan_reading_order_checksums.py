#!/usr/bin/env python3
"""Test the mod-101 diagonal under all alternating triangle read orders."""

from __future__ import annotations

from functools import reduce
from itertools import combinations
from math import gcd

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER
from eye_mystery.reading_orders import (
    TRIANGLE_ORDERS,
    is_canonical_range,
    values_for_orders,
)


def main() -> None:
    results = []
    for even in TRIANGLE_ORDERS:
        for odd in TRIANGLE_ORDERS:
            messages = tuple(
                values_for_orders(MESSAGES[name], even, odd)
                for name in MESSAGE_ORDER
            )
            totals = tuple(map(sum, messages))
            even_values = tuple(
                value for message in messages for value in message[::2]
            )
            odd_values = tuple(
                value for message in messages for value in message[1::2]
            )
            triple_gcds = tuple(
                (
                    reduce(gcd, (totals[index] for index in indices)),
                    indices,
                )
                for indices in combinations(range(9), 3)
            )
            diagonal_gcd = reduce(gcd, (totals[index] for index in (0, 4, 8)))
            results.append(
                (
                    diagonal_gcd,
                    max(value for value, _ in triple_gcds),
                    is_canonical_range(even_values),
                    is_canonical_range(odd_values),
                    even,
                    odd,
                    totals,
                )
            )

    print("orders tested:", len(results))
    print(
        "both triangle parities cover 0..82:",
        sum(even_ok and odd_ok for _, _, even_ok, odd_ok, *_ in results),
    )
    print("diagonal gcd >= 101:", sum(row[0] >= 101 for row in results))
    print("all-order maximum diagonal gcd:", max(row[0] for row in results))
    for row in sorted(results, reverse=True)[:10]:
        diagonal_gcd, maximum_gcd, even_ok, odd_ok, even, odd, totals = row
        print(
            f"diag={diagonal_gcd:>4} max3={maximum_gcd:>4} "
            f"canonical={even_ok and odd_ok} even={even} odd={odd} "
            f"diagonal-sums={tuple(totals[index] for index in (0, 4, 8))}"
        )


if __name__ == "__main__":
    main()
