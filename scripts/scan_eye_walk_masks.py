#!/usr/bin/env python3
"""Check cheap constant-step walk carriers before hidden-state models."""

from eye_mystery.corpus import MESSAGES, MESSAGE_ORDER, trigram_values
from eye_mystery.walk_mask import walk_violations


def best_constant_step(values: tuple[int, ...], modulus: int):
    projected = tuple(value % modulus for value in values)
    candidates = []
    for step in range(1, modulus):
        if step == -step % modulus:
            continue
        violations = walk_violations(projected, modulus=modulus, step=step)
        candidates.append((len(violations), step, violations))
    return min(candidates)


def main() -> None:
    for source in ("canonical trigrams", "raw directions"):
        print(source)
        values_by_message = {
            name: (
                trigram_values(MESSAGES[name])
                if source == "canonical trigrams"
                else MESSAGES[name]
            )
            for name in MESSAGE_ORDER
        }
        modulus_range = range(3, 84) if source == "canonical trigrams" else range(3, 6)
        ranked = []
        for modulus in modulus_range:
            violation_count = 0
            transition_count = 0
            steps = []
            for name in MESSAGE_ORDER:
                values = values_by_message[name]
                count, step, _ = best_constant_step(values, modulus)
                violation_count += count
                transition_count += len(values) - 1
                steps.append(step)
            ranked.append(
                (
                    violation_count / transition_count,
                    violation_count,
                    transition_count,
                    modulus,
                    tuple(steps),
                )
            )
        for fraction, violations, transitions, modulus, steps in sorted(ranked)[:8]:
            print(
                f"  modulus={modulus:2d} violations={violations}/{transitions}",
                f"({fraction:.3%}) per-message-best-steps={steps}",
            )


if __name__ == "__main__":
    main()
