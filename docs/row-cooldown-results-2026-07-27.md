# Physical-row recurrence cooldown — results

## Outcome

After marker removal and the independently established natural opening trims,
the nine bodies have exact minimum same-label recurrence distances:

```text
             East/West panels       minimum distances
physical row 1: E1 W1 E2            3 3 3
physical row 2: W2 E3 W3            2 2 2
physical row 3: E4 W4 E5            4 4 4
```

This is a real ciphertext invariant, but it was found retrospectively. It does
not identify an intended cooldown, key, plaintext, or decoder.

## Exact observations

The full lag-1 through lag-10 equality counts are:

```text
E1  0 0 2 2 0 1 2 1 0 1
W1  0 0 2 2 2 0 2 1 4 1
E2  0 0 2 2 2 0 2 2 3 0
W2  0 1 1 2 3 2 0 2 0 1
E3  0 1 1 3 3 0 1 0 4 1
W3  0 3 1 2 0 3 0 1 2 0
E4  0 0 0 3 0 3 1 1 0 2
W4  0 0 0 3 0 1 2 2 0 2
E5  0 0 0 3 1 2 2 1 0 1
```

Thus row 1 has no lag-2 recurrence and row 3 has no lag-2 or lag-3
recurrence; row 2 adds only the already known corpus-wide no-double property.
The registered contexts already contain the boundary recurrences at lag 3
and lag 4. After those cells are fixed, the remaining question is chiefly
whether any free cell introduces a shorter recurrence.

First-half minima reproduce the full vector exactly. Second-half minima are:

```text
3 3 3 | 3 3 2 | 4 4 4
```

Fitting thresholds `3,2,4` on first halves predicts all second halves, but
this split event is common under both nulls below and supplies no evidence.

## Frozen controls

The deterministic positive control generated 83-label processes with
minimum distances `3,2,4` and recovered the exact target vector.

Two 100,000-trial matched nulls used corrected empirical tails:

| Null | exact `333|222|444` | row-uniform | uniform and distinct | split pass |
|---|---:|---:|---:|---:|
| per-body multiset shuffle, no doubles | 2 (`.0000300`) | 3,522 (`.03523`) | 3 (`.0000400`) | 59,889 (`.59889`) |
| exact registered-context cells fixed | 72 (`.0007300`) | 1,681 (`.01682`) | 74 (`.0007500`) | 61,331 (`.61331`) |

The second null is the evidentiary control: it preserves the exact values of
all cells in the seven pre-registered nonliteral contexts, every per-body
multiset, and no adjacent doubles. Its fixed/free cell counts are:

```text
E1 18/56  W1 36/42  E2 36/57
W2  0/96  E3 25/106 W3  0/118
E4 30/68  W4 30/69  E5 30/63
```

The small exact tail retains the vector as a candidate invariant. It is not a
discovery p-value: the grouping and statistic were noticed after extensive
inspection, and no correction over that search history is available.

## Practice transfer and community-prior audit

The unchanged detector does not reproduce the pattern on sdlwdr's practice
ciphers:

```text
Cipher 3 A: 4 3 2 2 4 4
Cipher 3 B: 2 3 3 3 3 2
Cipher 3 C: 3 2 3 4 3 2
Cipher 4 raw: 2 2 2
Cipher 4 cyclic differences: 2 2 1
```

A read-only search of `silmä-cryptography` found no posted statement of this
exact physical-row `3/2/4` vector. The method is nevertheless prior art.
Community discussions by Lymm on 1 July, 4–5 and 22 December 2025 explicitly
analyze repeat-distance absences, show that they can vary greatly with the
plaintext mapping, and derive them from permutation products and stabilizers.
The community had therefore already identified both the technique and the
main reason not to interpret a missing short lag as an authored instruction.

## Judgment

Keep the exact rowwise vector in the evidence inventory, but do not claim it
as a cryptanalytic advance. Reopen it only if an independently selected
cipher family or in-game clue predicts the three row thresholds before
inspecting the recurrence data and then yields a new held-out consequence.
