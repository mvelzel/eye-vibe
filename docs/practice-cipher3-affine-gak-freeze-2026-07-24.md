# Practice cipher 3 — affine GAK batch freeze

## Motivation

The third wide batch excludes order-one/two recurrences in the visible
ciphertext. It does not exclude an affine deck state whose update depends on
the decoded plaintext action.

This is the most specific remaining construction-genealogy lead. The same
author's earlier practice puzzles use group-autokey/deck ideas, while Cipher 3
was described as “a bit more unique.” That makes a broader affine group action
worth one calibrated exact pass. Authorship is only the reason to test the
family; it is not evidence that the family is correct.

## Frozen machine

Work in `F83`. Write a hidden affine state as `(a,b)`, with `a != 0`, and its
visible coordinate as:

```text
x = b/a
```

Normalize each plaintext operation by its
translation-to-multiplier ratio `t`. Consecutive visible coordinates obey:

```text
t_i = (x_i - x_(i-1)) * a_(i-1)
a_i = u(t_i) * a_(i-1)
```

where the global update function `u` maps every realized nonzero plaintext
symbol to a nonzero field element. Cipher 3 has no adjacent ciphertext
doubles, so all decoded `t_i` are nonzero and discrete-log coordinates are
valid.

This batch tests the displayed `0..82` field coordinate only. An arbitrary
hidden permutation of the 83 labels is outside scope.

## First-symbol modes

All five pre-existing conventions are frozen:

| Mode | Previous visible coordinate | Initial hidden multiplier | Decoded body |
|---|---:|---:|---|
| `full` | `0` | `1` | complete stream |
| `primer` | first symbol | `1` | remainder |
| `skip` | `0` | `1` | remainder |
| `indicator-hidden` | `0` | first symbol | remainder |
| `indicator-both` | first symbol | first symbol | remainder |

A zero first symbol makes either indicator mode invalid for that stream; it
is not repaired to one.

## Lane A: finite structured update catalog

For each mode, exhaust exactly these global functions:

```text
u(t) = r*t+s                 r,s in F83
u(t) = g^t                   g in 1..82
u(t) = t^k                   k in 1..81
u(t) = 1/(t+s)               s in F83
```

A candidate is invalid if `u(t)=0` at a realized symbol. No exception value or
per-message parameter may be fitted.

Rank on group A by:

```text
(number of distinct decoded A symbols,
 negative A index of coincidence,
 mode order,
 family order,
 numeric parameters)
```

The selected candidate transfers unchanged to B and C. Report distinct counts
for A, B, C, and their union. Promotion requires at most 42 values in the
complete union. An English score may describe a survivor but may not select
one.

## Lane B: exact arbitrary-update boundary

For each first-symbol mode, encode the same equations in discrete-log
coordinates. The 82 possible nonzero plaintext symbols are state labels.
`u(t)` is one global arbitrary multiplier exponent per realized state.

Ask separately whether the decoded state union has cardinality at most 42 for:

```text
A
B
C
all eighteen streams
```

The all-stream query is the decisive model. Group queries diagnose whether a
timeout or contradiction appears only with transfer. Solver results are
reported as `SAT`, `UNSAT`, or `unknown: timeout`; neither timeout nor a poor
heuristic is an exclusion.

If `SAT`, print the complete decoded state streams and the realized update
table. A model is compatibility, not a solution: it promotes only if a
separate language/source invariant or exact re-encryption identifies the
plaintext labels.

## Positive controls

Before real scores:

1. encrypt reset streams from a known 42-symbol action alphabet with a catalog
   function and verify that Lane A retains the true family among the
   A-minimizers and transfers to at most 42 symbols on B/C;
2. encrypt streams with a known arbitrary nonzero update table and verify that
   Lane B returns `SAT` at the planted alphabet bound;
3. decode each planted model forward and require exact ciphertext replay.

Failed recovery invalidates the corresponding real result.

## Stop rules

- A Lane-A winner above 42 union symbols closes only the four structured
  function families in the five standard modes.
- Exact `UNSAT` for all five all-stream modes closes this standard-coordinate
  affine GAK family at the 42-symbol boundary.
- Exact `SAT` without readable/source-compatible plaintext records
  compatibility, not a solve.
- A timeout receives no deeper blind search unless group results or a
  structured survivor supplies a new invariant.
- No hidden label permutation, per-message `u`, zero-value exception,
  variable modulus, or language-fitted state merge may be added after seeing
  failure.

## Transfer value

If the family succeeds, it supplies a new attack method for the Eyes:
random-looking visible output can conceal a small action alphabet in an
evolving group state. If it fails exactly, the result is still valuable
because it separates author genealogy from mechanism and prevents a very
large arbitrary-update family from becoming an unfalsifiable Eye theory.
