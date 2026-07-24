#!/usr/bin/env python3
"""Independent optional CP-SAT check of adjacent hidden-wheel chords."""

from __future__ import annotations

import argparse

from eye_mystery.hidden_geometry import chord_constraints

try:
    from ortools.sat.python import cp_model
except ModuleNotFoundError as error:  # pragma: no cover - optional dependency
    raise SystemExit(
        "install the project optional dependency set 'cp' to run this check"
    ) from error


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--maximize", action="store_true")
    parser.add_argument("--log", action="store_true")
    args = parser.parse_args()

    constraints = chord_constraints()
    labels = sorted(
        {label for item in constraints for label in item.labels}
    )
    model = cp_model.CpModel()
    coordinates = {
        label: model.new_int_var(0, 82, f"coordinate_{label}")
        for label in labels
    }
    model.add_all_different(coordinates.values())
    first = constraints[0]
    model.add(coordinates[first.source_left] == 0)
    model.add(coordinates[first.source_right] == 1)

    enabled = []
    for index, item in enumerate(constraints):
        positive = model.new_bool_var(f"positive_{index}")
        active = (
            model.new_bool_var(f"active_{index}")
            if args.maximize
            else None
        )
        plus_wrap = model.new_int_var(-1, 1, f"plus_wrap_{index}")
        minus_wrap = model.new_int_var(-1, 1, f"minus_wrap_{index}")
        source_delta = (
            coordinates[item.source_right] - coordinates[item.source_left]
        )
        target_delta = (
            coordinates[item.target_right] - coordinates[item.target_left]
        )
        plus_enforcement = [positive]
        minus_enforcement = [positive.Not()]
        if active is not None:
            plus_enforcement.append(active)
            minus_enforcement.append(active)
            enabled.append(active)
        model.add(
            source_delta - target_delta == 83 * plus_wrap
        ).only_enforce_if(plus_enforcement)
        model.add(
            source_delta + target_delta == 83 * minus_wrap
        ).only_enforce_if(minus_enforcement)
    if args.maximize:
        model.maximize(sum(enabled))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_workers = args.workers
    solver.parameters.log_search_progress = args.log
    status = solver.solve(model)
    print(
        f"status={solver.status_name(status)}; wall={solver.wall_time:.6f}; "
        f"conflicts={solver.num_conflicts}; branches={solver.num_branches}"
    )
    if args.maximize:
        print(
            f"objective={solver.objective_value:g}; "
            f"bound={solver.best_objective_bound:g}"
        )
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(
            "coordinates="
            + ",".join(
                f"{label}:{solver.value(coordinates[label])}"
                for label in labels
            )
        )


if __name__ == "__main__":
    main()
