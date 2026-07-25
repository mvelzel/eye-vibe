# Thirty-sixth pass — phase-marker closure freeze

## Question

Does the later Gate `+3` operation close the previously missing self field of
the final-to-first-row marker transfer through independently measured phase
lengths?

The earlier audit established:

```text
final row +3: 27,77,33 -> 30,80,36
row 1:                       50,80,36
```

It treated `30` only as an absent marker. The final state trace independently
supplies:

```text
E4 old bridge length          20
late three-panel phase length 30
```

The inspected closure is therefore:

```text
27+3       = 30
20+30      = 50
77+3       = 80
33+3       = 36
```

Equivalently:

```text
shift(final row)              = (30,80,36)
repair self by E4 bridge 20   = (50,80,36)
                              = row 1
```

This observation was made before this freeze. All counts are conditional
specificity measures, not prospective discovery p-values.

## Fixed inputs

Freeze:

- orthodox marker ranks and natural row order;
- the already established final record roles:
  E4 self, W4/E5 non-self;
- exact externally supplied Gate operator `+3`;
- final bridge endpoints derived from the unique gap-11 anchors;
- late entries derived from the published final aligned contexts;
- equality signatures, not numeric labels, for measuring phase length;
- the existing 12,096 graph-conditioned scalar-assignment universe.

Derive rather than enter as target constants:

- E4 bridge length from its anchor endpoint to late entry;
- late phase length as the maximal common prefix of the three independently
  canonicalized late equality signatures;
- all marker values from each conditional assignment.

No plaintext, language score, body-value arithmetic, alternative shift, or
movable phase boundary enters the primary test.

## Primary staged statistics

For every conditional marker assignment, count:

1. `nonself`: the two aligned relations
   `W4+3=W1` and `E5+3=E2`;
2. `self_to_phase`: `nonself` plus
   `E4+3=late_phase_length`;
3. `full_closure`: `self_to_phase` plus
   `E1=E4_bridge_length+late_phase_length`.

Report the incremental fractions:

```text
P(self_to_phase | nonself)
P(full_closure | self_to_phase)
P(full_closure | nonself)
```

Do not multiply these as independent evidence.

Also report which of the two previously surviving full factoradic scalar
assignments satisfies the closure.

## Broad correction

The primary roles were already established, but disclose flexibility with two
broadened events while keeping `+3` and the measured body lengths fixed.

### Natural-position broad event

Allow:

- any ordered pair of distinct marker rows;
- any one of the three aligned positions as the repaired self slot;
- either distinct observed bridge length, `20` or `21`.

For ordinary positions require `target_i=source_i+3`. For the selected self
position require:

```text
source_i+3 = late_phase_length
target_i   = late_phase_length + bridge_length
```

### Permuted-target broad event

Additionally allow any permutation of the three target positions. This is the
broadest reported conditional event.

As a diagnostic on the observed grid, scan all nonzero shifts `1..82` under
both broad families. This does not replace the primary test because `+3` was
selected by independent later assets.

## Phase-extension holdout

Do not use the post-30 suffix or its equality relations in fitting the
closure. After the primary audit, inspect it only as a separate consequence:

- measure every final-panel pair's maximal late equality-prefix length;
- report whether the unique extension boundary is itself a marker;
- enumerate all marker matches among the fixed pair lengths.

This boundary was inspected during mechanism discovery and is retrospective,
not a prospective prediction.

## Calibration and promotion gate

Tests must recover:

- bridge lengths `(20,21,20)`;
- late triple phase length `30`;
- exact repaired vector `(50,80,36)`;
- a synthetic marker grid with a planted closure;
- failure after perturbing any one required target.

Promote a complete construction record only if:

- the fixed full closure is rare in the conditional universe;
- the broadened counts are reported;
- the relation selects at most one existing factoradic survivor;
- the phase extension supplies a coherent fixed boundary rather than a
  movable best fit.

Even a positive result remains header/state-machine structure. It does not
decode the body or validate the Gate dossier's Type4/Type6 allocator.
