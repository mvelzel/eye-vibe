# Physical-row recurrence cooldown — freeze

## Discovery and scope

This is a retrospective discovery, not a prospectively selected statistic.
After removing each marker and the already established natural copied opening,
the minimum same-label recurrence distances appeared constant within each
physical message row:

```text
row 1: 3,3,3
row 2: 2,2,2
row 3: 4,4,4
```

The following controls are frozen before their definitive runs. Small
50,000-trial exploratory screens suggested that the pattern is unusual, but
their values are not confirmatory and will not be combined with the frozen
results.

The canonical rows are:

```text
east1, west1, east2
west2, east3, west3
east4, west4, east5
```

Opening trims are the independently established `24,24,24 / 5,5,5 /
20,20,20`. No alternative grouping, trim, marker inclusion, cyclic cut, or
lag convention is searched.

## Statistic

For a word `x`, define:

```text
m(x) = min(j-i) over i<j and x[i]=x[j]
```

Report:

1. the exact nine-value vector;
2. whether all three values agree within every physical row;
3. whether the three row values are distinct;
4. lag-match counts `1..10` for every panel;
5. the same minima in the first and second half of every trimmed word.

The primary event is the exact vector `(3,3,3,2,2,2,4,4,4)`. Row agreement
and distinctness are broader descriptive statistics.

## Positive control

Generate three identity-labelled 83-symbol cooldown processes, with exclusion
windows `2,1,3`, at the nine real trimmed lengths. The detector must return
minimum recurrence distances `3,2,4` by row. If a deterministic plant lacks
an exact boundary hit, extend only that plant; do not alter the detector.

## Null A — multiset and no-double

Run 100,000 trials with seed `0xC001D04`. Independently permute every trimmed
word's complete multiset and reject arrangements containing an adjacent
double. This preserves:

- every message length and frequency table;
- the 83-symbol numeric inventory;
- the already known corpus-wide no-double fact;
- the physical rows and natural opening trims.

It deliberately breaks the registered isomorphic contexts.

## Null B — registered-context stress test

Run another 100,000 trials with seed `0xC001D05`. Freeze in place every
trimmed-word cell participating in any of the seven pre-registered nonliteral
contexts. Independently permute only the remaining cells of each word,
preserving its multiset and rejecting adjacent doubles.

This conditions on the exact values—not merely the equality signatures—of all
previously promoted context evidence. It asks whether the cooldown vector adds
anything beyond those selected structures. Because it freezes much of the
corpus, this is the primary evidentiary control.

Use corrected empirical tails `(hits+1)/(trials+1)`.

## Internal replication

Split every trimmed word at `floor(length/2)`. For each physical row, infer the
largest cooldown guaranteed by all three first halves:

```text
t(row) = min(m(first_half(panel))) over the row
```

Without refitting, require every second half in that row to have minimum
recurrence distance at least `t(row)`. Report this under both null families.
This is a robustness check, not a clean prospective holdout, because the
overall lead was found retrospectively.

## Practice-puzzle transfer

Apply the unchanged minimum-gap inventory to:

- all 18 marker-stripped sdlwdr Cipher 3 streams, retaining its authored
  `A/B/C` groups;
- the three raw Cipher 4 portions and their established cyclic-difference
  streams.

This transfer is diagnostic only. A match does not corroborate the Eyes, and
a mismatch does not reject either practice mechanism.

## Interpretation

- A context-fixed corrected tail below `.01` retains a new ciphertext
  invariant and motivates a separately frozen row-conditioned machine test.
- A common context-fixed event closes the lead as a consequence of already
  selected isomorphs.
- No result identifies plaintext, an allocator, or a decoder.
- Because the statistic was discovered after extensive exploration, even a
  small tail is hypothesis-generating until an external clue or genuinely
  unseen consequence selects the cooldown mechanism.
