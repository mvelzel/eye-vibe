"""Label-invariant tests for embedding isomorph contexts in affine groups."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

try:
    import z3
except ModuleNotFoundError:  # The exact solvers are an optional extra.
    z3 = None  # type: ignore[assignment]


MODULUS = 83


def z3_available() -> bool:
    """Return whether the optional exact-solver dependency is installed."""
    return z3 is not None


def _require_z3() -> None:
    if z3 is None:
        raise RuntimeError(
            "the affine embedding solvers require the optional 'z3-solver' package"
        )


@dataclass(frozen=True)
class Context:
    """One partial permutation induced between repeated plaintext passages."""

    name: str
    pairs: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class AffineEmbedding:
    coordinates: tuple[int, ...]
    transformations: dict[str, tuple[int, int]]


@dataclass(frozen=True)
class CoreMapping:
    """One context edge participating in an affine-embedding contradiction."""

    context: str
    left: int
    right: int


def verify_affine_embedding(
    contexts: Sequence[Context],
    embedding: AffineEmbedding,
    *,
    hidden_order: int = 82,
) -> bool:
    if len(embedding.coordinates) != MODULUS:
        return False
    if set(embedding.coordinates) != set(range(MODULUS)):
        return False
    squares = {pow(2, 2 * exponent, MODULUS) for exponent in range(41)}
    for context in contexts:
        if context.name not in embedding.transformations:
            return False
        multiplier, translation = embedding.transformations[context.name]
        if not 1 <= multiplier < MODULUS or not 0 <= translation < MODULUS:
            return False
        if hidden_order == 41 and multiplier not in squares:
            return False
        for left, right in context.pairs:
            if (
                multiplier * embedding.coordinates[left] + translation
            ) % MODULUS != embedding.coordinates[right]:
                return False
    return True


def context_from_sequences(
    name: str, source: Sequence[int], target: Sequence[int]
) -> Context:
    if len(source) != len(target):
        raise ValueError("isomorph sequences must have equal lengths")
    forward: dict[int, int] = {}
    reverse: dict[int, int] = {}
    for left, right in zip(source, target):
        if left in forward and forward[left] != right:
            raise ValueError(f"{name} is not a function")
        if right in reverse and reverse[right] != left:
            raise ValueError(f"{name} is not injective")
        forward[left] = right
        reverse[right] = left
    return Context(name, tuple(forward.items()))


def merge_contexts(name: str, contexts: Iterable[Context]) -> Context:
    pairs = []
    for context in contexts:
        pairs.extend(context.pairs)
    return context_from_sequences(
        name,
        tuple(left for left, _ in pairs),
        tuple(right for _, right in pairs),
    )


def find_affine_embedding(
    contexts: Sequence[Context],
    *,
    hidden_order: int = 82,
    timeout_ms: int = 300_000,
) -> tuple[str, AffineEmbedding | None, str | None]:
    """Conjugate partial context permutations into ``C83:C_hidden_order``.

    Ciphertext glyphs are treated only as labels.  A satisfying coordinate
    permutation and one affine map per context establish compatibility; UNSAT
    proves that the supplied repeated-plaintext assumptions cannot all arise
    from the requested affine action.
    """
    if hidden_order not in (41, 82):
        raise ValueError("hidden_order must be 41 or 82")
    if not contexts:
        raise ValueError("at least one context is required")
    _require_z3()

    observed = []
    for context in contexts:
        for left, right in context.pairs:
            if not 0 <= left < MODULUS or not 0 <= right < MODULUS:
                raise ValueError("ciphertext labels must be in 0..82")
            observed.extend((left, right))
    anchors = tuple(dict.fromkeys(observed))
    if len(anchors) < 2:
        raise ValueError("at least two distinct ciphertext labels are required")

    width = 7
    wide_width = 14
    solver = z3.SolverFor("QF_BV")
    solver.set(timeout=timeout_ms)
    coordinates = {
        label: z3.BitVec(f"coordinate_{label}", width) for label in anchors
    }
    for coordinate in coordinates.values():
        solver.add(z3.ULT(coordinate, MODULUS))
    # Only labels appearing in constraints need variables.  Any injection of
    # this observed subset extends to a permutation of all 83 labels.
    solver.add(z3.Distinct(*coordinates.values()))
    # Affine conjugation lets any two distinct coordinates be normalized.
    solver.add(coordinates[anchors[0]] == 0, coordinates[anchors[1]] == 1)

    squares = {pow(2, 2 * exponent, MODULUS) for exponent in range(41)}
    allowed_multipliers = tuple(
        sorted(squares) if hidden_order == 41 else range(1, MODULUS)
    )
    parameters = {}
    for index, context in enumerate(contexts):
        multiplier = z3.BitVec(f"multiplier_{index}", width)
        translation = z3.BitVec(f"translation_{index}", width)
        parameters[context.name] = (multiplier, translation)
        solver.add(z3.Or(*(multiplier == value for value in allowed_multipliers)))
        solver.add(z3.ULT(translation, MODULUS))
        for left, right in context.pairs:
            wide_multiplier = z3.ZeroExt(wide_width - width, multiplier)
            wide_coordinate = z3.ZeroExt(wide_width - width, coordinates[left])
            wide_translation = z3.ZeroExt(wide_width - width, translation)
            solver.add(
                z3.ZeroExt(wide_width - width, coordinates[right])
                == z3.URem(
                    wide_multiplier * wide_coordinate + wide_translation,
                    z3.BitVecVal(MODULUS, wide_width),
                )
            )

    outcome = solver.check()
    if outcome == z3.unknown:
        return "unknown", None, solver.reason_unknown()
    if outcome == z3.unsat:
        return "unsat", None, None

    model = solver.model()
    resolved: list[int | None] = [None] * MODULUS
    for label, variable in coordinates.items():
        resolved[label] = model.eval(variable).as_long()
    unused = iter(sorted(set(range(MODULUS)) - {v for v in resolved if v is not None}))
    for label, value in enumerate(resolved):
        if value is None:
            resolved[label] = next(unused)
    result = AffineEmbedding(
        tuple(value for value in resolved if value is not None),
        {
            name: (
                model.eval(multiplier).as_long(),
                model.eval(translation).as_long(),
            )
            for name, (multiplier, translation) in parameters.items()
        },
    )
    return "sat", result, None


def find_affine_embedding_graph(
    contexts: Sequence[Context],
    *,
    hidden_order: int = 82,
    timeout_ms: int = 300_000,
) -> tuple[str, AffineEmbedding | None, str | None]:
    """Solve the same embedding after eliminating most coordinate variables.

    Coordinates are propagated along a directed spanning forest of the partial
    context maps.  Only one seven-bit variable per forest root remains; all
    other coordinates are affine expressions in those roots and the context
    parameters.  Non-tree edges become the consistency equations.
    """
    if hidden_order not in (41, 82):
        raise ValueError("hidden_order must be 41 or 82")
    if not contexts:
        raise ValueError("at least one context is required")
    _require_z3()

    observed = []
    for context in contexts:
        for left, right in context.pairs:
            if not 0 <= left < MODULUS or not 0 <= right < MODULUS:
                raise ValueError("ciphertext labels must be in 0..82")
            observed.extend((left, right))
    anchors = tuple(dict.fromkeys(observed))
    if len(anchors) < 2:
        raise ValueError("at least two distinct ciphertext labels are required")

    width = 7
    wide_width = 14
    solver = z3.SolverFor("QF_BV")
    solver.set(timeout=timeout_ms)
    squares = {pow(2, 2 * exponent, MODULUS) for exponent in range(41)}
    allowed_multipliers = tuple(
        sorted(squares) if hidden_order == 41 else range(1, MODULUS)
    )
    parameters: dict[str, tuple[z3.BitVecRef, z3.BitVecRef]] = {}
    for index, context in enumerate(contexts):
        multiplier = z3.BitVec(f"graph_multiplier_{index}", width)
        translation = z3.BitVec(f"graph_translation_{index}", width)
        parameters[context.name] = (multiplier, translation)
        solver.add(z3.Or(*(multiplier == value for value in allowed_multipliers)))
        solver.add(z3.ULT(translation, MODULUS))

    def apply(context: Context, coordinate: z3.BitVecRef) -> z3.BitVecRef:
        multiplier, translation = parameters[context.name]
        wide_multiplier = z3.ZeroExt(wide_width - width, multiplier)
        wide_coordinate = z3.ZeroExt(wide_width - width, coordinate)
        wide_translation = z3.ZeroExt(wide_width - width, translation)
        remainder = z3.URem(
            wide_multiplier * wide_coordinate + wide_translation,
            z3.BitVecVal(MODULUS, wide_width),
        )
        return z3.Extract(width - 1, 0, remainder)

    coordinates: dict[int, z3.BitVecRef] = {
        anchors[0]: z3.BitVecVal(0, width)
    }
    roots = []
    edge_expressions: dict[tuple[str, int], z3.BitVecRef] = {}
    while len(coordinates) < len(anchors):
        changed = True
        while changed:
            changed = False
            for context in contexts:
                for left, right in context.pairs:
                    if left in coordinates and right not in coordinates:
                        key = (context.name, left)
                        expression = edge_expressions.setdefault(
                            key, apply(context, coordinates[left])
                        )
                        coordinates[right] = expression
                        changed = True
        if len(coordinates) == len(anchors):
            break
        label = next(value for value in anchors if value not in coordinates)
        root = z3.BitVec(f"coordinate_root_{len(roots)}", width)
        roots.append(root)
        solver.add(z3.ULT(root, MODULUS))
        coordinates[label] = root

    solver.add(coordinates[anchors[1]] == 1)
    solver.add(z3.Distinct(*(coordinates[label] for label in anchors)))
    for context in contexts:
        for left, right in context.pairs:
            key = (context.name, left)
            expression = edge_expressions.setdefault(
                key, apply(context, coordinates[left])
            )
            solver.add(coordinates[right] == expression)

    outcome = solver.check()
    if outcome == z3.unknown:
        return "unknown", None, solver.reason_unknown()
    if outcome == z3.unsat:
        return "unsat", None, None

    model = solver.model()
    resolved: list[int | None] = [None] * MODULUS
    for label, expression in coordinates.items():
        resolved[label] = model.eval(expression).as_long()
    unused = iter(sorted(set(range(MODULUS)) - {v for v in resolved if v is not None}))
    for label, value in enumerate(resolved):
        if value is None:
            resolved[label] = next(unused)
    result = AffineEmbedding(
        tuple(value for value in resolved if value is not None),
        {
            name: (
                model.eval(multiplier).as_long(),
                model.eval(translation).as_long(),
            )
            for name, (multiplier, translation) in parameters.items()
        },
    )
    return "sat", result, None


def find_affine_mapping_unsat_core(
    contexts: Sequence[Context],
    *,
    hidden_order: int = 82,
    timeout_ms: int = 300_000,
    minimize: bool = True,
) -> tuple[str, tuple[CoreMapping, ...], str | None]:
    """Return an edge-level UNSAT core for the direct embedding encoding.

    When ``minimize`` is true, repeated assumption checks shrink the solver's
    initial core to an irreducible one: removing any remaining mapping makes
    that particular set no longer prove UNSAT within the timeout.
    """
    if hidden_order not in (41, 82):
        raise ValueError("hidden_order must be 41 or 82")
    if not contexts:
        raise ValueError("at least one context is required")
    _require_z3()

    observed = []
    for context in contexts:
        for left, right in context.pairs:
            if not 0 <= left < MODULUS or not 0 <= right < MODULUS:
                raise ValueError("ciphertext labels must be in 0..82")
            observed.extend((left, right))
    anchors = tuple(dict.fromkeys(observed))
    if len(anchors) < 2:
        raise ValueError("at least two distinct ciphertext labels are required")

    width = 7
    wide_width = 14
    solver = z3.SolverFor("QF_BV")
    solver.set(timeout=timeout_ms)
    coordinates = {
        label: z3.BitVec(f"core_coordinate_{label}", width) for label in anchors
    }
    for coordinate in coordinates.values():
        solver.add(z3.ULT(coordinate, MODULUS))
    solver.add(z3.Distinct(*coordinates.values()))
    solver.add(coordinates[anchors[0]] == 0, coordinates[anchors[1]] == 1)

    squares = {pow(2, 2 * exponent, MODULUS) for exponent in range(41)}
    allowed_multipliers = tuple(
        sorted(squares) if hidden_order == 41 else range(1, MODULUS)
    )
    assumptions = []
    mappings: dict[z3.BoolRef, CoreMapping] = {}
    for context_index, context in enumerate(contexts):
        multiplier = z3.BitVec(f"core_multiplier_{context_index}", width)
        translation = z3.BitVec(f"core_translation_{context_index}", width)
        solver.add(z3.Or(*(multiplier == value for value in allowed_multipliers)))
        solver.add(z3.ULT(translation, MODULUS))
        for edge_index, (left, right) in enumerate(context.pairs):
            assumption = z3.Bool(f"edge_{context_index}_{edge_index}")
            assumptions.append(assumption)
            mappings[assumption] = CoreMapping(context.name, left, right)
            wide_multiplier = z3.ZeroExt(wide_width - width, multiplier)
            wide_coordinate = z3.ZeroExt(wide_width - width, coordinates[left])
            wide_translation = z3.ZeroExt(wide_width - width, translation)
            equation = z3.ZeroExt(
                wide_width - width, coordinates[right]
            ) == z3.URem(
                wide_multiplier * wide_coordinate + wide_translation,
                z3.BitVecVal(MODULUS, wide_width),
            )
            solver.add(z3.Implies(assumption, equation))

    outcome = solver.check(*assumptions)
    if outcome == z3.unknown:
        return "unknown", (), solver.reason_unknown()
    if outcome == z3.sat:
        return "sat", (), None

    core = list(solver.unsat_core())
    if minimize:
        index = 0
        while index < len(core):
            trial = core[:index] + core[index + 1 :]
            trial_outcome = solver.check(*trial)
            if trial_outcome == z3.unsat:
                # Z3 may identify a still smaller core during this check.
                core = list(solver.unsat_core())
                index = 0
            else:
                index += 1
    original_order = {assumption: index for index, assumption in enumerate(assumptions)}
    core.sort(key=original_order.__getitem__)
    return "unsat", tuple(mappings[assumption] for assumption in core), None
