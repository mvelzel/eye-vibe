#!/usr/bin/env python3
"""Report and calibrate the near-cyclic BWT of all nine Eye bodies."""

from __future__ import annotations

import argparse

from eye_mystery.body_bwt import (
    body_bwt_null_counts,
    concatenate_bodies,
    eye_bodies,
    lf_cycle_lengths,
    single_cycle_deletions,
)
from eye_mystery.marker_bwt import inverse_cyclic_bwt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20_260_721)
    args = parser.parse_args()

    stream = concatenate_bodies(eye_bodies())
    print("body values:", len(stream))
    print("LF cycle lengths:", lf_cycle_lengths(stream))
    print("one-value deletions yielding one cycle:")
    for index, name, body_index, value in single_cycle_deletions():
        candidate = stream[:index] + stream[index + 1 :]
        restored = inverse_cyclic_bwt(candidate, 0)
        preview = "".join(chr(item + 32) for item in restored[:80])
        print(
            f"  stream={index} {name} body={body_index} value={value} "
            f"inverse-preview={preview!r}"
        )
    print("prefix-tree parity-shuffle null:")
    for name, count in body_bwt_null_counts(args.trials, args.seed).items():
        print(f"  {name}: {count}")


if __name__ == "__main__":
    main()
