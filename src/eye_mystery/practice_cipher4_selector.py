"""Small selector-controlled walks for sdlwdr practice cipher 4."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from itertools import product

from eye_mystery.practice_cipher4_bijection import CaseNgrams


@dataclass(frozen=True)
class SelectorLaw:
    kind: str
    width: int
    offset: int = 0
    table: tuple[int, ...] = ()
    initial_direction: int = 1
    toggle_before: bool = True

    @property
    def name(self) -> str:
        parts = [self.kind, f"w{self.width}", f"o{self.offset:+d}"]
        if self.table:
            parts.append("t" + ",".join(f"{value:+d}" for value in self.table))
        if self.kind == "toggle":
            parts.append(f"d{self.initial_direction:+d}")
            parts.append("before" if self.toggle_before else "after")
        return ":".join(parts)


def selector_laws(width: int, offsets: Iterable[int] = (-1, 0, 1)) -> tuple[SelectorLaw, ...]:
    """Enumerate the frozen unsigned/sign/carry/toggle/lane families."""

    if width not in (2, 3):
        raise ValueError("only the observed pair and triple widths are supported")
    laws = [SelectorLaw("direct", width)]
    for offset in offsets:
        laws.append(SelectorLaw("unsigned", width, offset))
        for table in product((-1, 1), repeat=width):
            laws.append(SelectorLaw("signed", width, offset, tuple(table)))
        for table in product((0, 1), repeat=width):
            laws.append(SelectorLaw("carry", width, offset, tuple(table)))
        for mask in range(1, 1 << width):
            table = tuple(int(bool(mask & (1 << selector))) for selector in range(width))
            for initial_direction in (-1, 1):
                for toggle_before in (False, True):
                    laws.append(
                        SelectorLaw(
                            "toggle",
                            width,
                            offset,
                            table,
                            initial_direction,
                            toggle_before,
                        )
                    )
        laws.append(SelectorLaw("lanes", width, offset))
    return tuple(laws)


def decode_selector_walk(
    ranks: Sequence[int], modulus: int, law: SelectorLaw
) -> tuple[int, ...]:
    """Decode one quotient/remainder walk on ``Z/modulus``."""

    if modulus < 2:
        raise ValueError("modulus must be at least two")
    if any(rank not in range(57) for rank in ranks):
        raise ValueError("ranks must lie in 0..56")

    accumulator = 0
    direction = law.initial_direction
    lanes = [0] * law.width
    output = []
    for rank in ranks:
        quotient, selector = divmod(rank, law.width)
        if law.kind == "direct":
            value = quotient % modulus
        elif law.kind == "unsigned":
            accumulator = (accumulator + quotient + law.offset) % modulus
            value = accumulator
        elif law.kind == "signed":
            accumulator = (
                accumulator + law.table[selector] * (quotient + law.offset)
            ) % modulus
            value = accumulator
        elif law.kind == "carry":
            accumulator = (
                accumulator + quotient + law.offset + law.table[selector]
            ) % modulus
            value = accumulator
        elif law.kind == "toggle":
            should_toggle = bool(law.table[selector])
            if should_toggle and law.toggle_before:
                direction *= -1
            accumulator = (
                accumulator + direction * (quotient + law.offset)
            ) % modulus
            value = accumulator
            if should_toggle and not law.toggle_before:
                direction *= -1
        elif law.kind == "lanes":
            lanes[selector] = (
                lanes[selector] + quotient + law.offset
            ) % modulus
            value = lanes[selector]
        else:
            raise ValueError(f"unknown selector law: {law.kind}")
        output.append(value)
    return tuple(output)


@dataclass(frozen=True)
class RenderedWalk:
    score: float
    score_per_gram: float
    directions: tuple[int, ...]
    shifts: tuple[int, ...]
    texts: tuple[str, ...]


def best_affine_render(
    streams: Sequence[Sequence[int]],
    alphabet: str,
    model: CaseNgrams,
    *,
    independent_portion_shifts: bool,
) -> RenderedWalk:
    """Render coordinate streams under ring reflection and rotation."""

    modulus = len(alphabet)
    if not streams:
        raise ValueError("at least one stream is required")
    if any(value not in range(modulus) for stream in streams for value in stream):
        raise ValueError("coordinates must fit the alphabet")

    def render(stream: Sequence[int], direction: int, shift: int) -> str:
        return "".join(
            alphabet[(direction * value + shift) % modulus] for value in stream
        )

    if independent_portion_shifts:
        scores = []
        directions = []
        shifts = []
        texts = []
        for stream in streams:
            best = max(
                (
                    model.score(render(stream, direction, shift)),
                    direction,
                    shift,
                    render(stream, direction, shift),
                )
                for direction in (-1, 1)
                for shift in range(modulus)
            )
            score, direction, shift, text = best
            scores.append(score)
            directions.append(direction)
            shifts.append(shift)
            texts.append(text)
        total_score = sum(scores)
    else:
        total_score, direction, shift, texts = max(
            (
                sum(model.score(text) for text in candidate_texts),
                direction,
                shift,
                candidate_texts,
            )
            for direction in (-1, 1)
            for shift in range(modulus)
            for candidate_texts in (
                tuple(render(stream, direction, shift) for stream in streams),
            )
        )
        directions = [direction] * len(streams)
        shifts = [shift] * len(streams)

    grams = sum(max(0, len(stream) - model.order + 1) for stream in streams)
    return RenderedWalk(
        total_score,
        total_score / grams if grams else float("-inf"),
        tuple(directions),
        tuple(shifts),
        tuple(texts),
    )


def encode_unsigned_walk(
    plaintext: Sequence[int],
    *,
    width: int,
    modulus: int,
    selectors: Sequence[int],
    initial: int = 0,
) -> tuple[int, ...]:
    """Plant a quotient walk, used to verify the finite search."""

    if len(plaintext) != len(selectors):
        raise ValueError("plaintext and selector lengths differ")
    previous = initial
    ranks = []
    for value, selector in zip(plaintext, selectors, strict=True):
        if value not in range(modulus):
            raise ValueError("plaintext coordinate is outside the ring")
        if selector not in range(width):
            raise ValueError("selector is outside the declared width")
        quotient = (value - previous) % modulus
        rank = width * quotient + selector
        if rank not in range(57):
            raise ValueError("planted walk does not fit the observed rank band")
        ranks.append(rank)
        previous = value
    return tuple(ranks)
