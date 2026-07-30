#!/usr/bin/env python3
"""Read-only PE call-graph census for the installed Noita builds.

This deliberately stops at direct x86 ``E8 rel32`` edges and byte-level
references.  It does not execute the game or patch the executable.  The fixed
release addresses are the ones frozen by the existing Eye initializer/atlas
audits; the dev build is still scanned for strings, CodeView metadata, and
the same immediate signatures as a negative control.
"""

from __future__ import annotations

import argparse
import hashlib
import struct
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "src"))
sys.path.insert(0, str(REPOSITORY / "scripts"))

from audit_noita_binary import PEImage, parse_pe  # noqa: E402
from audit_compiled_eye_atlas import binary_signature  # noqa: E402


RELEASE_TARGETS = {
    "atlas_initializer": 0x0061E880,
    "row_renderer": 0x0061EC60,
    "message_initializer": 0x0061ED60,
    "message_parser": 0x0061EAF0,
    "message_draw": 0x0061E5C0,
}


def section_slice(data: bytes, image: PEImage, name: str) -> tuple[bytes, int]:
    section = next(candidate for candidate in image.sections if candidate.name == name)
    return (
        data[section.raw_offset : section.raw_offset + section.raw_size],
        image.image_base + section.virtual_address,
    )


def direct_calls(code: bytes, code_va: int, target_va: int) -> tuple[int, ...]:
    """Find direct near-call sites resolving to ``target_va``."""
    sites: list[int] = []
    for offset in range(len(code) - 4):
        if code[offset] != 0xE8:
            continue
        displacement = struct.unpack_from("<i", code, offset + 1)[0]
        call_va = code_va + offset
        if call_va + 5 + displacement == target_va:
            sites.append(call_va)
    return tuple(sites)


def va_to_offset(data: bytes, image: PEImage, address: int) -> int | None:
    for section in image.sections:
        start = image.image_base + section.virtual_address
        if start <= address < start + section.raw_size:
            return section.raw_offset + address - start
    return None


def codeview_record(data: bytes, image: PEImage) -> tuple[str, str] | None:
    """Return (GUID/age, PDB path) from the PE debug directory, if present."""
    pe_offset = struct.unpack_from("<I", data, 0x3C)[0]
    coff = pe_offset + 4
    optional = coff + 20
    magic = struct.unpack_from("<H", data, optional)[0]
    data_directory = optional + (96 if magic == 0x10B else 112)
    debug_rva, debug_size = struct.unpack_from("<II", data, data_directory + 6 * 8)
    debug_offset = va_to_offset(data, image, image.image_base + debug_rva)
    if debug_offset is None:
        return None
    for offset in range(debug_offset, debug_offset + debug_size, 28):
        _characteristics, _timestamp, _major, _minor, kind, size, _rva, raw = (
            struct.unpack_from("<IIHHIIII", data, offset)
        )
        if kind != 2 or data[raw : raw + 4] != b"RSDS":
            continue
        guid = data[raw + 4 : raw + 20].hex()
        age = struct.unpack_from("<I", data, raw + 20)[0]
        end = data.find(b"\0", raw + 24, raw + size)
        if end < 0:
            end = raw + size
        path = data[raw + 24 : end].decode("utf-8", errors="replace")
        return f"{guid}/age{age}", path
    return None


def occurrence_offsets(data: bytes, needle: bytes) -> tuple[int, ...]:
    offsets: list[int] = []
    start = 0
    while True:
        offset = data.find(needle, start)
        if offset < 0:
            return tuple(offsets)
        offsets.append(offset)
        start = offset + 1


def xrefs(data: bytes, image: PEImage, string_offset: int) -> tuple[int, ...]:
    address = None
    for section in image.sections:
        if section.raw_offset <= string_offset < section.raw_offset + section.raw_size:
            address = image.image_base + section.virtual_address + string_offset - section.raw_offset
            break
    if address is None:
        return ()
    pattern = struct.pack("<I", address)
    return tuple(
        image.describe_offset(offset)
        for offset in occurrence_offsets(data, pattern)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("executables", type=Path, nargs="+")
    args = parser.parse_args()

    for path in args.executables:
        data = path.read_bytes()
        image = parse_pe(data)
        text, text_va = section_slice(data, image, ".text")
        print(path)
        print(f"  sha256={hashlib.sha256(data).hexdigest()}")
        print(f"  image_base=0x{image.image_base:x} coff_timestamp=0x{image.timestamp:08x}")
        print(f"  codeview={codeview_record(data, image)!r}")
        if path.name.lower() == "noita.exe":
            for name, target in RELEASE_TARGETS.items():
                sites = direct_calls(text, text_va, target)
                formatted = ",".join(f"0x{site:08x}" for site in sites) or "none"
                print(f"  direct_calls[{name}]=[{formatted}]")
        # The compiler emits these 64-bit values as paired 32-bit stores, so
        # a raw qword scan is not a meaningful signature.  Reuse the existing
        # instruction-aware atlas detector instead; its 0/positive counts are
        # useful for comparing the release and dev builds.
        signatures = binary_signature(data)
        atlas_present = sum(value > 0 for value in signatures.values())
        print(f"  atlas_instruction_signature_fields={atlas_present}/{len(signatures)}")
        print(
            "  atlas_signature_counts="
            + " ".join(f"{key}:{value}" for key, value in signatures.items())
        )
        for needle in (
            b"data/particles/eye.xml",
            b"ThreeEyesAreWatchingYou",
            b"SecretsOfTheAllSeeing",
            b"DEBUG_TEST_SYMBOL_CLASSIFIER",
        ):
            records = []
            for offset in occurrence_offsets(data, needle):
                records.append((image.describe_offset(offset), xrefs(data, image, offset)))
            if records:
                print(f"  string[{needle.decode()}]={records}")


if __name__ == "__main__":
    main()
