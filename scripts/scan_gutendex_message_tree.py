#!/usr/bin/env python3
"""Scan Finnish Gutenberg lines/sentences for the complete Eye prefix tree."""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from http.client import RemoteDisconnected
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from pathlib import Path

from eye_mystery.source_fingerprints import (
    first_family_source_matches,
    normalize_source,
)
from eye_mystery.source_message_tree import (
    SourceEntry,
    message_tree_matches,
    message_tree_partials,
)


USER_AGENT = "Noita-eye-mystery research"


def fetch(url: str) -> bytes:
    error: Exception | None = None
    for attempt in range(3):
        try:
            return urlopen(
                Request(url, headers={"User-Agent": USER_AGENT}), timeout=90
            ).read()
        except (OSError, TimeoutError, URLError, RemoteDisconnected) as caught:
            error = caught
            if attempt < 2:
                time.sleep(0.5 * (attempt + 1))
    assert error is not None
    raise error


def catalog(search: str, maximum: int) -> list[dict[str, object]]:
    url: str | None = "https://gutendex.com/books/?" + urlencode(
        {"languages": "fi", "search": search}
    )
    books = []
    while url is not None and len(books) < maximum:
        page = json.loads(fetch(url))
        books.extend(page["results"])
        url = page["next"]
    return books[:maximum]


def static_catalog(path: Path, maximum: int) -> list[dict[str, object]]:
    books = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            languages = {value.strip() for value in row["Language"].split(";")}
            if row["Type"] != "Text" or "fi" not in languages:
                continue
            book_id = int(row["Text#"])
            books.append(
                {
                    "id": book_id,
                    "title": row["Title"],
                    "formats": {
                        "text/plain; charset=utf-8": (
                            f"https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8"
                        )
                    },
                }
            )
            if len(books) >= maximum:
                break
    return books


