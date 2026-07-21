#!/usr/bin/env python3
"""Search structured S_83 deck shuffles one swap away from an affine base."""

from __future__ import annotations

from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.deck_base import decode_affine_base_swap
from eye_mystery.metrics import index_of_coincidence


@dataclass(frozen=True)
class Result:
    skip_indicator: bool
    secondary: str
    multiplier: int
    offset: int
    unique: int
    under_26: float
    ioc: float


def main() -> None:
    messages = tuple(trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER)
    results = []
    for skip_indicator in (False, True):
        for secondary in (
            "none",
            "one-k",
            "adjacent",
            "mirror",
            "double",
            "half-turn",
            "fixed-1-2",
        ):
            for multiplier in range(1, 83):
                for offset in range(83):
                    streams = tuple(
                        decode_affine_base_swap(
                            message[skip_indicator:],
                            multiplier,
                            offset,
                            secondary=secondary,
                        )
                        for message in messages
                    )
                    combined = tuple(value for stream in streams for value in stream)
                    unique = len(set(combined))
                    results.append(
                        Result(
                            skip_indicator=skip_indicator,
                            secondary=secondary,
                            multiplier=multiplier,
                            offset=offset,
                            unique=unique,
                            under_26=sum(value < 26 for value in combined) / len(combined),
                            ioc=index_of_coincidence(combined, unique),
                        )
                    )

    print("Affine base shuffle followed by a plaintext-dependent top swap")
    print("skip secondary    a   b unique   <26%    IoC")
    for result in sorted(
        results,
        key=lambda item: (item.unique, -item.under_26, -item.ioc),
    )[:30]:
        print(
            f"{str(result.skip_indicator):<4} {result.secondary:<11} "
            f"{result.multiplier:>2} {result.offset:>3} {result.unique:>6} "
            f"{100 * result.under_26:>6.2f} {result.ioc:>6.3f}"
        )

    print("\nHighest normalized IoC")
    print("skip secondary    a   b unique   <26%    IoC")
    for result in sorted(results, key=lambda item: -item.ioc)[:20]:
        print(
            f"{str(result.skip_indicator):<4} {result.secondary:<11} "
            f"{result.multiplier:>2} {result.offset:>3} {result.unique:>6} "
            f"{100 * result.under_26:>6.2f} {result.ioc:>6.3f}"
        )


if __name__ == "__main__":
    main()
