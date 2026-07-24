#!/usr/bin/env python3
"""Run the frozen raw-eye selector-demultiplexing audit."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import P_MESSAGES, Q_MESSAGES
from eye_mystery.fourteenth_selector import (
    EyeSelectorSpec,
    audit_selector_demultiplexing,
    interleave_selector_lanes,
    select_selector_candidate,
)
from eye_mystery.practice_cipher4_routes import PatternModel


DEFAULT_CORPUS = Path(
    "/private/tmp/noita-eye-puzzle-scratchpad/"
    "research/data/lang/english-corpus-large.txt"
)


def normalize_english(text: str) -> tuple[int, ...]:
    values = []
    in_space = True
    for character in text.upper():
        if "A" <= character <= "Z":
            values.append(ord(character) - ord("A"))
            in_space = False
        elif not in_space:
            values.append(26)
            in_space = True
    return tuple(values)


def eye_bodies() -> dict[str, tuple[int, ...]]:
    streams = {}
    for name in MESSAGE_ORDER:
        body = trigram_values(MESSAGES[name])[1:]
        trim = 25 if name in P_MESSAGES else 6
        streams[name] = body[trim:]
    return streams


def planted_streams(
    source: tuple[int, ...],
    lengths: dict[str, int],
    seed: int,
) -> dict[str, tuple[int, ...]]:
    """Interleave five source chunks with the third eye as explicit lane tag."""

    rng = random.Random(seed)
    # Keep the 25 most frequent external symbols and remap them injectively.
    counts = Counter(source)
    alphabet = tuple(
        value
        for value, _ in sorted(
            counts.items(), key=lambda item: (-item[1], item[0])
        )[:25]
    )
    mapping = {value: index for index, value in enumerate(alphabet)}
    filtered = tuple(mapping[value] for value in source if value in mapping)
    cursor = 0
    output = {}
    for name in MESSAGE_ORDER:
        length = lengths[name]
        selectors = tuple(rng.randrange(5) for _ in range(length))
        lane_lengths = tuple(selectors.count(lane) for lane in range(5))
        segment = filtered[cursor : cursor + length]
        cursor += length + 17
        lanes = []
        lane_cursor = 0
        for lane_length in lane_lengths:
            lanes.append(segment[lane_cursor : lane_cursor + lane_length])
            lane_cursor += lane_length
        output[name] = interleave_selector_lanes(
            lanes,
            selectors,
            selector_index=2,
        )
    return output


def describe(label: str, candidate) -> None:
    print(label)
    print(f"  selected={candidate.spec.name}")
    print(f"  train={candidate.train_improvement:+.9f}")
    print(f"  heldout={candidate.heldout_improvement:+.9f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--order", type=int, default=14)
    parser.add_argument("--controls", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0x45594553454C4543)
    parser.add_argument(
        "--positive-only",
        action="store_true",
        help="run only the planted recovery check",
    )
    args = parser.parse_args()

    source = normalize_english(args.corpus.read_text(errors="ignore"))
    model = PatternModel.train(source, order=args.order)
    bodies = eye_bodies()
    planted = planted_streams(
        source,
        {name: len(stream) for name, stream in bodies.items()},
        args.seed ^ 0x504C414E54,
    )
    planted_candidate = select_selector_candidate(
        planted,
        model,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
    )
    describe("PLANTED", planted_candidate)
    target = EyeSelectorSpec(
        2, "concatenate", tuple(range(5)), 0
    )
    print(f"  target={target.name}")
    print(f"  exact_recovery={planted_candidate.spec == target}")
    if args.positive_only:
        return

    audit = audit_selector_demultiplexing(
        bodies,
        model,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
        controls=args.controls,
        seed=args.seed,
    )
    describe("OBSERVED", audit.selected)
    print(
        f"  controls_run={audit.controls_run}; "
        f"exceedances={audit.exceedances}; "
        f"stopped={audit.stopped_after_rejection}"
    )
    print(
        f"  null={audit.null_minimum:+.9f}..{audit.null_maximum:+.9f}; "
        f"mean={audit.null_mean:+.9f}; "
        f"upper={audit.corrected_upper_tail:.9f}"
    )


if __name__ == "__main__":
    main()
