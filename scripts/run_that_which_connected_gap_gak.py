#!/usr/bin/env python3
"""Bounded connected-gap ordinary-GAK audit for ``THAT WHICH``."""

from __future__ import annotations

import argparse
import random
import statistics

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.free_group_gak import (
    audit_free_group_gak,
    compress_free_group_audit,
    recover_fixed_schedule_gak_with_z3,
)
from eye_mystery.partially_known_arbitrary_state_gak import (
    recover_partially_known_arbitrary_state_gak,
)
from eye_mystery.sparse_gak_sat import encode_text


PAIRS = (
    ("east1", 40, 68),
    ("west1", 40, 70),
    ("east2", 45, 80),
)
PHRASE = "THAT WHICH"


def connected_instances() -> tuple[
    tuple[tuple[int | None, ...], ...],
    tuple[tuple[int, ...], ...],
    tuple[str, ...],
]:
    phrase, alphabet = encode_text(PHRASE)
    schedules = []
    ciphertexts = []
    for message, first, second in PAIRS:
        stream = trigram_values(MESSAGES[message])
        unknown_length = second - first - len(phrase)
        schedules.append((*phrase, *((None,) * unknown_length), *phrase))
        ciphertexts.append(stream[first : second + len(phrase)])
    return tuple(schedules), tuple(ciphertexts), alphabet


def fill_random(
    patterns: tuple[tuple[int | None, ...], ...],
    rng: random.Random,
    operation_count: int,
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            rng.randrange(operation_count) if symbol is None else symbol
            for symbol in pattern
        )
        for pattern in patterns
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=1_000)
    parser.add_argument("--seed", type=int, default=27072026)
    parser.add_argument("--constant-screen", action="store_true")
    parser.add_argument("--solve", action="store_true")
    parser.add_argument("--timeout-ms", type=int, default=120_000)
    args = parser.parse_args()
    patterns, ciphertexts, alphabet = connected_instances()
    operation_count = len(alphabet)

    print(
        f"traces={len(patterns)} lengths={tuple(map(len, patterns))} "
        f"pinned_symbols={''.join(alphabet)!r} operations={operation_count}"
    )
    if args.constant_screen:
        for fill in range(operation_count):
            fixed = tuple(
                tuple(fill if symbol is None else symbol for symbol in pattern)
                for pattern in patterns
            )
            status, _ = recover_partially_known_arbitrary_state_gak(
                fixed,
                ciphertexts,
                deck_size=83,
                plaintext_alphabet_size=operation_count,
                timeout_ms=args.timeout_ms,
            )
            print(f"constant_gap={fill} status={status}")

    rng = random.Random(args.seed)
    compatible = []
    all_core_sizes = []
    for trial in range(args.samples):
        plaintexts = fill_random(patterns, rng, operation_count)
        audit = audit_free_group_gak(plaintexts, ciphertexts)
        all_core_sizes.append(audit.core_states)
        if not audit.forced_nonfix_words:
            compatible.append((audit.core_states, trial, plaintexts, audit))
    print(
        f"free_group_compatible={len(compatible)}/{args.samples} "
        f"all_core_min_median_max="
        f"{min(all_core_sizes)}/{statistics.median(all_core_sizes):g}/"
        f"{max(all_core_sizes)}"
    )
    if not compatible:
        return
    compatible_sizes = [item[0] for item in compatible]
    best = min(compatible, key=lambda item: (item[0], item[1]))
    print(
        f"compatible_core_min_median_max="
        f"{min(compatible_sizes)}/{statistics.median(compatible_sizes):g}/"
        f"{max(compatible_sizes)}"
    )
    print(
        f"best_trial={best[1]} core={best[0]} "
        f"fixed_spans={best[3].fixed_words} "
        f"nonfixed_spans={best[3].nonfixed_words}"
    )
    compressed = compress_free_group_audit(
        best[2],
        ciphertexts,
        target_states=35,
        attempts=100,
        proposals_per_step=5_000,
        seed=best[1] + 35,
    )
    print(
        "compressed_core="
        + ("none" if compressed is None else str(compressed.core_states))
    )
    for (message, first, second), plaintext in zip(
        PAIRS, best[2], strict=True
    ):
        gap = plaintext[len(PHRASE) : -len(PHRASE)]
        print(
            f"{message}:{first}->{second} gap="
            + ",".join(map(str, gap))
        )

    if args.solve and compressed is not None:
        active_positions = max(map(lambda row: len(set(row)), ciphertexts))
        status, witness = recover_fixed_schedule_gak_with_z3(
            best[2],
            ciphertexts,
            deck_size=active_positions,
            replay_deck_size=83,
            plaintext_alphabet_size=operation_count,
            pinned_audit=compressed,
            timeout_ms=args.timeout_ms,
        )
        print(
            f"finite_completion={status} "
            f"forward_replay={'exact' if witness is not None else 'absent'}"
        )


if __name__ == "__main__":
    main()
