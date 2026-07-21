# Breadth-first novel synthesis — 21 July 2026

This checkpoint deliberately stops extending the current favorite cipher.
Its purpose is to widen the mechanism space, preserve strange but coherent
ideas, and only then choose a small number of discriminating tests.  “Novel”
here means not found in the sources or local research log checked so far; it
cannot prove that nobody has privately considered an idea.

## Frozen observations

These are inputs to the synthesis, not interpretations:

- The accepted trigram reading gives 1,036 values, exactly the contiguous set
  `0..82`, in nine streams of lengths `99,103,118,102,137,124,119,120,114`.
- No stream has an adjacent repeated value.  After the distinct first value,
  every stream shares two values.  The complete proper prefix depths are
  `24` for East 1/West 1/East 2, `5` for the other six, `9` for
  East 3/East 4/West 4/East 5, and `20` for East 4/West 4/East 5.
- Strong repeated equality patterns, reconvergences, and context maps exist.
  They are compatible with arbitrary GAK/XGAK but exclude cyclic, dihedral,
  and both affine transitive groups under the repeated-plaintext premise.
- The nine first values jointly encode a unique three-state trail order and a
  prefix-trie-compatible order.  Their unused digits form a cyclic BWT whose
  independently selected row decodes to `Fi!` up to rotation.
- Full message sums modulo 101 in the natural 3×3 arrangement are

  ```text
   0 84  7
  53  0  1
  32 88  0
  ```

  The three odd-East/main-diagonal first values are the exact additive check
  values that close their bodies modulo 101.
- The displayed format has 34 complete 26-trigram row-pairs and nine shorter
  final row-pairs.  The final lengths are `21,25,14,24,7,20,15,16,10` in
  canonical message order.
- The installed renderer stores base-7-packed row arrays and performs no
  runtime decryption.  A clue added after 2020 may still decode precomputed
  ciphertext; a borrowed source text must predate the internal construction.
- The later Gate Guardian asset reproduces the main-diagonal mirror-difference
  total 70 and some routing/checksum vocabulary, but the proposed full Type6
  decoder is not derivable from frozen asset rules.
- Known-plaintext recovery of arbitrary permutation-deck keys is real but
  underdetermined.  The local solver reaches arbitrary deck size 14 on a
  54-symbol toy and stalls at 16–26 under the same 30-second bound.

## Assumptions now suspended

None of the following is a frozen fact:

- the payload is natural-language prose;
- one trigram corresponds to one plaintext character;
- an equality-pattern isomorph must be a repeated plaintext substring;
- the nine panels are independent messages rather than rows, traces, shards,
  samples, or contexts of one object;
- every panel resets the same state, or all panels use the same cipher layer;
- `83` is the state-space size rather than the number of visible labels;
- the first trigram is merely a header and never participates in a transform;
- the useful arithmetic field is `F83` rather than `Z101`, base five, or no
  numeric field at all;
- the answer is Finnish, English, Hermetic prose, or even text;
- the intended clue was present when the Eyes first shipped.

## Wide mechanism map

Each family has a cheap observation that could separate it from a fitted
GAK/crib story.  The list is intentionally wider than the eventual work queue.

