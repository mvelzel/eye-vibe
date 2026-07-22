# Ninth pass, first causal batch — 22 July 2026

## Outcome

None of the first six causal lanes earns a deep search. Two intermediate
numbers looked positive, but both fail their stated promotion rule:

- a learned common permutation fits `108/209` context edges only because the
  input includes six literal copied-prefix maps dominated by `x -> x`;
- the factoradic header grouping ranks `2/280` among all three-triple
  partitions, but its held-out log gain is **negative**. It predicts worse
  than the unconditioned model.

The admissible common-base test is null-typical, and the other four lanes give
exact obstructions or high-complexity structures. This is a useful closure:
the Eye corpus does not hide a cheap decoder in any of these six relational
summaries.

## C. Common-base permutation locality

### Method

For every observed partial context map, count each forced edge `source ->
target`. Learn one global permutation of `0..82` maximizing agreement with all
edges. This is an exact maximum-weight bipartite assignment. It is a generous
lower-bound screen for the harder common-Cayley-radius problem: the base is
unpenalized, and individual context completions are not yet charged.

Each control retains every map's exact domain, image set, edge count, and
injectivity, but shuffles the image over the fixed domain. There are 1,000
controls.

### Result

| Input maps | Agreement | Control range | Corrected upper tail |
|---|---:|---:|---:|
| all 13 | `108/209` | `54..67` | `1/1001` |
| seven nonliteral isomorph maps | `36/117` | `35..42` | `819/1001 = 0.818182` |

The first row is contaminated by the six marker/prefix maps: the best base
gets `89/92` of their edges, almost all literal identity constraints. On the
seven genuinely nonliteral isomorph maps, the learned base is ordinary. Since
the generous lower-bound screen fails, a small shared Cayley neighborhood is
not supported. The broad arbitrary-GAK possibility is not rejected.

## E. Branch-intervention influence

### Method

At each of the five body-prefix branch nodes, form one position tape. A bit is
set when two messages leaving through different immediate child edges later
show the same label at the same coordinate. Within-child equality is assigned
to the deeper branch and excluded. Measure active columns, exact `GF(2)` rank,
exact Boolean rank, and pairwise nesting of the five row supports.

Controls freeze every prefix through each leaf's unique exit label and shuffle
only the remaining per-message suffix. This preserves the complete authored
prefix tree and each suffix multiset.

### Result

```text
branches          5
active columns   54       control 18..47
GF(2) rank        5       control 3..5
Boolean rank      5       control 3..5
nested row pairs  0       control 0..7
```

The footprint has maximum possible linear and Boolean rank and no nested row
pair. The unusually *large* active support is opposite the predeclared
low-footprint direction. It is also explained by the known later isomorphic
windows that the suffix-shuffle control destroys, so it is not independent
evidence for a causal intervention machine. The proposed triangular/nested
mechanism closes.

## F. Synchronization/observability spectrum

### Exact obstruction

For two aligned sequences, an injective partial relabelling exists **if and
only if** their first-occurrence/equality signatures are identical. Repeated
positions merely validate edges already forced by the equality signature.

All thirteen selected contexts therefore have no conflict by construction.
They contain 0–5 validation positions and learn their last new edge near the
end, but these values are functions of the same signatures used to select the
contexts. An equality-matched null has exactly the same profile. Without a
separately specified state machine or category projection, this lane cannot
observe synchronization rather than restate isomorphism. It closes as
non-identifying before planted-model fitting.

## G. Equality-skeleton automorphisms

### Method and result

Enumerate all `9!` message permutations preserving every aligned pairwise
equality-coordinate tape. The exact graph also preserves path length. A second
version truncates every body to the common first 98 coordinates so unique
lengths cannot force the answer.

```text
full path-union group order       1
common-98-coordinate group order 1
```

There is no nontrivial natural message orbit on which the factoradic header
permutations could act. The known West2/West4 ambiguity belongs to the coarse
header-edge graph, not the complete body equality skeleton.

## H. Forbidden-transition rectangles

### Method

Deduplicate all within-body directed transitions, construct the `83 x 83`
absent-edge matrix, and measure its exact binary rank and distinct row
neighborhoods. If `k` Boolean rectangles cover a matrix, its rows can show at
most `2^k` patterns, so `ceil(log2(distinct rows))` is a valid rectangle-cover
lower bound. The binary rank is reported only as a diagnostic, not mislabeled
as a Boolean-rank bound.

Controls use repeated directed double-edge swaps. They preserve the exact
in/out degree sequence, simple support, and the prohibition on self-loops.

### Result

```text
deduplicated present edges  843
absent-matrix GF(2) rank      82       control 80..83; lower tail 0.729271
distinct absent rows          83       every control 83
rectangle-cover lower bound    7       every control 7
```

This rejects a cover by six or fewer arbitrary rectangles. It does not by
itself reject three or four symbol categories, because a block model may use
several source/destination rectangles per category. Nothing about the support
is simpler than its degree-matched controls, so the lane does not promote.

## L. Header-class conditional dynamics

### Method

The frozen classes are P, West-Q, and East-Q. Strip every literal body prefix
through the leaf's unique trie exit. Represent subsequent transitions only by
label-invariant features: target repeat-distance bin, whether the directed
edge appeared earlier in that panel, and whether the source was new when it
was emitted.

For each held-out panel, compare a Dirichlet-smoothed feature model trained on
the other two panels of its header class with a global model trained on the
other eight. Exhaust all 280 unlabeled partitions of nine panels into three
triples.

### Result

At the frozen Jeffreys smoothing `alpha=0.5`:

```text
observed leave-one-out log gain  -3.408916
rank among partitions             2/280
best partition log gain          -2.924332
```

Even the best partition predicts worse than the global model. The apparently
small rank tail `0.007143` compares one bad model with other, still worse
models and cannot satisfy the required positive held-out gain. The rank is
also smoothing-sensitive:

| Boundary | alpha | Log gain | Rank |
|---|---:|---:|---:|
| full body | 0.1 | -3.368 | 5/280 |
| full body | 0.5 | -3.289 | 9/280 |
| leaf exit | 0.1 | -3.351 | 1/280 |
| leaf exit | 0.5 | -3.409 | 2/280 |
| leaf exit | 1.0 | -8.051 | 5/280 |
| leaf exit | 2.0 | -20.066 | 8/280 |

The header classifier remains real metadata, but this transition-feature
consumer is rejected.

## What transfers

1. Literal copied prefixes must be removed before any learned shared-operation
   statistic; otherwise the identity permutation wins automatically.
2. Isomorph windows and partial-bijection consistency are the same equality
   fact. A new synchronization claim needs an observable not fixed by the
   equality signature.
3. A favorable *rank among models* is not predictive evidence when every
   model has negative held-out gain.
4. The branch reconvergences are abundant but not low-rank, triangular, or
   nested. A successful mechanism must create complicated visible equality
   from a simple hidden rule rather than assume the visible footprint itself
   is simple.

## Reproduction

```sh
PYTHONPATH=src python3 -m unittest tests.test_ninth_causal
PYTHONPATH=src python3 scripts/run_ninth_causal_batch.py --controls 1000
```
