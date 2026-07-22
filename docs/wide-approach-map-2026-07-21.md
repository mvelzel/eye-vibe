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

## Second breadth expansion: complement spaces and construction traces

This expansion follows the failure of the literal procedural-wand tree.  It
does not deepen the nearest surviving number match.  Instead it opens another
set of mutually different representation and construction families.  A
targeted read-only Discord search after the first arithmetic pass corrected
the novelty claim: `83+42=125` was discussed publicly in July 2023, a paired
42-to-83 homophone construction in January 2024, and both
`42=(83+1)/2` and `42=5^3-83` in April 2024.  The count and generic pairing are
therefore longstanding community leads.  The older scratch research digest
had also already preserved the “42 blanks” fact; its omission from the current
repository ledger was an audit failure, not an absence of prior local work.
The contribution of this pass is the explicit low-capacity formulations and
their calibrated tests.

Several exact counts motivate the fan-out.  They were noticed retrospectively
and are not evidence until a frozen rule predicts something else:

```text
5^3 = 125 = 83 visible trigrams + 42 unused trigrams
83 = 2*42 - 1
orbits of x -> -x on Z83 = 1 + 41 = 42
non-self transitions from one of 83 labels = 82 = 2*41
125 = 83 visible + 18 values through modulus 101 + 24 values above it
marker-free body length = 1027 = 13*79
merged body-trie edge count = 918 = 34*27 = 9*102
```

The 42-character alphabet from sdlwdr's solved exercises is useful calibration,
not developer-authored Noita evidence.  The `18+24` split is especially
post-hoc: 18 was already compared with compressed branch records, while 24 is
also the deepest upper-family shared-prefix length.  The earlier scope failure
still applies and no assignment follows from these equations.

