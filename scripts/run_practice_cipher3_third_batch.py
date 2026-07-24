#!/usr/bin/env python3
"""Run the third wide conformance-vector batch for practice Cipher 3."""

from __future__ import annotations

import argparse
from collections import Counter

from eye_mystery.practice_cipher3_third import (
    affine_factor_inventory,
    berlekamp_massey_complexity,
    compression_audit,
    compression_shuffle_controls,
    longest_isomorphic_factor,
    named_streams,
    select_recurrence,
    strongest_isomorphic_evidence,
)
from eye_mystery.practice_cipher3_wide import load_cipher3


def percentile_tail(values: tuple[int, ...], observed: int) -> tuple[int, int]:
    """Return corrected lower-tail numerator/denominator."""

    return 1 + sum(value <= observed for value in values), len(values) + 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0xC1F3)
    args = parser.parse_args()

    streams = load_cipher3()
    affine = affine_factor_inventory(streams, minimum_length=4)
    exact = tuple(
        match
        for match in affine
        if match.multiplier == 1 and match.offset == 0
    )
    print("cross-stream factors (known branch excluded)")
    print("best affine", affine[0] if affine else None)
    print("best exact", exact[0] if exact else None)
    print("affine length histogram", Counter(match.length for match in affine))
    recurrent_maps = Counter(
        (match.orientation, match.multiplier, match.offset)
        for match in affine
        if match.length >= 5
    )
    print("recurrent affine maps length>=5", recurrent_maps.most_common(10))
    print(
        "best equality isomorph",
        longest_isomorphic_factor(streams, exclude_known_branch=True),
    )
    print("strongest equality evidence", strongest_isomorphic_evidence(streams))

    print("\nF83 recurrence screens")
    for body in (False, True):
        for order in (1, 2):
            print(select_recurrence(streams, order=order, body=body))
    print("\nBerlekamp-Massey body complexities")
    for name, message in named_streams(streams, body=True):
        complexity = berlekamp_massey_complexity(message)
        print(name, len(message), complexity, f"{complexity / len(message):.6f}")

    print("\ncompression signatures")
    audit = compression_audit(streams)
    print(audit)
    controls = compression_shuffle_controls(
        streams,
        controls=args.controls,
        seed=args.seed,
    )
    direct_tail = percentile_tail(
        controls.direct_lz78_phrases,
        audit.direct_lz78_phrases,
    )
    inverse_tail = percentile_tail(
        controls.inverse_bwt_lz78_phrases,
        audit.inverse_bwt_lz78_phrases,
    )
    print(
        "direct LZ78 lower tail",
        direct_tail,
        direct_tail[0] / direct_tail[1],
        "range",
        (min(controls.direct_lz78_phrases), max(controls.direct_lz78_phrases)),
    )
    print(
        "inverse-BWT LZ78 lower tail",
        inverse_tail,
        inverse_tail[0] / inverse_tail[1],
        "range",
        (
            min(controls.inverse_bwt_lz78_phrases),
            max(controls.inverse_bwt_lz78_phrases),
        ),
    )


if __name__ == "__main__":
    main()
