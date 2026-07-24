# Nineteenth wide horizon — Earthquake circle as Eye parameter diagram

## Why this reopens now

The Earthquake/Holy-Mountain magical circle has been discussed as a possible
Eye clue for years. Directly keywording `BDMAGICK` into deck and clock ciphers
was already negative. A different relationship becomes sharper only after the
validated final-row anchor record:

```text
natural copied-opening lengths       24,5,20
final trim                            20
final anchor starts                   16,18,17 = 16 + 021
clean repeat gap                      11 = 10 interiors + endpoint
marker component orders               six elements of S3
renderer alphabet                     five eyes + newline
```

Those are almost exactly the circle's independently authored finite
vocabulary. This is a possible parameter diagram, not evidence that the rune
letters spell a plaintext key.

## Ground-up asset provenance

The installed WAK routes both Earthquake and Holy Mountain collapse through:

```text
data/entities/projectiles/deck/crumbling_earth_effect.xml
data/scripts/buildings/workshop_collapse.lua
  -> data/entities/particles/image_emitters/magical_symbol[_fast].xml
  -> data/particles/image_emitters/animated_emitter[_large].png
```

The installed images have SHA-256:

```text
animated_emitter.png
0e752d47688bfe88f196bf312c98e720f6391b5cf616e145ed2ee8ca15ba591d

animated_emitter_large.png
7d839270f5abf0516faaa41d077f21181009a0a833cf2ab384dcf3a38475c9be
```

