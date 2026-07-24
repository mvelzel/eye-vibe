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
CARD_TRICK_LETTERS = "ABDMGICRTKEFHJLNOPQSUVWXYZ"
TRAILER_PHRASE = "A BAD MAGIC CARD TRICK"
ZERO_BAND = "0" * 24
ALTERNATING_BAND = "10101010101010101010"
IRREGULAR_BAND = "11110111011101110"


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


def asset_tape(*, reverse_binary: bool) -> str:
    """Join the 22-character community phrase to the 61 binary circle marks."""

    alternating = ALTERNATING_BAND[::-1] if reverse_binary else ALTERNATING_BAND
    irregular = IRREGULAR_BAND[::-1] if reverse_binary else IRREGULAR_BAND
    tape = TRAILER_PHRASE + ZERO_BAND + alternating + irregular
    if len(tape) != SIZE:
        raise AssertionError("joint asset tape must contain exactly 83 symbols")
    return tape


def tape_symbol_order(tape: str, *, first_occurrence: bool) -> tuple[str, ...]:
    """Return one of the two fixed collations admitted by the tape freeze."""

    return (
        tuple(dict.fromkeys(tape))
        if first_occurrence
        else tuple(sorted(set(tape)))
    )


def stable_tape_permutation(
    tape: str, symbol_order: tuple[str, ...]
) -> tuple[int, ...]:
    """Stable-sort tape positions by one fixed symbol collation."""

    rank = {symbol: index for index, symbol in enumerate(symbol_order)}
    return tuple(sorted(range(SIZE), key=lambda position: rank[tape[position]]))


def cyclic_tape_permutation(
    tape: str, symbol_order: tuple[str, ...]
) -> tuple[int, ...]:
    """Order the starting positions of all cyclic rotations lexicographically."""

    rank = {symbol: index for index, symbol in enumerate(symbol_order)}
    return tuple(
        sorted(
            range(SIZE),
            key=lambda position: tuple(
                rank[tape[(position + offset) % SIZE]] for offset in range(SIZE)
            ),
        )
    )


def asset_tape_base_permutations() -> dict[str, tuple[int, ...]]:
    """Construct stable and cyclic deck orders from the exact 83-slot tape."""

    candidates: dict[str, tuple[int, ...]] = {}
    for reverse_binary in (False, True):
        tape = asset_tape(reverse_binary=reverse_binary)
        direction = "ccw" if reverse_binary else "cw"
        for first_occurrence in (False, True):
            order = tape_symbol_order(tape, first_occurrence=first_occurrence)
            collation = "first" if first_occurrence else "natural"
            candidates[f"stable-{direction}-{collation}"] = stable_tape_permutation(
                tape, order
            )
            candidates[f"cyclic-{direction}-{collation}"] = cyclic_tape_permutation(
                tape, order
            )
    unique: dict[tuple[int, ...], str] = {}
    for name, permutation in candidates.items():
        unique.setdefault(permutation, name)
    return {name: permutation for permutation, name in unique.items()}


def asset_tape_base_audit(
    lines: tuple[tuple[int, ...], ...],
) -> tuple[BasePermutationResult, ...]:
    """Test the frozen stable/cyclic permutations of the 83-slot asset tape."""

    results = []
    for base_name, permutation in asset_tape_base_permutations().items():
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


@dataclass(frozen=True)
class TapeClassCutResult:
    binary_direction: str
    collation: str
    one_based: bool
    cut_direction: str
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


def _decode_tape_class_cut_line(
    ciphertext: tuple[int, ...],
    tape: str,
    class_rank: dict[str, int],
    *,
    one_based: bool,
    cut_right: bool,
) -> tuple[int, ...]:
    deck = tuple(range(SIZE))
    plaintext = []
    for card in ciphertext:
        rank = deck.index(card)
        plaintext.append(rank)
        distance = class_rank[tape[rank]] + int(one_based)
        if cut_right:
            distance = -distance
        distance %= SIZE
        deck = deck[distance:] + deck[:distance]
    return tuple(plaintext)


