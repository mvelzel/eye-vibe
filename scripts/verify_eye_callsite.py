#!/usr/bin/env python3
"""Verify the 2025 Eye initializer's compiled caller interface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "src"))

from eye_mystery.binary_initializer import audit_eye_callsite  # noqa: E402

from audit_noita_binary import parse_pe  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("executable", type=Path)
    args = parser.parse_args()

    data = args.executable.read_bytes()
    image = parse_pe(data)
    section = next(
        (candidate for candidate in image.sections if candidate.name == ".text"),
        None,
    )
    if section is None:
        raise SystemExit("PE executable has no .text section")
    text = data[
        section.raw_offset : section.raw_offset + section.raw_size
    ]
    text_va = image.image_base + section.virtual_address
    audit = audit_eye_callsite(text, text_va)

    calls = ",".join(f"0x{address:08x}" for address in audit.direct_call_sites)
    print(f"direct_initializer_calls={len(audit.direct_call_sites)} [{calls}]")
    print(f"callsite_va={audit.callsite_va and f'0x{audit.callsite_va:08x}'}")
    print(
        "initializer_arguments="
        f"{audit.initializer_argument_signature} "
        "(ecx=x, edx=y, stack=panel_index)"
    )
    print(
        "panel_index_loop="
        f"{audit.panel_index_loop_signature} (0..8)"
    )
    print(
        "side_parity_filter="
        f"{audit.side_filter_signature} "
        "(+1 keeps even five, -1 keeps odd four)"
    )
    print(f"coordinate_callsite={audit.coordinate_argument_signature}")
    print(f"exact_position_index_interface={audit.exact_interface}")
    if not audit.exact_interface:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
