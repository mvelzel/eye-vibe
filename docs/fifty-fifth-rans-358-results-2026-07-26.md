# Fifty-fifth pass — metadata-selected radix-five rANS

## Outcome

The new identity

```text
83 = 3 × 5² + 8
```

made one previously recorded but unexecuted idea concrete: interpret the
accepted `83/125` split as the total-frequency table of a radix-five
asymmetric numeral system.

The smallest key-free version is now rejected. Across all 16 natural
conventions, it destroys all seven fixed nonliteral Eye isomorphs at the
first decoded symbol. This is a narrow result about the standard
quasi-uniform table, not a rejection of every possible ANS construction.

## 1. Frozen model

The independently motivated quantities are:

```text
radix b             5
total frequency M  83
plaintext symbols  42 = (83 + 1) / 2
normalization L    83
state interval     [83,415)
```

A key-free 42-symbol table summing to 83 has 41 frequencies of two and one
frequency of one. The audit places that singleton at either endpoint.

The first accepted Eye glyph `h` supplies the state residue. Every complete
normalized state consistent with it is:

```text
x = 83q + h, q in {1,2,3,4}
```

The remaining raw eye digits supply the base-five refill stream. Both stream
directions are tested. This freezes:

```text
2 singleton positions × 2 digit directions × 4 state quotients
= 16 models
```

No plaintext alphabet, language score, fitted frequency, or message-specific
choice enters the audit.

## 2. Standard decode and positive control

For state `x`, residue `r = x mod 83`, symbol frequency `f`, and cumulative
frequency `c`, the decoder uses:

```text
x <- f floor(x/83) + r - c
while x < 83:
    x <- 5x + next_digit
```

This is the standard range-ANS update with radix-five renormalization. The
inverse encoder is implemented as well. Deterministic random 100-symbol
fixtures round-trip exactly for both frequency tables, including the terminal
state and every consumed digit.

The construction follows the ordinary ANS state-and-renormalization model
described in [Duda's original ANS paper](https://arxiv.org/abs/0902.0271).

## 3. Eye discriminator

Readable output is too flexible a target, so the test uses the seven fixed
accepted nonliteral isomorphs from the causal-context audit. Each emitted
symbol retains the exact original body-digit positions that caused its refill.
For each paired glyph interval, compare only emissions whose complete source
lies inside that interval.

Every model fails immediately:

```text
models                         16
fixed paired contexts           7
best literal agreement      6/189
total compared           185..189
maximum common prefix            0
equal restricted-growth maps   0/7
```

The best result is the forward stream with the singleton frequency at the
last symbol. Its six literal agreements are dispersed; no paired context
shares even its first decoded symbol. Changing the initial quotient does not
repair the failure.

## 4. Interpretation and stop rule

The attractive part of this lead was its unusually small selector burden:
`3,5,8`, radix five, alphabet size 83, and the natural 42-symbol pairing
jointly specify almost the entire machine. The preserved Eye repetitions then
provide a language-free falsifier.

The result closes:

```text
standard rANS
M = L = 83
b = 5
42 quasi-uniform symbols
one endpoint singleton
header as state residue
either raw digit direction
```

Do not widen this into arbitrary tANS spreads, interior singleton positions,
custom frequency tables, or plaintext-fitted probabilities. Those families
have enough design capacity to manufacture output and currently lack an
in-game or authored selector.

## Reproduction

```text
PYTHONPATH=src python3 scripts/audit_rans_358.py
```

The implementation and positive controls are:

- `src/eye_mystery/rans_358.py`
- `tests/test_rans_358.py`

