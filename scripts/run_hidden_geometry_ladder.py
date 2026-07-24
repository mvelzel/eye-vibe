#!/usr/bin/env python3
"""Run the frozen exact hidden-geometry lag ladder."""

from __future__ import annotations

import argparse
from collections import Counter

from eye_mystery.hidden_geometry import (
    FIRST_FAMILY_NAMES,
    LAST_FAMILY_NAMES,
    NONLITERAL_CONTEXT_SPECS,
    chord_constraints,
    linear_core_certificate,
    minimize_unsat_core,
    repair_hidden_geometry,
    repair_hidden_geometry_classes,
    solve_hidden_geometry,
    solve_hidden_geometry_bitvector,
)


def describe(
    label: str,
    constraints,
    *,
    timeout_ms: int,
    core: bool = False,
    encoding: str = "integer",
):
    if core:
        function = minimize_unsat_core
    elif encoding == "bitvector":
        function = solve_hidden_geometry_bitvector
    else:
        function = solve_hidden_geometry
    result = function(constraints, timeout_ms=timeout_ms)
    print(
        f"{label}: {result.outcome}; constraints={result.constraints}; "
        f"labels={result.labels}; seconds={result.elapsed_seconds:.3f}"
    )
    if result.reason:
        print(f"  reason={result.reason}")
    if result.core:
        print(f"  deletion-minimal core={len(result.core)}")
        for item in result.core:
            print(
                f"    {item.context} lag={item.lag} index={item.index}: "
                f"({item.source_left},{item.source_right}) ~ "
                f"({item.target_left},{item.target_right})"
            )
        print(
            "  core contexts="
            + repr(dict(sorted(Counter(item.context for item in result.core).items())))
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-ms", type=int, default=60_000)
    parser.add_argument("--max-lag", type=int, default=8)
    parser.add_argument("--minimize-core", action="store_true")
    parser.add_argument("--repair", action="store_true")
    parser.add_argument(
        "--mode",
        choices=("summary", "adjacent", "full"),
        default="summary",
    )
    parser.add_argument("--restarts", type=int, default=20)
    parser.add_argument("--steps", type=int, default=200_000)
    parser.add_argument(
        "--encoding",
        choices=("integer", "bitvector"),
        default="integer",
    )
    args = parser.parse_args()

    names = tuple(spec[0] for spec in NONLITERAL_CONTEXT_SPECS)
    certificate = linear_core_certificate()
    print(
        "short-core certificate: "
        f"constraints={certificate.constraints}; labels={certificate.labels}; "
        f"collision branches={certificate.forced_collision_branches}/"
        f"{certificate.orientation_branches}; "
        f"deletion survivors={certificate.deletion_survivors}"
    )
    print(
        "  collision witnesses="
        + repr(dict(certificate.collision_witness_counts))
    )
    if args.repair:
        constraints = chord_constraints()
        direct = repair_hidden_geometry(
            constraints, restarts=args.restarts, steps_per_restart=args.steps
        )
        result = repair_hidden_geometry_classes(
            constraints, restarts=args.restarts, steps_per_restart=args.steps
        )
        print(
            f"direct repair: {direct.satisfied}/{direct.constraints}; "
            f"restart={direct.restart}; step={direct.steps}; "
            f"complete={direct.complete}"
        )
        print(
            f"class repair: {result.satisfied}/{result.constraints}; "
            f"class-pair agreement={result.class_edge_agreement}/"
            f"{result.class_edges}; "
            f"restart={result.restart}; step={result.steps}; "
            f"complete={result.complete}"
        )
        if result.complete:
            print("coordinates=" + ",".join(map(str, result.coordinates)))
        return

    if args.mode == "summary":
        for name, _, _, _, _, length in NONLITERAL_CONTEXT_SPECS:
            describe(
                f"context={name},all-lags",
                chord_constraints(names=(name,), lags=range(1, length)),
                timeout_ms=args.timeout_ms,
                encoding=args.encoding,
            )
        maximum_length = max(spec[-1] for spec in NONLITERAL_CONTEXT_SPECS)
        for family, selected in (
            ("first", FIRST_FAMILY_NAMES),
            ("last", LAST_FAMILY_NAMES),
            ("combined", names),
        ):
            describe(
                f"family={family},all-lags",
                chord_constraints(
                    names=selected, lags=range(1, maximum_length)
                ),
                timeout_ms=args.timeout_ms,
                encoding=args.encoding,
            )
        for label, selected, maximum in (
            ("first", FIRST_FAMILY_NAMES, 6),
            ("last", LAST_FAMILY_NAMES, 3),
            ("combined", names, 3),
        ):
            describe(
                f"family={label},lags=1..{maximum}",
                chord_constraints(
                    names=selected, lags=range(1, maximum + 1)
                ),
                timeout_ms=args.timeout_ms,
                encoding=args.encoding,
            )
        describe(
            "family=last,lag=5",
            chord_constraints(names=LAST_FAMILY_NAMES, lags=(5,)),
            timeout_ms=args.timeout_ms,
            encoding=args.encoding,
        )
        return

    for name in names:
        describe(
            f"context={name},lag=1",
            chord_constraints(names=(name,)),
            timeout_ms=args.timeout_ms,
            encoding=args.encoding,
        )

    for family, selected in (
        ("first", FIRST_FAMILY_NAMES),
        ("last", LAST_FAMILY_NAMES),
        ("combined", names),
    ):
        describe(
            f"family={family},lag=1",
            chord_constraints(names=selected),
            timeout_ms=args.timeout_ms,
            core=args.minimize_core,
            encoding=args.encoding,
        )

    if args.mode == "adjacent":
        return

    for lag in range(1, args.max_lag + 1):
        describe(
            f"combined,lag={lag}",
            chord_constraints(lags=(lag,)),
            timeout_ms=args.timeout_ms,
            encoding=args.encoding,
        )
    for maximum in range(1, args.max_lag + 1):
        result = describe(
            f"combined,lags=1..{maximum}",
            chord_constraints(lags=range(1, maximum + 1)),
            timeout_ms=args.timeout_ms,
            core=args.minimize_core,
            encoding=args.encoding,
        )
        if result.outcome == "unsat":
            break


if __name__ == "__main__":
    main()
