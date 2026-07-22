#!/usr/bin/env python3
"""Inventory exact-size table/list candidates in an installed Noita WAK."""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from eye_mystery.asset_tables import lua_tables
from eye_mystery.wak import WakArchive


TARGETS = (5, 42, 83, 101)
CLUE_WORDS = re.compile(
    r"eye|secret|puzzle|gate|guardian|seula|molari|mokke|veska|cauldron|"
    r"void|calendar|kantele|ocarina|alchemy|orb|sampo|boss|wizard|magic|song",
    re.IGNORECASE,
)


def compact_preview(text: str, start: int, end: int) -> str:
    return re.sub(r"\s+", " ", text[start:end]).strip()[:220]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    archive = WakArchive.open(args.archive)

    lua_counts: Counter[int] = Counter()
    simple_five = []
    lua_hits = []
    lua_files = 0
    for entry in archive.entries:
        if not entry.path.lower().endswith(".lua"):
            continue
        lua_files += 1
        text = archive.read(entry).decode("utf-8", errors="ignore")
        for table in lua_tables(text):
            lua_counts[table.item_count] += 1
            if table.item_count in (42, 83, 101):
                lua_hits.append(
                    (
                        table.item_count,
                        entry.path,
                        table.assigned_name,
                        table.keyed_item_count,
                        compact_preview(text, table.start, table.end),
                    )
                )
            if (
                table.item_count == 5
                and table.keyed_item_count == 0
                and table.assigned_name
            ):
                simple_five.append(
                    (
                        entry.path,
                        table.assigned_name,
                        compact_preview(text, table.start, table.end),
                    )
                )

    print(f"lua files                    {lua_files}")
    print(
        "lua table target counts     "
        + " ".join(f"{target}:{lua_counts[target]}" for target in TARGETS)
    )
    for count, path, name, keyed, preview in lua_hits:
        print(
            f"  lua target {count}: {path} :: {name or '<anonymous>'} "
            f":: keyed={keyed} :: {preview}"
        )
    print(f"assigned simple five-lists   {len(simple_five)}")
    relevant_five = tuple(
        candidate
        for candidate in simple_five
        if CLUE_WORDS.search(candidate[0] + " " + candidate[1])
    )
    print(f"clue-named five-lists        {len(relevant_five)}")
    for path, name, preview in relevant_five:
        print(f"  {path} :: {name} :: {preview}")

    xml_counts: Counter[int] = Counter()
    xml_hits = []
    xml_files = xml_failures = 0
    for entry in archive.entries:
        if not entry.path.lower().endswith(".xml"):
            continue
        xml_files += 1
        try:
            root = ET.fromstring(archive.read(entry))
        except ET.ParseError:
            xml_failures += 1
            continue
        for element in root.iter():
            xml_counts[len(element)] += 1
            if len(element) in (42, 83, 101):
                xml_hits.append((len(element), entry.path, element.tag))
    print(f"xml files / parse failures   {xml_files}/{xml_failures}")
    print(
        "xml child target counts     "
        + " ".join(f"{target}:{xml_counts[target]}" for target in TARGETS)
    )
    for count, path, tag in xml_hits:
        print(f"  xml target {count}: {path} :: {tag}")

    line_counts: Counter[int] = Counter()
    line_hits = []
    for entry in archive.entries:
        if not entry.path.lower().endswith((".csv", ".tsv", ".txt")):
            continue
        contents = archive.read(entry)
        if b"\0" in contents:
            continue
        lines = tuple(
            line
            for line in contents.decode("utf-8", errors="ignore").splitlines()
            if line.strip()
        )
        line_counts[len(lines)] += 1
        if len(lines) in (42, 83, 101):
            line_hits.append((len(lines), entry.path))
    print(
        "text line target counts     "
        + " ".join(f"{target}:{line_counts[target]}" for target in TARGETS)
    )
    for count, path in line_hits:
        print(f"  line target {count}: {path}")


if __name__ == "__main__":
    main()
