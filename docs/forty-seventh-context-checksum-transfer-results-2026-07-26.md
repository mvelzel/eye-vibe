# Forty-seventh pass — registered-context checksum transfer results

## Outcome

Reject direct transfer of the final `(right scalar,left scalar)` checksum rule
to the other registered nonliteral contexts.

The `last-east5` calibration remains exact:

```text
ordered context       E4 -> E5
header scalars        left2, right3
predicted checks      3,2
observed checks       3,2
```

Across all six frozen external contexts:

```text
testable contexts     3/6
tested fields         4
matching fields       0/4
complete records      0
sign-reversed fields  0/4
```

The final branch record is therefore local typed evidence, not a universal
post-isomorph checksum transducer.

## Positive control

A synthetic context with an 11-class common prefix and two closed records was
constructed so that:

```text
left scalar2, right scalar3
left-right checks 3,2
```

The extractor recovers both exact windows and both checks. The failure is not
caused by the closed-window scanner or field ordering.

## Complete transfer inventory

| Context | Registered / actual common | Prediction | Closed checks | Result |
|---|---:|---:|---:|---|
| `first-gap30` | `18 / 32` | `0,0` | none | untestable |
| `first-cross` | `18 / 23` | `1,0` | `2,81,51` | `0/2` |
| `first-cross-late` | `18 / 23` | `1,0` | `2` | `0/1` |
| `first-gap28` | `9 / 19` | `0,0` | none | untestable |
| `last-west4` | `30 / 34` | `2,2` | none | untestable |
| `last-east3` | `25 / 27` | `3,2` | `11` | `0/1` |

The actual common lengths exceed several originally registered lengths because
the older contexts were conservative certificates, not maximal scans. The
transfer begins only at actual divergence, so this cannot explain the
failure.

## Broad assignment and sign controls

For every testable context, all `9×9=81` ordered panel assignments were
allowed while the observed closed checks stayed fixed.

- Calibration `(3,2)` is compatible with `4/81` panel assignments.
- `first-cross` begins `(2,81)` and has `0/81` compatible assignments.
- `last-east3` begins `11` and has `0/81` compatible assignments.
- `first-cross-late` begins `2`, compatible with 18 assignments on its single
  field, but it misses its fixed prediction `1`.

Every header scalar lies in `0..4`, so checks `81` and `11` cannot be rescued
by choosing different panels. Reversing the sum direction matches none of the
four frozen fields.

## Interpretation

Retain:

- the final `last-east5` branch roles;
- header scalar 2 as source type and scalar 3 as target type;
- its reciprocal checks `(3,2)`;
- the first branch's exact base-five `+3` carry and Gate echo.

Close:

- applying that checksum order after arbitrary registered isomorph contexts;
- treating every equality reconvergence as the same record schema;
- repairing the rule by sign, panel reassignment, or nonmaximal context
  lengths.

The negative result sharpens the architecture: the checksum record depends on
the final row's loop/source/target topology, not merely on an aligned
isomorphic prefix. Another transfer would require an independently defined
context with the same typed loop topology; none of the six external contexts
has that interface.

## Reproduction

```bash
PYTHONPATH=src python scripts/audit_context_checksum_transfer.py
PYTHONPATH=src python -m unittest tests.test_context_checksum_transfer
```

Implementation:

- `src/eye_mystery/context_checksum_transfer.py`
- `tests/test_context_checksum_transfer.py`
- freeze:
  `docs/forty-seventh-context-checksum-transfer-freeze-2026-07-26.md`
