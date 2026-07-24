# Fourteenth horizon: recursive branch-check result

## Outcome

The finite recursive branch-check lane is exactly negative.

The planted five-branch tree gives `5/5` leave-one-out predictions and root
closure. On the Eye trie, none of the 54 predeclared rules gives zero at even
one of the five branch nodes. Leave-one-out prediction is therefore `0/5`,
and the all-branch-selected tie rule gives root value 62 rather than zero.

The exact data gate fails before matched controls.

## Frozen rule

The model was committed before coefficient evaluation in
[`fourteenth-recursive-check-freeze-2026-07-24.md`](fourteenth-recursive-check-freeze-2026-07-24.md).
For every body-trie node:

```text
R(v) =
    a * incoming_label(v)
  + b * sum(R(child))
  + c * outdegree(v)
  + d * depth(v)
  mod 101
```

The family contains:

```text
a in {-1,+1}
b,c,d in {-1,0,+1}
54 rules
```

Each of the five outdegree-at-least-two nodes is held out in turn while the
rule maximizing zeros on the other four is selected. Ties are
coefficient-lexicographic and never inspect the held node. Separately, one
rule is selected on all five branches and tested at the unscored trie root.

Promotion required `5/5`, root zero, passing planted selection, and a joint
matched tail below `.01`.

## Positive control

The planted dictionary has five nested branch nodes at depths 1 through 5.
Their incoming labels equal their depths, making the label-consuming rule
`-incoming + depth` close at every branch and root.

The complete selector recovers:

```text
leave-one-out:           5/5
held-out values:         0,0,0,0,0
selected branch values:  0,0,0,0,0
root value:              0
```

It also independently verifies that `(1,1,0,0)` at the trie root equals the
ordinary deduplicated transition-label sum.

## Eye result

The five canonical branch paths have depths:

```text
2,24,5,9,20
```

which are the existing `BEXIT` hierarchy in the canonical path order. Across
all `54×5 = 270` rule/branch values:

```text
branch zeros:       0
leave-one-out:      0/5
```

Because every training fold has zero hits under every rule, deterministic
tie-breaking selects:

```text
(a,b,c,d)=(-1,-1,-1,-1)
```

Its Eye values are:

```text
branches: 96,32,64,73,5
root:     62
```

Thus both exact gates fail. Running 2,000 subgroup controls cannot turn the
observed score into `5/5` or the observed root into zero, so the conditional
control phase is correctly skipped.

## Interpretation

The known root checksum is not the terminal value of any branch-self-checking
recursion in this small natural family. In particular, the definitional
transition sum `(1,1,0,0)` does not validate the proper branch nodes, and no
combination of signed incoming label, child sum, outdegree, and depth repairs
that.

This rejects only the frozen uniform rule. It does not prove that no recursive
construction exists, but expanding coefficients, assigning different rules
by node type, or adding leaves as fitted checks would use five observations to
manufacture a formula. Such variants are closed absent an independently
authored game interface.

The original `37,774 mod 101 = 0` trie closure remains real and unexplained.
This result removes one proposed way of converting it into a predictive
machine; it does not erase the checksum itself.

## Reproduction

```bash
PYTHONPATH=src python scripts/run_fourteenth_recursive.py
PYTHONPATH=src python -m unittest tests.test_fourteenth_recursive -v
```

Definitions are in
[`fourteenth_recursive.py`](../src/eye_mystery/fourteenth_recursive.py).