| Family | Why it fits something real | First discriminating test |
|---|---|---|
| **Sampled suffix/LCP rows** | Distinct preceding values, a body prefix trie, a marker-selected trie order, and a literal marker BWT are exactly suffix-array vocabulary. | Ask whether one alphabet order sorts the bodies in the marker order; then test the stronger LF/row-shift identity. |
| **Trie-edge payload** | The copied prefixes may be structural framing; only branch edges may carry independent information. | Serialize each distinct trie edge once in every marker-derived traversal and test checksums/isomorphs against prefix-tree-preserving controls. |
| **Nominal allocation/cache trace** | Equality patterns become meaningful while numeric names remain flat and arbitrary; Gate's later cache/allocation imagery would be relevant without being a decoder. | Convert each body to first-use, reuse-distance, and live-cache events; look for a low-state grammar replicated outside the famous six windows. |
| **`Z101` walk with 83 visible and 18 null states** | The exact modulus-101 closures and later Gate grid become native; `83` need not be the hidden state count. | Fit only low-capacity step/null schedules and demand prediction of an unfit message endpoint or checksum marker. |
| **3×3 parity/check object** | Three diagonal self-check records and six signed off-diagonal records resemble a code or directed comparison matrix. | Test low-rank, cycle, determinant, and Reed–Solomon-style relations under frozen row/column symmetries; require a held-out cell. |
| **Twenty-six-column records** | The renderer repeatedly gives exact 26-wide records, which could index letters or columns rather than wrap prose. | Measure row permutations, column equality profiles, cross-row maps, and whether column-wise reading lowers state/alphabet complexity against row-preserving nulls. |
| **Three-state control transducer** | The markers already form a three-state trail; prefix families could be traces that share control states until branching. | Infer the smallest deterministic or reversible control machine jointly from trail edges and body divergence points. |
| **Graph/Euler walk** | No self-loops, flat vertex usage, copied route prefixes, and reconvergence are graph-trace properties without encryption. | Compare directed-edge multiplicities, cycle bases, and path endpoints with degree-preserving randomized walks. |
| **One continuous stream, nine cuts** | Marker orders may specify concatenation, BWT order, or reset locations rather than nine messages. | Exhaust marker-derived cut orders while scoring only invariants that survive arbitrary symbol relabelling; demand cross-boundary repeat prediction. |
| **Variable-length token or compressed data** | A large visible alphabet and language-resistant output need not be character substitution. | Test canonical prefix codes, run/phrase dictionaries, and entropy by 26-wide record without choosing semantic labels. |
| **Chosen self-test vectors** | Long copied prefixes and deliberate isomorphs could demonstrate a state machine rather than encode repeated prose. | Search whether branch continuations isolate algebraic properties as a designed conformance suite; predict a missing operation result. |
| **Header-selected checksum kernels** | Three headers are additive checks; the other six may select different small checksum rules through their digits or grid roles. | Freeze a tiny family of positional weights from the three checks and predict all six non-check residues with multiplicity correction. |
| **Raw-direction routing over the 3×3 grid** | `BEXIT` and the exact north/east/south exits show that eye directions can act as spatial instructions. | Route body trigrams without numeric conversion and test coverage/exit signatures against marker- and row-preserving shuffles. |
| **World-coordinate or biome selector** | Noita's intended Cessation route supplies a separate in-world sequence; Eye locations may similarly select operations or source positions. | Inventory only developer-authored coordinates/state cycles and seek an exact 9-, 26-, 83-, or 101-object correspondence with held-out prediction. |
| **Later construction diagram** | Gate may deliberately restate operations devised earlier even though it shipped later. | Accept only masks/rules frozen from the asset that predict one unresolved Eye or Gate quantity. |
| **Sieve/exact-cover payload** | Eyes, cauldron, materials, and Gate vocabulary all support selection rather than substitution. | Treat values as subset indices or incidence records and test exact-cover conservation laws across prefix siblings. |
| **Image, path, or executable bytecode** | The answer need not be prose; 83 labels can be opcodes, pixels, or coordinates. | Infer typed records from transition contexts and render only formats whose dimensions are independently supplied by the game. |
| **Deliberately planted equality skeleton** | Developers could have inserted the isomorphs as verification landmarks while using a different surrounding cipher. | Remove every constrained repeat window and compare the residual corpus to candidate cipher families; the model must explain both layers. |
| **Mixed layers by prefix family** | The exact trie could select different codecs or keys after a common bootstrap. | Fit family labels only at documented branch depths and require the common prefix to initialize the later family-specific state. |
| **Physical/manual construction artifact** | The output may reflect cards, paper strips, spreadsheet sorts, or a hand-built source tree rather than a named cipher. | Search for invariants of construction workflow—stable sorts, copied cells, off-by-one boundaries, and checksums—before named-cipher catalogs. |

## Breadth-first scoring

Use five 0–2 scores before deepening a family:

1. **Coverage:** explains independent hard structures, not just one anomaly.
2. **Selector:** has a game/source fact choosing it before seeing the output.
3. **Capacity control:** cannot fit arbitrary plaintext or keys by design.
4. **Cheap falsifiability:** has a bounded key-free or held-out test.
5. **Chronology:** construction inputs could exist when needed; decoding clues
   may be later.

Preliminary scores are deliberately coarse:

