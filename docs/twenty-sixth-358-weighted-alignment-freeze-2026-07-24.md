# Twenty-sixth pass — frozen `3,5,8` weighted panel alignment

## Question

The marker grid reads `3,5,8` by canonical columns. Test the narrowest direct
body consumer: use those three numbers, once and in that order, as coefficients
on the three naturally aligned panels in every marker row.

The fixed relation is:

```text
3 * column0 + 5 * column1 = 8 * column2  (mod 83)
```

The sign convention is not searched. It is the ordinary `3+5=8` form and is
translation-invariant because its coefficients sum to zero. No coefficient
permutation, sign variant, affine intercept, lag, eye-component order, or
per-panel equation is admitted.

## Fixed streams

Convert the accepted eyes to orthodox ranks `0..82`, remove the first marker,
and remove only the already established copied openings:

```text
row 1  east1, west1, east2   trim 24   lengths 74,78,93   score first 74
row 2  west2, east3, west3   trim  5   lengths 96,131,118 score first 96
row 3  east4, west4, east5   trim 20   lengths 98,99,93   score first 93
```

Each row is truncated to its shortest remaining panel. The real score is the
number of its aligned positions satisfying the equation. The single primary
statistic is the sum over all three rows, covering 263 positions. Per-row
scores are diagnostics and do not select a variant.

## Exact cyclic-alignment null

For a row of common length `L`, preserve the complete truncated sequence in
each panel. Hold column zero at offset zero and exhaust all `L²` relative
circular offsets of columns one and two. Holding the first offset is lossless:
a simultaneous rotation of all three length-`L` circles does not change the
full-cycle score.

This exact null preserves:

- every panel's symbol multiset;
- every panel's circular transition order;
- the natural row membership and column identity;
- modulus, coefficients, trims, and scored length.

It destroys only the observed cross-panel alignment. Construct one exact
score histogram per row, then convolve the three histograms. The total null
therefore represents every independent relative alignment across the rows,
with total mass:

```text
74² * 96² * 93²
```

Report the inclusive exact upper tail of the real total. There is no
Monte-Carlo seed and no within-family reselection.

## Calibration

A synthetic fixture must construct column zero from arbitrary columns one and
two using:

```text
column0 = inverse(3) * (8*column2 - 5*column1) mod 83
```

The implementation must recover a perfect score at real offsets. Tests must
also verify:

- the three real scored lengths;
- exact histogram mass `L²`;
- simultaneous-rotation invariance;
- exact convolution mass.

## Promotion and stop

Promote this one linear body interface only if its exact inclusive tail is
below `.01`. A positive result earns a separately frozen held-out field or
decoder test; it does not establish plaintext.

Otherwise close direct `3,5,8` weighted alignment. Do not rescue it with
coefficient permutations, other signs, offsets, raw-eye arithmetic, fitted
intercepts, or selected panels. The marker country-tag result remains intact.

No weighted body score was inspected before this freeze.
