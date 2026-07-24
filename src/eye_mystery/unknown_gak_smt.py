"""SMT-LIB encoding for ordinary GAK with unknown plaintext.

The encoding is intentionally solver-agnostic text.  The optional runner uses
an installed ``z3`` command-line executable, so the project does not require a
Python solver package.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import re
import shutil
import subprocess
from time import monotonic

from .unknown_gak import UnknownGAKWitness, replay_unknown_gak


@dataclass(frozen=True)
class SymbolicGAKResult:
    """One symbolic feasibility result and an optional exact replay witness."""

    status: str
    witness: UnknownGAKWitness | None
    elapsed_seconds: float
    formula_bytes: int
    solver_output: str


@dataclass(frozen=True)
class SymbolicGAKMessagesWitness:
    """One shared operation set and one plaintext schedule per reset message."""

    operations: tuple[tuple[int, ...], ...]
    plaintexts: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class SymbolicGAKMessagesResult:
    """Symbolic feasibility result for several identity-reset messages."""

    status: str
    witness: SymbolicGAKMessagesWitness | None
    elapsed_seconds: float
    formula_bytes: int
    solver_output: str


def _ite(index: str, values: Sequence[str]) -> str:
    expression = values[-1]
    for position in range(len(values) - 2, -1, -1):
        expression = f"(ite (= {index} {position}) {values[position]} {expression})"
    return expression


def build_unknown_gak_smt2(
    ciphertext: Sequence[int],
    *,
    deck_size: int,
    operation_alphabet_size: int,
    require_top_change: bool = True,
    require_unique_top_sources: bool = True,
    timeout_ms: int = 30_000,
    request_model: bool = True,
) -> str:
    """Build a finite integer SMT encoding of an unknown-plaintext GAK."""

    if deck_size < 2:
        raise ValueError("deck_size must be at least two")
    if operation_alphabet_size < 1:
        raise ValueError("operation_alphabet_size must be positive")
    if (
        require_top_change
        and require_unique_top_sources
        and operation_alphabet_size > deck_size - 1
    ):
        raise ValueError("too many distinct non-top source positions")
    if timeout_ms < 1:
        raise ValueError("timeout_ms must be positive")
    if any(not 0 <= value < deck_size for value in ciphertext):
        raise ValueError("ciphertext card is outside the deck")

    lines = [
        "(set-logic QF_LIA)",
        "(set-option :produce-models true)",
        f"(set-option :timeout {timeout_ms})",
    ]
    operation_names = []
    for symbol in range(operation_alphabet_size):
        row = []
        for position in range(deck_size):
            name = f"p_{symbol}_{position}"
            row.append(name)
            lines.append(f"(declare-const {name} Int)")
            lines.append(f"(assert (and (<= 0 {name}) (< {name} {deck_size})))")
        lines.append(f"(assert (distinct {' '.join(row)}))")
        if require_top_change:
            lines.append(f"(assert (not (= p_{symbol}_0 0)))")
        operation_names.append(tuple(row))

    if require_unique_top_sources and operation_alphabet_size > 1:
        tops = " ".join(row[0] for row in operation_names)
        lines.append(f"(assert (distinct {tops}))")
        # Plaintext-symbol names are arbitrary. Ordering the top sources removes
        # the k! operation-label symmetry without changing feasibility.
        lines.append(
            "(assert (< "
            + " ".join(row[0] for row in operation_names)
            + "))"
        )

    schedule_names = []
    previous = tuple(str(position) for position in range(deck_size))
    for offset, emitted in enumerate(ciphertext):
        schedule = f"q_{offset}"
        schedule_names.append(schedule)
        lines.append(f"(declare-const {schedule} Int)")
        lines.append(
            f"(assert (and (<= 0 {schedule}) (< {schedule} {operation_alphabet_size})))"
        )
        current = tuple(f"s_{offset}_{position}" for position in range(deck_size))
        for name in current:
            lines.append(f"(declare-const {name} Int)")

        for position, state_name in enumerate(current):
            operation_position = _ite(
                schedule,
                tuple(row[position] for row in operation_names),
            )
            if offset == 0:
                # Selecting from the identity reset deck returns the selected
                # position number itself.
                next_value = operation_position
            else:
                next_value = _ite(operation_position, previous)
            lines.append(f"(assert (= {state_name} {next_value}))")
        lines.append(f"(assert (= {current[0]} {emitted}))")
        previous = current

    lines.append("(check-sat)")
    if request_model:
        requested = [
            name for row in operation_names for name in row
        ] + schedule_names
        lines.append(f"(get-value ({' '.join(requested)}))")
    lines.append("(exit)")
    return "\n".join(lines) + "\n"


def _parse_witness(
    output: str,
    *,
    deck_size: int,
    operation_alphabet_size: int,
    plaintext_length: int,
) -> UnknownGAKWitness | None:
    assignments = {
        name: int(value)
        for name, value in re.findall(r"\((p_\d+_\d+|q_\d+)\s+(-?\d+)\)", output)
    }
    operation_names = tuple(
        tuple(f"p_{symbol}_{position}" for position in range(deck_size))
        for symbol in range(operation_alphabet_size)
    )
    schedule_names = tuple(f"q_{offset}" for offset in range(plaintext_length))
    required = {name for row in operation_names for name in row} | set(
        schedule_names
    )
    if not required <= assignments.keys():
        return None
    return UnknownGAKWitness(
        tuple(
            tuple(assignments[name] for name in row)
            for row in operation_names
        ),
        tuple(assignments[name] for name in schedule_names),
    )


def solve_unknown_gak_with_z3(
    ciphertext: Sequence[int],
    *,
    deck_size: int,
    operation_alphabet_size: int,
    timeout_ms: int = 30_000,
    z3_path: str | None = None,
) -> SymbolicGAKResult:
    """Run the SMT encoding with the Z3 command-line solver."""

    executable = z3_path or shutil.which("z3")
    if executable is None:
        raise RuntimeError("z3 executable is unavailable")
    formula = build_unknown_gak_smt2(
        ciphertext,
        deck_size=deck_size,
        operation_alphabet_size=operation_alphabet_size,
        timeout_ms=timeout_ms,
    )
    started = monotonic()
    try:
        completed = subprocess.run(
            (executable, "-in"),
            input=formula,
            text=True,
            capture_output=True,
            timeout=timeout_ms / 1_000 + 2,
            check=False,
        )
        output = completed.stdout + completed.stderr
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or "") + (error.stderr or "")
        return SymbolicGAKResult(
            "unknown",
            None,
            monotonic() - started,
            len(formula.encode()),
            output,
        )

    first_line = output.lstrip().splitlines()[0] if output.strip() else ""
    status = first_line if first_line in {"sat", "unsat", "unknown"} else "error"
    witness = None
    if status == "sat":
        witness = _parse_witness(
            output,
            deck_size=deck_size,
            operation_alphabet_size=operation_alphabet_size,
            plaintext_length=len(ciphertext),
        )
        if witness is None:
            raise AssertionError("SAT model did not contain every requested value")
        if replay_unknown_gak(
            witness.plaintext,
            witness.operations,
            deck_size=deck_size,
        ) != tuple(ciphertext):
            raise AssertionError("symbolic GAK witness failed exact replay")
    return SymbolicGAKResult(
        status,
        witness,
        monotonic() - started,
        len(formula.encode()),
        output,
    )


def build_unknown_gak_messages_smt2(
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    operation_alphabet_size: int,
    timeout_ms: int = 30_000,
    request_model: bool = True,
    anchor_first_outputs: bool = True,
) -> str:
    """Build one ordinary-GAK model shared by several reset messages.

    Operations use uninterpreted functions with inverse constraints on every
    argument reached by the unrolled observations. The resulting finite
    partial injections can always be extended to full permutations. Every
    observed top card is a composition evaluated at position zero, so complete
    deck-state arrays are unnecessary.
    """

    if not ciphertexts:
        raise ValueError("at least one ciphertext is required")
    if deck_size < 2:
        raise ValueError("deck_size must be at least two")
    if not 1 <= operation_alphabet_size <= deck_size - 1:
        raise ValueError("invalid double-free operation alphabet size")
    if timeout_ms < 1:
        raise ValueError("timeout_ms must be positive")
    if any(
        not 0 <= value < deck_size
        for ciphertext in ciphertexts
        for value in ciphertext
    ):
        raise ValueError("ciphertext card is outside the deck")

    lines = [
        "(set-logic QF_UFLIA)",
        "(set-option :produce-models true)",
        f"(set-option :timeout {timeout_ms})",
    ]
    operation_names = []
    for symbol in range(operation_alphabet_size):
        operation = f"p_{symbol}"
        inverse = f"pi_{symbol}"
        operation_names.append(operation)
        lines.append(f"(declare-fun {operation} (Int) Int)")
        lines.append(f"(declare-fun {inverse} (Int) Int)")
        value = f"({operation} 0)"
        lines.append(
            f"(assert (and (<= 0 {value}) (< {value} {deck_size})))"
        )
        lines.append(f"(assert (= ({inverse} {value}) 0))")
        lines.append(f"(assert (not (= ({operation} 0) 0)))")

    tops = " ".join(f"({name} 0)" for name in operation_names)
    if operation_alphabet_size > 1:
        lines.append(f"(assert (distinct {tops}))")

    first_outputs = tuple(
        dict.fromkeys(
            ciphertext[0] for ciphertext in ciphertexts if ciphertext
        )
    )
    if len(first_outputs) > operation_alphabet_size:
        lines.append("(assert false)")
    anchored = anchor_first_outputs and len(first_outputs) <= operation_alphabet_size
    first_operation: dict[int, int] = {}
    if anchored:
        for symbol, emitted in enumerate(first_outputs):
            first_operation[emitted] = symbol
            lines.append(
                f"(assert (= (p_{symbol} 0) {emitted}))"
            )
        extra_tops = [
            f"({operation_names[symbol]} 0)"
            for symbol in range(len(first_outputs), operation_alphabet_size)
        ]
        if len(extra_tops) > 1:
            lines.append(f"(assert (< {' '.join(extra_tops)}))")
    elif operation_alphabet_size > 1:
        lines.append(f"(assert (< {tops}))")

    schedule_names: list[tuple[str, ...]] = []
    intermediate_names: list[str] = []
    for message_index, ciphertext in enumerate(ciphertexts):
        message_schedule = []
        for offset, emitted in enumerate(ciphertext):
            schedule = f"q_{message_index}_{offset}"
            message_schedule.append(schedule)
            lines.append(f"(declare-const {schedule} Int)")
            lines.append(
                f"(assert (and (<= 0 {schedule}) "
                f"(< {schedule} {operation_alphabet_size})))"
            )
            if offset == 0 and anchored:
                lines.append(
                    f"(assert (= {schedule} {first_operation[emitted]}))"
                )
            # product p[q0] o ... o p[qt] acts on zero from right to
            # left. Name every nested value to avoid exponential expression
            # duplication.
            inner = "0"
            for layer in range(offset, -1, -1):
                value = f"e_{message_index}_{offset}_{layer}"
                intermediate_names.append(value)
                lines.append(f"(declare-const {value} Int)")
                images = tuple(
                    f"({operation} {inner})" for operation in operation_names
                )
                for operation, image in zip(
                    operation_names, images, strict=True
                ):
                    lines.append(
                        f"(assert (and (<= 0 {image}) (< {image} {deck_size})))"
                    )
                    lines.append(
                        f"(assert (= (pi_{operation[2:]} {image}) {inner}))"
                    )
                lines.append(
                    f"(assert (= {value} "
                    f"{_ite(f'q_{message_index}_{layer}', images)}))"
                )
                inner = value
            lines.append(f"(assert (= {inner} {emitted}))")
        schedule_names.append(tuple(message_schedule))

    lines.append("(check-sat)")
    if request_model:
        requested = [
            f"({operation} {position})"
            for operation in operation_names
            for position in range(deck_size)
        ] + [
            name for message_schedule in schedule_names for name in message_schedule
        ] + intermediate_names
        lines.append(f"(get-value ({' '.join(requested)}))")
    lines.append("(exit)")
    return "\n".join(lines) + "\n"


def _parse_messages_witness(
    output: str,
    *,
    deck_size: int,
    operation_alphabet_size: int,
    message_lengths: Sequence[int],
) -> SymbolicGAKMessagesWitness | None:
    schedule_assignments = {
        name: int(value)
        for name, value in re.findall(
            r"\((q_\d+_\d+)\s+(-?\d+)\)", output
        )
    }
    operation_assignments = {
        (int(symbol), int(position)): int(value)
        for symbol, position, value in re.findall(
            r"\(\(p_(\d+)\s+(\d+)\)\s+(-?\d+)\)",
            output,
        )
    }
    schedule_names = tuple(
        tuple(
            f"q_{message_index}_{offset}" for offset in range(length)
        )
        for message_index, length in enumerate(message_lengths)
    )
    intermediate_assignments = {
        (int(message), int(offset), int(layer)): int(value)
        for _, message, offset, layer, value in re.findall(
            r"\((e_(\d+)_(\d+)_(\d+))\s+(-?\d+)\)",
            output,
        )
    }
    used_inputs = {0}
    for message_index, length in enumerate(message_lengths):
        for offset in range(length):
            for layer in range(1, offset + 1):
                key = (message_index, offset, layer)
                if key not in intermediate_assignments:
                    return None
                used_inputs.add(intermediate_assignments[key])
    required_operations = {
        (symbol, position)
        for symbol in range(operation_alphabet_size)
        for position in used_inputs
    }
    required_schedule = {name for row in schedule_names for name in row}
    if (
        not required_operations <= operation_assignments.keys()
        or not required_schedule <= schedule_assignments.keys()
    ):
        return None
    completed_operations = []
    for symbol in range(operation_alphabet_size):
        partial = {
            position: operation_assignments[symbol, position]
            for position in used_inputs
        }
        if len(set(partial.values())) != len(partial):
            raise AssertionError("solver returned a non-injective partial operation")
        remaining_inputs = [
            position for position in range(deck_size) if position not in partial
        ]
        remaining_outputs = [
            value for value in range(deck_size) if value not in partial.values()
        ]
        operation = dict(partial)
        operation.update(zip(remaining_inputs, remaining_outputs, strict=True))
        completed_operations.append(
            tuple(operation[position] for position in range(deck_size))
        )
    return SymbolicGAKMessagesWitness(
        tuple(completed_operations),
        tuple(
            tuple(schedule_assignments[name] for name in row)
            for row in schedule_names
        ),
    )


def solve_unknown_gak_messages_with_z3(
    ciphertexts: Sequence[Sequence[int]],
    *,
    deck_size: int,
    operation_alphabet_size: int,
    timeout_ms: int = 30_000,
    z3_path: str | None = None,
) -> SymbolicGAKMessagesResult:
    """Run the shared-operation, multiple-reset-message SMT encoding."""

    executable = z3_path or shutil.which("z3")
    if executable is None:
        raise RuntimeError("z3 executable is unavailable")
    formula = build_unknown_gak_messages_smt2(
        ciphertexts,
        deck_size=deck_size,
        operation_alphabet_size=operation_alphabet_size,
        timeout_ms=timeout_ms,
    )
    started = monotonic()
    try:
        completed = subprocess.run(
            (executable, "-in"),
            input=formula,
            text=True,
            capture_output=True,
            timeout=timeout_ms / 1_000 + 2,
            check=False,
        )
        output = completed.stdout + completed.stderr
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or "") + (error.stderr or "")
        return SymbolicGAKMessagesResult(
            "unknown",
            None,
            monotonic() - started,
            len(formula.encode()),
            output,
        )

    first_line = output.lstrip().splitlines()[0] if output.strip() else ""
    status = first_line if first_line in {"sat", "unsat", "unknown"} else "error"
    witness = None
    if status == "sat":
        witness = _parse_messages_witness(
            output,
            deck_size=deck_size,
            operation_alphabet_size=operation_alphabet_size,
            message_lengths=tuple(map(len, ciphertexts)),
        )
        if witness is None:
            raise AssertionError("SAT model did not contain every requested value")
        for plaintext, ciphertext in zip(
            witness.plaintexts, ciphertexts, strict=True
        ):
            if replay_unknown_gak(
                plaintext,
                witness.operations,
                deck_size=deck_size,
            ) != tuple(ciphertext):
                raise AssertionError("multi-message GAK witness failed exact replay")
    return SymbolicGAKMessagesResult(
        status,
        witness,
        monotonic() - started,
        len(formula.encode()),
        output,
    )
