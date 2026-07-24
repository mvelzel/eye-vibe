# Twenty-eighth freeze — RNG locale-salt audit

## Observation that selected the lane

The current installed WAK contains the following two consecutive updates before
`SetRandomSeed` in both `items/chest_random.lua` and `items/utility_box.lua`:

```lua
rand_x = rand_x + 509.7
rand_y = rand_y + 683.1
SetRandomSeed( rand_x, rand_y )
```

The integer parts are assigned geographic E.164 calling codes:

```text
+509 -> HT (Haiti)
+683 -> NU (Niue)
```

`+683` is also the first coordinate-plane column checksum in the independently
specified marker construction. This was noticed after the marker result, so the
following inventory is a descriptive corroboration audit, not a discovery
test.

## Fixed source universe

- the user's current installed `data.wak`;
- every `.lua` entry;
- executable code only, after stripping line comments;
- every syntactically balanced two-argument call to `SetRandomSeed`;
- numeric literals used as additive or subtractive salts in either argument;
- simple same-variable salt updates in the preceding 12 physical lines when a
  call argument is a bare identifier:

```lua
v = v + NUMBER
v = v - NUMBER
v = NUMBER + v
```

The backward trace stops at the first other assignment to that variable.
Numbers in comments, string literals, multiplication, function arguments, RNG
bounds, or unrelated nearby statements are outside the grammar. Bare numeric
seeds are not coordinate salts.

## Fixed normalization

- preserve the sign and decimal spelling in the reported recipe;
- map a salt to a possible calling code by taking the absolute integer part
  (truncation toward zero);
- retain every parsed call, including calls with zero or one salt;
- deduplicate exact normalized two-argument salt recipes before comparative
  counts, so the copied chest and utility-box routine contributes one recipe.

## Frozen questions

1. How many calls and distinct normalized recipes contain at least one salt?
2. How many distinct recipes contain one of the three marker-plane codes
   `{34, 358, 683}`?
3. How many distinct recipes contain exactly one salt in each argument and both
   integer parts are assigned geographic calling codes?
4. Is `(509,683)` unique under question 3?

The calling-code mapping and geographic exclusion rule are exactly those pinned
for the three-plane locale audit. Region `001` is not geographic.

## Interpretation gate

A unique `(509,683)` or `683` occurrence would establish a real code-level
cross-reference candidate, but not intent. Promotion to an in-game Eye clue
would additionally require at least one of:

- eligible chronology and source history showing deliberate reuse;
- a role for both `509` and the fractional digits selected independently of
  the desired reading;
- a prediction about the Eye data not used to select this audit;
- a second independently authored asset using the same interface.

Without one of those, the result remains an interesting magic-constant
coincidence.
