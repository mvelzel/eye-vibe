# Wide architecture map — 21 July 2026

This pass deliberately starts wider than the existing deck-cipher programme.
Its purpose is to give unrelated mechanism families a cheap, falsifiable first
test before choosing another deep search.  A failed cheap necessity rejects
only the literal subclass named below, not the whole family.

## Fixed observations

- The accepted three-eye reading is overwhelmingly better than simple route,
  eye-order, reversal, and snake alternatives, and produces the contiguous
  alphabet `0..82`.
- The nine first symbols behave differently from the bodies: they enumerate a
  structured `S3` control pattern, and the three diagonal complete-message
  sums close modulo 101.
- After those symbols, the nine bodies form an exact nested prefix tree.
- Merging each copied body prefix once gives 918 labeled edges whose labels sum
  to zero modulo 101.
- The ciphertext is precomputed in native code.  A runtime clue may nevertheless
  have been added after the Eye Messages.
- Long repeated body windows preserve equality patterns.  Any proposed stateful
  cipher must explain them without assuming that equal ciphertext always means
  equal plaintext everywhere.

## Architecture lanes

| Lane | Concrete interpretation | First discriminator | State |
|---|---|---|---|
| systematic code | first symbols are checks/order fields for bodies | low-degree body moments predict all nine headers | literal moment rules negative |
| finite-field stream | symbols are states of a small recurrence over `F83` | exhaustive first-order affine recurrence | apparent excess vanishes in matched null |
| base-5 path | each trigram is an edge/state in a de-Bruijn-like walk | two-digit overlap under all component orders and reversals | literal order-two path negative |
| cross-message code | aligned 3×3 body slices are shares/codewords | determinant/minor closures after copied prefixes end | literal rank-two slices negative |
| prefix grammar | messages are leaves of a compressed grammar or trie | merge-once checksum plus a held-out recursive law | survivor; no decoder |
| hidden 101-state machine | visible symbols are 83 payload states and 18 structural/null states | independently order/type five branch nodes and thirteen exits | survivor; no assignment |
| adaptive deck | symbols select cards while the deck mutates | exact/heuristic equality-pattern constraints | extensively tested; residual arbitrary models remain |
| suffix transform | nine messages are rotations/suffix rows/BWT records | marker inequalities and literal suffix-row consistency | simple forms rejected |
| multi-tape scheduler | headers select permutations of three component tapes | one shared transducer predicts bodies | direct `S3` forms rejected |
| visual/physical mask | world geometry, sprites, or row length supplies a sieve | raw authored assets reproduce a non-fitted mask/parameter | Gate partials only |
| later in-game key | a calendar, wand, alchemy, or boss mechanic supplies an external selector | exact raw-code/asset identity and eligible chronology | active audit |
| source/crib | bodies encode a pre-existing Hermetic/Finnish text | source-backed held-out equality predictions | Waite suffix survives narrowly; full excerpts fail |

## Predeclared cheap probes

The following tests were specified before their Eye-corpus results were read.

### A. Inclusive 83-of-101 in-game selector

Inventory every direct Lua comparison of the form `Random(0,100) op n` in the
installed WAK and the archived loose early-access tree.  Record the complete
threshold histogram, exact paths, and duplicate-source issue.  Promotion
requires more than seeing the number 83: the successful outcome set must be
exactly the Eye alphabet `0..82`, and the code must supply relevant mechanism
vocabulary.  Chronology must distinguish a genuinely timestamped old asset
from a repository merely labelled early access.

### B. Base-5 de-Bruijn path

Convert each value to its three base-5 digits.  Across all six component
orders and both stream directions, count adjacent pairs whose trailing two
digits equal the next symbol's leading two digits.  Compare the best score to a
fixed-seed null that shuffles each body independently and preserves every
message length and symbol multiset.  A literal order-two path needs a dramatic
excess; an ordinary null score rejects only this path form.

### C. First-order finite-field recurrence

For every `(a,b)` in `F83²`, count body transitions satisfying
`next = a*current+b`.  Compare the exhaustive best score with the same
within-message permutation null.  This is a necessary test only for a shared,
position-independent affine recurrence; it says nothing about arbitrary deck
updates or higher-order state.

### D. Aligned 3×3 linear code

Place the nine natural-order messages in their established 3×3 header grid.
After body depth 24, where the large upper-three copied prefix ends, count
aligned slices with zero determinant over `F83` and `F101`.  Compare against
independent cyclic rotations of the nine fixed bodies, which retain local
message texture but destroy aligned cross-message coding.  A large excess
would motivate rank/minor reconstruction; a null result rejects the literal
rank-two share model.

### E. Systematic polynomial header checks

For each modulus 83 and 101, test body moments
`sum((position+1)^k * symbol)` for `k=0..4`, with signs `+/-`, against all nine
first symbols.  Report the maximum exact coverage rather than selecting a
favourite subset.  The already-known three diagonal `k=0`, modulus-101
closures are the baseline, not a fresh hit.  A useful systematic code should
predict substantially more than those three messages under one fixed rule.

## Promotion rule

No lane becomes the next deep search because it produces an evocative word,
a single residue, or a fitted plaintext.  It must make a second prediction
about held-out ciphertext structure or point to an independently authored
game selector.  Conversely, a clue added after October 2020 remains eligible
as a decoder clue; only borrowed construction material must predate the
cipher's internal construction.

