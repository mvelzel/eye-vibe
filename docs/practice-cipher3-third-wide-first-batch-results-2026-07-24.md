# Practice cipher 3 — third wide first-batch results

## Result

The first deliberately wide batch is negative. It finds no undisclosed
master-tape excerpt, recurring affine relation, low-order field generator,
direct numeric MTF/BWT interpretation, compression signature, or useful
equality-only grammar.

This does not solve Cipher 3. It narrows the mechanism by excluding five
cheap families with exact inventories, heldout residual tests, or matched
controls. The long A prefix tree remains the only strong positive structural
feature.

## Cross-stream exact and affine factors

Every pair of streams was compared in both directions at every pair of
offsets. For each two-symbol seed, the unique map

```text
y = a*x + b (mod 83), a != 0
```

was extended until its first mismatch. The disclosed A prefix branches were
removed before scoring.

There is no undisclosed exact common factor of length at least four. The
affine inventory contains 651 length-four and nine length-five runs. Its best
run is:

```text
A3[43:48] -> reverse(B5)[46:51]
a=46, b=80, length=5
```

All nine length-five maps occur once. No affine relation recurs in an
independent pair, so none meets the frozen prediction gate.

## Equality-pattern factors

Arbitrary relabelling can make a long factor look impressive when nearly
every value is new. The raw longest undisclosed equality isomorph is length 30
between A0 and reversed C3, but contains only one repeated equality
constraint.

The factor selected by actual repeat evidence is:

```text
C3[76:104] <-> C5[147:175]
length=28
distinct values=26
repeated constraints=2
```

Two constraints are insufficient to identify a grammar or common plaintext
tape. This closes only the equality-only explanation of the observed
non-A-prefix factors, not arbitrary hidden substitution.

## Low-order generators over `F83`

Order-one and order-two homogeneous recurrences were selected by minimizing
the residual alphabet on A, then transferred unchanged to B and C:

```text
order  coefficients  A residuals  B residuals  C residuals  union
1      (53)          77           83           83           83
2      (70,34)       75           83           83           83
```

Removing each first symbol gives the same result. Neither recurrence reduces
heldout data to the expected 42-symbol range.

The Berlekamp–Massey linear complexity of every body is essentially half its
length. Across all eighteen messages the ratio lies between
`0.497326` and `0.507692`. That is the random-like regime, not evidence for a
short linear recurrence.

## Compression and recoding

The 2,229 body events have:

```text
empirical entropy                6.344283 bits/symbol
maximum for 83 uniform symbols   6.375039 bits/symbol
adjacent equal pairs             0
direct LZ78 phrases              1588
direct MTF decoded union         83 symbols
largest one-message MTF union    80 symbols
```

Direct numeric MTF therefore does not produce a 42-symbol plaintext.

Treating the first value as a literal BWT primary index is invalid for A2,
A3, and A5 because the index exceeds the body length. The remaining 15
messages invert to 1,255 LZ78 phrases. In 1,000 controls that independently
shuffle each body while preserving its header and multiset:

```text
direct LZ78 lower tail       243/1001 = .242757
inverse-BWT LZ lower tail    759/1001 = .758242
```

Neither statistic is exceptional. This excludes the literal first-symbol
BWT-index interpretation and a direct MTF/BWT compression signature, not
encrypted, permuted, or packed codec metadata.

## Author and source audit

The complete read-only Discord thread supplies two relevant statements but no
mechanism hint. In May 2025 sdlwdr called the forthcoming third puzzle “a bit
more unique.” In July 2026 they said they had lost its source code and hoped
they would remember enough to confirm a solution. The original thread itself
contains only the A/B/C attachment and the corrected first A line.

Because the same author used Crawford's *Kalevala* in earlier puzzles, the
public-domain [Project Gutenberg Crawford
Kalevala](https://www.gutenberg.org/ebooks/5186) was checked for the observed
`43/8` prefix-tree shape under three normalizations. Thousands of matching
formulaic passage pairs exist, so that shape is common in this source and
does not locate a passage. The earlier static source-fingerprint test remains
negative. Kalevala is still plausible only under a mechanism that changes
the equality implication.

## Scope

Closed by this batch:

- undisclosed exact common substrings of length at least four;
- recurring pairwise affine common-tape masks in the frozen `F83` family;
- order-one/two homogeneous `F83` recurrences with a 42-value residual;
- a short linear recurrence visible in individual bodies;
- direct numeric MTF to a 42-symbol alphabet;
- the first symbol as a literal BWT primary index for all messages;
- exceptional direct or inverse-BWT LZ78 compressibility;
- an equality-only common-factor grammar beyond the disclosed prefix tree.

Still open:

- affine/deck state whose decoded action depends on hidden state;
- arbitrary PRNG or counter masking;
- the exact `83=2*42-1` two-sheet construction;
- higher-order state, output-rank decks, polygraphic routes, and
  variable-length codes;
- a source text after a mechanism supplies the correct source invariant.

The most motivated next test is an affine `AGL(1,83)` deck/GAK family. It is
not a recurrence in the visible ciphertext, and it follows the construction
genealogy of the author's solved ciphers without assuming their recovered
wheel.
