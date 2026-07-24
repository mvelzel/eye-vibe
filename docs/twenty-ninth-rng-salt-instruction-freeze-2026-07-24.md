# Twenty-ninth freeze — RNG salt as an Eye-alphabet instruction

## Observation that selected the lane

The independently inventoried chest salt recipe is:

```text
509.7 | 683.1
```

Taking the signed integer parts modulo the Eye alphabet size and applying the
standard ASCII+32 display gives:

```text
509 mod 83 = 11 -> ASCII 43 -> +
683 mod 83 = 19 -> ASCII 51 -> 3
```

Thus the pair reads `+3`. This was noticed after the salts and the Gate asset
were inspected. It is not a discovery test.

The reading has an asset-side target that predates this observation: Veska's
objectively separable lower eight-pixel band contains one five-pixel plus
component followed left-to-right by three singleton components. The existing
ground-up Gate audit already recorded this as a plausible `+3` pictogram while
rejecting the dossier's under-specified full `12+43+9+8` partition.

## Fixed comparison universe

Use the distinct salted recipes produced by the twenty-eighth frozen
`SetRandomSeed` grammar. Retain only recipes with exactly one salt feeding each
of the two arguments.

For every retained recipe:

1. truncate each signed decimal salt toward zero;
2. reduce each integer modulo 83 into `0..82`;
3. add 32 and display the two ASCII characters;
4. preserve authored argument order (`x`,`y`) as primary;
5. report reversed argument order as the sole order broadening;
6. repeat with absolute integer parts as a sign broadening.

No offsets, digit concatenations, decimal scaling, character shifts, modulus
changes, or multi-salt recipes are admitted.

## Frozen events

Report:

- number of eligible distinct recipes;
- exact primary text `+3`;
- exact `+3` under reversal and/or absolute-value broadening;
- a generic compact arithmetic instruction, defined before enumeration as:
  - first character in `+-*/%^&|`;
  - second character an ASCII decimal digit `0..9`.

The generic class is only a comparator. Since the target chose the transform,
even a unique result is descriptive.

## Interpretation gate

Promotion from a cross-reference candidate to a decoder instruction requires
a fixed operand and scope for the `+3` operation. In particular, `+3` must
predict an untouched Eye relation or recover a value without selecting its
input from the result. The Gate sprite alone supplies neither operand nor
scope.

Chronology is allowed only in the later-clue sense: the Eye Messages appeared
in October 2020, the Gate boss followed in December 2020 beta, and the RNG
salts entered the public game data with the March 2023 chest-randomness fix.
The salt pair cannot have been needed to construct the original ciphertext.
