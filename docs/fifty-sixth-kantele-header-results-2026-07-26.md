# Executable Kantele/header audit

**Date:** 26 July 2026  
**Outcome:** negative for this exact interface.

## Question

Two community documents had already proposed mapping the five Eye directions
to Kantele notes and playing Eye-derived music. The new, narrower question was:

> Do the real factoradic header operations turn the exact header-stripped
> renderer rows into Noita's executable Kantele secret songs?

This tests an in-game consumer rather than whether a derived tune sounds
intentional. It does not retest arbitrary sonification.

## Frozen construction

The current installed WAK has 14,745 entries. Its
`data/scripts/biomes/mountain_tree.lua` gives the five Kantele notes in the
order

```text
a, d, dis, e, g
```

and `data/scripts/magic/kantele.lua`, together with `alt_notes` in
`data/scripts/lib/utilities.lua`, gives these four executable note-index
sequences:

```text
portal   0 2 3 4
bomb     4 1 3 1
worm     1 3 0 3 2
alchemy  4 2 4 3 0
```

For every message, the audit:

1. removes the marker's three eyes in exact renderer-row geometry;
2. retains value `5` as the visual-row separator;
3. tries identity, the message's real six-symbol factoradic permutation, and
   its inverse;
4. searches both all substrings and exact separator-delimited rows.

The matched control repeats the complete selection after each of all 120
global permutations of the five eye labels. No song, route, or per-message
repair is chosen after seeing the real result.

## Complete result

The three real route scores are `(whole rows, row-terminal hits, all hits)`:

```text
identity        (0, 1, 3)
header          (0, 0, 9)
inverse-header  (0, 0, 6)
```

The favorable lexicographic selector therefore chooses identity. Its three
hits are:

```text
west1  bomb    [112,116)  ends at a row boundary
east3  bomb    [263,267)  internal substring
west3  portal   [44,48)   internal substring
```

There is no complete row matching any executable song under any real route.
The selected real score is only `(0,1,3)`. Of the 120 relabeling controls,
85 score at least as high:

```text
exact tail = 85/120 = 0.708333333
control maximum = (2,2,9)
```

The maximum control uses relabeling `(2,4,1,3,0)` and the header route. It
creates two exact-row songs, while the real labeling creates none.

## Decision

Close the direct interface

```text
real factoradic header operation
    -> globally relabeled renderer tape
    -> exact current Kantele secret-song matcher
```

The result does **not** reject every possible Kantele clue. Reopen only if an
independent game asset supplies a different note order, segmentation rule,
rhythm, or stateful song consumer. Do not reopen merely by trying more
pleasant-sounding sonifications.

## Reproduction

```text
PYTHONPATH=src python3 scripts/audit_kantele_header.py
```

Implementation:

- `src/eye_mystery/kantele_header.py`
- `tests/test_kantele_header.py`
