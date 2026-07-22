# Ninth wide pass: causal and quotient attacks — 22 July 2026

## Why change the question

Eight breadth passes have tested many ways to *read* the accepted labels:
finite fields, checksums, codebooks, transpositions, BWT/MTF, pointer tapes,
grammars, packets, image paths, and several game-authored selectors.  None
produced a decoder.  The next pass therefore asks a different question:

> What low-capacity mechanism could have *caused the observed equality,
> divergence, reconvergence, and no-double structure*?

This is wider than choosing another numerical transform.  The primary objects
are now equivalence relations, partial context maps, branch interventions,
transition support, and synchronization—not printable labels.

Claims of novelty below are modest.  “Project-original” means the exact test
was not found in the reviewed wiki, local research record, or read-only Discord
history; it cannot prove that nobody has privately considered it.

## Frozen facts

- The accepted read gives nine paths and 1,036 labels in `0..82`, with no
  adjacent doubles.
- Exact copied prefixes and six strong isomorphic windows exist, but context
  maps have chaining conflicts inconsistent with cyclic/GCTAK models.
- The merged body-prefix trie has five proper branch nodes and thirteen exits.
- The nine first trigrams are structured six-symbol factoradic headers with a
  reproducible three-way type classifier, but no direct body consumer.
- Arbitrary `A83`/`S83` GAK and XGAK remain structurally possible and vastly
  underdetermined.
- Recent read-only discussion supplies three concrete community leads:
  1. XGAK plaintext letters may share only three or four permutations, with
     the trailer altar proposed as a category selector;
  2. moving the first `N` cards to the back, where `N` is plaintext alphabet
     size, is a possible no-double scaffold for shared permutations;
  3. in ordinary GAK, plaintext permutations may lie a small distance from one
     shared base permutation.
- Those three ideas are hypotheses, not established properties of the Eyes.
  The proposed trailer categories are normal glyphs, nonstandard glyphs, and
  glyphs on the reverse side; the discussion also mentions the keyed phrase
  `A BAD MAGIC CARD TRICK`.

## Wide portfolio before depth

