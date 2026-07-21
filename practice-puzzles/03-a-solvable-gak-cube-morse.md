# A solvable GAK — solved (cube/Morse)

Source: [Discord thread](https://discord.com/channels/453998283174576133/1227024108286644284/threads/1486461163901554821), posted by `simplesmiler` on 25 March 2026.  The author later confirmed the intended first Morse letter and credited `Lymm` and `Surfinite` with solving it.  An independently replayed implementation is documented in the public [cube/Morse results](https://github.com/hansborr/noita-eye-puzzle-scratchpad/blob/main/research/data/practice-puzzles/SIX-RESULTS.md).

## Cracking method

First compare equality patterns rather than numeric labels.  The three 139-item
lines are exact relabelings of one hidden sequence.  Chaining the three
line-to-line bijections exposes the invariant opposite pairs `(1,6)`, `(2,5)`,
and `(3,4)`, identifying the six labels as cube faces.  Every observed
transition then goes between adjacent—not opposite—faces, which independently
checks that model.

Enumerate the finite cube orientations compatible with those opposite pairs and
propagate each possible initial orientation through the visible top-face walk.
Only three relative roll directions occur.  Treating those directions as a
three-symbol code, exhaust the six assignments to Morse dot, dash, and
letter-separator; the visible spaces already fix word boundaries.  One
assignment yields valid Morse across the whole message and readable language.

Thus the attack is: cross-sample isomorphisms → invariant face geometry →
finite-state orientation recovery → tiny codec assignment → Morse.

## Plaintext

```text
CUBE IS A GREAT TOY MODEL OF NON-COMMUTATIVITY.
```

## Verification and transfer

The cube walk replays all 139 symbols in each of the three relabeled lines.
Without a cube state before the first observed face, the raw data alone has a
first-mark ambiguity that also permits `FUBE ...`; the author explicitly
confirmed the intended opening Morse code is `-.-.` for `C`, closing it as
`CUBE`.

The transferable lessons are to use multiple isomorphic samples to reconstruct
the action geometry, and not to demand that the recovered physical actions are
letters—the first layer may expose a much smaller codec.  For the eyes this
supports testing in-game physical processes as action generators, but it does
not imply that the eye ciphertext itself is Morse or a cube walk.
