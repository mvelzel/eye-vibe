# Practice cipher 3 — signed 42-state path results

**Date:** 27 July 2026
**Outcome:** exact finite negative; no plaintext recovered

## Tested family

The 83 raw values were interpreted as every signed displacement on a
42-position plaintext line:

```text
-41,-40,...,0,...,+40,+41
```

The complete authored-coordinate catalog was:

```text
d(v) = ((sign*v + offset) mod 83) - 41
sign in {+1,-1}, offset in 0..82
166 maps
```

Two conventions were exhausted. `full` uses the first raw value as the
initial absolute plaintext position and every later value as a displacement.
`primer` ignores the first raw value and admits any per-message initial
position, but retains one global displacement map.

## Control

A planted fixture preserved all 18 real lengths, selected
`orientation=-1, offset=17`, and exercised every displacement. The complete
catalog recovered:

```text
mode     result   surviving maps
full     sat           1
primer   sat           2
```

The two primer survivors are reflected descriptions of the same bounded
walks. Every recovered state replayed inside `0..41`.

An earlier arbitrary-permutation version of this idea is not part of the
negative result. Both Z3 and CP-SAT timed out on their planted controls before
the real corpus was opened, so that broader model remains unresolved.

## Real corpus

```text
mode     surviving maps
full          0
primer        0
```

This is exact over the declared 166-map catalog. In primer mode a map is
admissible exactly when every message body's cumulative-sum range is at most
41, so no choice of starting state was missed.

## Decision

Close the authored-order signed-path reading of `83=2*42-1`. Cipher 3 is not a
bounded 42-state walk whose raw numeric labels are the signed steps under one
cyclic cut or reversal.

Do not generalize this to an arbitrary hidden permutation, a modular walk, or
a non-bijective step table. No solution text was recovered.

## Transferable method

When ciphertext size is `2n-1`, test the complete signed displacement set on
an `n`-state *line*, not only a two-sheet quotient or cyclic magnitude. A
primer convention can be decided without searching starts: the cumulative
body must have range at most `n-1`.

## Reproduction

```text
PYTHONPATH=src python3 -m unittest \
  tests.test_practice_cipher3_signed_path

PYTHONPATH=src python3 \
  scripts/run_practice_cipher3_signed_path.py --phase both
```
