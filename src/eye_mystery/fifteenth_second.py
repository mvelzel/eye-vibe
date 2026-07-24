"""Frozen E/G/H probes from the fifteenth wide novelty horizon."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import permutations

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.factoradic_headers import (
    P_MESSAGES,
    Q_EAST_MESSAGES,
    Q_WEST_MESSAGES,
)
from eye_mystery.hidden_geometry import (
    FIRST_FAMILY_NAMES,
    LAST_FAMILY_NAMES,
    context_sequences,
)


NATURAL_OPENING_TRIMS = {
    "east1": 24,
    "west1": 24,
    "east2": 24,
    "west2": 5,
    "east3": 5,
    "west3": 5,
    "east4": 20,
    "west4": 20,
    "east5": 20,
}
HEADER_GROUPS = {
    "P": P_MESSAGES,
    "Q-west": Q_WEST_MESSAGES,
    "Q-east": Q_EAST_MESSAGES,
}


def trimmed_eye_words() -> dict[str, tuple[int, ...]]:
    """Return markerless words after the three known natural-family openings."""

    output = {}
    for name in MESSAGE_ORDER:
        body = trigram_values(MESSAGES[name])[1:]
        output[name] = body[NATURAL_OPENING_TRIMS[name] :]
    return output


@dataclass(frozen=True)
class MorphismContradiction:
    panel: str
    source_index: int
    source: int
    expected: tuple[int, ...]
    observed: tuple[int, ...]


@dataclass(frozen=True)
class UniformMorphismFit:
    length: int
    productions: tuple[tuple[int, tuple[int, ...]], ...]
    observations: int
    predicted_observations: int
    new_productions: int
    contradiction: MorphismContradiction | None

    @property
    def exact(self) -> bool:
        return self.contradiction is None

    def production_map(self) -> dict[int, tuple[int, ...]]:
        return dict(self.productions)


def fit_uniform_morphism(
    words: Mapping[str, Sequence[int]],
    length: int,
    *,
    initial: Mapping[int, Sequence[int]] | None = None,
) -> UniformMorphismFit:
    """Fit or extend the phase-zero fixed-point equations for one uniform length."""

    if length not in range(2, 6):
        raise ValueError("the frozen uniform lengths are 2..5")
    productions = {
        symbol: tuple(image) for symbol, image in (initial or {}).items()
    }
    if any(len(image) != length for image in productions.values()):
        raise ValueError("an initial production has the wrong uniform length")
    initial_symbols = frozenset(productions)
    observations = predicted = new_productions = 0
    for panel, word in words.items():
        complete_blocks = len(word) // length
        for source_index in range(complete_blocks):
            source = word[source_index]
            start = length * source_index
            image = tuple(word[start : start + length])
            observations += 1
            if source in productions:
                predicted += source in initial_symbols
                if productions[source] != image:
                    return UniformMorphismFit(
                        length,
                        tuple(sorted(productions.items())),
                        observations,
                        predicted,
                        new_productions,
                        MorphismContradiction(
                            panel,
                            source_index,
                            source,
                            productions[source],
                            image,
                        ),
                    )
            else:
                productions[source] = image
                new_productions += 1
    return UniformMorphismFit(
        length,
        tuple(sorted(productions.items())),
        observations,
        predicted,
        new_productions,
        None,
    )


@dataclass(frozen=True)
class UniformMorphismAudit:
    length: int
    training: UniformMorphismFit
    heldout: UniformMorphismFit | None

    @property
    def exact(self) -> bool:
        return (
            self.training.exact
            and self.heldout is not None
            and self.heldout.exact
        )


def audit_uniform_morphisms(
    words: Mapping[str, Sequence[int]],
    *,
    train_names: Sequence[str] = P_MESSAGES,
    heldout_names: Sequence[str] = tuple(
        name for name in MESSAGE_ORDER if name not in P_MESSAGES
    ),
) -> tuple[UniformMorphismAudit, ...]:
    """Fit lengths 2..5 on P and extend the same productions on Q."""

    audits = []
    training_words = {name: words[name] for name in train_names}
    heldout_words = {name: words[name] for name in heldout_names}
    for length in range(2, 6):
        training = fit_uniform_morphism(training_words, length)
        heldout = (
            fit_uniform_morphism(
                heldout_words,
                length,
                initial=training.production_map(),
            )
            if training.exact
            else None
        )
        audits.append(UniformMorphismAudit(length, training, heldout))
    return tuple(audits)


@dataclass(frozen=True)
class FactorComplexity:
    length: int
    factors: int
    right_special: int


def factor_complexity(
    words: Mapping[str, Sequence[int]],
    *,
    maximum_length: int = 12,
) -> tuple[FactorComplexity, ...]:
    """Count within-panel factors and right-special factors."""

    if maximum_length < 1:
        raise ValueError("maximum factor length must be positive")
    output = []
    for length in range(1, maximum_length + 1):
        factors: set[tuple[int, ...]] = set()
        followers: dict[tuple[int, ...], set[int]] = {}
        for word in words.values():
            for start in range(len(word) - length + 1):
                factor = tuple(word[start : start + length])
                factors.add(factor)
                if start + length < len(word):
                    followers.setdefault(factor, set()).add(word[start + length])
        output.append(
            FactorComplexity(
                length,
                len(factors),
                sum(len(values) >= 2 for values in followers.values()),
            )
        )
    return tuple(output)


@dataclass(frozen=True, order=True)
class ChecksumRule:
    kind: str
    modulus: int
    sign: int
    reverse: bool = False
    degree: int = 0

    @property
    def name(self) -> str:
        direction = "-reverse" if self.reverse else ""
        degree = f"-d{self.degree}" if self.degree else ""
        sign = "plus" if self.sign == 1 else "minus"
        return f"{self.kind}{degree}{direction}-mod{self.modulus}-{sign}"


def checksum_rules() -> tuple[ChecksumRule, ...]:
    """Return the frozen named checksum dictionary before vector deduplication."""

    rules = []
    for modulus in (83, 101):
        for sign in (-1, 1):
            for kind in ("sum", "alternating", "xor", "digit-sum", "fletcher1", "fletcher2"):
                rules.append(ChecksumRule(kind, modulus, sign))
            for degree in (1, 2):
                for reverse in (False, True):
                    rules.append(
                        ChecksumRule(
                            "moment",
                            modulus,
                            sign,
                            reverse,
                            degree,
                        )
                    )
    return tuple(rules)


def _base5_digits(value: int) -> tuple[int, int, int]:
    if value not in range(125):
        raise ValueError("three base-five digits require a value in 0..124")
    return value // 25, value // 5 % 5, value % 5


def checksum_value(body: Sequence[int], rule: ChecksumRule) -> int | None:
    """Return one rule's visible-marker prediction."""

    modulus = rule.modulus
    values = tuple(reversed(body)) if rule.reverse else tuple(body)
    if rule.kind == "sum":
        raw = sum(values)
    elif rule.kind == "alternating":
        raw = sum(value if index % 2 == 0 else -value for index, value in enumerate(values))
    elif rule.kind == "xor":
        raw = 0
        for value in values:
            raw ^= value
    elif rule.kind == "digit-sum":
        raw = sum(sum(_base5_digits(value)) for value in values)
    elif rule.kind in ("fletcher1", "fletcher2"):
        first = second = 0
        for value in values:
            first = (first + value) % modulus
            second = (second + first) % modulus
        raw = first if rule.kind == "fletcher1" else second
    elif rule.kind == "moment":
        raw = sum(
            pow(index, rule.degree, modulus) * value
            for index, value in enumerate(values, start=1)
        )
    else:
        raise ValueError(f"unknown checksum rule: {rule.kind}")
    prediction = rule.sign * raw % modulus
    return prediction if prediction < 83 else None


