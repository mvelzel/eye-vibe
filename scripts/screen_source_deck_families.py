#!/usr/bin/env python3
"""Screen source-selected initial orders under small adaptive-deck machines.

This is deliberately a finite, predeclared family, not a plaintext search.  A
candidate has to be selected from an in-game/authoring source before it sees
the Eye output.  Each candidate is run through the small deck transitions
already used in the repository, in both natural directions.  The report
records exact equality-isomorph preservation and literal re-syncs, with the
final registered context held out from the headline score.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from pathlib import Path

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.deck import (
    move_to_back_decode,
    move_to_front_decode,
    ranks_to_labels,
    reverse_prefix_decode,
    rotate_to_front_decode,
    swap_with_front_decode,
    transpose_decode,
)
from eye_mystery.ninth_causal import CONTEXT_SPECS, equality_signature
from eye_mystery.noita_lore import ORB_LORE_KEYS


ROOT = Path(__file__).resolve().parents[1]
ASCII_SIZE = 83


def keyed_ascii(text: str) -> tuple[int, ...]:
    """First-occurrence keying over the engine's ASCII+32 83-card prefix."""

    key: list[int] = []
    for char in text.upper():
        card = ord(char) - 32
        if 0 <= card < ASCII_SIZE and card not in key:
            key.append(card)
    return tuple(key + [card for card in range(ASCII_SIZE) if card not in key])


def source_first_letters(text: str) -> tuple[int, ...]:
    """Key by first occurrence of ASCII letters in a source text."""

    return keyed_ascii("".join(char for char in text.upper() if "A" <= char <= "Z"))


PERIODIC_NAMES = """
hydrogen helium lithium beryllium boron carbon nitrogen oxygen fluorine neon
sodium magnesium aluminium silicon phosphorus sulfur chlorine argon potassium calcium
scandium titanium vanadium chromium manganese iron cobalt nickel copper zinc
gallium germanium arsenic selenium bromine krypton rubidium strontium yttrium zirconium
niobium molybdenum technetium ruthenium rhodium palladium silver cadmium indium tin
antimony tellurium iodine xenon caesium barium lanthanum cerium praseodymium neodymium
promethium samarium europium gadolinium terbium dysprosium holmium erbium thulium ytterbium
lutetium hafnium tantalum tungsten rhenium osmium iridium platinum gold mercury thallium lead bismuth
""".split()


def periodic_decks() -> Iterable[tuple[str, tuple[int, ...]]]:
    """Orders induced by the first 83 element names/symbol-like labels."""

    if len(PERIODIC_NAMES) != ASCII_SIZE:
        raise AssertionError(len(PERIODIC_NAMES))
    by_name = tuple(sorted(range(ASCII_SIZE), key=lambda card: PERIODIC_NAMES[card]))
    by_length = tuple(
        sorted(range(ASCII_SIZE), key=lambda card: (len(PERIODIC_NAMES[card]), card))
    )
    yield "periodic-name", by_name
    yield "periodic-name-reverse", tuple(reversed(by_name))
    yield "periodic-length", by_length


def grouped_ascii_decks() -> Iterable[tuple[str, tuple[int, ...]]]:
    """Stable source orders of the ASCII+32 card prefix."""

    cards = tuple(range(ASCII_SIZE))

    def group(card: int) -> tuple[int, int, int]:
        char = chr(card + 32)
        if char.isalpha() and char.isupper():
            return 0, ord(char), card
        if char.isalpha() and char.islower():
            return 1, ord(char), card
        if char.isdigit():
            return 2, ord(char), card
        return 3, ord(char), card

    yield "ascii-category", tuple(sorted(cards, key=group))
    yield "ascii-category-reverse", tuple(sorted(cards, key=group, reverse=True))


def source_decks() -> tuple[tuple[str, tuple[int, ...]], ...]:
    candidates: list[tuple[str, tuple[int, ...]]] = [
        ("identity", tuple(range(ASCII_SIZE))),
        ("reverse", tuple(reversed(range(ASCII_SIZE)))),
    ]
    # The first three are the BDMAGICK/trailer family.  The remaining words
    # are explicit Noita-facing developer keywords, not output-fitted keys.
    for key in (
        "BDMAGICK",
        "A BAD MAGIC CARD TRICK",
        "MAGICK",
        "NOITA",
        "EYES",
        "THREE EYES ARE WATCHING YOU",
        "SECRETS OF THE ALL SEEING",
        "FI358",
        "FINNISH",
        "FIBONACCI",
        "KANTELE",
    ):
        candidates.append((f"keyed-{key.lower().replace(' ', '-')}", keyed_ascii(key)))
    candidates.extend(grouped_ascii_decks())
    candidates.extend(periodic_decks())

    finnish = " ".join(text for _, text in ORB_LORE_KEYS)
    candidates.append(("finnish-orb-lore-first-letters", source_first_letters(finnish)))

    wall_path = ROOT / "artifacts" / "noita-wall-messages-en.txt"
    if wall_path.exists():
        candidates.append(("english-wall-messages-first-letters", source_first_letters(wall_path.read_text())))

    # The translation table is shipped by the installed game.  Only its source
    # ordering is used; values are not searched for a phrase.
    translation_path = Path(
        "/Users/mvelzel/Library/Application Support/CrossOver/Bottles/Steam/"
        "drive_c/Program Files (x86)/Steam/steamapps/common/Noita/"
        "data/translations/common.csv"
    )
    if translation_path.exists():
        candidates.append(("translation-common-first-letters", source_first_letters(translation_path.read_text())))

    dedup: dict[tuple[int, ...], str] = {}
    result: list[tuple[str, tuple[int, ...]]] = []
    for name, deck in candidates:
        if len(deck) != ASCII_SIZE or sorted(deck) != list(range(ASCII_SIZE)):
            raise AssertionError((name, len(deck), len(set(deck))))
        if deck not in dedup:
            dedup[deck] = name
            result.append((name, deck))
    return tuple(result)


