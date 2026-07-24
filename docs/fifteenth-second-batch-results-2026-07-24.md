# Fifteenth wide horizon — second batch results

## Outcome

The three frozen mechanisms E/G/H all close after passing their positive
controls:

1. every uniform morphism length `2..5` contradicts itself inside the
   training triple;
2. header-class checksum dispatch predicts `0/9` withheld markers;
3. none of the 18 missing-state reduction conventions preserves even the
   complete training event word.

These are clean exclusions of the declared finite objects, not a solution and
not evidence against unrelated morphic ciphers, checksums, or arithmetic.

Reproduce with:

```bash
PYTHONPATH=src python scripts/run_fifteenth_second_batch.py
PYTHONPATH=src python -m unittest tests.test_fifteenth_second -v
```

The complete suite passes 493 tests with Z3 enabled.

## E. Self-predicting uniform morphism

### Positive control

The plant uses the two prolongable productions

```text
0 -> 01
1 -> 10
```

on nine independent finite prefixes. The detector recovers those literal
length-two productions and predicts the heldout prefixes exactly. Length four
also closes because it is the second iterate of the same substitution; this
is expected rather than a second planted mechanism.

### Eye result

After removing the marker and only the known natural-family copied openings,
each candidate is already inconsistent in East 1:

```text
L=2, source index 8, label 40:
  expected 81,21
  observed 44,48

L=3, source index 8, label 40:
  expected 19,0,40
  observed 49,72,31

L=4, source index 8, label 40:
  expected 40,51,65,26
  observed 67,33,49,41

L=5, source index 8, label 40:
  expected 65,26,14,21,70
  observed 5,25,20,71,11
```

Because one visible source label demands two different productions, no
heldout fit or statistical control can repair the exact contradiction.

The descriptive `(distinct factors / right-special factors)` profile is:

```text
n= 1:  83 / 83
n= 2: 802 / 49
n= 3: 846 /  5
n= 4: 842 /  2
n= 5: 835 /  1
n= 6: 827 /  1
n= 7: 819 /  1
n= 8: 811 /  1
n= 9: 803 /  1
n=10: 795 /  1
n=11: 787 /  1
n=12: 779 /  1
```

The tape saturates all 83 one-symbol factors and rapidly approaches
mostly-unique longer factors. That is qualitatively unlike a small
low-complexity word, but the exact production contradictions—not this
description—close the lane.

**Boundary:** phase-zero shared uniform fixed-point productions of lengths
`2..5` are rejected. Panel-specific phases, nonuniform substitutions,
codings after a morphism, and reset automata are different hypotheses and
must be independently frozen rather than added here.

## G. Header-dispatched checksum algorithms

### Positive control

Three synthetic header classes were authored with different standard rules:

```text
P:      negative additive sum mod 83
Q-west: positive alternating sum mod 101
Q-east: positive Fletcher second accumulator mod 83
```

After prediction-vector deduplication the first is named
`fletcher1-mod83-minus`, because Fletcher's first accumulator is exactly the
additive sum. The plant has 32 distinct prediction vectors, makes all `9/9`
unambiguous leave-one-out predictions, and recovers the three dispatched
rules.

### Eye result

The same 32-vector dictionary gives:

```text
class    heldout panel  training-compatible rules  result
P        east1          0                          no prediction
P        west1          0                          no prediction
P        east2          0                          no prediction
Q-west   west2          0                          no prediction
Q-west   west3          0                          no prediction
Q-west   west4          0                          no prediction
Q-east   east3          0                          no prediction
Q-east   east4          1                          incorrect
Q-east   east5          0                          no prediction
```

The lone East 4 fold is informative. Training on East 3 and East 5 retains
`fletcher1-mod101-minus`, which is precisely the already-known negative
additive diagonal rule. Applied to East 4 it predicts a residue in
`83..100`, not a visible marker, while the actual marker is 27. Thus the
famous `east1/east3/east5` checksum cannot masquerade as a successful header
class: it crosses the factoradic partition and fails the withheld member.

There are `0/9` correct folds, no passed class, and no common dispatched rule.
Matched controls were not opened because the exact prerequisite failed.

**Boundary:** these factoradic classes do not dispatch the frozen additive,
alternating, xor, digit-sum, Fletcher, or degree-one/two moment algorithms
over 83/101. An algorithm selected by authored code or a different check
scope remains possible; per-panel fitting is forbidden.

## H. Missing-state reduction events

### Positive control

The fixture builds independent transition pairs whose event equality is
preserved by

```text
componentwise sum mod 5
serialization order 2,0,1
raw-rank threshold at 83
```

while every inequivalent rival is contradicted. The exact plant scores are:

```text
catalog:  18
selected: sum-order201
training: 6/6
heldout:  5/5
```

### Eye result

Selection on the first four nonliteral contexts chooses:

```text
selected: sum-order012
training: 45/59
heldout:  41/82
exact training conventions: 0/18
```

The first training contradiction is:

```text
first-gap30, index 3
source transition: 14 -> 21, event 0
target transition: 25 -> 64, event 1
```

The fixed winner's first heldout contradiction is:

```text
last-west4, index 4
source transition: 22 -> 60, event 0
target transition: 43 -> 66, event 1
```

For context, the heldout-best convention *if it were selected after looking*
would reach only `51/82`; the legitimate training winner reaches `41/82`.
Neither matters to the exact gate because no training convention preserves
the complete event word.

**Boundary:** the seven isomorph windows do not preserve one shared binary
event defined by componentwise sum or either difference, any of six digit
serializations, and reduction of raw cube ranks `83..124` by 83. This does
not alter the still-unresolved arbitrary lag-one 83-wheel CSP.

## Decision

No second-batch lane earns depth. Do not:

- introduce panel-specific morphism phases or productions;
- enlarge the checksum dictionary until two markers happen to fit;
- convert the approximate reduction bits to text;
- select a reduction convention on heldout data.

The wide horizon should now move laterally again. The nearest distinct finite
objects are reset/synchronizing automata and minimal predictive/Hankel state.
Before either implementation, freeze them together with several additional
novel candidates so the next choice again begins wide.

The original trie checksum, lag-one geometry, Gate construction vocabulary,
practice ciphers 3/4, source ancestry, and chronology leads remain active and
unchanged.
