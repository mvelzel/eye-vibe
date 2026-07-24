"""Bounded inventory of numeric salts that feed Noita's ``SetRandomSeed``."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal
import re

from .calling_codes import geographic_regions
from .wak import WakArchive


MARKER_PLANE_CODES = frozenset((34, 358, 683))
ARITHMETIC_OPERATORS = frozenset("+-*/%^&|")

_CALL = re.compile(r"\bSetRandomSeed\s*\(")
_IDENTIFIER = re.compile(r"^[A-Za-z_]\w*$")
_NUMBER = r"(?:\d+(?:\.\d*)?|\.\d+)"
_RIGHT_SALT = re.compile(rf"([+-])\s*({_NUMBER})")
_LEFT_ADDITION = re.compile(rf"(?<![\w.])([+-]?{_NUMBER})\s*\+")


@dataclass(frozen=True)
class RngSaltCall:
    """One executable SetRandomSeed call and salts reaching its arguments."""

    path: str
    line: int
    arguments: tuple[str, str]
    salts: tuple[tuple[Decimal, ...], tuple[Decimal, ...]]

    @property
    def recipe(self) -> tuple[tuple[Decimal, ...], tuple[Decimal, ...]]:
        return self.salts

    @property
    def integer_parts(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        first, second = self.salts
        return (
            tuple(abs(int(value)) for value in first),
            tuple(abs(int(value)) for value in second),
        )

    @property
    def marker_codes(self) -> tuple[int, ...]:
        return tuple(
            value
            for argument in self.integer_parts
            for value in argument
            if value in MARKER_PLANE_CODES
        )

    @property
    def is_geographic_pair(self) -> bool:
        parts = self.integer_parts
        return (
            len(parts[0]) == 1
            and len(parts[1]) == 1
            and bool(geographic_regions(parts[0][0]))
            and bool(geographic_regions(parts[1][0]))
        )

    def eye_ascii_pair(
        self, *, absolute: bool = False, reverse: bool = False
    ) -> str | None:
        """Map one salt per argument through signed integer mod 83 and ASCII+32."""

        if any(len(argument) != 1 for argument in self.salts):
            return None
        values = tuple(int(argument[0]) for argument in self.salts)
        if absolute:
            values = tuple(abs(value) for value in values)
        if reverse:
            values = tuple(reversed(values))
        return "".join(chr(value % 83 + 32) for value in values)

    def is_compact_arithmetic_instruction(
        self, *, absolute: bool = False, reverse: bool = False
    ) -> bool:
        text = self.eye_ascii_pair(absolute=absolute, reverse=reverse)
        return (
            text is not None
            and text[0] in ARITHMETIC_OPERATORS
            and text[1].isdigit()
            and text[1].isascii()
        )


def _strip_line_comment(line: str) -> str:
    """Remove a Lua line comment while respecting simple quoted strings."""

    quote: str | None = None
    escaped = False
    index = 0
    while index < len(line):
        char = line[index]
        if escaped:
            escaped = False
        elif char == "\\" and quote is not None:
            escaped = True
        elif quote is not None:
            if char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
        elif char == "-" and index + 1 < len(line) and line[index + 1] == "-":
            return line[:index]
        index += 1
    return line


def _split_arguments(body: str) -> tuple[str, str] | None:
    depth = 0
    quote: str | None = None
    escaped = False
    split_at = None
    for index, char in enumerate(body):
        if escaped:
            escaped = False
        elif char == "\\" and quote is not None:
            escaped = True
        elif quote is not None:
            if char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "," and depth == 0:
            if split_at is not None:
                return None
            split_at = index
    if split_at is None:
        return None
    return body[:split_at].strip(), body[split_at + 1 :].strip()


def _calls(text: str) -> tuple[tuple[int, tuple[str, str]], ...]:
    lines = text.splitlines()
    stripped = "\n".join(_strip_line_comment(line) for line in lines)
    found = []
    for match in _CALL.finditer(stripped):
        depth = 1
        quote: str | None = None
        escaped = False
        index = match.end()
        while index < len(stripped) and depth:
            char = stripped[index]
            if escaped:
                escaped = False
            elif char == "\\" and quote is not None:
                escaped = True
            elif quote is not None:
                if char == quote:
                    quote = None
            elif char in ("'", '"'):
                quote = char
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            index += 1
        if depth:
            continue
        arguments = _split_arguments(stripped[match.end() : index - 1])
        if arguments is None:
            continue
        line = stripped.count("\n", 0, match.start()) + 1
        found.append((line, arguments))
    return tuple(found)


def _direct_salts(expression: str) -> tuple[Decimal, ...]:
    view = []
    depth = 0
    quote: str | None = None
    escaped = False
    for char in expression:
        if escaped:
            escaped = False
            view.append(" ")
        elif char == "\\" and quote is not None:
            escaped = True
            view.append(" ")
        elif quote is not None:
            if char == quote:
                quote = None
            view.append(" ")
        elif char in ("'", '"'):
            quote = char
            view.append(" ")
        elif char in "([{":
            depth += 1
            view.append(" ")
        elif char in ")]}":
            depth = max(0, depth - 1)
            view.append(" ")
        else:
            view.append(char if depth == 0 else " ")
    top_level = "".join(view)

    salts = []
    for match in _RIGHT_SALT.finditer(top_level):
        sign, number = match.groups()
        value = Decimal(number)
        salts.append(value if sign == "+" else -value)
    for match in _LEFT_ADDITION.finditer(top_level):
        prefix = top_level[: match.start()].rstrip()
        if not prefix or prefix[-1] in "([{,":
            salts.append(Decimal(match.group(1)))
    return tuple(salts)


def _traced_salts(
    lines: tuple[str, ...],
    call_line: int,
    variable: str,
    *,
    window: int = 12,
) -> tuple[Decimal, ...]:
    assignment = re.compile(
        rf"^\s*(?:local\s+)?{re.escape(variable)}\s*=\s*(.*?)\s*$"
    )
    self_right = re.compile(
        rf"^{re.escape(variable)}\s*([+-])\s*({_NUMBER})$"
    )
    self_left = re.compile(
        rf"^({_NUMBER})\s*\+\s*{re.escape(variable)}$"
    )
    lower = max(0, call_line - 1 - window)
    for raw in reversed(lines[lower : call_line - 1]):
        code = _strip_line_comment(raw).strip()
        match = assignment.match(code)
        if match is None:
            continue
        right = match.group(1).strip()
        right_match = self_right.match(right)
        if right_match:
            sign, number = right_match.groups()
            value = Decimal(number)
            return (value if sign == "+" else -value,)
        left_match = self_left.match(right)
        if left_match:
            return (Decimal(left_match.group(1)),)
        return ()
    return ()


def scan_rng_locale_salts(
    files: Iterable[tuple[str, str]],
) -> tuple[RngSaltCall, ...]:
    """Scan Lua files using the frozen direct-plus-short-trace grammar."""

    hits = []
    for path, text in files:
        lines = tuple(text.splitlines())
        for line, arguments in _calls(text):
            salts = []
            for argument in arguments:
                direct = _direct_salts(argument)
                if direct:
                    salts.append(direct)
                elif _IDENTIFIER.fullmatch(argument):
                    salts.append(_traced_salts(lines, line, argument))
                else:
                    salts.append(())
            hits.append(RngSaltCall(path, line, arguments, (salts[0], salts[1])))
    return tuple(hits)


def scan_wak_rng_locale_salts(archive: WakArchive) -> tuple[RngSaltCall, ...]:
    """Scan every Lua entry in a WAK archive."""

    return scan_rng_locale_salts(
        (
            (entry.path, archive.read(entry).decode("utf-8", errors="ignore"))
            for entry in archive.entries
            if entry.path.lower().endswith(".lua")
        )
    )
