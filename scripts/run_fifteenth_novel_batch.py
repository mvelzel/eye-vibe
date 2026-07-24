#!/usr/bin/env python3
"""Run the four frozen probes in the fifteenth wide novelty batch."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import P_MESSAGES, Q_MESSAGES
from eye_mystery.fifteenth_novel import (
    ByteNgramModel,
    GraySpec,
    PackingSpec,
    PrefixCodeSpec,
    audit_gray_geometry,
    audit_multiset_projection,
    audit_prefix_code,
    audit_tree_isometry,
    bytes_to_bits,
    gray_position,
    gray_score,
    gray_specs,
    multiset_order,
    normalized_ascii,
    packing_specs,
    prefix_bits,
    select_prefix_code,
    symbols_from_plain_bits,
)
from eye_mystery.hidden_geometry import (
    ChordConstraint,
    FIRST_FAMILY_NAMES,
    LAST_FAMILY_NAMES,
    context_sequences,
)
from eye_mystery.practice_cipher4_routes import PatternModel
from eye_mystery.seventh_wide import renderer_body_tape


DEFAULT_CORPUS = Path(
    "/private/tmp/noita-eye-puzzle-scratchpad/"
    "research/data/lang/english-corpus-large.txt"
)
PREFIX_TARGET = PrefixCodeSpec(17, "header")
PACKING_TARGET = PackingSpec(8, 0, False)
TREE_TARGET = (2, 0, 1)
GRAY_TARGET = GraySpec((2, 0, 1), 0b101, "circular")


def pattern_values(data: bytes) -> tuple[int, ...]:
    return tuple(
        byte - ord("A") if ord("A") <= byte <= ord("Z") else 26
        for byte in data
    )


def eye_data():
    streams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    headers = {name: streams[name][0] for name in MESSAGE_ORDER}
    tapes = {
        name: renderer_body_tape(name, streams[name])
        for name in MESSAGE_ORDER
    }
    bodies = {}
    for name in MESSAGE_ORDER:
        body = streams[name][1:]
        trim = 25 if name in P_MESSAGES else 6
        bodies[name] = body[trim:]
    return streams, headers, tapes, bodies


def planted_prefix_tapes(
    source_bits: tuple[int, ...],
    headers: dict[str, int],
    lengths: dict[str, int],
) -> dict[str, tuple[int, ...]]:
    cursor = 0
    output = {}
    for name in MESSAGE_ORDER:
        symbols = symbols_from_plain_bits(
            source_bits[cursor:],
            headers[name],
            PREFIX_TARGET,
            maximum_symbols=lengths[name],
        )
        output[name] = symbols
        consumed = len(prefix_bits(symbols, headers[name], PREFIX_TARGET))
        cursor += consumed + 17 * 8
        cursor = (cursor + 7) // 8 * 8
    return output


def planted_multiset_streams(
    source: tuple[int, ...],
    lengths: dict[str, int],
    *,
    seed: int,
) -> dict[str, tuple[int, ...]]:
    representatives: dict[int, list[int]] = {}
    for value in range(83):
        class_index, _ = multiset_order(value)
        representatives.setdefault(class_index, []).append(value)
    selected_classes = tuple(sorted(representatives))[:27]
    if len(selected_classes) != 27:
        raise AssertionError("accepted cube does not expose 27 plant classes")
    generator = random.Random(seed)
    cursor = 0
    output = {}
    for name in MESSAGE_ORDER:
        length = lengths[name]
        segment = source[cursor : cursor + length]
        cursor += length + 31
        output[name] = tuple(
            generator.choice(representatives[selected_classes[symbol]])
            for symbol in segment
        )
    return output


def wreath_transform(value: int, order: tuple[int, ...]) -> int:
    source = value // 25, value // 5 % 5, value % 5
    target = [0, 0, 0]
    prefix = ()
    for level, component in enumerate(order):
        target[component] = (
            source[component] + 2 * sum(prefix) + level + 1
        ) % 5
        prefix = (*prefix, source[component])
    return 25 * target[0] + 5 * target[1] + target[2]


def planted_tree_contexts(seed: int):
    generator = random.Random(seed)
    names = tuple(f"tree-train-{index}" for index in range(4)) + tuple(
        f"tree-heldout-{index}" for index in range(3)
    )
    contexts = []
    for name in names:
        source = tuple(generator.sample(range(125), 40))
        target = tuple(wreath_transform(value, TREE_TARGET) for value in source)
        contexts.append((name, source, target))
    return (
        tuple(contexts),
        names[:4],
        names[4:],
    )


def gray_constraints(
    spec: GraySpec,
    positions: tuple[int, ...],
    *,
    context: str,
    shift: int,
) -> tuple[ChordConstraint, ...]:
    by_position = {
        gray_position(value, spec): value for value in range(125)
    }
    source = tuple(by_position[position] for position in positions)
    target = tuple(
        by_position[(position + shift) % 125] for position in positions
    )
    return tuple(
        ChordConstraint(
            context,
            1,
            index,
            source[index],
            source[index + 1],
            target[index],
            target[index + 1],
        )
        for index in range(len(source) - 1)
    )


def planted_gray_audit(seed: int):
    generator = random.Random(seed)
    train = []
    heldout = []
    for index in range(4):
        positions = tuple(generator.sample(range(125), 35))
        train.extend(
            gray_constraints(
                GRAY_TARGET,
                positions,
                context=f"gray-train-{index}",
                shift=11 + 7 * index,
            )
        )
    for index in range(3):
        positions = tuple(generator.sample(range(125), 35))
        heldout.extend(
            gray_constraints(
                GRAY_TARGET,
                positions,
                context=f"gray-heldout-{index}",
                shift=43 + 9 * index,
            )
        )
    train_scores = tuple(gray_score(train, spec) for spec in gray_specs())
    selected = min(
        train_scores,
        key=lambda score: (-score.agreements, score.spec),
    )
    exact_train = tuple(score.spec for score in train_scores if score.exact)
    return selected, gray_score(heldout, selected.spec), exact_train


def describe_contradiction(prefix: str, contradiction) -> None:
    if contradiction is None:
        print(f"  {prefix}=none")
        return
    print(f"  {prefix}={contradiction}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--controls", type=int, default=2000)
    parser.add_argument("--plant-controls", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0x4649465445454E)
    parser.add_argument("--positive-only", action="store_true")
    args = parser.parse_args()

    text = args.corpus.read_text(errors="ignore")
    ascii_source = normalized_ascii(text)
    pattern_source = pattern_values(ascii_source)
    byte_model = ByteNgramModel.train(ascii_source, order=4)
    pattern_model = PatternModel.train(pattern_source, order=14)
    _, headers, tapes, bodies = eye_data()

    print("A. HEADER-ORDERED PREFIX CODE")
    planted_tapes = planted_prefix_tapes(
        bytes_to_bits(ascii_source),
        headers,
        {name: len(tapes[name]) for name in MESSAGE_ORDER},
    )
    prefix_plant = select_prefix_code(
        planted_tapes,
        headers,
        byte_model,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
        packings=packing_specs(),
    )
    print(f"  planted_selected={prefix_plant.spec.name}")
    print(f"  planted_packing={prefix_plant.packing.name}")
    print(
        f"  planted_train={prefix_plant.train_score:+.9f}; "
        f"heldout={prefix_plant.heldout_score:+.9f}"
    )
    prefix_plant_exact = (
        prefix_plant.spec == PREFIX_TARGET
        and prefix_plant.packing == PACKING_TARGET
    )
    print(
        f"  planted_target={PREFIX_TARGET.name}/{PACKING_TARGET.name}; "
        f"exact_recovery={prefix_plant_exact}"
    )

    print("B. MULTISET/ORDER FACTORIZATION")
    planted_multisets = planted_multiset_streams(
        pattern_source,
        {name: len(bodies[name]) for name in MESSAGE_ORDER},
        seed=args.seed ^ 0x4D554C5449,
    )
    multiset_plant = audit_multiset_projection(
        planted_multisets,
        pattern_model,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
        controls=args.plant_controls,
        seed=args.seed ^ 0x504C414E54,
    )
    print(
        f"  planted_train={multiset_plant.train_score:+.9f}; "
        f"tail={multiset_plant.corrected_train_tail:.9f}"
    )
    print(
        f"  planted_heldout={multiset_plant.heldout_score:+.9f}; "
        f"tail={multiset_plant.corrected_heldout_tail:.9f}"
    )

    print("C. FIVE-ADIC GLYPH TREE")
    tree_contexts, tree_train_names, tree_heldout_names = (
        planted_tree_contexts(args.seed ^ 0x54524545)
    )
    tree_plant = audit_tree_isometry(
        tree_contexts,
        train_names=tree_train_names,
        heldout_names=tree_heldout_names,
    )
    print(
        f"  planted_selected={tree_plant.selected_order}; "
        f"target={TREE_TARGET}; "
        f"exact_recovery={tree_plant.selected_order == TREE_TARGET}"
    )
    print(
        f"  planted_train={tree_plant.train.agreements}/"
        f"{tree_plant.train.comparisons}; "
        f"heldout={tree_plant.heldout.agreements}/"
        f"{tree_plant.heldout.comparisons}"
    )

    print("D. REFLECTED BASE-FIVE GRAY GEOMETRY")
    gray_plant_train, gray_plant_heldout, gray_plant_exact = (
        planted_gray_audit(args.seed ^ 0x47524159)
    )
    print(
        f"  planted_selected={gray_plant_train.spec.name}; "
        f"target={GRAY_TARGET.name}"
    )
    print(
        f"  planted_train={gray_plant_train.agreements}/"
        f"{gray_plant_train.comparisons}; "
        f"heldout={gray_plant_heldout.agreements}/"
        f"{gray_plant_heldout.comparisons}; "
        f"exact_train_specs={len(gray_plant_exact)}"
    )
    positive = (
        prefix_plant_exact
        and multiset_plant.corrected_train_tail < 0.01
        and multiset_plant.corrected_heldout_tail < 0.01
        and tree_plant.selected_order == TREE_TARGET
        and tree_plant.train.exact
        and tree_plant.heldout.exact
        and gray_plant_train.exact
        and gray_plant_heldout.exact
    )
    print(f"POSITIVE_CONTROLS_PASS={positive}")
    if args.positive_only or not positive:
        return

    print("A. OBSERVED PREFIX CODE")
    prefix_audit = audit_prefix_code(
        tapes,
        headers,
        byte_model,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
        packing=PACKING_TARGET,
    )
    print(
        f"  selected={prefix_audit.selected.spec.name}/"
        f"{prefix_audit.selected.packing.name}"
    )
    print(
        f"  train={prefix_audit.selected.train_score:+.9f}; "
        f"heldout={prefix_audit.selected.heldout_score:+.9f}"
    )
    print(
        f"  exact_tail={prefix_audit.exact_exceedances}/"
        f"{prefix_audit.exact_controls}="
        f"{prefix_audit.exact_upper_tail:.9f}"
    )
    print(
        f"  null={prefix_audit.null_minimum:+.9f}.."
        f"{prefix_audit.null_maximum:+.9f}; "
        f"mean={prefix_audit.null_mean:+.9f}"
    )

    print("B. OBSERVED MULTISET/ORDER")
    multiset_audit = audit_multiset_projection(
        bodies,
        pattern_model,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
        controls=args.controls,
        seed=args.seed,
    )
    print(
        f"  train={multiset_audit.train_score:+.9f}; "
        f"tail={multiset_audit.corrected_train_tail:.9f} "
        f"({multiset_audit.train_exceedances}/"
        f"{multiset_audit.controls})"
    )
    print(
        f"  heldout={multiset_audit.heldout_score:+.9f}; "
        f"tail={multiset_audit.corrected_heldout_tail:.9f} "
        f"({multiset_audit.heldout_exceedances}/"
        f"{multiset_audit.controls})"
    )
    print(
        f"  order={multiset_audit.order_score}; "
        f"lower_tail={multiset_audit.corrected_order_tail:.9f}"
    )

    print("C. OBSERVED FIVE-ADIC TREE")
    tree_audit = audit_tree_isometry(
        context_sequences(),
        train_names=tuple(sorted(FIRST_FAMILY_NAMES)),
        heldout_names=tuple(sorted(LAST_FAMILY_NAMES)),
    )
    print(f"  selected_order={tree_audit.selected_order}")
    print(
        f"  train={tree_audit.train.agreements}/"
        f"{tree_audit.train.comparisons}; "
        f"exact={tree_audit.train.exact}"
    )
    print(
        f"  heldout={tree_audit.heldout.agreements}/"
        f"{tree_audit.heldout.comparisons}; "
        f"exact={tree_audit.heldout.exact}"
    )
    describe_contradiction(
        "train_contradiction",
        tree_audit.train.contradiction,
    )
    describe_contradiction(
        "heldout_contradiction",
        tree_audit.heldout.contradiction,
    )

    print("D. OBSERVED GRAY GEOMETRY")
    gray_audit = audit_gray_geometry(
        train_names=tuple(sorted(FIRST_FAMILY_NAMES)),
        heldout_names=tuple(sorted(LAST_FAMILY_NAMES)),
    )
    print(f"  selected={gray_audit.selected.name}")
    print(
        f"  train={gray_audit.train.agreements}/"
        f"{gray_audit.train.comparisons}; "
        f"exact={gray_audit.train.exact}"
    )
    print(
        f"  heldout={gray_audit.heldout.agreements}/"
        f"{gray_audit.heldout.comparisons}; "
        f"exact={gray_audit.heldout.exact}"
    )
    describe_contradiction(
        "train_contradiction",
        gray_audit.train.contradiction,
    )
    describe_contradiction(
        "heldout_contradiction",
        gray_audit.heldout.contradiction,
    )


if __name__ == "__main__":
    main()