def tape_class_cut_audit(
    lines: tuple[tuple[int, ...], ...],
) -> tuple[TapeClassCutResult, ...]:
    """Test the frozen 13-symbol first-N cut quotient of the joint asset tape."""

    results = []
    for reverse_binary in (False, True):
        tape = asset_tape(reverse_binary=reverse_binary)
        binary_direction = "ccw" if reverse_binary else "cw"
        for first_occurrence in (False, True):
            order = tape_symbol_order(tape, first_occurrence=first_occurrence)
            class_rank = {symbol: index for index, symbol in enumerate(order)}
            collation = "first" if first_occurrence else "natural"
            for one_based in (False, True):
                for cut_right in (False, True):
                    decoded = tuple(
                        _decode_tape_class_cut_line(
                            line,
                            tape,
                            class_rank,
                            one_based=one_based,
                            cut_right=cut_right,
                        )
                        for line in lines
                    )
                    flat = tuple(value for line in decoded for value in line)
                    results.append(
                        TapeClassCutResult(
                            binary_direction=binary_direction,
                            collation=collation,
                            one_based=one_based,
                            cut_direction="right" if cut_right else "left",
                            prefix_matches=sum(
                                line[0] == expected
                                for line, expected in zip(decoded, EXPECTED_PREFIXES)
                            ),
                            low_rank_count=sum(
                                value < len(NATURAL_PLAINTEXT) for value in flat
                            ),
                            total=len(flat),
                            distinct=len(set(flat)),
                            maximum=max(flat),
                            decoded=decoded,
                        )
                    )
    return tuple(sorted(results, key=lambda result: result.key, reverse=True))


@dataclass(frozen=True)
class TapeValueCutResult:
    binary_direction: str
    alphabet: str
    appended_nonletters: bool
    one_based: bool
    cut_direction: str
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


def tape_value_map(
    letters: str, *, appended_nonletters: bool
) -> dict[str, int]:
    """Map tape symbols through one fixed altar-derived alphabet convention."""

    mapping = {symbol: index for index, symbol in enumerate(letters)}
    if appended_nonletters:
        mapping.update({str(digit): 26 + digit for digit in range(10)})
        mapping[" "] = 36
    else:
        mapping.update({"0": 0, "1": 1, " ": 0})
    return mapping


def _decode_tape_value_cut_line(
    ciphertext: tuple[int, ...],
    tape: str,
    values: dict[str, int],
    *,
    one_based: bool,
    cut_right: bool,
) -> tuple[int, ...]:
    deck = tuple(range(SIZE))
    plaintext = []
    for card in ciphertext:
        rank = deck.index(card)
        plaintext.append(rank)
        distance = values[tape[rank]] + int(one_based)
        if cut_right:
            distance = -distance
        distance %= SIZE
        deck = deck[distance:] + deck[:distance]
    return tuple(plaintext)


def tape_value_cut_audit(
    lines: tuple[tuple[int, ...], ...],
) -> tuple[TapeValueCutResult, ...]:
    """Test the frozen altar-valued first-N cut family."""

    results = []
    alphabets = {
        "trailer": ALTAR_LETTERS,
        "card-trick": CARD_TRICK_LETTERS,
    }
    for reverse_binary in (False, True):
        tape = asset_tape(reverse_binary=reverse_binary)
        binary_direction = "ccw" if reverse_binary else "cw"
        for alphabet_name, letters in alphabets.items():
            for appended_nonletters in (False, True):
                values = tape_value_map(
                    letters, appended_nonletters=appended_nonletters
                )
                for one_based in (False, True):
                    for cut_right in (False, True):
                        decoded = tuple(
                            _decode_tape_value_cut_line(
                                line,
                                tape,
                                values,
                                one_based=one_based,
                                cut_right=cut_right,
                            )
                            for line in lines
                        )
                        flat = tuple(value for line in decoded for value in line)
                        results.append(
                            TapeValueCutResult(
                                binary_direction=binary_direction,
                                alphabet=alphabet_name,
                                appended_nonletters=appended_nonletters,
                                one_based=one_based,
                                cut_direction="right" if cut_right else "left",
                                prefix_matches=sum(
                                    line[0] == expected
                                    for line, expected in zip(
                                        decoded, EXPECTED_PREFIXES
                                    )
                                ),
                                low_rank_count=sum(
                                    value < len(NATURAL_PLAINTEXT)
                                    for value in flat
                                ),
                                total=len(flat),
                                distinct=len(set(flat)),
                                maximum=max(flat),
                                decoded=decoded,
                            )
                        )
    return tuple(sorted(results, key=lambda result: result.key, reverse=True))


