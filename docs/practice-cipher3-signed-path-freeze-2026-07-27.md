# Practice cipher 3 — signed 42-state path freeze

**Date:** 27 July 2026
**Status:** frozen before the real corpus is checked

## Motivation

The known plaintext alphabet has 42 positions, while Cipher 3 uses exactly 83
raw symbols:

```text
83 = 2*42 - 1 = |{-41,-40,...,0,...,+40,+41}|
```

This suggests a different reading from the failed static two-sheet quotient.
Each raw symbol may name one signed displacement on a *line* of 42 plaintext
states. The frozen finite family uses the authored numeric order under every
cyclic cut and both orientations:

```text
d(v) = ((sign*v + offset) mod 83) - 41

sign       +1 or -1
offset     0..82
catalog    166 maps
```

decodes a message by cumulative addition, with every intermediate state
required to remain in `0..41`.

This exact architecture has not been tested by the cyclic-distance,
two-sheet, or pair-quotient passes. It uses the cardinality identity as a
complete executable interface rather than as a static homophone count.

An arbitrary hidden permutation was the first proposed scope. Both Z3 and
CP-SAT timed out on its planted fixture at the frozen 20-second limit. No real
result was inspected. That broader family is therefore unresolved and is not
used as evidence here; the finite authored-coordinate catalog was frozen only
after that control failure.

## Frozen modes

Two conventions are admitted:

1. **full** — the first raw symbol maps to the initial absolute plaintext
   position; every later symbol maps to a signed displacement through the same
   table;
2. **primer** — the first raw symbol is ignored, each message receives an
   unconstrained initial state in `0..41`, and all remaining symbols map to
   signed displacements.

The second mode is the broader interpretation suggested by the unequal first
symbols before Cipher 3's copied A bodies. No per-message displacement key,
wraparound, clamping, missing displacement, or non-bijective map is allowed.

## Exact solver and positive control

Enumerate all 166 maps. In full mode, replay cumulative states and reject on
the first state outside `0..41`. In primer mode, let `s[i]` be the cumulative
body sums including the initial zero. A message has some legal initial state
exactly when:

```text
max(s) - min(s) <= 41
```

One witness is `start=-min(s)`. This makes the finite result exact; no
optimizer or timeout is involved.

A deterministic planted fixture preserves the 18 real message lengths,
selects a hidden member of the 166-map catalog, and includes every
displacement. One long message executes

```text
0,+1,-1,+2,-2,...,+41,-41
```

or the full-mode equivalent with the initial zero carried by the first event.
All remaining positions are filled by legal random bounded moves. Both frozen
modes must return `sat` and replay every planted state inside `0..41`.

## Decision rules

- `unsat` is an exact rejection of the corresponding 166-map signed-path
  mode.
- `sat` is only compatibility. Inspect the resulting plaintext-state streams,
  but do not call them a solution without stable language and exact replay
  under one global displacement table.
- Do not widen a failure to the unresolved arbitrary permutation, modular
  arithmetic, arbitrary tree state, or a non-bijective displacement table.

The real corpus must not be checked until the implementation tests and both
planted controls pass.