| Family | Coverage | Selector | Capacity | Cheap test | Chronology | Total |
|---|---:|---:|---:|---:|---:|---:|
| sampled suffix/LCP rows | 2 | 2 | 1 | 2 | 2 | **9** |
| nominal allocation/cache trace | 2 | 1 | 1 | 2 | 2 | **8** |
| `Z101` visible/null walk | 2 | 1 | 1 | 2 | 2 | **8** |
| 26-column records | 1 | 2 | 2 | 2 | 2 | **9** |
| 3×3 parity/check object | 2 | 2 | 1 | 2 | 2 | **9** |
| three-state control transducer | 2 | 2 | 1 | 1 | 2 | **8** |
| raw-direction 3×3 routing | 1 | 2 | 2 | 2 | 2 | **9** |
| external world selector | 1 | 2 | 2 | 1 | 2 | **8** |

The scores do not select a winner yet.  The first pass should run one cheap
necessity for each top family, record failures, then rescore.  A visually
exciting result may not jump the queue without an independent selector or a
held-out prediction.

## First bounded test: suffix/LCP necessity

The marker-derived trie order is

```text
E1, W1, E2, W2, E4, W4, E5, E3, W3.
```

Its adjacent body LCP depths are

```text
24, 24, 2, 5, 20, 20, 9, 5.
```

The first differing labels impose only these order relations:

```text
80<29<69<2<78
69<2<23
48<49
77<60<33
```

They are acyclic, so an arbitrary 83-label alphabet can sort the bodies in the
marker order.  Exactly `864/9!` panel orders are realizable; these are precisely
the depth-first leaf orders that keep every prefix cluster contiguous.  Thus
the body data alone do not prefer the observed one of those 864 orders.  The
interesting evidence remains that the headers independently choose one.

A scan of the 720 natural trigram orders formed by six eye-position priorities
and one shared permutation of the five direction values finds no order (or
reverse order) that sorts the bodies into the marker-derived order.  Most
decisively, the bodies cannot literally be all rows of one BWT rotation matrix:
all nine body rows start with the same symbol after their markers, whereas a
full LF row shift would require those starts to equal the nine distinct
preceding marker symbols.  The direct version is rejected.  The weaker
interpretation—headers diagram suffix/LCP machinery for sampled contexts—stays
open but must predict more than trie contiguity before promotion.

## Second bounded test: 3×3 conformance suite

Reading the already established marker pair as `middle -> first-1`, the first
six panels in canonical order are

```text
E1  0->1    W1  1->2    E2  2->0
W2  0->2    E3  2->1    W3  1->0
```

The first row is one directed three-cycle and the second row is its opposite;
together they use every non-self edge on three states exactly once.  The three
natural body rows independently share prefixes of lengths `24,5,20`, and their
checksum-zero representatives occupy the main diagonal.  This is a better fit
to a designed conformance/test matrix than to a low-rank parity matrix.

There is an even sharper equivalent statement.  Name a component order by
`(source,target,remaining)`.  The six edges then enumerate all of `S3` exactly
once: the first row contains the three even/cyclic eye orders and the second
contains the three odd/reflected eye orders.  This exact header structure was
not found elsewhere in the local log and is retained as a new construction
clue.

Conditioning on the observed nine-edge multiset, there are 90,720 distinct
assignments to the fixed panel positions.  In 108, or `1/840`, the first two
rows are opposite directed cycles.  This is not a discovery p-value: the edge
projection, row partition, and target property were inspected after the
marker/trie work.

Two simple decoder versions fail.  The mod-101 matrix has determinant `87`, so
it is full rank rather than a rank-one or rank-two parity table.  Exhausting
all affine maps over `F3` from `(first-1,middle,third mod 3,1)` to grid row and
column finds zero maps that recover the nine fixed cells.  The headers are not
a hidden affine coordinate table.  The conformance-suite interpretation stays
open only if it predicts a body relation or a missing operation; topology
alone is insufficient.

The most literal use of the new `S3` clue also fails.  Reordering every body
trigram by its header's `(source,target,remaining)` permutation, in both action
directions and both completions of the lone self-edge, expands the alphabet
from 83 to 117 labels, creates 176–192 values above 82, and destroys all three
row-prefixes at the first symbol.  It also removes two of the three mod-101
diagonal closures.  Therefore the headers do not simply tell us how to
unscramble each panel's eye components independently.  A surviving use would
have to combine the six permutations globally—as a sieve, parity comparison,
or test suite—rather than relabel each message in isolation.

## Lateral cheap probes

Several other literal versions can be bounded without displacing their broader
families:

