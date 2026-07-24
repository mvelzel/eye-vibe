# Eighteenth focused lead — gap-anchor/header freeze

## Observation boundary

A read-only `silmä-novel` file search located Tuska's 22 July 2026
observation:

```text
first real isomorph anchors in E4,W4,E5: 75,81,48
headers:                               27,77,33

75 - 48 = 27 mod 83
75 - 81 = 77 mod 83
81 - 48 = 33 mod 83
```

This relationship was not present in the local ledger. The exact values have
now been seen, so all flexibility below is charged explicitly before running
controls.

## Structural selector

Use orthodox full-trigram values. Remove the first marker and the known
20-symbol copied opening from each of `east4,west4,east5`.

For gap `g`, a clean gap anchor at position `i` means:

```text
x[i] = x[i+g]
all g-1 interior values are distinct
no interior value equals x[i]
```

Its equality signature is one repeated endpoint and otherwise singletons. At
the reported `g=11`, each real stream has exactly one such post-opening
anchor. The full-array positions are `37,39,38`; the values are `75,81,48`.

## Registered statistics

The exact reported statistic is:

```text
(h_E4,h_W4,h_E5) =
(a_E4-a_E5, a_E4-a_W4, a_W4-a_E5) mod 83
```

It predicts the two nonreference anchors from the identity-header panel:

```text
a_W4 = a_E4 - h_W4
a_E5 = a_E4 - h_E4
```

The selection-corrected statistic is deliberately broader. Search every gap
`g=2..30` at which all three streams have exactly one clean anchor. For each
gap, allow all six orderings `(a,b,c)` of the three anchors. A broad match
occurs if the multiset:

```text
{a-b, a-c, b-c} mod 83
```

equals the header multiset `{27,77,33}` for any ordering. This absorbs the
retrospective choice of gap, direction, message ordering, and header-to-edge
assignment. It is the promotion statistic; the narrower reported statistic
is diagnostic.

## Matched controls

Run 50,000 deterministic controls with seed `0x18a11`. Independently shuffle
each post-opening body while preserving:

- exact length;
- exact symbol multiset;
- no adjacent equal values.

Headers and the already removed copied openings stay fixed. For every control
recompute the targeted gap-11 statistic and the complete broad gap/order
search. Use plus-one corrected upper tails.

The detector first has to recover a short planted triple with one clean
gap-11 anchor per stream and the exact `75,81,48` relationship.

## Promotion and stop

Promote a real header/body construction link only if:

1. both predicted nonreference anchors are exact;
2. the exact targeted corrected tail is below `.01`;
3. the fully selection-corrected broad tail is below `.01`.

Promotion does not decode plaintext and does not prove modular subtraction is
the running cipher. It would establish that the final-row headers and a
label-invariant repeated-body landmark are coupled more tightly than expected
under the matched corpus nuisance structure.

If the broad tail is at least `.01`, retain the arithmetic as a retrospective
coincidence and do not scan more gap ranges or difference sign conventions.
