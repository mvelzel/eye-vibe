#!/usr/bin/env python3
"""Check the six ``THAT WHICH`` windows under ordinary GAK."""

from __future__ import annotations

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.gak_fixed_point import (
    combined_word_spans,
    find_stabilizer_contradictions_from_spans,
    find_word_status_conflicts,
)
from eye_mystery.isomorphs import pattern
try:
    from scripts.classify_that_which_windows import WINDOWS
except ModuleNotFoundError:  # Direct ``python scripts/...`` execution.
    from classify_that_which_windows import WINDOWS


PHRASE = "THAT WHICH"


def main() -> None:
    ciphertexts = tuple(
        trigram_values(MESSAGES[window.message])[
            window.offset : window.offset + len(PHRASE)
        ]
        for window in WINDOWS
    )
    names = tuple(
        f"{window.message}:{window.offset}"
        for window in WINDOWS
    )
    plains = (PHRASE,) * len(ciphertexts)
    spans = combined_word_spans(
        plains,
        ciphertexts,
        trace_names=names,
    )
    conflicts = find_word_status_conflicts(spans)
    contradictions = find_stabilizer_contradictions_from_spans(spans)
    fixed_words = tuple(
        sorted(
            {
                "".join(span.word)
                for span in spans
                if span.fixes_top
            },
            key=lambda word: (len(word), word),
        )
    )

    print(f"phrase={PHRASE!r} length={len(PHRASE)}")
    for name, ciphertext in zip(names, ciphertexts, strict=True):
        print(
            f"{name:10s} cards={' '.join(map(str, ciphertext))} "
            f"pattern={pattern(ciphertext)}"
        )
    print(f"word spans={len(spans)}")
    print(f"top-fixing words={fixed_words}")
    print(f"same-word status conflicts={len(conflicts)}")
    print(f"subgroup contradictions={len(contradictions)}")
    for contradiction in contradictions[:10]:
        print(
            "  "
            f"{''.join(contradiction.first.word)!r}:"
            f"{contradiction.first.fixes_top} "
            f"{''.join(contradiction.second.word)!r}:"
            f"{contradiction.second.fixes_top} "
            f"{''.join(contradiction.combined.word)!r}:"
            f"{contradiction.combined.fixes_top} "
            f"locations={contradiction.observation_locations}"
        )


if __name__ == "__main__":
    main()