## Results of the frozen probes

### A. The procedural-wand branch really is 83 of 101

The installed build contains the exact comparison twice, in
`scripts/gun/procedural/gun_procedural.lua` and `wand_petri.lua`. Both copies
make the same semantic choice inside good-card generation:

```lua
if( Random(0,100) < 83 ) then
    card = GetRandomActionWithType(..., ACTION_TYPE_MODIFIER, ...)
else
    card = GetRandomActionWithType(..., ACTION_TYPE_DRAW_MANY, ...)
end
```

Noita's two-argument integer `Random` includes both endpoints. The successful
set is therefore exactly `0..82`: 83 outcomes from a 101-value space, not 83
percent. This is an exact independent match to the Eye alphabet and checksum
modulus, embedded in relevant deck/wand vocabulary.

The match is also unusual inside the audited direct comparisons. The current
WAK has 74 `Random(0,100)` threshold comparisons across 22 distinct
operator/threshold pairs; `<83` occurs only in these two duplicated procedural
wand sources. The loose repository labelled early-access has 25 comparisons
across ten pairs and the same two copies. Its only Git commit was uploaded in
October 2022, so that label is not independent pre-Eye chronology. The earliest
independently timestamped copy found in the 61-snapshot public data repository
is commit `70696c9` on 9 February 2021. That is after the Eye Messages, making
the code fully eligible as a later decoder clue but not proving it helped
construct the ciphertext.

The complement initially looked stronger. Rolls `83..100` are not discarded:
all 18 route to `ACTION_TYPE_DRAW_MANY`, while `0..82` route to
`ACTION_TYPE_MODIFIER`. The compressed Eye trie has five branch nodes and
thirteen outgoing edges. But `5+13=18` counts internal nodes and relationships
as separate records; the corresponding recursive cast executes five internal
cards and nine leaf cards, fourteen nodes total. The exact roll is discarded
after selecting a type. This retains the bare alphabet/modulus selector but
demotes the claimed **typing evidence for the 18-record architecture**.

The checksum scopes fail separately. The lower-six subtree whose visible
residue is 70 owns 11 hypothetical node-plus-edge records, not all 18. The
all-nine scope owns 18 but has descendant residue 30, which does not close with
the missing set's residue 31. The current wand-tree decoder is rejected.

### B. Base-5 path is ordinary

The best of all twelve component-order/direction reads is the already accepted
forward order, with 52 order-two overlaps among 1,018 body transitions. In
5,000 fixed-seed within-message shuffles the range is 35..68 and the upper-tail
exceedance is `1360/5001 = 0.271946`. The literal de-Bruijn path is rejected.

### C. The affine-recurrence excess is copied-prefix structure

Exhausting all 6,889 rules over `F83` gives 34/1,018 transitions for
`next=17*current+45`. A naive within-message shuffle makes that look mildly
unusual (`2/201 = 0.009950`), but that null destroys the most important fixed
fact: many transitions are copied across exact message prefixes.

An arbitrary global relabeling preserves every equality, copied prefix, and
transition multiplicity. Under 500 such relabelings, the best-score range is
29..42 and 219 null samples meet or exceed 34; the corrected upper tail is
`220/501 = 0.439122`. Merging copied prefix nodes once changes the optimum to
26/917 under a different rule. The literal shared first-order recurrence is
rejected; the episode is also a warning to preserve the prefix trie in future
nulls.

### D. Aligned 3×3 slices are not rank-two shares

After body depth 24, the natural 3×3 grid has only 1/74 zero determinants under
both moduli. Independent cyclic rotations of the nine fixed bodies give upper
tails `3022/5001 = 0.604279` over `F83` and
`2599/5001 = 0.519696` over `F101`. There is no aligned low-rank excess.

### E. Low-degree systematic moments stop at the known diagonal

Across moduli 83 and 101, degrees 0..4, and both signs, the sole rule matching
more than one header is the already-known modulus-101 body sum with negative
sign. It matches exactly East 1, East 3, and East 5. Every other rule matches
at most one panel. No simple systematic polynomial checksum explains all nine
first symbols.

## Additional lateral controls

Two further key-free summaries were inspected after the frozen probes. They
are controls, not pre-registered discoveries.

Reading adjacent trigrams as literal points in the base-five eye cube gives a
Hamming-distance 1/2/3 profile of `115/425/478`. Its full-grid chi-square is
`9.46627`. Under 5,000 global relabelings of `0..82`—preserving the complete
equality/prefix skeleton and every transition multiplicity while randomizing
the base-five geometry—`3,713/5,001 = 0.742451` controls are at least as
extreme. The component geometry does not select a low-Hamming instruction
stream.

Taking each panel's first edge out of its deepest shared-prefix cluster gives

```text
80,29,69 / 69,78,23 / 77,60,33.
```

The second and third natural rows both sum to 170. An exact relabeling null
preserving the trie, the three diagonal checks, and all marker labels retains
that equality in `30,576,476,160 / 825,564,856,320 = 1/27` cases. The equality
was noticed post-hoc and is not selective enough to promote.

Reproduction is in `scripts/audit_noita_random_thresholds.py` and
`scripts/run_wide_architecture_probes.py`.