def checksum_prediction_vector(
    streams: Mapping[str, Sequence[int]],
    rule: ChecksumRule,
) -> tuple[int | None, ...]:
    return tuple(
        checksum_value(streams[name][1:], rule)
        for name in streams
    )


def deduplicated_checksum_rules(
    streams: Mapping[str, Sequence[int]],
) -> tuple[ChecksumRule, ...]:
    """Keep the lexicographically first rule for each complete prediction vector."""

    seen: set[tuple[int | None, ...]] = set()
    output = []
    for rule in sorted(checksum_rules()):
        vector = checksum_prediction_vector(streams, rule)
        if vector not in seen:
            seen.add(vector)
            output.append(rule)
    return tuple(output)


@dataclass(frozen=True)
class ChecksumFold:
    heldout: str
    compatible_rules: tuple[str, ...]
    prediction: int | None
    actual: int
    status: str


@dataclass(frozen=True)
class ChecksumClassAudit:
    name: str
    panels: tuple[str, ...]
    folds: tuple[ChecksumFold, ...]
    shared_rules: tuple[str, ...]
    passed: bool


@dataclass(frozen=True)
class ChecksumDispatchAudit:
    rules: int
    classes: tuple[ChecksumClassAudit, ...]

    @property
    def passed(self) -> bool:
        return all(group.passed for group in self.classes)

    @property
    def correct_folds(self) -> int:
        return sum(
            fold.status == "correct"
            for group in self.classes
            for fold in group.folds
        )


