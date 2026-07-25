# Thirty-second pass — synchronizing-bridge freeze

## Question

Do the three established clean gap-11 returns begin a label-invariant machine
trace that predicts the independently known late isomorphism boundary?

This is a state/conformance test, not a plaintext or numeric-value test.

## Independently fixed boundaries

For each final message:

1. remove neither marker nor copied opening when reporting full-array
   coordinates;
2. take the endpoint of its unique clean gap-11 repeat as the reset boundary;
3. take its already published late-context entry as the next phase boundary.

The resulting half-open bridges are:

```text
message  repeat endpoint  late entry  bridge
E4       48               68          [48,68), length 20
W4       50               71          [50,71), length 21
E5       49               69          [49,69), length 20
```

Late entries come unchanged from the registered contexts:

```text
last-west4: E4[68:98]  <-> W4[71:101]
last-east5: E4[68:98]  <-> E5[69:99]
```

The repeat endpoints, copied-opening frame, and late contexts all predate this
test. No boundary may be shifted to improve a score.

## Inspected observation

Canonicalize each bridge by replacing every label with its first-occurrence
number. All three signatures have a common prefix of length 17:

```text
0,1,2,3,4,5,6,7,8,9,10,4,11,3,6,12,13
```

The two East-Q bridges, E4 and E5, have the same complete length-20
signature:

```text
0,1,2,3,4,5,6,7,8,9,10,4,11,3,6,12,13,4,14,15
```

Their induced partial bijection is valid through all 20 bridge positions. The
first pair at the late entry conflicts with that old map, while the separately
registered 30-symbol late context beginning there is itself a valid partial
bijection. W4 agrees with the common bridge signature through position 16 and
first conflicts at position 17.

These facts were inspected before this freeze. The audit measures their
conditional specificity and cannot turn them into prospective discovery
p-values.

## Primary statistics

Using only equality signatures:

1. `triple_lcp`: longest common prefix of the three bridge signatures;
2. `east_complete`: whether E4 and E5 have identical complete bridge
   signatures;
3. `east_switch`: whether their complete bridge induces a valid partial
   bijection and adding the first late-entry pair causes the first conflict;
4. `joint`: `triple_lcp >= 17`, `east_complete`, and `east_switch`.

The East pair is primary because East/West is an independently established
factoradic header class, not a pair selected from the bridge values.

## Matched local control

Generate 50,000 independent controls. For each bridge:

- keep its first symbol—the gap-11 return endpoint—fixed;
- uniformly shuffle the remaining bridge multiset subject to no adjacent
  double;
- leave the loop, late context, and every symbol outside the bridge unchanged;
- reject the shuffle if either bridge boundary creates an adjacent double;
- reject it unless the original unique clean gap-11 anchor remains the only
  gap-11 anchor at its fixed position and value.

This preserves:

- complete body lengths and multisets;
- all three exact gap-11 loops and endpoints;
- the header-selected anchor positions and values;
- the no-adjacent-double rule;
- both published late contexts;
- every fact used to choose the bridge boundaries.

It breaks only the proposed reset-to-next-phase trace.

For each control report inclusive plus-one tails for all four primary
statistics. Joint selection is evaluated as one event, not by multiplying
dependent tails.

## Incremental W4 control

Condition on the complete observed E4/E5 bridge and its boundary switch.
Shuffle only W4 under the same constraints and count controls whose three-way
common-prefix length is at least 17.

This asks how much new information W4 contributes after the East relation is
taken as given. It is the most conservative state-trace statistic.

## Broad boundary/pair correction

In every control and the observation, additionally search:

- all three choices of the same-length/truncated bridge pair;
- endpoint included versus excluded;
- late-entry symbol excluded versus included.

Keep the fixed coordinates and forward direction. No position shift,
reversal, label arithmetic, or alternate late context is admitted.

Report:

- the maximum three-way common-prefix length over the four boundary
  conventions;
- whether any pair has a complete equality-signature match under a convention;
- whether any convention has both a pair match and the observed-or-larger
  three-way prefix.

This broad statistic charges the visible slicing and pair choices. It does not
charge every state-machine idea tried elsewhere in the project.

## Positive and negative controls

The detector must:

1. recover a synthetic three-bridge plant with a 17-symbol shared skeleton,
   a complete typed pair, and a first-symbol boundary conflict;
2. reject the same plant after one held-out equality is changed;
3. reproduce the fixed bridge coordinates from the canonical corpus rather
   than hard-coding the observed signatures;
4. verify that the published late contexts remain partial bijections.

## Interpretation gate

Promote a synchronizing/change-point record only if:

- the joint matched-control tail is below `.01`;
- the W4-conditioned tail is below `.01`;
- the broad boundary/pair tail is below `.01`;
- the positive control passes.

Even if all gates pass, the result establishes a designed equality-state
trace, not a plaintext, state alphabet, or transition rule.

Only after scoring may the observed common length `17` be compared with
Veska's independently measured `9+8=17`. Because the bridge test was
Gate-motivated and the comparison is retrospective, that match is
corroboration rather than an independent probability.

