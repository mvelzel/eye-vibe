# Twenty-eighth result — the `509.7,683.1` RNG salt is unique

## Outcome

The complete frozen current-WAK inventory finds one exceptional coordinate
salt recipe:

```lua
rand_x = rand_x + 509.7
rand_y = rand_y + 683.1
SetRandomSeed( rand_x, rand_y )
```

After exact duplicate recipes are collapsed, it is simultaneously:

- the only RNG salt recipe containing any marker-plane code
  `{34,358,683}`;
- the only recipe with one geographic calling code in each argument:
  `509 -> HT` and `683 -> NU`;
- an exact reuse of the first marker-plane column code `683 -> NU`.

The current installed WAK results are:

| Stage | Count |
|---|---:|
| executable `SetRandomSeed` calls | 332 |
| calls with an eligible additive/subtractive salt | 34 |
| distinct salted recipes | 28 |
| distinct recipes containing `34`, `358`, or `683` | **1** |
| distinct one-salt-per-argument geographic pairs | **1** |

The recipe occurs in two files:

```text
data/scripts/items/chest_random.lua:334
data/scripts/items/utility_box.lua:205
```

Those are copied implementations of the same reward routine, not two
independent authored witnesses.

## Historical result

The loose public early-access data contains 46 executable `SetRandomSeed`
calls, four eligible salted calls, four distinct recipes, and no marker-code
or geographic pair.

The public `vexx32/noita-data` history shows the chest salt block added in its
11 March 2023 stable snapshot:

```text
7b6eca945caa3f2fad7f759142cdd44033d80e5b
```

The previous public version calls `SetRandomSeed(rand_x,rand_y)` without the
two additions. The official same-day release notes say “Chest contents are a
bit more random,” and the source comment explains that the developers are
mixing position-seed coordinates constrained by `spawn_heart`.

This is clean later-clue chronology:

```text
October 2020  Eye Messages
December 2020 Gate Guardian on beta
March 2023    509.7,683.1 chest RNG salts
```

The constants cannot have been required to construct the original Eye
ciphertext, but can intentionally restate a decoding clue.

Sources:

- [public March 2023 data snapshot](https://github.com/vexx32/noita-data/commit/7b6eca945caa3f2fad7f759142cdd44033d80e5b)
- [official 11 March 2023 release notes](https://noitagame.com/release_notes/20230311/)

## Provenance and verification

The audited installed `data.wak` has:

```text
size       42,467,033 bytes
SHA-256    c95a0c01a55ec29267afef6bbec8a0cae0ba2b350638e2203674ed4dfb9227c3
entries    14,745
```

The parser strips executable line comments, balances calls and nested
parentheses, records only top-level additive/subtractive literals, and traces
the frozen simple same-variable update grammar for 12 preceding lines. Tests
cover comments, multiline calls, nested commas, reassignment stops, direct
salts, and traced salts.

A read-only Discord search found one prior exact `509.7 683.1` discussion in
`mod-development` from 2 September 2024. It concerns reproducing treasure
chest RNG and confirms that `SetRandomSeed` uses floating-point inputs; it
does not mention calling codes, the Eye Messages, or the Gate. No messages or
reactions were sent.

## Assessment

This promotes the salt pair from an uncalibrated number hit to a serious
in-game cross-reference candidate. The complete relevant code inventory makes
`683` and the two-code pair unique in their actual executable role.

It does not by itself establish intent. The source comment and release note
give the constants an ordinary bug-fix purpose, the copied utility routine is
not independent, `509` does not occur in the marker grid, and the decimal
fractions have no locale interpretation.

The next independently useful fact is documented separately: the integer
parts also map through the Eye alphabet to `+3`.

Protocol:
[`twenty-eighth-rng-locale-salt-freeze-2026-07-24.md`](twenty-eighth-rng-locale-salt-freeze-2026-07-24.md).

Implementation:

- `src/eye_mystery/rng_locale_salts.py`
- `scripts/audit_rng_locale_salts.py`
- `tests/test_rng_locale_salts.py`
