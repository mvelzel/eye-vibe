#!/usr/bin/env python3
"""Audit the reported ``0xacf68674 == CRC-32b('lumikki')`` coincidence.

The claim appears in the community progress document.  This script checks the
standard CRC-32 families and the mundane spelling/encoding variations that can
otherwise make hash reports difficult to reproduce.
"""

from __future__ import annotations

import hashlib
import itertools
import unicodedata
import zlib


TARGET = 0xACF68674
FIRST_LOW_WORD = 0x5634505C


def crc32_reflected(data: bytes, polynomial: int, initial: int, final: int) -> int:
    value = initial
    for byte in data:
        value ^= byte
        for _ in range(8):
            value = (value >> 1) ^ (polynomial if value & 1 else 0)
    return (value ^ final) & 0xFFFFFFFF


def crc32_direct(data: bytes, polynomial: int, initial: int, final: int) -> int:
    value = initial
    for byte in data:
        value ^= byte << 24
        for _ in range(8):
            value = ((value << 1) & 0xFFFFFFFF) ^ (
                polynomial if value & 0x80000000 else 0
            )
    return (value ^ final) & 0xFFFFFFFF


CRC_MODELS = {
    "CRC-32/ISO-HDLC (CRC-32b)": lambda data: crc32_reflected(
        data, 0xEDB88320, 0xFFFFFFFF, 0xFFFFFFFF
    ),
    "CRC-32/JAMCRC": lambda data: crc32_reflected(
        data, 0xEDB88320, 0xFFFFFFFF, 0
    ),
    "CRC-32/ISO init=0": lambda data: crc32_reflected(
        data, 0xEDB88320, 0, 0
    ),
    "CRC-32/ISO init=0 xorout=all": lambda data: crc32_reflected(
        data, 0xEDB88320, 0, 0xFFFFFFFF
    ),
    "CRC-32C/Castagnoli": lambda data: crc32_reflected(
        data, 0x82F63B78, 0xFFFFFFFF, 0xFFFFFFFF
    ),
    "CRC-32/BZIP2": lambda data: crc32_direct(
        data, 0x04C11DB7, 0xFFFFFFFF, 0xFFFFFFFF
    ),
    "CRC-32/MPEG-2": lambda data: crc32_direct(
        data, 0x04C11DB7, 0xFFFFFFFF, 0
    ),
    "CRC-32/POSIX": lambda data: crc32_direct(
        data, 0x04C11DB7, 0, 0xFFFFFFFF
    ),
}


def candidate_bytes():
    spellings = {
        "lumikki",
        "Lumikki",
        "LUMIKKI",
        "snow white",
        "Snow White",
        "SNOW WHITE",
        "snowwhite",
        "SnowWhite",
        "SNOWWHITE",
    }
    encodings = ("utf-8", "utf-16le", "utf-16be", "utf-32le", "utf-32be")
    suffixes = ("", "\n", "\r\n", "\0")
    for spelling, encoding, suffix in itertools.product(
        sorted(spellings), encodings, suffixes
    ):
        text = unicodedata.normalize("NFC", spelling + suffix)
        yield f"{spelling!r}+{suffix!r}/{encoding}", text.encode(encoding)


def main() -> None:
    standard = zlib.crc32(b"lumikki")
    print(f"target                       {TARGET:08x}")
    print(f"CRC-32b('lumikki')           {standard:08x}")
    print(f"target byte-reversed         {int.from_bytes(TARGET.to_bytes(4, 'big'), 'little'):08x}")

    packed = (TARGET << 32) | FIRST_LOW_WORD
    digits = []
    value = packed
    while value:
        digits.append(value % 7)
        value //= 7
    digits.reverse()
    print(f"first packed 64-bit word      {packed:016x}")
    print(f"base-7 digits                 {''.join(map(str, digits))}")
    print(
        "visible stored digits         "
        f"{len(digits) - 1} (trailing padding={digits[-1]})"
    )
    print(f"7^22 < 2^64 < 7^23           {7**22 < 2**64 < 7**23}")

    matches: list[tuple[str, str]] = []
    digest_matches: list[tuple[str, str]] = []
    for description, data in candidate_bytes():
        for model, function in CRC_MODELS.items():
            value = function(data)
            if value == TARGET or value.to_bytes(4, "big")[::-1] == TARGET.to_bytes(4, "big"):
                matches.append((description, model))
        for algorithm in hashlib.algorithms_guaranteed:
            digest_object = hashlib.new(algorithm, data)
            digest = (
                digest_object.digest(64)
                if algorithm.startswith("shake_")
                else digest_object.digest()
            )
            target = TARGET.to_bytes(4, "big")
            if target in digest or target[::-1] in digest:
                digest_matches.append((description, algorithm))

    print(f"CRC matches in candidate grid  {len(matches)}")
    for description, model in matches:
        print(f"  {model}: {description}")
    print(f"digest-chunk matches           {len(digest_matches)}")
    for description, algorithm in digest_matches:
        print(f"  {algorithm}: {description}")


if __name__ == "__main__":
    main()
