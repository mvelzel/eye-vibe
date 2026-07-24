"""Transfer Cessation's row-terminal sampler to the Earthquake wheel."""

from __future__ import annotations

import itertools
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.corpus import (
    MESSAGE_ORDER,
    MESSAGES,
    ROW_PAIR_TRIGRAM_LENGTHS,
    trigram_values,
)
from eye_mystery.earthquake_mask import MASK
from eye_mystery.ninth_causal import CONTEXT_SPECS
from eye_mystery.visual_rows import interleave_visual_rows, visual_rows


NONLITERAL_CONTEXTS = CONTEXT_SPECS[6:]
TRAIN_CONTEXTS = NONLITERAL_CONTEXTS[:4]
HELDOUT_CONTEXTS = NONLITERAL_CONTEXTS[4:]


@dataclass(frozen=True)
class ContextAgreement:
    """Agreement on context positions whose original labels differ."""

    agreements: int
    changed_positions: int
    exact_contexts: int
    contexts: int


@dataclass(frozen=True)
class OrientationResult:
    """Training-selected wheel direction and its train/held-out scores."""

    orientation: str
    training: ContextAgreement
    heldout: ContextAgreement


@dataclass(frozen=True)
class CessationWheelAudit:
    """Exact fixed-composition audit of the authored Earthquake tape."""

    real: OrientationResult
    uniform_endpoint: OrientationResult
    controls: int
    control_hits: int
    tail: float
    heldout_distribution: tuple[tuple[int, int], ...]

    @property
    def passes(self) -> bool:
        return self.tail < 0.01


def sample_visual_row(
    row: Sequence[int],
    tape: Sequence[int],
    *,
    terminal_aware: bool = True,
) -> tuple[int, ...]:
    """Sample one visual row with natural direction distances ``1..5``.

    ``pointer`` identifies the next unconsumed tape position. Nonterminal
    symbols sample the last consumed position. Under the transferred
    Cessation rule, the row terminal instead samples the next position after
    consumption.
    """

    if not tape or any(bit not in (0, 1) for bit in tape):
        raise ValueError("tape must be a non-empty binary sequence")
    if any(direction not in range(5) for direction in row):
        raise ValueError("eye directions must lie in 0..4")
    if not row:
        return ()

    pointer = 0
    output = []
    for index, direction in enumerate(row):
        distance = direction + 1
        terminal = index == len(row) - 1
        if terminal and terminal_aware:
            pointer = (pointer + distance) % len(tape)
            output.append(tape[pointer])
        else:
            output.append(tape[(pointer + distance - 1) % len(tape)])
            pointer = (pointer + distance) % len(tape)
    return tuple(output)


def sampled_message_values(
    name: str,
    tape: Sequence[int],
    *,
    terminal_aware: bool = True,
    messages: Mapping[str, Sequence[int]] = MESSAGES,
    row_pair_lengths: Mapping[str, Sequence[int]] = ROW_PAIR_TRIGRAM_LENGTHS,
) -> tuple[int, ...]:
    """Sample a message in visual rows and restore accepted trigram order."""

    rows = visual_rows(messages[name], row_pair_lengths[name])
    sampled_rows = tuple(
        sample_visual_row(row, tape, terminal_aware=terminal_aware)
        for row in rows
    )
    raw_bits = interleave_visual_rows(sampled_rows)
    if len(raw_bits) % 3:
        raise AssertionError("sampled Eye stream lost its trigram boundary")
    return tuple(
        4 * raw_bits[index] + 2 * raw_bits[index + 1] + raw_bits[index + 2]
        for index in range(0, len(raw_bits), 3)
    )


def sampled_streams(
    tape: Sequence[int],
    *,
    terminal_aware: bool = True,
    names: Sequence[str] = MESSAGE_ORDER,
) -> dict[str, tuple[int, ...]]:
    """Sample every requested canonical Eye message."""

    return {
        name: sampled_message_values(
            name,
            tape,
            terminal_aware=terminal_aware,
        )
        for name in names
    }


