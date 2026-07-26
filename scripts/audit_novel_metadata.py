#!/usr/bin/env python3
"""Print the compact metadata/stagger checks from the wide step-back."""

from eye_mystery.novel_metadata import (
    descriptor_permutation_matches,
    q_headers_are_noncenter_derangements,
    range_descriptor,
    row_staggers,
)


def main() -> None:
    descriptor = range_descriptor()
    print("range descriptor", descriptor)
    print("reconstructed size", descriptor.size)
    print("maximum glyph", descriptor.maximum_digits)
    print("matching 358 orders", descriptor_permutation_matches())
    print("Q noncenter derangements", q_headers_are_noncenter_derangements())
    for row in row_staggers():
        print(row)


if __name__ == "__main__":
    main()
