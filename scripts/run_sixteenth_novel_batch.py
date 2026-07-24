#!/usr/bin/env python3
"""Run the frozen A/C/D/E probes in the sixteenth wide horizon."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from eye_mystery.corpus import (
    MESSAGE_ORDER,
    MESSAGES,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)
from eye_mystery.factoradic_headers import P_MESSAGES, Q_MESSAGES
from eye_mystery.fifteenth_novel import normalized_ascii
from eye_mystery.hidden_geometry import context_sequences
from eye_mystery.practice_cipher4_routes import PatternModel
from eye_mystery.seventh_wide import renderer_body_tape
from eye_mystery.sixteenth_novel import (
    PROJECTIVE_POINTS,
    DyckSpec,
    Field25Spec,
    RowCodeSpec,
    accepted_projective_multiplicities,
    apply_projective_matrix,
    audit_dyck_syntax,
    audit_ray_projection,
    audit_rotor_router,
    audit_row_codes,
    base5_digits,
    base5_rank,
    evaluate_polynomial_f25,
    field25_specs,
    projective_context_audit,
    projective_point_scalar,
)


DEFAULT_CORPUS = Path(
    "/private/tmp/noita-eye-puzzle-scratchpad/"
    "research/data/lang/english-corpus-large.txt"
)
DYCK_TARGET = DyckSpec("header", "aligned")
ROW_TARGET = RowCodeSpec(Field25Spec(0, 2), (0, 2), False, 3)


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
    projected_bodies = {}
    for name in MESSAGE_ORDER:
        body = streams[name][1:]
        trim = 24 if name in P_MESSAGES else (
            5 if name in ("west2", "east3", "west3") else 20
        )
        projected_bodies[name] = body[trim:]
    raw_bodies = {name: MESSAGES[name][3:] for name in MESSAGE_ORDER}
    return streams, headers, tapes, projected_bodies, raw_bodies


def accepted_representatives() -> dict[int, tuple[int, ...]]:
    result: dict[int, list[int]] = {}
    for value in range(1, 83):
        point, _ = projective_point_scalar(value)
        result.setdefault(point, []).append(value)
    return {point: tuple(values) for point, values in result.items()}


def planted_ray_streams(
    source: tuple[int, ...],
    lengths: dict[str, int],
    *,
    seed: int,
) -> dict[str, tuple[int, ...]]:
    representatives = accepted_representatives()
    selected_points = tuple(sorted(representatives))[:27]
    generator = random.Random(seed)
    cursor = 0
    output = {}
    for name in MESSAGE_ORDER:
        length = lengths[name]
        segment = source[cursor : cursor + length]
        cursor += length + 29
        output[name] = tuple(
            generator.choice(representatives[selected_points[symbol]])
            for symbol in segment
        )
    return output


def planted_projective_contexts():
    matrix = (
        (1, 1, 0),
        (0, 1, 1),
        (1, 0, 1),
    )
    source = tuple(base5_rank(point) for point in PROJECTIVE_POINTS)
    target = tuple(apply_projective_matrix(value, matrix) for value in source)
    return (("projective-plant", source, target),)


def dyck_order(header: int, spec: DyckSpec) -> tuple[int, ...]:
    from eye_mystery.factoradic_headers import inverse, lexicographic_unrank

    order = lexicographic_unrank(header)
    return order if spec.route == "header" else inverse(order)


def planted_dyck_tape(
    header: int,
    length: int,
    *,
    seed: int,
) -> tuple[int, ...]:
    generator = random.Random(seed)
    order = dyck_order(header, DYCK_TARGET)
    opens = order[:3]
    closes = order[3:]
    stack: list[int] = []
    output = []
    for index in range(length):
        remaining = length - index
        choose_close = bool(stack) and (
            generator.random() < 0.48 or remaining <= len(stack)
        )
        if choose_close:
            bracket_type = stack.pop()
            output.append(closes[bracket_type])
        else:
            bracket_type = generator.randrange(3)
            stack.append(bracket_type)
            output.append(opens[bracket_type])
    return tuple(output)


def planted_dyck_audit(headers: dict[str, int], lengths: dict[str, int]):
    for attempt in range(100):
        tapes = {
            name: planted_dyck_tape(
                headers[name],
                lengths[name],
                seed=0xD1CC000 + 97 * attempt + index,
            )
            for index, name in enumerate(MESSAGE_ORDER)
        }
        selected, scores = audit_dyck_syntax(
            tapes,
            headers,
            train_names=P_MESSAGES,
            heldout_names=Q_MESSAGES,
        )
        if selected.spec == DYCK_TARGET and selected.exact:
            return selected, scores
    raise AssertionError("could not construct a discriminating Dyck plant")


ROTOR_CYCLES = (
    (0, 1, 2, 3, 4),
    (0, 2, 4, 1, 3),
    (0, 3, 1, 4, 2),
    (0, 4, 3, 2, 1),
    (0, 1, 3, 2, 4),
)


def planted_rotor_stream(
    length: int,
    *,
    seed: int,
) -> tuple[int, ...]:
    generator = random.Random(seed)
    phases = [generator.randrange(5) for _ in range(5)]
    current = generator.randrange(5)
    output = [current]
    while len(output) < length:
        following = ROTOR_CYCLES[current][phases[current]]
        phases[current] = (phases[current] + 1) % 5
        output.append(following)
        current = following
    return tuple(output)


def planted_rotor_streams(lengths: dict[str, int]):
    return {
        name: planted_rotor_stream(
            lengths[name],
            seed=0xA070000 + index,
        )
        for index, name in enumerate(MESSAGE_ORDER)
    }


def pack_row_symbol(
    field_value: tuple[int, int],
    control: int,
    eye_pair: tuple[int, int],
) -> int:
    digits = [0, 0, 0]
    digits[eye_pair[0]] = field_value[0]
    digits[eye_pair[1]] = field_value[1]
    remaining = next(index for index in range(3) if index not in eye_pair)
    digits[remaining] = control
    return base5_rank(digits)


def planted_row(
    coefficients: tuple[tuple[int, int], ...],
    *,
    seed: int,
) -> tuple[int, ...]:
    from eye_mystery.sixteenth_novel import F25_ELEMENTS

    generator = random.Random(seed)
    outputs = tuple(
        evaluate_polynomial_f25(coefficients, value, ROW_TARGET.field)
        for value in F25_ELEMENTS
    ) + (coefficients[-1],)
    return tuple(
        pack_row_symbol(
            value,
            generator.randrange(5),
            ROW_TARGET.eye_pair,
        )
        for value in outputs
    )


def planted_row_streams(seed: int):
    generator = random.Random(seed)
    streams = {}
    for name in MESSAGE_ORDER:
        values = []
        for row_index, length in enumerate(ROW_PAIR_TRIGRAM_LENGTHS[name]):
            if length == 26:
                coefficients = tuple(
                    (generator.randrange(5), generator.randrange(5))
                    for _ in range(ROW_TARGET.degree)
                )
                leading = (0, 0)
                while leading == (0, 0):
                    leading = generator.randrange(5), generator.randrange(5)
                values.extend(
                    planted_row(
                        (*coefficients, leading),
                        seed=seed ^ (len(values) << 8) ^ row_index,
                    )
                )
            else:
                values.extend(generator.randrange(125) for _ in range(length))
        streams[name] = tuple(values)
    return streams


def projective_positive_control(
    pattern_source: tuple[int, ...],
    bodies: dict[str, tuple[int, ...]],
    *,
    plant_controls: int,
    seed: int,
) -> bool:
    print("A. PG(2,5) RAY HOMOPHONY")
    multiplicities = accepted_projective_multiplicities()
    print(
        f"  points={len(multiplicities)} "
        f"multiplicities={min(multiplicities)}..{max(multiplicities)} "
        f"sum={sum(multiplicities)}"
    )
    plant_context = projective_context_audit(planted_projective_contexts())[0]
    print(
        f"  context_plant functional={plant_context.functional} "
        f"injective={plant_context.injective} "
        f"incidence={plant_context.collinearity_agreements}/"
        f"{plant_context.triple_comparisons}"
    )
    model = PatternModel.train(pattern_source, order=14)
    lengths = {name: len(bodies[name]) for name in MESSAGE_ORDER}
    plant_streams = planted_ray_streams(
        pattern_source,
        lengths,
        seed=seed ^ 0xA0A0,
    )
    plant = audit_ray_projection(
        plant_streams,
        model,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
        controls=plant_controls,
        seed=seed ^ 0xA0A1,
    )
    print(
        f"  language_plant train_tail={plant.corrected_train_tail:.9f} "
        f"heldout_tail={plant.corrected_heldout_tail:.9f}"
    )
    positive = (
        plant_context.incidence_exact
        and plant.corrected_train_tail < 0.01
        and plant.corrected_heldout_tail < 0.01
    )
    return positive


def describe_projective_real(
    pattern_source: tuple[int, ...],
    bodies: dict[str, tuple[int, ...]],
    *,
    controls: int,
    seed: int,
) -> None:
    print("A. PG(2,5) EYE RESULT")
    model = PatternModel.train(pattern_source, order=14)
    real_contexts = projective_context_audit(context_sequences())
    for result in real_contexts:
        print(
            f"  {result.context}: function={result.functional} "
            f"injective={result.injective} incidence="
            f"{result.collinearity_agreements}/{result.triple_comparisons} "
            f"conflict={result.projective_conflict or result.collinearity_conflict}"
        )
    real = audit_ray_projection(
        bodies,
        model,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
        controls=controls,
        seed=seed ^ 0xA0A2,
    )
    print(
        f"  eye_language train={real.train_score:+.9f} "
        f"tail={real.corrected_train_tail:.9f}; "
        f"heldout={real.heldout_score:+.9f} "
        f"tail={real.corrected_heldout_tail:.9f}"
    )


def dyck_positive_control(
    headers: dict[str, int],
    tapes: dict[str, tuple[int, ...]],
) -> bool:
    print("D. HEADER-TYPED DYCK SYNTAX")
    plant, _ = planted_dyck_audit(
        headers,
        {name: len(tapes[name]) for name in MESSAGE_ORDER},
    )
    print(
        f"  plant selected={plant.spec.name} exact={plant.exact} "
        f"P={plant.training_prefix}/{plant.training_symbols} "
        f"Q={plant.heldout_prefix}/{plant.heldout_symbols}"
    )
    return plant.spec == DYCK_TARGET and plant.exact


def describe_dyck_real(
    headers: dict[str, int],
    tapes: dict[str, tuple[int, ...]],
) -> None:
    print("D. HEADER-TYPED DYCK EYE RESULT")
    selected, scores = audit_dyck_syntax(
        tapes,
        headers,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
    )
    print(
        f"  eye selected={selected.spec.name} "
        f"P={selected.training_prefix}/{selected.training_symbols} "
        f"valid_panels={selected.training_valid_panels}/3 "
        f"Q={selected.heldout_prefix}/{selected.heldout_symbols} "
        f"valid_panels={selected.heldout_valid_panels}/6"
    )
    print(f"  first_P={selected.first_training_contradiction}")
    print(f"  first_Q={selected.first_heldout_contradiction}")
    for score in scores:
        print(
            f"    {score.spec.name}: "
            f"{score.training_prefix}/{score.training_symbols} -> "
            f"{score.heldout_prefix}/{score.heldout_symbols}"
        )


def rotor_positive_control(raw_bodies: dict[str, tuple[int, ...]]) -> bool:
    print("E. FIVE-STATE ROTOR ROUTER")
    plant_streams = planted_rotor_streams(
        {name: len(raw_bodies[name]) for name in MESSAGE_ORDER}
    )
    plant = audit_rotor_router(
        plant_streams,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
    )
    print(
        f"  plant exact={plant.exact} cycles={plant.training.cycles}"
    )
    return plant.exact


def describe_rotor_real(raw_bodies: dict[str, tuple[int, ...]]) -> None:
    print("E. FIVE-STATE ROTOR EYE RESULT")
    real = audit_rotor_router(
        raw_bodies,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
    )
    print(
        f"  eye training_exact={real.training.exact} "
        f"observations={real.training.observations} "
        f"conflict={real.training.contradiction}"
    )
    if real.heldout is not None:
        print(
            f"  eye heldout_exact={real.heldout.exact} "
            f"observations={real.heldout.observations} "
            f"conflict={real.heldout.contradiction}"
        )


def row_positive_control(
    streams: dict[str, tuple[int, ...]],
    *,
    seed: int,
) -> bool:
    print("C. P1(F25) EXTENDED ROW CODE")
    print(
        f"  irreducible_fields={len(field25_specs())}; "
        f"target={ROW_TARGET.name}"
    )
    plant = audit_row_codes(
        planted_row_streams(seed ^ 0xC0DEC0DE),
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
    )
    print(
        f"  plant selected={plant.selected.name} "
        f"P={plant.training.exact_rows}/{plant.training.rows} "
        f"Q={plant.heldout.exact_rows}/{plant.heldout.rows} "
        f"exact_train_specs={len(plant.exact_training_specs)}"
    )
    positive = plant.selected == ROW_TARGET and plant.exact
    return positive


def describe_row_codes_real(
    streams: dict[str, tuple[int, ...]],
) -> None:
    print("C. P1(F25) EYE RESULT")
    real = audit_row_codes(
        streams,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
    )
    print(
        f"  eye selected={real.selected.name} "
        f"P={real.training.exact_rows}/{real.training.rows} "
        f"Q={real.heldout.exact_rows}/{real.heldout.rows} "
        f"exact_train_specs={len(real.exact_training_specs)} "
        f"exact={real.exact}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--controls", type=int, default=2000)
    parser.add_argument("--plant-controls", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0x5165454E4345)
    parser.add_argument("--positive-only", action="store_true")
    args = parser.parse_args()

    ascii_source = normalized_ascii(args.corpus.read_text(errors="ignore"))
    pattern_source = pattern_values(ascii_source)
    streams, headers, tapes, bodies, raw_bodies = eye_data()

    projective_positive = projective_positive_control(
        pattern_source,
        bodies,
        plant_controls=args.plant_controls,
        seed=args.seed,
    )
    dyck_positive = dyck_positive_control(headers, tapes)
    rotor_positive = rotor_positive_control(raw_bodies)
    row_positive = row_positive_control(streams, seed=args.seed)
    positive = (
        projective_positive
        and dyck_positive
        and rotor_positive
        and row_positive
    )
    print(f"POSITIVE_CONTROLS_PASS={positive}")
    if args.positive_only or not positive:
        return

    describe_projective_real(
        pattern_source,
        bodies,
        controls=args.controls,
        seed=args.seed,
    )
    describe_dyck_real(headers, tapes)
    describe_rotor_real(raw_bodies)
    describe_row_codes_real(streams)


if __name__ == "__main__":
    main()
