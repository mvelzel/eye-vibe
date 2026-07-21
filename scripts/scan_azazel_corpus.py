#!/usr/bin/env python3
"""Scan Azazelin Tähti's Finnish occult articles for literal Eye geometry.

The public sitemap includes the Finnish Corpus Hermeticum XIII and Emerald
Tablet translations already considered individually, plus a bounded corpus of
related Finnish esoteric prose.  Sitemap ``lastmod`` is used only as a public
availability filter; it cannot determine Noita's internal construction date.
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from html.parser import HTMLParser
from urllib.request import Request, urlopen

from eye_mystery.source_fingerprints import (
    first_family_source_matches,
    normalize_source,
)
from eye_mystery.source_message_tree import (
    SourceEntry,
    message_tree_matches,
    message_tree_partials,
)


SITEMAP = "https://www.azazel.fi/wp-sitemap-posts-soa_page_article-1.xml"
USER_AGENT = "Noita-eye-mystery source-geometry research"
XML_NAMESPACE = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


@dataclass(frozen=True)
class SitemapEntry:
    url: str
    last_modified: date | None


class ArticleParser(HTMLParser):
    """Extract block-level prose from the WordPress ``entry-content`` section."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.suppressed = 0
        self.current: list[str] = []
        self.blocks: list[str] = []

    def handle_starttag(self, tag, attrs) -> None:
        classes = (dict(attrs).get("class", "") or "").split()
        if self.depth:
            if tag == "section":
                self.depth += 1
            if tag in {"script", "style", "nav", "form"}:
                self.suppressed += 1
            if tag == "br" and not self.suppressed:
                self._flush()
        elif tag == "section" and "entry-content" in classes:
            self.depth = 1

    def handle_endtag(self, tag) -> None:
        if not self.depth:
            return
        if tag in {"script", "style", "nav", "form"} and self.suppressed:
            self.suppressed -= 1
        if tag in {"p", "li", "h1", "h2", "h3", "h4", "blockquote"}:
            self._flush()
        if tag == "section":
            self.depth -= 1
            if not self.depth:
                self._flush()

    def handle_data(self, data) -> None:
        if self.depth and not self.suppressed:
            self.current.append(data)

    def _flush(self) -> None:
        text = " ".join(" ".join(self.current).split())
        if text:
            self.blocks.append(text)
        self.current.clear()


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    return urlopen(request, timeout=60).read().decode("utf-8", errors="ignore")


def sitemap_entries(source: str) -> tuple[SitemapEntry, ...]:
    root = ET.fromstring(source)
    result = []
    for element in root.findall("s:url", XML_NAMESPACE):
        location = element.findtext("s:loc", namespaces=XML_NAMESPACE)
        modified = element.findtext("s:lastmod", namespaces=XML_NAMESPACE)
        if not location:
            continue
        parsed_date = date.fromisoformat(modified[:10]) if modified else None
        result.append(SitemapEntry(location, parsed_date))
    return tuple(result)


def candidate_entries(
    url: str, blocks: tuple[str, ...], mode: str
) -> tuple[SourceEntry, ...]:
    fragments = set(blocks)
    for block in blocks:
        fragments.update(re.split(r"(?<=[.!?])\s+", block))
    result = []
    for index, fragment in enumerate(fragments):
        normalized = normalize_source(
            fragment, mode=mode, transliterate_finnish=True
        )
        if 90 <= len(normalized) <= 140:
            result.append(SourceEntry(f"{url}#{index}", normalized))
    return tuple(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cutoff",
        type=date.fromisoformat,
        default=None,
        help="retain sitemap lastmod dates on or before YYYY-MM-DD",
    )
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    entries = sitemap_entries(fetch(SITEMAP))
    if args.cutoff is not None:
        entries = tuple(
            entry
            for entry in entries
            if entry.last_modified is not None
            and entry.last_modified <= args.cutoff
        )
    print("sitemap:", SITEMAP)
    print("cutoff:", args.cutoff or "none", "articles:", len(entries))

    articles: dict[str, tuple[str, ...]] = {}
    failures = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(fetch, entry.url): entry for entry in entries}
        for future in as_completed(futures):
            entry = futures[future]
            try:
                source = future.result()
            except Exception as error:  # pragma: no cover - network reporting
                failures.append((entry.url, str(error)))
                continue
            article_parser = ArticleParser()
            article_parser.feed(source)
            articles[entry.url] = tuple(article_parser.blocks)

    print("loaded:", len(articles), "failures:", len(failures))
    for url, error in failures:
        print("  failure:", url, error)

    for mode in ("letters", "spaces"):
        texts = {
            url: normalize_source(
                " ".join(blocks), mode=mode, transliterate_finnish=True
            )
            for url, blocks in articles.items()
        }
        source_entries = tuple(
            source_entry
            for url, blocks in articles.items()
            for source_entry in candidate_entries(url, blocks, mode)
        )
        fingerprints = first_family_source_matches(texts)
        trees = message_tree_matches(source_entries)
        partials = message_tree_partials(source_entries)
        print(
            f"mode={mode} characters={sum(map(len, texts.values()))} "
            f"candidates={len(source_entries)} fingerprints={len(fingerprints)} "
            f"trees={len(trees)}"
        )
        print(
            "  partials:",
            f"upper24={len(partials.upper24)}",
            f"deep20={len(partials.deep20)}",
            f"nested9={len(partials.nested9)}",
            f"lower6={len(partials.lower6)}",
            f"roots={len(partials.roots)}",
        )
        for match in fingerprints:
            print("  fingerprint:", repr(match.block), match.gap30[:1])


if __name__ == "__main__":
    main()
