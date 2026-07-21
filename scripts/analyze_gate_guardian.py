#!/usr/bin/env python3
"""Rebuild the low-level Gate Guardian facts relevant to the Eyes.

The script starts from the installed PNG/XML/Lua data and intentionally stops
before assigning Type4/Type6 semantics.  It checks the mod-101 Eye checksum
grid, an independent null, objective palette/geometry facts, the natural
four-piece assembly, simple mirror residuals, literal Q-C successor edges, and
the executable spawn topology.  These are the claims that can be audited
without the theory author's private masks or interpreter.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import re
from typing import Iterable, Sequence
import xml.etree.ElementTree as ET

from PIL import Image, ImageOps

from eye_mystery.corpus import MESSAGE_ORDER, MESSAGES, trigram_values


MODULUS = 101
MARK_COLOR = (60, 57, 65, 255)
SPRITES = {
    "Veska": "gate_monster_a.png",
    "Molari": "gate_monster_b.png",
    "Mokke": "gate_monster_c.png",
    "Seula": "gate_monster_d.png",
}
AXES = {
    "main-diagonal": ((1, 3), (2, 6), (5, 7)),
    "anti-diagonal": ((0, 8), (1, 5), (3, 7)),
    "horizontal": ((0, 6), (1, 7), (2, 8)),
    "vertical": ((0, 2), (3, 5), (6, 8)),
}
QC_EDGES = {
    "east4": (68, 69),
    "west4": (23, 24),
    "east5": (30, 31),
}


def checksum_grid() -> tuple[int, ...]:
    return tuple(
        sum(trigram_values(MESSAGES[name])) % MODULUS for name in MESSAGE_ORDER
    )


def circular_magnitude(left: int, right: int) -> int:
    difference = (left - right) % MODULUS
    return min(difference, MODULUS - difference)


def reflection_total(
    values: Sequence[int], pairs: Iterable[tuple[int, int]]
) -> tuple[tuple[int, ...], int]:
    magnitudes = tuple(circular_magnitude(values[left], values[right]) for left, right in pairs)
    return magnitudes, sum(magnitudes)


def fixed_axis_probability(target: int) -> Fraction:
    """Exact baseline for three independent uniform mod-101 pair differences."""

    numerator = 0
    for first in range(MODULUS // 2 + 1):
        for second in range(MODULUS // 2 + 1):
            third = target - first - second
            if not 0 <= third <= MODULUS // 2:
                continue
            weights = tuple(1 if value == 0 else 2 for value in (first, second, third))
            numerator += weights[0] * weights[1] * weights[2]
    return Fraction(numerator, MODULUS**3)


def palette(image: Image.Image) -> Counter[tuple[int, int, int, int]]:
    return Counter(image.convert("RGBA").get_flattened_data())


def mask(image: Image.Image, predicate) -> set[tuple[int, int]]:
    rgba = image.convert("RGBA")
    return {
        (x, y)
        for y in range(rgba.height)
        for x in range(rgba.width)
        if predicate(rgba.getpixel((x, y)))
    }


def connected_components(
    points: set[tuple[int, int]], *, diagonals: bool = True
) -> tuple[frozenset[tuple[int, int]], ...]:
    directions = tuple(
        (dx, dy)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        if (dx or dy) and (diagonals or not (dx and dy))
    )
    unseen = set(points)
    components: list[frozenset[tuple[int, int]]] = []
    while unseen:
        start = unseen.pop()
        stack = [start]
        component = {start}
        while stack:
            x, y = stack.pop()
            for dx, dy in directions:
                neighbour = (x + dx, y + dy)
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    component.add(neighbour)
                    stack.append(neighbour)
        components.append(frozenset(component))
    return tuple(components)


def symmetric_difference_count(image: Image.Image, selected: set[tuple[int, ...]]) -> int:
    rgba = image.convert("RGBA")
    return sum(
        (rgba.getpixel((x, y)) in selected)
        != (rgba.getpixel((rgba.width - 1 - x, y)) in selected)
        for y in range(rgba.height)
        for x in range(rgba.width // 2)
    )


def natural_assembly(images: dict[str, Image.Image]) -> tuple[Image.Image, dict[str, tuple[int, int]]]:
    """Tile the four authored pieces using only edge alignment and dimensions."""

    width = images["Molari"].width + images["Veska"].width + images["Mokke"].width
    height = images["Seula"].height + images["Veska"].height
    positions = {
        "Molari": (0, height - images["Molari"].height),
        "Veska": (images["Molari"].width, height - images["Veska"].height),
        "Mokke": (
            images["Molari"].width + images["Veska"].width,
            height - images["Mokke"].height,
        ),
        "Seula": ((width - images["Seula"].width) // 2, 0),
    }
    canvas = Image.new("RGBA", (width, height))
    for name in ("Molari", "Veska", "Mokke", "Seula"):
        canvas.alpha_composite(images[name], positions[name])
    return canvas, positions


def spawn_records(data_root: Path) -> tuple[tuple[str, int, int, int], ...]:
    spawner = data_root / "entities/buildings/wizardcave_gate_monster_spawner.xml"
    root = ET.parse(spawner).getroot()
    records = []
    for entity in root.findall("./Entity"):
        transform = entity.find("./InheritTransformComponent/Transform")
        loader = entity.find("./LoadEntitiesComponent")
        if transform is None or loader is None:
            continue
        filename = Path(loader.attrib["entity_file"]).stem
        records.append(
            (
                filename,
                int(transform.attrib["position.x"]),
                int(transform.attrib["position.y"]),
                int(loader.attrib["timeout_frames"]),
            )
        )
    return tuple(records)


def numeric_literals(paths: Iterable[Path]) -> Counter[int]:
    result: Counter[int] = Counter()
    for path in paths:
        for token in re.findall(r"(?<![A-Za-z_])\d+(?:\.\d+)?", path.read_text()):
            value = float(token)
            if value.is_integer():
                result[int(value)] += 1
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--assets",
        type=Path,
        required=True,
        help="directory containing gate_monster_a.png through gate_monster_d.png",
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        help="unpacked Noita data root containing entities/ and scripts/",
    )
    parser.add_argument(
        "--assembly-output",
        type=Path,
        help="optional path for the naturally tiled four-piece PNG",
    )
    args = parser.parse_args()

    grid = checksum_grid()
    print("canonical grid")
    for start in range(0, 9, 3):
        print(" ", grid[start : start + 3])
    for name, pairs in AXES.items():
        magnitudes, total = reflection_total(grid, pairs)
        print(f"{name}: magnitudes={magnitudes} total={total}")
    probability = fixed_axis_probability(70)
    print(
        "uniform fixed-axis P(total=70):",
        f"{probability.numerator}/{probability.denominator}",
        f"= {float(probability):.9f}",
    )

    images = {
        name: Image.open(args.assets / filename).convert("RGBA")
        for name, filename in SPRITES.items()
    }
    print("\nsprite palettes")
    for name, image in images.items():
        counts = palette(image)
        digest = sha256((args.assets / SPRITES[name]).read_bytes()).hexdigest()
        print(
            f"{name}: size={image.size} colors={len(counts)} "
            f"opaque={sum(count for color, count in counts.items() if color[3])} "
            f"mark-color={counts[MARK_COLOR]} sha256={digest}"
        )
        for color, count in counts.most_common():
            print(f"  {color}: {count}")

    molari_alpha = mask(images["Molari"], lambda color: color[3] > 0)
    mirrored_mokke_alpha = mask(
        ImageOps.mirror(images["Mokke"]), lambda color: color[3] > 0
    )
    difference = molari_alpha ^ mirrored_mokke_alpha
    print("\npaired side geometry")
    print("Molari opaque pixels:", len(molari_alpha))
    print("mirrored Mokke opaque pixels:", len(mirrored_mokke_alpha))
    print("opaque-mask symmetric difference:", len(difference), sorted(difference))

    veska_marks = mask(images["Veska"], lambda color: color == MARK_COLOR)
    upper = {(x, y) for x, y in veska_marks if 9 <= x <= 40 and 12 <= y <= 22}
    middle = {(x, y) for x, y in veska_marks if 24 <= y <= 42}
    lower = {(x, y) for x, y in veska_marks if 13 <= x <= 49 and 46 <= y <= 53}
    remainder = veska_marks - upper - middle - lower
    print("\nVeska mark audit")
    print(
        "spatially separated counts remainder|middle|upper|lower:",
        len(remainder), len(middle), len(upper), len(lower),
    )
    print(
        "upper 8-neighbour component sizes:",
        sorted(map(len, connected_components(upper))),
    )
    print(
        "lower 8-neighbour component sizes:",
        sorted(map(len, connected_components(lower))),
    )
    print(
        "note: the natural bands give 11|44|9|8; obtaining 12|43|9|8 "
        "requires reclassifying one middle pixel by an additional rule"
    )

    seula = images["Seula"]
    opaque_colors = sorted(color for color in palette(seula) if color[3])
    print("\nSeula simple vertical-mirror residuals (one half)")
    for color in opaque_colors:
        print(color, symmetric_difference_count(seula, {color}))
    print(
        "RGBA mismatch pairs:",
        sum(
            seula.getpixel((x, y)) != seula.getpixel((seula.width - 1 - x, y))
            for y in range(seula.height)
            for x in range(seula.width // 2)
        ),
    )
    print("alpha mismatch pairs: 0")

    assembly, positions = natural_assembly(images)
    print("\nnatural static assembly")
    print("size:", assembly.size, "positions:", positions)
    if args.assembly_output:
        args.assembly_output.parent.mkdir(parents=True, exist_ok=True)
        assembly.save(args.assembly_output)
        print("saved:", args.assembly_output)

    print("\nliteral Q-C successor edges")
    all_successors = []
    for name, message in MESSAGES.items():
        values = trigram_values(message)
        for index, (left, right) in enumerate(zip(values, values[1:])):
            if right == left + 1 and left % 5 < 4:
                all_successors.append((name, index, left, right))
    print("all carry-free third-eye +1 edges:", all_successors)
    for name, edge in QC_EDGES.items():
        hits = [
            index
            for index, pair in enumerate(zip(trigram_values(MESSAGES[name]), trigram_values(MESSAGES[name])[1:]))
            if pair == edge
        ]
        print(name, edge, hits)

    if args.data_root:
        print("\nexecutable source topology")
        records = spawn_records(args.data_root)
        for record in records:
            print(record)
        source_paths = (
            args.data_root / "entities/buildings/wizardcave_gate_monster_spawner.xml",
            args.data_root / "entities/buildings/wizardcave_gate.xml",
            args.data_root / "scripts/buildings/wizardcave_gate.lua",
            args.data_root / "entities/animals/boss_gate/gate_monster_death.lua",
            args.data_root / "entities/animals/boss_gate/gate_monster_push.lua",
            *sorted((args.data_root / "entities/animals/boss_gate").glob("*.xml")),
        )
        literals = numeric_literals(source_paths)
        claimed = (17, 18, 39, 66, 68, 69, 70, 72, 73, 83, 101, 124)
        print("Eye-theory integers present in executable XML/Lua:")
        print({value: literals[value] for value in claimed if literals[value]})


if __name__ == "__main__":
    main()