def candidate_entries(
    label: str, text: str, *, normalization: str
) -> list[SourceEntry]:
    fragments = set(text.splitlines())
    fragments.update(re.split(r"(?<=[.!?])\s+", text))
    fragments.update(re.split(r"\n\s*\n", text))
    entries = []
    for index, fragment in enumerate(fragments):
        normalized = normalize_source(
            fragment,
            mode=normalization,
            transliterate_finnish=True,
        ).upper()
        if 90 <= len(normalized) <= 145:
            entries.append(SourceEntry(f"{label} fragment {index}", normalized))
    return entries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", default="")
    parser.add_argument("--max-books", type=int, default=100)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--include-markers", action="store_true")
    parser.add_argument(
        "--same-book",
        action="store_true",
        help="match each book separately instead of pooling all entries",
    )
    parser.add_argument("--repeat-fingerprint", action="store_true")
    parser.add_argument("--catalog-csv", type=Path)
    parser.add_argument(
        "--normalization",
        choices=("letters", "spaces", "both"),
        default="both",
        help="source characters retained for length and prefix matching",
    )
    args = parser.parse_args()
    books = (
        static_catalog(args.catalog_csv, args.max_books)
        if args.catalog_csv is not None
        else catalog(args.search, args.max_books)
    )

    modes = (
        ("letters", "spaces")
        if args.normalization == "both"
        else (args.normalization,)
    )

    def load(book: dict[str, object]) -> tuple[str, str]:
        formats = book["formats"]
        assert isinstance(formats, dict)
        url = formats.get("text/plain; charset=utf-8")
        if not isinstance(url, str):
            return "", ""
        label = f"{book['id']}: {book['title']}"
        try:
            text = fetch(url).decode("utf-8", errors="ignore")
        except (OSError, TimeoutError, URLError, RemoteDisconnected):
            fallback = (
                f"https://www.gutenberg.org/cache/epub/{book['id']}/"
                f"pg{book['id']}.txt"
            )
            try:
                text = fetch(fallback).decode("utf-8", errors="ignore")
            except (OSError, TimeoutError, URLError, RemoteDisconnected):
                return "", label
        return text, label

    matches: dict[str, list[object]] = {mode: [] for mode in modes}
    fingerprint_matches: dict[str, list[object]] = {
        mode: [] for mode in modes
    }
    partial_counts = {
        mode: {
            "upper24": 0,
            "deep20": 0,
            "nested9": 0,
            "lower6": 0,
            "roots": 0,
        }
        for mode in modes
    }
    partial_examples: dict[
        str, dict[str, list[tuple[str, object]]]
    ] = {
        mode: {name: [] for name in partial_counts[mode]}
        for mode in modes
    }
    entry_count = {mode: 0 for mode in modes}
    loaded_count = 0
    failed_labels = []
    pooled_entries = {mode: [] for mode in modes}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(load, book) for book in books]
        for completed, future in enumerate(as_completed(futures), start=1):
            text, label = future.result()
            loaded_count += bool(text)
            if not text and label:
                failed_labels.append(label)
            for mode in modes:
                entries = candidate_entries(
                    label, text, normalization=mode
                )
                entry_count[mode] += len(entries)
                if args.same_book:
                    matches[mode].extend(
                        message_tree_matches(
                            entries,
                            include_markers=args.include_markers,
                        )
                    )
                    if args.repeat_fingerprint and text:
                        normalized = normalize_source(
                            text,
                            mode=mode,
                            transliterate_finnish=True,
                        )
                        fingerprint_matches[mode].extend(
                            first_family_source_matches({label: normalized})
                        )
                    partials = message_tree_partials(
                        entries, include_markers=args.include_markers
                    )
                    for name in partial_counts[mode]:
                        values = getattr(partials, name)
                        partial_counts[mode][name] += len(values)
                        examples = partial_examples[mode][name]
                        if len(examples) < 20:
                            examples.extend(
                                (label, value)
                                for value in values[: 20 - len(examples)]
                            )
                else:
                    pooled_entries[mode].extend(entries)
            if completed % 100 == 0 or completed == len(futures):
                entry_summary = ",".join(
                    f"{mode}:{entry_count[mode]}" for mode in modes
                )
                tree_summary = ",".join(
                    f"{mode}:{len(matches[mode])}" for mode in modes
                )
                fingerprint_summary = ",".join(
                    f"{mode}:{len(fingerprint_matches[mode])}"
                    for mode in modes
                )
                print(
                    f"progress: {completed}/{len(futures)} "
                    f"loaded={loaded_count} entries={entry_summary} "
                    f"trees={tree_summary} "
                    f"fingerprints={fingerprint_summary}",
                    flush=True,
                )
    if not args.same_book:
        for mode in modes:
            matches[mode] = list(
                message_tree_matches(
                    pooled_entries[mode],
                    include_markers=args.include_markers,
                )
            )
    print("books:", len(books), "loaded:", loaded_count)
    print("failed books:", len(failed_labels))
    for label in failed_labels:
        print("  failed:", label)
    for mode in modes:
        print(f"normalization: {mode}")
        print("candidate entries:", entry_count[mode])
        print("complete message trees:", len(matches[mode]))
        for match in matches[mode]:
            for name, entry in match.by_name().items():
                print(name, entry.source, entry.text)
        if args.repeat_fingerprint:
            print(
                "complete first-family repeat fingerprints:",
                len(fingerprint_matches[mode]),
            )
            for match in fingerprint_matches[mode]:
                print("  block:", repr(match.block))
                print(
                    "    gap30:",
                    len(match.gap30),
                    match.gap30[:5],
                )
                print(
                    "    gap35:",
                    len(match.gap35),
                    match.gap35[:5],
                )
                print(
                    "    inner:",
                    len(match.inner_gap28),
                    match.inner_gap28[:5],
                )
        if args.same_book:
            print("partial tree components:", partial_counts[mode])
            for name, examples in partial_examples[mode].items():
                for label, value in examples:
                    print(f"  {name}: {label}: {value}")


if __name__ == "__main__":
    main()
