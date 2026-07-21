#!/usr/bin/env python3
"""Index an installed Noita ``data.wak`` and search paths or raw contents."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from eye_mystery.wak import WakArchive


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--path-regex")
    parser.add_argument("--content-regex")
    parser.add_argument("--case-sensitive", action="store_true")
    parser.add_argument(
        "--show-text",
        action="store_true",
        help="decode and display every path match (use with a narrow path regex)",
    )
    parser.add_argument(
        "--extract-dir",
        type=Path,
        help="extract path matches beneath this directory",
    )
    args = parser.parse_args()

    archive = WakArchive.open(args.archive)
    print(
        f"version={archive.version} entries={len(archive.entries)} "
        f"directory_end=0x{archive.directory_end:x}"
    )
    flags = 0 if args.case_sensitive else re.IGNORECASE
    if args.path_regex:
        expression = re.compile(args.path_regex, flags)
        path_hits = [entry for entry in archive.entries if expression.search(entry.path)]
        print(f"path_hits={len(path_hits)}")
        for entry in path_hits:
            print(f"  {entry.path} offset=0x{entry.offset:x} size={entry.size}")
            if args.show_text:
                print(archive.read(entry).decode("utf-8", errors="replace"))
            if args.extract_dir:
                relative = Path(entry.path)
                if relative.is_absolute() or ".." in relative.parts:
                    raise ValueError(f"unsafe WAK path {entry.path!r}")
                destination = args.extract_dir / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(archive.read(entry))
    if args.content_regex:
        hits = tuple(
            archive.matching_contents(args.content_regex.encode("utf-8"), flags=flags)
        )
        print(f"content_hits={len(hits)}")
        for entry, offset in hits:
            print(f"  {entry.path}+0x{offset:x}")


if __name__ == "__main__":
    main()
