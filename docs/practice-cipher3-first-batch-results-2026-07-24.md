# Practice cipher 3 — first mechanism-transfer batch

## Outcome

The first four lanes in the frozen mechanism horizon are negative. None keeps
heldout groups B/C inside the known 42-symbol plaintext range, predicts a
compact state set, or produces language beyond matched controls.

```text
A recovered C82 wheel      heldout language tail  .422886
C fixed coordinate drift   unique A/B/C           78/82/82
D physical deck family     outside-42 A/B/C        136/364/582
E cipher-5 recursion       outside-42 A/B/C        159/351/581
```

The puzzle remains unsolved. The result matters because it replaces one
unendorsed progression premise with four independent, calibrated mechanism
transfers from solved deck puzzles.

## Input partition and exceptional-symbol check

The author-supplied A/B/C partition is used as train/heldout structure:

```text
A lengths  57,65,57,66,66,67        378 events
B lengths  115,117,126,111,115,120  704 events
C lengths  188,191,192,185,215,194  1165 events
```

Raw value 42 renders as `J`. In solved sdlwdr ciphers 1 and 2 it is a very rare
control outside their common 82-position wheel. In cipher 3 it occurs
`4/6/12` times in A/B/C, 22 total. Its frequency and varied positions are
compatible with an ordinary member of the 83-symbol ciphertext alphabet. The
full exceptional-control test below does not promote it.

## A. Recovered 82-wheel transfer

### Method

The exact 82-card order independently recovered from ciphers 1 and 2 is reused
without refitting. Every non-`J` symbol is mapped to its wheel coordinate. The
complete bounded control family has:

- two initial traversal directions;
- two initial parity sheets;
- output or no output at `J`;
- optional parity flip, traversal reversal, accumulator reset, and anchor
  reset at `J`;
- both plaintext-wheel orientations;
- the English and Finnish 42-symbol trigram models.

This is `32×2×2×2×2 = 512` global interpretations. A 42-way plaintext rotation
is selected separately for each reset message, as in the solved Wadsworth
puzzles. The global interpretation is selected on A. B/C receive only their
allowed rotations.

Every null globally permutes all 82 non-`J` ciphertext labels while preserving
every `J` position, length, frequency, reset, and no-double fact. The complete
family and all rotations are reselected.

### Result

The selected rule uses the English model, reversed plaintext and ciphertext
orientations, initial parity zero, emits nothing at `J`, and resets only the
accumulator there.

```text
A score per trigram          -15.610363
B/C score per trigram        -16.052209
null range                   -16.174676 .. -15.962022
null mean                    -16.060633
controls >= observed         84 / 200
corrected upper tail         85 / 201 = .422886
```

The output is alphanumeric/punctuation gibberish. Representative starts are:

```text
A0  R 2Z8L9AIF 9-8W60MH.-7Z E.SG8!8NFABFE...
B0  IU59W5G7ULT!OFKFVF’G2TL6.ITEJMSELOKTND...
C0  FYC!GGDQD9TVKM05IL4E9HUL8TYL5!KYWPKC?...
```

The implementation's positive control exactly reproduces the solved
cipher-1 section containing `J`, including its emit-and-parity-flip semantics.
**Decision:** close direct ciphers-1/2 wheel reuse.

## C. Fixed position drift

For the standard `C83` coordinate and the recovered non-`J` `C82` coordinate,
both orientations and every fixed reset-relative drift `k*i` are exhausted.
The coordinate system, direction, and `k` are selected only by A's decoded
support.

```text
selected       recovered C82, direction -1, k=9
A              78 states / 374 ordinary events
B              82 states / 698 ordinary events
C              82 states / 1153 ordinary events
```

A planted progression collapses to one state in the unit test. The real
training result is already far above 42 and becomes the complete 82-state
wheel in both heldout groups. **Decision:** close fixed linear drift. This does
not alter the older exact result for an arbitrary single-`C83` progression.

## D. Named physical deck updates

The scan uses 8,598 distinct identity, interleave, Monge, Josephus, and
near-size affine bases. Each is paired with seven selected-rank updates:

```text
swap front, move front/back, cut to/after,
reverse prefix/suffix
```

Both full and first-symbol-as-primer modes are selected on A, for 120,372
distinct base/action/mode candidates. Every message resets its deck. B/C are
decoded once under the A winner.

```text
base          affine-82-fixed0-13-16
action        move-to-front
mode          body
A             136 outside 0..41; 75 distinct; maximum 82
B             364 outside 0..41; 82 distinct; maximum 82
C             582 outside 0..41; 82 distinct; maximum 82
```

The necessary plaintext-range gate fails by hundreds of events. **Decision:**
close this complete named physical family.

## E. Cipher-5 recursive update transfer

The exact recursive increasing-chunk reversal solved in cipher 5 supplies all
83 plaintext-selected update permutations. Six natural initial decks are
tested: raw forward/reverse and the recovered 82-wheel forward/reverse with
`J` at either end. Full/body and emit-before/update-before timing give 24
models.

All twelve update-before-output models are non-unique and therefore invalid.
All twelve emit-then-update models replay their ciphertext exactly, but none
approaches the plaintext range. The A-selected model is:

```text
initial deck   recovered wheel, J first, forward
mode/timing    body, emit then update
A              159 outside 0..41; 82 distinct
B              351 outside 0..41; 82 distinct
C              581 outside 0..41; 83 distinct
```

**Decision:** close direct reuse of cipher 5's recursive operation family.

## What remains

The frozen standard-`C83` quotient/action lane B and label-invariant isomorph
lane F remain active. They do not depend on any first-batch survivor. Language
search remains gated behind a finite mechanism.

## Transfer to the Eyes

- A key reused by the same author can be tested exactly, but thematic
  authorship is not evidence of reuse.
- A control symbol's role should replicate in its frequency and heldout
  consequences. Merely occupying the same raw label as a solved control fails.
- Training on short streams and reserving longer streams exposed every
  overfit: the physical and recursive winners expand back to almost all 83
  ranks.
- Exact ciphertext replay is necessary but weak for a dynamic substitution:
  every invertible wrong update can replay after decoding its own ranks. The
  plaintext range and heldout behavior carry the evidence.

## Reproduction

```bash
PYTHONPATH=src python3 scripts/run_practice_cipher3_first_batch.py
PYTHONPATH=src python3 scripts/run_practice_cipher3_wheel_transfer.py \
  --english-corpus /path/to/sherlock.txt /path/to/crawford-kalevala.txt \
  --finnish-corpus /path/to/seven-brothers.txt /path/to/kalevala-fi.txt \
  --controls 200 --workers 1
PYTHONPATH=src python3 -m unittest tests.test_practice_cipher3_wide -v
```