| Lane opened or revisited | Concrete interpretation | Cheap discriminator before deep work |
|---|---|---|
| **Visible/unused cube dual alphabet** | Values `0..82` are ciphertext glyphs; the missing base-five trigrams `83..124` are a disjoint 42-symbol plaintext/control alphabet. | Exhaust only canonical offset/reflection maps between the two contiguous sets and require language or held-out equality structure. |
| **Reflection quotient of `C83`** | A center on the 83-cycle identifies `+d` with `-d`, giving exactly 42 orbits.  A header may name the center. | Test all 83 global centers, nine marker centers, and the rolling previous-symbol center under one frozen natural-42 ordering; compare to matched relabelings. |
| **Three-tier trigram type space** | The full cube is `83 payload + 18 checksum/control + 24 framing` rather than one 125-glyph alphabet. | Use contiguous tiers only; demand that one natural ordering of the 18 and 24 states closes a second branch/check relation without subset selection. |
| **No-repeat enumerative code** | Because the next label never equals the current one, each transition can be ranked canonically among 82 allowed labels and split into a sign bit plus one of 41 magnitudes. | Decode standard/reversed exclusion ranks, both parity splits, and one fixed 41-symbol alphabet; reject unless structure beats no-double, prefix-preserving controls. |
| **Base-five carry/borrow side channel** | Arithmetic carries between the three displayed eyes may carry control bits while the numeric value remains cipher-like. | Enumerate six component orders and both subtraction directions; score the two carry bits and signed digit residuals against global-label nulls. |
| **Packed-base-seven framing language** | Padding, five directions, and row separators in the hardcoded base-seven serialization may be typed records rather than irrelevant storage. | Reconstruct the exact framed streams including row and chunk boundaries; test only boundary-conditioned invariants that disappear when separators are shuffled. |
| **Snapshot/delta tree** | The nine bodies are hand-copied versions or branches of one worksheet/object, so the prefix tree is construction history rather than repeated plaintext. | Build minimal edit scripts between sibling leaves and test whether edits concentrate at common columns, record ends, or stable-sort boundaries. |
| **Forked PRNG trajectories** | Shared prefixes are identical seeded generator histories; branch points are reseeds or injected controls. | Test low-capacity linear/xorshift/LCG relations on suffixes and cross-branch state offsets, with an exact held-out suffix requirement. |
| **Local rewrite or cellular rule** | Each stream is a generated trajectory whose next symbol depends on a short context, not encrypted prose. | Measure contradictions for arbitrary order-1 through order-4 context functions and compare their minimum description length with trie-preserving nulls. |
| **Metamorphic 3×3 operator suite** | Cell `(i,j)` is the output of one operation on two of three hidden objects; the diagonal is a self-test and off-diagonal cells are directed pairs. | Test symmetric-pair identities, edit transforms, common suffixes, and cycle compositions before any numeric group is fitted. |
| **Quasigroup/Latin relation** | The six non-self S3 headers identify ordered pairs and bodies serialize a partial multiplication or comparison table. | Seek key-free uniqueness laws of the form `(row,input)->output` across aligned contexts and require the third row to be predicted. |
| **Delayed three-tape scheduler** | The three eyes are separate control/data tapes combined with fixed lags, not three simultaneous base-five digits. | Exhaust small relative lags and six tape orders; measure cross-tape mutual information and prefix preservation against per-tape cyclic shifts. |
| **Header as length/shape descriptor** | The first trigram may encode full-row count, tail length, branch depth, checksum type, or a tuple of these rather than text. | Exhaust affine and digitwise rules over only independently present quantities, correct for the whole rule table, and demand more than the known three checks. |
| **Factored record geometry** | `1027=13*79` or `918=34*27` may specify a rectangular non-text object; 13 also counts compressed exits and 34 counts complete displayed records. | Lay out only marker-derived trie traversals in those dimensions and test row/column conservation against identical factorizations of matched nulls. |
| **Residual random cover plus planted skeleton** | The equality windows, prefixes, and checks are deliberate verification marks embedded in otherwise random or strongly encrypted filler. | Remove every forced copied node once, then compare residual unigram, digram, compression, and context statistics with a fitted no-double random generator. |
| **Serialization side channel** | The 64-bit chunk divisions, leading-zero recovery, padding digits, and shortened final chunks carry metadata outside the visible trigrams. | Inventory exact base-seven capacities and padding per authored constant; accept only a pattern invariant under decompiler high-word repair. |
| **Metadata-only instruction** | The actual answer may be assembled from markers, branch depths, lengths, locations, and checks rather than from a body plaintext. | Predeclare one serialization of independently decoded metadata and require checksum/grammar closure without selecting words after rendering. |
| **Later lookup table rather than algorithm** | A post-2020 asset may map 83 visible labels or 42 quotient classes directly, like Cessation's external state cycle. | Search game-authored tables for exact domain coverage and chronology; require one held-out mapping, not shared numerology. |

### Breadth protocol for this expansion

The first implementation pass will touch unrelated lanes rather than spending
its budget on the attractive `83/42/125` coincidence alone:

1. reflection-quotient and no-repeat-rank outputs;
2. arbitrary short-context determinism;
3. header-versus-length/shape rules;
4. small-lag three-tape dependence;
5. the two factored record layouts;
6. residual-randomness after merging copied prefixes.

Each probe must preserve the exact prefix/equality skeleton in its null model
when that skeleton affects the statistic.  Only after all six have a bounded
result will this map be rescored and at most two survivors receive deeper
cryptographic or asset work.

## Results of the second fan-out

The direct literal forms are mostly negative:

- The best of all 83 global reflection centers has normalized IoC `1.067915`;
  171 of 200 global-label relabelings do at least as well
  (`172/201 = 0.855721`).  Using each message marker as its center gives
  `1.011314` (`63/201 = 0.313433`), and using the previous symbol as a rolling
  center gives `1.012449` (`116/201 = 0.577114`).  The direct natural-42 output
  is visibly alphanumeric gibberish.  This rejects the canonical
  distance-labelled quotient, not every possible ordering of the 42 orbits.