- None of the 34 complete 26-wide records contains 26 distinct labels.  Their
  unique-count distribution is centered at 21–23; under independent uniform
  no-adjacent-double rows, seeing no all-unique record has probability about
  `0.563`.  This rejects “each row is a 26-letter substitution permutation,”
  not column-wise or typed-record readings.
- Only 105 of 469 body repeat events have an LRU/working-set distance at most
  eight, and the maximum is 66.  A literal eight-entry cache like the proposed
  Gate subdiagram cannot carry the whole corpus.  A nominal allocation trace
  with a larger or typed store remains possible.
- Exhausting every affine step rule `a*value+b` on cumulative states modulo 101
  (nonzero `a`) gives a best total of 582 distinct per-message states, with
  60–76 in each body.  The exact checksum modulus does not by itself produce a
  low-state additive walk.
- The repeated marker control edges do not have fixed mod-101 body weights:
  edge `0->2` occurs with full residues `53` and `88`, while `1->0` occurs with
  `1` and `0`.  A direct weighted-edge interpretation of the message sums is
  rejected.

After these probes, the strongest genuinely new retained fact is the global
`S3` enumeration in the first six headers.  Its next admissible test must use
all six operations symmetrically or predict one of the three repeated/selected
operations in the last row; another independently fitted per-panel transform
would not count.

## Third bounded test: an exact body echo of the marker BWT

The S3 structure produces one unexpectedly exact cross-layer identity.  The
last even/cyclic panel is East 2 and the first odd/reflected panel is West 2,
the canonical boundary between the two complete S3 rows.  Use the East 2
header order `(2,0,1)` on the universal two-symbol body root, reversing that
root as in a backwards/BWT reconstruction.  Then append the first West 2
symbol after its row's five-symbol common prefix, transformed by West 2's
header order `(0,2,1)`:

```text
East 2 body[1]  010 --(2,0,1)--> 001   1   !
East 2 body[0]  231 --(2,0,1)--> 123  38   F
West 2 body[5]  234 --(0,2,1)--> 243  73   i
```

The resulting nine digits are exactly `001123243`, and the values are exactly
`1,38,73 = !Fi`: not merely the same letters, but the complete digit string
independently restored from the marker BWT.  Exhausting the 3×3 family obtained
by choosing any of the three even-row header orders and any of the three
odd-row exits gives nine distinct triples; this exact triple occurs once, at
the observed canonical boundary.

This is the strongest new synthesis lead, but it is not yet a decryption or a
valid p-value.  The target `!Fi` was known before the construction was noticed;
reversing the root, choosing the odd-row exit rather than its divergence at
the universal root, and defining the 3×3 comparison family are inspected
choices.  Promotion requires a held-out consequence: the frozen
root/frame/exit rule must predict a second marker/body quantity, or a later
in-game asset must independently specify the same S3 boundary operation.

## Fourth bounded test: do the S3 headers name the body transforms?

The final header row naturally supplies the identity and the two adjacent
transpositions of three components:

```text
E4 = 012 = e
W4 = 021 = (12)
E5 = 102 = (01)
```

This gives a genuinely predictive interpretation.  Call the strong observed
East 4→East 5 context map `A` and the East 4→West 4 map `B`.  If the headers
name those two body permutations, they must satisfy the Coxeter presentation
of `S3`:

```text
A^2 = e
B^2 = e
ABA = BAB
```

The partial body maps are already sufficient to reject all three necessities.
Of seven observed edges of `A^2`, all seven move their source; of eight
observed edges of `B^2`, all eight move their source.  The two braid words are
both known at source 31 but force different targets:

```text
ABA(31) = 41
BAB(31) = 69
```

No completion of the unobserved map entries can repair those conflicts.  The
clean header `S3` organization therefore does **not** directly label the two
strong last-family body-context transforms.  This is a held-out failure and
prevents the attractive header pattern from being promoted into a decoder.
The header structure and retrospective `!Fi` echo remain construction clues;
any surviving use must be a global sieve/check/test organization rather than
the literal action of those permutations on the body alphabet.

## Fifth bounded test: five-direction S3 transducer

A different use of the same group avoids assigning one header permutation to
an entire body.  Map the five raw eye directions injectively to five of the six
elements of `S3`, choose one of the six fixed eye orders within every trigram,
and compose the complete body.  The resulting permutation should send the
header's encoded source state to its encoded target state.  This has only
`6P5 * 6 = 4,320` models and uses no plaintext or language score.

