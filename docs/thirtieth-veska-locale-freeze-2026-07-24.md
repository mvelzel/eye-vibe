# Thirtieth freeze — direct Veska locale reading

## Observation that selected the lane

The earlier ground-up Gate audit fixed two spatially separate Veska mark bands
before this reading was noticed:

```text
upper: 9 pixels, left-to-right 8-neighbour component sizes 1,5,3
lower: 8 pixels, one five-pixel plus followed by three singleton components
```

Read the upper component sizes as decimal `153`. Under the Eye modulus and
ASCII+32 convention:

```text
153 mod 83 = 70 -> f
(153 + 3) mod 83 = 73 -> i
```

The Gate marks therefore admit a direct `fi` reading: the upper band supplies
the operand, and the lower band supplies `+3`. This matches the marker BWT
suffix independently recovered as `!Fi`.

This observation is post hoc. The following checks describe its specificity;
they do not create a discovery p-value.

## Fixed asset extraction

Use the exact mark color `(60,57,65,255)` in the unchanged Veska sprite
SHA-256:

```text
a2e7dd2bfb9b573eb733c1e4d2e52fa0163925b8aeb233b37870332dc264854f
```

Retain the previously published bands:

```text
upper: 9 <= x <= 40 and 12 <= y <= 22
lower: 13 <= x <= 49 and 46 <= y <= 53
```

Use 8-neighbour connected components. Order upper components by their minimum
`x`. Recognize the lower operator only when:

- exactly one five-pixel component is an orthogonal plus (center plus four
  cardinal neighbours);
- every other component is a singleton;
- every singleton lies strictly to the right of the plus.

The increment is the singleton count.

## Fixed reading and comparisons

Primary:

1. concatenate the one-digit upper component sizes in natural left-to-right
   order as a decimal integer;
2. emit `n mod 83 + 32`;
3. add the lower increment to the same `n`, reduce mod 83, and emit again.

Comparators:

- report all six permutations of the upper component order;
- report the horizontal mirror, which reverses left-to-right order;
- over all 83 possible starting residues, count:
  - lowercase-to-lowercase `+3` pairs;
  - pairs that are an assigned two-letter geographic region code in the
    pinned libphonenumber map;
- report which upper-component permutations form assigned region codes.

No alternate band, connectivity, base, modulus, character offset, arithmetic
operator, component weighting, or decimal digit separator is admitted.

## Chronology and interpretation gate

The identical sprite is present in the public 9 February 2021 data snapshot,
and community evidence places the boss on beta in December 2020. It postdates
the October 2020 Eye Messages and is eligible only as a later decoder clue.
The March 2023 RNG salt pair is later still and can independently restate the
`+3` operator.

Promotion here means “deliberate later locale/header cross-reference,” not
“body decoder.” A body operation still needs an independently fixed scope and
must predict an untouched equality or re-encrypt recovered plaintext.
