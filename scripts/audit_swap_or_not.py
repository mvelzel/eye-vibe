#!/usr/bin/env python3
"""Audit the seven Eye isomorph maps against low-round swap-or-not shuffles."""

from __future__ import annotations

import argparse
import random

import numpy as np

from eye_mystery.affine_embedding import context_from_sequences
from eye_mystery.hidden_geometry import context_sequences


def eye_contexts():
    return tuple(
        context_from_sequences(name, source, target)
        for name, source, target in context_sequences()
    )


def random_deranged_context(context, rng: random.Random):
    sources = tuple(left for left, _ in context.pairs)
    while True:
        targets = tuple(rng.sample(range(83), len(sources)))
        if all(left != right for left, right in zip(sources, targets)):
            return context_from_sequences("null", sources, targets)


def endpoint_form_arrays(rounds: int):
    """Vectorize every key tuple and its relaxed affine endpoint forms."""

    keys = np.indices((83,) * rounds, dtype=np.int16).reshape(rounds, -1)
    zero = np.zeros(keys.shape[1], dtype=np.int16)
    forms = [(1, zero)]
    for key in keys:
        forms += [
            (-sign, (key - constant) % 83)
            for sign, constant in tuple(forms)
        ]
    return keys, tuple(forms)


def vector_audit(context, keys, forms):
    """Return exact best fit, exemplar, and count of compatible key tuples."""

    scores = np.zeros(keys.shape[1], dtype=np.uint8)
    for left, right in context.pairs:
        difference = (right - left) % 83
        total = (right + left) % 83
        covered = np.zeros(keys.shape[1], dtype=bool)
        for sign, constants in forms:
            covered |= constants == (difference if sign == 1 else total)
        scores += covered
    best_index = int(scores.argmax())
    best = int(scores[best_index])
    return best, tuple(int(row[best_index]) for row in keys), int(
        np.count_nonzero(scores == len(context.pairs))
    )


def has_compatible_key(context, forms) -> bool:
    """Test full compatibility while shrinking the surviving key set."""

    survivors = np.arange(len(forms[0][1]), dtype=np.int64)
    for left, right in context.pairs:
        difference = (right - left) % 83
        total = (right + left) % 83
        covered = np.zeros(len(survivors), dtype=bool)
        for sign, constants in forms:
            covered |= constants[survivors] == (
                difference if sign == 1 else total
            )
        survivors = survivors[covered]
        if not len(survivors):
            return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=3, choices=(1, 2, 3))
    parser.add_argument("--null-trials", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260726)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    arrays = {
        rounds: endpoint_form_arrays(rounds)
        for rounds in range(1, args.rounds + 1)
    }
    for context in eye_contexts():
        audits = tuple(
            (rounds, *vector_audit(context, *arrays[rounds]))
            for rounds in range(1, args.rounds + 1)
        )
        print(
            context.name,
            "pairs=" + str(len(context.pairs)),
            " ".join(
                f"r{rounds}={best}/{len(context.pairs)}"
                f"[keys={keys},full_keys={full_keys}]"
                for rounds, best, keys, full_keys in audits
            ),
        )
        if args.null_trials:
            compatible = 0
            forms = arrays[args.rounds][1]
            for _ in range(args.null_trials):
                null_context = random_deranged_context(context, rng)
                if has_compatible_key(null_context, forms):
                    compatible += 1
            print(
                f"  matched deranged-injection null: "
                f"compatible={compatible}/{args.null_trials}"
            )


if __name__ == "__main__":
    main()
