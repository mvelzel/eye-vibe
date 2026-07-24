#!/usr/bin/env python3
"""Run the frozen B/H/I probes in the sixteenth wide horizon."""

from __future__ import annotations

import random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import (
    P_MESSAGES,
    Q_MESSAGES,
    compose,
    inverse,
)
from eye_mystery.hidden_geometry import (
    FIRST_FAMILY_NAMES,
    LAST_FAMILY_NAMES,
    context_sequences,
)
from eye_mystery.seventh_wide import renderer_body_tape
from eye_mystery.sixteenth_second import (
    ONE125,
    ZERO125,
    Field125Spec,
    GF125Representation,
    MobiusCoefficients,
    NecklaceSpec,
    OuterSpec,
    apply_mobius,
    apply_permutation,
    audit_gf125_contexts,
    audit_necklaces,
    audit_outer_actions,
    field125_rank,
    field125_specs,
    f125_mul,
    f125_sub,
    gf125_representations,
    least_rotation_index,
    outer_header_action,
    ranked_renderer_word,
)


OUTER_TARGET = OuterSpec(0, "header")
NECKLACE_TARGET = NecklaceSpec("header", False)
GF125_TARGET = GF125Representation(Field125Spec(0, 1, 1), 1)


def eye_data():
    streams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    headers = {name: streams[name][0] for name in MESSAGE_ORDER}
    tapes = {
        name: renderer_body_tape(name, streams[name])
        for name in MESSAGE_ORDER
    }
    masks = {
        name: tuple(value == 5 for value in tapes[name])
        for name in MESSAGE_ORDER
    }
    return streams, headers, tapes, masks


def planted_outer_audit(
    valid_tapes: dict[str, tuple[int, ...]],
    headers: dict[str, int],
    masks: dict[str, tuple[bool, ...]],
):
    encoded = {}
    for name in MESSAGE_ORDER:
        action = outer_header_action(headers[name], OUTER_TARGET)
        encoded[name] = apply_permutation(valid_tapes[name], inverse(action))
    return audit_outer_actions(
        encoded,
        headers,
        masks,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
    )


def rotate(values: tuple[int, ...], offset: int) -> tuple[int, ...]:
    return values[offset:] + values[:offset]


def primitive_random_tape(length: int, generator: random.Random) -> tuple[int, ...]:
    while True:
        tape = tuple(generator.randrange(6) for _ in range(length))
        if len(set(tape)) == 6:
            return tape


def planted_necklace_audit(
    headers: dict[str, int],
    lengths: dict[str, int],
):
    for attempt in range(100):
        generator = random.Random(0x4E45434B + attempt)
        tapes = {}
        for name in MESSAGE_ORDER:
            tape = primitive_random_tape(lengths[name], generator)
            ranked = ranked_renderer_word(
                tape,
                headers[name],
                NECKLACE_TARGET,
            )
            tapes[name] = rotate(tape, least_rotation_index(ranked))
        selected, scores = audit_necklaces(
            tapes,
            headers,
            train_names=P_MESSAGES,
            heldout_names=Q_MESSAGES,
        )
        if selected.spec == NECKLACE_TARGET and selected.exact:
            return selected, scores
    raise AssertionError("could not construct a discriminating necklace plant")


def random_field_value(generator: random.Random):
    return (
        generator.randrange(5),
        generator.randrange(5),
        generator.randrange(5),
    )


def random_mobius_coefficients(
    generator: random.Random,
    representation: GF125Representation,
) -> MobiusCoefficients:
    field = representation.field
    while True:
        coefficients = tuple(random_field_value(generator) for _ in range(4))
        first, second, third, fourth = coefficients
        determinant = f125_sub(
            f125_mul(first, fourth, field),
            f125_mul(second, third, field),
        )
        if determinant != ZERO125:
            return coefficients  # type: ignore[return-value]


def planted_gf125_contexts(seed: int = 0xF1252026):
    generator = random.Random(seed)
    names = tuple(sorted(FIRST_FAMILY_NAMES)) + tuple(
        sorted(LAST_FAMILY_NAMES)
    )
    contexts = []
    for name in names:
        coefficients = random_mobius_coefficients(generator, GF125_TARGET)
        candidates = list(range(125))
        generator.shuffle(candidates)
        source = []
        target = []
        for value in candidates:
            image = apply_mobius(value, GF125_TARGET, coefficients)
            if image is None:
                continue
            source.append(value)
            target.append(image)
            if len(source) == 12:
                break
        if len(source) != 12 or len(set(target)) != 12:
            raise AssertionError("Möbius plant did not produce an injective context")
        contexts.append((name, tuple(source), tuple(target)))
    return tuple(contexts)


