# Seventeenth horizon lane C — predictive Hankel freeze

## Empirical series

Use markerless bodies after removing the already known copied openings:

```text
east1/west1/east2          24 symbols
west2/east3/west3           5 symbols
east4/west4/east5          20 symbols
```

For a set of reset messages, define `f(w)` as the total number of contiguous
occurrences of word `w` without crossing a message boundary. The empty word
occurs at every token boundary.

For prefix vocabulary `U_r` and suffix vocabulary `V_s`, containing the empty
word plus every observed word of lengths `1..r` or `1..s`, build:

```text
H[u,v] = f(u || v)
```

This is a finite block of the empirical Hankel matrix of the body series.

## Frozen family

Test exactly:

```text
(r,s) in {(1,1), (2,1), (1,2)}
field prime in {83,101,257}
```

For each depth pair, score:

```text
minimum over the three primes of
    1 - rank(H) / min(number of rows, number of columns)
```

The minimum requires a deficit to survive every field. Select the depth pair
with maximum training score on P; ties use the order above. The field is not a
selectable parameter.

Apply the selected depth unchanged to Q. Promotion requires:

1. positive rank deficit on all three P and Q fields;
2. corrected Q lower-rank tail at most `.01` under the complete selection
   control below;
3. a separately frozen continuation statistic predicted by the recovered
   rank. A low rank alone is not a decoder.

## Joint control

Use 200 deterministic controls. Independently shuffle each trimmed message
while preserving:

- its exact length;
- its exact symbol multiset;
- the no-adjacent-double condition.

Each control shuffles P and Q, reselects `(r,s)` on its own P split, and scores
its corresponding Q split. This reproduces the complete selection procedure.
The copied-prefix nuisance has already been removed rather than regenerated.

The corrected upper tail counts controls whose selected-Q deficit is at least
the real selected-Q deficit.

## Positive control

Before Eye scoring, generate reset streams from one small deterministic
weighted/periodic automaton with the same no-double condition. The complete
pipeline must:

- yield a positive deficit on every field;
- beat at least 99% of its shuffled controls on heldout messages;
- choose one of the frozen depth pairs without a plant-only convention.

If this fails, no real rank is interpreted.

## Scope

A negative result closes only low empirical Hankel rank at these shallow
depths after copied-prefix removal. It does not exclude a large automaton,
nonstationary panel-specific state, or a rank visible only after an
independently selected symbol quotient.
