#!/usr/bin/env python3
"""Matched-control audit of the frozen Wall-context deck screen.

The null applies one random permutation to the 83 Wall-context rows.  This
preserves every parameter table's multiset, the raw/zero-based relationship,
and all cross-field relationships within a Wall occurrence while breaking the
proposed assignment from Eye label to Wall occurrence.
"""

from __future__ import annotations

import argparse
import random
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from eye_mystery.noita_wall_messages import load_wall_message_lines
from eye_mystery.ninth_causal import CONTEXT_SPECS
from eye_mystery.synchronizing_bridge import bridge_specs, observed_metrics
from eye_mystery.wall_context_deck import (
    UPDATE_FAMILIES,
    decode_labels,
    encode_ranks,
    wall_parameter_tables,
)

from screen_source_deck_families import (
    ASCII_SIZE,
    body_streams,
    context_scores,
)


ROOT = Path(__file__).resolve().parents[1]
WALL_TEXT = ROOT / "artifacts" / "noita-wall-messages-en.txt"


@dataclass(frozen=True)
class Model:
    table: str
    deck: str
    family: str
    direction: str


@dataclass(frozen=True)
class Candidate:
    model: Model
    bridge_joint: bool
    bridge_lcp: int
    east_complete: bool
    east_switch: bool
    changed_positions: int
    departures_from_initial_relabel: int
    dynamic_input_labels: int
    static_relabel: bool
    global_equality_preserved: bool
    gated_departures_from_initial_relabel: int
    gated_dynamic_input_labels: int
    gated_static_relabel: bool
    old_bridge_departures: int
    new_phase_departures: int


def _transformed_streams(
    streams: Mapping[str, Sequence[int]],
    *,
    deck: Sequence[int],
    parameters: Sequence[int],
    family: str,
    direction: str,
    parameter_index: str,
) -> dict[str, tuple[int, ...]]:
    if direction == "label-decode":
        return {
            name: decode_labels(
                stream,
                deck,
                parameters,
                family=family,
                parameter_index=parameter_index,
            )
            for name, stream in streams.items()
        }
    if direction == "rank-encode":
        return {
            name: encode_ranks(
                stream,
                deck,
                parameters,
                family=family,
                parameter_index=parameter_index,
            )
            for name, stream in streams.items()
        }
    raise ValueError(direction)


def _degeneracy(
    source: Mapping[str, Sequence[int]],
    transformed: Mapping[str, Sequence[int]],
    *,
    deck: Sequence[int],
    direction: str,
) -> tuple[int, int, int, bool, bool, int, int, bool]:
    outputs_by_input: dict[int, set[int]] = defaultdict(set)
    gated_outputs_by_input: dict[int, set[int]] = defaultdict(set)
    changed = 0
    initial_relabel_departures = 0
    gated_relabel_departures = 0
    source_pairs: dict[int, list[tuple[str, int]]] = defaultdict(list)
    target_pairs: dict[int, list[tuple[str, int]]] = defaultdict(list)
    gated_cells: set[tuple[str, int]] = set()
    for _, left, left_start, right, right_start, length in CONTEXT_SPECS[6:]:
        gated_cells.update((left, position) for position in range(left_start, left_start + length))
        gated_cells.update((right, position) for position in range(right_start, right_start + length))
    inverse_deck = {label: rank for rank, label in enumerate(deck)}
    for name in source:
        for position, (before, after) in enumerate(
            zip(source[name], transformed[name], strict=True)
        ):
            baseline = (
                inverse_deck[before]
                if direction == "label-decode"
                else deck[before]
            )
            outputs_by_input[before].add(after)
            source_pairs[before].append((name, position))
            target_pairs[after].append((name, position))
            changed += before != after
            initial_relabel_departures += after != baseline
            if (name, position) in gated_cells:
                gated_outputs_by_input[before].add(after)
                gated_relabel_departures += after != baseline

    dynamic_labels = sum(len(outputs) > 1 for outputs in outputs_by_input.values())
    gated_dynamic_labels = sum(
        len(outputs) > 1 for outputs in gated_outputs_by_input.values()
    )
    static_relabel = dynamic_labels == 0
    # Exact equality-relation comparison over all message-position cells.
    global_equality = {
        frozenset(cells) for cells in source_pairs.values()
    } == {
        frozenset(cells) for cells in target_pairs.values()
    }
    return (
        changed,
        initial_relabel_departures,
        dynamic_labels,
        static_relabel,
        global_equality,
        gated_relabel_departures,
        gated_dynamic_labels,
        gated_dynamic_labels == 0,
    )


