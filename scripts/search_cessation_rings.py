#!/usr/bin/env python3
"""Test Eye symbols as Cessation-style skips through candidate text rings."""

from __future__ import annotations

import argparse
import heapq
from itertools import permutations
from pathlib import Path
from urllib.request import Request, urlopen

from eye_mystery.cipher_clock import AKI_DISK_INPUT_RING
from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.initials import perfect_successor_rotation
from eye_mystery.marker_bwt import (
    marker_bwt_lf_order,
    marker_bwt_plaintext_order,
)
from eye_mystery.ngram import TetragramModel, tetragram_code
from eye_mystery.noita_secret_messages import SECRET_MESSAGES, letters_only
from eye_mystery.prefix_hierarchy import serialize_trie_edges


NOITA_KEYED_ALPHABET = "bdmagickefhjlnopqrstuvwxyz"
FINNISH_ALPHABET = "abcdefghijklmnopqrstuvwxyzåäö"
SECRET_DEPTH_ORDER = (
    "G9",
    "G7",
    "G6",
    "G10",
    "G8",
    "G11",
    "G12",
    "G1",
    "G2",
    "G3",
    "G4",
    "G5",
)


def normalize_finnish(text: str) -> str:
    return text.translate(
        str.maketrans(
            {
                "ä": "q",
                "ö": "x",
                "å": "z",
                "Ä": "Q",
                "Ö": "X",
                "Å": "Z",
            }
        )
    )


def message_orders() -> tuple[tuple[str, ...], ...]:
    candidates = (
        MESSAGE_ORDER,
        perfect_successor_rotation(),
        marker_bwt_lf_order(),
        marker_bwt_plaintext_order(),
    )
    result = []
    for order in candidates:
        assert order is not None
        for variant in (tuple(order), tuple(reversed(order))):
            if variant not in result:
                result.append(variant)
    return tuple(result)


def skip_ring(
    values: tuple[int, ...],
    ring: str,
    *,
    initial_pointer: int,
    reset_value: int | None = None,
) -> str:
    pointer = initial_pointer
    output = []
    for value in values:
        if reset_value is not None and value == reset_value:
            pointer = initial_pointer
            continue
        if value < 1:
            raise ValueError("skip values must be positive")
        pointer = (pointer + value) % len(ring)
        output.append(ring[pointer])
    return "".join(output)


def score_texts(model: TetragramModel, texts: tuple[str, ...]) -> float:
    """Score consecutive four-character windows without deleting symbols."""

    total = 0.0
    windows = 0
    floor = min(model.log_probabilities)
    for raw_text in texts:
        text = normalize_finnish(raw_text).upper()
        for start in range(len(text) - 3):
            chunk = text[start : start + 4]
            windows += 1
            if all("A" <= character <= "Z" for character in chunk):
                values = tuple(ord(character) - ord("A") for character in chunk)
                total += model.log_probabilities[tetragram_code(values)]
            else:
                total += floor
    return total / max(1, windows)


def serialize_body_trie(order: tuple[str, ...], *, breadth_first: bool) -> tuple[int, ...]:
    """Emit each unique marker-free prefix-tree edge exactly once."""
    streams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    return serialize_trie_edges(
        streams,
        order,
        start=1,
        breadth_first=breadth_first,
    )


