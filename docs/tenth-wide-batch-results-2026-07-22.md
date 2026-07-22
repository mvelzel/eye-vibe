# Tenth wide horizon, first batch — results, 22 July 2026

## Outcome

None of the six cheap screens supplies a decoder or earns depth.

One result initially crossed its frozen promotion line: mod-101 differences
between sibling trie branches had a four-variant corrected tail of
`4/1001 = 0.003996`. Its independently frozen validation on the seven
nonliteral context maps is ordinary, tail `874/2001 = 0.436782`. The branch
effect is therefore retained only as an isolated one-support-slot anomaly.

The other five lanes close directly or under their matched controls. This
leaves the ten unexecuted lanes in the wide horizon intact; it does not make
one of them true by elimination.

## F. Ordinal-pattern echoes

### Method

Strip every copied body prefix through each leaf's unique trie exit. For
sliding lengths 3–8, convert windows to tie-aware ordinal patterns under:

- all six lexicographic orders of the three base-five eye components;
- all six ordered projections onto a pair of eyes.

Count matching patterns belonging to different panels. Controls globally
relabel the 83 body symbols while preserving the complete equality structure,
all nine markers, and the three diagonal message sums. All 72 variants are
reselected inside every control by leave-one-control-out empirical rank.

### Result

The selected all-panel variant is length 7 under full component order
`(middle, low, high)`, with 61 cross-panel collisions. Its individual tail is
`0.021978`; the correctly reselected family tail is `0.594406`.

Training only on East 1, West 1, and East 2 selects length 6 under
`(middle, high, low)`, training tail `0.047952`. The fixed variant gives 32
collisions in East 4, West 4, and East 5, held-out tail `0.349650`.

An earlier z-score diagnostic selected an outer-eye length-8 pattern, but that
choice was unstable because several discrete control distributions had nearly
zero variance. Empirical rank selection removes the artifact.

**Disposition:** reject simple ordinal-pattern recurrence in the frozen
full/pair projections. This also supplies no independent validation for the
first/third-eye transition residue.

## G. Riffle/Gilbreath rising sequences

For each of the seven nonliteral partial context maps, sort observed sources
under all six base-five component orders and both directions, then count
increasing runs in the corresponding targets. One global convention minimizes
the sum. Controls shuffle every fixed image over its exact domain while
retaining injectivity and fixed-point count.

```text
all contexts       58 rising sequences / 117 edges
convention         (low, high, middle), forward
control range      51..65
lower tail         0.550450

first four train   20 / 45
last three test    40 / 72
held-out range     30..45
held-out tail      0.899101
```

**Disposition:** reject low rising-sequence complexity under any authored
base-five lexicographic order. This does not reject a riffle under an unknown
83-card order, which would require an external selector or a capacity-charged
learned-order test.

## H. 84-card Faro sentinel

The exact algebra is real but closes the pure proposal rather than opening a
new group:

```text
84-card out-Faro: position x -> 2*x mod 83 for every x=0..82
sentinel position: 83 -> 83
multiplicative order of 2 mod 83: 82
```

Thus the 83 non-sentinel positions form the complete nonzero orbit plus fixed
zero under multiplication by two. Adding cuts of the visible 83 positions
generates affine maps `x -> a*x+b` over `F83`, precisely a group family already
excluded by the strong Eye context certificate.

An 84-card in-Faro moves position 83 to 82. It does not preserve a hidden
sentinel, so a duplicate-label, skip, or output rule must be supplied before a
mixed in/out-Faro model is defined.

**Disposition:** reject pure out-Faro plus visible cuts as a new Eye family.
Retain mixed Faro only as selector-gated; do not invent the sentinel rule from
the ciphertext.

## J. Graph cover / bisimulation quotient

Directed color refinement starts with all 83 labels in one class and refines
by incoming and outgoing neighbor-color multiplicities on the deduplicated
843-edge transition support.

```text
stable classes       83/83
singleton classes    83
largest class         1
iterations            2
degree/no-loop null  83..83 classes
lower tail            1.000000
```

With any one of the nine panels withheld, the remaining graph still refines
to 83 singleton classes.

**Disposition:** there is no nontrivial untyped equitable quotient or simple
graph cover. A typed-edge cover remains a different hypothesis, but its edge
types must come from outside this fit.

## K. Differential branch trails

### First screen

Each pair of panels belongs to exactly one least-common-ancestor branch of the
copied-prefix trie. At aligned coordinates after that branch, count repeated
differences separately for four frozen representations. Positional controls
freeze every prefix through its leaf exit and shuffle only suffixes, thereby
preserving every message length, multiset, and integer sum.

| representation | repeated mass / 3,611 | summed support | individual tail |
|---|---:|---:|---:|
| mod 83 | 3,217 | 394 | 0.001998 |
| mod 101 | 3,142 | 469 | 0.000999 |
| outer-eye pair mod 5 | 3,487 | 124 | 0.018981 |
| middle eye mod 5 | 3,586 | 25 | 1.000000 |

The tie-safe reselected family chooses mod 101 and gives corrected tail
`4/1001 = 0.003996`. The 1,000 mod-101 controls span repeated mass
`3116..3141`, equivalently summed support `470..495`; the observation is one
support slot beyond that range.

### Frozen independent validation

The validation fixes `delta=(target-source) mod 101` and moves to the seven
nonliteral context maps. It counts support separately in each map and uses
2,000 domain/image/injectivity/fixed-point-matched shuffles.

```text
map supports          11,13,13,6,22,21,20
edges                 117
summed support        106
repeated mass          11
control range        2..21
upper tail           874/2001 = 0.43678161
```

**Disposition:** validation fails. Retain the branch deficit as an isolated
screening anomaly and, as pre-registered, do not inspect missing residues for
semantic `70`, `31`, `42`, Gate, or checksum stories.

## L. Context-map holonomy

Treating a composition residual as holonomy first requires independently
observed context windows to form a semantic loop. Their endpoint graph has:

```text
vertices     11
edges         7
components    4
cycle rank    0
```

It is a forest. Arbitrarily composing maps through coincident ciphertext
labels does not create an observed context loop; it reduces to the previously
negative partial-group word closure.

**Disposition:** reject semantic context holonomy with the present windows.
A future new context could create a real cycle, at which point the test may be
reopened without changing its definition.

## Reproduction

```bash
PYTHONPATH=src python scripts/run_tenth_wide_batch.py --controls 1000
PYTHONPATH=src python scripts/run_tenth_differential_validation.py --controls 2000
PYTHONPATH=src python -m unittest tests.test_tenth_wide
```

Definitions are in `src/eye_mystery/tenth_wide.py`. The validation definition
was committed before its result in
`docs/tenth-differential-validation-freeze-2026-07-22.md`.
