"""Audit integer ``Random(0, 100)`` branches in Noita Lua sources."""

from __future__ import annotations

import mmap
import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

from .wak import WakArchive


RANDOM_0_100_COMPARISON = re.compile(
    rb"Random\s*\(\s*0\s*,\s*100\s*\)\s*(<=|>=|<|>)\s*(-?\d+)"
)


@dataclass(frozen=True)
class RandomThresholdHit:
    path: str
    offset: int
    operator: str
    threshold: int


def _hits_in_blob(path: str, contents: bytes) -> Iterator[RandomThresholdHit]:
    for match in RANDOM_0_100_COMPARISON.finditer(contents):
        yield RandomThresholdHit(
            path=path,
            offset=match.start(),
            operator=match.group(1).decode("ascii"),
            threshold=int(match.group(2)),
        )


def scan_blob_thresholds(
    blobs: Iterable[tuple[str, bytes]],
) -> tuple[RandomThresholdHit, ...]:
    """Find all direct integer threshold comparisons in named byte strings."""

    return tuple(
        hit
        for path, contents in blobs
        for hit in _hits_in_blob(path, contents)
    )


def scan_wak_thresholds(archive: WakArchive) -> tuple[RandomThresholdHit, ...]:
    """Find every direct threshold comparison without crossing WAK entries."""

    hits: list[RandomThresholdHit] = []
    with archive.path.open("rb") as source:
        with mmap.mmap(source.fileno(), 0, access=mmap.ACCESS_READ) as data:
            for entry in archive.entries:
                if not entry.path.lower().endswith(".lua"):
                    continue
                contents = data[entry.offset : entry.offset + entry.size]
                hits.extend(_hits_in_blob(entry.path, contents))
    return tuple(hits)


def scan_directory_thresholds(root: Path) -> tuple[RandomThresholdHit, ...]:
    """Find every direct threshold comparison in a loose Lua data tree."""

    return scan_blob_thresholds(
        (str(path.relative_to(root)), path.read_bytes())
        for path in sorted(root.rglob("*.lua"))
    )


def successful_outcomes(operator: str, threshold: int) -> tuple[int, ...]:
    """Return successful values assuming Noita's inclusive integer range 0..100."""

    predicates = {
        "<": lambda value: value < threshold,
        "<=": lambda value: value <= threshold,
        ">": lambda value: value > threshold,
        ">=": lambda value: value >= threshold,
    }
    try:
        predicate = predicates[operator]
    except KeyError as error:
        raise ValueError(f"unsupported comparison operator {operator!r}") from error
    return tuple(value for value in range(101) if predicate(value))
