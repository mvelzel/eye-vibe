"""Bounded static inventory of cardinality-bearing Lua arithmetic."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import re

from .wak import WakArchive


TARGET_CARDINALITIES = frozenset((9, 42, 83, 101))

_RANDOM = re.compile(
    r"\bRandom\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)"
)
_RANDOM_PARTITION = re.compile(
    r"\bRandom\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)"
    r"\s*(<=|>=|==|<|>)\s*(-?\d+)"
)
_NUMERIC_FOR = re.compile(
    r"\bfor\s+([A-Za-z_]\w*)\s*=\s*(-?\d+)\s*,\s*(-?\d+)"
    r"(?:\s*,\s*(-?\d+))?"
)
_MODULO = re.compile(r"%\s*(\d+)")
_ASSIGNMENT = re.compile(
    r"\s*(?:\blocal\s+)?\b([A-Za-z_]\w*)\s*="
)


@dataclass(frozen=True)
class LuaArithmeticHit:
    """One literal arithmetic signature and conservative lookup-flow flag."""

    cardinality: int
    kind: str
    path: str
    line: int
    source: str
    detail: str
    feeds_lookup: bool


def _comparison_count(
    low: int, high: int, operator: str, threshold: int
) -> tuple[int, int]:
    if high < low:
        return 0, 0
    predicates = {
        "<": lambda value: value < threshold,
        "<=": lambda value: value <= threshold,
        ">": lambda value: value > threshold,
        ">=": lambda value: value >= threshold,
        "==": lambda value: value == threshold,
    }
    true_count = sum(predicates[operator](value) for value in range(low, high + 1))
    return true_count, high - low + 1 - true_count


def _range_count(low: int, high: int, step: int) -> int:
    if step == 0 or (high - low) * step < 0:
        return 0
    return abs(high - low) // abs(step) + 1


def _lookup_flow(
    lines: tuple[str, ...],
    line_index: int,
    variable: str | None,
    *,
    window: int = 20,
) -> bool:
    current = lines[line_index].split("--", 1)[0]
    if _RANDOM.search(current) and re.search(r"\[[^\]]*\bRandom\s*\(", current):
        return True
    if variable is None:
        return False
    bracket_use = re.compile(
        rf"\[[^\]]*\b{re.escape(variable)}\b[^\]]*\]"
    )
    if bracket_use.search(current):
        return True
    reassignment = re.compile(
        rf"(?:\blocal\s+)?\b{re.escape(variable)}\s*="
    )
    for later in lines[line_index + 1 : line_index + 1 + window]:
        code = later.split("--", 1)[0]
        if reassignment.search(code):
            break
        if bracket_use.search(code):
            return True
    return False


def scan_lua_arithmetic_signatures(
    files: Iterable[tuple[str, str]],
    *,
    targets: frozenset[int] = TARGET_CARDINALITIES,
) -> tuple[LuaArithmeticHit, ...]:
    """Scan Lua source without treating unrelated numeric literals as clues."""

    hits = []
    for path, text in files:
        lines = tuple(text.splitlines())
        for line_index, raw_source in enumerate(lines):
            code = raw_source.split("--", 1)[0]

            for match in _RANDOM.finditer(code):
                low, high = map(int, match.groups())
                cardinality = high - low + 1
                if cardinality not in targets:
                    continue
                assignment = _ASSIGNMENT.match(code[: match.start()])
                variable = assignment.group(1) if assignment else None
                hits.append(
                    LuaArithmeticHit(
                        cardinality,
                        "random_domain",
                        path,
                        line_index + 1,
                        raw_source.strip(),
                        f"[{low},{high}]",
                        _lookup_flow(lines, line_index, variable),
                    )
                )

            for match in _RANDOM_PARTITION.finditer(code):
                low = int(match.group(1))
                high = int(match.group(2))
                operator = match.group(3)
                threshold = int(match.group(4))
                true_count, false_count = _comparison_count(
                    low, high, operator, threshold
                )
                for branch, cardinality in (
                    ("true", true_count),
                    ("false", false_count),
                ):
                    if cardinality in targets:
                        hits.append(
                            LuaArithmeticHit(
                                cardinality,
                                "random_partition",
                                path,
                                line_index + 1,
                                raw_source.strip(),
                                f"{branch}; other={false_count if branch == 'true' else true_count}",
                                False,
                            )
                        )

            for match in _NUMERIC_FOR.finditer(code):
                variable = match.group(1)
                low = int(match.group(2))
                high = int(match.group(3))
                step = int(match.group(4) or 1)
                cardinality = _range_count(low, high, step)
                if cardinality in targets:
                    hits.append(
                        LuaArithmeticHit(
                            cardinality,
                            "numeric_for",
                            path,
                            line_index + 1,
                            raw_source.strip(),
                            f"[{low},{high}] step {step}",
                            _lookup_flow(lines, line_index, variable),
                        )
                    )

            for match in _MODULO.finditer(code):
                cardinality = int(match.group(1))
                if cardinality not in targets:
                    continue
                assignment = _ASSIGNMENT.match(code[: match.start()])
                variable = assignment.group(1) if assignment else None
                hits.append(
                    LuaArithmeticHit(
                        cardinality,
                        "modulo",
                        path,
                        line_index + 1,
                        raw_source.strip(),
                        f"mod {cardinality}",
                        _lookup_flow(lines, line_index, variable),
                    )
                )
    return tuple(hits)


def scan_wak_arithmetic_signatures(
    archive: WakArchive,
) -> tuple[LuaArithmeticHit, ...]:
    """Scan every Lua entry in a WAK archive."""

    return scan_lua_arithmetic_signatures(
        (
            (entry.path, archive.read(entry).decode("utf-8", errors="ignore"))
            for entry in archive.entries
            if entry.path.lower().endswith(".lua")
        )
    )
