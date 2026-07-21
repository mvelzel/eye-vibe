#!/usr/bin/env python3
"""Test a two-plaintext-symbol delayed-isomorphism interpretation.

If a group-autokey-style state update depends on the current plaintext symbol
and the preceding ``k`` symbols, two occurrences of the same plaintext need
not be isomorphic during their first ``k`` outputs.  Once the rolling windows
are wholly inside the repeated phrase, their remaining ciphertext must be
isomorphic.  This script measures that delayed boundary in the six prominent
first-family windows.

The conditioned null keeps the actual ten-symbol isomorphs and independently
draws later ciphertext symbols uniformly from the other 82 values, preserving
Noita's no-adjacent-double rule.  It calibrates the extension only; it is not a
discovery probability for the selected windows or Waite phrase.
"""

from __future__ import annotations

import argparse

import numpy as np

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.isomorphs import pattern

try:
    from scripts.classify_that_which_windows import WINDOWS
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from classify_that_which_windows import WINDOWS


def delayed_patterns(trim: int, end: int) -> tuple[str, ...]:
    if trim < 0 or end <= trim:
        raise ValueError("require 0 <= trim < end")
    values: list[str] = []
    for window in WINDOWS:
        stream = trigram_values(MESSAGES[window.message])
        values.append(
            pattern(stream[window.offset + trim : window.offset + end])
        )
    return tuple(values)


def delayed_common_end(trim: int) -> int:
    limit = min(
        len(trigram_values(MESSAGES[window.message])) - window.offset
        for window in WINDOWS
    )
    end = trim
    for candidate in range(trim + 1, limit + 1):
        if len(set(delayed_patterns(trim, candidate))) != 1:
            break
        end = candidate
    return end


def conditioned_null(
    *,
    trials: int,
    maximum_extension: int,
    trim: int,
    seed: int,
    batch_size: int = 5_000,
) -> tuple[int, ...]:
    """Return success counts for extensions of length ``1..maximum``."""

    if trials < 1 or maximum_extension < 1 or batch_size < 1:
        raise ValueError("trial, extension, and batch counts must be positive")
    prefixes = np.asarray(
        [
            trigram_values(MESSAGES[window.message])[
                window.offset : window.offset + 10
            ]
            for window in WINDOWS
        ],
        dtype=np.int16,
    )
    if len({pattern(row) for row in prefixes}) != 1:
        raise ValueError("the fixed ten-symbol prefixes are not isomorphic")

    rng = np.random.default_rng(seed)
    successes = np.zeros(maximum_extension, dtype=np.int64)
    completed = 0
    while completed < trials:
        batch = min(batch_size, trials - completed)
        extensions = np.empty(
            (batch, len(WINDOWS), maximum_extension), dtype=np.int16
        )
        previous = np.broadcast_to(prefixes[:, -1], (batch, len(WINDOWS)))
        for index in range(maximum_extension):
            draw = rng.integers(0, 82, size=previous.shape, dtype=np.int16)
            current = draw + (draw >= previous)
            extensions[:, :, index] = current
            previous = current

        fixed = np.broadcast_to(
            prefixes,
            (batch, len(WINDOWS), prefixes.shape[1]),
        )
        for length in range(1, maximum_extension + 1):
            sequence = np.concatenate(
                (fixed, extensions[:, :, :length]), axis=2
            )[:, :, trim:]
            equality = sequence[:, :, :, None] == sequence[:, :, None, :]
            successes[length - 1] += np.count_nonzero(
                np.all(equality[:, 1:] == equality[:, :1], axis=(1, 2, 3))
            )
        completed += batch
    return tuple(int(value) for value in successes)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=200_000)
    parser.add_argument("--maximum-extension", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20260721)
    args = parser.parse_args()

    for trim in range(6):
        end = delayed_common_end(trim)
        print(f"trim={trim} common-end={end} retained={end - trim}")
    for phrase in ("THAT WHICH IS ", "THAT WHICH IS THE"):
        print(
            f"Waite T-aligned {phrase!r} length={len(phrase)} "
            f"with trim2: classes={len(set(delayed_patterns(2, len(phrase))))}"
        )
    successes = conditioned_null(
        trials=args.trials,
        maximum_extension=args.maximum_extension,
        trim=2,
        seed=args.seed,
    )
    for extension, success in enumerate(successes, start=1):
        actual = len(set(delayed_patterns(2, 10 + extension))) == 1
        print(
            f"extension={extension} actual={actual} "
            f"null={success}/{args.trials}={success / args.trials:.8f}"
        )
    print(
        "verdict: two-symbol memory is compatible through raw end 17 and "
        "with the 17-character T-aligned 'THAT WHICH IS THE'; this is a "
        "conditioned compatibility result, not a key or decryption"
    )


if __name__ == "__main__":
    main()
