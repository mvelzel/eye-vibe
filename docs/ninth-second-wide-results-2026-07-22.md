# Ninth pass, second wide slice — results, 22 July 2026

## Outcome

The three frozen lanes do not supply a decoder.

- The trailer categories reproduce the proposed shared-start precondition, but
  do not preserve any of the three concrete funny-obstacle pairs.
- The radix-five borrow result is statistically fragile and its interpretation
  fails ablation. A simpler high/low-eye comparison retains a small,
  independently held-out anomaly, but it was found post hoc and does not pass
  the family correction required for promotion.
- The strict one-worldline checkpoint model is exactly empty: every directed
  panel overlap is zero.

The comparison residue is retained as a bounded lead. It is not evidence that
the bodies are arithmetic, and it is not a plaintext result.

## A. Trailer-category XGAK

Ordinary first-occurrence keying of `A-Z0-9` by
`A BAD MAGIC CARD TRICK` exactly gives the proposed alphabet:

```text
ABDMGICRTKEFHJLNOPQSUVWXYZ0123456789
```

All nine candidate initial digits `1..9` occupy the same proposed category in
all four frozen variants. This satisfies the category-level prerequisite for
nine different first output positions to select one shared operation class.
It does not prove that the proposed XGAK machine reaches a common post-first
state; that requires the still-unknown permutations and initial deck.

The stronger immediate prediction fails. With Q on either side, and with the
back letters and digits either merged or split, the positionwise category
mismatches are:

```text
EAST / WEST       0
COPPER / SILVER   0,1,3
FROZEN / MOLTEN   0,1,3
```

Thus the proposed quotient cannot make those documented plaintext pairs use
the same operation at every position. It may still be a start selector rather
than a complete operation quotient.

The exact 36-symbol trailer alphabet also has no space, comma, or full stop.
Those are the unsupported symbols in the literal Waite sentence. Normalizing
`THAT WHICH` to `THATWHICH` gives the category tape
`1,0,0,1,2,0,1,1,0`, but its two occurrences are identical plaintext and
therefore add no new XGAK constraint.

**Disposition:** retain the exact digit-start selector; reject the claim that
the three/four categories alone explain all funny-obstacle allomorphs. Do not
fit arbitrary `S83` operations until a crib or independently authored
operation rule can demand a held-out symbol.

## K. Borrow automaton and ablation

### Frozen result

Across the seven nonliteral isomorphic contexts, the best of six digit orders
and two subtraction directions matches `63/141` two-borrow states. Under
2,000 arbitrary global label permutations the corrected upper tail is
`3/2001 = 0.001499`. Training on the first four contexts selects a convention
with `27/59`; that fixed convention scores `35/82` on the last three, tail
`10/2001 = 0.004998`.

Those controls preserve every equality and copied prefix, but not the three
known complete-message checksum facts. A harder subgroup control permutes only
labels with the same East-1/East-3/East-5 count triple and fixes all nine
marker labels. It preserves those three integer sums exactly. Under 2,000 such
controls the borrow tails become:

```text
all seven contexts        0.007496   null 37..71
first-to-last held-out    0.013493   null 11..38
```

The held-out requirement fails `0.01`. Correcting the all-context result for
the two frozen scores also gives at least `0.014992`. The separate frozen
first-order Markov score has tail `0.035482`. The exhaustive 6,806 affine
relabelings of `F83` are more favorable—`10/6806` overall and `12/6806`
held-out—but they preserve much less of the known Eye structure than the
checksum subgroup.

### The arithmetic interpretation fails

Six explicit feature variants expose what generated the preliminary result:

| feature | all-context score | arbitrary tail | held-out score | held-out tail |
|---|---:|---:|---:|---:|
| first two propagated borrow bits | 63/141 | 0.001499 | 35/82 | 0.004998 |
| first borrow bit | 90/141 | 0.056972 | 51/82 | 0.060470 |
| second borrow bit | 91/141 | 0.011494 | 46/82 | 0.170915 |
| all three propagated borrow bits | 31/141 | 0.043978 | 15/82 | 0.149925 |
| two independent digit comparisons | 63/141 | 0.001000 | 35/82 | 0.004998 |
| two digit-change bits | 76/141 | 0.106447 | 45/82 | 0.085957 |

The winning borrow order processes high eye, low eye, then middle eye, while
serializing only the first two intermediate bits. It therefore never emits a
feature of the middle eye. Removing borrow propagation entirely is at least as
strong. The result is not evidence for radix-five subtraction.

The simpler surviving feature asks, for each adjacent transition, whether the
high and low base-five digits separately increase. It preserves that two-bit
pattern across the seven isomorphic contexts `63/141` times. The first four
contexts independently select the same high/low convention (`28/59`) and the
last three score `35/82`. Its per-context contributions are:

```text
first-gap30       4/17
first-cross       8/17
first-cross-late 10/17
first-gap28       6/8
last-west4       12/29
last-east5       11/29
last-east3       12/24
```

The checksum-preserving tails are `0.005997` overall and `0.006997` held-out;
the exhaustive affine tails are `3/6806 = 0.000441` and
`23/6806 = 0.003379`. This is the slice's only residue worth retaining.
However, it was identified by inspecting a six-member ablation family.
Bonferroni correction across those six variants alone gives at least
`0.035982` and `0.041982`. It consequently earns an independent future test,
not depth or a cipher claim.

**Disposition:** reject the carry/borrow interpretation. Retain exactly one
scoped hypothesis: corresponding transitions in true plaintext-isomorphic
windows may preserve a one-sided product order on the first and third eyes
more often than arbitrary equality/checksum-preserving relabelings. A valid
next test must be chosen without inspecting these seven scores and must predict
a new context, asset quantity, or operation—not merely try more digit
relations on the same windows.

## N. One worldline, nine checkpoints

Every one of the 72 directed panel pairs has literal suffix/prefix overlap
zero. Every pair also has equality-isomorphic overlap zero when at least two
repeat validations are required. Consequently all `9! = 362,880` panel orders
score zero, including canonical placement and the independently decoded
East-5-first trail.

**Disposition:** reject direct checkpoint continuation, literally and under
one injective relabeling. This does not reject a transformed worldline, but a
transform must be independently supplied before that broader model becomes
testable.

## Reproduction

```bash
PYTHONPATH=src python scripts/run_ninth_second_slice.py --controls 2000
PYTHONPATH=src python -m unittest tests.test_ninth_second
```

The implementation is in `src/eye_mystery/ninth_second.py`. The seeded run
reselects all advertised conventions inside every control. The affine family
is exhaustive; the arbitrary and checksum-subgroup tails use the standard
plus-one correction.