def audit_checksum_dispatch(
    streams: Mapping[str, Sequence[int]],
    *,
    groups: Mapping[str, Sequence[str]] = HEADER_GROUPS,
) -> ChecksumDispatchAudit:
    """Run the strict, unanimous two-of-three leave-one-out audit."""

    rules = deduplicated_checksum_rules(streams)
    predictions = {
        rule: {
            name: checksum_value(streams[name][1:], rule)
            for name in streams
        }
        for rule in rules
    }
    classes = []
    for group_name, raw_panels in groups.items():
        panels = tuple(raw_panels)
        if len(panels) != 3:
            raise ValueError("checksum dispatch groups must contain three panels")
        folds = []
        candidate_sets: list[set[ChecksumRule]] = []
        for heldout in panels:
            training = tuple(name for name in panels if name != heldout)
            compatible = tuple(
                rule
                for rule in rules
                if all(
                    predictions[rule][name] == streams[name][0]
                    for name in training
                )
            )
            candidate_sets.append(set(compatible))
            heldout_predictions = {
                predictions[rule][heldout] for rule in compatible
            }
            if not compatible:
                prediction = None
                status = "no-prediction"
            elif len(heldout_predictions) != 1:
                prediction = None
                status = "ambiguous"
            else:
                prediction = next(iter(heldout_predictions))
                status = (
                    "correct"
                    if prediction == streams[heldout][0]
                    else "incorrect"
                )
            folds.append(
                ChecksumFold(
                    heldout,
                    tuple(rule.name for rule in compatible),
                    prediction,
                    streams[heldout][0],
                    status,
                )
            )
        shared = set.intersection(*candidate_sets) if candidate_sets else set()
        passed = all(fold.status == "correct" for fold in folds) and bool(shared)
        classes.append(
            ChecksumClassAudit(
                group_name,
                panels,
                tuple(folds),
                tuple(sorted(rule.name for rule in shared)),
                passed,
            )
        )
    return ChecksumDispatchAudit(len(rules), tuple(classes))


COMPONENT_ORDERS = tuple(permutations(range(3)))


@dataclass(frozen=True, order=True)
class ReductionSpec:
    operation: str
    order: tuple[int, int, int]

    @property
    def name(self) -> str:
        return f"{self.operation}-order{''.join(map(str, self.order))}"


def reduction_specs() -> tuple[ReductionSpec, ...]:
    return tuple(
        ReductionSpec(operation, order)
        for operation in ("sum", "forward-diff", "reverse-diff")
        for order in COMPONENT_ORDERS
    )


