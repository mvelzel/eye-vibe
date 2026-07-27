#!/usr/bin/env python3
"""Run the frozen CNF solver on the four unresolved context pairs."""

from __future__ import annotations

import argparse
import multiprocessing
from queue import Empty

from eye_mystery.hidden_geometry_cnf import solve_hidden_geometry_cnf
from eye_mystery.hidden_geometry_pairs import (
    pair_constraints,
    planted_sat_pair,
    split_equidistant_triangle,
)


TARGET_PAIRS = (
    ("first-gap30", "first-cross"),
    ("last-west4", "last-east5"),
    ("last-west4", "last-east3"),
    ("last-east5", "last-east3"),
)


def _solve_worker(left: str, right: str, queue) -> None:
    result = solve_hidden_geometry_cnf(pair_constraints(left, right))
    queue.put(result)


def _run_with_timeout(
    left: str,
    right: str,
    *,
    timeout_seconds: float,
):
    context = multiprocessing.get_context("spawn")
    queue = context.Queue()
    process = context.Process(target=_solve_worker, args=(left, right, queue))
    process.start()
    process.join(timeout_seconds)
    if process.is_alive():
        process.terminate()
        process.join()
        queue.close()
        return None
    if process.exitcode != 0:
        queue.close()
        raise RuntimeError(
            f"CNF child for {left}+{right} exited {process.exitcode}"
        )
    try:
        return queue.get_nowait()
    except Empty as error:
        raise RuntimeError("CNF child returned no result") from error
    finally:
        queue.close()


def _check_controls() -> None:
    sat_left, sat_right = planted_sat_pair()
    triangle_left, triangle_right = split_equidistant_triangle()
    observed = tuple(
        solve_hidden_geometry_cnf(constraints, modulus=modulus).outcome
        for constraints, modulus in (
            (sat_left, 7),
            (sat_right, 7),
            (sat_left + sat_right, 7),
            (triangle_left, 5),
            (triangle_right, 5),
            (triangle_left + triangle_right, 5),
        )
    )
    expected = ("sat", "sat", "sat", "sat", "sat", "unsat")
    if observed != expected:
        raise AssertionError(
            f"CNF controls failed: expected {expected}, got {observed}"
        )
    duplicate = solve_hidden_geometry_cnf(
        sat_left,
        modulus=7,
        fixed_coordinates={2: 0},
    )
    if duplicate.outcome != "unsat":
        raise AssertionError("CNF injection control failed")
    print(f"controls={observed}; duplicate={duplicate.outcome}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=120.0)
    args = parser.parse_args()
    _check_controls()
    counts = {"sat": 0, "unsat": 0, "unknown": 0}
    for left, right in TARGET_PAIRS:
        result = _run_with_timeout(
            left,
            right,
            timeout_seconds=args.seconds,
        )
        if result is None:
            counts["unknown"] += 1
            print(
                f"pair={left}+{right}; outcome=unknown; "
                f"reason=timeout; seconds={args.seconds:.3f}",
                flush=True,
            )
            continue
        counts[result.outcome] += 1
        print(
            f"pair={left}+{right}; outcome={result.outcome}; "
            f"constraints={result.constraints}; labels={result.labels}; "
            f"classes={result.classes}; variables={result.variables}; "
            f"clauses={result.clauses}; seconds={result.elapsed_seconds:.3f}",
            flush=True,
        )
        if result.outcome == "sat":
            print(
                "coordinates="
                + ",".join(
                    f"{label}:{coordinate}"
                    for label, coordinate in result.coordinates
                ),
                flush=True,
            )
    print(f"summary={counts}")


if __name__ == "__main__":
    main()
