#!/usr/bin/env python3
"""Run the six frozen tests in the seventh wide Eye-cipher funnel."""

from __future__ import annotations

import argparse
from random import Random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.language_null import prefix_tree_parity_shuffle
from eye_mystery.seventh_wide import (
    bwt_mtf_score,
    change_score,
    gap_score,
    ordinal_score,
    pointer_score,
    six_block_score,
)


def relabel_bodies(
    streams: dict[str, tuple[int, ...]], mapping: list[int]
) -> dict[str, tuple[int, ...]]:
    return {
        name: (stream[0], *(mapping[value] for value in stream[1:]))
        for name, stream in streams.items()
    }


def attach_headers(
    streams: dict[str, tuple[int, ...]], bodies: dict[str, tuple[int, ...]]
) -> dict[str, tuple[int, ...]]:
    return {name: (streams[name][0], *bodies[name]) for name in MESSAGE_ORDER}


def corrected(hits: int, controls: int) -> str:
    return f"{hits + 1}/{controls + 1} = {(hits + 1)/(controls + 1):.6f}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260722)
    args = parser.parse_args()

    streams = {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}
    bodies = {name: stream[1:] for name, stream in streams.items()}
    generator = Random(args.seed)

    observed_a = bwt_mtf_score(streams)
    observed_b = six_block_score(streams)
    observed_c = gap_score(streams)
    observed_d = change_score(streams)
    observed_e = pointer_score(streams)
    observed_f = ordinal_score(streams)

    null_a = []
    null_c = []
    null_d = []
    null_f = []
    for _ in range(args.controls):
        mapping = list(range(83))
        generator.shuffle(mapping)
        relabeled = relabel_bodies(streams, mapping)
        null_a.append(bwt_mtf_score(relabeled))
        null_c.append(gap_score(relabeled))
        null_d.append(change_score(relabeled))
        null_f.append(ordinal_score(relabeled))

    null_b = []
    null_e = []
    for _ in range(args.controls):
        shuffled_bodies = prefix_tree_parity_shuffle(
            bodies, bodies, generator, start=0
        )
        shuffled = attach_headers(streams, shuffled_bodies)
        null_b.append(six_block_score(shuffled))
        null_e.append(pointer_score(shuffled))

    a_hits = sum(
        (score.runs, -score.mtf_zeros)
        <= (observed_a.runs, -observed_a.mtf_zeros)
        for score in null_a
    )
    b_hits = sum(
        (score.adjacent_equal, score.repeated_bigrams)
        >= (observed_b.adjacent_equal, observed_b.repeated_bigrams)
        for score in null_b
    )
    c_hits = sum(
        (score.compressed_bytes, score.runs)
        <= (observed_c.compressed_bytes, observed_c.runs)
        for score in null_c
    )
    d_hits = sum(
        (score.compressed_bytes, score.runs)
        <= (observed_d.compressed_bytes, observed_d.runs)
        for score in null_d
    )
    e_hits = sum(
        (score.compressed_bytes, score.entropy)
        <= (observed_e.compressed_bytes, observed_e.entropy)
        for score in null_e
    )
    f_hits = sum(
        (score.matches, score.initial_matches)
        >= (observed_f.matches, observed_f.initial_matches)
        for score in null_f
    )

    print("A header-ordered BWT->MTF:", observed_a)
    print("  corrected lower tail:", corrected(a_hits, args.controls))
    print("B six-token block transposition:", observed_b)
    print("  corrected upper tail:", corrected(b_hits, args.controls))
    print("C Z101 hidden-gap derivative:", observed_c)
    print("  corrected lower tail:", corrected(c_hits, args.controls))
    print("D sequential eye-change family:", observed_d)
    print("  corrected lower tail:", corrected(d_hits, args.controls))
    print("E temporal occurrence pointers:", observed_e)
    print("  corrected lower tail:", corrected(e_hits, args.controls))
    print("F ordinal/factoradic self-indexing:", observed_f)
    print("  corrected upper tail:", corrected(f_hits, args.controls))


if __name__ == "__main__":
    main()