One model uniquely fits eight of the nine header edges.  It reads each trigram
in eye order `(2,1,0)` and maps directions `0..4` to

```text
120, 210, 012, 201, 021
```

respectively—all of `S3` except `102`.  It predicts every non-self edge and
misses only East 4, the lone self-edge.  That looks sharp within the uncalibrated
model table: the complete best-match histogram is

```text
matches  models
0        112
1        460
2       1035
3       1211
4        878
5        430
6        161
7         32
8          1
```

An exact conditional null shows why this is not evidence.  Reassign the nine
intact observed bodies to the fixed nine headers in all `9!` ways, preserving
every body's order, counts, prefixes, and internal dependencies, and optimize
the same frozen 4,320-model family.  Of 362,880 assignments, 282,468 admit an
eight-edge best fit and 74,436 admit all nine; only 5,976 fall below eight.
Thus `98.353%` reach at least eight and `20.512%` reach nine.  The observed
eight-edge result is ordinary and weaker than many shuffled associations.
This rejects the low-capacity five-direction `S3` product as a predictive
header/body coupling despite its unique in-sample near-fit.

## Sixth bounded test: sieve the copied prefixes once

The pre-registered trie-edge family produces the first positive held-out result
of the breadth pass.  Remove the nine established markers, merge the exact
copied body prefixes into one prefix trie, and count each distinct labeled edge
once.  Depth-first versus breadth-first traversal and sibling order cannot
change the multiset.  It contains 918 edges whose values sum to

```text
37774 = 374 * 101
```

so the complete deduplicated body trie closes exactly modulo 101.  This is a
fourth natural zero-check object, structurally different from the three
individual diagonal messages.

Several controls localize the result:

- keeping the markers (`start=0`) gives residue 63; starting at body offsets 2
  and 3 gives 35 and 30;
- merging reversed bodies as a suffix trie performs no useful deduplication
  and gives residue 92;
- building the trie over the raw direction digits after their three-digit
  markers gives residue 23, so the closure needs the accepted trigram symbols;
- the three natural row-family tries give residues 55, 90, and 3 rather than
  zero; the complete nine-leaf object matters;
- removing any one panel breaks the closure;
- among every possible common start offset, offset 41 also happens to close.
  That second post-hoc hit is expected-scale noise and prevents a claim that
  offset 1 is numerically unique; offset 1 is selected independently because
  it is exactly the marker/body boundary.

The label-multiplicity vector supplies useful calibration.  Among all 6,806
affine permutations of the visible `0..82` alphabet, 71 (`1.043%`) retain a
zero trie sum; identity is the only one of the 83 additive translations.
A seeded sample of 200,000 arbitrary global label permutations—which preserves
the complete equality skeleton and trie topology—closes 1,895 times
(`0.9475%`).  Finally, over `F101` the nine complete message count vectors have
rank 9, and adding the trie-edge count vector raises it to 10.  Therefore the
new equation is not a formal linear consequence of any combination of the
nine known message sums.

An exact conditional calibration removes the main weakness of those simple
relabeling controls.  Group visible labels by their complete occurrence-count
triple in East 1, East 3, and East 5.  Permuting labels within a group preserves
all three diagonal complete-message sums **exactly**, not just modulo 101, and
also preserves the entire equality trie.  Convolving every within-group
permutation gives the full subgroup rather than a Monte Carlo estimate:

```text
constraint                                  zero / total                         rate
three diagonal sums preserved exactly       1,307,844,501,760 / 132,090,377,011,200   0.990113%
same, with all nine marker labels frozen        8,174,134,656 /     825,564,856,320   0.990126%
```

Thus the existing zero checks do not make the trie closure common in this huge
exact conditional subgroup; it behaves almost precisely like one additional
uniform equation modulo 101.  This still samples a structured subgroup rather
than every permutation satisfying the checks, but it is a much better matched
control than unconditional relabeling.

The calibration is not a pristine discovery p-value: the modulus and corpus
were already known to be checksum-rich, and the exact conditional universe is
a structured subgroup chosen after the result.  Still, unlike the
retrospective body `!Fi` echo, the exact statistic was named in the mechanism
map before it was evaluated, the body boundary is independently fixed, the
result is invariant under every traversal choice, and the diagonal checks are
now explicitly conditioned.  This promotes
**prefix-trie edge sieving plus mod-101 closure** to the strongest novel
mechanical lead.  The next work must seek a second prediction: a developer
asset selecting the same merge-once rule, or a non-fitted recursive checksum
law at internal trie branches.

