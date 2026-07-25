# Forty-first pass — state-table transform freeze

## Question

Does the promoted middle-eye control wheel select a direct low-capacity
geometric transform between the three `5×5` class-to-visible-label tables?

This screen tests direct table/substitution consumers before moving to a
stateful allocator.

## Fixed tables

For E4, W4, and E5:

- use late equality classes `0..24`;
- map class `5*r+c` to grid coordinate `(r,c)`;
- retain the actual visible rank assigned to each class;
- reserve control classes `5,15,20` as training diagnostics;
- reserve class10 and the boundary34 exit as held-out consequences.

No language score or plaintext alphabet enters this pass.

## Family A — class-coordinate D4

For every ordered panel pair, test all eight D4 transforms of the `5×5`
coordinate square.

Report:

- exact visible-label matches;
- the modal fixed mod-83 output offset and its match count.

Broaden with all 25 toroidal row/column translations after each D4 transform.

## Family B — visible-eye geometry

Decode every visible rank into its three base-five eye directions. For every
ordered panel pair, test:

- all six eye-position permutations;
- one shared physical D4 direction transform on all three eyes;
- the broad family with an independent physical D4 transform per eye.

Re-encode and count exact target labels.

## Held-out control

For the visible-eye families, score only classes `5,15,20` during selection.
Report:

- maximum training matches;
- number of co-best models;
- how many co-best models predict class10.

A direct geometric consumer must predict class10 rather than merely match an
unrelated cell elsewhere.

## Capacity and promotion gate

Inventory model counts:

```text
coordinate D4                 6×8
coordinate D4 + translations 6×8×25
shared visible D4            6×6×8
independent-eye D4           6×6×8^3
```

Promote only if:

- one low-capacity family explains most control states;
- class10 is predicted by the same frozen transform;
- performance materially exceeds ordinary isolated coincidences.

Three or fewer exact matches in the 18,432-model independent-eye family is
an automatic rejection. A modal offset explaining only three cells is also
rejected.