@dataclass(frozen=True)
class CiphertextAutokeyResult:
    initial_deck: str
    key_source: str
    alignment_mode: str
    one_based: bool
    cut_direction: str
    binary_direction: str | None
    value_alphabet: str | None
    appended_nonletters: bool | None
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


def _decode_ciphertext_autokey_line(
    ciphertext: tuple[int, ...],
    initial_deck: tuple[int, ...],
    key_values: tuple[int, ...],
    *,
    cumulative: bool,
    one_based: bool,
    cut_right: bool,
) -> tuple[int, ...]:
    deck = initial_deck
    plaintext = []
    for card in ciphertext:
        plaintext.append(deck.index(card))
        distance = key_values[card] + int(one_based)
        if cut_right:
            distance = -distance
        distance %= SIZE
        source = deck if cumulative else initial_deck
        deck = source[distance:] + source[:distance]
    return tuple(plaintext)


def ciphertext_autokey_audit(
    lines: tuple[tuple[int, ...], ...],
) -> tuple[CiphertextAutokeyResult, ...]:
    """Test the frozen raw and asset-valued 83-card ciphertext autokeys."""

    initial_decks = {
        "natural": tuple(range(SIZE)),
        "trailer": keyed_deck(ALTAR_LETTERS),
        "card-trick": keyed_deck(CARD_TRICK_LETTERS),
    }
    results = []

    def add_family(
        *,
        key_source: str,
        key_values: tuple[int, ...],
        binary_direction: str | None,
        value_alphabet: str | None,
        appended_nonletters: bool | None,
    ) -> None:
        for initial_name, initial_deck in initial_decks.items():
            for cumulative in (False, True):
                for one_based in (False, True):
                    for cut_right in (False, True):
                        decoded = tuple(
                            _decode_ciphertext_autokey_line(
                                line,
                                initial_deck,
                                key_values,
                                cumulative=cumulative,
                                one_based=one_based,
                                cut_right=cut_right,
                            )
                            for line in lines
                        )
                        flat = tuple(value for line in decoded for value in line)
                        results.append(
                            CiphertextAutokeyResult(
                                initial_deck=initial_name,
                                key_source=key_source,
                                alignment_mode=(
                                    "cumulative" if cumulative else "absolute"
                                ),
                                one_based=one_based,
                                cut_direction="right" if cut_right else "left",
                                binary_direction=binary_direction,
                                value_alphabet=value_alphabet,
                                appended_nonletters=appended_nonletters,
                                prefix_matches=sum(
                                    line[0] == expected
                                    for line, expected in zip(
                                        decoded, EXPECTED_PREFIXES
                                    )
                                ),
                                low_rank_count=sum(
                                    value < len(NATURAL_PLAINTEXT)
                                    for value in flat
                                ),
                                total=len(flat),
                                distinct=len(set(flat)),
                                maximum=max(flat),
                                decoded=decoded,
                            )
                        )

    add_family(
        key_source="raw",
        key_values=tuple(range(SIZE)),
        binary_direction=None,
        value_alphabet=None,
        appended_nonletters=None,
    )

    alphabets = {
        "trailer": ALTAR_LETTERS,
        "card-trick": CARD_TRICK_LETTERS,
    }
    for reverse_binary in (False, True):
        tape = asset_tape(reverse_binary=reverse_binary)
        binary_direction = "ccw" if reverse_binary else "cw"
        for alphabet_name, letters in alphabets.items():
            for appended_nonletters in (False, True):
                values = tape_value_map(
                    letters, appended_nonletters=appended_nonletters
                )
                add_family(
                    key_source="asset-tape",
                    key_values=tuple(values[symbol] for symbol in tape),
                    binary_direction=binary_direction,
                    value_alphabet=alphabet_name,
                    appended_nonletters=appended_nonletters,
                )

    return tuple(sorted(results, key=lambda result: result.key, reverse=True))


FULL_CIRCLE_SCHEDULES = (
    "sum",
    "outer-minus-inner",
    "inner-minus-outer",
    "alternating-select",
    "irregular-select",
    "alternating-sign-sum",
    "irregular-sign-sum",
    "split-sign",
)


