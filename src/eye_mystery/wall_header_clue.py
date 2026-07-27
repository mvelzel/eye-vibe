"""Audit the Wall-message count/header and context-selection hypothesis.

This module keeps the hypothesis deliberately small.  It tests the exact
``50, 63, 33`` count correspondence and the sixteen immediate context reads
obtained from four natural message orders, two indexing origins, and two
directions.  It does not fit arbitrary word classes or score language.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction

from .checksum_self_pointer import MESSAGES_UNDER_TEST, ODD_EAST_HEADERS
from .corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from .isomorphs import pattern
from .wall_83_masks import (
    ASSET_XML_ORDER,
    THAT_WHICH_WINDOWS,
    WORLD_VERTICAL_ORDER,
)
from .wall_baconian import WallWord, tokenize_wall


OMITTED_YOU_SITES = (
    ("G12", 0, "Why else would be here?"),
    ("G12", 1, "Why else would be reading this?"),
)


@dataclass(frozen=True)
class WallHeaderCounts:
    periods: int
    literal_you: int
    omitted_you: int
    repaired_you: int
    questions: int
    expanded_you: int

    @property
    def header_tuple(self) -> tuple[int, int, int]:
        return self.periods, self.repaired_you, self.questions


@dataclass(frozen=True)
class OddEastChecksum:
    message: str
    header: int
    total: int
    quotient: int
    remainder: int


@dataclass(frozen=True)
class YouContext:
    zero_index: int
    map_id: str
    token: str
    previous: str | None
    following: str | None


@dataclass(frozen=True)
class ContextRead:
    order_name: str
    indexing: str
    direction: str
    indices: tuple[int, int, int]
    words: tuple[str, str, str]
    contexts: tuple[YouContext, YouContext, YouContext]

    @property
    def phrase(self) -> str:
        return " ".join(word.upper() for word in self.words)


@dataclass(frozen=True)
class DirectTableAudit:
    field: str
    unique_outputs: int
    window_patterns: tuple[str, ...]
    expected_pattern: str
    preserved_windows: int
    common_pattern: bool
    message_prefixes: tuple[tuple[str, tuple[str, ...]], ...]


def wall_header_counts(
    lines_by_id: Mapping[str, Sequence[str]],
) -> WallHeaderCounts:
    """Return the frozen visible counts and the two explicit G12 repairs."""

    text = "\n".join(
        line
        for map_id in WORLD_VERTICAL_ORDER
        for line in lines_by_id[map_id]
    )
    words = tuple(
        word
        for map_id in WORLD_VERTICAL_ORDER
        for word in tokenize_wall(map_id, lines_by_id[map_id])
    )
    literal_you = sum(word.normalized == "you" for word in words)
    expanded_you = sum(
        word.normalized.startswith("you")
        for word in words
    )
    for map_id, line_index, expected_fragment in OMITTED_YOU_SITES:
        if expected_fragment not in lines_by_id[map_id][line_index]:
            raise ValueError(f"omitted-YOU site changed: {map_id}:{line_index}")
    omitted_you = len(OMITTED_YOU_SITES)
    return WallHeaderCounts(
        periods=text.count("."),
        literal_you=literal_you,
        omitted_you=omitted_you,
        repaired_you=literal_you + omitted_you,
        questions=text.count("?"),
        expanded_you=expanded_you,
    )


def odd_east_checksums() -> tuple[OddEastChecksum, ...]:
    """Return the three independently established mod-101 checksum records."""

    records = []
    for message, expected_header in zip(
        MESSAGES_UNDER_TEST,
        ODD_EAST_HEADERS,
        strict=True,
    ):
        values = trigram_values(MESSAGES[message])
        total = sum(values)
        quotient, remainder = divmod(total, 101)
        if values[0] != expected_header:
            raise ValueError(f"{message}: unexpected initial glyph")
        records.append(
            OddEastChecksum(
                message,
                values[0],
                total,
                quotient,
                remainder,
            )
        )
    return tuple(records)


def ordered_words(
    lines_by_id: Mapping[str, Sequence[str]],
    order: Sequence[str],
) -> tuple[WallWord, ...]:
    return tuple(
        word
        for map_id in order
        for word in tokenize_wall(map_id, lines_by_id[map_id])
    )


def expanded_you_contexts(
    lines_by_id: Mapping[str, Sequence[str]],
    order: Sequence[str],
) -> tuple[YouContext, ...]:
    """Return the 83 ``you*`` tokens and their immediate word contexts."""

    words = ordered_words(lines_by_id, order)
    result = []
    for word_index, word in enumerate(words):
        if not word.normalized.startswith("you"):
            continue
        result.append(
            YouContext(
                zero_index=len(result),
                map_id=word.map_id,
                token=word.normalized,
                previous=(
                    words[word_index - 1].normalized
                    if word_index
                    else None
                ),
                following=(
                    words[word_index + 1].normalized
                    if word_index + 1 < len(words)
                    else None
                ),
            )
        )
    if len(result) != 83:
        raise ValueError(f"expected 83 expanded-YOU tokens, got {len(result)}")
    return tuple(result)


def context_read(
    lines_by_id: Mapping[str, Sequence[str]],
    order: Sequence[str],
    *,
    order_name: str,
    one_based: bool,
    following: bool,
) -> ContextRead:
    contexts = expanded_you_contexts(lines_by_id, order)
    indices = tuple(
        header - int(one_based)
        for header in ODD_EAST_HEADERS
    )
    selected = tuple(contexts[index] for index in indices)
    maybe_words = tuple(
        context.following if following else context.previous
        for context in selected
    )
    if any(word is None for word in maybe_words):
        raise ValueError("selected expanded-YOU token lacks requested context")
    words = maybe_words
    return ContextRead(
        order_name=order_name,
        indexing="one-based" if one_based else "zero-based",
        direction="following" if following else "previous",
        indices=indices,  # type: ignore[arg-type]
        words=words,  # type: ignore[arg-type]
        contexts=selected,  # type: ignore[arg-type]
    )


def natural_context_reads(
    lines_by_id: Mapping[str, Sequence[str]],
) -> tuple[ContextRead, ...]:
    """Return the frozen 4x2x2 sensitivity family."""

    orders = (
        ("world-y", WORLD_VERTICAL_ORDER),
        ("reverse-world-y", tuple(reversed(WORLD_VERTICAL_ORDER))),
        ("asset-xml", ASSET_XML_ORDER),
        ("reverse-asset-xml", tuple(reversed(ASSET_XML_ORDER))),
    )
    return tuple(
        context_read(
            lines_by_id,
            order,
            order_name=order_name,
            one_based=one_based,
            following=following,
        )
        for order_name, order in orders
        for one_based in (False, True)
        for following in (False, True)
    )


def fixed_ordered_word_probability(
    lines_by_id: Mapping[str, Sequence[str]],
    target: Sequence[str],
) -> Fraction:
    """Descriptive probability for a fixed ordered target under permutation.

    This is not a discovery p-value: ``AND CREATED GOD`` was noticed before
    the target was frozen.  It only reports the exact multiset calculation.
    """

    contexts = expanded_you_contexts(lines_by_id, WORLD_VERTICAL_ORDER)
    if any(context.previous is None for context in contexts):
        raise ValueError("fixed world-Y order lacks a previous context")
    counts = Counter(context.previous for context in contexts)
    remaining = len(contexts)
    probability = Fraction(1, 1)
    used: Counter[str] = Counter()
    for raw_word in target:
        word = raw_word.lower()
        probability *= Fraction(counts[word] - used[word], remaining)
        used[word] += 1
        remaining -= 1
    return probability


def direct_context_table_audit(
    lines_by_id: Mapping[str, Sequence[str]],
    *,
    field: str = "previous",
    prefix_length: int = 25,
) -> DirectTableAudit:
    """Apply one 83-entry context field to every canonical Eye value.

    This is the most literal consumer of the proposed Wall table.  It tests
    the accepted trigram stream directly and reports whether the fixed
    ``THAT WHICH`` equality signature survives the table's collisions.
    """

    if field not in {"previous", "following", "token"}:
        raise ValueError(f"unsupported context field: {field}")
    contexts = expanded_you_contexts(lines_by_id, WORLD_VERTICAL_ORDER)
    table = tuple(getattr(context, field) for context in contexts)
    if any(value is None for value in table):
        raise ValueError(f"{field} table contains a missing boundary context")
    expected_patterns = {
        pattern(values)
        for _, values in THAT_WHICH_WINDOWS
    }
    if len(expected_patterns) != 1:
        raise ValueError("canonical THAT-WHICH windows lost their shared pattern")
    expected_pattern = next(iter(expected_patterns))
    window_patterns = tuple(
        pattern(tuple(table[value] for value in values))
        for _, values in THAT_WHICH_WINDOWS
    )
    return DirectTableAudit(
        field=field,
        unique_outputs=len(set(table)),
        window_patterns=window_patterns,
        expected_pattern=expected_pattern,
        preserved_windows=sum(
            candidate == expected_pattern
            for candidate in window_patterns
        ),
        common_pattern=len(set(window_patterns)) == 1,
        message_prefixes=tuple(
            (
                message,
                tuple(
                    table[value]  # type: ignore[misc]
                    for value in trigram_values(MESSAGES[message])[:prefix_length]
                ),
            )
            for message in MESSAGE_ORDER
        ),
    )
