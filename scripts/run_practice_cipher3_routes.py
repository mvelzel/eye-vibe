#!/usr/bin/env python3
"""Calibrate and run the frozen six-stream Cipher 3 route catalog."""

from __future__ import annotations

import argparse
import hashlib
import random
from collections import Counter
from pathlib import Path

from eye_mystery.practice_cipher3_routes import (
    RouteScore,
    SixStreamRoute,
    coordinate_equivalence_class,
    equivalent_coordinate_order,
    generate_action_control,
    globally_equivalent_coordinate_order,
    route_catalog,
    route_sort_key,
    score_route,
    search_routes,
)
from eye_mystery.practice_cipher3_wide import (
    load_cipher3,
    normalize_plaintext42,
)


TRAINING_SHA256 = "922e2a12ccb43a4c9544c260b2166c6ad2097aeb5957faeee113f173bb857cd0"
CONTROL_ROUTES = (
    SixStreamRoute(
        "row",
        False,
        (2, 5, 1, 4, 0, 3),
        "snake-reverse",
    ),
    SixStreamRoute(
        "column",
        True,
        (4, 1, 5, 0, 3, 2),
        "snake",
        True,
        True,
    ),
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_groups() -> dict[str, tuple[tuple[int, ...], ...]]:
    source = load_cipher3()
    return {
        group: tuple(tuple(row) for row in source[group])
        for group in ("A", "B", "C")
    }


def format_route(route: SixStreamRoute) -> str:
    common = (
        f"{route.kind} trim={int(route.trim_body)} "
        f"order={''.join(map(str, route.row_order))} mode={route.mode}"
    )
    if route.kind == "column":
        return (
            f"{common} align={'R' if route.align_right else 'L'} "
            f"columns={'R' if route.reverse_columns else 'L'}"
        )
    return common


def score_summary(label: str, score: RouteScore) -> str:
    return (
        f"{label}: edges={score.distinct_edges}/{score.events} "
        f"K={score.effective_uniform_choices:.6f} "
        f"diff={score.difference_support} "
        f"degree={score.maximum_outdegree}/{score.maximum_indegree}"
    )


def equivalent_rank(
    scores: tuple[RouteScore, ...],
    lengths: tuple[int, ...],
    true_route: SixStreamRoute,
) -> int:
    return next(
        index
        for index, score in enumerate(scores, 1)
        if equivalent_coordinate_order(
            lengths,
            score.route,
            true_route,
        )
    )


def selected_is_equivalent(
    lengths: tuple[int, ...],
    selected: SixStreamRoute,
    true_route: SixStreamRoute,
) -> bool:
    return equivalent_coordinate_order(lengths, selected, true_route)


def control_groups(
    lengths: dict[str, tuple[int, ...]],
    route: SixStreamRoute,
    weights: tuple[float, ...],
    *,
    seed: int,
) -> dict[str, tuple[tuple[int, ...], ...]]:
    shifts = random.Random(seed ^ 0x51F75).sample(range(1, 83), 42)
    return {
        group: generate_action_control(
            lengths[group],
            route,
            shifts,
            weights,
            seed=seed ^ (group_index + 1) * 0x9E3779B1,
        )
        for group_index, group in enumerate(("A", "B", "C"))
    }


def has_no_doubles(groups: dict[str, tuple[tuple[int, ...], ...]]) -> bool:
    return not any(
        left == right
        for rows in groups.values()
        for row in rows
        for left, right in zip(row, row[1:])
    )


def selector_value(score: RouteScore, selector: str) -> float:
    if selector == "broad":
        return score.effective_uniform_choices
    if selector == "additive":
        return float(score.difference_support)
    raise ValueError(f"unknown selector: {selector}")


def staged_scores(
    groups: dict[str, tuple[tuple[int, ...], ...]],
    lengths: dict[str, tuple[int, ...]],
    catalog: tuple[SixStreamRoute, ...],
    selected: RouteScore,
    selector: str,
) -> tuple[
    tuple[SixStreamRoute, ...],
    tuple[tuple[SixStreamRoute, RouteScore], ...],
    tuple[tuple[SixStreamRoute, RouteScore], ...],
    tuple[tuple[SixStreamRoute, RouteScore, RouteScore], ...],
]:
    a_class = coordinate_equivalence_class(
        lengths["A"],
        catalog,
        selected.route,
    )
    b_scored = tuple(
        (route, score_route(groups["B"], route))
        for route in a_class
    )
    b_survivors = tuple(
        (route, score)
        for route, score in b_scored
        if selector_value(score, selector) <= 42
    )
    c_scored = tuple(
        (route, score_b, score_route(groups["C"], route))
        for route, score_b in b_survivors
    )
    return a_class, b_scored, b_survivors, c_scored


def report_staged(
    selector: str,
    selected: RouteScore,
    groups: dict[str, tuple[tuple[int, ...], ...]],
    lengths: dict[str, tuple[int, ...]],
    catalog: tuple[SixStreamRoute, ...],
    *,
    true_route: SixStreamRoute | None = None,
) -> None:
    a_class, b_scored, b_survivors, c_scored = staged_scores(
        groups,
        lengths,
        catalog,
        selected,
        selector,
    )
    c_passes = tuple(
        (route, score_b, score_c)
        for route, score_b, score_c in c_scored
        if selector_value(score_c, selector) <= 42
    )
    print(
        f"  {selector} staged A-class={len(a_class)} "
        f"B-survivors={len(b_survivors)} C-passes={len(c_passes)}"
    )
    if true_route is not None:
        length_sets = tuple(lengths[group] for group in ("A", "B", "C"))
        true_in_a = any(
            equivalent_coordinate_order(lengths["A"], route, true_route)
            for route in a_class
        )
        true_in_b = any(
            globally_equivalent_coordinate_order(
                length_sets,
                route,
                true_route,
            )
            for route, _score_b in b_survivors
        )
        true_in_c = any(
            globally_equivalent_coordinate_order(
                length_sets,
                route,
                true_route,
            )
            and selector_value(score_c, selector) <= 42
            for route, _score_b, score_c in c_scored
        )
        print(
            f"  {selector} true/global-equivalent "
            f"A={true_in_a} B={true_in_b} C={true_in_c}"
        )
    for route, score_b in b_scored:
        print(
            f"    B {format_route(route)} "
            f"value={selector_value(score_b, selector):.6f} "
            f"pass={selector_value(score_b, selector) <= 42}"
        )
    for route, score_b, score_c in c_scored:
        print(
            f"    C {format_route(route)} "
            f"B={selector_value(score_b, selector):.6f} "
            f"C={selector_value(score_c, selector):.6f} "
            f"C-pass={selector_value(score_c, selector) <= 42}"
        )


def run_control(
    lengths: dict[str, tuple[int, ...]],
    weights: tuple[float, ...],
    catalog: tuple[SixStreamRoute, ...],
    *,
    seed: int,
) -> None:
    for control_index, true_route in enumerate(CONTROL_ROUTES):
        if not any(route.kind == true_route.kind for route in catalog):
            continue
        groups = control_groups(
            lengths,
            true_route,
            weights,
            seed=seed ^ control_index * 0xC0117A,
        )
        search = search_routes(groups["A"], catalog=catalog)
        broad = search.broad[0]
        additive = search.additive[0]
        broad_b = score_route(groups["B"], broad.route)
        broad_c = score_route(groups["C"], broad.route)
        additive_b = score_route(groups["B"], additive.route)
        additive_c = score_route(groups["C"], additive.route)
        broad_rank = equivalent_rank(
            search.broad,
            lengths["A"],
            true_route,
        )
        additive_rank = equivalent_rank(
            search.additive,
            lengths["A"],
            true_route,
        )
        broad_exact = selected_is_equivalent(
            lengths["A"],
            broad.route,
            true_route,
        )
        additive_exact = selected_is_equivalent(
            lengths["A"],
            additive.route,
            true_route,
        )
        print(f"CONTROL {control_index + 1}")
        print(f"  true     {format_route(true_route)}")
        print(f"  broad    {format_route(broad.route)}")
        print(f"  additive {format_route(additive.route)}")
        print(
            f"  equivalent rank broad={broad_rank} additive={additive_rank} "
            f"selected={broad_exact}/{additive_exact}"
        )
        print(f"  no adjacent doubles={has_no_doubles(groups)}")
        print(f"  {score_summary('broad A', broad)}")
        print(f"  {score_summary('broad B', broad_b)}")
        print(f"  {score_summary('broad C', broad_c)}")
        print(f"  {score_summary('additive A', additive)}")
        print(f"  {score_summary('additive B', additive_b)}")
        print(f"  {score_summary('additive C', additive_c)}")
        report_staged(
            "broad",
            broad,
            groups,
            lengths,
            catalog,
            true_route=true_route,
        )
        report_staged(
            "additive",
            additive,
            groups,
            lengths,
            catalog,
            true_route=true_route,
        )


def run_real(
    groups: dict[str, tuple[tuple[int, ...], ...]],
    lengths: dict[str, tuple[int, ...]],
    catalog: tuple[SixStreamRoute, ...],
) -> None:
    search = search_routes(groups["A"], catalog=catalog)
    broad = search.broad[0]
    additive = search.additive[0]
    print("REAL")
    for name, selected in (("broad", broad), ("additive", additive)):
        print(f"  {name} selected {format_route(selected.route)}")
        print(f"  {score_summary(f'{name} A', selected)}")
        report_staged(
            name,
            selected,
            groups,
            lengths,
            catalog,
        )
    print("  broad top=")
    for result in search.broad[:5]:
        print(f"    {score_summary(format_route(result.route), result)}")
    print("  additive top=")
    for result in search.additive[:5]:
        print(f"    {score_summary(format_route(result.route), result)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--training",
        type=Path,
        default=Path("/private/tmp/pg1661.txt"),
    )
    parser.add_argument("--phase", choices=("control", "real"), default="control")
    parser.add_argument("--catalog", choices=("all", "row", "column"), default="all")
    parser.add_argument("--seed", type=int, default=20260727)
    args = parser.parse_args()

    training_hash = file_sha256(args.training)
    if training_hash != TRAINING_SHA256:
        raise SystemExit(f"unexpected training SHA-256: {training_hash}")
    plaintext = normalize_plaintext42(args.training.read_text(errors="ignore"))
    counts = Counter(plaintext)
    weights = tuple(float(counts[value] + 1) for value in range(42))
    all_routes = route_catalog()
    catalog = tuple(
        route
        for route in all_routes
        if args.catalog == "all" or route.kind == args.catalog
    )
    catalog = tuple(sorted(catalog, key=route_sort_key))
    groups = load_groups()
    lengths = {
        group: tuple(map(len, groups[group]))
        for group in ("A", "B", "C")
    }

    if args.phase == "control":
        run_control(
            lengths,
            weights,
            catalog,
            seed=args.seed,
        )
    else:
        run_real(groups, lengths, catalog)


if __name__ == "__main__":
    main()