def reduction_raw(left: int, right: int, spec: ReductionSpec) -> int:
    left_digits = _base5_digits(left)
    right_digits = _base5_digits(right)
    if spec.operation == "sum":
        digits = tuple((a + b) % 5 for a, b in zip(left_digits, right_digits, strict=True))
    elif spec.operation == "forward-diff":
        digits = tuple((b - a) % 5 for a, b in zip(left_digits, right_digits, strict=True))
    elif spec.operation == "reverse-diff":
        digits = tuple((a - b) % 5 for a, b in zip(left_digits, right_digits, strict=True))
    else:
        raise ValueError(f"unknown reduction operation: {spec.operation}")
    serialized = tuple(digits[index] for index in spec.order)
    return 25 * serialized[0] + 5 * serialized[1] + serialized[2]


def reduction_event(left: int, right: int, spec: ReductionSpec) -> int:
    return int(reduction_raw(left, right, spec) >= 83)


def deduplicated_reduction_specs() -> tuple[ReductionSpec, ...]:
    """Deduplicate conventions by their complete accepted-pair event table."""

    seen: set[bytes] = set()
    output = []
    for spec in reduction_specs():
        table = bytes(
            reduction_event(left, right, spec)
            for left in range(83)
            for right in range(83)
        )
        if table not in seen:
            seen.add(table)
            output.append(spec)
    return tuple(output)


@dataclass(frozen=True)
class ReductionContradiction:
    context: str
    index: int
    source_pair: tuple[int, int]
    target_pair: tuple[int, int]
    source_event: int
    target_event: int


@dataclass(frozen=True)
class ReductionScore:
    spec: ReductionSpec
    agreements: int
    comparisons: int
    contradiction: ReductionContradiction | None

    @property
    def exact(self) -> bool:
        return self.agreements == self.comparisons


def reduction_score(
    contexts: Sequence[tuple[str, Sequence[int], Sequence[int]]],
    spec: ReductionSpec,
) -> ReductionScore:
    agreements = comparisons = 0
    contradiction = None
    for name, source, target in contexts:
        if len(source) != len(target):
            raise ValueError("aligned reduction contexts must have equal lengths")
        for index in range(len(source) - 1):
            source_pair = source[index], source[index + 1]
            target_pair = target[index], target[index + 1]
            source_event = reduction_event(*source_pair, spec)
            target_event = reduction_event(*target_pair, spec)
            comparisons += 1
            agreements += source_event == target_event
            if source_event != target_event and contradiction is None:
                contradiction = ReductionContradiction(
                    name,
                    index,
                    source_pair,
                    target_pair,
                    source_event,
                    target_event,
                )
    return ReductionScore(spec, agreements, comparisons, contradiction)


@dataclass(frozen=True)
class ReductionAudit:
    catalog_size: int
    selected: ReductionSpec
    training: ReductionScore
    heldout: ReductionScore
    exact_training_specs: tuple[str, ...]

    @property
    def exact(self) -> bool:
        return self.training.exact and self.heldout.exact


def audit_reduction_events(
    *,
    contexts: Sequence[tuple[str, Sequence[int], Sequence[int]]] | None = None,
    train_names: frozenset[str] = FIRST_FAMILY_NAMES,
    heldout_names: frozenset[str] = LAST_FAMILY_NAMES,
) -> ReductionAudit:
    available = tuple(contexts if contexts is not None else context_sequences())
    training_contexts = tuple(item for item in available if item[0] in train_names)
    heldout_contexts = tuple(item for item in available if item[0] in heldout_names)
    if not training_contexts or not heldout_contexts:
        raise ValueError("both reduction families require at least one context")
    catalog = deduplicated_reduction_specs()
    training_scores = tuple(
        reduction_score(training_contexts, spec) for spec in catalog
    )
    selected = min(
        training_scores,
        key=lambda score: (-score.agreements, score.spec),
    )
    return ReductionAudit(
        len(catalog),
        selected.spec,
        selected,
        reduction_score(heldout_contexts, selected.spec),
        tuple(score.spec.name for score in training_scores if score.exact),
    )
