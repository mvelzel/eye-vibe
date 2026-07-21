#!/usr/bin/env python3
"""Check the proposed universal index-25 entropy/periodicity pivot."""

from __future__ import annotations

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.entropy_pivot import (
    lag_autocorrelation,
    mod_five_counts,
    rolling_entropies,
    shannon_entropy,
)


PIVOT = 25
WINDOW = 5


def report(label: str, streams: dict[str, tuple[int, ...]]) -> None:
    print(f"{label} (index is zero-based window start)")
    print("message H[24] H[25] H[26] delta25 counts[0..4] lag5-pre lag5-post")
    for name in MESSAGE_ORDER:
        stream = streams[name]
        rolling = rolling_entropies(stream, WINDOW)
        before = stream[:PIVOT]
        after = stream[PIVOT + 1 :]
        print(
            name,
            *(f"{rolling[index]:.6f}" for index in range(PIVOT - 1, PIVOT + 2)),
            f"{rolling[PIVOT] - rolling[PIVOT - 1]:+.6f}",
            mod_five_counts(after),
            f"{lag_autocorrelation(before, 5):+.6f}",
            f"{lag_autocorrelation(after, 5):+.6f}",
        )
    print(
        "mean entropy before/after pivot:",
        f"{sum(shannon_entropy(stream[:PIVOT]) for stream in streams.values()) / len(streams):.6f}",
        f"{sum(shannon_entropy(stream[PIVOT + 1 :]) for stream in streams.values()) / len(streams):.6f}",
    )
    print()


def main() -> None:
    report("raw eye directions", {name: MESSAGES[name] for name in MESSAGE_ORDER})
    report(
        "canonical trigrams modulo five",
        {
            name: tuple(value % 5 for value in trigram_values(MESSAGES[name]))
            for name in MESSAGE_ORDER
        },
    )


if __name__ == "__main__":
    main()
