# Twenty-sixth result — `3,5,8` is not a direct linear body weight

## Outcome

The one frozen weighted interface is negative.

After removing markers and established copied openings, the fixed equation

```text
3 * column0 + 5 * column1 = 8 * column2  (mod 83)
```

holds at only four of 263 aligned body positions. The exact
relative-circular-alignment null has inclusive upper tail:

```text
171017439974 / 436487491584 = 0.391803759
```

This closes direct canonical `3,5,8` linear combination of the three panel
columns. It does not weaken the positive marker-layer `!Fi` / `+358` result.

## Exact row results

| Natural row | Length | Real | Null range | Inclusive upper tail |
|---|---:|---:|---:|---:|
| East1, West1, East2 | 74 | 2 | `0..6` | `1253/5476 = .228816654` |
| West2, East3, West3 | 96 | 1 | `0..7` | `6252/9216 = .678385417` |
| East4, West4, East5 | 93 | 1 | `0..6` | `5851/8649 = .676494392` |
| **Convolved total** | **263** | **4** | **`0..19`** | **`.391803759`** |

The real result is unexceptional both in total and in every row. Row one does
not provide a promising training excess, and neither later row supplies a
held-out surprise.

## Calibration and null verification

The implementation passes a deterministic plant built from:

```text
x0 = inverse(3) * (8*x2 - 5*x1) mod 83
```

and recovers every planted position. Simultaneously rotating all three plant
columns leaves the score unchanged.

The three exact row histogram masses are:

```text
74² = 5,476
96² = 9,216
93² = 8,649
```

Their convolution has exactly:

```text
74² * 96² * 93² = 436,487,491,584
```

controls. Each row null preserves the entire truncated panel circles and
exhausts both relative offsets, so no Monte-Carlo uncertainty or selected
variant is involved.

## Disposition

Per the frozen stop rule, do not try:

- coefficient permutations or alternative signs;
- affine intercepts or lags;
- raw-eye/component arithmetic;
- selecting one favorable row;
- nearby Fibonacci weights.

The defensible interpretation remains that `+358` is marker metadata. A body
consumer still requires an independently specified operation.

Implementation:

- `src/eye_mystery/weighted_alignment.py`
- `scripts/audit_358_weighted_alignment.py`
- `tests/test_weighted_alignment.py`

Protocol:
[`twenty-sixth-358-weighted-alignment-freeze-2026-07-24.md`](twenty-sixth-358-weighted-alignment-freeze-2026-07-24.md).
