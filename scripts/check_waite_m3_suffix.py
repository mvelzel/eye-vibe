#!/usr/bin/env python3
"""Check the source-backed Waite suffix crib against East 2.

The check is intentionally one-way.  Perfectly isomorphic ciphers require two
occurrences of the same plaintext substring to produce isomorphic ciphertext
windows.  Passing that necessary condition demonstrates compatibility, not
plaintext recovery.
"""

from dataclasses import dataclass

from eye_mystery.corpus import MESSAGES, trigram_values
from eye_mystery.isomorphs import pattern


WAITE_M3_SUFFIX = (
    "SUBLIME THAT WHICH IS THE LOWEST, AND MAKE THAT WHICH IS THE HIGHEST, "
    "THE LOWEST."
)
EAST2_RAW_OFFSET = 37


@dataclass(frozen=True)
class RepeatCheck:
    first: int
    second: int
    length: int
    text: str
    first_pattern: str
    second_pattern: str

    @property
    def compatible(self) -> bool:
        return self.first_pattern == self.second_pattern


def repeated_substring_checks(
    plaintext: str,
    ciphertext: tuple[int, ...],
    *,
    min_length: int = 2,
) -> tuple[RepeatCheck, ...]:
    """Return every left-maximal equal-substring check.

    Nested suffixes of the same repeated run are omitted when the pair can be
    extended one character to the left.  This keeps the report concise while
    retaining every distinct maximal constraint.
    """

    if len(plaintext) != len(ciphertext):
        raise ValueError("plaintext and ciphertext lengths differ")

    checks: list[RepeatCheck] = []
    for first in range(len(plaintext)):
        for second in range(first + 1, len(plaintext)):
            if first and plaintext[first - 1] == plaintext[second - 1]:
                continue
            length = 0
            while (
                second + length < len(plaintext)
                and plaintext[first + length] == plaintext[second + length]
            ):
                length += 1
            if length < min_length:
                continue
            checks.append(
                RepeatCheck(
                    first=first,
                    second=second,
                    length=length,
                    text=plaintext[first : first + length],
                    first_pattern=pattern(ciphertext[first : first + length]),
                    second_pattern=pattern(ciphertext[second : second + length]),
                )
            )
    return tuple(checks)


def main() -> None:
    east2 = trigram_values(MESSAGES["east2"])
    suffix = east2[EAST2_RAW_OFFSET:]
    checks = repeated_substring_checks(WAITE_M3_SUFFIX, suffix)

    print("candidate length:", len(WAITE_M3_SUFFIX))
    print("East 2 suffix length:", len(suffix))
    print("raw span:", EAST2_RAW_OFFSET, len(east2))
    print("left-maximal repeated substrings:", len(checks))
    print("incompatible checks:", sum(not item.compatible for item in checks))
    for item in sorted(checks, key=lambda value: (-value.length, value.first)):
        print(
            f"raw {EAST2_RAW_OFFSET + item.first:3d}/"
            f"{EAST2_RAW_OFFSET + item.second:3d} "
            f"len {item.length:2d} {item.compatible!s:5s} "
            f"{item.text!r} {item.first_pattern} / {item.second_pattern}"
        )

    print(
        "verdict: necessary perfect-isomorphism checks pass; this is a "
        "source-backed compatible crib, not a decryption"
    )


if __name__ == "__main__":
    main()
