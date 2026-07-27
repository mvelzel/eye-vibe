# Seventy-fifth pass — header/context finite-order results

## Result

All three frozen conventions are **impossible**:

```text
source header      rejected
target header      rejected
target*source^-1   rejected
```

This is invariant under every renaming of the 83 visible labels.  It is
therefore a stronger negative than merely failing to apply the six-symbol
header permutations directly to the displayed base-five coordinates.

## Exact contradictions

The five target-header orders are `4,4,5,5,5`.  Four context maps admit
finite-order completions with those exponents.  The East 4 -> West 4 map does
not: its partial graph contains a forced path on seven distinct vertices.  Any
completion must put that path in a cycle of length at least seven, while an
image of West 4's order-five header can contain only cycles of lengths one or
five.

The source convention also fails both West 1 -> East 2 maps: West 1 has order
two, while each partial map contains a forced four-vertex path.  The East 4 ->
West 4 seven-vertex path additionally exceeds East 4's order six.

The relative convention fails four of five maps.  Its first-family element has
order two; the three final relative orders are `4,2,4`.  Only East 4 -> East 3
admits the required finite-order completion.

The exact table is:

```text
context           source target source-mode target-mode relative-mode
first-cross       W1     E2     false       true        false
first-cross-late  W1     E2     false       true        false
last-west4        E4     W4     false       false       false
last-east5        E4     E5     true        true        false
last-east3        E4     E3     true        true        true
```

## Boundary

This rejects the model in which one source, target, or relative factoradic
header element acts as the complete relabeling for each registered
cross-panel context, even through an arbitrary permutation representation on
83 labels.

It does **not** reject:

- the promoted metadata/type interpretation of the headers;
- a header selecting a multi-step schedule rather than one group element;
- a body-state relation that also depends on the intervening plaintext or
  prefix state;
- GAK/XGAK or another state machine whose context map is not a header image.

No plaintext, key, or body update rule was recovered.

## Reproduction

```bash
PYTHONPATH=src .venv/bin/python -m unittest tests.test_partial_permutation
PYTHONPATH=src .venv/bin/python scripts/audit_header_context_order.py
```

The exact path/cycle completion routine is in
`src/eye_mystery/partial_permutation.py`; its planted and contradiction controls
are in `tests/test_partial_permutation.py`. The implementation also matches
brute-force completion of every partial injection through alphabet size four
for exponents one through six.
