# sdlwdr #1 — two-cycle Wadsworth cipher

**Status:** Solved; puzzle-author confirmed.  The original generator has not
been published, so this record stops short of an independent byte-for-byte
re-encryption.

**Thread:** [A practice cipher](https://discord.com/channels/453998283174576133/1227024108286644284/threads/1353799556076146708)

## Solution

The plaintext is the English Crawford translation of **The Kalevala, Rune
XLII, “Capture of the Sampo.”**  In normalized form it begins `WAINAMOINEN OLD
AND TRUTHFUL WITH THE BLACKSMITH ILMARINEN ...`; the complete source text is
available in [Project Gutenberg's public-domain edition](https://www.gutenberg.org/files/5186/5186-h/5186-h.htm).

The cipher is a Wadsworth-like unequal-wheel construction.  Its 83 ciphertext
symbols decompose into one fixed symbol, `J`, and two 41-cycles.  After a
choice of cycle orientation and origin, the recovered cycles were:

```text
pX9?E@8mq/'rD~]U6=$);\j!2Y7Kk*P(`HLbnW"IR
#BMFCg%5A^>:iVZO1G-+,e[o.af30c<hl4QS_TdN&
```

One working interleaving of those cycles is:

```text
p>9iEZ81q-',D[].6f$0;<jl2Q7_kdP&`BLFng"5R^X:?V@OmG/+re~oUa=3)c\h!4YSKT*N(#HMbCW%IA
```

Here `~` denotes the literal-space ciphertext symbol.  The string covers all
raw symbols except `J`.

`J` is the exceptional output for a plaintext double.  It also changes which
parity class is used on the following step.

## How it was cracked

1. **Rule out an ordinary periodic key.**  Repeated-string separations had
   Kasiski gcd 1.  That made a Vigenère-like fixed period a poor explanation
   and shifted attention from absolute characters to transformations between
   equal-pattern passages.
2. **Chain long isomorphs.**  A repeated plaintext passage encrypted from two
   states induces a bijection between the ciphertext symbols in the two
   windows.  Chaining and composing those partial bijections exposed the
   effective permutation on the ciphertext alphabet.  Instead of one
   arbitrary 83-permutation, it closed as `1 + 41 + 41`: a fixed point and two
   equally sized cycles.
3. **Replace character labels by cycle coordinates.**  Once symbols were
   numbered by position around their 41-cycles, adjacent ciphertext movement
   became highly constrained.  The observed movements split cleanly by
   parity, which is not expected from a general deck shuffle or substitution.
4. **Interleave the cycles.**  The two 41-cycles can be combined into a virtual
   82-position wheel.  Correcting each ciphertext delta for its parity and
   accumulating the result modulo 42 reduces the stateful 83-symbol stream to
   a small plaintext-side alphabet.  Encountering `J` represents a repeated
   plaintext character and flips the parity convention.
5. **Finish only after the structural reduction.**  Frequency and substitution
   work on the resulting 42-symbol stream produced readable English.  A phrase
   match identified Rune XLII, and sdlwdr replied “nicely done,” closing the
   remaining orientation/origin ambiguity.

The important discovery was not the final source lookup: it was that composed
isomorph maps reveal the cycle structure of the hidden action.  Source search
became decisive only after that group reduction had produced language.

## Transfer to the Eyes

- Compose partial maps from multiple Eye isomorphs and inspect cycle type
  before assuming a familiar named cipher.
- Two large equal cycles plus a fixed point can be the footprint of two
  coprime/unequal wheels rather than an arbitrary `S83` deck action.
- Exceptional symbols may encode an event such as a double *and* alter hidden
  state; treating them only as plaintext characters can destroy the invariant.
- Kasiski gcd 1 excludes a fixed period, not stateful wheel arithmetic.

## Verification boundary

The community attack recovered the cycle decomposition, reduced the stream to
the source text, and received author confirmation.  Because the exact encoder
was not posted, this record deliberately does not claim exact replay.  The
cycle strings above are origin/orientation conventions; rotating or reversing
a cycle gives an equivalent representation.