def changed_label_agreement(
    sampled: Mapping[str, Sequence[int]],
    specs: Sequence[tuple[str, str, int, str, int, int]],
    *,
    original: Mapping[str, Sequence[int]] | None = None,
) -> ContextAgreement:
    """Score sampled equality only where an aligned source label changes."""

    if original is None:
        original = {
            name: trigram_values(MESSAGES[name])
            for name in MESSAGE_ORDER
        }

    agreements = 0
    changed_positions = 0
    exact_contexts = 0
    for _, left_name, left_start, right_name, right_start, length in specs:
        context_agreements = 0
        context_changed = 0
        for offset in range(length):
            left_original = original[left_name][left_start + offset]
            right_original = original[right_name][right_start + offset]
            if left_original == right_original:
                continue
            context_changed += 1
            changed_positions += 1
            equal = (
                sampled[left_name][left_start + offset]
                == sampled[right_name][right_start + offset]
            )
            context_agreements += int(equal)
            agreements += int(equal)
        exact_contexts += int(
            context_changed > 0 and context_agreements == context_changed
        )
    return ContextAgreement(
        agreements,
        changed_positions,
        exact_contexts,
        len(specs),
    )


def select_orientation(
    candidates: Sequence[OrientationResult],
) -> OrientationResult:
    """Select by training agreement, with the frozen forward tie break."""

    if {candidate.orientation for candidate in candidates} != {
        "forward",
        "reverse",
    }:
        raise ValueError("orientation candidates must be forward and reverse")
    return max(
        candidates,
        key=lambda result: (
            result.training.agreements,
            result.orientation == "forward",
        ),
    )


def evaluate_orientation(
    tape: Sequence[int],
    *,
    terminal_aware: bool = True,
) -> OrientationResult:
    """Select forward/reverse on training contexts, then score held out."""

    candidates = []
    for orientation, candidate_tape in (
        ("forward", tuple(tape)),
        ("reverse", tuple(reversed(tape))),
    ):
        sampled = sampled_streams(
            candidate_tape,
            terminal_aware=terminal_aware,
        )
        training = changed_label_agreement(sampled, TRAIN_CONTEXTS)
        heldout = changed_label_agreement(sampled, HELDOUT_CONTEXTS)
        candidates.append(OrientationResult(orientation, training, heldout))
    return select_orientation(candidates)


def fixed_composition_tapes(
    *,
    length: int = len(MASK),
    zeroes: int = MASK.count(0),
) -> tuple[tuple[int, ...], ...]:
    """Enumerate every binary tape with the authored length/composition."""

    if length < 1 or zeroes not in range(length + 1):
        raise ValueError("invalid tape length or zero count")
    tapes = []
    for zero_positions in itertools.combinations(range(length), zeroes):
        tape = [1] * length
        for position in zero_positions:
            tape[position] = 0
        tapes.append(tuple(tape))
    return tuple(tapes)


def run_cessation_wheel_audit(
    tape: Sequence[int] = MASK,
) -> CessationWheelAudit:
    """Run the exact preregistered real-versus-all-tapes audit."""

    real_tape = tuple(tape)
    if len(real_tape) != len(MASK) or real_tape.count(0) != MASK.count(0):
        raise ValueError("real tape must have the registered length/composition")

    real = evaluate_orientation(real_tape, terminal_aware=True)
    uniform_endpoint = evaluate_orientation(real_tape, terminal_aware=False)

    distribution: dict[int, int] = {}
    control_hits = 0
    controls = fixed_composition_tapes()
    for control in controls:
        result = evaluate_orientation(control, terminal_aware=True)
        score = result.heldout.agreements
        distribution[score] = distribution.get(score, 0) + 1
        control_hits += int(score >= real.heldout.agreements)

    return CessationWheelAudit(
        real=real,
        uniform_endpoint=uniform_endpoint,
        controls=len(controls),
        control_hits=control_hits,
        tail=control_hits / len(controls),
        heldout_distribution=tuple(sorted(distribution.items())),
    )