def _phase_departures(
    source: Mapping[str, Sequence[int]],
    transformed: Mapping[str, Sequence[int]],
    *,
    deck: Sequence[int],
    direction: str,
) -> tuple[int, int]:
    inverse_deck = {label: rank for rank, label in enumerate(deck)}

    def departure(message: str, position: int) -> bool:
        before = source[message][position]
        baseline = (
            inverse_deck[before]
            if direction == "label-decode"
            else deck[before]
        )
        return transformed[message][position] != baseline

    old = 0
    new = 0
    for name, spec in bridge_specs().items():
        old += sum(
            departure(name, position)
            for position in range(spec.endpoint_full, spec.late_entry_full)
        )
        new += sum(
            departure(name, position)
            for position in range(spec.late_entry_full, spec.late_entry_full + 30)
        )
    return old, new


def screen(
    tables: Sequence[tuple[str, Sequence[int]]],
    streams: Mapping[str, Sequence[int]],
) -> tuple[Candidate, ...]:
    decks = (
        ("identity", tuple(range(ASCII_SIZE))),
        ("reverse", tuple(reversed(range(ASCII_SIZE)))),
    )
    candidates: list[Candidate] = []
    for table_name, parameters in tables:
        for deck_name, deck in decks:
            for family in UPDATE_FAMILIES:
                for direction, parameter_index in (
                    ("label-decode", "label"),
                    ("rank-encode", "rank"),
                    ("label-decode", "rank"),
                    ("rank-encode", "label"),
                ):
                    transformed = _transformed_streams(
                        streams,
                        deck=deck,
                        parameters=parameters,
                        family=family,
                        direction=direction,
                        parameter_index=parameter_index,
                    )
                    if context_scores(transformed)[:2] != (6, 1):
                        continue
                    bridge = observed_metrics(transformed)
                    (
                        changed,
                        relabel_departures,
                        dynamic,
                        static,
                        global_equality,
                        gated_departures,
                        gated_dynamic,
                        gated_static,
                    ) = _degeneracy(
                        streams,
                        transformed,
                        deck=deck,
                        direction=direction,
                    )
                    old_departures, new_departures = _phase_departures(
                        streams,
                        transformed,
                        deck=deck,
                        direction=direction,
                    )
                    candidates.append(
                        Candidate(
                            model=Model(
                                table=table_name,
                                deck=deck_name,
                                family=family,
                                direction=(
                                    f"{direction}/"
                                    f"{parameter_index}-update"
                                ),
                            ),
                            bridge_joint=bridge.joint,
                            bridge_lcp=bridge.triple_lcp,
                            east_complete=bridge.east_complete,
                            east_switch=bridge.east_switch,
                            changed_positions=changed,
                            departures_from_initial_relabel=relabel_departures,
                            dynamic_input_labels=dynamic,
                            static_relabel=static,
                            global_equality_preserved=global_equality,
                            gated_departures_from_initial_relabel=gated_departures,
                            gated_dynamic_input_labels=gated_dynamic,
                            gated_static_relabel=gated_static,
                            old_bridge_departures=old_departures,
                            new_phase_departures=new_departures,
                        )
                    )
    return tuple(candidates)


def permute_context_assignment(
    tables: Sequence[tuple[str, Sequence[int]]],
    permutation: Sequence[int],
) -> tuple[tuple[str, tuple[int, ...]], ...]:
    if sorted(permutation) != list(range(ASCII_SIZE)):
        raise ValueError("context permutation is not a permutation of 0..82")
    return tuple(
        (name, tuple(values[index] for index in permutation))
        for name, values in tables
    )


def specific_model_control(
    model: Model,
    *,
    table_values: Sequence[int],
    streams: Mapping[str, Sequence[int]],
    controls: int,
    seed: int,
) -> tuple[int, int]:
    """Return all-seven and gated bridge hits for one fixed model."""

    rng = random.Random(seed)
    deck = (
        tuple(range(ASCII_SIZE))
        if model.deck == "identity"
        else tuple(reversed(range(ASCII_SIZE)))
    )
    direction, update = model.direction.split("/")
    parameter_index = update.removesuffix("-update")
    all_seven = 0
    bridge_joint = 0
    for _ in range(controls):
        permutation = list(range(ASCII_SIZE))
        rng.shuffle(permutation)
        parameters = tuple(table_values[index] for index in permutation)
        transformed = _transformed_streams(
            streams,
            deck=deck,
            parameters=parameters,
            family=model.family,
            direction=direction,
            parameter_index=parameter_index,
        )
        passed = context_scores(transformed)[:2] == (6, 1)
        all_seven += passed
        bridge_joint += passed and observed_metrics(transformed).joint
    return all_seven, bridge_joint


