"""Axis-typed branch-machine screens for the final Eye phase."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import combinations, product

from eye_mystery.factoradic_headers import (
    base5_digits as header_base5_digits,
    header_ranks,
)
from eye_mystery.gap_anchor import FINAL_MESSAGES
from eye_mystery.middle_eye_cycle import CLOCKWISE_FROM_UP
from eye_mystery.phase_marker_closure import (
    late_signatures,
    phase_closure_metrics,
    phase_topology_observation,
)
from eye_mystery.terminal_source_return import class_labels


MODULUS = 83
SYSTEMATIC_CLASSES = tuple(range(25))
SYSTEMATIC_HOLDOUTS = (10, 24)


@dataclass(frozen=True)
class DisagreementWindow:
    start: int
    end: int
    left: tuple[int, ...]
    right: tuple[int, ...]
    difference: int
    difference_mod83: int

    @property
    def length(self) -> int:
        return self.end - self.start


def closed_disagreement_windows(
    left: Sequence[int],
    right: Sequence[int],
) -> tuple[DisagreementWindow, ...]:
    """Return unequal aligned runs that are followed by an equality."""

    left = tuple(left)
    right = tuple(right)
    limit = min(len(left), len(right))
    windows = []
    position = 0
    while position < limit:
        if left[position] == right[position]:
            position += 1
            continue
        start = position
        while position < limit and left[position] != right[position]:
            position += 1
        if position == limit:
            break
        left_word = left[start:position]
        right_word = right[start:position]
        difference = sum(left_word) - sum(right_word)
        windows.append(
            DisagreementWindow(
                start=start,
                end=position,
                left=left_word,
                right=right_word,
                difference=difference,
                difference_mod83=difference % MODULUS,
            )
        )
    return tuple(windows)


def _second_position(
    signature: Sequence[int],
    class_id: int,
) -> int | None:
    positions = tuple(
        index for index, value in enumerate(signature) if value == class_id
    )
    return positions[1] if len(positions) > 1 else None


@dataclass(frozen=True)
class AxisRoleObservation:
    loop: str
    source_mate: str
    target_mate: str
    common_boundary: int
    source_boundary: int
    role_directions: tuple[int, int, int, int]
    complete: bool
    clockwise_from_up: bool


def third_axis_roles() -> AxisRoleObservation:
    """Classify third-coordinate directions by their scoped second use."""

    topology = phase_topology_observation()
    loop = topology.loop
    source_mate = next(
        name for name in topology.source_pair if name != loop
    )
    target_mate = next(
        name for name in topology.target_pair if name != loop
    )
    signatures = late_signatures()
    common = phase_closure_metrics().late_common_length
    source_boundary = max(
        length
        for _pair, length in phase_closure_metrics().late_pair_lcps
    )

    roles: dict[str, int] = {}
    for direction in range(1, 5):
        positions = {
            name: _second_position(signatures[name], direction)
            for name in FINAL_MESSAGES
        }
        values = tuple(positions.values())
        if (
            values[0] is not None
            and len(set(values)) == 1
            and int(values[0]) < common
        ):
            roles["common"] = direction
        elif (
            positions[loop] == positions[source_mate]
            and positions[loop] is not None
            and int(positions[loop]) >= common
            and positions[target_mate] is None
        ):
            roles["source"] = direction
        elif (
            positions[loop] is None
            and positions[source_mate] is None
            and positions[target_mate] is not None
            and int(positions[target_mate]) >= common
        ):
            roles["target"] = direction
        elif all(position is None for position in values):
            roles["absent"] = direction

    complete = set(roles) == {"common", "source", "target", "absent"}
    ordered = tuple(
        roles.get(role, -1)
        for role in ("common", "source", "target", "absent")
    )
    return AxisRoleObservation(
        loop=loop,
        source_mate=source_mate,
        target_mate=target_mate,
        common_boundary=common,
        source_boundary=source_boundary,
        role_directions=ordered,  # type: ignore[arg-type]
        complete=complete,
        clockwise_from_up=complete and ordered == CLOCKWISE_FROM_UP,
    )


@dataclass(frozen=True)
class BranchChecksumObservation:
    windows: tuple[DisagreementWindow, ...]
    source_direction: int
    target_direction: int
    predicted_differences: tuple[int, int]
    observed_differences: tuple[int, ...]
    reciprocal_controls: bool


def branch_checksum_observation() -> BranchChecksumObservation:
    """Audit closed loop/target disagreements in the fixed orientation."""

    roles = third_axis_roles()
    signatures = late_signatures()
    windows = closed_disagreement_windows(
        signatures[roles.loop],
        signatures[roles.target_mate],
    )
    source_direction = roles.role_directions[1]
    target_direction = roles.role_directions[2]
    predicted = (target_direction, source_direction)
    observed = tuple(window.difference_mod83 for window in windows)
    return BranchChecksumObservation(
        windows=windows,
        source_direction=source_direction,
        target_direction=target_direction,
        predicted_differences=predicted,
        observed_differences=observed,
        reciprocal_controls=observed == predicted,
    )


def base5_digits(value: int) -> tuple[int, int, int]:
    if value < 0:
        raise ValueError("class ID cannot be negative")
    return value // 25, (value // 5) % 5, value % 5


def coordinate_sum(values: Sequence[int]) -> tuple[int, int, int]:
    digits = tuple(base5_digits(value) for value in values)
    return tuple(sum(item[index] for item in digits) for index in range(3))


@dataclass(frozen=True)
class CarryRewriteObservation:
    source_word: tuple[int, ...]
    target_word: tuple[int, ...]
    source_digits: tuple[tuple[int, int, int], ...]
    target_digits: tuple[tuple[int, int, int], ...]
    common_tokens: tuple[int, ...]
    source_residual: tuple[int, ...]
    target_residual: tuple[int, ...]
    coordinate_residual: tuple[int, int, int]
    weighted_residual: int
    repair_class: int
    repair_is_target_direction: bool
    repaired: bool


def _cancel_common(
    left: Sequence[int],
    right: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    left_counts = Counter(left)
    right_counts = Counter(right)
    common_counts = left_counts & right_counts
    common = tuple(
        value
        for value in sorted(common_counts)
        for _ in range(common_counts[value])
    )
    for value in common:
        left_counts[value] -= 1
        right_counts[value] -= 1
    left_values = []
    for value in left:
        if left_counts[value] > 0:
            left_values.append(value)
            left_counts[value] -= 1
    right_values = []
    for value in right:
        if right_counts[value] > 0:
            right_values.append(value)
            right_counts[value] -= 1
    left_residual = tuple(left_values)
    right_residual = tuple(right_values)
    return common, left_residual, right_residual


def carry_rewrite_observation() -> CarryRewriteObservation:
    checksum = branch_checksum_observation()
    if not checksum.windows:
        raise AssertionError("late branch has no closed disagreement")
    window = checksum.windows[0]
    common, source_residual, target_residual = _cancel_common(
        window.left,
        window.right,
    )
    source_sum = coordinate_sum(source_residual)
    target_sum = coordinate_sum(target_residual)
    residual = tuple(
        left - right
        for left, right in zip(source_sum, target_sum, strict=True)
    )
    weighted = 25 * residual[0] + 5 * residual[1] + residual[2]
    repair = checksum.target_direction
    return CarryRewriteObservation(
        source_word=window.left,
        target_word=window.right,
        source_digits=tuple(map(base5_digits, window.left)),
        target_digits=tuple(map(base5_digits, window.right)),
        common_tokens=common,
        source_residual=source_residual,
        target_residual=target_residual,
        coordinate_residual=residual,  # type: ignore[arg-type]
        weighted_residual=weighted,
        repair_class=repair,
        repair_is_target_direction=repair == checksum.target_direction,
        repaired=sum(source_residual) == sum(target_residual) + repair,
    )


@dataclass(frozen=True)
class AssignmentBaseline:
    assignments: int
    difference3: int
    difference3_with_term3: int


def branch_assignment_baseline() -> AssignmentBaseline:
    """Enumerate broad distinct four-term residual assignments in 0..24."""

    assignments = 0
    difference3 = 0
    with_term = 0
    for left1, left2, right1, right2 in product(range(25), repeat=4):
        if len({left1, left2, right1, right2}) != 4:
            continue
        assignments += 1
        if left1 + left2 - right1 - right2 == 3:
            difference3 += 1
            with_term += 3 in {left1, left2, right1, right2}
    return AssignmentBaseline(assignments, difference3, with_term)


@dataclass(frozen=True)
class RepeatInterval:
    class_id: int
    first: int
    second: int


@dataclass(frozen=True)
class AccessDisciplineAudit:
    intervals: tuple[RepeatInterval, ...]
    repeat_order: tuple[int, ...]
    first_order: tuple[int, ...]
    laminar_stack: bool
    fifo_queue: bool
    endpoint_deque: bool
    first_deque_failure: int | None


def access_discipline_audit() -> AccessDisciplineAudit:
    """Test strict one-shot stack, queue, and deque repeat disciplines."""

    common = phase_closure_metrics().late_common_length
    signature = late_signatures()[third_axis_roles().loop][:common]
    positions: dict[int, list[int]] = {}
    for position, class_id in enumerate(signature):
        positions.setdefault(class_id, []).append(position)
    intervals = tuple(
        RepeatInterval(class_id, hits[0], hits[1])
        for class_id, hits in positions.items()
        if len(hits) > 1
    )
    repeat_ordered = tuple(
        sorted(intervals, key=lambda interval: interval.second)
    )
    first_ordered = tuple(
        sorted(intervals, key=lambda interval: interval.first)
    )

    def crossing(left: RepeatInterval, right: RepeatInterval) -> bool:
        return (
            left.first < right.first < left.second < right.second
            or right.first < left.first < right.second < left.second
        )

    laminar = not any(
        crossing(left, right)
        for left, right in combinations(intervals, 2)
    )
    repeat_order = tuple(interval.class_id for interval in repeat_ordered)
    first_order = tuple(interval.class_id for interval in first_ordered)

    remaining = list(first_order)
    deque_failure = None
    for class_id in repeat_order:
        if class_id not in (remaining[0], remaining[-1]):
            deque_failure = class_id
            break
        remaining.remove(class_id)

    return AccessDisciplineAudit(
        intervals=tuple(sorted(intervals, key=lambda item: item.class_id)),
        repeat_order=repeat_order,
        first_order=first_order,
        laminar_stack=laminar,
        fifo_queue=repeat_order == first_order,
        endpoint_deque=deque_failure is None,
        first_deque_failure=deque_failure,
    )


@dataclass(frozen=True)
class AffineColumnScreen:
    column: str
    maximum_training_matches: int
    cobest_models: int
    cobest_both_holdouts: int


def affine_column_screen(
    values: Sequence[int],
    *,
    column: str = "plant",
    holdouts: tuple[int, int] = SYSTEMATIC_HOLDOUTS,
) -> AffineColumnScreen:
    """Fit every affine F5²-to-F5 map and score fixed holdouts."""

    values = tuple(values)
    if len(values) != 25 or any(value not in range(5) for value in values):
        raise ValueError("affine column must contain 25 values in F5")
    training = tuple(index for index in range(25) if index not in holdouts)
    maximum = -1
    cobest: list[tuple[int, int, int]] = []
    for row_weight, column_weight, offset in product(range(5), repeat=3):
        predicted = tuple(
            (
                row_weight * (class_id // 5)
                + column_weight * (class_id % 5)
                + offset
            )
            % 5
            for class_id in range(25)
        )
        score = sum(predicted[index] == values[index] for index in training)
        if score > maximum:
            maximum = score
            cobest = [(row_weight, column_weight, offset)]
        elif score == maximum:
            cobest.append((row_weight, column_weight, offset))
    both = 0
    for row_weight, column_weight, offset in cobest:
        if all(
            (
                row_weight * (index // 5)
                + column_weight * (index % 5)
                + offset
            )
            % 5
            == values[index]
            for index in holdouts
        ):
            both += 1
    return AffineColumnScreen(column, maximum, len(cobest), both)


def output_digit_columns() -> dict[str, tuple[int, ...]]:
    columns = {}
    for panel in FINAL_MESSAGES:
        labels = class_labels(panel)
        for eye, weight in enumerate((25, 5, 1)):
            columns[f"{panel}.eye{eye}"] = tuple(
                (labels[class_id] // weight) % 5
                for class_id in SYSTEMATIC_CLASSES
            )
    return columns


@dataclass(frozen=True)
class PairProjection:
    left: str
    right: str
    distinct_pairs: int


@dataclass(frozen=True)
class SystematicCodeAudit:
    affine_screens: tuple[AffineColumnScreen, ...]
    pair_projections: tuple[PairProjection, ...]
    maximum_output_pair_coverage: int
    complete_output_pairs: tuple[PairProjection, ...]


def systematic_code_audit() -> SystematicCodeAudit:
    outputs = output_digit_columns()
    columns: dict[str, tuple[int, ...]] = {
        "input.middle": tuple(index // 5 for index in range(25)),
        "input.third": tuple(index % 5 for index in range(25)),
        **outputs,
    }
    projections = tuple(
        PairProjection(
            left,
            right,
            len(set(zip(columns[left], columns[right], strict=True))),
        )
        for left, right in combinations(columns, 2)
    )
    output_projections = tuple(
        projection
        for projection in projections
        if projection.left in outputs or projection.right in outputs
    )
    maximum = max(
        projection.distinct_pairs for projection in output_projections
    )
    return SystematicCodeAudit(
        affine_screens=tuple(
            affine_column_screen(values, column=name)
            for name, values in outputs.items()
        ),
        pair_projections=projections,
        maximum_output_pair_coverage=maximum,
        complete_output_pairs=tuple(
            projection
            for projection in output_projections
            if projection.distinct_pairs == 25
        ),
    )


@dataclass(frozen=True)
class TransitionCoverAudit:
    length: int
    classes: int
    transitions: int
    distinct_transitions: int
    repeated_transitions: tuple[tuple[tuple[int, int], int], ...]


def transition_cover_audit() -> TransitionCoverAudit:
    common = phase_closure_metrics().late_common_length
    signature = late_signatures()[third_axis_roles().loop][:common]
    counts = Counter(zip(signature, signature[1:]))
    return TransitionCoverAudit(
        length=len(signature),
        classes=len(set(signature)),
        transitions=len(signature) - 1,
        distinct_transitions=len(counts),
        repeated_transitions=tuple(
            sorted((edge, count) for edge, count in counts.items() if count > 1)
        ),
    )


@dataclass(frozen=True)
class AxisMarkerPrediction:
    class_id: int
    source: str
    target: str
    predicted: int
    actual: int

    @property
    def matches(self) -> bool:
        return self.predicted == self.actual


@dataclass(frozen=True)
class AxisMarkerHit:
    class_id: int
    source: str
    target: str
    difference: int
    markers: tuple[str, ...]


@dataclass(frozen=True)
class AxisMarkerAudit:
    labels: tuple[tuple[int, tuple[tuple[str, int], ...]], ...]
    direction_model: tuple[AxisMarkerPrediction, ...]
    scope_model: tuple[AxisMarkerPrediction, ...]
    direction_matches: int
    scope_matches: int
    broad_hits: tuple[AxisMarkerHit, ...]


def axis_marker_audit() -> AxisMarkerAudit:
    """Run the frozen numeric holdout for third-axis classes 2 and 3."""

    roles = third_axis_roles()
    labels = {
        class_id: {
            panel: class_labels(panel)[class_id]
            for panel in FINAL_MESSAGES
        }
        for class_id in (2, 3)
    }

    def difference(class_id: int, source: str, target: str) -> int:
        return (
            labels[class_id][target] - labels[class_id][source]
        ) % MODULUS

    def predictions(
        specs: Sequence[tuple[int, str, str, int]],
    ) -> tuple[AxisMarkerPrediction, ...]:
        return tuple(
            AxisMarkerPrediction(
                class_id,
                source,
                target,
                predicted,
                difference(class_id, source, target),
            )
            for class_id, source, target, predicted in specs
        )

    direction_model = predictions(
        (
            (2, roles.source_mate, roles.loop, 77),
            (3, roles.loop, roles.target_mate, 27),
        )
    )
    scope_model = predictions(
        (
            (2, roles.source_mate, roles.loop, 77),
            (3, roles.target_mate, roles.loop, 36),
        )
    )

    ranks = header_ranks()
    marker_lookup = {
        value: tuple(name for name, rank in ranks.items() if rank == value)
        for value in set(ranks.values())
    }
    broad_hits = tuple(
        AxisMarkerHit(
            class_id,
            source,
            target,
            difference(class_id, source, target),
            marker_lookup[difference(class_id, source, target)],
        )
        for class_id in (2, 3)
        for source in FINAL_MESSAGES
        for target in FINAL_MESSAGES
        if source != target
        and difference(class_id, source, target) in marker_lookup
    )
    return AxisMarkerAudit(
        labels=tuple(
            (
                class_id,
                tuple((panel, labels[class_id][panel]) for panel in FINAL_MESSAGES),
            )
            for class_id in (2, 3)
        ),
        direction_model=direction_model,
        scope_model=scope_model,
        direction_matches=sum(item.matches for item in direction_model),
        scope_matches=sum(item.matches for item in scope_model),
        broad_hits=broad_hits,
    )


@dataclass(frozen=True)
class HeaderScalarBranchObservation:
    header_digits: tuple[tuple[str, tuple[int, int, int]], ...]
    scalar_digits: tuple[tuple[str, int], ...]
    source_scalar: int
    target_scalar: int
    positive_header_digits: tuple[int, ...]
    repeated_third_directions: tuple[int, ...]
    absent_third_directions: tuple[int, ...]
    source_role_matches_scalar: bool
    target_role_matches_scalar: bool
    reciprocal_checks_match_scalars: bool
    used_digit_set_matches_repeats: bool


def header_scalar_branch_observation() -> HeaderScalarBranchObservation:
    """Join final header scalar fields to the label-invariant branch record."""

    roles = third_axis_roles()
    checks = branch_checksum_observation()
    ranks = header_ranks()
    digits = {
        panel: header_base5_digits(ranks[panel])
        for panel in FINAL_MESSAGES
    }
    scalars = {panel: digits[panel][2] for panel in FINAL_MESSAGES}
    source_values = {
        scalars[roles.loop],
        scalars[roles.source_mate],
    }
    if len(source_values) != 1:
        raise AssertionError("source pair does not share a header scalar")
    source_scalar = next(iter(source_values))
    target_scalar = scalars[roles.target_mate]
    positive_header_digits = tuple(
        sorted(
            {
                digit
                for panel_digits in digits.values()
                for digit in panel_digits
                if digit
            }
        )
    )
    repeated = tuple(sorted(roles.role_directions[:3]))
    absent = (roles.role_directions[3],)
    return HeaderScalarBranchObservation(
        header_digits=tuple((panel, digits[panel]) for panel in FINAL_MESSAGES),
        scalar_digits=tuple(
            (panel, scalars[panel]) for panel in FINAL_MESSAGES
        ),
        source_scalar=source_scalar,
        target_scalar=target_scalar,
        positive_header_digits=positive_header_digits,
        repeated_third_directions=repeated,
        absent_third_directions=absent,
        source_role_matches_scalar=(
            roles.role_directions[1] == source_scalar
        ),
        target_role_matches_scalar=(
            roles.role_directions[2] == target_scalar
        ),
        reciprocal_checks_match_scalars=(
            checks.observed_differences
            == (target_scalar, source_scalar)
        ),
        used_digit_set_matches_repeats=(
            positive_header_digits == repeated
        ),
    )
