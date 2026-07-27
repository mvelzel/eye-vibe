# Seventy-sixth pass — additive edit-diamond results

## Result

Cipher 4 remains unsolved.  Its one-character edit does select a simple
operation exactly:

```text
rank paths       18,22  versus  12
centered steps  -10,-6  versus -16
neutral          28
```

Thus subtracting the independently fixed midpoint of the `0..56` rank band
makes the two-step insertion path and one-step direct path have identical
displacement.  The next 105 recovered actions are copied exactly, so this is
an executable local synchronization diamond rather than a language score.

The observation does **not** solve the codec.  Applying the same additive
model to every rejoin between consecutive maximal copied blocks of length at
least ten requires neutrals:

```text
28,55,48,28,32,24  (mod 57)
```

No global neutral exists.  Direct centered accumulation uses all 57 states and
has normalized IoC `0.991509489742`; the previous signed-band language audit
also found no readable rendering on any ring `19..83`.  The defensible result
is therefore local: one branch behaves like composition of centered
increments, while a single global additive plaintext state is false.

The exact frequency-matched probability that a frozen ordered two-rank draw
from portion 1 and one-rank draw from portion 2 satisfy the midpoint equation
is `0.017482426180`.  This is calibration, not a discovery p-value: the edit
was inspected before the test was frozen, and the duplicated portion-3
instance is the same event.

## Eye transfer

The frozen literal search covers all 36 Eye-message pairs, two copied
four-symbol boundary contexts, gap lengths `1..8`, and both one-symbol length
differences.  It finds:

```text
literal short edit diamonds  0
midpoint-41 diamonds         0
```

So the Cipher 4 arithmetic does not transfer literally to the Eyes.  The
Eyes' important cross-panel contexts are equality-isomorphic under unknown
label maps; assigning first-occurrence numbers to those labels and adding
them would be analyst-created arithmetic, so that broader transfer is not
admissible.

## What was learned

- An insertion/rejoin can select an update convention before plaintext is
  known: solve the equality of the two path products.
- A duplicated comparison through the same branch is one observation, not
  two independent confirmations.
- A locally exact synchronization law must be tested at every other rejoin
  before being promoted to a global cipher.
- For the Eyes, the analogous useful object is the already promoted
  label-invariant phase/rejoin topology.  Cipher 4 supplies no numeric Eye
  operation or key.

Reproduction:

```text
PYTHONPATH=src .venv/bin/python scripts/audit_edit_diamonds.py
PYTHONPATH=src .venv/bin/python -m unittest tests.test_edit_diamond
```