- Canonically ranking each transition after deleting the forbidden current
  label gives normalized IoC `1.026457` for `rank//2` and `1.045601` for
  `rank%41`; the sign/high-half bit is `51.607%` one.  The best class statistic
  has matched upper tail `38/201 = 0.189055`.  The literal no-repeat
  enumerative decoder is not selected.
- The strongest delayed component-tape relation is ordinary: `0.142678` bits
  at zero lag between the first two eyes, with global-relabel upper tail
  `59/201 = 0.293532`.
- Arbitrary next-symbol functions of context orders one through four have
  matched upper tails `0.562874`, `0.407186`, `1.0`, and `0.998004` under
  prefix-tree-preserving shuffles.  The apparent high-order determinism is
  sparse-context memorization, not a local generator.
- The best signed-offset rule connecting a header to message length, row
  count, tail, or display height matches four panels.  It is exceeded in
  `988/1001 = 0.987013` marker-permutation controls.
- The post-hoc `13x79` raw-body layouts have at most one zero row/column sum,
  with global-relabel upper tail `175/201 = 0.870647`.
- Merging copied prefixes once moves the distribution toward, rather than away
  from, uniform: entropy rises from `6.267139` to `6.289341` bits and normalized
  IoC falls from `1.071586` to `1.028964`.  This is compatible with a planted
  skeleton plus high-entropy cover, but is not by itself a decoder.

The initially surviving `34x27` layout received the promised stricter audit.
In the fixed marker-derived depth-first and breadth-first serializations it has
three and four zero row/column sums modulo 101.  A rejection sampler preserves
all nine marker labels and the complete diagonal message count vectors, then
conditions on the already-known merged-trie sum of zero.  Among 5,000 accepted
relabelings, 33 have selected maximum four and two have five.  The corrected
conditional upper tail is therefore

```text
36/5001 = 0.00719856.
```

This is a genuine conditional curiosity but not a discovery probability.  The
factorization was noticed retrospectively, and the 27-wide blocks do not align
with trie returns: the depth-first phase-zero cut hits none of eight structural
boundaries; the breadth-first cut hits only three of 135.  The zero rows cross
singleton suffixes without a common structural role.  If all 27 cyclic record
phases are admitted, the selected maximum remains four but 105 of 1,000
strict controls reach at least four (`106/1001 = 0.105894`).  Thus the numeric
effect stays logged, while the current record interpretation is demoted.

No lane earns a deep decoder from this fan-out.  The most coherent residual
question is narrower: the exact 42-class complement has a second canonical
ordering not covered by circular distance—the multiplicative quotient
`F83*/{+1,-1}`, which has order 41 plus the zero class.  A bounded discrete-log
ordering test is admissible; arbitrary permutations of the 42 classes are not.

That final bounded test is also negative.  All 40 primitive generators of
`F83*`, all 83 global centers plus the per-message marker centers, and natural
zero placements at plaintext positions 36 and 41 give 6,720 models, with the
orbit of field value 1 fixed at plaintext class zero.  Against
the large English corpus, the best average tetragram score is `-16.94394`,
versus `-9.03528` for held-in prose and a `-17.14575..-17.02949` range for 200
uniform controls.  Against Finnish *Kalevala*, the corresponding values are
`-16.08232`, `-10.61812`, and `-16.20614..-16.11668`.  The tiny advantage over
uniform is unsurprising after selecting the best of thousands of candidates;
the previews are alphanumeric gibberish.  Both canonical low-capacity
83-to-42 decoders are rejected.  Revisit the complement only if an independent
game asset orders the 42 classes.

