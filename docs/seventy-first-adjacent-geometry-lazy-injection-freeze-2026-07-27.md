# Seventy-first pass — lazy injection geometry freeze

## Motivation

The three hard two-context instances are quickly SAT when coordinate
injectivity is removed. Their first models collapse many labels. This
diagnostic was inspected before this freeze, so it motivates the method rather
than constituting prospective evidence.

## Exact algorithm

For each frozen pair:

1. build the existing integer chord-class solver with no `Distinct`;
2. solve the modular chord equations exactly;
3. group labels occupying the same coordinate;
4. if every coordinate is unique, replay and return `SAT`;
5. otherwise add `z[a] != z[b]` for every colliding pair in that model;
6. repeat until `SAT`, `UNSAT`, or the total timeout.

This is lazy constraint generation for the same complete injection condition.
There are finitely many label pairs, so an unbounded run is complete. No
coordinate, collision, or distance is selected from the desired result.

## Frozen targets and budget

Use canonical order and a total 120-second budget per pair:

```text
first-gap30 + first-cross
last-west4 + last-east5
last-east5 + last-east3
```

Add all collisions from each model, not one chosen collision. Use the existing
translation/scaling anchor and chord-class factorization unchanged.

## Controls

- recover the jointly SAT `F7` pair with unique coordinates;
- accept each half of a split `F5` three-leaf equal-distance star;
- verify that the star union is SAT without injection but UNSAT with it;
- replay every returned SAT coordinate map with the original checker.

## Interpretation and stop rule

- `SAT` is a complete injective pair witness.
- `UNSAT` exactly rejects that pair and therefore the global adjacent-cycle
  hypothesis.
- Timeout remains `UNKNOWN`, regardless of the number of cuts or rounds.
- If all three remain unknown, stop generic encodings and move to a
  cycle-space separator method.
