# Twenty-seventh result — a unique generic locale checksum

## Outcome

The observed marker assignment is the sole generic calling-code/BWT-region
match in the frozen 12,096-assignment universe.

The rule does not name Finland in advance:

1. sum the third-digit grid's natural columns as three decimal digits;
2. require an assigned geographic calling code;
3. decode the same digits through the fixed marker trail/BWT route;
4. require the BWT's two-letter suffix to be one of that calling code's
   assigned regions.

Only the observed assignment passes:

```text
assignment    001134223
column sums   3,5,8
calling code  +358
regions       FI, AX
BWT text      !Fi
factoradic    yes
```

It remains the only match when all D4 grid views are admitted. It is also the
only matching survivor of the unchanged full factoradic predicate.

This strongly corroborates a self-checking locale field in the marker layer.
It remains descriptive rather than a discovery p-value because the generic
rule was formulated after seeing `+358` and `!Fi`.

## Three coordinate planes

The complete observed header grid has:

| Eye coordinate | Canonical column sums | Calling code | Regions |
|---|---:|---:|---|
| first | `6,8,3` | `+683` | `NU` (Niue) |
| middle | `0,3,4` | `+34` | `ES` (Spain) |
| third/scalar | `3,5,8` | `+358` | `FI`, `AX` (Finland, Åland) |

The first two planes are already fixed graph coordinates. Their country-code
readings were noticed retrospectively and have no independently calibrated
text match. The third plane is different: it is the reassigned scalar/payload
plane, and its fixed BWT suffix selects `FI` from the two regions sharing
`+358`.

## Exact conditional counts

The audit reproduces the earlier universe:

| Stage | Count |
|---|---:|
| multiset assignments | 22,680 |
| reconstructed ranks all in `0..82` | 15,120 |
| nine distinct ranks | **12,096** |

Within the 12,096 admissible assignments:

| Event | Count |
|---|---:|
| natural view is an assigned geographic calling code | 1,282 |
| some D4 view is an assigned geographic calling code | 3,914 |
| valid BWT text has a two-letter ASCII suffix | 173 |
| natural code's region matches BWT suffix | **1** |
| natural semantic match also begins `!` | **1** |
| D4 code's region matches BWT suffix | **1** |
| D4 semantic match also begins `!` | **1** |

The old factoradic predicate remains untouched:

| Event | Count |
|---|---:|
| full factoradic survivors | 2 |
| factoradic plus natural semantic match | **1** |
| factoradic plus D4 semantic match | **1** |

No alternative country, region, punctuation, assignment, or D4 orientation
survives the generic relation.

## Data and verification

The calling-code map is an exact 215-entry transcription of Google's generated
libphonenumber map at commit:

```text
f7e3e88c92b905c8d6edb81f336dbe25edc05b52
```

The downloaded upstream Java file used for byte-for-byte map comparison had
SHA-256:

```text
ab2f17e0ba1d5105fbfa7c1039ae0bafe1a6b22c22fdbe85df3ab0a62ba2c517
```

The local map compares equal on all 215 entries. Region `001` is excluded as
non-geographic. Tests cover padded `034 -> 34`, multi-region `358 -> FI,AX`,
sum overflow, case folding, and a D4-only fixture.

A read-only server-wide Discord search found no relevant prior discussion of
`683` or Niue; the numerical hits were unrelated. No messages or reactions
were sent.

## Interpretation boundary

This result upgrades the narrow interpretation:

> The first trigrams behave like a deliberately redundant metadata header,
> and the scalar payload identifies locale/region `FI`.

It does **not** establish:

- that every body character decrypts to Finnish;
- that `FI`, `358`, `NU`, or `ES` is a cipher key;
- that the first/middle plane country codes are intentionally semantic;
- a calibrated probability over every post-hoc cultural database or parser;
- any body decoder.

The body-weight test is independently negative, so the country code should not
be pushed into arithmetic without a new authored consumer.

## Best next use

Promote `FI` as a metadata constraint, not as free key material. The cleanest
next steps are:

1. search game assets/version history for an authored locale/header interface
   that couples two-letter region tags to Eye-like three-column arithmetic;
2. prefer Finnish over English only after a decoder is recovered without
   language selection;
3. revisit source/token hypotheses only when they can predict an untouched
   equality or exact re-encryption;
4. continue unresolved practice cipher #4 for a transferable nonlinear
   state-machine operation.

Implementation:

- `src/eye_mystery/calling_codes.py`
- `src/eye_mystery/locale_checksum.py`
- `scripts/audit_three_plane_locale.py`
- `tests/test_locale_checksum.py`

Protocol:
[`twenty-seventh-three-plane-locale-freeze-2026-07-24.md`](twenty-seventh-three-plane-locale-freeze-2026-07-24.md).
