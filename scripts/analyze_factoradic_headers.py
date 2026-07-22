#!/usr/bin/env python3
"""Reproduce the finite core of the proposed S6 Eye header structure."""

from __future__ import annotations

from eye_mystery.corpus import MESSAGE_ORDER
from eye_mystery.factoradic_headers import (
    SYMBOLS,
    fixed_symbols,
    graph_conditioned_audit,
    header_ranks,
    observed_signature,
    permutation_order,
)


def main() -> None:
    ranks = header_ranks()
    signature = observed_signature()
    print("Six-symbol order:", SYMBOLS)
    print("message rank permutation order fixed newline-preimage")
    for name, permutation in zip(MESSAGE_ORDER, signature.permutations, strict=True):
        print(
            name,
            ranks[name],
            permutation,
            permutation_order(permutation),
            fixed_symbols(permutation),
            permutation.index(5),
        )
    print("P group order/ranks:", signature.p_group_order, signature.p_group_ranks)
    print("Q group order:", signature.q_group_order)
    print("newline preimages:", "".join(map(str, signature.newline_preimages)))
    print("East-Q/West-Q right cosets:", signature.east_q_cosets, signature.west_q_cosets)

    audit = graph_conditioned_audit()
    print("graph-conditioned counts:", audit)
    print("full conditional fraction:", f"{audit.full}/{audit.distinct_ranks}")


if __name__ == "__main__":
    main()
