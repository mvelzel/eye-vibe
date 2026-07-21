#!/usr/bin/env python3
"""Compare an installed Noita WAK with an unpacked historical data tree."""

from __future__ import annotations

import argparse
import difflib
import os
import re
from pathlib import Path

from eye_mystery.wak import WakArchive


def tree_files(root: Path) -> dict[str, Path]:
    result = {}
    for directory, names, files in os.walk(root):
        names[:] = [name for name in names if name != ".git"]
        for name in files:
            path = Path(directory) / name
            result[path.relative_to(root).as_posix()] = path
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("historical_tree", type=Path)
    parser.add_argument("--path-regex", default=".*")
    parser.add_argument("--show-diff", action="store_true")
    args = parser.parse_args()

    archive = WakArchive.open(args.archive)
    old_files = tree_files(args.historical_tree)
    pattern = re.compile(args.path_regex, re.IGNORECASE)
    statuses: dict[str, list[str]] = {"added": [], "changed": [], "same": []}
    wak_paths = set()
    for entry in archive.entries:
        relative = entry.path.removeprefix("data/")
        wak_paths.add(relative)
        old_path = old_files.get(relative)
        if old_path is None:
            status = "added"
        else:
            old_contents = old_path.read_bytes().replace(b"\r\n", b"\n")
            new_contents = archive.read(entry).replace(b"\r\n", b"\n")
            status = "same" if old_contents == new_contents else "changed"
        statuses[status].append(relative)
    removed = sorted(set(old_files) - wak_paths)

    print(
        f"wak={len(archive.entries)} tree={len(old_files)} "
        f"added={len(statuses['added'])} changed={len(statuses['changed'])} "
        f"removed={len(removed)} same={len(statuses['same'])}"
    )
    for status in ("added", "changed"):
        matching = [path for path in statuses[status] if pattern.search(path)]
        print(f"{status}_matching={len(matching)}")
        for path in matching:
            print(f"  {status}: {path}")
            if args.show_diff and status == "changed":
                entry = next(
                    item for item in archive.entries
                    if item.path.removeprefix("data/") == path
                )
                old_text = old_files[path].read_bytes().replace(b"\r\n", b"\n").decode(
                    "utf-8", errors="replace"
                )
                new_text = archive.read(entry).replace(b"\r\n", b"\n").decode(
                    "utf-8", errors="replace"
                )
                print(
                    "".join(
                        difflib.unified_diff(
                            old_text.splitlines(keepends=True),
                            new_text.splitlines(keepends=True),
                            fromfile=f"2023/{path}",
                            tofile=f"installed/{path}",
                        )
                    )
                )
    removed_matching = [path for path in removed if pattern.search(path)]
    print(f"removed_matching={len(removed_matching)}")
    for path in removed_matching:
        print(f"  removed: {path}")


if __name__ == "__main__":
    main()