def outer_positive(
    tapes: dict[str, tuple[int, ...]],
    headers: dict[str, int],
    masks: dict[str, tuple[bool, ...]],
) -> bool:
    print("B. OUTER-S6 POSITIVE CONTROL")
    audit = planted_outer_audit(tapes, headers, masks)
    selected = audit.selected
    print(
        f"  catalog={audit.catalog_size} target={OUTER_TARGET.name} "
        f"selected={selected.spec.name} "
        f"P={selected.training_mismatches}/{selected.training_symbols} "
        f"Q={selected.heldout_mismatches}/{selected.heldout_symbols} "
        f"exact_P={len(audit.exact_training_specs)}"
    )
    return selected.exact and OUTER_TARGET.name in audit.exact_training_specs


def necklace_positive(
    tapes: dict[str, tuple[int, ...]],
    headers: dict[str, int],
) -> bool:
    print("H. NECKLACE POSITIVE CONTROL")
    selected, _ = planted_necklace_audit(
        headers,
        {name: len(tapes[name]) for name in MESSAGE_ORDER},
    )
    print(
        f"  target={NECKLACE_TARGET.name} selected={selected.spec.name} "
        f"P={selected.training_canonical}/3 "
        f"Q={selected.heldout_canonical}/6 exact={selected.exact}"
    )
    return selected.spec == NECKLACE_TARGET and selected.exact


def gf125_positive() -> bool:
    print("I. GF(125) POSITIVE CONTROL")
    contexts = planted_gf125_contexts()
    audit = audit_gf125_contexts(
        contexts,
        train_names=FIRST_FAMILY_NAMES,
        heldout_names=LAST_FAMILY_NAMES,
    )
    print(
        f"  catalog={audit.catalog_size} target={GF125_TARGET.name} "
        f"selected={audit.selected.name} "
        f"P={audit.training_exact_contexts}/4 "
        f"Q={audit.heldout_exact_contexts}/3 "
        f"exact_P_representations={len(audit.exact_training_representations)}"
    )
    return (
        GF125_TARGET.name in audit.exact_training_representations
        and audit.heldout_exact_contexts == 3
    )


def describe_outer_real(
    tapes: dict[str, tuple[int, ...]],
    headers: dict[str, int],
    masks: dict[str, tuple[bool, ...]],
) -> None:
    print("B. OUTER-S6 EYE RESULT")
    audit = audit_outer_actions(
        tapes,
        headers,
        masks,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
    )
    score = audit.selected
    print(
        f"  selected={score.spec.name} "
        f"P={score.training_mismatches}/{score.training_symbols} "
        f"Q={score.heldout_mismatches}/{score.heldout_symbols} "
        f"exact_P={len(audit.exact_training_specs)} exact={score.exact}"
    )
    print(f"  P_panels={score.training_panel_mismatches}")
    print(f"  Q_panels={score.heldout_panel_mismatches}")


def describe_necklace_real(
    tapes: dict[str, tuple[int, ...]],
    headers: dict[str, int],
) -> None:
    print("H. NECKLACE EYE RESULT")
    selected, scores = audit_necklaces(
        tapes,
        headers,
        train_names=P_MESSAGES,
        heldout_names=Q_MESSAGES,
    )
    print(
        f"  selected={selected.spec.name} "
        f"P={selected.training_canonical}/3 "
        f"Q={selected.heldout_canonical}/6 exact={selected.exact}"
    )
    for score in scores:
        print(
            f"    {score.spec.name}: "
            f"P={score.training_canonical}/3 "
            f"Q={score.heldout_canonical}/6 "
            f"P_primitive={score.training_primitive}/3"
        )
    for panel in (*selected.training, *selected.heldout):
        print(
            f"    {panel.name}: least={panel.least_rotation}/"
            f"{panel.length} period={panel.primitive_period} "
            f"border={panel.border} factors={panel.lyndon_factors}"
        )


def describe_gf125_real() -> None:
    print("I. GF(125) EYE RESULT")
    audit = audit_gf125_contexts(
        context_sequences(),
        train_names=FIRST_FAMILY_NAMES,
        heldout_names=LAST_FAMILY_NAMES,
    )
    print(
        f"  selected={audit.selected.name} "
        f"P_exact={audit.training_exact_contexts}/4 "
        f"Q_exact={audit.heldout_exact_contexts}/3 "
        f"exact_P_representations={len(audit.exact_training_representations)} "
        f"exact={audit.exact}"
    )
    for score in (*audit.training, *audit.heldout):
        print(
            f"    {score.context}: {score.matches}/{score.edges} "
            f"fit={score.fit_indices} "
            f"first={score.first_contradiction}"
        )


def main() -> None:
    _, headers, tapes, masks = eye_data()
    outer_ok = outer_positive(tapes, headers, masks)
    necklace_ok = necklace_positive(tapes, headers)
    gf125_ok = gf125_positive()
    positive = outer_ok and necklace_ok and gf125_ok
    print(f"POSITIVE_CONTROLS_PASS={positive}")
    if not positive:
        return
    describe_outer_real(tapes, headers, masks)
    describe_necklace_real(tapes, headers)
    describe_gf125_real()


if __name__ == "__main__":
    main()