def digits_for_trigrams(values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        digit
        for value in values
        for digit in (value // 25, (value // 5) % 5, value % 5)
    )


def load_corpus(paths: list[Path], urls: list[str]) -> str:
    parts = [path.read_text(errors="ignore") for path in paths]
    for url in urls:
        request = Request(url, headers={"User-Agent": "Noita-eye-mystery research"})
        parts.append(
            urlopen(request, timeout=60).read().decode("utf-8", errors="ignore")
        )
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language-corpus", type=Path, action="append", default=[])
    parser.add_argument("--language-corpus-url", action="append", default=[])
    parser.add_argument("--top", type=int, default=15)
    parser.add_argument(
        "--ring",
        action="append",
        choices=(
            "noita-keyed-26",
            "finnish-29",
            "ascii32-83",
            "disk-114",
            "secret-gid-letters",
            "secret-depth-letters",
        ),
    )
    parser.add_argument(
        "--direction", choices=("forward", "reverse", "both"), default="both"
    )
    parser.add_argument(
        "--fixed-pointer",
        action="store_true",
        help="use only the Cessation convention: pointer immediately before index zero",
    )
    parser.add_argument("--skip-merged", action="store_true")
    args = parser.parse_args()
    if not args.language_corpus and not args.language_corpus_url:
        raise SystemExit("provide at least one Finnish language corpus")

    corpus = normalize_finnish(
        load_corpus(args.language_corpus, args.language_corpus_url)
    )
    model = TetragramModel.train(corpus)
    rings = {
        "noita-keyed-26": NOITA_KEYED_ALPHABET,
        "finnish-29": FINNISH_ALPHABET,
        "ascii32-83": "".join(chr(value + 32) for value in range(83)),
        "disk-114": AKI_DISK_INPUT_RING,
        "secret-gid-letters": "".join(
            letters_only(text) for text in SECRET_MESSAGES.values()
        ),
        "secret-depth-letters": "".join(
            letters_only(SECRET_MESSAGES[name]) for name in SECRET_DEPTH_ORDER
        ),
    }
    if args.ring:
        rings = {name: rings[name] for name in args.ring}
    orders = message_orders()
    full_raw = {name: MESSAGES[name] for name in MESSAGE_ORDER}
    body_raw = {name: MESSAGES[name][3:] for name in MESSAGE_ORDER}
    full_trigrams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    body_trigrams = {
        name: full_trigrams[name][1:] for name in MESSAGE_ORDER
    }
    trie_streams = tuple(
        (
            f"trie-{'bfs' if breadth_first else 'dfs'}-{order_index}",
            serialize_body_trie(order, breadth_first=breadth_first),
        )
        for order_index, order in enumerate(orders)
        for breadth_first in (False, True)
    )

    best = []
    serial = 0

    def record(description: str, texts: tuple[str, ...]) -> None:
        nonlocal serial
        score = score_texts(model, texts)
        item = (score, serial, description, texts)
        serial += 1
        if len(best) < args.top:
            heapq.heappush(best, item)
        elif item > best[0]:
            heapq.heapreplace(best, item)

    for ring_name, base_ring in rings.items():
        reversals = {
            "forward": (False,),
            "reverse": (True,),
            "both": (False, True),
        }[args.direction]
        for reverse in reversals:
            ring = base_ring[::-1] if reverse else base_ring
            pointers = (len(ring) - 1,) if args.fixed_pointer else range(len(ring))
            for initial_pointer in pointers:
                # Raw directions as the five positive skip distances.
                for steps in permutations(range(1, 6)):
                    for marker_mode, streams in (
                        ("full", full_raw),
                        ("body", body_raw),
                    ):
                        mapped = {
                            name: tuple(steps[value] for value in streams[name])
                            for name in MESSAGE_ORDER
                        }
                        # Reset per panel.  The order is immaterial to the score.
                        texts = tuple(
                            skip_ring(
                                mapped[name],
                                ring,
                                initial_pointer=initial_pointer,
                            )
                            for name in MESSAGE_ORDER
                        )
                        record(
                            f"raw-positive ring={ring_name} reverse={reverse} "
                            f"pointer={initial_pointer} map={steps} mode={marker_mode} reset",
                            texts,
                        )
                        # Preserve the independently established one-character-
                        # per-trigram layer: apply all three skips, then read.
                        triple_steps = {
                            name: tuple(
                                sum(mapped[name][start : start + 3])
                                for start in range(0, len(mapped[name]), 3)
                            )
                            for name in MESSAGE_ORDER
                        }
                        triple_texts = tuple(
                            skip_ring(
                                triple_steps[name],
                                ring,
                                initial_pointer=initial_pointer,
                            )
                            for name in MESSAGE_ORDER
                        )
                        record(
                            f"raw-triple-read ring={ring_name} reverse={reverse} "
                            f"pointer={initial_pointer} map={steps} mode={marker_mode} reset",
                            triple_texts,
                        )
                        # Persistent state in each independently decoded marker order.
                        for order_index, order in enumerate(orders):
                            values = tuple(
                                value for name in order for value in mapped[name]
                            )
                            record(
                                f"raw-positive ring={ring_name} reverse={reverse} "
                                f"pointer={initial_pointer} map={steps} mode={marker_mode} "
                                f"continuous-order={order_index}",
                                (
                                    skip_ring(
                                        values,
                                        ring,
                                        initial_pointer=initial_pointer,
                                    ),
                                ),
                            )
                            triple_values = tuple(
                                value
                                for name in order
                                for value in triple_steps[name]
                            )
                            record(
                                f"raw-triple-read ring={ring_name} reverse={reverse} "
                                f"pointer={initial_pointer} map={steps} mode={marker_mode} "
                                f"continuous-order={order_index}",
                                (
                                    skip_ring(
                                        triple_values,
                                        ring,
                                        initial_pointer=initial_pointer,
                                    ),
                                ),
                            )

                # Accepted trigrams as distances, both with and without zero reset.
                for marker_mode, streams in (
                    ("full", full_trigrams),
                    ("body", body_trigrams),
                ):
                    for plus_one, reset_value in ((True, None), (False, 0)):
                        label = "plus-one" if plus_one else "zero-reset"
                        texts = []
                        for name in MESSAGE_ORDER:
                            values = streams[name]
                            if plus_one:
                                values = tuple(value + 1 for value in values)
                            texts.append(
                                skip_ring(
                                    values,
                                    ring,
                                    initial_pointer=initial_pointer,
                                    reset_value=reset_value,
                                )
                            )
                        record(
                            f"trigram-{label} ring={ring_name} reverse={reverse} "
                            f"pointer={initial_pointer} mode={marker_mode} reset",
                            tuple(texts),
                        )

                # Cessation-like merging: serialize every unique body-trie edge
                # once, then decode either its trigrams or their base-five digits.
                for trie_name, values in (() if args.skip_merged else trie_streams):
                    for layer, sequence in (
                        ("trigram", tuple(value + 1 for value in values)),
                        ("raw", digits_for_trigrams(values)),
                    ):
                        if layer == "trigram":
                            record(
                                f"merged-{trie_name}-{layer} ring={ring_name} "
                                f"reverse={reverse} pointer={initial_pointer}",
                                (
                                    skip_ring(
                                        sequence,
                                        ring,
                                        initial_pointer=initial_pointer,
                                    ),
                                ),
                            )
                        else:
                            for steps in permutations(range(1, 6)):
                                mapped = tuple(steps[value] for value in sequence)
                                record(
                                    f"merged-{trie_name}-{layer} ring={ring_name} "
                                    f"reverse={reverse} pointer={initial_pointer} map={steps}",
                                    (
                                        skip_ring(
                                            mapped,
                                            ring,
                                            initial_pointer=initial_pointer,
                                        ),
                                    ),
                                )

    reference = normalize_finnish(corpus)[-3108:]
    letters_reference = "".join(
        character
        for character in normalize_finnish(corpus).upper()
        if "A" <= character <= "Z"
    )[-3108:]
    print("Noita keyed alphabet:", NOITA_KEYED_ALPHABET)
    print("raw language-corpus reference:", f"{score_texts(model, (reference,)):.4f}")
    print(
        "letters-only language-corpus reference:",
        f"{score_texts(model, (letters_reference,)):.4f}",
    )
    print("mechanisms scored:", serial)
    print("unique marker-free trie edges:", len(trie_streams[0][1]))
    print("best candidates:")
    display = str.maketrans({"q": "ä", "x": "ö", "z": "å", "Q": "Ä", "X": "Ö", "Z": "Å"})
    for score, _, description, texts in sorted(best, reverse=True):
        preview = " / ".join(text[:100] for text in texts[:3]).translate(display)
        print(f"  score={score:.4f} {description}")
        print("   ", preview)


if __name__ == "__main__":
    main()
