# Giant-dollar mirror-width audit — 22 July 2026

## Result

The recent Discord observation contains a real authored near-symmetry, but the
reported `23rd` exceptional row is not selected by the raw-width rule alone.
Starting from the PNG alpha mask, the two centre-outward opaque-width traces
agree under reversal everywhere in a 60-row containing interval except one
pair:

```text
left y=34: 11 pixels
right y=35: 12 pixels
```

This is worth retaining as construction-language evidence. It does not yet
connect the dollar to an Eye operation, and a particular 43-row crop must be
specified independently before its one-based mismatch position can be treated
as a parameter.

## Raw asset and chronology

The audited file is Noita's boss-centipede reward asset:

```text
entities/animals/boss_centipede/rewards/giant_dollar.png
dimensions          41 x 75 RGBA
SHA-256             0bc8284f0b915d73e350343faa4be2ff3d36f4e73e0edea59267a3d55a69e9c1
opaque pixels       1,311
transparent pixels  1,764
```

The copy in the available archived early-access tree and the copy in the
current extracted data are byte-identical. A Noita Discord message from 30
September 2019 also describes a giant golden dollar-sign reward. Unlike the
Gate Guardian, the dollar therefore clearly predates the October 2020 Eye
release and is eligible both as an original construction hint and as a later
decoder clue. Chronological eligibility is not evidence of an intended link.

## Independently frozen measurement

The alpha mask has exactly three columns opaque on all 75 rows:

```text
x = 19, 20, 21
```

These objectively define the vertical stem. For every row, the audit counts
the contiguous opaque run from `x=19` leftward and from `x=21` rightward. This
uses no palette choice, tracing tolerance, fitted curve, or Eye number.

The reported Discord fact can be reproduced by comparing the 43 left rows
`12..54` with right rows `57..15` in reverse order. Exactly 42 rows agree. The
only mismatch has zero-based index 22, hence it is the 23rd scanline, with
widths `11|12`.

That compact reproduction is not the whole selection audit. A 75-row sequence
contains 33 possible 43-row windows. Exhausting both starts and both right-side
orientations gives:

```text
33 * 33 * 2 = 2,178 alignments
best equality              42 / 43
best absolute error        1 pixel
number of best alignments  18
```

All 18 best alignments use the same physical reflection, `left_y + right_y =
69`, and contain the same single `11|12` defect. Their crop starts are:

```text
left 5, right 22  -> mismatch is scanline 30
left 6, right 21  -> mismatch is scanline 29
...
left 12, right 15 -> mismatch is scanline 23
...
left 22, right 5  -> mismatch is scanline 13
```

The shared geometry is even clearer without forcing length 43: left rows
`5..64` against reversed right rows `5..64` agree on 59 of 60 rows, again with
only `11|12`. Thus `42/43` is a true subwindow of a larger near-symmetry. The
choice that calls the defect row 23 may still be objective if “void,” “divider,”
and the triangle rotation uniquely define that crop, but those masks and
coordinates were not given in the message and are not implied by centre-run
widths alone.

## What this does and does not promote

Promoted:

- the sprite deliberately or accidentally contains a very clean reflected
  centre-run relation with one one-pixel raster defect;
- mirror, reverse, compare, and symmetric-difference operations remain
  plausible Noita construction vocabulary;
- the asset is old enough that chronology cannot reject it.

Not promoted:

- `11`, `12`, `23`, `42`, or `43` as Eye keys;
- the claim that the dollar instructs a Gate Guardian sieve;
- the separate 13-pixel residual, whose curve/fold mask has not yet been
  reconstructed from a frozen rule;
- the Discord claim that each transformed void has possible widths
  `23,22,...,1`; centre-outward raw opaque runs max out below 23, so that claim
  necessarily uses a different geometric construction.

The correct next test is to obtain or independently formalize the two void
masks, divider, triangle rotation, and difference-row partition without using
the desired Eye/Gate values. If that full pipeline predicts an uninspected
asset quantity or one of the unresolved Type6 values, the clue promotes. If
the masks remain movable, the result stays visual corroboration rather than a
decoder.

## Reproduction

```bash
PYTHONPATH=src python3 scripts/analyze_giant_dollar.py \
  --image /path/to/current/giant_dollar.png \
  --early-image /path/to/early-access/giant_dollar.png
```

The reusable implementation is in `src/eye_mystery/giant_dollar.py`; unit and
raw-asset regression tests are in `tests/test_giant_dollar.py`.
