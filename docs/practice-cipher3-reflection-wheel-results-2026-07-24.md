# Practice cipher 3 — hidden reflection-wheel results

## Outcome

Two finite reflection-wheel families are negative under a positive control:

```text
displayed standard wheel     real -15.538194 / trigram, gibberish
166 old-wheel insertions     real -15.394573 / trigram, gibberish
matched planted controls           -7.178008 / trigram, 100% plaintext
```

A completely arbitrary hidden wheel is not rejected. Its joint optimizer
fails its own planted control, reaching only `9.017497%` plaintext accuracy
after 500,000 steps and no dihedrally equivalent wheel. Running it on the real
corpus would therefore produce an uninterpretable local optimum, so the
frozen stop rule prevents that run from being used as evidence.

Cipher 3 remains unsolved.

## 1. Exact rejection of one global direction

The real transition support contains:

```text
directed edges                  1845
reciprocal unordered pairs       253
maximum reciprocal degree         14  (raw state 82)
```

Suppose every transition were one of 42 consecutive forward steps on an
unknown 83-cycle. For both `a->b` and `b->a` to be allowed, their complementary
distances must both lie in that 42-step half. Under the natural nonzero
convention, only boundary distances 41 and 42 can do so. A state can therefore
have at most two reciprocal partners. State 82 has fourteen.

This is a label-independent contradiction for a single global direction. It
does not apply after identifying `+d` and `-d`, or when a larger state carries
a direction bit.

## 2. Why the reflection quotient was tested

For hidden coordinates `z` in `Z83`,

```text
min((z(b)-z(a)) mod 83, (z(a)-z(b)) mod 83)
```

has nonzero values `1..41`. Together with zero, it gives exactly 42 classes.
This makes `Z83/{±1}` a structurally exact bridge between the 83 ciphertext
labels and the author's known 42-character plaintext alphabet.

Each message's first raw value is treated as a primer. The remaining adjacent
transitions become magnitude classes. One injective global substitution maps
the 41 observed magnitudes into:

```text
ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .-’?!
```

Message boundaries reset language windows.

## 3. Displayed standard order

Holding raw `0..82` as the cyclic order and optimizing only the 41-class
substitution gives:

```text
matched planted control   -7.178008 / trigram, 100.000000%
real corpus              -15.538194 / trigram
```

The real output is uniform alphanumeric/punctuation gibberish. Representative
starts are:

```text
T187.DDSCTWHIT!SYDRE.?1QPW8-JC.-!-7RZD5.Z0KP?T’VX.NW8CNI
6QSQBK4E’NL4.QE9FJZ6.WARJW!RC4N0Z2.S9VQJCK Q-OX57OXRWIO...
```

The control establishes that the key solver can recover this exact model at
the stated length and budget. **Decision:** close the authored standard
reflection wheel.

## 4. Every old-wheel insertion

The exact 82-position wheel independently recovered from practice ciphers 1
and 2 omits exceptional raw `J=42`. The complete finite family inserts `J` at
every one of 83 positions, under both orientations: 166 named candidates.
Only the plaintext substitution is optimized per candidate.

The planted control uses `forward-17`. It is selected exactly, together with
its unavoidable dihedral equivalent:

```text
reverse-65    -7.178008   100.000000%
forward-17    -7.178008   100.000000%
forward-18    -7.785895    95.827725%
forward-16    -7.804872    95.379094%
```

The real leaders are tightly clustered far below the control:

```text
reverse-32   -15.394573
forward-43   -15.406071
forward-45   -15.407968
forward-67   -15.412124
forward-72   -15.412679
```

All render as gibberish. The winner begins:

```text
LIL? Z.QG0 FMPDTYAWSV0PLHYQNYWQA1-P0M74GJ6W-GW2ON PYPY1C
```

**Decision:** close every direct reflection-quotient reuse of the solved
cipher-1/2 wheel, including all possible exceptional-card insertions.

## 5. Arbitrary hidden wheel

The joint annealer has two exact move types:

- swap two raw labels' positions on the hidden 83-cycle;
- swap two magnitude-to-plaintext assignments.

It rescored only incident transitions and affected trigram windows. Three
diagnostics locate the failure:

```text
true wheel fixed, key unknown        10,000 steps -> 100% plaintext
true key fixed, wheel unknown       500,000 steps -> 9.47%, wrong wheel
both unknown                        500,000 steps -> 9.02%, wrong wheel
```

The language substitution is easy once the geometry is correct. Local wheel
swaps are the bottleneck. Circular spectral initialization also fails on the
matched planted corpus: no eigenvector pair recovers the wheel, and the best
candidate preserves only 10 of 83 true cyclic adjacencies.

This is an optimizer failure, not a cipher-family failure. The real arbitrary
wheel is not scored or rendered as a candidate. A future attempt needs a
global wheel-recovery method, a known plaintext, or an author constraint—not
more restarts of the same local move.

## Transfer to the Eyes

- The reciprocal-edge obstruction is a cheap exact necessity for any claimed
  one-direction half-cycle. It should precede language work.
- A `Z83/{±1}` alphabet fit is mathematically natural but not a key. Recovering
  an arbitrary hidden cyclic coordinate is the hard step.
- Positive controls must recover geometry, not merely improve a language
  score. Here the key solver succeeds and the wheel solver fails, which
  prevents a false real-corpus result.
- The Eyes' literal reflection quotient has already been tested in several
  authored coordinate orders. This practice result does not justify reopening
  arbitrary-wheel annealing without a new global initializer.

## Reproduction

The finite scans:

```bash
PYTHONPATH=src python3 scripts/run_practice_cipher3_reflection_wheel.py \
  --mode both --skip-joint --standard-scan --fixed-scan \
  --restarts 4 --fixed-iterations 5000
```

The failed arbitrary-wheel positive control:

```bash
PYTHONPATH=src python3 scripts/run_practice_cipher3_reflection_wheel.py \
  --mode control --restarts 1 --iterations 500000
```

Tests:

```bash
PYTHONPATH=src python3 -m unittest \
  tests.test_practice_cipher3_reflection -v
```