The same paths in
[`defektu/noita-early-access-data`](https://github.com/defektu/noita-early-access-data)
are byte-identical. That repository was uploaded later and is not by itself a
cryptographic timestamp, but it supports the asset being from an early-access
build. The magical symbol also appears in pre-1.0 trailer/promotional
material. Thus it is chronologically eligible as construction material, not a
later explanation invented after the Eyes.

The current community transcription, beginning at the small authored gap, is
documented on the
[`Mysteries and Oddities`](https://noita.wiki.gg/wiki/Mysteries_and_Oddities#Earthquake_Circle)
page:

| row | content | length | distinct | primitive period | counts |
|---|---|---:|---:|---:|---|
| outer letters | `KMGICKMGICKMGICKMGICKMGICKMGICKM` | 32 | 5 | 5 | `K,M=7`; `G,I,C=6` |
| zero band | `000000000000000000000000` | 24 | 1 | 1 | `0=24` |
| alternating band | `10101010101010101010` | 20 | 2 | 2 | `0=10,1=10` |
| irregular band | `11110111011101110` | 17 | 2 | 17 | `0=4,1=13` |
| inner letters | `AGICKMAGICKMAGICKMAGICKM` | 24 | 6 | 6 | every letter `=4` |

The two circulated 17-bit transcriptions differ only by rotation/reversal;
the small gap must fix phase, while clockwise versus anticlockwise remains a
real two-way ambiguity.

## Prior art boundary

Do not claim the broad circle/Eye link as new:

- in October 2021, Discord already noted that the first and final copied
  openings have lengths 24 and 20, matching circle bands;
- in March 2026, Nick 2.0 explicitly added the middle length 5, the five
  distinct `MGICK` letters, and the five eye types;
- in June 2023, mill proposed treating the 17-bit band as a 17-position
  cipher wheel with the alternating band affecting every other position;
- other discussion connects the circle's `24,20,17` geometry to a diamond
  asset with radii `24,20,16`.

The project-original synthesis is narrower: the newly validated final anchor
record supplies an objective consumer for the previously loose `20/17/10/6`
vocabulary.

## Exact candidate selector

The most economical construction reading is:

```text
20-ring circumference          remove the final family's 20-symbol opening
17-ring circumference          one-based address 17 -> zero-based start 16
W4 component order 021         starts 16,18,17 across E4,W4,E5
20-ring balanced population    ten selected/unselected events
repeat framing                 A + ten interiors + A -> gap 11
period-6 inner rune ring       six S3 component-order controls
period-5 outer rune ring       five visible eye directions
```

This predicts every previously unexplained selector in the final landmark
record:

```text
trim=20, base=16, order=021, gap=11
```

It was assembled after seeing those facts and must not receive a fresh
random-tail claim. Its value is explanatory compression and the prospective
predictions below.

## Wide map before depth

| Lane | Candidate role | First falsifiable test | Stop rule |
|---|---|---|---|
| **A. Five-to-six alphabet augmentation** | Outer `MGICK` is the five visible eye directions; inner `MAGICK` adds the renderer newline as the sixth symbol. | Search the sprite/rune ordering and renderer code for an independently fixed eye-direction-to-rune correspondence. If found, apply that one symbol order to the factoradic headers. | Without a non-Eye mapping, `5` and `6` are only cardinalities; do not scan `5!` rune assignments and report the best. |
| **B. Natural-family trim diagram** | `24`, period `5`, and `20` select the three maximal copied openings. | Enumerate the fixed displayed triplet partition and all 280 unlabeled three-triple partitions; record whether `24/5/20` is unique, while acknowledging that the asset-number match is post-hoc. | Partition rarity does not prove the circle link and may not be multiplied with the known prefix evidence. |
| **C. Final address diagram** | `20`, `17`, balanced count `10`, and W4 `021` produce trim, base, gap, and panel order. | Treat the recipe above as fixed and ask it to predict a new field, not merely restate anchor coordinates. | No fresh p-value for the already seen coordinates. |
| **D. Irregular 17-bit mask** | The unused actual bit pattern is a selector over 17-symbol slices beginning at the circle-selected final starts. | **Completed:** forward/reverse and ones/zeros on conditionally matched final bodies. | All four variants score zero on all four registered held-out metrics; corrected tail `1`. Close direct masking at these starts. |
| **E. Six-way component control** | Inner `MAGICK` period 6 means the first six header edges enumerate S3, while the final row executes selected orders. | Derive one ordering/sign convention from the circle gap and rune direction, then test an unused first/second-row marker role. | Six as a bare cardinality is insufficient; no arbitrary rune-to-permutation assignment. |
| **F. Physical wheel timing** | The 17 and 20 bands are coupled rotating schedules; an eye trigram samples three radii at each tick. | Reconstruct only the two physical directions and the authored gap phase, then test whether the nine ciphertext equality skeletons survive one shared wheel state rule. | If a model needs panel-specific phase or fitted substitutions, stop. |
| **G. Diamond corroboration** | The reported diamond radii `24,20,16` independently repeat the two trim lengths and zero-based final address. | **Completed:** acquire the original document, Discord attachment, WAK assets, and spawner. | The quoted numbers are generated by an analyst's radius-six Manhattan board, not the sprite. Reject this as independent numeric corroboration. Preserve the separate exact desert-glyph transform. |
| **H. Archaeology** | Version deltas may reveal whether circle bands were edited to teach the Eye construction. | Hash the magical-symbol images across dated depot manifests and earliest public trailers. | An unchanged old asset establishes eligibility, not intent; a later edit must predict a role. |

## Ranking

| Lane | Evidence fit | Falsifiability | New information | Independence | Priority |
|---|---:|---:|---:|---:|---:|
| D. irregular mask | — | — | — | — | **closed** |
| G. diamond geometry | — | — | — | — | **closed** |
| A. five-to-six alphabet | 5 | 4 | 5 | 2 | **16** |
| E. six-way control | 5 | 4 | 4 | 3 | **16** |
| F. wheel timing | 4 | 4 | 5 | 3 | **16** |
| B. family trims | 5 | 3 | 3 | 2 | **13** |
| C. final address | 5 | 3 | 3 | 2 | **13** |
| H. archaeology | 4 | 3 | 3 | 3 | **13** |

## Disposition

Lane D was the first prospective cryptographic test because the *content* of
the 17-bit band had not been used to fit the selector. Its exact slices,
orientations, metrics, and matched null were frozen before inspecting scores.

Lane G is now audited. The installed diamond glyph is a `23×20` decorated
ruin block, but `24,20,16,85` come from a constructed radius-six Manhattan
board using walk lengths `1,2,3`; they are not authored pixel counts. The
claimed independent corroboration is rejected.

The acquisition did recover a different exact lead. Diamond, three-oval, and
`¡!¡` blocks are the three decorated desert pieces sharing spawn weight
`.6`. Defektu's document uses them to pair accepted trigrams with orders
`y=021`, `x=120` and emit `5x+y` or `x²+y`. Both published outputs reproduce
exactly. The squared output's high IoC partly comes from its many-to-one
`.0624` baseline; after maximizing over all six relative component
alignments, matched 20,000-control tails are `.019199` and `.013799`.
Preserve the transform, but do not promote it as a decode. Full audit:
[`twentieth-diamond-reading-audit-2026-07-24.md`](twentieth-diamond-reading-audit-2026-07-24.md).

Lane D is now negative. After removing the known gap-11 endpoints, all four
registered mask variants score zero for nontrivial skeleton, common repeats,
supported partial bijection, and aligned numeric equality. Every one of
50,000 controls is at least observed; corrected tail `1`. Results:
[`twenty-first-earthquake-mask-results-2026-07-24.md`](twenty-first-earthquake-mask-results-2026-07-24.md).

Do not rotate or shift the failed mask. The next Earthquake action must move
laterally to physical wheel timing or wait for an independently fixed
rune-to-eye/component ordering.
