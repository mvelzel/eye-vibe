# Hidden geometry from Eye isomorphs — results

## Outcome

The breadth pass produced one exact negative result and one genuinely open
subcase.

- **A shared hidden 83-cycle cannot preserve the short multi-step chord
  geometry of the nonliteral isomorphs.** The last family is inconsistent by
  cumulative lags 1–3 and even at lag 5 alone. The first family is inconsistent
  by cumulative lags 1–6.
- **Adjacent steps alone remain unresolved.** Each context separately has an
  exact wheel witness. The combined 141-equation instance did not return SAT
  or UNSAT under three bounded formulations, and no wheel is claimed.

This does not decode the messages. It also does not reject an adjacent-only
differential cipher: allowing every textual step to choose its orientation is
strictly weaker than a rigid context transformation, and the joint exact case
is computationally difficult.

## 1. Exact model

Assign every observed glyph label `a` a distinct coordinate `z[a]` in
`F83`. For an aligned source chord `(a,b)` and target chord `(c,d)`, require

```text
z[b] - z[a] = +(z[d] - z[c])  (mod 83)
```

or

```text
z[b] - z[a] = -(z[d] - z[c])  (mod 83).
```

This is exactly equality of unsigned circular distances. The sign is free for
every chord. Translation and multiplication by any nonzero field element
preserve all equations, so the implementation fixes one constrained edge to
coordinates `0,1`. This removes solver symmetry without assuming the authored
numeric label order.

At lag 1, the seven fixed contexts give:

```text
141 equality links
185 distinct undirected chord edges
44 transitive distance classes
71 observed labels
1 connected incidence component
115 graph cycles
```

No distance class has degree greater than two or contains a cycle, so the
cheap local obstruction “three same-length neighbors around one point” does
not apply.

## 2. Individual contexts pass

Every context is satisfiable at lag 1. More strongly, every context is
satisfiable when **all** within-window lags are imposed:

| context | all-lag equations | exact result |
|---|---:|---:|
| `first-gap30` | 153 | SAT |
| `first-cross` | 153 | SAT |
| `first-cross-late` | 153 | SAT |
| `first-gap28` | 36 | SAT |
| `last-west4` | 435 | SAT |
| `last-east5` | 435 | SAT |
| `last-east3` | 300 | SAT |

Thus no occurrence is intrinsically incompatible with an unknown wheel.
Every one can masquerade as a distance-preserving partial relabeling when
fitted alone. This makes a joint or held-out requirement essential.

## 3. Shared multi-lag geometry fails

When contexts must share one wheel:

| family | constraint set | equations | exact result |
|---|---|---:|---:|
| first four | all lags | 495 | UNSAT |
| last three | all lags | 1,170 | UNSAT |
| all seven | all lags | 1,665 | UNSAT |
| first four | cumulative lags 1–6 | 294 | UNSAT |
| last three | cumulative lags 1–3 | 237 | UNSAT |
| all seven | cumulative lags 1–3 | 402 | UNSAT |
| last three | lag 5 only | 70 | UNSAT |

The immediately preceding cumulative cases are not claimed SAT:

```text
first family, lags 1–5: UNKNOWN after 120 s
last family,  lags 1–2: UNKNOWN after 120 s
```

Therefore lags 6 and 3 are the first **proved** contradictions in the bounded
ladder, not proved mathematical minima. The lag-5-only result shows that the
failure is not solely an artifact of cumulatively recreating every pairwise
distance.

## 4. Eight-equation exact certificate

The last-family cumulative contradiction shrinks to eight equations involving
only `last-east5` and `last-east3`. `last-west4` is unnecessary.

