"""Structural scanners for authored table-like records in Noita text assets."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class LuaTable:
    start: int
    end: int
    item_count: int
    keyed_item_count: int
    assigned_name: str


def mask_lua_literals_and_comments(text: str) -> str:
    """Blank Lua strings/comments while preserving delimiters and positions."""
    output = list(text)
    index = 0
    while index < len(text):
        if text.startswith("--[[", index):
            end = text.find("]]", index + 4)
            end = len(text) if end < 0 else end + 2
            output[index:end] = " " * (end - index)
            index = end
            continue
        if text.startswith("--", index):
            end = text.find("\n", index + 2)
            end = len(text) if end < 0 else end
            output[index:end] = " " * (end - index)
            index = end
            continue
        if text[index] in "'\"":
            quote = text[index]
            cursor = index + 1
            while cursor < len(text):
                if text[cursor] == "\\":
                    cursor += 2
                    continue
                if text[cursor] == quote:
                    cursor += 1
                    break
                cursor += 1
            # Keep one marker so a quoted scalar still counts as an item.
            output[index:cursor] = "S" + " " * (cursor - index - 1)
            index = cursor
            continue
        index += 1
    return "".join(output)


def _top_level_items(masked: str, start: int, end: int) -> tuple[str, ...]:
    items = []
    cursor = start + 1
    item_start = cursor
    curly = round_depth = square = 0
    while cursor < end:
        character = masked[cursor]
        if character == "{":
            curly += 1
        elif character == "}":
            curly -= 1
        elif character == "(":
            round_depth += 1
        elif character == ")":
            round_depth -= 1
        elif character == "[":
            square += 1
        elif character == "]":
            square -= 1
        elif character == "," and not (curly or round_depth or square):
            item = masked[item_start:cursor].strip()
            if item:
                items.append(item)
            item_start = cursor + 1
        cursor += 1
    final = masked[item_start:end].strip()
    if final:
        items.append(final)
    return tuple(items)


def lua_tables(text: str) -> tuple[LuaTable, ...]:
    """Return balanced Lua table literals and their top-level item counts."""
    masked = mask_lua_literals_and_comments(text)
    stack: list[int] = []
    tables = []
    for index, character in enumerate(masked):
        if character == "{":
            stack.append(index)
        elif character == "}" and stack:
            start = stack.pop()
            items = _top_level_items(masked, start, index)
            prefix = masked[max(0, start - 160) : start]
            match = re.search(r"([A-Za-z_][A-Za-z0-9_.]*)\s*=\s*$", prefix)
            tables.append(
                LuaTable(
                    start,
                    index + 1,
                    len(items),
                    sum("=" in item for item in items),
                    match.group(1) if match else "",
                )
            )
    return tuple(sorted(tables, key=lambda table: table.start))


_LUA_QUOTED_STRING = re.compile(r"(?P<quote>['\"])(?:\\.|(?!\1).)*?(?P=quote)")


def assigned_string_list(text: str, name: str) -> tuple[str, ...]:
    """Extract a simple quoted-string array assigned to ``name``.

    This deliberately accepts only an unkeyed table containing one ordinary
    single- or double-quoted scalar per item.  It is an asset-audit helper,
    not a general Lua evaluator.
    """
    candidates = tuple(table for table in lua_tables(text) if table.assigned_name == name)
    if len(candidates) != 1:
        raise ValueError(f"expected one {name!r} table, found {len(candidates)}")
    table = candidates[0]
    if table.keyed_item_count:
        raise ValueError(f"{name!r} is keyed rather than a simple list")
    source = text[table.start + 1 : table.end - 1]
    tokens = tuple(match.group(0) for match in _LUA_QUOTED_STRING.finditer(source))
    if len(tokens) != table.item_count:
        raise ValueError(
            f"{name!r} has {table.item_count} items but {len(tokens)} quoted strings"
        )
    try:
        values = tuple(ast.literal_eval(token) for token in tokens)
    except (SyntaxError, ValueError) as error:
        raise ValueError(f"{name!r} contains a non-Python-compatible Lua string") from error
    if not all(isinstance(value, str) for value in values):
        raise ValueError(f"{name!r} contains a non-string item")
    return values