def full_circle_steps(
    schedule: str, *, reverse: bool, plus_one: bool
) -> tuple[int, ...]:
    """Build one 83-tick step tape from all four nonconstant circle rows."""

    outer_letters = "KMGIC"
    inner_letters = "MAGICK"
    alternating = ALTERNATING_BAND
    irregular = IRREGULAR_BAND
    if reverse:
        outer_letters = outer_letters[::-1]
        inner_letters = inner_letters[::-1]
        alternating = alternating[::-1]
        irregular = irregular[::-1]
    letter_values = {symbol: index for index, symbol in enumerate(ALTAR_LETTERS)}
    steps = []
    for tick in range(SIZE):
        outer = letter_values[outer_letters[tick % len(outer_letters)]]
        inner = letter_values[inner_letters[tick % len(inner_letters)]]
        alternating_bit = int(alternating[tick % len(alternating)])
        irregular_bit = int(irregular[tick % len(irregular)])
        if schedule == "sum":
            step = outer + inner
        elif schedule == "outer-minus-inner":
            step = outer - inner
        elif schedule == "inner-minus-outer":
            step = inner - outer
        elif schedule == "alternating-select":
            step = outer if alternating_bit else inner
        elif schedule == "irregular-select":
            step = outer if irregular_bit else inner
        elif schedule == "alternating-sign-sum":
            step = (1 if alternating_bit else -1) * (outer + inner)
        elif schedule == "irregular-sign-sum":
            step = (1 if irregular_bit else -1) * (outer + inner)
        elif schedule == "split-sign":
            step = (
                (1 if alternating_bit else -1) * outer
                + (1 if irregular_bit else -1) * inner
            )
        else:
            raise ValueError(f"unknown full-circle schedule {schedule!r}")
        steps.append((step + int(plus_one)) % SIZE)
    return tuple(steps)


@dataclass(frozen=True)
class FullCircleClockResult:
    initial_deck: str
    schedule: str
    physical_direction: str
    alignment_mode: str
    plus_one: bool
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


def _decode_full_circle_clock_line(
    ciphertext: tuple[int, ...],
    initial_deck: tuple[int, ...],
    steps: tuple[int, ...],
    *,
    cumulative: bool,
) -> tuple[int, ...]:
    deck = initial_deck
    plaintext = []
    for tick, card in enumerate(ciphertext):
        plaintext.append(deck.index(card))
        distance = steps[tick % len(steps)]
        source = deck if cumulative else initial_deck
        deck = source[distance:] + source[:distance]
    return tuple(plaintext)


def full_circle_clock_audit(
    lines: tuple[tuple[int, ...], ...],
) -> tuple[FullCircleClockResult, ...]:
    """Test the frozen time-driven four-ring rotating-disk family."""

    initial_decks = {
        "natural": tuple(range(SIZE)),
        "trailer": keyed_deck(ALTAR_LETTERS),
        "card-trick": keyed_deck(CARD_TRICK_LETTERS),
    }
    results = []
    for schedule in FULL_CIRCLE_SCHEDULES:
        for reverse in (False, True):
            physical_direction = "ccw" if reverse else "cw"
            for plus_one in (False, True):
                steps = full_circle_steps(
                    schedule, reverse=reverse, plus_one=plus_one
                )
                for initial_name, initial_deck in initial_decks.items():
                    for cumulative in (False, True):
                        decoded = tuple(
                            _decode_full_circle_clock_line(
                                line,
                                initial_deck,
                                steps,
                                cumulative=cumulative,
                            )
                            for line in lines
                        )
                        flat = tuple(value for line in decoded for value in line)
                        results.append(
                            FullCircleClockResult(
                                initial_deck=initial_name,
                                schedule=schedule,
                                physical_direction=physical_direction,
                                alignment_mode=(
                                    "cumulative" if cumulative else "absolute"
                                ),
                                plus_one=plus_one,
                                prefix_matches=sum(
                                    line[0] == expected
                                    for line, expected in zip(
                                        decoded, EXPECTED_PREFIXES
                                    )
                                ),
                                low_rank_count=sum(
                                    value < len(NATURAL_PLAINTEXT)
                                    for value in flat
                                ),
                                total=len(flat),
                                distinct=len(set(flat)),
                                maximum=max(flat),
                                decoded=decoded,
                            )
                        )
    return tuple(sorted(results, key=lambda result: result.key, reverse=True))
