# Sixtieth pass — Cipher 3 affine two-sheet quotient

## Result

The matched plant passes decisively, but the real Cipher 3 corpus fails on
both complete streams and marker-stripped bodies. This closes the complete
83-member family

```text
x ~ a-x (mod 83),  a in 0..82
```

as a static `83 -> 42` quotient followed by one global substitution. No
plaintext was recovered.

## Calibration

The control used the real 18 stream lengths, one planted reflection `a=37`, a
random permutation of the known 42-character plaintext alphabet, and random
choice between the two representatives of each non-singleton orbit. The
search saw only group A when selecting the reflection and substitution.

At the frozen strong budget:

```text
mode   planted  selected  screen rank  A accuracy   B/C accuracy
full       37        37          1     100.000000%   99.946495%
body       37        37          1     100.000000%   99.946150%
```

The frozen A key reads the B/C plant at about `-7.03` log units per trigram.
The small held-out error is confined to plaintext-key information absent from
the shorter A training split; it does not affect recovery of the reflection
or readable held-out text.

## Real corpus

The same exhaustive reflection screen and top-six refinement gives:

```text
mode   selected  A score/trigram  B/C score/trigram
full       82       -13.296105        -15.695016
body       82       -13.287232        -15.697603
```

All displayed previews are uniform gibberish. The held-out deficit relative
to the matched plant is about `8.67` log units per trigram. Smaller pilot runs
selected reflections `46` for full streams and `60` for bodies, while keeping
the same poor real/plant separation. The real key is therefore not only
unreadable but unstable under additional search.

## Decision

Closed:

- all 83 standard-coordinate affine involutions of the visible labels;
- full-stream and first-symbol-stripped reset conventions;
- one static orbit quotient followed by one global injective 42-symbol
  substitution.

Still open:

- an arbitrary non-affine pairing of the 83 labels;
- an affine quotient after an unknown hidden coordinate permutation;
- a stateful sheet schedule;
- direction-free *transition* magnitudes, except for the previously closed
  fixed-wheel families.

The exact count `83=2*42-1` remains architecturally possible, but it does not
license fitting a hidden pairing after this finite family fails.

Reproduction:

```text
PYTHONPATH=src python3 -m unittest tests.test_practice_cipher3_two_sheet
PYTHONPATH=src python3 scripts/run_practice_cipher3_two_sheet.py \
  --mode both --screen-iterations 10000 \
  --refine-iterations 80000 --refine-restarts 4 --shortlist 6
```
