# Sixtieth horizon — Cipher 3 affine two-sheet quotient

**Frozen:** 26 July 2026, before any real-language score was calculated.

## Motivation

Cipher 3 uses 83 visible symbols while the author's solved ciphers use a
42-symbol plaintext alphabet:

```text
83 = 2*42 - 1
```

The exact two-sheet lane remains open. An arbitrary pairing of 83 labels into
41 pairs and one singleton is too flexible, but the visible labels admit a
complete finite family of 83 affine involutions:

```text
R_a(x) = a - x mod 83,  a in 0..82
```

Every `R_a` has one fixed point and 41 two-element orbits. Quotienting by its
orbits therefore gives exactly 42 symbols without fitting the pairing.

This is distinct from the earlier reflection-wheel attack. That attack mapped
*transition magnitudes* on a hidden cycle. This lane pairs the displayed
symbols themselves under a fixed standard-coordinate involution.

## Frozen test

For both complete streams and marker-stripped bodies:

1. quotient every raw value by each of the 83 orbits of `R_a`;
2. on group A only, optimize one injective substitution from the 42 quotient
   symbols to the known 42-character plaintext alphabet;
3. select `a` and the substitution by group-A trigram likelihood;
4. freeze both and score groups B and C without any refit.

The language model is trained on the same public Crawford *Kalevala* corpus
used in the earlier Cipher 3 source audit. Punctuation remains part of the
42-symbol model; text is not collapsed to A–Z.

## Required control

Construct matched-length English plaintext from a held-out portion of the
training corpus. Encrypt it under one planted affine involution and a random
42-symbol substitution, choosing either representative of each two-element
orbit. The exact same two-stage search must:

- select the planted involution;
- recover a readable group-A key;
- retain readable held-out B/C text.

The plant is allowed the unavoidable global relabelling symmetry of quotient
orbit identifiers, but not a different reflection.

## Promotion and stop rules

Promote only if:

1. the planted reflection is recovered;
2. the real A-selected key gives B/C language scores near the matched
   plaintext control;
3. the decoded text is stable across independent restarts and re-encodes under
   the quotient/substitution model.

If the plant fails, the search is uncalibrated and the real score is
uninterpretable. If the plant passes but real B/C collapses, close all 83
standard-coordinate affine two-sheet quotients. Do not add an arbitrary
hidden permutation after seeing the result.
