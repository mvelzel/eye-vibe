#!/usr/bin/env python3
"""Run the six predeclared tests in the fifth wide Eye fan-out."""

from __future__ import annotations

import argparse
import random
from statistics import median

from eye_mystery.corpus import (
    MESSAGES,
    MESSAGE_ORDER,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)
from eye_mystery.fifth_wide import (
    best_cellular_fit,
    best_grid_fit,
    best_radix_fit,
    best_stable_sort_fit,
    cellular_leave_one_pair_out,
    directed_edge_reuse,
    relabel_streams,
    rotate,
    transition_occupancy,
    turtle_bounding_area,
)
from eye_mystery.language_null import prefix_tree_parity_shuffle
from eye_mystery.visual_rows import visual_rows


GRID_ROWS = (
    ("east1", "west1", "east2", 24),
    ("east3", "west2", "west3", 5),
    ("east5", "east4", "west4", 20),
)


def row_chunks(streams: dict[str, tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    rows = []
    for name in MESSAGE_ORDER:
        cursor = 0
        for length in ROW_PAIR_TRIGRAM_LENGTHS[name]:
            rows.append(streams[name][cursor : cursor + length])
            cursor += length
    return tuple(rows)


def unique_visual_pairs(
    raw: dict[str, tuple[int, ...]], *, skip_first_pair: bool = False
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    pairs = []
    for name in MESSAGE_ORDER:
        rows = visual_rows(raw[name], ROW_PAIR_TRIGRAM_LENGTHS[name])
        start = 2 if skip_first_pair else 0
        pairs.extend(zip(rows[start::2], rows[start + 1 :: 2], strict=True))
    return tuple(dict.fromkeys(pairs))


def grid_records(
    bodies: dict[str, tuple[int, ...]],
    eligible: tuple[tuple[int, int], ...] | None = None,
) -> tuple[tuple[int, int, int], ...]:
    if eligible is None:
        selected = []
        for row_index, (target, left, right, start) in enumerate(GRID_ROWS):
            limit = min(len(bodies[target]), len(bodies[left]), len(bodies[right]))
            for index in range(start, limit):
                values = (bodies[target][index], bodies[left][index], bodies[right][index])
                if len(set(values)) == 3:
                    selected.append((row_index, index))
        eligible = tuple(selected)
    return tuple(
        (
            bodies[GRID_ROWS[row_index][0]][index],
            bodies[GRID_ROWS[row_index][1]][index],
            bodies[GRID_ROWS[row_index][2]][index],
        )
        for row_index, index in eligible
    )


def eligible_grid_positions(
    bodies: dict[str, tuple[int, ...]],
) -> tuple[tuple[int, int], ...]:
    positions = []
    for row_index, (target, left, right, start) in enumerate(GRID_ROWS):
        limit = min(len(bodies[target]), len(bodies[left]), len(bodies[right]))
        for index in range(start, limit):
            if len({bodies[target][index], bodies[left][index], bodies[right][index]}) == 3:
                positions.append((row_index, index))
    return tuple(positions)


def rotated_grid_bodies(
    bodies: dict[str, tuple[int, ...]], generator: random.Random
) -> dict[str, tuple[int, ...]]:
    output = {}
    starts = {
        name: start
        for target, left, right, start in GRID_ROWS
        for name in (target, left, right)
    }
    for name, body in bodies.items():
        start = starts[name]
        tail = body[start:]
        output[name] = body[:start] + rotate(tail, generator.randrange(len(tail)))
    return output


def turtle_score(raw: dict[str, tuple[int, ...]]) -> tuple[int, str]:
    canonical = sum(turtle_bounding_area(raw[name][3:]) for name in MESSAGE_ORDER)
    visual = 0
    for name in MESSAGE_ORDER:
        rows = visual_rows(raw[name], ROW_PAIR_TRIGRAM_LENGTHS[name])
        visual += turtle_bounding_area(tuple(value for row in rows for value in row))
    return min((canonical, "canonical"), (visual, "visual"))


def corrected(at_least: int, controls: int) -> float:
    return (at_least + 1) / (controls + 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=2_000)
    parser.add_argument(
        "--sort-controls",
        type=int,
        help="optional larger independent refinement for lane D",
    )
    parser.add_argument("--seed", type=int, default=0xF17E)
    args = parser.parse_args()
    generator = random.Random(args.seed)

    whole = {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}
    bodies = {name: whole[name][1:] for name in MESSAGE_ORDER}
    raw = {name: MESSAGES[name] for name in MESSAGE_ORDER}

    graph_observed, transitions, distinct = directed_edge_reuse(tuple(bodies.values()))
    graph_occupancy = transition_occupancy(tuple(bodies.values()))
    radix_observed = best_radix_fit(tuple(bodies.values()))
    graph_controls = []
    radix_controls = []
    for _ in range(args.controls):
        shuffled = prefix_tree_parity_shuffle(bodies, bodies, generator, start=0)
        graph_controls.append(directed_edge_reuse(tuple(shuffled.values()))[0])
        radix_controls.append(best_radix_fit(tuple(shuffled.values())).fraction)

    pairs = unique_visual_pairs(raw)
    suffix_pairs = unique_visual_pairs(raw, skip_first_pair=True)
    cellular_observed = best_cellular_fit(pairs)
    cellular_cross_validation = cellular_leave_one_pair_out(
        pairs,
        radius=cellular_observed.radius,
        shift=cellular_observed.shift,
    )
    cellular_controls = []
    suffix_cellular_observed = best_cellular_fit(
        suffix_pairs, maximum_radius=1
    )
    suffix_full_observed = best_cellular_fit(suffix_pairs)
    suffix_cross_validation = cellular_leave_one_pair_out(
        suffix_pairs,
        radius=suffix_full_observed.radius,
        shift=suffix_full_observed.shift,
    )
    suffix_cellular_controls = []
    for _ in range(args.controls):
        control_pairs = tuple(
            (top, rotate(bottom, generator.randrange(len(bottom))))
            for top, bottom in pairs
        )
        cellular_controls.append(best_cellular_fit(control_pairs).accuracy)
        suffix_control_pairs = tuple(
            (top, rotate(bottom, generator.randrange(len(bottom))))
            for top, bottom in suffix_pairs
        )
        suffix_cellular_controls.append(
            best_cellular_fit(
                suffix_control_pairs, maximum_radius=1
            ).accuracy
        )

    rows = row_chunks(whole)
    sort_observed = best_stable_sort_fit(rows)
    sort_controls = []
    sort_control_count = args.sort_controls or args.controls
    sort_generator = random.Random(args.seed ^ 0x5077)
    for _ in range(sort_control_count):
        mapping = list(range(83))
        sort_generator.shuffle(mapping)
        control_rows = row_chunks(relabel_streams(whole, mapping))
        sort_controls.append(best_stable_sort_fit(control_rows).fraction)

    eligible = eligible_grid_positions(bodies)
    grid_observed = best_grid_fit(grid_records(bodies, eligible))
    grid_controls = []
    for _ in range(args.controls):
        rotated = rotated_grid_bodies(bodies, generator)
        grid_controls.append(best_grid_fit(grid_records(rotated, eligible)).matches)

    turtle_observed, turtle_order = turtle_score(raw)
    turtle_controls = []
    for _ in range(args.controls):
        shuffled = prefix_tree_parity_shuffle(raw, raw, generator, start=3)
        turtle_controls.append(turtle_score(shuffled)[0])

    print("A directed graph route")
    print(
        f"  edge reuse={graph_observed}; transitions={transitions}; distinct={distinct}; "
        f"control median={median(graph_controls)}"
    )
    print(
        f"  maximum out/in degree={graph_occupancy.maximum_outdegree}/"
        f"{graph_occupancy.maximum_indegree}; effective uniform choices="
        f"{graph_occupancy.effective_uniform_choices:.6f}"
    )
    graph_hits = sum(value >= graph_observed for value in graph_controls)
    print(f"  corrected upper tail={(graph_hits + 1)}/{args.controls + 1}={corrected(graph_hits,args.controls):.6f}")

    print("B two-dimensional local rewrite")
    print(
        f"  unique row pairs={len(pairs)}; best={cellular_observed.correct}/"
        f"{cellular_observed.samples}={cellular_observed.accuracy:.6f}; "
        f"radius={cellular_observed.radius}; shift={cellular_observed.shift}; "
        f"contexts={cellular_observed.contexts}; control median={median(cellular_controls):.6f}"
    )
    print(
        f"  leave-one-pair-out={cellular_cross_validation.correct}/"
        f"{cellular_cross_validation.covered}="
        f"{cellular_cross_validation.accuracy:.6f} on "
        f"{cellular_cross_validation.covered}/{cellular_cross_validation.samples}="
        f"{cellular_cross_validation.coverage:.6f} covered cells"
    )
    cellular_hits = sum(value >= cellular_observed.accuracy for value in cellular_controls)
    print(f"  corrected upper tail={(cellular_hits + 1)}/{args.controls + 1}={corrected(cellular_hits,args.controls):.6f}")
    suffix_cellular_hits = sum(
        value >= suffix_cellular_observed.accuracy
        for value in suffix_cellular_controls
    )
    print(
        f"  after dropping prefix-bearing first row pairs: radius<=1 best="
        f"{suffix_cellular_observed.correct}/{suffix_cellular_observed.samples}="
        f"{suffix_cellular_observed.accuracy:.6f}; corrected upper tail="
        f"{suffix_cellular_hits + 1}/{args.controls + 1}="
        f"{corrected(suffix_cellular_hits,args.controls):.6f}"
    )
    print(
        f"  suffix-only radius-3 held-out coverage="
        f"{suffix_cross_validation.correct}/{suffix_cross_validation.covered} "
        f"on {suffix_cross_validation.covered}/{suffix_cross_validation.samples} cells"
    )

    print("C direct mixed-radix packet")
    print(
        f"  best printable={radix_observed.printable}/{radix_observed.length}="
        f"{radix_observed.fraction:.6f}; base={radix_observed.target_base}; "
        f"reversed={radix_observed.reversed_digits}; control median={median(radix_controls):.6f}"
    )
    radix_hits = sum(value >= radix_observed.fraction for value in radix_controls)
    print(f"  corrected upper tail={(radix_hits + 1)}/{args.controls + 1}={corrected(radix_hits,args.controls):.6f}")

    print("D stable-sort worksheet")
    print(
        f"  agreement={sort_observed.agreement}/{sort_observed.comparisons}="
        f"{sort_observed.fraction:.6f}; order={sort_observed.component_order}; "
        f"descending={sort_observed.descending}; control median={median(sort_controls):.6f}"
    )
    sort_hits = sum(value >= sort_observed.fraction for value in sort_controls)
    print(
        f"  corrected upper tail={(sort_hits + 1)}/{sort_control_count + 1}="
        f"{corrected(sort_hits,sort_control_count):.6f}"
    )

    print("E nonlinear digitwise grid operator")
    print(
        f"  pairwise-distinct reference positions={len(eligible)}; best="
        f"{grid_observed.matches}/{grid_observed.samples}; operation={grid_observed.operation}; "
        f"control median={median(grid_controls)}"
    )
    grid_hits = sum(value >= grid_observed.matches for value in grid_controls)
    print(f"  corrected upper tail={(grid_hits + 1)}/{args.controls + 1}={corrected(grid_hits,args.controls):.6f}")

    print("F raw-direction turtle drawing")
    print(
        f"  selected bounding-area sum={turtle_observed}; order={turtle_order}; "
        f"control median={median(turtle_controls)}"
    )
    turtle_hits = sum(value <= turtle_observed for value in turtle_controls)
    print(f"  corrected lower tail={(turtle_hits + 1)}/{args.controls + 1}={corrected(turtle_hits,args.controls):.6f}")


if __name__ == "__main__":
    main()