The first recursive inventory gives descendant-edge residues at the five
documented branching nodes:

```text
all nine after depth 2       30
upper three after depth 24   19
lower six after depth 5      70
nested four after depth 9    89
last three after depth 20    13
```

The lower-six node is the unique 70.  This equals the already reproduced main-
diagonal mirror-difference total in the mod-101 message grid, but both numbers
come from the Eye corpus and the target 70 was known before this inventory.
It is therefore a retrospective internal echo, not independent Gate evidence.
In particular, the claimed **70-pixel Seula residual remains unreproduced**:
simple raw-sprite masks give 0, 4, 109, 302, 411, or 480, and the dossier did
not define the extra mask needed to obtain 70.  A future asset-derived selector
would still be valuable; the present branch value does not supply one.

There is one genuine asset-selected number worth a stronger test.  Veska's
upper and lower pictograms objectively contain 9 and 8 authored pixels even
though the dossier's surrounding `12|43` partition fails.  The trie happens to
factor twice by their sum 17:

```text
918   = 54 * 17
37774 = 22 * 17 * 101 = 22 * 1717
```

Within the exact diagonal-check-preserving relabeling subgroup, joint
divisibility by `17*101` occurs in
`125,161,099,264 / 132,090,377,011,200 = 0.094754%`; freezing every marker
label gives `830,894,368 / 825,564,856,320 = 0.100646%`.  These exploratory
rates are stronger than the mod-101 equation alone, but 17 was tested after
inspecting the factorization and the topology's edge count is fixed in this
null.  They are not discovery probabilities.

The obvious 17-role mechanism fails.  Partition each of the canonical,
East-5-first trail, marker-trie, and marker-LF serializations into either 17
consecutive 54-edge records or 17 cyclic lanes, under both DFS and BFS.  None
of the 136 resulting records has the expected sum 2,222; no consecutive record
closes modulo 101.  One marker-LF/DFS cyclic lane closes, which is ordinary at
this search size.  Thus Gate's objective `9|8=17` remains a possible later
grouping hint, but it does not currently supply the grouping or a decoder.

## Seventh bounded test: 18 structural null states

The trie and modulus support a more coherent, if deliberately adventurous,
architecture.  The visible alphabet is `0..82`, so `Z101` contains exactly 18
missing labels, `83..100`, with sum

```text
83 + ... + 100 = 1647 = 16*101 + 31.
```

The compressed nine-leaf body trie has five branching nodes and thirteen
outgoing compressed branch edges—exactly 18 typed structural records.  This
also gives a literal possible parsing of the already recovered breadth-first
depth string `BEXIT`: branch nodes plus exits.  Most sharply, the lower-six
descendant trie has residue 70, so adding every missing label once closes:

```text
lower-six distinct descendants  70
missing labels 83..100           31
                                  --
                                 101 = 0 mod 101
```

This predicts a joint event rather than renaming the full-trie zero.  In the
exact diagonal-check-preserving subgroup with all nine markers fixed,

```text
full trie = 0 and lower-six descendants = 70
80,918,060 / 825,564,856,320 = 0.0098015%
```

Without marker freezing the rate is
`12,948,675,076 / 132,090,377,011,200 = 0.0098029%`.  Conditional on the full
trie already closing, the lower event remains almost exactly `1/101`.  Four
proper internal branch nodes were eligible for the post-hoc complement search;
summing their exact joint counts gives a conservative union bound of `0.03922%`
with markers fixed.  The root descendant vector is algebraically tied to the
full trie and cannot produce this target under the same condition.

This is not a discovery p-value.  The missing-state interpretation, the
node-plus-edge record count, and the branch complement were noticed after the
trie closure, and `BEXIT` has several possible readings.  More importantly,
the hypothesis supplies only the **set** of structural labels `83..100`; it has
no canonical bijection assigning those labels to the five nodes and thirteen
exits.  It is promoted as the strongest novel architecture, not a decoder.
Its next falsification target is precise: an in-game asset or a key-free body
relation must order or type those 18 records without reference to desired
plaintext.

## Eighth bounded audit: the wand generator partitions 83 and 18

A newly surfaced raw-code identity meets half of that promotion target. The
installed procedural-wand generator draws an inclusive integer in `0..100`
and executes:

```text
0..82   -> ACTION_TYPE_MODIFIER
83..100 -> ACTION_TYPE_DRAW_MANY
```

