#!/usr/bin/env python3
"""Solve a known-prefix crib in the common-base sparse-deck model.

Each plaintext symbol selects a fixed top-swap rank and one fixed non-top
transposition.  The nine distinct markers are modeled as ordinary, distinct
plaintext symbols so they can establish message-specific hidden states.
"""

from __future__ import annotations

import argparse

import z3

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.deck_shuffles import standard_base_candidates


HERMITIC_PREFIXES = {
    "east1": "THATWHICHISABOVEISLIKETO",
    "west1": "THATWHICHISABOVEISLIKETO",
    "east2": "THATWHICHISABOVEISLIKETO",
    "west2": "THERE",
    "east3": "THEREISNO",
    "west3": "THERE",
    "east4": "THEREISNOGOODTHATCAN",
    "west4": "THEREISNOGOODTHATCAN",
    "east5": "THEREISNOGOODTHATCAN",
}

LOWER_WITNESS_RANKS = {
    "T": 66,
    "H": 18,
    "E": 49,
    "R": 75,
    "I": 2,
    "S": 60,
    "N": 29,
    "O": 40,
    "G": 59,
    "D": 15,
    "A": 68,
    "C": 36,
}

LOWER_WITNESS_SWAPS = {
    "T": (5, 18),
    "H": (18, 55),
    "E": (18, 54),
    "R": (18, 49),
    "I": (9, 18),
    "S": (59, 66),
    "N": (59, 60),
    "O": (9, 40),
    "G": (9, 18),
    "D": (29, 47),
    "A": (3, 66),
    "C": (54, 68),
}

