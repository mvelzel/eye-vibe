# Twenty-first test freeze — Earthquake 17-bit mask

## Status

This protocol is frozen before inspecting any real masked slice or real score.

The Earthquake circle's numerical row lengths were used retrospectively to
construct the final-row selector. Its irregular row content has not yet been
used:

```text
11110111011101110
```

This is the first prospective test in the nineteenth wide horizon.

## Fixed input

Use only the three copied-opening-trimmed final bodies in fixed order:

```text
east4, west4, east5
```

Their already established clean-gap starts are fixed:

```text
16,18,17
```

Take exactly 17 values beginning at each start. Do not search nearby starts,
other messages, other slice lengths, or cyclic rotations.

## Mask family

The small authored gap fixes phase. Clockwise versus anticlockwise remains a
real ambiguity, and the sparse or dense side of a binary sieve may carry the
payload. Therefore the complete registered family is:

```text
forward ones
forward zeros
reverse ones
reverse zeros
```

No other rotation, phase, Boolean operation, or panel-specific orientation is
allowed.

## Remove the known answer

Offsets `0` and `11` are the already established equal anchor endpoints in
every panel. They are removed from every selected view before scoring. A mask
variant cannot receive credit for retaining the known repeat.

All promotion metrics therefore operate only on held-out offsets among:

```text
1..10,12..16
```

## Frozen metrics

For each mask variant, align the three selected held-out sequences by their
original slice offsets.

### 1. Nontrivial exact equality skeleton

Canonicalise each sequence by first occurrence. Score `1` only when all three
canonical skeletons are identical **and** contain at least one repeated pair.
An all-distinct skeleton scores `0`.

### 2. Common repeat pairs

For every unordered pair of selected offsets, count it when all three panels
have equality at that pair. All-false agreements do not count.

### 3. Consistent partial-bijection support

For each of the three panel pairs, compare equality relations on every
unordered selected-offset pair:

- `support` increases when either panel repeats;
- `conflict` increases when exactly one panel repeats.

That panel pair contributes its support only if `conflict=0`; otherwise it
contributes zero. Sum the contributions across all three panel pairs. This
prevents an all-distinct alignment from being described as a strong
partial-bijection result.

### 4. Aligned numeric equality

At each selected held-out offset, count the three unordered panel pairs whose
actual mod-83 values are equal.

No language score, modular sum, best affine map, substring, or plaintext crib
may be introduced after seeing the real slices.

## Conditional matched null

Run 50,000 controls with seed:

```text
0x21E17
```

For each final body independently:

1. preserve its exact length and multiset;
2. keep the real anchor value fixed at its registered start and start+11;
3. shuffle all other positions;
4. reject adjacent equal values;
5. reject unless the fixed pair remains the unique clean gap-11 anchor.

This conditions on the complete already promoted selector rather than making
controls rediscover it. It also preserves numeric anchor labels, so an
unrelated label coincidence is not obtained by weakening the null.

Apply all four mask variants and all four metrics to every accepted control.
For each metric, compare the real maximum over the four variants to the
control maximum over the same four variants. Use plus-one empirical tails.

Correct the minimum of the four metric tails by Bonferroni:

```text
corrected tail = min(1, 4 × minimum metric tail)
```

The mask is promoted only if:

```text
corrected tail < .01
```

The winning metric must also be nonzero. A zero-valued tie, an all-distinct
exact skeleton, or an interesting-looking unregistered arithmetic value
fails.

## Positive control

### Pre-evaluation correction

This wording was corrected after freezing but before inspecting real slices
or scores. Once known offset `0` is removed, the forward-one offsets are a
strict subset of the reverse-one offsets. Some registered metrics therefore
cannot identify forward-one uniquely even on a plant. Requiring a unique
variant would be mathematically impossible.

Before real evaluation, construct a three-panel plant with:

- the fixed gap-11 anchor in every panel;
- one extra common equality pair on forward-one offsets;
- a conflict-free nontrivial partial bijection;
- one aligned numeric equality;
- no adjacent doubles.

The detector must score every planted field nonzero in the forward-one view.
A tied or stronger superset view is allowed; real and control data already
maximize over the same complete four-variant family. The conditional shuffler
must preserve each plant's length, multiset, fixed anchor pair,
no-adjacent-double rule, and unique clean gap-11 witness.

## Stop rule

If the corrected gate fails, close the irregular mask as a direct selector on
these final slices. Do not rescue it by rotating the mask, shifting starts,
changing slice length, choosing separate directions per panel, or fitting a
plaintext.

If it passes, inspect only the preregistered winning field first and require
it to predict a new structural role before attempting any decoder.
