# Thirty-second pass — synchronizing-bridge results

## Result

The final-row gap-11 returns begin a designed, label-invariant, piecewise
state trace.

From the three repeat endpoints to the independently published late-context
entries:

```text
E4  [48,68)  length 20
W4  [50,71)  length 21
E5  [49,69)  length 20
```

all three equality signatures agree for exactly 17 positions. E4 and E5 then
remain equality-isomorphic for their complete 20-symbol bridges. At the next
aligned pair their old partial bijection conflicts, exactly where a different
known 30-symbol isomorphism begins.

Fifty thousand controls preserve the complete selectors and nuisances. None
reproduces any primary or broadened event. Every corrected tail is:

```text
1 / 50001 = .0000199996
```

This promotes a synchronizing/change-point record, not plaintext or a
recovered transition rule.

## Exact phase trace

The three bridge signatures begin:

```text
0,1,2,3,4,5,6,7,8,9,10,4,11,3,6,12,13
```

This is a 17-position trace with 14 first-seen classes and three repeat
events:

```text
position 11 repeats position 4
position 13 repeats position 3
position 14 repeats position 6
```

After that shared phase:

```text
E4/E5 suffix  4,14,15       = repeat,new,new
W4 suffix     14,15,16,8    = new,new,new,repeat
```

Thus the header-typed schedule is:

```text
gap-11 return
    -> common 17-position equality phase
    -> East-Q three-position suffix / West-Q four-position suffix
    -> new common 30-position equality phase
```

The late phase has one common signature across all three panels:

```text
0,1,2,3,4,5,6,7,8,5,9,10,11,12,13,14,15,16,0,17,
18,19,20,21,22,23,20,1,24,15
```

The two registered pair profiles both have 25 partial-bijection edges, five
validation positions, first validation at position 9, last new edge at
position 28, and no conflict.

## Boundary switch

For E4 versus E5, the old bridge map contains 16 edges and four validation
positions. It is valid through all 20 positions:

```text
first validation  11
last new edge     19
first conflict    none
```

Appending the first late-context pair produces the first conflict at exactly
position 20. Starting a fresh map at that same pair yields the known valid
30-symbol phase.

This is the key causal distinction: the late context is not merely adjacent
to another pattern-similar window. Its first symbol is an objective
partial-bijection change point selected by the gap-return bridge.

W4 contributes independent information. Its bridge follows the same equality
signature through position 16 and first departs at position 17. Conditioning
on the complete observed East bridge and switch, no W4-only control reaches a
17-symbol common prefix.

## Matched controls

Each control:

- fixes the gap-11 endpoint;
- shuffles only the rest of each bridge;
- preserves the exact bridge and body multisets;
- preserves the complete loop and all late-context symbols;
- preserves the no-adjacent-double rule, including both bridge boundaries;
- rejects any shuffle that loses or duplicates the unique fixed gap-11
  anchor.

Measured exceedances:

| Statistic | Exceedances | Corrected tail |
|---|---:|---:|
| three-way prefix at least 17 | `0/50000` | `.0000199996` |
| complete E4/E5 bridge | `0/50000` | `.0000199996` |
| exact E4/E5 boundary switch | `0/50000` | `.0000199996` |
| primary joint event | `0/50000` | `.0000199996` |
| W4 prefix, conditioned on observed East phase | `0/50000` | `.0000199996` |
| broad maximum prefix | `0/50000` | `.0000199996` |
| any broad complete pair | `0/50000` | `.0000199996` |
| broad pair-plus-prefix joint | `0/50000` | `.0000199996` |

The broad comparison searches all three pair choices and the four
endpoint/entry inclusion conventions. It does not shift positions, reverse
streams, or inspect numeric labels.

The detector recovers a planted 17-position trace, typed complete pair, and
first-symbol map conflict. Breaking one held-out equality reduces the common
prefix to 11 and rejects the plant.

## Relation to Veska and the Gate dossier

Veska's independently measured upper/lower bands contain exactly `9+8=17`
authored pixels. The Eye bridge now supplies an independently executable
17-position state phase on the strongest final-row record.

This makes the Gate's `9|8=17` split more relevant than a bare numerical echo:
both objects describe a boundary between typed operation phases. However:

- the bridge lane was motivated by Gate/state-machine work;
- the `17` comparison was made after inspecting the Eye trace;
- the complete `12+43+9+8` Veska partition is still under-specified;
- no Gate mask assigns the 17 bridge positions to Type4/Type6 roles.

The match is construction-language corroboration, not an independent
probability and not validation of the dossier's cache allocator.

## Consequence

The body is no longer supported only as “possibly stateful.” At least one
region is a controlled conformance trace with:

1. a selected return/reset;
2. a shared equality-state phase;
3. a header-side-dependent transition suffix;
4. an exact map switch;
5. a second shared equality-state phase.

The next bounded problem is to explain the typed suffixes and predict an
unused exit or later equality. Numeric plaintext scoring remains premature.

## Reproduction

```text
PYTHONPATH=src python3 scripts/audit_synchronizing_bridge.py --controls 50000
PYTHONPATH=src python3 -m unittest tests.test_synchronizing_bridge
```

Implementation:

- `src/eye_mystery/synchronizing_bridge.py`
- `scripts/audit_synchronizing_bridge.py`
- `tests/test_synchronizing_bridge.py`

