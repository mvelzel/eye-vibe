#!/usr/bin/env python3
"""Run the exact connected-gap ordinary-GAK Hail Mary formulation."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import time
from collections.abc import Sequence

from eye_mystery.arbitrary_gak_sat import encrypt_messages
from eye_mystery.arbitrary_state_sparse_gak import (
    recover_arbitrary_state_gak_witness,
)
from eye_mystery.cp_sat_gak import recover_cp_sat_gak
from eye_mystery.cp_sat_free_group_completion import (
    recover_cp_sat_free_group_completion,
)
from eye_mystery.explicit_permutation_gak import (
    ExplicitPermutationGAKWitness,
    recover_explicit_permutation_gak,
)
from eye_mystery.free_group_gak import compress_free_group_audit
from eye_mystery.sparse_gak_sat import encode_text
from eye_mystery.symbolic_sparse_gak import recover_symbolic_sparse_gak

from run_that_which_connected_gap_gak import connected_instances


CANDIDATE_452_GAPS = (
    (2, 5, 0, 4, 1, 0, 1, 1, 1, 1, 1, 2, 0, 2, 2, 3, 6, 0),
    (3, 0, 4, 0, 0, 5, 6, 3, 1, 1, 2, 5, 1, 6, 0, 3, 6, 4, 6, 2),
    (6, 4, 4, 0, 6, 6, 3, 4, 1, 4, 0, 1, 2, 6, 0, 6, 3, 3, 6, 5, 5, 1, 0, 4, 6),
)


def candidate_452_schedules() -> tuple[tuple[int, ...], ...]:
    patterns, _, _ = connected_instances()
    schedules = []
    for pattern, gap in zip(patterns, CANDIDATE_452_GAPS, strict=True):
        gap_values = iter(gap)
        schedule = tuple(
            next(gap_values) if symbol is None else symbol
            for symbol in pattern
        )
        try:
            next(gap_values)
        except StopIteration:
            pass
        else:
            raise AssertionError("candidate gap exceeds the frozen pattern")
        schedules.append(schedule)
    return tuple(schedules)


def _random_permutation(size: int, rng: random.Random) -> tuple[int, ...]:
    values = list(range(size))
    rng.shuffle(values)
    return tuple(values)


def same_shaped_plant(
    *,
    deck_size: int = 83,
    seed: int = 31072026,
) -> tuple[
    tuple[tuple[int | None, ...], ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    """Construct the frozen three-trace symbolic positive control."""

    patterns, _, alphabet = connected_instances()
    rng = random.Random(seed)
    action_count = len(alphabet) + 2
    operations = tuple(
        _random_permutation(deck_size, rng)
        for _ in range(action_count)
    )
    decks = tuple(_random_permutation(deck_size, rng) for _ in patterns)
    plaintexts: list[tuple[int, ...]] = []
    for trace_index, pattern in enumerate(patterns):
        gap_index = 0
        plaintext: list[int] = []
        for symbol in pattern:
            if symbol is not None:
                plaintext.append(symbol)
                continue
            # Both hidden actions occur in every gap. The pinned actions remain
            # available so the control has the same unknown-selector domain as
            # the real query.
            if gap_index == 0:
                plaintext.append(len(alphabet))
            elif gap_index == 1:
                plaintext.append(len(alphabet) + 1)
            else:
                plaintext.append(rng.randrange(action_count))
            gap_index += 1
        # Avoid identical planted schedules across the independent traces.
        plaintext[-len(encode_text("THAT WHICH")[0]) - 1] = (
            len(alphabet) + trace_index % 2
        )
        plaintexts.append(tuple(plaintext))
    ciphertexts = tuple(
        encrypt_messages((plaintext,), deck, operations)[0]
        for plaintext, deck in zip(plaintexts, decks, strict=True)
    )
    return patterns, tuple(plaintexts), ciphertexts, operations


def _digest_witness(witness: ExplicitPermutationGAKWitness) -> str:
    payload = repr(
        (
            witness.initial_decks,
            witness.operations,
            witness.plaintexts,
        )
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _print_gaps(
    schedules: Sequence[Sequence[int]],
    *,
    phrase_length: int,
) -> None:
    labels = ("east1", "west1", "east2")
    for label, schedule in zip(labels, schedules, strict=True):
        gap = schedule[phrase_length:-phrase_length]
        print(f"{label}_gap=" + ",".join(map(str, gap)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        choices=("plant", "real", "candidate452", "impossible"),
    )
    parser.add_argument("--actions", type=int)
    parser.add_argument("--deck-size", type=int, default=83)
    parser.add_argument("--timeout-ms", type=int, default=300_000)
    parser.add_argument(
        "--backend",
        choices=(
            "sparse",
            "explicit",
            "pairwise-fixed",
            "cp-sat",
            "cp-group-fixed",
        ),
        default="sparse",
    )
    parser.add_argument(
        "--no-position-symmetry",
        action="store_true",
    )
    parser.add_argument(
        "--no-action-symmetry",
        action="store_true",
    )
    parser.add_argument(
        "--pin-plant-gaps",
        action="store_true",
        help="diagnostic: expose the planted gap schedule to the solver",
    )
    parser.add_argument(
        "--hint-plant-key",
        action="store_true",
        help="diagnostic: give CP-SAT the planted operations as hints",
    )
    parser.add_argument(
        "--pin-compressed-core",
        action="store_true",
        help="pin the frozen 34-state quotient of candidate 452",
    )
    parser.add_argument(
        "--print-witness-json",
        action="store_true",
        help="print the complete constructive witness as one JSON record",
    )
    args = parser.parse_args()
    phrase, alphabet = encode_text("THAT WHICH")
    planted_operations = None
    pinned_audit = None

    if args.mode == "plant":
        (
            patterns,
            planted_plaintexts,
            ciphertexts,
            planted_operations,
        ) = same_shaped_plant(deck_size=args.deck_size)
        action_count = args.actions or len(alphabet) + 2
        if action_count < len(alphabet) + 2:
            raise SystemExit("the planted control needs at least nine actions")
        print(
            f"mode=plant deck={args.deck_size} actions={action_count} "
            f"lengths={tuple(map(len, patterns))}"
        )
        _print_gaps(planted_plaintexts, phrase_length=len(phrase))
        if args.pin_plant_gaps:
            patterns = planted_plaintexts
    elif args.mode == "real":
        patterns, ciphertexts, _ = connected_instances()
        action_count = args.actions or len(alphabet)
        print(
            f"mode=real deck={args.deck_size} actions={action_count} "
            f"lengths={tuple(map(len, patterns))}"
        )
    elif args.mode == "candidate452":
        _, ciphertexts, _ = connected_instances()
        patterns = candidate_452_schedules()
        action_count = args.actions or len(alphabet)
        print(
            f"mode=candidate452 deck={args.deck_size} "
            f"actions={action_count} lengths={tuple(map(len, patterns))}"
        )
        _print_gaps(patterns, phrase_length=len(phrase))
        if args.pin_compressed_core:
            pinned_audit = compress_free_group_audit(
                patterns,
                ciphertexts,
                target_states=35,
                attempts=100,
                proposals_per_step=5_000,
                seed=487,
            )
            if pinned_audit is None:
                raise SystemExit("failed to reproduce the compressed core")
            print(f"pinned_core_states={pinned_audit.core_states}")
    else:
        patterns = ((0, 0, 0),)
        ciphertexts = ((0, 1, 1),)
        action_count = args.actions or 1
        print(
            f"mode=impossible deck={args.deck_size} actions={action_count}"
        )

    started = time.monotonic()
    if args.backend == "pairwise-fixed":
        if any(symbol is None for pattern in patterns for symbol in pattern):
            raise SystemExit("pairwise-fixed requires a fully pinned schedule")
        status, fixed_witness = recover_arbitrary_state_gak_witness(
            patterns,  # type: ignore[arg-type]
            ciphertexts,
            deck_size=args.deck_size,
            plaintext_alphabet_size=action_count,
            timeout_ms=args.timeout_ms,
        )
        witness = (
            None
            if fixed_witness is None
            else ExplicitPermutationGAKWitness(
                initial_decks=fixed_witness.initial_decks,
                operations=fixed_witness.operations,
                plaintexts=tuple(
                    tuple(int(symbol) for symbol in pattern)
                    for pattern in patterns
                ),
            )
        )
    elif args.backend == "cp-group-fixed":
        if any(symbol is None for pattern in patterns for symbol in pattern):
            raise SystemExit("cp-group-fixed requires a fully pinned schedule")
        status, witness = recover_cp_sat_free_group_completion(
            patterns,  # type: ignore[arg-type]
            ciphertexts,
            deck_size=args.deck_size,
            plaintext_alphabet_size=action_count,
            timeout_seconds=args.timeout_ms / 1_000,
            break_state_symmetry=not args.no_position_symmetry,
            pinned_audit=pinned_audit,
            operation_hints=(
                planted_operations if args.hint_plant_key else None
            ),
        )
    elif args.backend == "cp-sat":
        status, witness = recover_cp_sat_gak(
            patterns,
            ciphertexts,
            deck_size=args.deck_size,
            plaintext_alphabet_size=action_count,
            timeout_seconds=args.timeout_ms / 1_000,
            break_position_symmetry=not args.no_position_symmetry,
        )
    else:
        recovery = (
            recover_symbolic_sparse_gak
            if args.backend == "sparse"
            else recover_explicit_permutation_gak
        )
        status, witness = recovery(
            patterns,
            ciphertexts,
            deck_size=args.deck_size,
            plaintext_alphabet_size=action_count,
            pinned_action_count=(
                min(len(alphabet), action_count)
                if args.mode != "impossible"
                else 1
            ),
            timeout_ms=args.timeout_ms,
            break_position_symmetry=not args.no_position_symmetry,
            break_extra_action_symmetry=not args.no_action_symmetry,
        )
    elapsed = time.monotonic() - started
    print(
        f"status={status} elapsed_seconds={elapsed:.3f} "
        f"exact_replay={'yes' if witness is not None else 'no'}"
    )
    if witness is not None:
        print(f"witness_sha256={_digest_witness(witness)}")
        _print_gaps(witness.plaintexts, phrase_length=len(phrase))
        if args.print_witness_json:
            print(
                "witness_json="
                + json.dumps(
                    {
                        "initial_decks": witness.initial_decks,
                        "operations": witness.operations,
                        "plaintexts": witness.plaintexts,
                    },
                    separators=(",", ":"),
                )
            )


if __name__ == "__main__":
    main()
