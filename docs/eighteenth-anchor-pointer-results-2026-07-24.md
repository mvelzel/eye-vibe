# Final anchor record pointer/gauge follow-up — results

## Result

The pointer survives the preregistered broad matched control:

```text
broad corrected tail = 7/50001 = .000139997
```

This promotes the pointer as another field of the shared final-row record.
It is not an independent p-value to multiply with earlier anchor tests.

## Exact closure

E4's unique clean gap-11 repeat is:

```text
trimmed positions 16 -> 27
anchor value       75
```

The endpoint equals the E4 marker. Converting the endpoint from the trimmed
body to the full array adds the one marker and copied 20-symbol opening:

```text
27 = h_E4
27 + 1 + 20 = 48 = a_E5
```

Under E4 order `012`, the established slot rule is source minus remaining,
so component 2 is E5. The pointer fixes that anchor without choosing an
arbitrary additive seed. The three marker differences then reconstruct the
entire record:

```text
a_E5 = 48
a_E4 = a_E5 + h_E4       = 48 + 27 = 75 mod 83
a_W4 = a_E4 - h_W4       = 75 - 77 = 81 mod 83
h_E5 = a_W4 - a_E5       = 81 - 48 = 33 mod 83  (check)
```

The same exact witness is recovered from both the positive plant and the
real corpus:

```text
gap=11
carrier=E4
boundary=end
trimmed position=27
marker=27 with offset 0
anchor=48 with offset 21
```

## Controls

Across 50,000 new length-, multiset-, and no-double-preserving body shuffles:

```text
1747  have one clean gap-11 anchor in all three panels
   0  also reproduce the exact endpoint pointer
   0  reproduce the exact numeric slot rule
   0  reproduce both exact fields
   6  survive the fully broadened joint search
```

The exact pointer and joint corrected tails are both
`1/50001 = .0000199996`. More importantly, the broad family lets every
control:

- reselect any gap from 2 through 30;
- use any panel and the repeat start or endpoint;
- use any marker and any anchor;
- independently add offsets `0,1,20,21` for zero/one-based trimmed,
  post-opening, and full-array coordinates;
- proceed after any broadened anchor-difference match.

Six controls survive that full menu, giving the promoted corrected tail
`7/50001 = .000139997`.

## Consequence

The final row is now a closed self-describing record rather than a system of
differences needing one free gauge value. It contains:

```text
clean gap-11 equalities       select three anchor values
W4 order 021                  ranks their positions
target column 120             ranks their values
slots 0 and 2                 select source-minus-remaining
E4 endpoint/full-array frame  fixes a_E5 = 48
markers 27,77,33              reconstruct and check every anchor
```

This remains structural metadata, not plaintext. The most important open
semantic question is why the construction chooses base position 16, gap 11,
and the final row. The pointer makes the `11` repeat look more like a
synchronizing/addressing mechanism, but it does not yet prove that role.
