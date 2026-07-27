# Wall-steganography transfer — results

## Outcome

The practice-puzzle rule does **not** transfer literally to the 12 translated
Noita Wall Messages. The predeclared unchanged decoder gives 98 Morse groups:
46 valid and 52 invalid. No message contains an alphabetic output run longer
than three characters, and none is intelligible.

## Exact readout

```text
G9  words= 11 groups= 1 valid= 0 longest= 0 decode=?
G7  words= 15 groups= 3 valid= 2 longest= 1 decode=E3?
G6  words= 14 groups= 4 valid= 3 longest= 2 decode=?4NE
G10 words= 24 groups= 4 valid= 2 longest= 0 decode=33??
G8  words= 26 groups= 7 valid= 4 longest= 2 decode=?EA??IU
G11 words= 42 groups= 9 valid= 5 longest= 2 decode=X??U?U?LU
G12 words= 48 groups= 8 valid= 0 longest= 0 decode=????????
G1  words=171 groups=30 valid=14 longest= 3 decode=VFG???OZ????GVF????S??WA?N3D??
G2  words= 52 groups=11 valid= 6 longest= 2 decode=1?R?V?3??SF
G3  words= 59 groups=12 valid= 6 longest= 2 decode=???J2UU??EP?
G4  words= 15 groups= 5 valid= 3 longest= 2 decode=?M?NE
G5  words= 38 groups= 4 valid= 1 longest= 1 decode=O???
TOTAL groups=98 valid=46 invalid=52
```

The corpus, protocol, and acceptance gate were fixed before these outputs were
inspected in
[`wall-steganography-transfer-freeze-2026-07-27.md`](wall-steganography-transfer-freeze-2026-07-27.md).
The exact reproduction command is implemented by
[`../scripts/test_wall_steganography_transfer.py`](../scripts/test_wall_steganography_transfer.py).

## Interpretation boundary

This rejects only a literal second layer in the current English translations
under Lymm's recovered punctuation/capitalization plus word-length Morse rule.
It does not test the original Finnish glyph stream, image geometry, other
linguistic steganography, or the Eye ciphertext. No parameter was retuned
after the negative output.
