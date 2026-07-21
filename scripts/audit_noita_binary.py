#!/usr/bin/env python3
"""Locate Eye-message and CRC constants in installed Noita executables.

This is a read-only binary audit.  It reports raw file offsets and maps them to
PE sections/virtual addresses so that hits in executable code can be separated
from lookup tables or other static data.
"""

from __future__ import annotations

import argparse
import hashlib
import struct
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Section:
    name: str
    virtual_address: int
    virtual_size: int
    raw_offset: int
    raw_size: int


@dataclass(frozen=True)
class PEImage:
    image_base: int
    timestamp: int
    sections: tuple[Section, ...]

    def describe_offset(self, offset: int) -> str:
        for section in self.sections:
            if section.raw_offset <= offset < section.raw_offset + section.raw_size:
                delta = offset - section.raw_offset
                address = self.image_base + section.virtual_address + delta
                return f"{section.name}+0x{delta:x} VA=0x{address:08x}"
        return "outside-sections"


def parse_pe(data: bytes) -> PEImage:
    if data[:2] != b"MZ":
        raise ValueError("not an MZ executable")
    pe_offset = struct.unpack_from("<I", data, 0x3C)[0]
    if data[pe_offset : pe_offset + 4] != b"PE\0\0":
        raise ValueError("missing PE signature")
    coff = pe_offset + 4
    section_count = struct.unpack_from("<H", data, coff + 2)[0]
    timestamp = struct.unpack_from("<I", data, coff + 4)[0]
    optional_size = struct.unpack_from("<H", data, coff + 16)[0]
    optional = coff + 20
    magic = struct.unpack_from("<H", data, optional)[0]
    if magic != 0x10B:
        raise ValueError(f"expected PE32 optional header, got 0x{magic:x}")
    image_base = struct.unpack_from("<I", data, optional + 28)[0]
    section_table = optional + optional_size
    sections = []
    for index in range(section_count):
        header = section_table + 40 * index
        name = data[header : header + 8].split(b"\0", 1)[0].decode("ascii")
        virtual_size, virtual_address, raw_size, raw_offset = struct.unpack_from(
            "<IIII", data, header + 8
        )
        sections.append(
            Section(name, virtual_address, virtual_size, raw_offset, raw_size)
        )
    return PEImage(image_base, timestamp, tuple(sections))


def crc_table(*, polynomial: int, reflected: bool) -> tuple[int, ...]:
    table = []
    for byte in range(256):
        value = byte if reflected else byte << 24
        for _ in range(8):
            if reflected:
                value = (value >> 1) ^ (polynomial if value & 1 else 0)
            else:
                value = ((value << 1) & 0xFFFFFFFF) ^ (
                    polynomial if value & 0x80000000 else 0
                )
        table.append(value & 0xFFFFFFFF)
    return tuple(table)


def occurrences(data: bytes, pattern: bytes) -> tuple[int, ...]:
    result = []
    start = 0
    while True:
        offset = data.find(pattern, start)
        if offset < 0:
            return tuple(result)
        result.append(offset)
        start = offset + 1


def patterns() -> tuple[tuple[str, bytes], ...]:
    bzip2 = crc_table(polynomial=0x04C11DB7, reflected=False)
    iso_hdlc = crc_table(polynomial=0xEDB88320, reflected=True)
    result = [
        ("Eye first packed word LE", struct.pack("<Q", 0xACF686745634505C)),
        ("Eye first packed word BE", struct.pack(">Q", 0xACF686745634505C)),
        ("Eye/LUMIKKI half LE", struct.pack("<I", 0xACF68674)),
        ("Eye/LUMIKKI half BE", struct.pack(">I", 0xACF68674)),
        ("CRC-32/BZIP2 polynomial LE", struct.pack("<I", 0x04C11DB7)),
        ("CRC-32/BZIP2 polynomial BE", struct.pack(">I", 0x04C11DB7)),
        ("CRC-32/ISO-HDLC polynomial LE", struct.pack("<I", 0xEDB88320)),
        ("CRC-32/ISO-HDLC polynomial BE", struct.pack(">I", 0xEDB88320)),
        ("lumikki ASCII", b"lumikki"),
        ("LUMIKKI ASCII", b"LUMIKKI"),
        ("lumikki UTF-16LE", "lumikki".encode("utf-16le")),
    ]
    eye_halves = (
        0x5634505C,
        0xACF68674,
        0x2C9AC076,
        0x981E2346,
        0x2E474A1F,
        0x29848A73,
        0xC220213A,
        0x75A31019,
        0x01FECF4E,
        0x2C7AA564,
        0x2BF7569A,
        0xF9B307F9,
    )
    for index, value in enumerate(eye_halves):
        result.append(
            (f"Eye opening half {index:02d} LE 0x{value:08x}", struct.pack("<I", value))
        )
    for name, table in (("CRC-32/BZIP2", bzip2), ("CRC-32/ISO-HDLC", iso_hdlc)):
        for count in (256, 16, 8, 4):
            result.append(
                (
                    f"{name} table first {count} LE words",
                    struct.pack(f"<{count}I", *table[:count]),
                )
            )
            result.append(
                (
                    f"{name} table first {count} BE words",
                    struct.pack(f">{count}I", *table[:count]),
                )
            )
    return tuple(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("executables", type=Path, nargs="+")
    args = parser.parse_args()
    for path in args.executables:
        data = path.read_bytes()
        image = parse_pe(data)
        print(path)
        print(f"  bytes={len(data)} sha256={hashlib.sha256(data).hexdigest()}")
        print(
            f"  image_base=0x{image.image_base:x} coff_timestamp=0x{image.timestamp:08x}"
        )
        print(
            "  sections:",
            " ".join(
                f"{section.name}[raw=0x{section.raw_offset:x}+0x{section.raw_size:x},"
                f"rva=0x{section.virtual_address:x}]"
                for section in image.sections
            ),
        )
        for name, pattern in patterns():
            hits = occurrences(data, pattern)
            if hits:
                locations = ", ".join(
                    f"0x{offset:x} ({image.describe_offset(offset)})"
                    for offset in hits[:20]
                )
                suffix = " ..." if len(hits) > 20 else ""
                print(f"  {name}: {len(hits)} hit(s): {locations}{suffix}")
        print()


if __name__ == "__main__":
    main()