| Lane | Causal interpretation | First bounded test | Prior-work boundary |
|---|---|---|---|
| **A. Trailer-category XGAK quotient** | Plaintext symbols use only three or four distinct permutations and differ mainly by output position. | Freeze the proposed altar categories, derive every category pattern implied by source-backed cribs and documented stutter/funny-obstacle alternatives, and test whether one global partition satisfies all backbone constraints. | Earlier XGAK work allowed one arbitrary operation per plaintext symbol; no exact category partition has been tested. |
| **B. First-`N` cut scaffold** | Every step removes the output-eligible first `N` cards from immediate reuse, explaining no doubles while category shuffles act on the remainder. | For `N` in the independently motivated plaintext sizes 26, 27, 36, and 42, enumerate only cut direction, output timing, reversal, and one fixed within-packet interleave. Reject models that cannot reproduce a planted XGAK fixture before touching the Eyes. | This is the concrete 22 July Discord suggestion, not generic move-to-front/back already tested. |
| **C. Common-base permutation locality** | Plaintext operations are one base permutation plus a small number of swaps, explaining similar but conflicting context maps. | Given all strong partial context maps, solve the minimum common Cayley-radius completion: one base permutation and per-operation transposition budgets. Compare the optimum with size- and domain-matched randomized partial maps. | Previous deck scans picked named shuffles; they did not complete several observed partial maps jointly around a learned common base. |
| **D. Deck-chaining quotient** | Reconvergences reveal equivalence classes of hidden deck states or plaintext operations without recovering absolute card labels. | Define a label-invariant quotient rule and require it to reduce a planted solvable GCTAK fixture, then a planted small GAK fixture, before applying it to Eye contexts. | Graph chaining is established for GCTAK; its extension to GAK remains an informal community target. |
| **E. Branch-intervention influence matrix** | The copied prefix tree is a designed set of interventions: a divergence changes only a bounded downstream region before state reconvergence. | At every documented branch, mark which later equality relations with other panels are broken or restored. Test whether the branch-by-relation matrix is triangular, nested, or low Boolean rank against prefix-tree-preserving branch-label controls. | Trie sums and grammar tests measured payload reuse, not the *causal footprint* of each divergence. Project-original exact test. |
| **F. Synchronization/observability spectrum** | Different hidden states become observationally indistinguishable after a short category/action word. | From every aligned isomorph pair, compute the earliest length at which its partial context map becomes forced, conflicts, or reconverges. Compare the spectrum with planted CTAK, small GAK, grouped-XGAK, and equality-matched null paths. | Existing work counted hidden-state lower bounds and conflicts but not a calibrated resynchronization-time spectrum. Project-original test. |
| **G. Equality-skeleton automorphisms** | Headers label symmetries of the nine path/trie structure rather than operations on numeric body values. | Build the unlabeled path-union structure with message, row, and branch incidence colors; enumerate its automorphism group. Test whether factoradic header permutations act on any natural orbit without fitted relabeling. | Factoradic lanes acted on labels, positions, or S6 features. None asked whether headers describe automorphisms of the equality skeleton itself. Project-original test. |
| **H. Forbidden-transition rectangle cover** | No doubles and XGAK output categories arise from a few forbidden source/destination blocks rather than 83 unrelated exclusions. | Deduplicate copied transitions, form the 83×83 observed-support matrix, and measure the minimum category-respecting Boolean rectangle cover of structurally absent transitions. Calibrate with degree- and no-loop-preserving directed graph controls. | Earlier transition tests used counts, Hamming changes, or affine maps; none tested low-rank *absence* structure. Project-original test. |
| **I. Latent isomorph-template edit channel** | Several messages are edited versions of one plaintext/category template; cipher-state changes turn literal repeats into nearby isomorphs. | Replace each window by its first-occurrence/equality signature, then perform a three-way edit alignment with costs frozen from planted GAK/XGAK simulations. Require one template to predict held-out branch alignments. | Direct message alignments and RePair use literal labels. This aligns relational signatures and admits insertions/deletions. Project-original test. |
| **J. Typed opcode/operand records** | The bodies are an executable or construction trace with alternating role classes, not prose. | Infer the smallest held-out-predictive stochastic block model on predecessor/successor contexts after copied-prefix deduplication. Require stable role classes across panels and a block grammar that predicts withheld edges. | Entropy, packets, and cache roles were fixed readouts; no context-only type inference with held-out prediction has been run. Project-original test. |
| **K. Base-five carry automaton** | Three eye digits are a display for ordinary radix-five arithmetic with carry/borrow state, not affine `F5^3` geometry. | For adjacent canonical labels, serialize the two carry bits from addition/subtraction under all six global digit orders and two directions; test transition compression and branch synchronization under global-label controls. | Literal `F5^3` affine maps discard carries, while change masks discard arithmetic direction. Project-original representation, selector-weak. |
| **L. Header-class conditional dynamics** | The three factoradic header types select different generators, reset conventions, or record roles. | Deduplicate copied transitions, fit one permutation-invariant transition feature model with and without the frozen three header classes, and require leave-one-panel-out predictive gain. | Header cosets and direct transforms were negative; conditional predictive dynamics have not been tested. |
| **M. Placement-state selector** | The native spawn algorithm's world/parallel/biome state supplies message-specific parameters, analogous to Cessation's in-world cycle. | Reconstruct the exact native placement inputs and outputs for all nine message types; test only values used before body selection or rendering. Require an exact 9/83/101 correspondence before proposing a decoder. | Lua inventories found no consumer and generic RNG fitting is banned; this is a native provenance audit, not an RNG search. |
| **N. Worldline rather than reset messages** | The nine panels are checkpoints of one hidden process viewed at different parallel-world depths. | Order panels only by authored East/West trigger chronology and test whether prefixes are compatible with state snapshots, suffix overlap, or conjugate resets under label-invariant constraints. | Earlier one-stream tests concatenated marker orders and scored compression; they did not model panels as observations of a common evolving state. |

