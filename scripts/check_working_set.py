#!/usr/bin/env python3
"""Validate the compact, repository-local resumption documents."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIMITS = {
    ROOT / "AGENTS.md": 90,
    ROOT / "docs/working-set/README.md": 80,
    ROOT / "docs/working-set/current-state.md": 230,
    ROOT / "docs/working-set/next-actions.md": 200,
    ROOT / "docs/working-set/evidence-map.md": 180,
}
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def validate() -> tuple[str, ...]:
    errors: list[str] = []
    for path, limit in LIMITS.items():
        if not path.is_file():
            errors.append(f"missing required working-set file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        lines = len(text.splitlines())
        if lines > limit:
            errors.append(
                f"{path.relative_to(ROOT)} has {lines} lines; limit is {limit}"
            )
        for target in LINK.findall(text):
            if "://" in target or target.startswith("#"):
                continue
            relative = target.split("#", 1)[0]
            resolved = (path.parent / relative).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(
                    f"{path.relative_to(ROOT)} links outside repository: {target}"
                )
                continue
            if not resolved.exists():
                errors.append(
                    f"{path.relative_to(ROOT)} has missing link target: {target}"
                )
    return tuple(errors)


def main() -> None:
    errors = validate()
    if errors:
        raise SystemExit("\n".join(errors))
    print("working set: OK")
    for path, limit in LIMITS.items():
        lines = len(path.read_text(encoding="utf-8").splitlines())
        print(f"  {path.relative_to(ROOT)}: {lines}/{limit} lines")


if __name__ == "__main__":
    main()

