# Sixteenth wide horizon — second batch freeze

## Purpose

The first A/C/D/E batch closed four mechanisms. This second batch does not
relax them. It selects three different queued objects from the already frozen
wide horizon:

- **B:** the exceptional outer automorphism of `S6`;
- **H:** header-defined canonical necklace/Lyndon cuts;
- **I:** fractional semilinear actions in `GF(125)`.

The first is a six-symbol group action, the second is label-ordered word
combinatorics, and the third is complete-cube field geometry. No real Eye
score may be calculated until this file is committed.

Each implementation must pass a planted positive control before any real
score is admissible. The abstract identities `Out(S6)=C2`,
`PGL(2,5) ~= S5`, and `125=5^3` are construction motives, not scoreable Eye
evidence.

## B. Exceptional outer-`S6` renderer action

### Canonical construction

On six points:

1. enumerate the 15 **duads** (two-point subsets);
2. enumerate the 15 **synthemes** (partitions into three duads);
3. enumerate the six **pentads** (sets of five synthemes partitioning all
   duads);
4. order pentads lexicographically;
5. let a permutation of the six original points act on the six pentads.

This gives one explicit outer automorphism `phi:S6->S6`. Validate before use:

```text
phi(pq) = phi(p)phi(q)
transposition -> triple transposition
standard point-stabilizer S5 -> transitive exotic S5
```

The exact choice of pentad labels is arbitrary up to inner conjugacy, so the
complete frozen catalog is:

```text
c phi(h) c^-1  for every c in S6
```

under header or inverse-header route: `720*2=1440` named candidates.

### Renderer-syntax consumer

For every panel, apply its transformed header permutation to the exact
six-symbol renderer body tape. The expected newline mask is fixed by the
authored visual rows. A decoded tape is syntactically valid iff:

- every expected newline position contains symbol 5; and
- no other position contains symbol 5.

Select the candidate with the fewest newline-mask mismatches on P, breaking
ties by its frozen name. Apply that exact candidate unchanged to Q.

### Positive control and decision

Choose one catalog member and encode valid renderer tapes by its inverse,
panel by panel. The audit must recover an exact P candidate and decode Q with
zero mismatches.

Promotion requires zero P and zero Q mismatches. A guaranteed abstract exotic
`S5`, a train-only fixpoint, or a low mismatch count fails. A negative result
closes only this direct outer-header renderer action; it does not reject the
factoradic metadata or every possible outer-automorphism consumer.

## H. Header-defined necklace and Lyndon cuts

### Frozen word

Use the exact marker-removed renderer body tape, including every authored
newline. Each header supplies an alphabet order by either its unranked
permutation or inverse. Test the tape forward or reversed: four candidates.

For a candidate:

1. replace each renderer symbol by its rank in the candidate header order;
2. compute the lexicographically least cyclic rotation;
3. record whether the existing cut is that least rotation;
4. compute primitivity, border length, and Duval Lyndon factor count only as
   diagnostics.

No cyclic shift is selected. The hypothesis is precisely that the authored
start is already the canonical necklace cut.

Select the candidate maximizing canonical P panels, then primitive P panels,
with frozen-name tie breaking. Apply it unchanged to Q.

### Positive control and decision

Generate primitive tapes and rotate each to its unique least rotation under
one target header route/direction. The exact target must make every planted
P and Q panel canonical.

Promotion requires all three P and all six Q panels canonical. A shared factor
count, short border, or nearly minimal cut cannot pass. Failure does not
reopen arbitrary rotation scans, BWT collation, or language-selected cuts.

## I. `GF(125)` Möbius/Frobenius contexts

### Frozen field catalog

Interpret digits `(a,b,c)` as

```text
a*t^2 + b*t + c
```

in `F5[t]/f(t)`, for each of the 40 monic irreducible cubics `f`. Enumerate
the three Frobenius powers `k=0,1,2`. One representation therefore means:

```text
field polynomial f
source premap x -> x^(5^k)
```

For each repeated context, fit its own fractional map

```text
y = (A*x^(5^k)+B) / (C*x^(5^k)+D)
```

from three distinct source/target edges by homogeneous linear algebra. Demand
`AD-BC != 0`; a zero denominator predicts infinity and fails because the Eye
alphabet contains no infinity sentinel.

The complete catalog has `40*3=120` representations. Coefficients are local
to a context; field polynomial and Frobenius power are global.

### Train/heldout rule

For each representation and context, enumerate three-edge fitting subsets in
lexicographic order and keep the map with maximum exact edge agreement,
breaking ties by normalized coefficient tuple.

Select one representation on the four first-family contexts by:

1. exact contexts;
2. total matched edges;
3. frozen representation name.

Apply that representation unchanged to the three last-family contexts, while
fitting only their local fractional coefficients.

### Positive control and decision

Generate seven independent planted Möbius maps in one selected field and
Frobenius representation. The target representation must be among the exact
training equivalence class and remain exact heldout. If field-isomorphic
representations are observationally equivalent, report the full class rather
than claim false uniqueness.

Promotion requires all four training and all three heldout contexts exact.
Any fourth-edge contradiction rejects a local map. Approximate agreement,
train-only closure, or increasing to arbitrary rational degree fails.

Literal affine `F5^3` actions are already rejected and are not rerun. This
lane tests only the genuinely different fractional/Frobenius completion.

## Branching rule

- Commit this freeze before calculating B/H/I real scores.
- Run all three positive controls before opening any real score.
- Failure in one lane cannot donate its convention to another.
- If all three close, return to breadth across reset/Hankel, graph covering,
  finite-state coding, archaeology, and practice-puzzle transfer. Do not
  enlarge the closest miss.
- If one survives exactly, freeze its selected object and demand a second
  consequence before plaintext scoring.
- Preserve the original trie checksum, arbitrary lag-one wheel, factoradic
  metadata, Gate construction vocabulary, practice ciphers 3/4, source
  ancestry, and chronology ledger.

## Result

All three mechanisms close after their plants pass:

- the best of 1,440 outer-`S6` renderer actions has `53/977` P and
  `364/2190` Q newline-mask mismatches; no P candidate is exact;
- all four necklace conventions have `0/3` canonical P and `0/6` canonical Q
  panels;
- no `GF(125)` representation makes any context exact; the selected
  `t^3+2t^2+2t+3`, Frobenius-one representation reaches only
  `8/18,6/18,9/18,6/9` on P and `7/30,7/30,7/25` on Q.

Full evidence:
[`sixteenth-second-batch-results-2026-07-24.md`](sixteenth-second-batch-results-2026-07-24.md).
Return to breadth; do not expand these failed families.
