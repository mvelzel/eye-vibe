#!/usr/bin/env python3
"""Test a Cessation-style Eye walk with an unknown alphabet-ring ordering.

The five visible directions are assigned the positive skips 1..5.  Three
skips are applied for each accepted Eye trigram and the resulting ring state
is emitted once.  Because the ring ordering is unknown, an injective
monoalphabetic solver supplies the state-to-letter labels.
"""

from __future__ import annotations

import argparse
import heapq
from collections import Counter
from itertools import permutations
from pathlib import Path
from urllib.request import Request, urlopen

from eye_mystery.cessation import trace_trigram_skip_states
from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES
from eye_mystery.mono_substitution import solve_mono_substitution
from eye_mystery.ngram import TetragramModel, ascii_letters


def normalize_finnish(text: str) -> str:
    """Keep Finnish diacritics distinct inside the solver's A-Z alphabet."""

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


def load_corpus(paths: list[Path], urls: list[str]) -> str:
    parts = [path.read_text(errors="ignore") for path in paths]
    for url in urls:
        request = Request(url, headers={"User-Agent": "Noita-eye-mystery research"})
        parts.append(
            urlopen(request, timeout=60).read().decode("utf-8", errors="ignore")
        )
    return normalize_finnish("\n".join(parts))


def frequency_profile_distance(
    streams: tuple[tuple[int, ...], ...], target: tuple[float, ...]
) -> float:
    """Monoalphabetic-invariant distance between sorted frequency profiles."""

    counts = Counter(value for stream in streams for value in stream)
    total = sum(counts.values())
    observed = sorted((count / total for count in counts.values()), reverse=True)
    expected = sorted(target, reverse=True)[: len(observed)]
    expected_total = sum(expected)
    expected = [value / expected_total for value in expected]
    return sum(
        (actual - wanted) ** 2 / max(wanted, 1e-12)
        for actual, wanted in zip(observed, expected, strict=True)
    )


def build_streams(
    steps: tuple[int, ...], modulus: int, *, omit_markers: bool
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        trace_trigram_skip_states(
            MESSAGES[name][3:] if omit_markers else MESSAGES[name],
            steps,
            modulus,
        )
        for name in MESSAGE_ORDER
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language-corpus", type=Path, action="append", default=[])
    parser.add_argument("--language-corpus-url", action="append", default=[])
    parser.add_argument("--modulus", type=int, action="append")
    parser.add_argument("--profile-shortlist", type=int, default=48)
    parser.add_argument("--solver-shortlist", type=int, default=12)
    parser.add_argument("--screen-restarts", type=int, default=2)
    parser.add_argument("--screen-iterations", type=int, default=25_000)
    parser.add_argument("--restarts", type=int, default=12)
    parser.add_argument("--iterations", type=int, default=150_000)
    parser.add_argument("--seed", type=int, default=20260721)
    parser.add_argument("--top", type=int, default=8)
    args = parser.parse_args()
    if not args.language_corpus and not args.language_corpus_url:
        raise SystemExit("provide at least one Finnish language corpus")

    corpus = load_corpus(args.language_corpus, args.language_corpus_url)
    model = TetragramModel.train(corpus)
    corpus_letters = ascii_letters(corpus)
    corpus_counts = Counter(corpus_letters)
    target_total = len(corpus_letters) + 26
    target = tuple(
        (corpus_counts[letter] + 1) / target_total for letter in range(26)
    )
    moduli = tuple(args.modulus or (26,))
    if any(modulus not in range(2, 27) for modulus in moduli):
        raise SystemExit("modulus must be in 2..26 for an injective A-Z solve")

    # An unknown starting position is absorbed by the substitution key.  Test
    # both ring directions, panel resets, marker inclusion, and every bijection
    # from the five eye directions to the visible skip values 1..5.
    profile_heap = []
    serial = 0
    total_candidates = 0
    for modulus in moduli:
        for sign in (1, -1):
            for positive_steps in permutations(range(1, 6)):
                steps = tuple(sign * value for value in positive_steps)
                for omit_markers in (False, True):
                    streams = build_streams(
                        steps, modulus, omit_markers=omit_markers
                    )
                    distance = frequency_profile_distance(streams, target)
                    item = (
                        -distance,
                        serial,
                        modulus,
                        steps,
                        omit_markers,
                        streams,
                    )
                    serial += 1
                    total_candidates += 1
                    if len(profile_heap) < args.profile_shortlist:
                        heapq.heappush(profile_heap, item)
                    elif item > profile_heap[0]:
                        heapq.heapreplace(profile_heap, item)

    screened = []
    for rank, item in enumerate(sorted(profile_heap, reverse=True)):
        _, _, modulus, steps, omit_markers, streams = item
        result = solve_mono_substitution(
            streams,
            model,
            restarts=args.screen_restarts,
            iterations=args.screen_iterations,
            seed=args.seed + rank,
        )
        windows = sum(max(0, len(stream) - 3) for stream in streams)
        score = result.score / max(1, windows)
        screened.append(
            (score, modulus, steps, omit_markers, streams, result)
        )

    finalists = sorted(screened, reverse=True, key=lambda item: item[0])[
        : args.solver_shortlist
    ]
    refined = []
    for rank, (_, modulus, steps, omit_markers, streams, _) in enumerate(finalists):
        result = solve_mono_substitution(
            streams,
            model,
            restarts=args.restarts,
            iterations=args.iterations,
            seed=args.seed + 100_000 + rank,
        )
        windows = sum(max(0, len(stream) - 3) for stream in streams)
        refined.append(
            (
                result.score / max(1, windows),
                modulus,
                steps,
                omit_markers,
                result,
            )
        )

    reference_length = sum(len(stream) for stream in finalists[0][4])
    reference = corpus_letters[-reference_length:]
    reference_score = model.score(reference) / max(1, len(reference) - 3)
    print("mechanism candidates:", total_candidates)
    print("profile-screened:", len(profile_heap))
    print("language-refined:", len(refined))
    print("held-in Finnish reference:", f"{reference_score:.4f}")
    print("best candidates:")
    display = str.maketrans({"Q": "Ä", "X": "Ö", "Z": "Å"})
    for score, modulus, steps, omit_markers, result in sorted(
        refined, reverse=True
    )[: args.top]:
        print(
            f"  score={score:.4f} modulus={modulus} steps={steps} "
            f"mode={'body/reset' if omit_markers else 'full/reset'} "
            f"states={len(result.states)}"
        )
        for name, plaintext in zip(
            MESSAGE_ORDER[:3], result.plaintexts[:3], strict=True
        ):
            print(f"    {name}: {plaintext[:100].translate(display)}")


if __name__ == "__main__":
    main()
