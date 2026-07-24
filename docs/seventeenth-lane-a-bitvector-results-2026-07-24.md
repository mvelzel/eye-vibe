# Seventeenth horizon lane A — bit-vector geometry results

## Result

The new exact encoding is valid and substantially faster on every individual
context, but it does not decide any of the three joint lag-one instances
within the frozen 60-second bounds.

Adjacent-only hidden geometry remains open. There is no wheel and no `UNSAT`
claim.

## Encoding

The already frozen model is unchanged:

```text
z[b]-z[a] = ±(z[d]-z[c]) mod 83
all observed z labels are distinct
```

The new formulation uses:

- seven-bit coordinates constrained to `0..82`;
- one six-bit magnitude `1..41` for each of the 44 transitive edge classes;
- explicit unsigned conditional add/subtract for exact mod-83 wrap;
- one `Distinct` constraint over all touched labels;
- the same translation/scaling normalization `z[a]=0, z[b]=1`.

It adds no lag, plaintext, ordering, or fitted distance class.

## Controls

All frozen gates pass:

- a planted satisfiable instance returns `SAT`;
- an equidistant triangle over `F5` returns `UNSAT`, agreeing with the integer
  solver;
- all five modular first/last wrap cases exercised by the plant replay;
- every one of the seven Eye contexts is `SAT` separately;
- the complete hidden-geometry test file passes seven tests in 1.802 seconds.

The individual-context result agrees with the prior exact integer formulation
while being fast enough to serve as an independent encoding check.

## Joint results

```text
family       constraints  labels  result                 elapsed
first        59           45      unknown: timeout       60.029 s
last         82           62      unknown: timeout       60.032 s
all seven    141          71      unknown: timeout       60.045 s
```

The three results reproduce across fresh processes. No partial model is
interpreted.

## Decision

Per the precommitted stop rule, Lane A remains unresolved and does not receive
more blind solver budget. A custom cycle-space sign propagator is retained as
a future exact method only if another lane supplies a useful state bound,
class identification, or symmetry break.

The seventeenth horizon now moves laterally to:

1. Lane E, the parameter-free directed equitable/fibration quotient;
2. Lane C, predictive Hankel rank with panel-heldout controls.

Neither lane may borrow a fitted wheel from this timeout.
