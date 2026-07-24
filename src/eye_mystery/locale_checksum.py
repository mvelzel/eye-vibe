"""Generic calling-code/BWT-region audit of the Eye marker scalar plane."""

from __future__ import annotations

from dataclasses import dataclass
from string import ascii_letters

from eye_mystery.calling_codes import geographic_regions
from eye_mystery.corpus import MESSAGE_ORDER
from eye_mystery.factoradic_headers import (
    base5_digits,
    header_ranks,
    unique_multiset_permutations,
)
from eye_mystery.initials import initial_digits
from eye_mystery.marker_country import (
    BwtReading,
    Grid,
    assignment_bwt_reading,
    assignment_ranks,
    column_sums,
    d4_views,
    is_full_factoradic_event,
    marker_grid,
)


def decimal_column_code(grid: Grid) -> int | None:
    """Parse three single-digit column sums as one padded decimal integer."""

    digits = column_sums(grid)
    if any(digit not in range(10) for digit in digits):
        return None
    return 100 * digits[0] + 10 * digits[1] + digits[2]


def calling_code_views(
    assignment: tuple[int, ...], *, d4: bool
) -> tuple[tuple[int, tuple[int, int, int], tuple[str, ...]], ...]:
    """Return geographic calling codes in the natural or all D4 views."""

    grid = marker_grid(assignment)
    views = d4_views(grid) if d4 else (grid,)
    results = []
    for view in views:
        code = decimal_column_code(view)
        regions = geographic_regions(code) if code is not None else ()
        if regions:
            results.append((code, column_sums(view), regions))
    return tuple(dict.fromkeys(results))


def eligible_region_suffix(reading: BwtReading) -> str | None:
    if reading.text is None or len(reading.text) != 3:
        return None
    suffix = reading.text[1:]
    if any(character not in ascii_letters for character in suffix):
        return None
    return suffix.upper()


def region_matches_code(reading: BwtReading, code: int) -> bool:
    suffix = eligible_region_suffix(reading)
    return suffix is not None and suffix in geographic_regions(code)


@dataclass(frozen=True)
class LocaleMatch:
    assignment: tuple[int, ...]
    natural: bool
    code: int
    digits: tuple[int, int, int]
    regions: tuple[str, ...]
    text: str
    factoradic: bool


@dataclass(frozen=True)
class PlaneSummary:
    coordinate: int
    digits: tuple[int, int, int]
    code: int | None
    regions: tuple[str, ...]


def observed_plane_summaries() -> tuple[PlaneSummary, ...]:
    markers = initial_digits()
    output = []
    for coordinate in range(3):
        assignment = tuple(marker[coordinate] for marker in markers)
        grid = marker_grid(assignment)
        digits = column_sums(grid)
        code = decimal_column_code(grid)
        output.append(
            PlaneSummary(
                coordinate,
                digits,
                code,
                geographic_regions(code) if code is not None else (),
            )
        )
    return tuple(output)


@dataclass(frozen=True)
class LocaleChecksumAudit:
    all_assignments: int
    in_range: int
    distinct_ranks: int
    natural_geographic_code: int
    d4_geographic_code: int
    bwt_letter_suffix: int
    natural_semantic_match: int
    natural_bang_match: int
    d4_semantic_match: int
    d4_bang_match: int
    full_factoradic: int
    full_natural_semantic_match: int
    full_d4_semantic_match: int
    matches: tuple[LocaleMatch, ...]


def locale_checksum_audit() -> LocaleChecksumAudit:
    labels = tuple(base5_digits(header_ranks()[name])[2] for name in MESSAGE_ORDER)
    counts = {
        "all": 0,
        "in_range": 0,
        "distinct": 0,
        "natural_code": 0,
        "d4_code": 0,
        "letter_suffix": 0,
        "natural_match": 0,
        "natural_bang": 0,
        "d4_match": 0,
        "d4_bang": 0,
        "full": 0,
        "full_natural": 0,
        "full_d4": 0,
    }
    matches = []

    for assignment in unique_multiset_permutations(labels):
        counts["all"] += 1
        ranks = assignment_ranks(assignment)
        if max(ranks.values()) > 82:
            continue
        counts["in_range"] += 1
        if len(set(ranks.values())) != 9:
            continue
        counts["distinct"] += 1

        reading = assignment_bwt_reading(assignment)
        suffix = eligible_region_suffix(reading)
        natural_views = calling_code_views(assignment, d4=False)
        broad_views = calling_code_views(assignment, d4=True)
        natural_matches = tuple(
            view for view in natural_views if region_matches_code(reading, view[0])
        )
        broad_matches = tuple(
            view for view in broad_views if region_matches_code(reading, view[0])
        )
        natural_match = bool(natural_matches)
        broad_match = bool(broad_matches)
        counts["natural_code"] += bool(natural_views)
        counts["d4_code"] += bool(broad_views)
        counts["letter_suffix"] += suffix is not None
        counts["natural_match"] += natural_match
        counts["natural_bang"] += (
            natural_match
            and reading.text is not None
            and reading.text.startswith("!")
        )
        counts["d4_match"] += broad_match
        counts["d4_bang"] += (
            broad_match
            and reading.text is not None
            and reading.text.startswith("!")
        )

        factoradic = is_full_factoradic_event(ranks)
        counts["full"] += factoradic
        counts["full_natural"] += factoradic and natural_match
        counts["full_d4"] += factoradic and broad_match
        for code, digits, regions in broad_matches:
            matches.append(
                LocaleMatch(
                    assignment=assignment,
                    natural=(code, digits, regions) in natural_matches,
                    code=code,
                    digits=digits,
                    regions=regions,
                    text=reading.text or "",
                    factoradic=factoradic,
                )
            )

    return LocaleChecksumAudit(
        all_assignments=counts["all"],
        in_range=counts["in_range"],
        distinct_ranks=counts["distinct"],
        natural_geographic_code=counts["natural_code"],
        d4_geographic_code=counts["d4_code"],
        bwt_letter_suffix=counts["letter_suffix"],
        natural_semantic_match=counts["natural_match"],
        natural_bang_match=counts["natural_bang"],
        d4_semantic_match=counts["d4_match"],
        d4_bang_match=counts["d4_bang"],
        full_factoradic=counts["full"],
        full_natural_semantic_match=counts["full_natural"],
        full_d4_semantic_match=counts["full_d4"],
        matches=tuple(matches),
    )
