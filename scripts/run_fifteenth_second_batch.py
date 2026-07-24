#!/usr/bin/env python3
"""Run the frozen E/G/H probes in the fifteenth wide novelty horizon."""

from __future__ import annotations

import random

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import (
    P_MESSAGES,
    Q_EAST_MESSAGES,
    Q_WEST_MESSAGES,
)
from eye_mystery.fifteenth_second import (
    ChecksumRule,
    ReductionSpec,
    audit_checksum_dispatch,
    audit_reduction_events,
    audit_uniform_morphisms,
    checksum_value,
    deduplicated_reduction_specs,
    factor_complexity,
    reduction_event,
    trimmed_eye_words,
)


def fixed_point_prefix(
    seed: int,
    productions: dict[int, tuple[int, ...]],
    length: int,
) -> tuple[int, ...]:
    word = (seed,)
    while len(word) < length:
        word = tuple(value for symbol in word for value in productions[symbol])
    return word[:length]


def planted_morphism_words() -> dict[str, tuple[int, ...]]:
    productions = {0: (0, 1), 1: (1, 0)}
    lengths = (192, 181, 173, 167, 159, 151, 143, 137, 131)
    return {
        name: fixed_point_prefix(index % 2, productions, length)
        for index, (name, length) in enumerate(
            zip(MESSAGE_ORDER, lengths, strict=True)
        )
    }


def planted_checksum_streams(seed: int = 0xE1E1502):
    """Author three checksum types and reject only invalid/ambiguous fixtures."""

    generator = random.Random(seed)
    target_rules = {
        "P": ChecksumRule("sum", 83, -1),
        "Q-west": ChecksumRule("alternating", 101, 1),
        "Q-east": ChecksumRule("fletcher2", 83, 1),
    }
    groups = {
        "P": P_MESSAGES,
        "Q-west": Q_WEST_MESSAGES,
        "Q-east": Q_EAST_MESSAGES,
    }
    for attempt in range(10_000):
        streams = {}
        valid = True
        for group_name, names in groups.items():
            rule = target_rules[group_name]
            for panel_index, name in enumerate(names):
                body = tuple(
                    generator.randrange(83)
                    for _ in range(39 + 7 * panel_index + attempt % 3)
                )
                marker = checksum_value(body, rule)
                if marker is None:
                    valid = False
                    break
                streams[name] = (marker, *body)
            if not valid:
                break
        if valid:
            audit = audit_checksum_dispatch(streams, groups=groups)
            if audit.passed:
                return streams, audit
    raise AssertionError("could not construct an unambiguous checksum plant")


def planted_reduction_family(
    target: ReductionSpec,
    *,
    prefix: str,
    seed: int,
) -> tuple[tuple[str, tuple[int, ...], tuple[int, ...]], ...]:
    """Cover every rival with an equality contradiction to the target."""

    generator = random.Random(seed)
    catalog = deduplicated_reduction_specs()
    remaining = {spec for spec in catalog if spec != target}
    contexts = []
    attempts = 0
    while remaining and attempts < 1_000_000:
        attempts += 1
        source = generator.randrange(83), generator.randrange(83)
        target_pair = generator.randrange(83), generator.randrange(83)
        if reduction_event(*source, target) != reduction_event(*target_pair, target):
            continue
        covered = {
            spec
            for spec in remaining
            if reduction_event(*source, spec)
            != reduction_event(*target_pair, spec)
        }
        if not covered:
            continue
        contexts.append(
            (
                f"{prefix}-{len(contexts)}",
                source,
                target_pair,
            )
        )
        remaining -= covered
    if remaining:
        raise AssertionError(
            f"reduction plant did not distinguish: "
            f"{sorted(spec.name for spec in remaining)}"
        )
    return tuple(contexts)


def planted_reduction_audit():
    target = ReductionSpec("sum", (2, 0, 1))
    training = planted_reduction_family(
        target,
        prefix="plant-train",
        seed=0xE1E1503,
    )
    heldout = planted_reduction_family(
        target,
        prefix="plant-heldout",
        seed=0xE1E1504,
    )
    return audit_reduction_events(
        contexts=(*training, *heldout),
        train_names=frozenset(name for name, _, _ in training),
        heldout_names=frozenset(name for name, _, _ in heldout),
    )


def describe_morphism() -> None:
    plant = audit_uniform_morphisms(planted_morphism_words())
    plant_exact = tuple(audit.length for audit in plant if audit.exact)
    print("E uniform morphism")
    print(f"  plant exact lengths={plant_exact}")
    real = audit_uniform_morphisms(trimmed_eye_words())
    for audit in real:
        training = audit.training
        if training.contradiction is not None:
            print(
                f"  L={audit.length} train contradiction="
                f"{training.contradiction}"
            )
        else:
            assert audit.heldout is not None
            print(
                f"  L={audit.length} train exact "
                f"productions={len(training.productions)} "
                f"heldout exact={audit.heldout.exact} "
                f"predicted={audit.heldout.predicted_observations}"
            )
            if audit.heldout.contradiction is not None:
                print(
                    f"    heldout contradiction="
                    f"{audit.heldout.contradiction}"
                )
    profile = factor_complexity(trimmed_eye_words())
    print(
        "  complexity="
        + ",".join(
            f"{item.length}:{item.factors}/{item.right_special}"
            for item in profile
        )
    )


def describe_checksums() -> None:
    _, plant = planted_checksum_streams()
    print("G checksum dispatch")
    print(
        f"  plant rules={plant.rules} correct={plant.correct_folds}/9 "
        f"pass={plant.passed}"
    )
    for group in plant.classes:
        print(f"    plant {group.name} shared={group.shared_rules}")
    streams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    real = audit_checksum_dispatch(streams)
    print(
        f"  eye rules={real.rules} correct={real.correct_folds}/9 "
        f"pass={real.passed}"
    )
    for group in real.classes:
        print(
            f"    {group.name} pass={group.passed} "
            f"shared={group.shared_rules}"
        )
        for fold in group.folds:
            print(
                f"      hold {fold.heldout}: {fold.status}; "
                f"candidates={len(fold.compatible_rules)} "
                f"prediction={fold.prediction} actual={fold.actual}"
            )


def describe_reductions() -> None:
    plant = planted_reduction_audit()
    print("H missing-state reduction")
    print(
        f"  plant catalog={plant.catalog_size} "
        f"selected={plant.selected.name} "
        f"train={plant.training.agreements}/{plant.training.comparisons} "
        f"heldout={plant.heldout.agreements}/{plant.heldout.comparisons} "
        f"exact={plant.exact}"
    )
    real = audit_reduction_events()
    print(
        f"  eye catalog={real.catalog_size} selected={real.selected.name} "
        f"train={real.training.agreements}/{real.training.comparisons} "
        f"heldout={real.heldout.agreements}/{real.heldout.comparisons} "
        f"exact={real.exact}"
    )
    print(f"  exact training specs={real.exact_training_specs}")
    print(f"  first train contradiction={real.training.contradiction}")
    print(f"  first heldout contradiction={real.heldout.contradiction}")


def main() -> None:
    describe_morphism()
    describe_checksums()
    describe_reductions()


if __name__ == "__main__":
    main()
