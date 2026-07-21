#!/usr/bin/env python3
"""Search structured plaintext mappings in affine F_83 group autokey."""

from __future__ import annotations

from dataclasses import dataclass

from eye_mystery.affine_gak import decode_affine_gak
from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.metrics import index_of_coincidence


@dataclass(frozen=True)
class Result:
    family: str
    mode: str
    parameters: tuple[int, ...]
    unique: int
    ioc: float


def evaluate(family, mode, parameters, function, messages):
    streams = tuple(decode_affine_gak(message, function, mode) for message in messages)
    if any(stream is None for stream in streams):
        return None
    combined = tuple(value for stream in streams for value in stream)  # type: ignore[union-attr]
    unique = len(set(combined))
    return Result(
        family=family,
        mode=mode,
        parameters=parameters,
        unique=unique,
        ioc=index_of_coincidence(combined, unique),
    )


def main() -> None:
    messages = tuple(trigram_values(MESSAGES[name]) for name in MESSAGE_ORDER)
    modes = ("full", "primer", "skip", "indicator-hidden", "indicator-both")
    results = []
    for mode in modes:
        for linear in range(83):
            for offset in range(83):
                result = evaluate(
                    "u(t)=a*t+b",
                    mode,
                    (linear, offset),
                    lambda value, a=linear, b=offset: a * value + b,
                    messages,
                )
                if result is not None:
                    results.append(result)
        for generator in range(1, 83):
            result = evaluate(
                "u(t)=g^t",
                mode,
                (generator,),
                lambda value, g=generator: pow(g, value, 83),
                messages,
            )
            if result is not None:
                results.append(result)
        for exponent in range(1, 82):
            result = evaluate(
                "u(t)=t^k (0->1)",
                mode,
                (exponent,),
                lambda value, k=exponent: 1 if value == 0 else pow(value, k, 83),
                messages,
            )
            if result is not None:
                results.append(result)
        for shift in range(83):
            result = evaluate(
                "u(t)=1/(t+s)",
                mode,
                (shift,),
                lambda value, s=shift: 0
                if (value + s) % 83 == 0
                else pow((value + s) % 83, -1, 83),
                messages,
            )
            if result is not None:
                results.append(result)

    print("Affine group-autokey candidates (few symbols, then high IoC)")
    print("family              mode              parameters unique    IoC")
    for result in sorted(results, key=lambda item: (item.unique, -item.ioc))[:50]:
        print(
            f"{result.family:<19} {result.mode:<17} {str(result.parameters):<12} "
            f"{result.unique:>6} {result.ioc:>6.3f}"
        )


if __name__ == "__main__":
    main()
