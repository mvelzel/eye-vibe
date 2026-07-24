# Fifteenth wide horizon — second batch freeze

## Purpose

The first fifteenth-horizon batch tested four unrelated representations before
deepening any of them. None promoted. This second batch preserves that
breadth-first rule by testing three more mechanisms with exact contradictions
available:

- **E:** a shared uniform morphism;
- **G:** factoradic-header classes dispatching checksum algorithms;
- **H:** explicit reduction from the missing `83..124` cube states.

The real Eye scores must not be calculated until this file is committed. Each
implementation must first pass a planted positive control. A failed positive
control invalidates the test rather than the hypothesis.

## Existing-work boundary

This batch does **not** reopen:

- deterministic RePair or ordinary phrase compression;
- linear recurrences of orders 1–32;
- polynomial position moments or geometric hashes fitted panel by panel;
- ordinary base-five subtraction borrows, independent digit comparisons, or
  hidden-`Z101` crossings.

Those objects already have explicit negative or scoped boundaries. The three
tests below operate on a substitution production, an algorithm type, and a
missing-state reduction event respectively.

## E. Self-predicting uniform morphism

### Frozen object

For a finite word `w` and uniform length `L`, a phase-zero fixed-point prefix
must satisfy

```text
mu(w[i]) = w[L*i : L*i+L]
```

whenever the complete block exists. Thus every repeated source label must
induce the same length-`L` production. This is a strict, identifiable
consequence of a uniform morphic fixed point; merely assigning a private name
to each observed block is forbidden.

Use marker-stripped trigram words. Remove only the independently established
common opening of each natural sibling triple:

```text
east1, west1, east2: 24
west2, east3, west3:  5
east4, west4, east5: 20
```

Test `L = 2,3,4,5`. Learn literal productions from the first natural triple
and require the same visible-label productions in the remaining six panels.
There is no component permutation, reversal, panel-specific phase, private
alphabet, or approximate fit.

The diagnostic factor-complexity profile records, for lengths `1..12`, the
number of distinct factors and right-special factors after trimming. It
cannot promote the lane by itself.

### Positive control and decision

A fixture made from prefixes of a shared `2`-uniform substitution must recover
length `2`, its productions, and exact heldout consistency. On the Eyes:

- a contradiction inside the training triple closes the corresponding `L`;
- an exact training production with any heldout contradiction closes that
  candidate;
- promotion requires at least one production system exact on both halves.

No statistical tail can rescue a literal production contradiction.

## G. Header-dispatched checksum algorithms

### Frozen groups and target

Use the independently reproduced factoradic partition:

```text
P:      east1, west1, east2
Q-west: west2, west3, west4
Q-east: east3, east4, east5
```

For every panel, the first trigram is the check field and every remaining
trigram is the body. A rule predicts the first trigram exactly; it is not
allowed to predict a residue class that must later be interpreted.

### Frozen rule dictionary

Deduplicate rules that have the same nine-panel prediction vector. The named
dictionary contains, over moduli `83` and `101` and both signs where
applicable:

1. additive sum;
2. alternating sum beginning positive;
3. bitwise xor;
4. sum of all three base-five digits;
5. forward and reverse position moments of degrees `1` and `2`;
6. Fletcher first and second accumulators.

For modulus `101`, a prediction is valid only when the residue lies in
`0..82`; residues `83..100` do not name a visible marker.

### Strict leave-one-out prediction

For each class and each of its three possible heldout panels:

1. retain every dictionary rule that predicts the other two markers exactly;
2. if the retained set is empty, record **no prediction**;
3. if its rules disagree on the withheld marker, record **ambiguous**;
4. otherwise make their unanimous marker prediction.

A class passes only if all three heldout markers are correctly and
unambiguously predicted and the same rule-equivalence class survives the
three folds. This prevents catalog order or the withheld marker from breaking
ties.

The known `east1/east3/east5` additive mod-101 diagonal crosses these header
classes and therefore cannot by itself pass this test.

### Positive control and decision

Plant three groups whose markers were authored by three different dictionary
rules. All nine leave-one-out predictions and the dispatched rules must be
recovered. On the Eyes, any missing, ambiguous, or incorrect fold prevents
promotion. Only if all nine folds pass will matched controls be run; controls
must preserve the known diagonal complete-message sums while reselecting the
entire dictionary.

## H. Missing-state reduction events

### Frozen event

Write each accepted label as its canonical three base-five digits. For two
adjacent labels `a,b`, apply one componentwise operation modulo five:

```text
sum:          a + b
forward diff: b - a
reverse diff: a - b
```

Serialize the three result digits in one of the six component orders as one
raw cube rank `r in 0..124`. The event is

```text
reduce83(r) = 1 if r >= 83 else 0.
```

When the event is one, the accepted representative is `r-83`. This is the
specific use of the 42 excluded cube states that ordinary digit-borrow tests
did not model. The frozen catalog has `3 * 6 = 18` named conventions,
deduplicated only if their complete `83*83` event tables are identical.

### Train/heldout split

For each of the seven established nonliteral aligned contexts, compare the
complete adjacent-event word on the source window with that on its target
window.

```text
train:   first-gap30, first-cross, first-cross-late, first-gap28
heldout: last-west4, last-east5, last-east3
```

Select the convention with the most event agreements on training, breaking
ties by its frozen name. Apply it unchanged to heldout. Record the first
contradiction in each half.

### Positive control and decision

Construct independent two-symbol context pairs that preserve every event of
one target convention while contradicting every inequivalent rival at least
once. The target equivalence class must be uniquely recovered on training and
remain exact on heldout.

Promotion on the Eyes requires complete equality in both families. An
approximate score is descriptive only. If training is exact but heldout is
not, the hypothesis fails its prediction; if training itself is inexact, the
whole fixed catalog closes without controls.

## Branching rule

Commit this freeze before running any real score.

- If E, G, and H all close after passing their plants, return to breadth and
  freeze the next distinct mechanisms—reset automata and predictive Hankel
  state—before implementation.
- If exactly one survives, demand a second consequence of its *same* fitted
  object; do not add plaintext scoring or extra transforms.
- The unresolved lag-one wheel, recursive trie checksum, Gate construction
  vocabulary, practice ciphers 3/4, and source/chronology work remain on the
  lead ledger. This batch neither tests nor rejects them.
