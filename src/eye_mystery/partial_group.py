"""Exact deductions from partial observations of permutation-group elements.

An isomorphic ciphertext repeat exposes only some edges of the permutation
relating its two contexts.  Those edges can still be inverted and composed:
if ``f(x)=y`` and ``g(y)=z`` are observed, then ``(g o f)(x)=z`` is forced.
Two such partial words that send the same source to different targets must be
different elements in every full permutation-group completion.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from .partial_permutation import validate_partial_permutation


PartialMap = dict[int, int]


@dataclass(frozen=True)
class PartialWord:
    """A group word and the label edges that the observations force for it."""

    letters: tuple[str, ...]
    pairs: tuple[tuple[int, int], ...]

    @property
    def mapping(self) -> PartialMap:
        return dict(self.pairs)

    @property
    def name(self) -> str:
        return " ".join(self.letters) if self.letters else "identity"


def canonical_pairs(mapping: Mapping[int, int]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(mapping.items()))


def inverse_partial(mapping: Mapping[int, int]) -> PartialMap:
    """Return the forced restriction of the inverse permutation."""

    if len(set(mapping.values())) != len(mapping):
        raise ValueError("partial map must be injective")
    return {target: source for source, target in mapping.items()}


def compose_partial(
    first: Mapping[int, int], second: Mapping[int, int]
) -> PartialMap:
    """Apply ``first`` and then ``second`` wherever both edges are known."""

    return {
        source: second[middle]
        for source, middle in first.items()
        if middle in second
    }


def conflict_witness(
    left: Mapping[int, int], right: Mapping[int, int]
) -> tuple[int, int, int] | None:
    """Return one edge proving that two partial words are distinct."""

    for source in sorted(set(left) & set(right)):
        if left[source] != right[source]:
            return source, left[source], right[source]
    return None


def _inverse_name(name: str) -> str:
    return name[:-3] if name.endswith("^-1") else f"{name}^-1"


def generate_partial_words(
    generators: Mapping[str, Mapping[int, int]],
    alphabet_size: int,
    *,
    max_depth: int,
    minimum_edges: int = 1,
) -> tuple[PartialWord, ...]:
    """Close observed generator edges under short reduced group words.

    The result contains the full identity map plus one shortest witness for
    every distinct nonempty partial restriction reached.  Adjacent inverse
    letters are skipped because their *full* permutations cancel exactly; a
    merely partial composition would otherwise understate that known fact.
    """

    if max_depth < 1:
        raise ValueError("max_depth must be positive")
    if minimum_edges < 1:
        raise ValueError("minimum_edges must be positive")

    letters: dict[str, PartialMap] = {}
    for name, raw_mapping in generators.items():
        mapping = dict(raw_mapping)
        validate_partial_permutation(mapping, alphabet_size)
        if name.endswith("^-1"):
            raise ValueError("generator names may not end in ^-1")
        letters[name] = mapping
        letters[f"{name}^-1"] = inverse_partial(mapping)

    identity = PartialWord(
        letters=(), pairs=tuple((value, value) for value in range(alphabet_size))
    )
    discovered: dict[tuple[tuple[int, int], ...], PartialWord] = {
        identity.pairs: identity
    }
    frontier: list[PartialWord] = []
    for name in sorted(letters):
        pairs = canonical_pairs(letters[name])
        if len(pairs) < minimum_edges or pairs in discovered:
            continue
        word = PartialWord((name,), pairs)
        discovered[pairs] = word
        frontier.append(word)

    for _depth in range(2, max_depth + 1):
        next_frontier: list[PartialWord] = []
        for word in frontier:
            current = word.mapping
            for name in sorted(letters):
                if word.letters and _inverse_name(word.letters[-1]) == name:
                    continue
                composed = compose_partial(current, letters[name])
                if len(composed) < minimum_edges:
                    continue
                pairs = canonical_pairs(composed)
                if pairs in discovered:
                    continue
                candidate = PartialWord(word.letters + (name,), pairs)
                discovered[pairs] = candidate
                next_frontier.append(candidate)
        frontier = next_frontier
        if not frontier:
            break

    return tuple(
        sorted(
            discovered.values(),
            key=lambda word: (len(word.letters), word.letters, word.pairs),
        )
    )


def distinctness_clique(words: tuple[PartialWord, ...]) -> tuple[PartialWord, ...]:
    """Return a deterministic clique of provably distinct group elements.

    This is a valid lower-bound witness, not a maximum-clique claim.  Several
    degree and seed orderings are tried, and every returned pair has an
    explicit conflicting image for at least one common source.
    """

    mappings = tuple(word.mapping for word in words)
    neighbours = []
    for left_index, left in enumerate(mappings):
        neighbours.append(
            {
                right_index
                for right_index, right in enumerate(mappings)
                if right_index != left_index
                and conflict_witness(left, right) is not None
            }
        )

    degrees = tuple(len(items) for items in neighbours)
    best: tuple[int, ...] = ()
    seed_orders = (
        sorted(range(len(words)), key=lambda i: (-degrees[i], i)),
        sorted(range(len(words)), key=lambda i: (degrees[i], i)),
        list(range(len(words))),
    )
    for seed_order in seed_orders:
        for seed in seed_order:
            clique = [seed]
            candidates = sorted(
                neighbours[seed], key=lambda i: (-degrees[i], i)
            )
            for candidate in candidates:
                if all(candidate in neighbours[item] for item in clique):
                    clique.append(candidate)
            result = tuple(sorted(clique))
            if len(result) > len(best):
                best = result

    return tuple(words[index] for index in best)


def verify_distinctness_clique(words: tuple[PartialWord, ...]) -> bool:
    return all(
        conflict_witness(left.mapping, right.mapping) is not None
        for index, left in enumerate(words)
        for right in words[index + 1 :]
    )