## Controls and capacity limits

- Tests on equality alone use prefix-tree-preserving positional controls.  A
  null must keep every feature that directly determines the statistic.
- Transition-support tests use directed degree- and no-loop-preserving edge
  swaps after copied occurrences are deduplicated.
- Numeric/base-five tests use global body-label permutations with headers
  frozen, and reselect every stated global convention inside each control.
- GAK/XGAK causal statistics first need planted controls whose true operation
  categories, permutation radius, or synchronization times are known.
- A learned partition, block model, or common base must be global.  Per-panel
  categories or keys are prohibited.
- Promotion requires either an exact necessity or a corrected matched tail
  below `0.01`, followed by a held-out panel, branch, or independently authored
  prediction.  A low-dimensional fit without prediction does not promote.

## Breadth-first ranking

Scores are 0–2 for coverage, independent selector, capacity control, cheap
falsifiability, and chronology.

| Lane | Coverage | Selector | Capacity | Cheap | Chronology | Total |
|---|---:|---:|---:|---:|---:|---:|
| A. trailer categories | 2 | 2 | 1 | 1 | 2 | **8** |
| B. first-`N` cut | 1 | 1 | 2 | 1 | 2 | **7** |
| C. common-base locality | 2 | 1 | 2 | 2 | 2 | **9** |
| D. deck-chaining quotient | 2 | 0 | 2 | 1 | 2 | **7** |
| E. branch influence | 2 | 2 | 2 | 2 | 2 | **10** |
| F. synchronization spectrum | 2 | 1 | 2 | 2 | 2 | **9** |
| G. skeleton automorphisms | 2 | 2 | 2 | 2 | 2 | **10** |
| H. forbidden rectangles | 1 | 1 | 2 | 2 | 2 | **8** |
| I. relational edit template | 2 | 1 | 1 | 1 | 2 | **7** |
| J. typed records | 1 | 0 | 1 | 2 | 2 | **6** |
| K. carry automaton | 1 | 0 | 2 | 2 | 2 | **7** |
| L. header-conditional dynamics | 2 | 2 | 2 | 2 | 2 | **10** |
| M. placement selector | 1 | 2 | 2 | 1 | 2 | **8** |
| N. worldline snapshots | 1 | 2 | 1 | 1 | 2 | **7** |

## First batch before any deep branch

The first cheap batch is **C, E, F, G, H, and L**.  These six are mutually
different: permutation completion, causal branch footprints, synchronization,
graph symmetry, forbidden-support factorization, and header-conditioned
prediction.  All can fail without guessing plaintext.

Lanes A and B remain high-value but selector-gated until the exact proposed
altar category sets and a complete first-`N` shuffle definition are frozen.
Lane D starts with method calibration rather than Eye fitting.  Lanes I–N stay
on the ledger and are not deleted if the first batch closes.

No first-batch statistic will be implemented until this portfolio is committed.

## First-batch result

The six tests are complete and none promotes. The all-context common-base hit
was literal-prefix identity contamination; the seven nonliteral maps give
`36/117` agreements with corrected tail `0.818182`. Branch influence has
maximum `GF(2)` and Boolean rank five and zero nested row pairs. The proposed
synchronization spectrum is exactly determined by the equality signatures
used to select its windows. Both full and equal-length-truncated equality
skeletons have automorphism group order one. The absent-transition matrix has
binary rank 82 and all 83 row patterns. Header classes rank `2/280`, but their
held-out log gain is `-3.408916`, so they make prediction worse.

Definitions, controls, false-positive audit, and reproduction are in
[`ninth-causal-batch-2026-07-22.md`](ninth-causal-batch-2026-07-22.md).

The second wide slice was then frozen before execution. It acquires the exact
proposed trailer categories and places them beside independent radix-five
carry and one-worldline tests. See
[`ninth-second-wide-freeze-2026-07-22.md`](ninth-second-wide-freeze-2026-07-22.md).
