# Thirty-ninth pass — Veska state-selector results

> **Status correction, 26 July 2026:** This state-selector interpretation is
> withdrawn from the promoted model. It maps Veska into already measured Eye
> quantities without a complete asset decoder or held-out consequence, so the
> fit contributes no evidence to either theory.

## Outcome

Promote Veska as a later state-selector diagram for the executable Eye control
cycle:

```text
upper 1,5,3 -> 15 | 3
                |   |
                |   +-- E4 loop suffix width
                +------ terminal late equality class

lower +3    -> returned header27 +3 = phase length30
```

The same authored marks retain their already reproduced locale reading
`153,+3 -> fi`. These are two uses of one object, not independent statistical
events.

## Fixed parse

The late common phase has five repeated classes:

```text
5,0,20,1,15
```

The distinct typed suffix widths are:

```text
3,4
```

Splitting the fixed component string `153` after its second digit gives:

```text
class15, suffix3
```

Class 15 is exactly the terminal repeat selected by row 2. Width 3 is the
typed suffix of the E4 loop panel. E5 also has width 3, but the header topology
independently selects E4 as the loop and source-operation origin.

## Broad parsing inventory

Crossing all repeated classes with both distinct widths gives ten possible
decimal concatenations. Exactly one equals 153:

```text
(15,3)
```

The finite inventory frequency is `1/10`. It is descriptive after inspection,
not a discovery p-value.

The result is unchanged when broadening to:

- every late class ID `0..24`;
- both nonempty splits of the fixed string `153`;
- every permutation of component lengths `1,5,3`;
- both typed widths `3,4`.

The complete valid-parse inventory remains:

```text
components (1,5,3), split 15|3
```

No other component ordering produces a valid class/suffix pair.

## Lower tape execution

The terminal source subtraction returns:

```text
W4_label67 - E4_label40 = header27
```

Veska's lower tape supplies exactly the next operation:

```text
27+3 = 30
```

`30` is the independently measured late three-panel phase length. No new
number convention, modulus, sign, or target is introduced at this step.

## Locale double reading

The prior raw-sprite audit remains valid:

```text
153 mod83 + ASCII32       = f
(153+3) mod83 + ASCII32   = i
```

The state-machine reading now explains why the asset may have used exactly
`153,+3`, beyond merely restating `FI`:

- `15` selects the terminal equality state;
- `3` selects the loop-panel width;
- `+3` restarts the returned header state.

This is a plausible deliberate double encoding by a later clue. The Gate boss
still postdates the Eye Messages and cannot have been required to construct
their original renderer.

## Revised Gate assessment

Promoted:

- Veska `9|8=17` matches the first common phase width;
- upper `15|3` selects the terminal state and loop suffix;
- lower `+3` restarts the closed cycle;
- `153,+3` redundantly yields `fi`;
- the Eye headers themselves execute target-to-source scope routing.

Still unproved:

- Seula's claimed 70-pixel residual mask;
- the exact 72-mark Type4 partition rule;
- side-band operand scopes;
- the eight-entry Type6 cache role table;
- allocation of first-seen values.

The useful part of the Gate theory is now an executable construction diagram.
The full dossier machine remains unsupported.

## Next falsification target

Three repeated states produce marker-valued pair differences:

```text
position9  class5   distance4   W4->E4 = marker77
position26 class20  distance4   E5->E4 = marker36
position29 class15  distance13  E4->W4 = marker27
```

Freeze a scope/direction schedule from header types and repeat structure before
testing those values. A successful schedule must explain the two marker hits
and predict why repeat events at positions 18 and 27 are not control returns.

## Reproduction

```bash
PYTHONPATH=src python scripts/audit_veska_state_selector.py
PYTHONPATH=src python -m unittest tests.test_veska_state_selector
```

Implementation:

- `src/eye_mystery/veska_state_selector.py`
- `tests/test_veska_state_selector.py`
- frozen protocol:
  `docs/thirty-ninth-veska-state-selector-freeze-2026-07-26.md`
