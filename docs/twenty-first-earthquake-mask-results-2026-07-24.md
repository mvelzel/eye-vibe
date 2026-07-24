# Twenty-first test — Earthquake 17-bit mask results

## Result

The prospective direct-sieve model fails completely:

```text
corrected tail = 1
passes = false
```

All four mask variants score zero on all four registered held-out metrics.
The irregular Earthquake row does not select a shared equality skeleton,
partial bijection, or aligned numeric field from the fixed final slices.

Under the frozen stop rule, this closes direct masking at starts `16,18,17`.
No rotations, shifted starts, alternate lengths, panel-specific directions,
or post-hoc arithmetic repairs are licensed.

## Positive control

The plant exercises every registered field in the forward-one view:

```text
nontrivial exact skeleton       1
common repeat pairs             1
consistent bijection support    3
aligned numeric equalities      3
```

Its three conditional shuffles preserve length, multiset, fixed gap-11
anchor, no adjacent doubles, and the unique registered witness. They require
`2,1,1` attempts respectively.

## Exact real slices

The 17 values beginning at the registered trimmed starts are:

```text
east4 start16
75,48,54,55,19,62,64,14,47,51,70,75,5,11,47,45,58

west4 start18
81,39,14,78,0,25,65,43,66,64,38,81,23,24,50,57,30

east5 start17
48,54,55,52,62,72,69,10,57,22,58,48,67,53,7,34,32
```

Offsets `0` and `11` are the known anchor repeats and are excluded below.

### Forward ones

Offsets:

```text
1,2,3,5,6,7,9,10,13,14,15
```

Values:

```text
east4 48,54,55,62,64,14,51,70,11,47,45
west4 39,14,78,25,65,43,64,38,24,50,57
east5 54,55,52,72,69,10,22,58,53,7,34
```

### Forward zeros

Offsets:

```text
4,8,12,16
```

Values:

```text
east4 19,47,5,58
west4 0,66,23,30
east5 62,57,67,32
```

### Reverse ones

Offsets:

```text
1,2,3,5,6,7,9,10,13,14,15,16
```

Values:

```text
east4 48,54,55,62,64,14,51,70,11,47,45,58
west4 39,14,78,25,65,43,64,38,24,50,57,30
east5 54,55,52,72,69,10,22,58,53,7,34,32
```

### Reverse zeros

Offsets:

```text
4,8,12
```

Values:

```text
east4 19,47,5
west4 0,66,23
east5 62,57,67
```

Every selected sequence is internally all-distinct. No selected aligned
offset has equal numeric values in any panel pair.

## Matched controls

Each of 50,000 controls independently preserves:

- complete body length and multiset;
- the real numeric anchor at the registered start and start+11;
- no adjacent doubles;
- the fixed witness as the unique clean gap-11 anchor.

The shuffler used:

```text
1,305,953 attempts for 150,000 accepted streams
mean 8.706353 attempts per stream
```

For every metric, the observed maximum over all four variants is zero. Every
control is therefore at least observed:

```text
metric                            observed  controls >=  tail
nontrivial exact skeleton                0  50000/50000  1
common repeat pairs                      0  50000/50000  1
consistent partial-bijection support     0  50000/50000  1
aligned numeric equalities               0  50000/50000  1
```

The four-metric Bonferroni correction remains `1`.

## Interpretation

The Earthquake circle may still be:

- a retrospective vocabulary of lengths/cardinalities;
- a physical wheel or timing diagram;
- a component-order clue;
- unrelated to the Eyes.

What it is not, under this test, is a direct binary sieve on the fixed
17-symbol final slices. This negative removes the highest-priority lane from
the nineteenth horizon without weakening the independently validated final
anchor record.

The next Earthquake work should move laterally to a genuinely different
consumer—fixed physical wheel timing or an independently derived
rune-to-component order—not rescue this failed mask.