def run(
    *,
    controls: int,
    seed: int,
    specific_controls: int = 0,
) -> tuple[str, ...]:
    if controls < 1:
        raise ValueError("controls must be positive")
    lines_by_id = dict(load_wall_message_lines(WALL_TEXT))
    tables = wall_parameter_tables(lines_by_id)
    streams = body_streams()
    observed = screen(tables, streams)
    rng = random.Random(seed)
    survivor_histogram: Counter[int] = Counter()
    bridge_histogram: Counter[int] = Counter()
    any_survivor = 0
    any_bridge = 0
    survivor_total = 0
    bridge_total = 0
    static_total = 0
    global_equality_total = 0
    gated_static_total = 0
    maximum_survivors = 0
    maximum_bridge = 0
    model_survivor_hits: Counter[Model] = Counter()
    model_bridge_hits: Counter[Model] = Counter()
    examples: list[tuple[int, int, tuple[Model, ...]]] = []
    for control_index in range(controls):
        permutation = list(range(ASCII_SIZE))
        rng.shuffle(permutation)
        candidates = screen(
            permute_context_assignment(tables, permutation),
            streams,
        )
        bridges = tuple(candidate for candidate in candidates if candidate.bridge_joint)
        survivor_histogram[len(candidates)] += 1
        bridge_histogram[len(bridges)] += 1
        any_survivor += bool(candidates)
        any_bridge += bool(bridges)
        survivor_total += len(candidates)
        bridge_total += len(bridges)
        static_total += sum(candidate.static_relabel for candidate in candidates)
        global_equality_total += sum(
            candidate.global_equality_preserved for candidate in candidates
        )
        gated_static_total += sum(
            candidate.gated_static_relabel for candidate in candidates
        )
        model_survivor_hits.update(candidate.model for candidate in candidates)
        model_bridge_hits.update(candidate.model for candidate in bridges)
        maximum_survivors = max(maximum_survivors, len(candidates))
        maximum_bridge = max(maximum_bridge, len(bridges))
        if bridges and len(examples) < 5:
            examples.append(
                (
                    control_index,
                    len(candidates),
                    tuple(candidate.model for candidate in bridges),
                )
            )

    observed_bridge = tuple(
        candidate for candidate in observed if candidate.bridge_joint
    )
    observed_static = sum(candidate.static_relabel for candidate in observed)
    observed_global = sum(
        candidate.global_equality_preserved for candidate in observed
    )
    observed_gated_static = sum(
        candidate.gated_static_relabel for candidate in observed
    )
    count_tail = sum(
        frequency
        for count, frequency in survivor_histogram.items()
        if count >= len(observed)
    )
    bridge_tail = sum(
        frequency
        for count, frequency in bridge_histogram.items()
        if count >= len(observed_bridge)
    )
    out = [
        f"controls={controls}",
        f"seed={seed:#x}",
        "models=480",
        "null=one common random permutation of 83 Wall context rows",
        f"observed_all_seven={len(observed)}",
        f"observed_bridge_joint={len(observed_bridge)}",
        f"observed_static_relabels={observed_static}",
        f"observed_global_equality_preservers={observed_global}",
        f"observed_gated_static_relabels={observed_gated_static}",
        f"control_any_all_seven={any_survivor}/{controls}",
        f"control_any_bridge_joint={any_bridge}/{controls}",
        f"control_count_at_least_observed={count_tail}/{controls}",
        f"control_bridge_count_at_least_observed={bridge_tail}/{controls}",
        f"control_total_all_seven={survivor_total}",
        f"control_total_bridge_joint={bridge_total}",
        f"control_static_relabels={static_total}",
        f"control_global_equality_preservers={global_equality_total}",
        f"control_gated_static_relabels={gated_static_total}",
        f"control_max_all_seven={maximum_survivors}",
        f"control_max_bridge_joint={maximum_bridge}",
        f"all_seven_histogram={dict(sorted(survivor_histogram.items()))}",
        f"bridge_joint_histogram={dict(sorted(bridge_histogram.items()))}",
        "--- observed all-seven candidates ---",
    ]
    out.extend(
        f"{candidate} control_all7={model_survivor_hits[candidate.model]}/{controls} "
        f"control_bridge={model_bridge_hits[candidate.model]}/{controls}"
        for candidate in observed
    )
    out.append("--- control bridge examples ---")
    out.extend(str(example) for example in examples)
    if specific_controls:
        table_lookup = dict(tables)
        specific_models = (
            Model(
                "previous-length/zero-based",
                "reverse",
                "reverse-distance-prefix",
                "label-decode/rank-update",
            ),
            Model(
                "following-length/raw",
                "identity",
                "swap-top-distance",
                "label-decode/label-update",
            ),
        )
        out.append("--- high-activity model controls ---")
        for index, model in enumerate(specific_models):
            all_seven_hits, bridge_hits = specific_model_control(
                model,
                table_values=table_lookup[model.table],
                streams=streams,
                controls=specific_controls,
                seed=seed ^ 0x5EEC1F1C ^ index,
            )
            out.append(
                f"{model} controls={specific_controls} "
                f"all7={all_seven_hits} bridge_joint={bridge_hits}"
            )
    return tuple(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=500)
    parser.add_argument("--specific-controls", type=int, default=0)
    parser.add_argument("--seed", type=lambda text: int(text, 0), default=0x83A11)
    args = parser.parse_args()
    print(
        "\n".join(
            run(
                controls=args.controls,
                seed=args.seed,
                specific_controls=args.specific_controls,
            )
        )
    )


if __name__ == "__main__":
    main()
