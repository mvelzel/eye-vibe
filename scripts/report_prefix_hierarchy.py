#!/usr/bin/env python3
"""Report the complete nested common-prefix tree after message markers."""

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.prefix_hierarchy import (
    breadth_first_prefix_clusters,
    prefix_clusters,
)


def main() -> None:
    streams = {
        name: trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER
    }
    for cluster in prefix_clusters(streams, start=1):
        print(f"length={cluster.length:>2}  {' '.join(cluster.members)}")
    east5_first = MESSAGE_ORDER[-1:] + MESSAGE_ORDER[:-1]
    ordered_streams = {name: streams[name] for name in east5_first}
    breadth_first = breadth_first_prefix_clusters(ordered_streams, start=1)
    depths = tuple(cluster.length for cluster in breadth_first)
    print()
    print("East-5-first breadth-first depths:", depths)
    print("A1Z26:", "".join(chr(64 + depth) for depth in depths))


if __name__ == "__main__":
    main()