def body_streams() -> dict[str, tuple[int, ...]]:
    # CONTEXT_SPECS uses marker-inclusive coordinates.  The marker is retained
    # here so that every source-selected operation is tested against the same
    # frozen coordinate system as the repository's canonical audit.
    return {name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER}


def decoder_families() -> Iterable[tuple[str, Callable[[Sequence[int], Sequence[int]], tuple[int, ...]]]]:
    yield "identity", lambda stream, _deck: tuple(stream)
    yield "move-to-front", move_to_front_decode
    yield "move-to-back", move_to_back_decode
    yield "swap-front", swap_with_front_decode
    yield "reverse-prefix", reverse_prefix_decode
    yield "rotate-front", rotate_to_front_decode
    for distance in (1, 2, 3, 4, 5, 8, 13, 21, 41):
        yield f"transpose-{distance}", lambda stream, deck, distance=distance: transpose_decode(stream, deck, distance)


def context_scores(streams: dict[str, Sequence[int]]) -> tuple[int, int, int, int]:
    """Return train-isomorph, held-out-isomorph, literal, held-out-literal."""

    iso: list[bool] = []
    literal: list[bool] = []
    for _, left, left_start, right, right_start, length in CONTEXT_SPECS[6:]:
        left_values = streams[left][left_start : left_start + length]
        right_values = streams[right][right_start : right_start + length]
        iso.append(equality_signature(left_values) == equality_signature(right_values))
        literal.append(tuple(left_values) == tuple(right_values))
    return (
        sum(iso[:-1]),
        int(iso[-1]),
        sum(literal[:-1]),
        int(literal[-1]),
    )


def run() -> tuple[str, ...]:
    bodies = body_streams()
    rows: list[tuple[int, int, int, int, str, str, str]] = []
    for deck_name, deck in source_decks():
        for family, decoder in decoder_families():
            # Calibration guard: every accepted family must replay a planted
            # rank stream exactly before it is allowed to touch Eye data.
            probe = tuple((index * 17 + 3) % ASCII_SIZE for index in range(37))
            if family == "identity":
                assert tuple(probe) == tuple(probe)
            else:
                if family.startswith("transpose-"):
                    operation, distance = "transpose", int(family.split("-", 1)[1])
                else:
                    operation, distance = family, 1
                planted = ranks_to_labels(probe, deck, operation, distance)
                assert decoder(planted, deck) == probe, (deck_name, family)
            decoded = {name: decoder(stream, deck) for name, stream in bodies.items()}
            scores = context_scores(decoded)
            rows.append((*scores, deck_name, family, "label-decode"))
            # Inverse direction: values are interpreted as rank instructions,
            # and the emitted card labels are the decoded stream.
            if family == "identity":
                emitted = {name: tuple(stream) for name, stream in bodies.items()}
                inverse_scores = context_scores(emitted)
                rows.append((*inverse_scores, deck_name, family, "rank-encode"))
                continue
            if family.startswith("transpose-"):
                operation, distance = "transpose", int(family.split("-", 1)[1])
            else:
                operation, distance = family, 1
            emitted = {
                name: ranks_to_labels(stream, deck, operation, distance)
                for name, stream in bodies.items()
            }
            inverse_scores = context_scores(emitted)
            rows.append((*inverse_scores, deck_name, family, "rank-encode"))

    rows.sort(key=lambda row: (-row[0], -row[1], -row[2], -row[3], row[4], row[5], row[6]))
    out = [
        f"source_decks={len(source_decks())}",
        f"families={len(tuple(decoder_families()))}",
        "train_iso heldout_iso train_literal heldout_literal deck family direction",
    ]
    out.extend(
        f"{train:>9} {held:>11} {lit:>13} {hlit:>15} {deck:<42} {family:<16} {direction}"
        for train, held, lit, hlit, deck, family, direction in rows[:30]
    )
    out.append("--- exact all-context candidates ---")
    exact = [row for row in rows if row[:4] == (6, 1, 6, 1)]
    out.extend(" ".join(map(str, row)) for row in exact)
    out.append(f"exact_all={len(exact)}")
    return tuple(out)


if __name__ == "__main__":
    print("\n".join(run()))
