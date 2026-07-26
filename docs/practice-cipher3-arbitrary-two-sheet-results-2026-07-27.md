# Practice cipher 3 — arbitrary two-sheet results

**Date:** 27 July 2026
**Outcome:** strong calibrated negative; no plaintext recovered

## Tested family

One global static key maps the 83 raw values onto sdlwdr's established
42-character alphabet:

```text
q : 83 raw symbols -> 42 plaintext symbols
```

Exactly one plaintext symbol has one raw representative; every other symbol
has two. This tests the full *architecture* of an arbitrary static
`83=2*42-1` quotient without assuming the failed affine pairing
`x ~ a-x mod83`.

The optimizer preserves those capacities exactly. Its only moves swap two raw
assignments or migrate the singleton role. The key is selected on group A;
groups B and C are never used for tuning.

This is a calibrated heuristic search, not an exhaustive proof over all
`83!/(2!^41)` keys.

## Positive control

The 42-symbol trigram model was trained on Project Gutenberg's *Sherlock
Holmes*. Independent planted plaintext came from Project Gutenberg's
*Moby-Dick*, retained the 18 real message lengths, and was encrypted with a
random valid two-sheet key. The plant's A passages were chosen only to cover
the 42-symbol alphabet; its B/C passages were disjoint.

Frozen budget:

```text
4 restarts
300,000 iterations per restart
temperature 18.0 -> 0.08
```

Results:

```text
mode   A score/tri   B+C score/tri   A accuracy   B+C accuracy
full    -8.632496      -7.404421     94.444444%    98.448368%
body    -8.620864      -7.487876     94.354839%    97.199785%
```

The frozen A key renders untouched heldout prose such as:

```text
... UNLESS MEDICINALLY THAT MAN HAS PROJABLY GOT A QUOGGY
SPOT IN HIM SOMEWHERE? AS A GENERAL RULE ...
```

Minor letter errors account for the less-than-perfect accuracy. The mechanism,
key representation, and optimizer are operational at the frozen budget.

## Real corpus

The real run was performed once in each predeclared mode:

```text
mode   A score/tri   B+C score/tri   heldout deficit vs plant
full   -12.088359     -15.749327             -8.344906
body   -12.171343     -15.744717             -8.256841
```

Representative full-mode output:

```text
A0  6FTELS OUQM08’D YF2-TWEAQUIEAVIZZKVVHD8!FX6Z3XPROMQUIZ?M0
B0  6 L2’KJ!0TPTBKXZEH. KFDJMG?KO0F G-FH P4DB.L-26RCVJ7R...
C0  8G7AZ.-3Z72QQP2AU7AQ37J’L6OQ5LH’U!8A -0WI’82O8GD!...
```

Body mode is equally unreadable. The key overfits the short A group and
collapses on B/C, unlike the planted control.

## Decision

Stop the direct arbitrary static two-sheet lane. At a solver budget that
recovers an independent matched plant almost perfectly on heldout text, the
real corpus is separated by more than eight log units per heldout trigram and
contains no language.

At this search budget, this is strong evidence against:

- one global static 83-to-42 homophonic substitution;
- the arbitrary hidden-pairing model with 41 doubletons and one singleton;
- both payload-first and first-symbol-as-indicator conventions.

It is not exact UNSAT and does not exclude a stateful sheet schedule,
polygraphic/radix codec, or dynamic homophone allocation.

## Transferable method

When an alphabet identity suggests a hidden quotient, optimize the complete
capacity-constrained mapping rather than only a convenient coordinate family.
Preserve the quotient's exact preimage sizes during every move. Most
importantly, select the key on one corpus family and demand readable text on
another: the real A score alone looked substantially better than random, but
heldout B/C exposed it as overfit.

## Reproduction

```text
PYTHONPATH=src python3 -m unittest \
  tests.test_practice_cipher3_arbitrary_two_sheet

PYTHONPATH=src python3 \
  scripts/run_practice_cipher3_arbitrary_two_sheet.py \
  --phase control --mode both --restarts 4 --iterations 300000

PYTHONPATH=src python3 \
  scripts/run_practice_cipher3_arbitrary_two_sheet.py \
  --phase real --mode both --restarts 4 --iterations 300000
```

The two Project Gutenberg inputs and their exact SHA-256 values are recorded
in the freeze document. The script refuses mismatched files.
