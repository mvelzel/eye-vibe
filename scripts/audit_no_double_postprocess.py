#!/usr/bin/env python3
"""Search the Eyes for exact arithmetic no-double replacement signatures."""

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values
from eye_mystery.no_double_postprocess import no_double_postprocess_witnesses


def main() -> None:
    streams = {
        name: trigram_values(MESSAGES[name])
        for name in MESSAGE_ORDER
    }
    witnesses = no_double_postprocess_witnesses(streams)
    print("witnesses", len(witnesses))
    for witness in witnesses:
        print(witness)


if __name__ == "__main__":
    main()
