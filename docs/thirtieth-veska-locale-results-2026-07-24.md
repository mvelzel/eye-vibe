# Thirtieth result — Veska directly reads `fi`

## Outcome

Using the Gate asset bands fixed before this interpretation was noticed,
Veska supplies a complete Eye-alphabet operation:

```text
upper components, left to right: 1,5,3 -> 153
lower components:                  +3

153 mod 83       = 70 -> chr(70+32) = 'f'
(153+3) mod 83   = 73 -> chr(73+32) = 'i'
```

The asset therefore reads:

```text
fi
```

This exactly matches, case-insensitively, the `FI` locale selected by the
original Eye marker layer:

```text
marker scalar grid columns  -> +358 -> regions FI,AX
marker fixed-trail BWT       -> !Fi
Veska upper/lower marks      -> fi
```

This is a clean and substantially simpler extraction than the dossier's
provisional Type4/Type6 machine. It uses an operand, a visible operation, the
independently established Eye modulus, and the standard display offset.

## Pixel verification

The unchanged Veska sprite has SHA-256:

```text
a2e7dd2bfb9b573eb733c1e4d2e52fa0163925b8aeb233b37870332dc264854f
```

The exact mark color is `(60,57,65,255)`.

Previously fixed upper-band points:

```text
(9,18)
(21,16) (22,15) (23,13) (23,14) (24,12)
(39,20) (40,21) (40,22)
```

Their 8-neighbour components have left-to-right sizes `1,5,3`.

Previously fixed lower-band points:

```text
(13,48) (14,47) (14,48) (14,49) (15,48)
(37,48)
(46,53)
(49,46)
```

The first five are an exact orthogonal plus. The remaining three are
singletons strictly to its right. The audited whole-band counts remain
`11 remainder + 44 middle + 9 upper + 8 lower = 72`; this reading does not
claim the dossier's under-specified `12+43+9+8` partition.

## Order and semantic comparators

All six permutations of upper component order give:

| Component order | Eye text | Assigned geographic region |
|---|---:|---:|
| natural `1,5,3` | **`fi`** | FI |
| `1,3,5` | `TW` | TW |
| `5,1,3` | `/2` | no |
| `5,3,1` | `AD` | AD |
| `3,1,5` | `be` | BE |
| mirrored `3,5,1` | `36` | no |

Four of six permutations happen to name some region, so generic
“country-code-looking text” is weak evidence. The discriminating fact is that
the authored spatial order alone names the independently selected marker
locale `FI`; horizontal reflection does not.

Across every possible starting residue in `0..82`, a `+3` operation yields:

```text
15 / 83  lowercase-to-lowercase pairs
24 / 83  case-insensitive assigned geographic region pairs
 1 / 83  exact lowercase fi
```

These are specificity descriptions, not a corrected p-value. The bands,
decimal concatenation, modulus, and semantic target were all part of a
post-hoc investigative path.

## Chronology

The exact sprite is byte-identical in the public 9 February 2021 data commit
and the January 2025 installed build. Contemporary community evidence places
the awakened boss on beta by 14–15 December 2020, after the Eye Messages'
October 2020 appearance.

Therefore:

- Veska cannot be the original encryption key;
- it is eligible as a deliberately added decoder/header clue;
- the March 2023 `509.7,683.1` RNG salts can be a still later independent
  restatement of its `+3`.

## Discord novelty check

Read-only server-wide searches for `Veska 153` and `Veska fi` found no prior
discussion of this arithmetic reading. The lone relevant `Veska fi` hit is a
2023 message noting the known Finnish goalkeeper slang behind the boss-part
names (`veska`, `mokke`, `molari`). That overt Finnish naming makes the locale
echo thematically appropriate, while also raising the ordinary background
rate of Finnish references in the asset.

No messages or reactions were sent.

## Assessment

This does **not** validate the full Gate dossier. The Seula residual, Type6
cache, first-seen allocator, and claimed no-leftover Veska partition remain
unreproduced or incomplete.

It does promote one narrow Gate claim much further:

> Veska is very plausibly a later construction diagram for the Eye marker's
> Finnish locale tag.

The result still does not decode any body symbol. The correct next use is to
look for an independently fixed body field on which a `+3 mod83` transition
predicts an untouched relation, rather than trying arbitrary shifts.

Protocol:
[`thirtieth-veska-locale-freeze-2026-07-24.md`](thirtieth-veska-locale-freeze-2026-07-24.md).

Implementation:

- `src/eye_mystery/gate_locale.py`
- `scripts/analyze_gate_guardian.py`
- `tests/test_gate_locale.py`
