"""Finite audit of the residue-seven header/phase-length ledger."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import permutations

from eye_mystery.factoradic_headers import (
    base5_digits,
    graph_conditioned_audit,
    header_ranks,
    lexicographic_unrank,
)
from eye_mystery.gate_plus3_transfer import (
    ROWS,
    admissible_assignment_ranks,
    assignment_ranks,
)
from eye_mystery.gap_anchor import FINAL_MESSAGES
from eye_mystery.synchronizing_bridge import (
    bridge_specs,
    observed_metrics,
)


NEWLINE_SYMBOL = 5
ALL_SYMBOLS = tuple(range(6))
ROW2 = ROWS[1]
FINAL_ROW = ROWS[2]


def phase_suffix_lengths() -> tuple[int, int, int]:
    """Return bridge length minus the promoted common phase length."""

    specs = bridge_specs()
    common = observed_metrics().triple_lcp
    return tuple(
        specs[name].length - common
        for name in FINAL_MESSAGES
    )  # type: ignore[return-value]


def suffix_assignments() -> tuple[tuple[int, int, int], ...]:
    return tuple(sorted(set(permutations(phase_suffix_lengths()))))


def row2_circulation(ranks: Mapping[str, int]) -> int:
    return sum(ranks[name] for name in ROW2) % 83


def final_scalar_sum(ranks: Mapping[str, int]) -> int:
    return sum(base5_digits(ranks[name])[2] for name in FINAL_ROW)


def symbol_preimage(rank: int, symbol: int) -> int:
    if symbol not in ALL_SYMBOLS:
        raise ValueError("factoradic symbol must lie in 0..5")
    return lexicographic_unrank(rank).index(symbol)


def phase_sums(
    ranks: Mapping[str, int],
    *,
    symbol: int = NEWLINE_SYMBOL,
    suffixes: Sequence[int] | None = None,
) -> tuple[int, int, int]:
    suffixes = phase_suffix_lengths() if suffixes is None else tuple(suffixes)
    if len(suffixes) != 3:
        raise ValueError("one suffix length is required per final panel")
    return tuple(
        symbol_preimage(ranks[name], symbol) + suffix
        for name, suffix in zip(FINAL_ROW, suffixes, strict=True)
    )  # type: ignore[return-value]


def exact_ledger_match(ranks: Mapping[str, int]) -> bool:
    target = row2_circulation(ranks)
    return phase_sums(ranks) == (target, target, target)


@dataclass(frozen=True)
class LedgerWitness:
    symbol: int
    suffixes: tuple[int, int, int]
    constant: int
    matches_row2: bool


def ledger_witnesses(
    ranks: Mapping[str, int],
    *,
    symbols: Sequence[int] = ALL_SYMBOLS,
    suffix_variants: Sequence[tuple[int, int, int]] | None = None,
    require_row2: bool,
) -> tuple[LedgerWitness, ...]:
    suffix_variants = (
        suffix_assignments()
        if suffix_variants is None
        else tuple(suffix_variants)
    )
    target = row2_circulation(ranks)
    preimages = {
        symbol: tuple(
            symbol_preimage(ranks[name], symbol)
            for name in FINAL_ROW
        )
        for symbol in symbols
    }
    witnesses = []
    for symbol in symbols:
        for suffixes in suffix_variants:
            sums = tuple(
                preimage + suffix
                for preimage, suffix in zip(
                    preimages[symbol],
                    suffixes,
                    strict=True,
                )
            )
            if len(set(sums)) != 1:
                continue
            matches = sums[0] == target
            if require_row2 and not matches:
                continue
            witnesses.append(
                LedgerWitness(symbol, suffixes, sums[0], matches)
            )
    return tuple(witnesses)


@dataclass(frozen=True)
class PhaseLedgerAudit:
    assignments: int
    exact_matches: int
    exact_and_final_scalar_matches: int
    any_symbol_matches: int
    any_suffix_matches: int
    any_symbol_and_suffix_matches: int
    constant_only_matches: int
    constant_and_suffix_matches: int
    fixed_suffix_symbols: tuple[int, ...]
    observed_circulation: int
    observed_suffixes: tuple[int, int, int]
    observed_preimages: tuple[int, int, int]
    observed_sums: tuple[int, int, int]
    observed_witnesses: tuple[LedgerWitness, ...]
    factoradic_survivors: int
    matching_factoradic_survivors: tuple[tuple[int, ...], ...]


def audit_phase_ledger() -> PhaseLedgerAudit:
    assignments = admissible_assignment_ranks()
    suffixes = phase_suffix_lengths()
    counts = {
        "exact": 0,
        "scalar": 0,
        "symbol": 0,
        "suffix": 0,
        "both": 0,
        "constant": 0,
        "constant_suffix": 0,
    }
    fixed_suffix_symbols: set[int] = set()
    for ranks in assignments:
        target = row2_circulation(ranks)
        row2_witnesses = ledger_witnesses(ranks, require_row2=True)
        constant_witnesses = ledger_witnesses(ranks, require_row2=False)
        exact = any(
            witness.symbol == NEWLINE_SYMBOL
            and witness.suffixes == suffixes
            for witness in row2_witnesses
        )
        counts["exact"] += exact
        counts["scalar"] += exact and final_scalar_sum(ranks) == target
        counts["symbol"] += any(
            witness.suffixes == suffixes
            for witness in row2_witnesses
        )
        fixed_suffix_symbols.update(
            witness.symbol
            for witness in row2_witnesses
            if witness.suffixes == suffixes
        )
        counts["suffix"] += any(
            witness.symbol == NEWLINE_SYMBOL
            for witness in row2_witnesses
        )
        counts["both"] += bool(row2_witnesses)
        counts["constant"] += any(
            witness.suffixes == suffixes
            for witness in constant_witnesses
        )
        counts["constant_suffix"] += bool(constant_witnesses)

    observed = header_ranks()
    full_audit = graph_conditioned_audit()
    matching_survivors = tuple(
        assignment
        for assignment in full_audit.survivors
        if exact_ledger_match(assignment_ranks(assignment))
    )
    return PhaseLedgerAudit(
        assignments=len(assignments),
        exact_matches=counts["exact"],
        exact_and_final_scalar_matches=counts["scalar"],
        any_symbol_matches=counts["symbol"],
        any_suffix_matches=counts["suffix"],
        any_symbol_and_suffix_matches=counts["both"],
        constant_only_matches=counts["constant"],
        constant_and_suffix_matches=counts["constant_suffix"],
        fixed_suffix_symbols=tuple(sorted(fixed_suffix_symbols)),
        observed_circulation=row2_circulation(observed),
        observed_suffixes=suffixes,
        observed_preimages=tuple(
            symbol_preimage(observed[name], NEWLINE_SYMBOL)
            for name in FINAL_ROW
        ),  # type: ignore[arg-type]
        observed_sums=phase_sums(observed),
        observed_witnesses=ledger_witnesses(
            observed,
            require_row2=False,
        ),
        factoradic_survivors=full_audit.full,
        matching_factoradic_survivors=matching_survivors,
    )