SHARED_WITNESS_SECOND_SWAPS = {
    "T": (3, 62),
    "H": (48, 68),
    "A": (9, 61),
    "W": (18, 75),
    "I": (24, 36),
    "C": (2, 42),
    "E": (1, 9),
    "R": (1, 24),
    "S": (17, 24),
    "N": (17, 18),
    "O": (18, 36),
    "G": (18, 18),
    "D": (2, 2),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base",
        default="identity",
        help="standard base-candidate name, or identity",
    )
    parser.add_argument("--timeout-ms", type=int, default=60_000)
    parser.add_argument("--solver-seed", type=int, default=0)
    parser.add_argument(
        "--hidden-swaps", type=int, choices=(1, 2, 3), default=1
    )
    parser.add_argument(
        "--messages",
        help="comma-separated message names (default: all nine)",
    )
    parser.add_argument(
        "--omit-markers",
        action="store_true",
        help="reset after and omit the distinct first ciphertext symbol",
    )
    parser.add_argument("--top-length", type=int)
    parser.add_argument("--lower-length", type=int)
    parser.add_argument(
        "--text",
        help="override the crib text when exactly one message is selected",
    )
    parser.add_argument("--unsat-core", action="store_true")
    parser.add_argument(
        "--incremental-last",
        action="store_true",
        help="solve the prefix first, then add the final output constraint",
    )
    parser.add_argument(
        "--incremental-output",
        metavar="MESSAGE:ZERO_BASED_POSITION",
        help="defer one named output constraint until after the first solve",
    )
    parser.add_argument(
        "--fix-rank",
        action="append",
        default=[],
        metavar="SYMBOL:RANK",
    )
    parser.add_argument(
        "--fix-swap",
        action="append",
        default=[],
        metavar="SYMBOL:SLOT:LEFT:RIGHT",
    )
    parser.add_argument(
        "--seed-lower-witness",
        action="store_true",
        help="fix the verified lower ranks and slot-0 swaps",
    )
    parser.add_argument(
        "--seed-shared-witness",
        action="store_true",
        help="fix the verified upper-10/lower-20 ranks and first two slots",
    )
    args = parser.parse_args()

    candidates = dict(standard_base_candidates(83))
    if args.base == "identity":
        base = tuple(range(83))
    elif args.base in candidates:
        base = candidates[args.base]
    else:
        raise SystemExit(f"unknown standard base: {args.base}")

    selected_order = MESSAGE_ORDER
    if args.messages:
        requested = tuple(args.messages.split(","))
        unknown = set(requested) - set(MESSAGE_ORDER)
        if unknown:
            raise SystemExit(f"unknown messages: {sorted(unknown)}")
        selected_order = tuple(
            name for name in MESSAGE_ORDER if name in requested
        )
    selected_prefixes = {}
    if args.text and len(selected_order) != 1:
        raise SystemExit("--text requires exactly one selected message")
    for name in selected_order:
        prefix = args.text or HERMITIC_PREFIXES[name]
        limit = (
            args.top_length
            if name in ("east1", "west1", "east2")
            else args.lower_length
        )
        selected_prefixes[name] = prefix if limit is None else prefix[:limit]
    plaintexts = {
        name: (
            tuple(selected_prefixes[name])
            if args.omit_markers
            else (f"marker:{name}", *selected_prefixes[name])
        )
        for name in selected_order
    }
    ciphertext_start = 1 if args.omit_markers else 0
    ciphertexts = {
        name: trigram_values(MESSAGES[name])[ciphertext_start:][
            : len(plaintexts[name])
        ]
        for name in selected_order
    }
    alphabet = tuple(
        dict.fromkeys(
            symbol
            for name in selected_order
            for symbol in plaintexts[name]
        )
    )
    safe_names = {
        symbol: f"s{index}" for index, symbol in enumerate(alphabet)
    }
    value_sort = z3.BitVecSort(7)
    ranks = {
        symbol: z3.BitVec(f"rank_{safe_names[symbol]}", 7)
        for symbol in alphabet
    }
    lefts = {
        (symbol, slot): z3.BitVec(
            f"left_{safe_names[symbol]}_{slot}", 7
        )
        for symbol in alphabet
        for slot in range(args.hidden_swaps)
    }
    rights = {
        (symbol, slot): z3.BitVec(
            f"right_{safe_names[symbol]}_{slot}", 7
        )
        for symbol in alphabet
        for slot in range(args.hidden_swaps)
    }

    solver = z3.SolverFor("QF_AUFBV")
    solver.set(timeout=args.timeout_ms)
    solver.set(random_seed=args.solver_seed)
    if args.unsat_core:
        solver.set(unsat_core=True)
    solver.add(z3.Distinct(*ranks.values()))
    for symbol in alphabet:
        solver.add(z3.UGE(ranks[symbol], 1), z3.ULT(ranks[symbol], 83))
        for slot in range(args.hidden_swaps):
            left = lefts[symbol, slot]
            right = rights[symbol, slot]
            solver.add(z3.UGE(left, 1), z3.ULT(left, 83))
            solver.add(z3.UGE(right, 1), z3.ULT(right, 83))
            solver.add(z3.ULE(left, right))
    for specification in args.fix_rank:
        try:
            symbol, rendered_rank = specification.rsplit(":", 1)
            fixed_rank = int(rendered_rank)
        except ValueError as error:
            raise SystemExit(
                f"invalid --fix-rank {specification!r}"
            ) from error
        if symbol not in ranks or not 1 <= fixed_rank < 83:
            raise SystemExit(
                f"invalid --fix-rank {specification!r}"
            )
        solver.add(ranks[symbol] == z3.BitVecVal(fixed_rank, 7))
    if args.seed_lower_witness or args.seed_shared_witness:
        for symbol, fixed_rank in LOWER_WITNESS_RANKS.items():
            if symbol in ranks:
                solver.add(
                    ranks[symbol] == z3.BitVecVal(fixed_rank, 7)
                )
        if args.seed_shared_witness and "W" in ranks:
            solver.add(ranks["W"] == z3.BitVecVal(13, 7))
    for specification in args.fix_swap:
        try:
            symbol, rendered_slot, rendered_left, rendered_right = (
                specification.rsplit(":", 3)
            )
            slot = int(rendered_slot)
            fixed_left = int(rendered_left)
            fixed_right = int(rendered_right)
        except ValueError as error:
            raise SystemExit(
                f"invalid --fix-swap {specification!r}"
            ) from error
        if (
            symbol not in ranks
            or not 0 <= slot < args.hidden_swaps
            or not 1 <= fixed_left < 83
            or not 1 <= fixed_right < 83
        ):
            raise SystemExit(
                f"invalid --fix-swap {specification!r}"
            )
        solver.add(
            lefts[symbol, slot] == z3.BitVecVal(fixed_left, 7),
            rights[symbol, slot] == z3.BitVecVal(fixed_right, 7),
        )
    if args.seed_lower_witness or args.seed_shared_witness:
        if args.hidden_swaps < 1:
            raise SystemExit("lower witness requires a hidden-swap slot")
        for symbol, (fixed_left, fixed_right) in (
            LOWER_WITNESS_SWAPS.items()
        ):
            if symbol in ranks:
                solver.add(
                    lefts[symbol, 0] == z3.BitVecVal(fixed_left, 7),
                    rights[symbol, 0]
                    == z3.BitVecVal(fixed_right, 7),
                )
        if args.seed_shared_witness and "W" in ranks:
            solver.add(
                lefts["W", 0] == z3.BitVecVal(2, 7),
                rights["W", 0] == z3.BitVecVal(29, 7),
            )
    if args.seed_shared_witness:
        if args.hidden_swaps < 2:
            raise SystemExit("shared witness requires two hidden-swap slots")
        for symbol, (fixed_left, fixed_right) in (
            SHARED_WITNESS_SECOND_SWAPS.items()
        ):
            if symbol in ranks:
                solver.add(
                    lefts[symbol, 1] == z3.BitVecVal(fixed_left, 7),
                    rights[symbol, 1]
                    == z3.BitVecVal(fixed_right, 7),
                )

    position_variable = z3.BitVec("position", 7)
    identity_deck = z3.Lambda(position_variable, position_variable)
    base_array = z3.Array("base_positions", value_sort, value_sort)
    for position, old_position in enumerate(base):
        solver.add(
            z3.Select(base_array, z3.BitVecVal(position, 7))
            == z3.BitVecVal(old_position, 7)
        )
    identity_base = base == tuple(range(83))

    total_steps = sum(map(len, plaintexts.values()))
    deferred_output: z3.BoolRef | None = None
    deferred_location: tuple[str, int] | None = None
    if args.incremental_output:
        try:
            deferred_name, rendered_position = (
                args.incremental_output.rsplit(":", 1)
            )
            deferred_location = (deferred_name, int(rendered_position))
        except ValueError as error:
            raise SystemExit(
                f"invalid --incremental-output {args.incremental_output!r}"
            ) from error
    steps = 0
    for message_index, name in enumerate(selected_order):
        deck = identity_deck
        for position, (symbol, ciphertext) in enumerate(
            zip(plaintexts[name], ciphertexts[name], strict=True)
        ):
            if identity_base:
                base_deck = deck
            else:
                base_deck = z3.Lambda(
                    position_variable,
                    z3.Select(
                        deck,
                        z3.Select(base_array, position_variable),
                    ),
                )
            rank = ranks[symbol]
            card_at_rank = z3.Select(base_deck, rank)
            output_constraint = card_at_rank == z3.BitVecVal(ciphertext, 7)
            should_defer = (
                args.incremental_last and steps == total_steps - 1
            ) or deferred_location == (name, position)
            if should_defer:
                if deferred_output is not None:
                    raise SystemExit("only one output can be deferred")
                deferred_output = output_constraint
            elif args.unsat_core:
                solver.assert_and_track(
                    output_constraint,
                    z3.Bool(f"output_{name}_{position}"),
                )
            else:
                solver.add(output_constraint)
            card_at_top = z3.Select(base_deck, z3.BitVecVal(0, 7))
            top_deck = z3.Store(
                z3.Store(base_deck, z3.BitVecVal(0, 7), card_at_rank),
                rank,
                card_at_top,
            )
            shuffled_deck = top_deck
            for slot in range(args.hidden_swaps):
                left = lefts[symbol, slot]
                right = rights[symbol, slot]
                card_at_left = z3.Select(shuffled_deck, left)
                card_at_right = z3.Select(shuffled_deck, right)
                shuffled_deck = z3.Store(
                    z3.Store(shuffled_deck, left, card_at_right),
                    right,
                    card_at_left,
                )
            next_deck = z3.Array(
                f"deck_m{message_index}_p{position + 1}",
                value_sort,
                value_sort,
            )
            solver.add(
                next_deck == shuffled_deck
            )
            deck = next_deck
            steps += 1

    print(
        f"base={args.base} symbols={len(alphabet)} steps={steps} "
        f"constraints={len(solver.assertions())}",
        flush=True,
    )
    result = solver.check()
    if deferred_output is not None:
        print("prefix result:", result, flush=True)
        if result == z3.sat:
            solver.add(deferred_output)
            result = solver.check()
    print("result:", result)
    if result == z3.unsat and args.unsat_core:
        print("unsat output core:", tuple(map(str, solver.unsat_core())))
    if result != z3.sat:
        return
    model = solver.model()
    print("symbol rank hidden-swaps")
    for symbol in alphabet:
        rendered_swaps = " ".join(
            f"{model.eval(lefts[symbol, slot]).as_long():>2}:"
            f"{model.eval(rights[symbol, slot]).as_long():>2}"
            for slot in range(args.hidden_swaps)
        )
        print(
            f"{symbol:>12} {model.eval(ranks[symbol]).as_long():>2} "
            f"{rendered_swaps}"
        )


if __name__ == "__main__":
    main()
