#!/usr/bin/env python3
"""Test the Eye bodies as suffix/LCP or complete BWT rows."""

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.suffix_rows import (
    complete_bwt_rows_pass_first_column_test,
    count_realisable_orders,
    lcp_divergence,
    natural_trigram_sort_orders,
    order_constraints,
    order_is_realisable,
)


TRIE_ORDER = (
    "east1",
    "west1",
    "east2",
    "west2",
    "east4",
    "west4",
    "east5",
    "east3",
    "west3",
)


def main() -> None:
    values = {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}
    markers = {name: stream[0] for name, stream in values.items()}
    bodies = {name: stream[1:] for name, stream in values.items()}
    lcp = tuple(
        lcp_divergence(bodies[left], bodies[right])[0]
        for left, right in zip(TRIE_ORDER, TRIE_ORDER[1:])
    )
    constraints = order_constraints(TRIE_ORDER, bodies)
    natural_orders = natural_trigram_sort_orders(bodies)

    print("marker-derived order:", ",".join(TRIE_ORDER))
    print("adjacent LCP depths:", lcp)
    print("alphabet constraints:", constraints)
    print("arbitrary alphabet realisable:", order_is_realisable(TRIE_ORDER, bodies))
    print("realisable panel orders:", count_realisable_orders(bodies), "/ 362880")
    print("distinct natural trigram sort orders:", len(natural_orders), "/ 720 rules")
    print("natural order hit:", TRIE_ORDER in natural_orders)
    print("natural reverse hit:", TRIE_ORDER[::-1] in natural_orders)
    print(
        "complete BWT first/last-column multiset test:",
        complete_bwt_rows_pass_first_column_test(bodies, markers),
    )


if __name__ == "__main__":
    main()
