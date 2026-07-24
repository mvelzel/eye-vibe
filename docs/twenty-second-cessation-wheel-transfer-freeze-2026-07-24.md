# Twenty-second freeze: Cessation row sampler on the Earthquake wheel

## Why this is a lateral test

Directly masking the final 17-symbol Eye slices with the Earthquake circle's
irregular row was decisively negative.  The next registered action does not
shift or repair that mask.  It changes the *operation* from static selection
to physical wheel traversal.

A newly shared, independently solved practice puzzle supplies a precise
operation worth transferring.  In Discord channel
`silmä-teollinan-älly`, Lquid posted
`cessation-cipher-llm-recovery-results.zip` on 23 July 2026.  The downloaded
archive has SHA-256:

```text
1c4a834e9722bf3287e008d973ff4eae914988c3a4129b8fcdcac13ad00c8e71
```

Its ledger and independent verifier recover an 85-byte plaintext by treating
digits `1..5` as forward distances through a binary tape, resetting the
pointer at each printed line, sampling the last consumed position for every
nonterminal digit, and sampling the first position *after* consumption for
the line-terminal digit.  The terminal exception changes exactly the 22
damaged bits of the simpler endpoint reading.  The puzzle author confirmed
the reported plaintext and surrounding figures in the same discussion.

This practice puzzle is not an in-game Eye clue.  Its value is methodological:
it identifies a concrete row-reset/terminal-aware sampler that the prior
Cessation-to-Eyes scans did not test.  Those scans reset at interleaved
row-pair chunks and sampled the 31-bit Void calendar key uniformly; they did
not reconstruct the actual visual rows, use the 17-bit Earthquake wheel, or
give row terminals a distinct timing rule.

## Frozen inputs

Binary wheel, beginning at the authored small gap:

```text
11110111011101110
```

Eye directions use the engine values:

```text
centre=0, up=1, right=2, down=3, left=4
```

The natural transfer is therefore fixed without a fitted lookup:

```text
distance = direction + 1
```

Use the canonical full visual rows reconstructed by
`visual_rows()`.  The first marker's two upper eyes and one lower eye remain
in those rows and therefore affect the first two row states.  After sampling,
interleave the bit rows back into the accepted trigram order and interpret
each sampled bit triple as a value in `0..7`.

For each visual row:

1. set `pointer=0`, the next unconsumed tape position;
2. for every nonterminal direction `d`, emit
   `tape[pointer+d]`, then advance `pointer += d+1`;
3. for the terminal direction `d`, first advance `pointer += d+1`, then emit
   `tape[pointer]`;
4. reduce tape addresses modulo 17.

This is the exact practice-puzzle timing convention, not a family selected on
the Eyes.

## Train/held-out discriminator

Use only the seven fixed nonliteral Eye context pairs:

```text
training: first-gap30, first-cross, first-cross-late, first-gap28
held out: last-west4, last-east5, last-east3
```

Within each aligned context, score only positions whose original accepted
trigram labels differ.  This removes literal fixed-label carryover.  The score
is the number of those positions at which the sampled `0..7` trigrams agree.

The wheel has two physical directions.  Choose forward or reverse solely by
the training score, breaking a tie in favor of forward.  Apply that direction
unchanged to the three held-out contexts.  The single primary statistic is
the held-out agreement count.

## Exact matched null

The real 17-bit row contains four zeroes and thirteen ones.  Enumerate all

```text
C(17,4) = 2,380
```

binary tapes with that exact composition, including the authored tape.
For every control tape, repeat the same forward/reverse training selection
and held-out scoring.  The exact inclusive upper tail is:

```text
number of tapes with held-out score >= real score
--------------------------------------------------
                         2,380
```

Promote only if the tail is below `.01`.  Report, without a second
significance claim:

- training and held-out denominators;
- orientation selected on the real tape;
- exact-context matches;
- the corresponding score under uniform endpoint timing, where the terminal
  direction samples the last consumed position like every other direction;
- a positive fixture proving that visual-row reconstruction, terminal timing,
  orientation selection, and held-out scoring are executable.

## Stop rule

If the registered tail fails, close this exact sampler.  Do not rotate the
gap-fixed tape, permute direction distances, choose phases per message or
row, remove the marker after seeing the result, replace visual rows with
interleaved chunks, or add byte/language scoring.  A later attempt would need
an independent in-game rule selecting a different mapping or timing.

