"""Final finite tests from the twelfth Eye-cipher novelty horizon.

This module implements the three remaining hypotheses that make a selected,
falsifiable prediction:

* a signed 42-class quotient as a projective line over ``F41``;
* concentration in the singular spectrum of the directed transition support;
* one global linear convolutional parity check on the raw five-ary streams.

Storage bitplanes, conventional cipher modes, and executable game clues are
closed by audits or identifiability arguments rather than arbitrary scans.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations, product

from eye_mystery.corpus import MESSAGES
from eye_mystery.factoradic_headers import P_MESSAGES, Q_MESSAGES
from eye_mystery.twelfth_novelty import _homogeneous_null_vector
from eye_mystery.twelfth_second import raw_suffix_starts
from eye_mystery.wide_complements import (
    primitive_roots_f83,
    reflection_log_orbit,
)


ProjectivePoint = int | None
ProjectiveMatrix = tuple[int, int, int, int]


def fit_projective_mobius(
    pairs: Sequence[tuple[ProjectivePoint, ProjectivePoint]],
    prime: int,
) -> ProjectiveMatrix | None:
    """Fit a Möbius map through three finite-or-infinite point pairs."""

    if len(pairs) != 3:
        raise ValueError("exactly three pairs determine a projective map")
    rows = []
    for source, target in pairs:
        source_x, source_z = (1, 0) if source is None else (source, 1)
        target_y, target_w = (1, 0) if target is None else (target, 1)
        rows.append(
            (
                target_w * source_x,
                target_w * source_z,
                -target_y * source_x,
                -target_y * source_z,
            )
        )
    vector = _homogeneous_null_vector(rows, prime)
    if vector is None:
        return None
    a, b, c, d = vector
    if (a * d - b * c) % prime == 0:
        return None
    return a, b, c, d


def apply_projective_mobius(
    matrix: ProjectiveMatrix,
    value: ProjectivePoint,
    prime: int,
) -> ProjectivePoint:
    """Apply a Möbius map to a point of ``P1(F_prime)``."""

    source_x, source_z = (1, 0) if value is None else (value, 1)
    a, b, c, d = matrix
    numerator = (a * source_x + b * source_z) % prime
    denominator = (c * source_x + d * source_z) % prime
    if denominator == 0:
        return None
    return numerator * pow(denominator, -1, prime) % prime


def signed_projective_relation(
    mapping: Mapping[int, int],
    center: int,
    *,
    generator: int = 2,
) -> tuple[tuple[ProjectivePoint, ProjectivePoint], ...]:
    """Quotient an Eye context by reflection around one global field center."""

    return tuple(
        sorted(
            {
                (
                    None
                    if source == center
                    else reflection_log_orbit(
                        source,
                        center,
                        generator,
                        zero_class=41,
                    ),
                    None
                    if target == center
                    else reflection_log_orbit(
                        target,
                        center,
                        generator,
                        zero_class=41,
                    ),
                )
                for source, target in mapping.items()
            },
            key=lambda pair: (
                41 if pair[0] is None else pair[0],
                41 if pair[1] is None else pair[1],
            ),
        )
    )


def maximum_projective_relation_support(
    relation: Sequence[tuple[ProjectivePoint, ProjectivePoint]],
    prime: int = 41,
) -> int:
    """Return the largest exact PGL support fitted from any three edges."""

    relation = tuple(relation)
    if len(relation) < 3:
        return len(relation)
    best = 0
    for selected in combinations(relation, 3):
        matrix = fit_projective_mobius(selected, prime)
        if matrix is None:
            continue
        support = sum(
            apply_projective_mobius(matrix, source, prime) == target
            for source, target in relation
        )
        best = max(best, support)
    return best


@dataclass(frozen=True)
class SignedProjectiveScore:
    center: int
    relation_sizes: tuple[int, ...]
    supports: tuple[int, ...]

    @property
    def extra_support(self) -> int:
        return sum(
            support - min(3, size)
            for support, size in zip(
                self.supports, self.relation_sizes, strict=True
            )
        )

    @property
    def exact_contexts(self) -> int:
        return sum(
            support == size
            for support, size in zip(
                self.supports, self.relation_sizes, strict=True
            )
        )


def signed_projective_score(
    mappings: Sequence[Mapping[int, int]],
    center: int,
    *,
    generator: int = 2,
) -> SignedProjectiveScore:
    relations = tuple(
        signed_projective_relation(
            mapping,
            center,
            generator=generator,
        )
        for mapping in mappings
    )
    return SignedProjectiveScore(
        center,
        tuple(map(len, relations)),
        tuple(
            maximum_projective_relation_support(relation)
            for relation in relations
        ),
    )


def select_signed_projective_center(
    mappings: Sequence[Mapping[int, int]],
) -> SignedProjectiveScore:
    """Scan the complete pre-existing family of 83 global reflection centers."""

    return min(
        (signed_projective_score(mappings, center) for center in range(83)),
        key=lambda score: (
            -score.exact_contexts,
            -score.extra_support,
            score.center,
        ),
    )


def signed_projective_scan_reaches(
    mappings: Sequence[Mapping[int, int]],
    threshold: SignedProjectiveScore,
) -> bool:
    """Return early when the complete center scan reaches a frozen score.

    This is mathematically the same upper-tail event as selecting every null
    winner, but avoids spending time ranking a control after it is already
    known to be at least as extreme as the observed corpus.
    """

    target = (threshold.exact_contexts, threshold.extra_support)
    return any(
        (score.exact_contexts, score.extra_support) >= target
        for score in (
            signed_projective_score(mappings, center)
            for center in range(83)
        )
    )


def primitive_generator_supports(
    mappings: Sequence[Mapping[int, int]],
    center: int,
) -> tuple[tuple[int, ...], ...]:
    """Expose the coordinate-isomorphism check over all 40 primitive roots."""

    return tuple(
        signed_projective_score(
            mappings,
            center,
            generator=generator,
        ).supports
        for generator in primitive_roots_f83()
    )


def leading_singular_energy_fraction(
    edges: Iterable[tuple[int, int]],
    *,
    alphabet_size: int = 83,
    iterations: int = 200,
) -> float:
    """Return ``sigma_1(A)^2 / ||A||_F^2`` for a binary adjacency matrix.

    The calculation is matrix-free deterministic power iteration on ``A^T A``.
    Its all-positive initial vector has nonzero projection on a Perron leading
    eigenvector.  The denominator is the number of directed support edges.
    """

    edge_set = frozenset(edges)
    if not edge_set:
        raise ValueError("at least one transition edge is required")
    if iterations < 1:
        raise ValueError("at least one power iteration is required")
    for source, target in edge_set:
        if (
            source not in range(alphabet_size)
            or target not in range(alphabet_size)
        ):
            raise ValueError("transition lies outside the visible alphabet")

    scale = alphabet_size**-0.5
    vector = [scale] * alphabet_size
    for _ in range(iterations):
        left = [0.0] * alphabet_size
        for source, target in edge_set:
            left[source] += vector[target]
        right = [0.0] * alphabet_size
        for source, target in edge_set:
            right[target] += left[source]
        norm = sum(value * value for value in right) ** 0.5
        if norm == 0.0:
            raise ValueError("adjacency support has zero singular energy")
        vector = [value / norm for value in right]

    left = [0.0] * alphabet_size
    for source, target in edge_set:
        left[source] += vector[target]
    leading_squared = sum(value * value for value in left)
    return leading_squared / len(edge_set)


def normalized_five_ary_filters() -> tuple[tuple[int, ...], ...]:
    """Enumerate all 124 normalized memory-one through memory-three filters.

    The current-symbol coefficient is fixed to one, eliminating scalar
    duplicates.  The oldest coefficient is required to be nonzero so each
    tuple has its advertised memory.
    """

    filters = []
    for length in range(2, 5):
        for middle in product(range(5), repeat=length - 2):
            for oldest in range(1, 5):
                filters.append((1, *middle, oldest))
    return tuple(filters)


FIVE_ARY_FILTERS = normalized_five_ary_filters()


@dataclass(frozen=True)
class SyndromeCount:
    zeros: int
    positions: int

    @property
    def zero_rate(self) -> float:
        return self.zeros / self.positions if self.positions else 0.0


def convolutional_syndrome_count(
    coefficients: Sequence[int],
    names: Iterable[str],
    *,
    messages: Mapping[str, Sequence[int]] = MESSAGES,
    starts: Mapping[str, int] | None = None,
) -> SyndromeCount:
    """Count zero syndromes after each independently fixed suffix start.

    At the first scored position, preceding filter digits may belong to the
    already observed branch-exit context.  This matches the frozen transducer
    convention: ``starts[name]`` selects prediction positions, not a reset.
    """

    coefficients = tuple(coefficients)
    if len(coefficients) not in range(2, 5):
        raise ValueError("filter length must be two through four")
    if coefficients[0] % 5 != 1 or coefficients[-1] % 5 == 0:
        raise ValueError("filter must be normalized with its oldest tap nonzero")
    if starts is None:
        starts = raw_suffix_starts()

    zeros = positions = 0
    memory = len(coefficients) - 1
    for name in names:
        stream = messages[name]
        for index in range(max(memory, starts[name]), len(stream)):
            syndrome = sum(
                coefficient * stream[index - lag]
                for lag, coefficient in enumerate(coefficients)
            ) % 5
            zeros += syndrome == 0
            positions += 1
    return SyndromeCount(zeros, positions)


@dataclass(frozen=True)
class ConvolutionalSelection:
    coefficients: tuple[int, ...]
    training: SyndromeCount
    heldout: SyndromeCount


def select_convolutional_filter(
    *,
    messages: Mapping[str, Sequence[int]] = MESSAGES,
    starts: Mapping[str, int] | None = None,
    training_names: Sequence[str] = P_MESSAGES,
    heldout_names: Sequence[str] = Q_MESSAGES,
) -> ConvolutionalSelection:
    """Select on the three P panels and score once on the six Q panels."""

    if starts is None:
        starts = raw_suffix_starts()
    scored = tuple(
        (
            convolutional_syndrome_count(
                coefficients,
                training_names,
                messages=messages,
                starts=starts,
            ),
            coefficients,
        )
        for coefficients in FIVE_ARY_FILTERS
    )
    # Lexicographic taps make the complete-family tie break reproducible.
    training, coefficients = min(
        scored,
        key=lambda item: (-item[0].zero_rate, item[1]),
    )
    heldout = convolutional_syndrome_count(
        coefficients,
        heldout_names,
        messages=messages,
        starts=starts,
    )
    return ConvolutionalSelection(coefficients, training, heldout)
