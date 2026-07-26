#!/usr/bin/env python3
"""Audit the exact Earthquake-gear construction on the seven Eye contexts."""

from __future__ import annotations

import argparse

from eye_mystery.earthquake_gears import (
    audit_direct_rank,
    direct_parameter_candidates,
    solve_hidden_gear_with_z3,
    solve_relaxed_pairs_with_z3,
)
from eye_mystery.hidden_geometry import context_sequences


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--alphabet-sizes",
        type=int,
        nargs="+",
        default=(26, 29),
    )
    parser.add_argument("--timeout-ms", type=int, default=120_000)
    parser.add_argument(
        "--free-weights",
        action="store_true",
        help="also attempt the much harder arbitrary-weight hidden model",
    )
    parser.add_argument(
        "--relaxed-only",
        action="store_true",
        help="run the hidden same-distance relaxation but not exact continuity",
    )
    parser.add_argument("--skip-hidden", action="store_true")
    args = parser.parse_args()

    contexts = context_sequences()
    for alphabet_size in args.alphabet_sizes:
        direct = audit_direct_rank(
            contexts,
            plaintext_alphabet_size=alphabet_size,
        )
        print(
            f"direct m={alphabet_size}: "
            f"full_contexts={direct.best_full_contexts}/{direct.contexts} "
            f"matched_transitions={direct.best_matched_transitions}/"
            f"{direct.transitions} "
            f"best=(direction={direct.best_direction:+d},"
            f"scale={direct.best_scale}) "
            f"complete_configurations={direct.complete_configurations}"
        )
        for name, matched, transitions in direct.per_context_prefixes:
            print(f"  {name}: best_prefix={matched}/{transitions}")
        parameter_screen = direct_parameter_candidates(
            contexts,
            plaintext_alphabet_size=alphabet_size,
        )
        print(
            f"direct all-weights m={alphabet_size}: "
            f"survivors={len(parameter_screen.survivors)} "
            f"constraints={parameter_screen.constraints_tested}/"
            f"{parameter_screen.total_constraints} "
            f"stop={parameter_screen.stopping_constraint}"
        )

        if args.skip_hidden:
            continue
        relaxed = solve_relaxed_pairs_with_z3(
            contexts,
            plaintext_alphabet_size=alphabet_size,
            timeout_ms=args.timeout_ms,
        )
        print(
            f"hidden relaxed-pairs m={alphabet_size}: "
            f"{relaxed.status} elapsed={relaxed.elapsed_seconds:.3f}s "
            f"allowed_pairs={relaxed.allowed_pairs} "
            f"formula_bytes={relaxed.formula_bytes}"
        )
        if relaxed.status == "unsat":
            continue
        if args.relaxed_only:
            continue
        for direction in (-1, 1):
            result = solve_hidden_gear_with_z3(
                contexts,
                plaintext_alphabet_size=alphabet_size,
                direction=direction,
                weights=(1, 1, 1),
                timeout_ms=args.timeout_ms,
            )
            print(
                f"hidden equal-weights m={alphabet_size} "
                f"direction={direction:+d}: "
                f"{result.status} elapsed={result.elapsed_seconds:.3f}s "
                f"formula_bytes={result.formula_bytes}"
            )
            if result.witness is not None:
                print(f"  weights={result.witness.weights}")
                print(
                    "  coordinates="
                    + ",".join(
                        f"{label}:{position}"
                        for label, position in result.witness.coordinates
                    )
                )
                for context in result.witness.contexts:
                    print(
                        f"  {context.name}: "
                        f"phases={context.source_phase},{context.target_phase} "
                        f"distances={','.join(map(str, context.distances))}"
                    )
            if args.free_weights:
                free = solve_hidden_gear_with_z3(
                    contexts,
                    plaintext_alphabet_size=alphabet_size,
                    direction=direction,
                    timeout_ms=args.timeout_ms,
                )
                print(
                    f"hidden free-weights m={alphabet_size} "
                    f"direction={direction:+d}: "
                    f"{free.status} elapsed={free.elapsed_seconds:.3f}s "
                    f"formula_bytes={free.formula_bytes}"
                )
                if free.witness is not None:
                    print(f"  weights={free.witness.weights}")


if __name__ == "__main__":
    main()
