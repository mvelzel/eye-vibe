#!/usr/bin/env python3
"""Audit numeric SetRandomSeed salts against marker-plane calling codes."""

from __future__ import annotations

import argparse
from pathlib import Path

from eye_mystery.calling_codes import geographic_regions
from eye_mystery.rng_locale_salts import scan_wak_rng_locale_salts
from eye_mystery.wak import WakArchive


def _format_recipe(recipe: tuple[tuple[object, ...], tuple[object, ...]]) -> str:
    return " | ".join(
        ",".join(str(value) for value in argument) or "-"
        for argument in recipe
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()

    calls = scan_wak_rng_locale_salts(WakArchive.open(args.archive))
    salted = tuple(call for call in calls if any(call.salts))
    recipes = {}
    for call in salted:
        recipes.setdefault(call.recipe, []).append(call)

    marker = {
        recipe: occurrences
        for recipe, occurrences in recipes.items()
        if occurrences[0].marker_codes
    }
    geographic = {
        recipe: occurrences
        for recipe, occurrences in recipes.items()
        if occurrences[0].is_geographic_pair
    }

    print(f"SetRandomSeed calls: {len(calls)}")
    print(f"salted calls: {len(salted)}")
    print(f"distinct salted recipes: {len(recipes)}")
    print(f"marker-code recipes: {len(marker)}")
    print(f"geographic-pair recipes: {len(geographic)}")

    paired = {
        recipe: occurrences
        for recipe, occurrences in recipes.items()
        if occurrences[0].eye_ascii_pair() is not None
    }
    primary_instructions = {
        recipe: occurrences
        for recipe, occurrences in paired.items()
        if occurrences[0].is_compact_arithmetic_instruction()
    }
    broadened_instructions = {
        recipe: occurrences
        for recipe, occurrences in paired.items()
        if any(
            occurrences[0].is_compact_arithmetic_instruction(
                absolute=absolute, reverse=reverse
            )
            for absolute in (False, True)
            for reverse in (False, True)
        )
    }
    exact_plus_three = {
        recipe: occurrences
        for recipe, occurrences in paired.items()
        if occurrences[0].eye_ascii_pair() == "+3"
    }
    broadened_plus_three = {
        recipe: occurrences
        for recipe, occurrences in paired.items()
        if any(
            occurrences[0].eye_ascii_pair(
                absolute=absolute, reverse=reverse
            )
            == "+3"
            for absolute in (False, True)
            for reverse in (False, True)
        )
    }
    print(f"one-salt-per-argument recipes: {len(paired)}")
    print(f"primary compact-instruction recipes: {len(primary_instructions)}")
    print(f"broadened compact-instruction recipes: {len(broadened_instructions)}")
    print(f"primary exact +3 recipes: {len(exact_plus_three)}")
    print(f"broadened exact +3 recipes: {len(broadened_plus_three)}")

    for heading, selected in (
        ("marker-code recipes", marker),
        ("geographic-pair recipes", geographic),
        ("primary compact-instruction recipes", primary_instructions),
        ("broadened compact-instruction recipes", broadened_instructions),
    ):
        print(f"\n{heading}:")
        for recipe, occurrences in sorted(
            selected.items(), key=lambda item: _format_recipe(item[0])
        ):
            first = occurrences[0]
            regions = [
                tuple(
                    geographic_regions(value)
                    for value in argument
                )
                for argument in first.integer_parts
            ]
            print(
                f"  {_format_recipe(recipe)} "
                f"parts={first.integer_parts} regions={regions} "
                f"occurrences={len(occurrences)}"
            )
            for call in occurrences:
                print(
                    f"    {call.path}:{call.line} "
                    f"SetRandomSeed({call.arguments[0]}, {call.arguments[1]})"
                )
            print(
                "    eye-ascii "
                + " ".join(
                    f"abs={absolute} reverse={reverse}:"
                    f"{first.eye_ascii_pair(absolute=absolute, reverse=reverse)!r}"
                    for absolute in (False, True)
                    for reverse in (False, True)
                )
            )


if __name__ == "__main__":
    main()
