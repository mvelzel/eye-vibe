# Swap-or-not card-shuffle audit — freeze

## Lead

In a read-only `silmä-novel` message from 29 August 2024, sdlwdr linked the
CRYPTO 2012 paper *An Enciphering Scheme Based on a Card Shuffle* and suggested
that its shuffle might produce the Eye messages' nonliteral isomorphs.

Sources:

- Discord provenance:
  <https://discord.com/channels/453998283174576133/1063583558154854521/1278499376788144282>
- Hoang, Morris, and Rogaway:
  <https://www.iacr.org/archive/crypto2012/74170001/74170001.pdf>

The surrounding Discord discussion does not contain an execution of the
proposal, and the construction was not found in the repository.

## Frozen direct model

The paper's generalized swap-or-not round on `Z_83` has a round key `k`. A
value `x` either stays at `x` or moves to `k-x mod 83`; the round's Boolean
function chooses which paired positions swap.

This audit asks whether each of the seven accepted nonliteral Eye context maps
can be produced by one, two, or three such rounds in the visible trigram-rank
coordinates `0..82`. Each context may have its own round keys because the lead
does not supply a cross-context key schedule.

The test deliberately relaxes the construction by ignoring the requirement
that both cards in a selected pair make the same swap decision. After fixed
round keys, every possible endpoint is one of at most `2^r` affine forms:

```text
y =  x + c
y = -x + c
```

Every observed source-target edge must match at least one form. Failure is
therefore an exact exclusion of the real shuffle for that key tuple; success
would be only a necessary condition and would trigger a stronger
pair-consistency test.

No hidden relabeling, fourth or later round, plaintext crib, or fitted Boolean
round function is admitted.

## Matched null

For each context, preserve its exact source labels and number of distinct
mappings. Draw an injective target sample from `0..82`, rejecting fixed points
because all observed mappings move. Test 1,000 controls with seed `20260726`
for full three-round endpoint compatibility.

The null measures how often this flexible low-round endpoint family accepts a
random partial permutation. It does not turn rejection into positive evidence.

## Promotion gate

A surviving context must first pass exact pair-consistency. A useful Eye lead
must then supply an independent round-function or key-schedule clue that
predicts more than one context. The unrestricted many-round pseudorandom
permutation construction is not promoted merely because arbitrary
substitutions preserve equality patterns.
