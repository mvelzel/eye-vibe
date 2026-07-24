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


def apply_position_permutation(
    deck: tuple[int, ...], permutation: tuple[int, ...]
) -> tuple[int, ...]:
    """Reorder a deck; each output position names one previous position."""

    if len(deck) != SIZE or set(permutation) != set(range(SIZE)):
        raise ValueError("expected an 83-position permutation")
    return tuple(deck[position] for position in permutation)


def compose_position_permutations(
    first: tuple[int, ...], second: tuple[int, ...]
) -> tuple[int, ...]:
    """Return the position permutation produced by applying first, then second."""

    return tuple(first[position] for position in second)


def stable_partition_permutation(
    pattern: str, *, reverse: bool, ones_first: bool
) -> tuple[int, ...]:
    """Repeat an authored binary row and collect its two position packets."""

    if set(pattern) != {"0", "1"}:
        raise ValueError("pattern must contain both binary symbols")
    tape = pattern[::-1] if reverse else pattern
    preferred = "1" if ones_first else "0"
    bits = tuple(tape[position % len(tape)] for position in range(SIZE))
    return tuple(
        position
        for symbol in (preferred, "0" if preferred == "1" else "1")
        for position, bit in enumerate(bits)
        if bit == symbol
    )


def circle_base_permutations() -> dict[str, tuple[int, ...]]:
    """Construct the source-fixed cuts and repeated binary partitions."""

    candidates: dict[str, tuple[int, ...]] = {}
    natural = tuple(range(SIZE))
    for width in (17, 20, 24, 32):
        candidates[f"cut+{width}"] = natural[width:] + natural[:width]
        candidates[f"cut-{width}"] = natural[-width:] + natural[:-width]

    patterns = {
        "alternating20": "10101010101010101010",
        "irregular17": "11110111011101110",
    }
    for pattern_name, pattern in patterns.items():
        for reverse in (False, True):
            for ones_first in (False, True):
                direction = "ccw" if reverse else "cw"
                packet = "ones" if ones_first else "zeros"
                candidates[f"{pattern_name}-{direction}-{packet}"] = (
                    stable_partition_permutation(
                        pattern, reverse=reverse, ones_first=ones_first
                    )
                )

    for reverse in (False, True):
        for ones_first in (False, True):
            alternating = stable_partition_permutation(
                patterns["alternating20"], reverse=reverse, ones_first=ones_first
            )
            irregular = stable_partition_permutation(
                patterns["irregular17"], reverse=reverse, ones_first=ones_first
            )
            direction = "ccw" if reverse else "cw"
            packet = "ones" if ones_first else "zeros"
            candidates[f"outside-in-{direction}-{packet}"] = (
                compose_position_permutations(alternating, irregular)
            )

    unique: dict[tuple[int, ...], str] = {}
    for name, permutation in candidates.items():
        unique.setdefault(permutation, name)
    return {name: permutation for permutation, name in unique.items()}


def permutation_powers(permutation: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """Return powers zero through 83 for one position permutation."""

    powers = [tuple(range(SIZE))]
    for _ in range(SIZE):
        powers.append(compose_position_permutations(powers[-1], permutation))
    return tuple(powers)


@dataclass(frozen=True)
class BasePermutationResult:
    base: str
    exponent_mode: str
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


def _decode_base_permutation_line(
    ciphertext: tuple[int, ...],
    powers: tuple[tuple[int, ...], ...],
    exponent_mode: str,
) -> tuple[int, ...]:
    deck = tuple(range(SIZE))
    plaintext = []
    for card in ciphertext:
        rank = deck.index(card)
        plaintext.append(rank)
        if exponent_mode == "fixed":
            exponent = 1
        elif exponent_mode == "rank":
            exponent = rank
        elif exponent_mode == "rank+1":
            exponent = rank + 1
        else:
            raise ValueError(f"unknown exponent mode {exponent_mode!r}")
        deck = apply_position_permutation(deck, powers[exponent])
    return tuple(plaintext)


def circle_base_permutation_audit(
    lines: tuple[tuple[int, ...], ...],
) -> tuple[BasePermutationResult, ...]:
    """Test the frozen cut/partition base permutations and exponent schedules."""

    results = []
    for base_name, permutation in circle_base_permutations().items():
        powers = permutation_powers(permutation)
        for exponent_mode in ("fixed", "rank", "rank+1"):
            decoded = tuple(
                _decode_base_permutation_line(line, powers, exponent_mode)
                for line in lines
            )
            flat = tuple(value for line in decoded for value in line)
            results.append(
                BasePermutationResult(
                    base=base_name,
                    exponent_mode=exponent_mode,
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
