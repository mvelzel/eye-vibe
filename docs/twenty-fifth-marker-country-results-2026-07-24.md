# Twenty-fifth result — the marker country tag

## Outcome

The frozen conditional audit is positive as a **marker-layer discriminator**,
not as a body-cipher solution.

In canonical engine order, the third digits of the nine header trigrams form:

```text
0 0 1
1 3 4
2 2 3
```

The natural column sums are exactly `(3,5,8)`. On the same fixed coordinates,
the already established East-5-first edge trail and primary-row-zero BWT route
decodes the nine digits to `!Fi`.

Of 12,096 assignments that keep the first two base-five coordinates fixed and
give nine distinct ranks in `0..82`, only the observed assignment has both
readings. The result survives the two frozen broadenings: case-insensitive
`Fi` and all D4 views of the square.

This conjunction also resolves the one ambiguity in the previously published
factoradic-header filter. That unchanged filter has two survivors. The
observed survivor has column sums `(3,5,8)` and BWT text `!Fi`; the other has
column sums `(4,4,8)`, no D4 `358` view, and no valid single-cycle BWT text.

## Frozen universe

Only the observed third-digit multiset `001122334` was reassigned. The
following remained fixed:

- each message's first two header digits;
- canonical 3×3 engine placement;
- the unique marker-successor trail, beginning at East 5;
- BWT primary row zero and stable LF convention;
- orthodox base-five trigrams and the `0..82` range;
- the complete newline-type, P/D4, Q/S5, and coset factoradic predicate.

No body symbol, language model, source text, or game asset entered the audit.

## Exact counts

The range and distinctness filters reproduce the earlier factoradic audit:

| Stage | Count |
|---|---:|
| distinct multiset assignments | 22,680 |
| all reconstructed ranks in `0..82` | 15,120 |
| nine distinct reconstructed ranks | **12,096** |

All remaining counts use that 12,096-assignment universe:

| Event | Count |
|---|---:|
| natural ordered column sums `(3,5,8)` | 224 |
| `(3,5,8)` in any D4 view | 855 |
| fixed-trail BWT has one LF cycle | 1,137 |
| one cycle and all three decoded values in `0..82` | 404 |
| valid BWT text with case-insensitive `Fi` suffix | 2 |
| exact BWT text `!Fi` | 1 |
| natural `358` and case-insensitive `Fi` | **1** |
| natural `358` and exact `!Fi` | **1** |
| D4-broadened `358` and case-insensitive `Fi` | **1** |
| D4-broadened `358` and exact `!Fi` | **1** |

The only other case-insensitive suffix is:

```text
assignment   100134223
column sums  4,5,7
BWT text     %Fi
factoradic   false
```

Thus the broadened text event does not introduce another country-code
candidate.

## Factoradic ambiguity

Applying the old predicate without adding `358` leaves:

| Assignment | Column sums | D4 `358` | BWT text |
|---|---|---:|---|
| `001134223` | `3,5,8` | yes | `!Fi` |
| `001234213` | `4,4,8` | no | invalid/non-single-cycle |

The alternatives differ by the known West2/West4 duplicate-edge scalar swap.
The country-code layout therefore chooses the actual authored scalar
assignment rather than merely its graph-isomorphism class.

## Interpretation boundary

This is stronger than two isolated curiosities:

1. `!Fi` uses an edge-trail/BWT reading.
2. `+358` uses the canonical spatial columns.
3. The second reading resolves a pre-existing two-survivor ambiguity under a
   predicate defined before `358` was noticed.

But it is not a clean probability claim. Both readings reuse the same nine
digits, and `358` was discovered retrospectively. The 224 and 855 counts are
descriptive conditional counts, not corrected tails over every recognizable
number, country code, text token, grid statistic, and rendering that could
have been tried. Their probabilities must not be multiplied by the earlier
BWT counts.

The defensible promotion is narrow:

> The first trigrams very likely carry designed, self-checking metadata, and
> their payload is consistent with a Finland/Finnish tag.

This does not prove Finnish plaintext, validate any proposed body decoder, or
make `FI358` an admissible key without a separate construction rule.
`3,5,8` as a Fibonacci fragment remains a semantic rival in isolation, but
the full `+358` country-code reading explains `Fi` directly.

## Next consequence

Return to the breadth portfolio rather than treating the tag as plaintext.
The best next body-facing discriminators are:

1. test whether the row-one zero circulation and row-two residue seven predict
   a body-map holonomy already present in equality-derived context maps;
2. test whether the final marker row supplies that seven as a fixed syndrome;
3. only if an independent consumer appears, compare Finnish and English
   scoring on held-out output or admit `FI358` as key material.

Implementation:

- `src/eye_mystery/marker_country.py`
- `scripts/audit_marker_country_tag.py`
- `tests/test_marker_country.py`

The preregistration is
[`twenty-fifth-wide-marker-country-horizon-2026-07-24.md`](twenty-fifth-wide-marker-country-horizon-2026-07-24.md).
