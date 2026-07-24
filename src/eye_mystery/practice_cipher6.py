"""Finite paired-deck audit for sdlwdr Practice Cipher #6."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from eye_mystery.chaocipher import decrypt


SIZE = 83
EXPECTED_PREFIXES = tuple(range(27, 36))
NADIRS = (17, 20, 24, 32, 41, 42)
NATURAL_PLAINTEXT = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .\n,?-"
ALTAR_LETTERS = "BDMAGICKEFHJLNOPQRSTUVWXYZ"


def read_ciphertext(path: Path) -> tuple[tuple[int, ...], ...]:
    """Read the nine printable-ASCII lines as zero-based card labels."""

    lines = path.read_text().splitlines()
    if len(lines) != 9:
        raise ValueError(f"expected nine lines, got {len(lines)}")
    values = tuple(tuple(ord(character) - 33 for character in line) for line in lines)
    if any(not 0 <= value < SIZE for line in values for value in line):
        raise ValueError("ciphertext contains a card outside ASCII 33..115")
    return values


def keyed_deck(keyword: str) -> tuple[int, ...]:
    """Construct an 83-card deck by keying A=0..Z=25, then appending cards."""

    front: list[int] = []
    for character in keyword.upper():
        if not "A" <= character <= "Z":
            continue
        value = ord(character) - ord("A")
        if value not in front:
            front.append(value)
    return tuple(front + [value for value in range(SIZE) if value not in front])


def candidate_decks() -> dict[str, tuple[int, ...]]:
    """Return only source-fixed initial orders admitted by the frozen lane."""

    return {
        "natural": tuple(range(SIZE)),
        "trailer": keyed_deck(ALTAR_LETTERS),
        "card-trick": keyed_deck("A BAD MAGIC CARD TRICK"),
        "outer-gap-cw": keyed_deck("KMGIC"),
        "outer-gap-ccw": keyed_deck("CIGMK"),
        "outer-cycle-cw": keyed_deck("MGICK"),
        "outer-cycle-ccw": keyed_deck("KCIGM"),
        "inner-cw": keyed_deck("MAGICK"),
        "inner-ccw": keyed_deck("KCGIAM"),
    }


@dataclass(frozen=True)
class PairedDeckResult:
    left: str
    right: str
    nadir: int
    prefix_matches: int
    low_rank_count: int
    total: int
    distinct: int
    maximum: int
    decoded: tuple[tuple[int, ...], ...]

    @property
    def low_rank_fraction(self) -> float:
        return self.low_rank_count / self.total

    @property
    def key(self) -> tuple[int, int, int, int]:
        return (
            self.prefix_matches,
            self.low_rank_count,
            -self.maximum,
            -self.distinct,
        )


def paired_deck_audit(
    lines: tuple[tuple[int, ...], ...],
) -> tuple[PairedDeckResult, ...]:
    """Enumerate the frozen generalized-Chaocipher initial pairs and nadirs."""

    decks = candidate_decks()
    results = []
    for left_name, left in decks.items():
        for right_name, right in decks.items():
            for nadir in NADIRS:
                decoded = tuple(
                    decrypt(line, left, right, nadir=nadir) for line in lines
                )
                flat = tuple(value for line in decoded for value in line)
                results.append(
                    PairedDeckResult(
                        left=left_name,
                        right=right_name,
                        nadir=nadir,
                        prefix_matches=sum(
                            line[0] == expected
                            for line, expected in zip(decoded, EXPECTED_PREFIXES)
                        ),
                        low_rank_count=sum(value < len(NATURAL_PLAINTEXT) for value in flat),
                        total=len(flat),
                        distinct=len(set(flat)),
                        maximum=max(flat),
                        decoded=decoded,
                    )
                )
    return tuple(sorted(results, key=lambda result: result.key, reverse=True))


def render_line(values: Iterable[int], *, altar: bool = False) -> str:
    """Render recovered low ranks under the two fixed plaintext alphabets."""

    letters = ALTAR_LETTERS if altar else "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet = letters + NATURAL_PLAINTEXT[26:]
    return "".join(alphabet[value] if value < len(alphabet) else "¤" for value in values)

