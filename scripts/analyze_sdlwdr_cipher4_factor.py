#!/usr/bin/env python3
"""Screen both 3-by-19 factorizations of sdlwdr practice cipher 4."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from eye_mystery.practice_cipher4 import cyclic_differences
from eye_mystery.practice_cipher4_factor import (
    contiguous_width_screen,
    difference_ladder,
    entropy,
    label_shuffle_audit,
    normalized_ioc,
    serial_shuffle_audit,
)


ROOT = Path(__file__).resolve().parents[1]


def render_audit(name: str, audit) -> None:
    print(
        f"  {name}: observed={audit.observed:.9f} "
        f"null={audit.null_minimum:.9f}..{audit.null_maximum:.9f} "
        f"mean={audit.null_mean:.9f} "
        f"lower={audit.lower_tail:.9f} upper={audit.upper_tail:.9f}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        type=Path,
        default=ROOT / "artifacts/practice-sdlwdr/cipher4.json",
    )
    parser.add_argument("--controls", type=int, default=5_000)
    parser.add_argument("--label-controls", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=0x53444C5744520403)
    args = parser.parse_args()

    messages = json.loads(args.data.read_text())
    ranks = tuple(
        tuple(value - 22 for value in cyclic_differences(message))
        for message in messages
    )
    flat = tuple(value for stream in ranks for value in stream)
    if any(value not in range(57) for value in flat):
        raise AssertionError("the difference stream escaped the 57-rank band")

    missing = sorted(set(range(57)) - set(flat))
    print(f"lengths={tuple(map(len, ranks))} missing={missing}")
    print("\ncontiguous quotient/remainder width screen")
    width_rows = contiguous_width_screen(
        ranks,
        widths=tuple(range(2, 29)),
        controls=min(args.controls, 500),
        seed=args.seed ^ 0x571D7,
    )
    for row in sorted(width_rows, key=lambda item: item.remainder_excess):
        print(
            f"  width={row.width:>2} q_symbols={row.quotient_symbols:>2} "
            f"r_symbols={row.remainder_symbols:>2} "
            f"q_mi={row.quotient_observed:.6f} "
            f"q_excess={row.quotient_excess:+.6f} "
            f"r_mi={row.remainder_observed:.6f} "
            f"r_excess={row.remainder_excess:+.6f}"
        )
    for name, quotient_divisor, quotient_size, remainder_size in (
        ("29 payload x 2 selector", 2, 29, 2),
        ("19 payload x 3 selector", 3, 19, 3),
        ("3 selector x 19 payload", 19, 3, 19),
    ):
        quotient = tuple(
            tuple(value // quotient_divisor for value in stream)
            for stream in ranks
        )
        remainder = tuple(
            tuple(value % quotient_divisor for value in stream)
            for stream in ranks
        )
        print(f"\n{name}")
        for component_name, streams, size in (
            ("quotient", quotient, quotient_size),
            ("remainder", remainder, remainder_size),
        ):
            values = tuple(value for stream in streams for value in stream)
            print(
                f"  {component_name}: symbols={len(set(values))} "
                f"entropy={entropy(values):.9f} "
                f"normalized_ioc={normalized_ioc(values, size):.9f} "
                f"counts={sorted(Counter(values).items())}"
            )
            render_audit(
                f"{component_name} serial-MI pooled",
                serial_shuffle_audit(
                    streams,
                    controls=args.controls,
                    seed=args.seed ^ quotient_divisor ^ size,
                ),
            )
            for index, stream in enumerate(streams):
                render_audit(
                    f"{component_name} serial-MI portion{index + 1}",
                    serial_shuffle_audit(
                        (stream,),
                        controls=args.controls,
                        seed=args.seed ^ quotient_divisor ^ size ^ index ^ 0x51,
                    ),
                )
        render_audit(
            "coordinate-MI under random label order",
            label_shuffle_audit(
                flat,
                divisor=quotient_divisor,
                controls=args.label_controls,
                seed=args.seed ^ quotient_divisor ^ 0x1ABE1,
            ),
        )

    for width, modulus in ((2, 29), (3, 19)):
        payload = tuple(
            tuple(value // width for value in stream) for stream in ranks
        )
        print(f"\n{modulus}-symbol payload finite-difference ladder")
        for order, layer in enumerate(
            difference_ladder(payload, modulus=modulus, orders=8)
        ):
            values = tuple(value for stream in layer for value in stream)
            print(
                f"  order={order} symbols={len(set(values))} "
                f"entropy={entropy(values):.9f} "
                f"normalized_ioc={normalized_ioc(values, modulus):.9f}"
            )


if __name__ == "__main__":
    main()