| context | lag | index | forced chord equality |
|---|---:|---:|---|
| `last-east5` | 3 | 13 | `(42,40) ~ (20,21)` |
| `last-east5` | 1 | 16 | `(40,65) ~ (21,40)` |
| `last-east3` | 2 | 9 | `(49,40) ~ (79,20)` |
| `last-east3` | 3 | 9 | `(49,65) ~ (79,19)` |
| `last-east3` | 2 | 11 | `(40,79) ~ (20,64)` |
| `last-east3` | 1 | 12 | `(65,79) ~ (19,64)` |
| `last-east5` | 2 | 15 | `(33,65) ~ (62,40)` |
| `last-east5` | 2 | 13 | `(42,33) ~ (20,62)` |

The certificate no longer depends on an SMT solver:

1. Choose `+` or `-` for each equality: exactly `2^8 = 256` branches.
2. In each branch, the eight equations are homogeneous linear equations over
   `F83`.
3. Row-reduce them and test whether some vector `e_a-e_b` lies in the row
   space. If so, every solution forces `z[a]=z[b]`, contradicting distinct
   glyph coordinates.
4. All `256/256` branches force a collision. Twenty-three different label
   pairs serve as the first lexicographic witness; `(19,20)` witnesses 55
   branches.

The core is deletion-minimal. Removing each row leaves respectively

```text
3, 5, 8, 8, 8, 8, 2, 2
```

orientation branches with no forced collision. Those branches really admit
an injective assignment: the solution subspace is then not contained in any
of the `11 choose 2 = 55` coordinate-equality hyperplanes, and fewer than 83
proper hyperplanes cannot cover a vector space over `F83`.

This is a compact, dependency-free proof of the multi-lag rejection.

## 5. Adjacent-only case is still open

The lag-1 instance is not being relabeled as negative:

```text
every context separately          SAT in under one second
first family jointly              UNKNOWN after 60 s
last family jointly               UNKNOWN after 60 s
all seven jointly                 UNKNOWN after 60 s
```

Additional bounded diagnostics:

- a second, one-hot Boolean Z3 encoding timed out on representative dense
  pairs and on the joint case;
- an independent eight-worker CP-SAT feasibility model returned `UNKNOWN`
  after 300 seconds, after roughly 5.0 million branches and 2.0 million
  conflicts;
- CP-SAT maximization found 61/141 while retaining an upper bound of 141 after
  180 seconds;
- a permutation-preserving min-conflicts search found 65/141 after five
  100,000-step restarts;
- the class-pair local objective likewise failed its planted-recovery role.

None of those incomplete searches proves impossibility, and none found a
complete wheel. This subcase remains a legitimate future exact-CSP target,
but it does not justify decrypting under a fitted wheel.

## 6. Cryptanalytic interpretation

The result separates three hypotheses that had previously blurred together:

1. **Rigid context symmetry:** already inside the old hidden affine/dihedral
   family and rejected.
2. **Multi-step metric preservation:** now rejected by an eight-equation
   certificate.
3. **Adjacent-only differential preservation:** still undecided.

The third is the only surviving geometry route from this pass. It would mean
that repeated plaintext preserves each immediate motion class while longer
chords need not compose geometrically—more like a stateful differential
transducer than a literal wheel rotation. Any continuation should therefore
model the sequence of adjacent distance classes directly and demand
first-family/last-family prediction. Adding lag-2 geometry as an innocent
regularizer is no longer allowed: it changes the hypothesis into one already
contradicted.

## Reproduction

With the optional Z3 dependency available:

```bash
PYTHONPATH=src python scripts/run_hidden_geometry_ladder.py --mode summary
PYTHONPATH=src python -m unittest tests.test_hidden_geometry -v
```

The eight-row proof itself does not require Z3:

```bash
PYTHONPATH=src python -c \
  'from eye_mystery.hidden_geometry import linear_core_certificate; print(linear_core_certificate())'
```

The optional independent CP-SAT diagnostic is:

```bash
PYTHONPATH=src python scripts/run_hidden_geometry_cpsat.py --seconds 300
PYTHONPATH=src python scripts/run_hidden_geometry_cpsat.py --maximize --seconds 180
```

Definitions are in `src/eye_mystery/hidden_geometry.py`.
