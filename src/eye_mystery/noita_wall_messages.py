"""Load the frozen English translations of Noita's Wall Messages."""

from __future__ import annotations

import re
from pathlib import Path


HEADER_RE = re.compile(r"^=== (G\d+) ===$", re.MULTILINE)
EDITORIAL_RE = re.compile(r"\s*\[sic\]")


def load_wall_messages(path: Path) -> tuple[tuple[str, str], ...]:
    """Return ``(map_id, text)`` records in artifact order."""

    return tuple(
        (map_id, " ".join(" ".join(lines).split()))
        for map_id, lines in load_wall_message_lines(path)
    )


def load_wall_message_lines(
    path: Path,
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Return records while preserving authored line and repeated-space layout."""

    source = path.read_text(encoding="utf-8").strip()
    headers = tuple(HEADER_RE.finditer(source))
    records: list[tuple[str, tuple[str, ...]]] = []
    for index, header in enumerate(headers):
        start = header.end()
        end = headers[index + 1].start() if index + 1 < len(headers) else len(source)
        body = EDITORIAL_RE.sub("", source[start:end]).strip("\n")
        records.append((header.group(1), tuple(body.splitlines())))
    return tuple(records)
