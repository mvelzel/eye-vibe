#!/usr/bin/env python3
"""Check the proposed universal index-25 entropy/periodicity pivot."""

from __future__ import annotations

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.entropy_pivot import (
    exact_pivot_rows,
    glyph_projections,
    lag_autocorrelation,
    mod_five_counts,
    period_scan_control,
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
        after = stream[PIVOT:]
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
        f"{sum(shannon_entropy(stream[PIVOT:]) for stream in streams.values()) / len(streams):.6f}",
    )
    print()


def main() -> None:
    projections = glyph_projections(MESSAGES)
    print("Exact claim: glyphs 25..49, 25 values, lag 5")
    print("projection message counts[0..4] lag matches/comparisons")
    for projection, streams in projections.items():
        for name, row in exact_pivot_rows(streams).items():
            print(
                projection,
                name,
                row.counts,
                f"{row.lag_matches}/{row.lag_comparisons}",
            )
    print()

    for label, lags, trials in (
        ("fixed lag 5; projection and cut selected", (5,), 1_000),
        ("lags 2..10; projection, lag, and cut selected", tuple(range(2, 11)), 1_000),
    ):
        observed, controls = period_scan_control(
            MESSAGES,
            lags=lags,
            trials=trials,
            seed=24_072_026,
        )
        upper = (sum(score >= observed.matches for score in controls) + 1) / (
            trials + 1
        )
        ordered = sorted(controls)
        print(label)
        print("observed:", observed)
        print(
            "controls min/median/max:",
            ordered[0],
            ordered[len(ordered) // 2],
            ordered[-1],
        )
        print("selection-corrected upper tail:", f"{upper:.9f}")
        print()

    # Retain the older rolling-entropy report for transparent comparison with
    # the PDF's graph, but align the five-valued analysis to glyph positions.
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
