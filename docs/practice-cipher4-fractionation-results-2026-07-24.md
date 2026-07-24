# Practice Cipher 4: homophone and fractionation results

## Result

Cipher 4 remains unsolved. Three bounded tests close three plausible
interpretations of the already recovered 57-rank action stream:

1. the 200-symbol common block is not an exact static-homophone rendering of
   the four public English/Finnish source texts tested;
2. the binary/ternary remainder is not a stable lane selector under the
   frozen demultiplexing family;
3. quotient and remainder were not paired at different short-block positions
   under the frozen typed reassociation family.

The quotient/remainder observation is still a descriptive fact, not a
plaintext or codec. The hypotheses and thresholds were frozen in
[`practice-cipher4-fractionation-freeze-2026-07-24.md`](practice-cipher4-fractionation-freeze-2026-07-24.md).
Lane A was found while inventorying the gap and is explicitly exploratory;
lanes B and C were scored only after their families and controls were fixed.

## A. Exact source-homophone fingerprint

For the common block at portion index 1, offset 6, length 200, the recovered
action stream has 50 symbols and 150 repeated-position constraints. A static
homophonic encoding must map every occurrence of one action symbol to the same
source character. Different action symbols may map to the same character, so
the test imposes **no** cap on homophones.

No compatible window occurs in either letters-only or space-preserving
normalization of:

| Corpus | Letters only | Letters + spaces |
|---|---:|---:|
| *Sherlock Holmes* | 446,804 | 555,727 |
| Crawford's English *Kalevala* | 643,085 | 786,014 |
| Finnish *Seitsemän veljestä* | 504,356 | 606,010 |
| Finnish *Kalevala* | 446,006 | 531,219 |
| **Total** | **2,040,251** | **2,478,970** |

This is an exact equality-fingerprint exclusion for these concrete
normalizations and passages. It does not exclude another source, a
context-dependent homophone, or a mechanism that changes equality.

Reproduce with
[`scan_sdlwdr_cipher4_homophonic_sources.py`](../scripts/scan_sdlwdr_cipher4_homophonic_sources.py);
`--maximum-homophones 0` requests the uncapped test.

## B. Selector demultiplexing

For widths two and three, write each rank as `rank = width*q + r`. The frozen
family treats `r` as a lane tag, scores the `q` lanes separately or
concatenated under every lane order and reversal mask, selects on portions 1
and 2, and evaluates that fixed convention on portion 3. Each of 2,000 null
runs shuffles selectors within portions and repeats the complete train-side
selection.

The selected real convention was:

```text
w3:concatenate:order=1,2,0:reverse=011
train improvement:    +1.032855526
held-out improvement: -0.102488285
null range:            -1.675509850 .. +1.421053377
null mean:             -0.070234679
corrected upper tail:  1080/2001 = 0.539730135
```

It fails even before multiplicity correction because the selected transform
hurts the held-out portion.

The matched planted fixture interleaves two independently substituted English
streams with explicit binary lane tags. The same audit gives:

```text
selected:              w2:concatenate:order=0,1:reverse=00
train improvement:    +1.480881658
held-out improvement: +1.198863859
null range:            -1.809303189 .. -0.092163750
null mean:             -0.876362920
corrected upper tail:  1/201 = 0.004975124
```

The positive control demonstrates that the family and statistic can recover
the mechanism they are meant to test.

## C. Typed coordinate reassociation

This family preserves the unequal coordinate types. Within blocks of periods
2 through 32 it holds the quotient sequence fixed and pairs it with selectors
shifted left, shifted right, or reversed. Both widths give 186 candidates.
Controls shuffle selectors within each portion and repeat complete model
selection.

An order-8 equality-pattern model failed its planted control, so its real score
was declared inadmissible. Orders `8,10,12,14,16,20` were then compared only
on the planted fixture. Order 14 was the smallest that exactly selected the
planted width-3, period-7 inverse and was frozen before scoring real data.

The real result, with 100 controls, was:

```text
selected:              w3:p2:shift-right
train improvement:    +0.149509731
held-out improvement: -0.365859218
null range:            -1.229652676 .. +1.114933114
null mean:             -0.047874727
corrected upper tail:  77/101 = 0.762376238
```

The period-7 planted reassociation is recovered exactly:

```text
selected inverse:      w3:p7:shift-left
train improvement:    +2.725635164
held-out improvement: +2.495782837
null range:            -1.247841949 .. +1.264680961
null mean:             +0.079438937
corrected upper tail:  1/101 = 0.009900990
```

The real family is negative. One hundred controls suffice to reject promotion:
77 controls exceed the observed held-out improvement.

## Transferable method

- Test a proposed homophonic source by its equality fingerprint before
  guessing a key; unlimited many-to-one mappings still require equal cipher
  symbols to align with equal source characters.
- Separate model calibration from real-data selection. A statistic that
  cannot recover a planted instance is not allowed to pronounce on the real
  puzzle.
- Select an entire transform family on training portions and evaluate one
  fixed winner on held-out material. A good training score is not evidence
  when it reverses out of sample.
- Preserve coordinate types when the domains differ. Ordinary Bifid-style
  mixing would illegitimately put a 19-state value into a ternary slot.
- The exact `3×19` decomposition remains interesting only descriptively.
  These results reject two natural uses of it; they do not erase the numeric
  observation.

Implementation is in
[`practice_cipher4_fractionation.py`](../src/eye_mystery/practice_cipher4_fractionation.py)
and
[`analyze_sdlwdr_cipher4_fractionation.py`](../scripts/analyze_sdlwdr_cipher4_fractionation.py).

## Remaining boundary

The frozen lanes involving run packets, type-preserving deck deals, quotient
digraph packets, boundary symbols, and edited lane templates have not been
executed. They are lower priority after B and C fail. Resume them only if an
author hint names a matching deck operation or a packet model supplies a
qualitatively different invariant; do not extend the negative selector family
with fitted codebooks.
