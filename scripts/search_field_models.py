#!/usr/bin/env python3
"""Test reproducible arithmetic cipher families over F_83."""

from __future__ import annotations

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.field_search import (
    affine_recurrence,
    best,
    polynomial_position_mask,
    shifted_ratio,
    tangent_difference,
    two_lag_recurrence,
)


def show(title: str, results: list) -> None:
    print(f"\n{title}")
    print("parameters         unique    IoC  length")
    for result in best(results):
        print(
            f"{str(result.parameters):<18} {result.unique:>6} "
            f"{result.ioc:>6.3f} {result.length:>7}"
        )


def main() -> None:
    messages = [trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER]
    show("Affine recurrence c[i] - a*c[i-lag]", affine_recurrence(messages))
    show(
        "Two-lag recurrence c[i] - a*c[i-1] - b*c[i-2]",
        two_lag_recurrence(messages),
    )
    show("Quadratic positional mask", polynomial_position_mask(messages))
    show("Shifted projective ratios", shifted_ratio(messages))
    show("Projective tangent differences", tangent_difference(messages))


if __name__ == "__main__":
    main()