This is an exact 83+18 partition of a 101-state space. It is not merely a
comment calling something “83%.” A complete WAK inventory finds 74 direct
`Random(0,100)` comparisons across 22 operator/threshold pairs; `<83` occurs
only in the two duplicated procedural-wand sources. The public data history
independently timestamps the code to 9 February 2021. That is too late to prove
construction use but fully eligible as a decoder clue.

The type assignment aligns with the structural interpretation. The five
compressed Eye branch nodes have fan-outs `(2,3,3,2,3)`, totaling thirteen
continuations. A serialized draw-many execution tree therefore contains

```text
5 branch instructions + 13 drawn continuations = 18 structural records.
```

Current draw-many cards include arities two and three, though also larger and
variable arities, so the fan-outs are legal but not uniquely selected. The
same generator contains the previously noted 26-slot deck clamp and a
capacity-9 unshuffle condition, matching the complete Eye row width and panel
count. Because this four-number convergence was assembled retrospectively and
each value has an ordinary balance/UI explanation, it is not assigned a
probability.

The runtime semantics is genuinely tree-shaped: `draw_actions(n)` draws and
executes each child immediately, and a child action may recurse into another
`draw_actions` call. The Eye degrees produce exactly nine leaves via
`1+sum(d-1)`. All five Eye branch depths lie inside the first 26-symbol row;
in East-5-first breadth order they remain the independently recovered
`BEXIT`. The literal card trace is nevertheless too small—26 deck slots cannot
account for 918 merged payload edges—so a viable construction must separate
control topology from encrypted payload or use repeated casts.

This audit initially appeared to promote the 83-visible/18-structural machine
from a purely internal numerical architecture to one with independent
game-authored typing evidence. It still lacked the essential bijection from
`83..100` to branch records. The
actual Lua uses the roll to choose an action type and then chooses a card
separately; it does not emit the roll as a label. A literal decoder must now
predict the branch arities or restore a full execution tree under source-
derived rules, without enumerating 18! labelings. Details and reproduction are
in `docs/procedural-wand-architecture.md` and
`scripts/analyze_wand_selector.py`.

## Ninth bounded audit: execution and checksum scopes do not match

Grounding the analogy in actual recursive execution reverses the promotion.
A rooted tree with five internal nodes of degrees `(2,3,3,2,3)` has nine leaves
and fourteen action/card nodes. Its thirteen edges are relationships between
those nodes. The `5+13=18` construction counts internal nodes and edges as
separate record types; Noita's gun runtime does not emit that representation.

The checksum complement has a second, independent locality failure:

```text
scope       descendant residue   hypothetical node+edge records
all nine             30                         18
upper three          19                          4
lower six            70                         11
nested four          89                          7
last three           13                          4
```

Thus `70+31=101` attaches all 18 missing values to a subtree owning only 11
proposed records. The scope owning all 18 has residue 30 and does not close.
Exactly five of the 31,824 unordered 11-label subsets of `83..100` sum to 31
modulo 101, but no source-derived rule chooses one; testing them for language
would fit the target after inspection.

This rejects the current local recursive-checksum/wand decoder. The exact
`Random(0,100)<83` identity remains a legitimate later-clue candidate, but it
must now earn relevance through a new prediction or an authored node/edge
serialization. It cannot inherit significance from the failed 18-record
mapping.

## Tenth bounded audit: two more structural summaries are ordinary

Two key-free ideas from the wide map were tested before returning to a deeper
cipher family.

First, reading each trigram literally as three base-five eye states gives an
adjacent Hamming-distance profile of `115,425,478` for distances one, two, and
three. The apparent shortage of three-eye changes is not special once the
restricted `0..82` label geometry and copied transition skeleton are respected.
Among 5,000 global label relabelings, `3,713/5,001 = 0.742451` are at least as
far from the full-grid reference profile.

Second, the first edge that makes each prefix-tree leaf unique produces the
natural grid

```text
80 29 69
69 78 23
77 60 33
```

The lower two rows both sum to 170. In the exact subgroup preserving the three
diagonal checks, every marker, and the complete trie, row-sum equality occurs
in exactly `30,576,476,160 / 825,564,856,320 = 1/27` assignments. Since the
equality and extraction were inspected after seeing the tree, it is not a
selective held-out prediction. Both observations are retained for completeness
and dropped as active decoder leads.
