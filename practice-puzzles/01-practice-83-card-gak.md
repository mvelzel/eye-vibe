# Practice 83 card GAK cipher — solved

Source: [Discord thread](https://discord.com/channels/453998283174576133/1227024108286644284/threads/1528485978099028078), posted by `orionsayshi` on 19 July 2026.

## Cracking method

This was not a blind identification problem: the post deliberately supplied
the rules behind a spoiler.  The useful cracking question was whether those
rules made each ciphertext symbol locally invertible, without guessing words.

Maintain the current ordered deck.  At each position, first apply the common
Mongean base shuffle.  Then try the only 26 possible letter actions—cuts
`1..26` for `A..Z`—and compare the resulting top card with the observed
ciphertext value.  There is exactly one matching cut at every one of the 89
positions.  Commit that letter and deck state, then continue.

The relevant construction is therefore only:

1. Perform a Mongean shuffle: draw from the old top and place successive cards
   alternately on the top and bottom of a new pile.
2. Convert the letter with `A=1, ..., Z=26` and cut that many cards from the top
   to the bottom.
3. Emit the new top card.

The attack reduces an apparent stateful `S83` search to 89 independent
26-choice tests.  No language score, crib, or backtracking is involved.

## Plaintext

```text
hello i hope you found this cipher interesting let me know if you noticed any weaknesses or quirks thank you
```

The posted plaintext omits spaces:

```text
helloihopeyoufoundthiscipherinterestingletmeknowifyounoticedanyweaknessesorquirksthankyou
```

## Verification and transfer

`tests/test_practice_gak.py` converts the recovered letters back to cuts and
reproduces all 89 ciphertext values exactly.  The useful transfer is to test
whether a proposed action family is **locally separating**: from each reachable
state, do its 83 candidate actions emit distinct observables?  If so, a hidden
state cipher may decode greedily.  The real eyes do not disclose this action
family, so the family must first be justified independently.
