# Cessation row sampler on the Earthquake wheel — results

## Result

The frozen transfer is strongly negative.

```text
terminal-aware real direction      forward
training changed-label agreement   19 / 63
held-out changed-label agreement   17 / 85
exact training contexts             0 / 4
exact held-out contexts             0 / 3

composition-matched tapes          2,380
tapes at least as high             2,273
inclusive exact upper tail          0.955042017
promotion threshold                 0.01
```

The fixed practice-puzzle terminal exception does not rescue the result. With
uniform endpoint timing, the same independently selected direction is forward,
training is `17/63`, and held out is `16/85`. The exception therefore adds
two training agreements and one held-out agreement, but the authored tape
remains near the low end of its exact matched distribution.

## What was executed

For each canonical visual Eye row, engine direction `d` became distance
`d+1` around the gap-fixed tape:

```text
11110111011101110
```

Every row reset to tape position zero. Nonterminal eyes sampled the last
consumed position; the terminal eye sampled the first position after
consumption. Sampled rows were then re-interleaved into the accepted trigram
order and read as three-bit values.

Only the four first-family nonliteral contexts selected forward versus
reverse. The score on the final three contexts counted sampled-value equality
only at positions where the original `0..82` labels differ:

```text
training denominator   63
held-out denominator   85
```

This avoids scoring copied labels as successes. No text, byte phase, tape
rotation, direction permutation, message-specific state, or language model
entered selection.

## Exact control

The authored row has thirteen ones and four zeroes. Every one of the
`C(17,4)=2,380` tapes with that composition underwent the identical
forward/reverse training selection before held-out scoring. The complete
held-out distribution was:

```text
score : count
11:2   13:4   14:17  15:27  16:57  17:90
18:134 19:158 20:190 21:275 22:236 23:257
24:258 25:196 26:146 27:113 28:87  29:47
30:40  31:24  32:8   33:6   34:6   36:2
```

The real score `17` is exceeded or tied by `2,273/2,380` tapes.

## Validation

The positive fixture suite checks:

- visual-row sampling and exact re-interleaving for all nine messages;
- the terminal-aware one-position timing difference on a hand-computed row;
- omission of literal source=target positions and detection of a planted exact
  changed-label context;
- training-only orientation choice and the forward tie break;
- exact enumeration of all 2,380 fixed-composition tapes, including the real
  tape.

Implementation:

```text
src/eye_mystery/cessation_wheel.py
scripts/run_cessation_wheel_audit.py
tests/test_cessation_wheel.py
```

## Decision

Close this exact sampler. Do not rotate the authored gap phase, permute
direction distances, choose phases by panel or row, drop the marker after
seeing the score, or switch back to interleaved row-pair chunks. Those changes
would form a new selected family after a decisive failure.

This result does **not** reject:

- the validated final-row self-describing anchor record;
- physical wheel models selected by some other independent in-game rule;
- Cessation's general lesson that a later puzzle can expose reusable
  construction vocabulary;
- the separate desert-glyph transform or unresolved practice ciphers.

