# Twenty-ninth result — the RNG salt uniquely spells `+3`

## Outcome

The exceptional chest RNG salt pair has a second exact reading:

```text
509 mod 83 = 11 -> chr(11+32) = '+'
683 mod 83 = 19 -> chr(19+32) = '3'
```

So its authored argument order spells:

```text
+3
```

Among all 28 distinct salted recipes in the frozen WAK inventory, 11 have
exactly one salt in each argument. The chest recipe is:

- the only primary-order compact arithmetic instruction;
- the only exact `+3`;
- still the only exact `+3` after sign and argument-order broadening.

## Complete eligible inventory

Signed integer part modulo 83, then ASCII+32:

| Salt recipe | Primary text | Absolute-sign text | Source |
|---|---:|---:|---|
| `-437,235` | `]e` | `6e` | `items/egg_hatch.lua` |
| `11,-21` | `+^` | `+5` | `director_helpers.lua` |
| `236,-4125` | `f9` | `fZ` | `magic/altar_tablet_magic.lua` |
| `2533,-36` | `KO` | `KD` | `projectiles/random_explosion.lua` |
| `2617.941,-1229.3581` | `L0` | `Lc` | `item_spawnlists.lua` |
| `325,-235` | `l.` | `le` | `projectile_transmutation.lua` |
| `35,-253` | `Co` | `C$` | `biome_scripts.lua` |
| `425,-243` | `*&` | `*m` | `item_spawnlists.lua` |
| `436,-3252` | `5d` | `5/` | `projectiles/transmutation.lua` |
| `45,-2123` | `MC` | `MP` | `biome_scripts.lua` |
| `509.7,683.1` | **`+3`** | **`+3`** | chest/utility reward routine |

Exact counts:

| Event | Count |
|---|---:|
| one-salt-per-argument recipes | 11 |
| primary operator-plus-digit recipes | **1** |
| operator-plus-digit after sign/order broadening | 3 |
| primary exact `+3` | **1** |
| broadened exact `+3` | **1** |

The two extra broadened arithmetic strings are `+5` from `11,-21` after
absolute-value conversion and `/5` from reversed absolute `436,-3252`.
Neither equals the Gate target.

## Gate connection

The existing raw-sprite audit had already measured Veska's lower mark band as:

```text
one orthogonal five-pixel plus + three singleton components
```

Thus the source-code salt pair independently reproduces a literal Gate
pictogram under the Eye modulus and display alphabet. The 2023 salts postdate
both the 2020 Eyes and the 2020 Gate boss, so they can be a later restatement
but not a construction input.

The source comment still supplies a normal gameplay reason for arbitrary
floating salts. This result is therefore a strong cross-reference candidate,
not proof that the developers selected the constants for the Eye puzzle.

Most importantly, `+3` now has an asset-local operand: Veska's upper
left-to-right component sizes are `1,5,3`. The direct resulting locale reading
is in the thirtieth result.

Protocol:
[`twenty-ninth-rng-salt-instruction-freeze-2026-07-24.md`](twenty-ninth-rng-salt-instruction-freeze-2026-07-24.md).
