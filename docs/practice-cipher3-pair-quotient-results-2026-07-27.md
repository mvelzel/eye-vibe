# Practice cipher 3 — projective pair-quotient results

**Date:** 27 July 2026
**Outcome:** strong calibrated negative; no plaintext recovered

## Tested family

Every candidate combines consecutive raw values over `F83`,

```text
u = x + k*y,  k in F83
u = y              (projective infinity)
```

then takes one affine two-sheet quotient `u ~ r-u`, `r in F83`, and applies
one global bijection from the resulting 42 classes to sdlwdr's established
plaintext alphabet.

Five frozen overlap/block routes give:

```text
5 * 84 * 83 = 34,860 structural architectures
```

A length-six equality-pattern likelihood ratio screens the entire catalog.
It compares the language pattern probability with the independent-uniform
pattern probability; raw pattern likelihood was rejected during control
tuning because it rewards the dominant all-distinct pattern. Twelve
candidates per route enter A-only substitution search, and eight enter final
refinement. B+C never select a structure or key.

The original [read-only author
thread](https://discord.com/channels/453998283174576133/1227024108286644284/threads/1354671018949738526)
still supplies no mechanism or source hint beyond the corpus correction and
the author's statement that the source code was lost.

## Positive controls

Independent *Moby-Dick* plaintext retained the real 18 raw lengths. One
overlapping and one disjoint architecture were hidden inside the full
34,860-model search:

```text
plant       structural rank       selected       A accuracy   B+C accuracy
overlap     route 1, global 2     exactly        100.000000%  100.000000%
disjoint    route 11, global 30   exactly         92.972973%   96.544276%
```

Frozen scores:

```text
plant       A score/trigram   B+C score/trigram
overlap        -9.032410          -7.229609
disjoint       -9.600954          -7.581465
```

The A-selected keys render untouched B/C prose. Representative control text:

```text
IR-OIL UNLESS MEDICINALLY THAT MAN HAS PROBABLY GOT A QUOGGY
SPOT IN HIM SOMEWHERE. AS A GENERAL RULE ...
```

Thus both route classes, the structural screen, and the substitution stage
are operational at the frozen budget.

## Real corpus

The real corpus was run once:

```text
selected route       stride 2, start 2
selected slope       33
selected reflection  70
A score/trigram      -11.630946
B+C score/trigram    -15.865307
```

Relative to the matched disjoint plant, the heldout deficit is:

```text
-15.865307 - (-7.581465) = -8.283842
```

Complete first-message previews from each group:

```text
A0  YS JFBJ100W.GLAT-M1?FS1FOW-
B0  M4J4J222AW2K9A6J99SXG.2U’C!WHS.PXPPB9JDV MVVQ?.8T’RSZW.1
C0  A38LS6750UI4GWT?M8TZ I2?-F Y?2JHFK5B..IY2JK9Y?U!PFM-VNNXGE!3E2UL40JF2FEU-40E!2R0OMVG1Y?X5ANFV
```

The structurally highest candidates are unstable alternatives, not a common
relation:

```text
2/2, slope33, reflection52   0.117430
2/0, slope6,  reflection9    0.110789
2/2, infinity, reflection69  0.106584
2/2, infinity, reflection47  0.101171
2/2, slope6,  reflection9    0.100832
```

## Decision

Stop this projective pair-quotient lane. A search that exactly recovers both
hidden route classes and transfers their keys to untouched prose instead
overfits the short real A group and collapses on B+C.

This is strong evidence against the frozen architecture as an English
character cipher:

- every affine-linear consecutive-pair projection over `F83`;
- every affine `83 -> 42` involution quotient;
- the five explicit overlap/block routes;
- one global bijective 42-symbol substitution.

It is not exact UNSAT. Only the structurally shortlisted candidates received
language-key optimization, and the controls calibrate English prose. The
result does not exclude triples, nonlinear pair maps, variable-length codes,
non-English conformance data, or stateful sheet schedules.

## Transferable method

An equality-pattern detector must be calibrated as a likelihood ratio.
Absolute language-pattern likelihood ranked the planted plaintext near last
because random 42-symbol streams repeatedly realize the single most common
all-distinct pattern. Subtracting its exact independent-uniform probability
moved the true relations to route ranks 1 and 11. Also preserve equal
shortlist capacity per route; otherwise longer outputs receive an accidental
selection advantage.

## Reproduction

```text
PYTHONPATH=src python3 -m unittest \
  tests.test_practice_cipher3_pair_quotient

PYTHONPATH=src python3 \
  scripts/run_practice_cipher3_pair_quotient.py --phase control

PYTHONPATH=src python3 \
  scripts/run_practice_cipher3_pair_quotient.py --phase real
```

Exact source hashes, the full search budget, and the pre-real stop gates are
recorded in the freeze document.