The packed-base-seven lane is independently negative.  A greedy encoder that
appends renderer newline symbols, maps them with the five directions to digits
`1..6`, adds the documented zero padding digit, and takes the longest prefix
fitting in a u64 reproduces all 150 engine constants exactly.  The 21- versus
22-symbol nonfinal blocks are forced by overflow, while final short blocks are
ordinary suffixes.  Boundaries cross 69 newlines and terminate on only 16.
Treating the 141 capacity choices as bits gives a best printable-byte statistic
with fixed-weight upper tail `8259/10001 = 0.825817`.  Therefore serialization
does not add an out-of-band key; any future use of capacity must justify why a
decoder would recompute that feature from the ciphertext.

The snapshot/delta lane is the first survivor of the third cycle, but only at
the architectural level.  In the two deepest sibling trios, unrestricted edit
alignment saves just 12 operations over fixed-index substitutions and trailing
truncation; only five of 2,000 prefix-tree- and exit-preserving suffix shuffles
are as low (`6/2001 = 0.0029985`).  The known equality windows make the bodies
unusually position-synchronous.  Their positions do not favor the 26-column
display: column-concentration and row-edge tests have upper tails `0.839580`
and `0.653673`.

A new wide transform follows from that survivor without assuming plaintext.
The equality relation among three aligned sibling values has exactly five set
partitions.  The two deepest trios thus yield two five-state tapes, suggesting
either new base-five trigrams or the two coordinates of a 5x5 alphabet.  Both
bounded literal forms are negative.  The optimized `0..82` range fit is more
common in state-count controls (`0.986028`), and the exhaustive Polybius
relabeling/reversal search produces repetitive gibberish with selected upper
tail `0.896208`.  Generic Polybius proposals are longstanding; targeted
read-only Discord searches did not locate the equality-partition variant, but
absence from those searches is not a novelty proof.  Preserve position
synchrony and stop fitting the five states without a game-authored selector.

The metadata-only lane produces one exact survivor.  In `BEXIT` breadth order,
sum each branch node's distinct outgoing labels and add its depth modulo 101.
The five results are `99,99,0,89,89`.  The paired-zero-paired pattern supplies
three linear constraints independent of the three diagonal sums and full-trie
checksum (rank `4 -> 7`).  It occurs in exactly `1/135` of the marker-fixed,
diagonal-preserving subgroup and at corrected rate `27/5009 = 0.0053903` after
also conditioning on full-trie closure in a seeded sample.  Only coefficient
one survives the full family `exit_sum + k*depth`, `k in Z101`.

This remains retrospective: the branch objects, breadth order, and modulus had
prior support, but the combine operator did not.  Retain it as a possible
error/check grammar and demand an external combine rule or held-out prediction
before interpreting the residues.

Reproduction is in `scripts/run_second_wide_probes.py` and
`scripts/calibrate_factored_34x27.py`; the quotient-log test is in
`scripts/search_reflection_quotient_logs.py`; the storage reconstruction is in
`scripts/analyze_storage_serialization.py`; the delta tests are in
`scripts/analyze_snapshot_delta.py` and
`scripts/search_partition_polybius.py`; the metadata identity is in
`scripts/analyze_metadata_instruction.py`.

## Fourth bounded audit: exact authored lookup tables

A raw installed-data inventory searches balanced Lua literals, XML child
lists, and line-oriented text for exact sizes 5, 42, 83, and 101. The only
83-entry family is four identical copies of `gun_names` in procedural-wand
code; there are no 42- or 101-entry Lua tables. This count has been known in
Discord since 2022. The table is nevertheless a legitimate construction-key
candidate because the archived early-access tree contains the identical list
and lacks the Eye payload, although that archive was published only in 2022.

The lookup fails two bounded attacks. Fifteen deterministic word features,
both marker policies, and full family reselection under shuffled name-label
assignments give corrected English-score tail `316/2001 = 0.157921`.
Alphabetical/reverse name decks transferred into the exact solved
practice-#5 recursive shuffle put at best `560/1027` outputs in `0..41`, with
corrected tail `240/2001 = 0.119940`. Therefore the literal table stays paused
unless another authored asset says how to consume it. Details are in
`docs/game-authored-table-audit.md`.
