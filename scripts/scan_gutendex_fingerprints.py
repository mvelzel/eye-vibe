#!/usr/bin/env python3
"""Scan a bounded Finnish Gutenberg query for the Eye repeat fingerprint."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from eye_mystery.source_fingerprints import (
    first_family_source_matches,
    gap_repeats,
    normalize_source,
)


USER_AGENT = "Noita-eye-mystery research"


def fetch(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    return urlopen(request, timeout=90).read()


def catalog(search: str, max_books: int) -> list[dict[str, object]]:
    url: str | None = "https://gutendex.com/books/?" + urlencode(
        {"languages": "fi", "search": search}
    )
    books = []
    while url is not None and len(books) < max_books:
        page = json.loads(fetch(url))
        books.extend(page["results"])
        url = page["next"]
    return books[:max_books]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", required=True)
    parser.add_argument("--max-books", type=int, default=100)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--mode", choices=("letters", "spaces"), default="letters")
    args = parser.parse_args()

    books = catalog(args.search, args.max_books)

    def load(book: dict[str, object]) -> tuple[str, str] | None:
        formats = book["formats"]
        assert isinstance(formats, dict)
        url = formats.get("text/plain; charset=utf-8")
        if not isinstance(url, str):
            return None
        title = str(book["title"])
        text = fetch(url).decode("utf-8", errors="ignore")
        return (
            f"{book['id']}: {title}",
            normalize_source(
                text,
                args.mode,
                transliterate_finnish=True,
            ),
        )

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        loaded = tuple(executor.map(load, books))
    texts = dict(item for item in loaded if item is not None)
    print(
        "catalog books:",
        len(books),
        "plain texts:",
        len(texts),
        "normalized characters:",
        sum(map(len, texts.values())),
    )
    for length, gap in ((18, 30), (18, 35), (9, 28)):
        count = sum(
            len(positions)
            for text in texts.values()
            for positions in gap_repeats(text, length=length, gap=gap).values()
        )
        print(f"length={length} gap={gap} repeat pairs={count}")
    matches = first_family_source_matches(texts)
    print("complete first-family fingerprints:", len(matches))
    for match in matches:
        print(repr(match.block))
        print("  gap30:", match.gap30[:5])
        print("  gap35:", match.gap35[:5])
        print("  inner:", match.inner_gap28[:5])


if __name__ == "__main__":
    main()
