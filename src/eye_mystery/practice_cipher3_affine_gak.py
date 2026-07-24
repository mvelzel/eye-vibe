"""Affine group-autokey tests for sdlwdr practice Cipher 3."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass

from eye_mystery.affine_gak import MODULUS, decode_affine_gak
from eye_mystery.metrics import index_of_coincidence
from eye_mystery.practice_cipher3_wide import GROUPS, load_cipher3


MODES = (
    "full",
    "primer",
    "skip",
    "indicator-hidden",
    "indicator-both",
)
FAMILIES = (
    "linear",
    "power-base",
    "power-exponent",
    "reciprocal-shift",
)


@dataclass(frozen=True)
class StructuredCandidate:
    mode: str
    family: str
    parameters: tuple[int, ...]


def structured_candidates() -> tuple[StructuredCandidate, ...]:
    """Return the complete frozen five-mode, four-family catalog."""

    candidates = []
    for mode in MODES:
        candidates.extend(
            StructuredCandidate(mode, "linear", (linear, offset))
            for linear in range(MODULUS)
            for offset in range(MODULUS)
        )
        candidates.extend(
            StructuredCandidate(mode, "power-base", (generator,))
            for generator in range(1, MODULUS)
        )
        candidates.extend(
            StructuredCandidate(mode, "power-exponent", (exponent,))
            for exponent in range(1, MODULUS - 1)
        )
        candidates.extend(
            StructuredCandidate(mode, "reciprocal-shift", (shift,))
            for shift in range(MODULUS)
        )
    return tuple(candidates)


def candidate_multiplier(candidate: StructuredCandidate, value: int) -> int:
    """Evaluate one frozen structured multiplier function."""

    if candidate.family == "linear":
        linear, offset = candidate.parameters
        return (linear * value + offset) % MODULUS
    if candidate.family == "power-base":
        (generator,) = candidate.parameters
        return pow(generator, value, MODULUS)
    if candidate.family == "power-exponent":
        (exponent,) = candidate.parameters
        return pow(value, exponent, MODULUS)
    if candidate.family == "reciprocal-shift":
        (shift,) = candidate.parameters
        denominator = (value + shift) % MODULUS
        return 0 if denominator == 0 else pow(denominator, -1, MODULUS)
    raise ValueError(f"unknown structured family: {candidate.family}")


def decode_candidate(
    messages: Sequence[Sequence[int]],
    candidate: StructuredCandidate,
) -> tuple[tuple[int, ...], ...] | None:
    """Decode reset messages under one structured candidate."""

    decoded = []
    for message in messages:
        stream = decode_affine_gak(
            message,
            lambda value: candidate_multiplier(candidate, value),
            candidate.mode,
        )
        if stream is None:
            return None
        decoded.append(stream)
    return tuple(decoded)


@dataclass(frozen=True)
class TrainingScore:
    candidate: StructuredCandidate
    unique: int
    ioc: float


@dataclass(frozen=True)
class StructuredSearchResult:
    selected: StructuredCandidate
    training_unique: int
    validation_unique: int | None
    heldout_unique: int | None
    complete_unique: int | None
    training_ioc: float
    valid_candidates: int
    training_at_most_42: int
    minimizers: tuple[StructuredCandidate, ...]


def _candidate_key(score: TrainingScore) -> tuple[object, ...]:
    return (
        score.unique,
        -score.ioc,
        MODES.index(score.candidate.mode),
        FAMILIES.index(score.candidate.family),
        score.candidate.parameters,
    )


def structured_search(
    streams: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> StructuredSearchResult:
    """Select a structured update on A and transfer it unchanged to B/C."""

    if streams is None:
        streams = load_cipher3()
    scores = []
    at_most_42 = 0
    for candidate in structured_candidates():
        decoded = decode_candidate(streams["A"], candidate)
        if decoded is None:
            continue
        combined = tuple(value for message in decoded for value in message)
        unique = len(set(combined))
        if unique <= 42:
            at_most_42 += 1
        scores.append(
            TrainingScore(
                candidate,
                unique,
                index_of_coincidence(combined, unique),
            )
        )
    if not scores:
        raise ValueError("the structured catalog has no valid A candidate")
    selected_score = min(scores, key=_candidate_key)
    minimum_key = (
        selected_score.unique,
        -selected_score.ioc,
    )
    minimizers = tuple(
        score.candidate
        for score in scores
        if (score.unique, -score.ioc) == minimum_key
    )
    decoded_groups = {
        group: decode_candidate(streams[group], selected_score.candidate)
        for group in GROUPS
    }
    unique_by_group = {
        group: (
            None
            if decoded_groups[group] is None
            else len(
                set(
                    value
                    for message in decoded_groups[group] or ()
                    for value in message
                )
            )
        )
        for group in GROUPS
    }
    complete = (
        None
        if any(decoded is None for decoded in decoded_groups.values())
        else len(
            set(
                value
                for group in GROUPS
                for message in decoded_groups[group] or ()
                for value in message
            )
        )
    )
    return StructuredSearchResult(
        selected_score.candidate,
        unique_by_group["A"],
        unique_by_group["B"],
        unique_by_group["C"],
        complete,
        selected_score.ioc,
        len(scores),
        at_most_42,
        minimizers,
    )


def encrypt_affine_gak(
    plaintext: Sequence[int],
    multiplier_for_plaintext: Callable[[int], int],
    mode: str,
    *,
    header: int = 1,
) -> tuple[int, ...]:
    """Encrypt one reset stream under the coordinate model used by the tests."""

    if mode == "full":
        prefix: tuple[int, ...] = ()
        previous = 0
        hidden = 1
    elif mode == "primer":
        prefix = (header % MODULUS,)
        previous = header % MODULUS
        hidden = 1
    elif mode == "skip":
        prefix = (header % MODULUS,)
        previous = 0
        hidden = 1
    elif mode == "indicator-hidden":
        prefix = (header % MODULUS,)
        previous = 0
        hidden = header % MODULUS
    elif mode == "indicator-both":
        prefix = (header % MODULUS,)
        previous = header % MODULUS
        hidden = header % MODULUS
    else:
        raise ValueError(f"unknown affine GAK mode: {mode}")
    if hidden == 0:
        raise ValueError("indicator modes require a nonzero header")

    ciphertext = list(prefix)
    for symbol in plaintext:
        if symbol % MODULUS == 0:
            raise ValueError("this affine coordinate cannot encode zero")
        current = (previous + symbol * pow(hidden, -1, MODULUS)) % MODULUS
        ciphertext.append(current)
        multiplier = multiplier_for_plaintext(symbol) % MODULUS
        if multiplier == 0:
            raise ValueError("plaintext update multiplier must be nonzero")
        hidden = hidden * multiplier % MODULUS
        previous = current
    return tuple(ciphertext)


def discrete_log_table(generator: int = 2) -> dict[int, int]:
    """Return nonzero F83 discrete logs for a primitive generator."""

    table = {}
    value = 1
    for exponent in range(MODULUS - 1):
        table[value] = exponent
        value = value * generator % MODULUS
    if len(table) != MODULUS - 1:
        raise ValueError(f"{generator} is not primitive modulo {MODULUS}")
    return table


def _mode_parts(
    message: Sequence[int],
    mode: str,
) -> tuple[int, int, tuple[int, ...]]:
    message = tuple(message)
    if mode == "full":
        return 0, 1, message
    if not message:
        raise ValueError("header mode requires a nonempty message")
    if mode == "primer":
        return message[0], 1, message[1:]
    if mode == "skip":
        return 0, 1, message[1:]
    if mode == "indicator-hidden":
        return 0, message[0], message[1:]
    if mode == "indicator-both":
        return message[0], message[0], message[1:]
    raise ValueError(f"unknown affine GAK mode: {mode}")


@dataclass(frozen=True)
class ExactGakResult:
    status: str
    reason: str
    realized_states: tuple[int, ...]
    update_exponents: tuple[tuple[int, int], ...]
    state_streams: tuple[tuple[str, tuple[int, ...]], ...]


def solve_exact_affine_gak(
    named_messages: Sequence[tuple[str, Sequence[int]]],
    *,
    mode: str,
    max_symbols: int = 42,
    timeout_ms: int = 30_000,
) -> ExactGakResult:
    """Solve the arbitrary-update affine GAK boundary with Z3."""

    import z3

    if not 1 <= max_symbols <= MODULUS - 1:
        raise ValueError("max_symbols must be between 1 and 82")
    logs = discrete_log_table()
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    updates = z3.Array(
        "gak_updates",
        z3.BitVecSort(7),
        z3.BitVecSort(7),
    )
    for state in range(MODULUS - 1):
        solver.add(
            z3.ULT(
                z3.Select(updates, z3.BitVecVal(state, 7)),
                z3.BitVecVal(MODULUS - 1, 7),
            )
        )
    representatives = tuple(
        z3.BitVec(f"gak_representative_{index}", 7)
        for index in range(max_symbols)
    )
    for representative in representatives:
        solver.add(
            z3.ULT(representative, z3.BitVecVal(MODULUS - 1, 7))
        )
    for left, right in zip(representatives, representatives[1:]):
        solver.add(z3.ULT(left, right))

    symbolic_streams = []
    all_states = []
    for message_index, (name, message) in enumerate(named_messages):
        previous, initial_hidden, body = _mode_parts(message, mode)
        if initial_hidden == 0:
            return ExactGakResult(
                "invalid",
                f"{name} has a zero hidden-state indicator",
                (),
                (),
                (),
            )
        differences = []
        for current in body:
            difference = (current - previous) % MODULUS
            if difference == 0:
                return ExactGakResult(
                    "invalid",
                    f"{name} contains a zero visible difference",
                    (),
                    (),
                    (),
                )
            differences.append(logs[difference])
            previous = current
        if not differences:
            continue
        states = tuple(
            z3.BitVec(f"gak_state_{message_index}_{position}", 7)
            for position in range(len(differences))
        )
        symbolic_streams.append((name, states))
        all_states.extend(states)
        for state in states:
            solver.add(z3.ULT(state, z3.BitVecVal(MODULUS - 1, 7)))
            solver.add(z3.Or([state == value for value in representatives]))
        solver.add(
            states[0]
            == z3.BitVecVal(
                (differences[0] + logs[initial_hidden])
                % (MODULUS - 1),
                7,
            )
        )
        for position in range(len(states) - 1):
            delta = (
                differences[position + 1] - differences[position]
            ) % (MODULUS - 1)
            wide_sum = (
                z3.ZeroExt(1, states[position])
                + z3.BitVecVal(delta, 8)
                + z3.ZeroExt(1, z3.Select(updates, states[position]))
            )
            reduced = z3.If(
                z3.UGE(wide_sum, z3.BitVecVal(2 * (MODULUS - 1), 8)),
                wide_sum - z3.BitVecVal(2 * (MODULUS - 1), 8),
                z3.If(
                    z3.UGE(wide_sum, z3.BitVecVal(MODULUS - 1, 8)),
                    wide_sum - z3.BitVecVal(MODULUS - 1, 8),
                    wide_sum,
                ),
            )
            solver.add(
                z3.ZeroExt(1, states[position + 1]) == reduced
            )

    outcome = solver.check()
    if outcome == z3.unknown:
        return ExactGakResult(
            "unknown",
            solver.reason_unknown(),
            (),
            (),
            (),
        )
    if outcome == z3.unsat:
        return ExactGakResult("unsat", "", (), (), ())

    model = solver.model()
    concrete_streams = tuple(
        (
            name,
            tuple(model.eval(state).as_long() for state in states),
        )
        for name, states in symbolic_streams
    )
    realized = tuple(
        sorted(
            {
                state
                for _, states in concrete_streams
                for state in states
            }
        )
    )
    update_exponents = tuple(
        (
            state,
            model.eval(z3.Select(updates, state)).as_long(),
        )
        for state in realized
    )
    return ExactGakResult(
        "sat",
        "",
        realized,
        update_exponents,
        concrete_streams,
    )


def replay_exact_model(
    result: ExactGakResult,
    named_messages: Sequence[tuple[str, Sequence[int]]],
    *,
    mode: str,
) -> bool:
    """Re-encrypt an exact model and require byte-for-byte ciphertext replay."""

    if result.status != "sat":
        return False
    messages = {name: tuple(message) for name, message in named_messages}
    logs_to_values = tuple(pow(2, exponent, MODULUS) for exponent in range(82))
    value_to_log = discrete_log_table()
    updates = dict(result.update_exponents)
    for name, state_stream in result.state_streams:
        original = messages[name]
        plaintext = tuple(logs_to_values[state] for state in state_stream)

        def multiplier(value: int) -> int:
            return logs_to_values[updates[value_to_log[value]]]

        header = original[0] if mode != "full" else 1
        if encrypt_affine_gak(
            plaintext,
            multiplier,
            mode,
            header=header,
        ) != original:
            return False
    return True


def named_group(
    streams: Mapping[str, Sequence[Sequence[int]]],
    groups: Sequence[str],
) -> tuple[tuple[str, tuple[int, ...]], ...]:
    """Return named messages for one or more Cipher 3 groups."""

    return tuple(
        (f"{group}{index}", tuple(message))
        for group in groups
        for index, message in enumerate(streams[group])
    )
