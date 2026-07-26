# Forty-third pass — cross-panel numeric-carrier freeze

## Question

Can the two other synchronized final panels supply the numeric information
missing from an equality-only allocator?

The common late phase gives 25 aligned class records:

```text
class -> (E4 rank, W4 rank, E5 rank)
```

This differs from the earlier aligned-column polynomial-share test: records
are joined by independently established equality class, not raw body
position.

## Holdouts

Fit on 23 classes and withhold:

- class10: the rightward middle-eye control that reappears at boundary34;
- class24: the independently selected `7+17` phase-overlap target, first
  appearing at position28.

Both target ranks are hidden during fitting. Source-panel ranks remain
available because this pass asks whether the other panels are the carrier.

## Family A — mod-83 affine records

For each target panel, exhaust

```text
target = a*source1 + b*source2 + c              mod 83
target = a*source1 + b*source2 + d*class + c    mod 83
```

with all coefficients. Count the complete model family, maximum training
matches, co-best models, and co-best holdout predictions.

## Family B — shared base-5 eye arithmetic

Decode each rank as three base-5 eye digits. Exhaust:

- all six eye orders independently in both sources and the target;
- shared coefficients `a,b` in `0..4`;
- one fixed offset per output eye.

For each output eye:

```text
target_eye = a*source1_eye + b*source2_eye + offset_eye mod 5
```

The same coefficients serve all three eyes and all classes. The family has
`6^3 * 5^5 = 675,000` models per target.

## Promotion gate

A carrier promotes only if a frozen model reproduces all 23 training classes
and predicts both held-out target ranks. Partial fits do not promote, no
matter how suggestive their coefficients look.

