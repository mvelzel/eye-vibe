# Practice cipher 3 — affine GAK results

## Result

The finite structured affine group-autokey lane is negative. The exact
arbitrary-update lane remains unresolved because every real 42-state query
times out even on group A. The two outcomes are deliberately kept separate.

No plaintext was recovered.

## Controls

Both frozen controls pass before real scoring.

The structured fixture encrypts eighteen reset streams from all 42 planted
action symbols with:

```text
mode = indicator-both
u(t) = 2^t mod 83
```

The complete 35,675-candidate catalog retains the true family among its
A-minimizers and transfers it to B/C with no more than 42 decoded values.

A separate arbitrary-update fixture uses four action states. The exact solver
returns `SAT` at the planted four-state bound, its model re-encrypts the entire
ciphertext exactly, and all five first-symbol conventions pass direct
encrypt/decode round trips.

These controls validate the equations and finite search. They do not imply
that the exact encoding can decide the much larger real instance within its
time bound.

## Structured catalog

The frozen catalog contains:

```text
5 first-symbol modes
6,889 affine-linear functions per mode
82 exponential-base functions per mode
81 power-exponent functions per mode
83 reciprocal-shift functions per mode
35,675 candidates total
```

Only 2,291 candidates remain valid on every A event; the rest produce a zero
multiplier. None of the valid candidates decodes A to 42 or fewer values.

The unique A-selected winner is:

```text
mode        skip
function    u(t) = 70*t + 60 mod 83
A values    75
A IoC       1.016215981
```

It encounters a zero multiplier on B/C, so the heldout decode is invalid.
Because the training minimum is already 75, this is not a near miss. The four
structured function families are closed in the five standard-coordinate
first-symbol modes.

## Exact arbitrary update

The exact model gives each realized nonzero plaintext action one arbitrary
global update multiplier and asks whether all decoded states fit in at most
42 labels.

With a ten-second bound, every group-A query returns:

```text
full                unknown: timeout
primer              unknown: timeout
skip                unknown: timeout
indicator-hidden    unknown: timeout
indicator-both      unknown: timeout
```

As a diagnostic, all eighteen messages were also queried at the unconstrained
82-state ceiling. All five modes again time out. This means the present solver
formulation is not decisive on the real corpus; it is not evidence for or
against a 42-state model.

The frozen stop rule applies. There is no structured survivor or group-level
exact result to justify deeper blind solver tuning. The arbitrary-update
family remains open and explicitly marked `unknown`, not rejected.

## Scope

Closed:

- standard-coordinate `AGL(1,83)` GAK with global `u(t)=r*t+s`;
- the same machine with `u(t)=g^t`, `u(t)=t^k`, or `u(t)=1/(t+s)`;
- all five frozen first-symbol conventions for those structured functions.

Open:

- an arbitrary global nonzero update function at the 42-action boundary;
- a hidden permutation of the displayed 83 coordinates;
- non-affine deck actions and higher-order state;
- the exact `83=2*42-1` two-sheet architecture.

## Method transfer

- A hidden state can make visible linear complexity look random, so test the
  state equations rather than only ciphertext recurrence.
- Select global update rules on one split and allow invalid heldout updates to
  count as failure; do not add zero exceptions after transfer.
- A passing small SAT fixture validates equations, not real-instance
  tractability. Report timeout separately from finite-family failure.
- Construction genealogy is useful for choosing a bounded family, but the
  family still needs a prediction gate. Here authorship motivated the test;
  it did not rescue the 75-symbol training minimum.
