#!/usr/bin/env python3
"""Screen the frozen Wall-context parameterized reversible deck family."""

from __future__ import annotations

from pathlib import Path

from eye_mystery.noita_wall_messages import load_wall_message_lines
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


def model_rows(
    *,
    crossed_indices: bool = False,
) -> tuple[tuple[int, int, int, int, str, str, str, str], ...]:
    lines_by_id = dict(load_wall_message_lines(WALL_TEXT))
    tables = wall_parameter_tables(lines_by_id)
    decks = (
        ("identity", tuple(range(ASCII_SIZE))),
        ("reverse", tuple(reversed(range(ASCII_SIZE)))),
    )
    bodies = body_streams()
    probe = tuple((index * 17 + 3) % ASCII_SIZE for index in range(83))
    rows = []
    for table_name, parameters in tables:
        for deck_name, deck in decks:
            for family in UPDATE_FAMILIES:
                for parameter_index in ("label", "rank"):
                    planted = encode_ranks(
                        probe,
                        deck,
                        parameters,
                        family=family,
                        parameter_index=parameter_index,
                    )
                    if (
                        decode_labels(
                            planted,
                            deck,
                            parameters,
                            family=family,
                            parameter_index=parameter_index,
                        )
                        != probe
                    ):
                        raise AssertionError(
                            (table_name, deck_name, family, parameter_index)
                        )
                directions = (
                    (
                        "label-decode/rank-update",
                        decode_labels,
                        "rank",
                    ),
                    (
                        "rank-encode/label-update",
                        encode_ranks,
                        "label",
                    ),
                ) if crossed_indices else (
                    (
                        "label-decode/label-update",
                        decode_labels,
                        "label",
                    ),
                    (
                        "rank-encode/rank-update",
                        encode_ranks,
                        "rank",
                    ),
                )
                for direction, transform, parameter_index in directions:
                    transformed = {
                        name: transform(
                            stream,
                            deck,
                            parameters,
                            family=family,
                            parameter_index=parameter_index,
                        )
                        for name, stream in bodies.items()
                    }
                    rows.append(
                        (
                            *context_scores(transformed),
                            table_name,
                            deck_name,
                            family,
                            direction,
                        )
                    )
    rows.sort(
        key=lambda row: (
            -row[0],
            -row[1],
            -row[2],
            -row[3],
            row[4:],
        )
    )
    return tuple(rows)


def run(*, crossed_indices: bool = False) -> tuple[str, ...]:
    rows = model_rows(crossed_indices=crossed_indices)
    out = [
        f"crossed_indices={crossed_indices}",
        "parameter_tables=10",
        "decks=2",
        f"families={len(UPDATE_FAMILIES)}",
        f"models={len(rows)}",
        "train_iso heldout_iso train_literal heldout_literal "
        "table deck family direction",
    ]
    out.extend(
        f"{train:>9} {held:>11} {literal:>13} {held_literal:>15} "
        f"{table:<42} {deck:<8} {family:<28} {direction}"
        for (
            train,
            held,
            literal,
            held_literal,
            table,
            deck,
            family,
            direction,
        ) in rows[:40]
    )
    all_seven = [row for row in rows if row[0:2] == (6, 1)]
    out.append(f"all_seven_isomorphs={len(all_seven)}")
    out.extend(f"all_seven={row}" for row in all_seven)
    return tuple(out)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--crossed-indices", action="store_true")
    arguments = parser.parse_args()
    print("\n".join(run(crossed_indices=arguments.crossed_indices)))
