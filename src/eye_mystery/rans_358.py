"""The key-free radix-5, total-83 quasi-uniform rANS interpretation."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.ninth_causal import CONTEXT_SPECS


TOTAL_FREQUENCY = 83
RADIX = 5
LOWER_BOUND = 83
SYMBOLS = 42


@dataclass(frozen=True)
class QuasiUniformTable:
    """A 42-symbol table with 41 frequencies of two and one of one."""

    singleton: str

    def __post_init__(self) -> None:
        if self.singleton not in {"first", "last"}:
            raise ValueError("singleton must be first or last")

    def frequency_and_cumulative(self, symbol: int) -> tuple[int, int]:
        if symbol not in range(SYMBOLS):
            raise ValueError("symbol lies outside the 42-symbol alphabet")
        if self.singleton == "last":
            return (2, 2 * symbol) if symbol < 41 else (1, 82)
        return (1, 0) if symbol == 0 else (2, 2 * symbol - 1)

    def symbol_for_residue(self, residue: int) -> int:
        if residue not in range(TOTAL_FREQUENCY):
            raise ValueError("residue lies outside the rANS table")
        if self.singleton == "last":
            return residue // 2 if residue < 82 else 41
        return 0 if residue == 0 else 1 + (residue - 1) // 2


@dataclass(frozen=True)
class RansEmission:
    symbol: int
    consumed_positions: tuple[int, ...]


@dataclass(frozen=True)
class RansDecode:
    emissions: tuple[RansEmission, ...]
    consumed_digits: int
    terminal_state: int

    @property
    def symbols(self) -> tuple[int, ...]:
        return tuple(emission.symbol for emission in self.emissions)


def decode_rans(
    digits: Sequence[int],
    initial_state: int,
    table: QuasiUniformTable,
    *,
    reverse: bool = False,
    maximum_symbols: int | None = None,
) -> RansDecode:
    """Decode a complete radix-5 digit stream with standard rANS steps."""

    if not LOWER_BOUND <= initial_state < RADIX * LOWER_BOUND:
        raise ValueError("initial state lies outside the normalization interval")
    frozen = tuple(digits)
    if any(digit not in range(RADIX) for digit in frozen):
        raise ValueError("rANS digits must lie in 0..4")
    positions = list(range(len(frozen)))
    if reverse:
        positions.reverse()

    state = initial_state
    cursor = 0
    consumed: tuple[int, ...] = ()
    emissions = []
    while maximum_symbols is None or len(emissions) < maximum_symbols:
        residue = state % TOTAL_FREQUENCY
        quotient = state // TOTAL_FREQUENCY
        symbol = table.symbol_for_residue(residue)
        frequency, cumulative = table.frequency_and_cumulative(symbol)
        emissions.append(RansEmission(symbol, consumed))
        state = frequency * quotient + residue - cumulative

        refill = []
        while state < LOWER_BOUND and cursor < len(positions):
            position = positions[cursor]
            state = RADIX * state + frozen[position]
            refill.append(position)
            cursor += 1
        consumed = tuple(refill)
        if state < LOWER_BOUND:
            break
    return RansDecode(tuple(emissions), cursor, state)


def encode_rans(
    symbols: Sequence[int],
    terminal_state: int,
    table: QuasiUniformTable,
) -> tuple[int, tuple[int, ...]]:
    """Encode symbols and return ``(initial_state, decoder_digit_stream)``."""

    if not LOWER_BOUND <= terminal_state < RADIX * LOWER_BOUND:
        raise ValueError("terminal state lies outside the normalization interval")
    state = terminal_state
    emitted_digits = []
    for symbol in reversed(tuple(symbols)):
        frequency, cumulative = table.frequency_and_cumulative(symbol)

        def encoded(candidate: int) -> int:
            return (
                TOTAL_FREQUENCY * (candidate // frequency)
                + candidate % frequency
                + cumulative
            )

        while encoded(state) >= RADIX * LOWER_BOUND:
            emitted_digits.append(state % RADIX)
            state //= RADIX
        state = encoded(state)
    return state, tuple(reversed(emitted_digits))


def restricted_growth(values: Sequence[int]) -> tuple[int, ...]:
    labels: dict[int, int] = {}
    return tuple(labels.setdefault(value, len(labels)) for value in values)


def context_output(
    decode: RansDecode,
    *,
    start: int,
    length: int,
) -> tuple[int, ...]:
    """Return emissions wholly sourced inside one accepted-glyph interval."""

    if start < 1:
        raise ValueError("context must begin after the state/header glyph")
    lower = (start - 1) * 3
    upper = (start + length - 1) * 3
    return tuple(
        emission.symbol
        for emission in decode.emissions
        if emission.consumed_positions
        and all(lower <= position < upper for position in emission.consumed_positions)
    )


@dataclass(frozen=True)
class RansContextResult:
    name: str
    left_length: int
    right_length: int
    literal_matches: int
    compared: int
    common_prefix: int
    pattern_equal: bool


@dataclass(frozen=True)
class RansModelResult:
    singleton: str
    reverse: bool
    quotient: int
    literal_matches: int
    compared: int
    common_prefix: int
    pattern_equal_contexts: int
    contexts: tuple[RansContextResult, ...]


def eye_rans_audit() -> tuple[RansModelResult, ...]:
    """Run the 16 standard quasi-uniform variants on fixed Eye contexts."""

    headers = {
        name: trigram_values(MESSAGES[name])[0]
        for name in MESSAGES
    }
    results = []
    for singleton in ("last", "first"):
        table = QuasiUniformTable(singleton)
        for reverse in (False, True):
            for quotient in range(1, RADIX):
                decodes = {
                    name: decode_rans(
                        MESSAGES[name][3:],
                        quotient * TOTAL_FREQUENCY + headers[name],
                        table,
                        reverse=reverse,
                    )
                    for name in MESSAGES
                }
                contexts = []
                for (
                    context_name,
                    left_name,
                    left_start,
                    right_name,
                    right_start,
                    length,
                ) in CONTEXT_SPECS[6:]:
                    left = context_output(
                        decodes[left_name],
                        start=left_start,
                        length=length,
                    )
                    right = context_output(
                        decodes[right_name],
                        start=right_start,
                        length=length,
                    )
                    compared = min(len(left), len(right))
                    prefix = next(
                        (
                            index
                            for index, (left_value, right_value) in enumerate(
                                zip(left, right)
                            )
                            if left_value != right_value
                        ),
                        compared,
                    )
                    contexts.append(
                        RansContextResult(
                            context_name,
                            len(left),
                            len(right),
                            sum(
                                left_value == right_value
                                for left_value, right_value in zip(left, right)
                            ),
                            compared,
                            prefix,
                            len(left) == len(right)
                            and restricted_growth(left) == restricted_growth(right),
                        )
                    )
                results.append(
                    RansModelResult(
                        singleton,
                        reverse,
                        quotient,
                        sum(context.literal_matches for context in contexts),
                        sum(context.compared for context in contexts),
                        sum(context.common_prefix for context in contexts),
                        sum(context.pattern_equal for context in contexts),
                        tuple(contexts),
                    )
                )
    return tuple(results)
