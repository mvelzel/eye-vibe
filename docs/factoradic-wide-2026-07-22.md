# Wide S6/body interface pass — 22 July 2026

## Outcome

The independently reproduced factoradic header structure does not transfer to
the body through any of six natural direct interfaces. No lane promotes. This
does not reject the header classifier; it sharply favors “metadata or dynamic
seed whose update rule is still missing” over “apply the header permutation to
the following symbols.”

The calibration freezes all nine real headers and globally permutes only the
83 body labels. It therefore preserves body equality, all copied prefixes,
message lengths, and the complete header structure while breaking a proposed
absolute lexicographic-S6 meaning of the bodies. Each statistic reselects its
small declared orientation family inside every control. Five hundred controls
are sufficient here because no result approaches the `0.01` promotion line.

Reproduction:

```text
PYTHONPATH=src python3 scripts/run_factoradic_wide.py --trials 500 --seed 20260722
```

## Results

| lane | observed | corrected matched-control tail | decision |
|---|---:|---:|---|
| A. message product predicts identity/header/inverse | `0/9` | `501/501 = 1` upper | reject |
| B1. adjacent quotient support | 119 distinct of 120 possible S5 elements | `501/501 = 1` lower | reject small-generator walk |
| B2. quotient rank remains visible `0..82` | `742/1018` | `396/501 = 0.790419` upper | reject |
| B3. quotient belongs to P's D4 | `80/1018` | `164/501 = 0.327345` upper | reject |
| C. summed running-state support | 680 states over nine messages | `498/501 = 0.994012` lower | reject compression |
| E1. body token shares header coset | 75 tokens | `482/501 = 0.962076` upper | reject |
| E2. adjacent tokens stay in one P coset | `80/1018` | `164/501 = 0.327345` upper | reject |
| F. selected absolute/quotient cycle-type MI | `0.0354916` bits | `258/501 = 0.514970` upper | reject |

The adjacent quotient result is particularly strong as a kill: because every
rank `0..82` fixes center under canonical unranking, all body permutations and
their quotients live in one S5 of size 120. The observed transitions cover 119
of those elements. The body is not walking on a conspicuously small S6
generator vocabulary.

The running-state test selects left/right action, token inversion, and header
inversion. Even the best route visits 680 distinct per-message states in total;
only three of 500 controls are at least that uncompressed under the lower-tail
test. This is the opposite of a useful state collapse.

## Moving newline is syntactically destructive

The delimiter lane uses the exact reconstructed renderer tape, not the
accepted trigram stream: five eye symbols plus an authored newline after every
visual row. Applying each message's header permutation forward or backward is
always formally a six-symbol substitution, but Q swaps newline with a frequent
gaze symbol. The results are:

| direction | output rows | empty rows | rows length at least 15 | longest row | non-newline counts mod 3 by message |
|---|---:|---:|---:|---:|---|
| forward | 327 | 30 | 57 | 44 | `000010112` |
| inverse | 456 | 75 | 43 | 44 | `000010121` |

The source has 86 nonempty authored visual rows. The transformed Q tapes are
mostly short fragments, contain many empty rows, and five messages fail
three-symbol retokenization in both directions. Literal migration of the row
delimiter is rejected. This is an exact syntactic falsifier rather than a
language score.

## Scope

This pass does not test every state machine seeded by a six-symbol header. An
unknown dynamic update could use a header merely to select a program, shuffle,
or register class. What is now disallowed without new evidence is rescuing the
lead through arbitrary S6 feature-to-letter tables, per-message conventions,
or another fixed substitution.

The seventh portfolio lane—label-invariant “deck chaining” or recovery of
merged XGAK operation classes—is qualitatively different. It remains open only
as a method-development problem and should first solve a known GCTAK/practice
fixture. It is not evidence that the Eye body uses the factoradic permutations.
