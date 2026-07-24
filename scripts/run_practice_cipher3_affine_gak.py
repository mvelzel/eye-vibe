#!/usr/bin/env python3
"""Run the frozen affine GAK batch for sdlwdr practice Cipher 3."""

from __future__ import annotations

import argparse

from eye_mystery.practice_cipher3_affine_gak import (
    MODES,
    named_group,
    replay_exact_model,
    solve_exact_affine_gak,
    structured_search,
)
from eye_mystery.practice_cipher3_wide import GROUPS, load_cipher3


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--exact-groups",
        choices=(*GROUPS, "all"),
        nargs="*",
        default=(),
    )
    parser.add_argument(
        "--exact-modes",
        choices=MODES,
        nargs="*",
        default=(),
    )
    parser.add_argument("--max-symbols", type=int, default=42)
    parser.add_argument("--timeout-ms", type=int, default=30_000)
    parser.add_argument("--skip-structured", action="store_true")
    args = parser.parse_args()

    streams = load_cipher3()
    if not args.skip_structured:
        result = structured_search(streams)
        print("structured catalog")
        print(result)

    for group_name in args.exact_groups:
        groups = GROUPS if group_name == "all" else (group_name,)
        messages = named_group(streams, groups)
        for mode in args.exact_modes:
            print(
                f"exact group={group_name} mode={mode} "
                f"alphabet<={args.max_symbols}"
            )
            result = solve_exact_affine_gak(
                messages,
                mode=mode,
                max_symbols=args.max_symbols,
                timeout_ms=args.timeout_ms,
            )
            print(
                result.status,
                result.reason,
                f"realized={len(result.realized_states)}",
                f"replay={replay_exact_model(result, messages, mode=mode)}",
            )
            if result.status == "sat":
                print("states", result.realized_states)
                print("updates", result.update_exponents)
                for name, state_stream in result.state_streams:
                    print(name, " ".join(map(str, state_stream)))


if __name__ == "__main__":
    main()
