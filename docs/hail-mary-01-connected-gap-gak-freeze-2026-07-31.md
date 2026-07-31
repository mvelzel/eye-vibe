# Hail Mary 01: connected-gap ordinary GAK — freeze

## Target

Exhaust the literal one-update-per-character ordinary-GAK interpretation of
the three repeated `THAT WHICH` windows. This is the unfinished exact
`K=7..42` test frozen on 2026-07-27, not a new crib search.

The three canonical trigram segments remain:

```text
East 1   40 -> 68   10 fixed + 18 unknown + 10 fixed
West 1   40 -> 70   10 fixed + 20 unknown + 10 fixed
East 2   45 -> 80   10 fixed + 25 unknown + 10 fixed
```

The two ends are `THAT WHICH`; its seven literal characters have shared,
pinned action labels. Each unknown position chooses any of `K` shared
actions. The segments have independent arbitrary start decks. There is no
reset, context state, selector layer, token merging, or postprocessor.

## Acceptance and controls

A positive result requires complete shared position permutations, complete
start decks, a plaintext action at every gap position, and independent exact
forward replay of all three segments.

Before interpreting the Eye query, the solver must:

1. recover and replay a same-length, same-placement planted three-trace
   instance with seven pinned phrase actions and two hidden gap actions;
2. reject the impossible repeated-action orbit `A B B`.

SAT is only compatibility. UNSAT at deck size 83 is a rejection for that
`K`; UNSAT at a smaller active-state reduction is not. `unknown` is not
negative evidence.

## Exhaustion ladder

1. Replace the quadratic prefix/deck encodings with direct card-position
   evolution through complete inverse-permutation tables.
2. Run the same-shaped plant at 83 positions and the impossible control.
3. Test the real `K=7` problem first at 83 positions; use smaller position
   counts only as search aids for constructive witnesses.
4. If unresolved, try solver representations/tactics, safe position and
   extra-action symmetry breaking, source-selected fixed gap schedules, and
   free-group-derived constraints.
5. Continue through `K=42` only where the controls pass and the nesting is
   meaningful. Stop on the first exactly replayed witness.

The branch is abandoned only after these materially distinct formulations
either reject it or fail under passed same-shaped controls. Merely spending a
larger timeout on the old encoding does not count as exhaustion.
