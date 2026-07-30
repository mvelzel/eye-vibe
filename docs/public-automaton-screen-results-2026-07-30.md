# Public 25-cell automaton screen (2026-07-30)

## Question and provenance

The public repository [noita-eyes](https://git.ignore.pl/noita-eyes) contains
commit `2eee005` (2024-11-07), titled “Sketch of Patrick's simplified
automaton/cipher mechanism.” Its `automaton/init.lua` defines five operations
on a 25-cell state arranged as `9|7|9`: pivot, up, right, down, and left. The
Eye directions `0..4` select those operations. Its `machine.lua` resets the
state for every message to the 25-character seed
`abcdefghijklm opqrstuvxyz`, applies the three operations in every canonical
Eye trigram, and emits cell 3 except every third trigram, where it emits cell
19. This is a complete authored proposal, so it can be replayed without
fitting any parameter.

The Python port is [`public_automaton.py`](../src/eye_mystery/public_automaton.py);
the screen is [`screen_public_automaton.py`](../scripts/screen_public_automaton.py).
The port was checked against the repository's Lua program for all nine
messages, byte-for-byte at the output-string level.

The same repository's earlier `graph.lua` encoder (the 2024 commits
`a2ebf34`–`419e19c`) uses the same state actions and output slots but an
alternate source-authored seed, `abcdefghiwklm opqrstuvxyz`. Replaying that
variant is also included in the script; it changes only the seed-dependent
letters and remains non-linguistic, with the same equality-agreement vector
`8/18, 11/18, 4/18, 1/9, 3/30, 9/30, 6/25`.

## Method

1. Use the accepted canonical direction streams, including their marker
   trigrams; do not remove or reorder any input.
2. Reset the 25-cell seed for each message.
3. Apply the exact five Lua permutations for each three-direction trigram.
4. Emit the exact two-slot schedule from `machine.lua`.
5. Check the complete output for readable structure and compare the seven
   registered nonliteral equality/isomorph windows. A decoder that turns those
   deliberately repeated plaintext passages into literal text should at least
   preserve their equality skeletons under this fixed reset-and-output rule.

No seed, slot schedule, operation order, alphabet, or output was selected from
the Eye results.

## Verified result

The exact outputs are:

```text
east1  rutiezfv frk dlj jeoyzlohlxzfmdf vbpiqqttskrioghqcxxqakkzuztjiisxmmojjyfyrzlptxxpzohtgorcdmogjchrrz
west1  ftuilzksckfocmegcglbqzebakiamykmxxitzxxrrs pzyclxqmzzxhhkbvzod mhfumcbxhghuarvkgryodgzoc ivpiymfiiuhrpe
east2  rmliuzv fvraftdbfbugpzdghukejutjyedyeqhcrt jatcyu qdmeexeshyqtzstqbomqxatlevouyc rhpulistq vyqbsgajxrzhlilxaszeedkvzpb
west2  otuvqayshxk sazlfdupsmyozipplkmodipdpuuqsgjxmlf fhyvvhsjux lkyoxraiayctypdbbzcgjf zmeomosgizcplziefdhc
east3  ubcdhypmqxuvlzlmhsr dmvblucocsdrrpgzuuppczmozby mlrulphhdgtjrulpgguqzhpddm zaqyubrrfctadbfmazubzybpyqieokurhgixhgpffmjsijzuyzd xyegshaadc
west3  to mqavumkmmkjduipfkuqd  eoazixzvrxg uhzgugaovybdvxsrlctyejhetbzlqxxfxryoxxlapcmfjkdzvvbeieymrphhejetzozzjbvv udvao qchgesyl
east4  jedrhpvk zssedfpgqbtrvxv kakfodo mrzfsbbqgxeasqacdrlrqfxppmrttkyrhhl msmxaz  bkxuoelxhxbqi ekkgzeuxdkoiqdmixdjgomfokmme
west4  yefpbrlxtqooefdrczh pevkgttyxxbmvhbhplvuuhhuykkypmikhqklkudyyat  yjfxcmkca xzsrcpuviixhbrludbmqcmqumvrhvdxlogjpujqqjxhbl
east5  otuvaqcgkzfftusqrpx vqeazmsmmtvtdsjlcuhhcrdmazqrfhzpluh gkcvpj uuu zqzfxzvhtijjvjbmdhxsap qugaslkggpbulkyrtroqhgls
```

Each output uses 24–25 of the 25 seed characters, has Shannon entropy
4.442–4.554 bits/character, and is visibly non-linguistic. The seven
nonliteral equality checks are all false (0/7 exact signatures); per-window
position agreements are only `8/18`, `11/18`, `4/18`, `1/9`, `3/30`, `9/30`,
and `6/25`. The copied opening also has no literal common prefix beyond an
accidental one-character match in East1/East2; the East4/East5 and East4/West4
openings diverge immediately.

## Interpretation and stop rule

This is a clean negative for the authored public automaton *as written*: it is
not a decoder of the canonical Eye streams under either source-authored reset
seed. The result does **not** reject every finite-state
automaton, a different seed, a message-level key, or a variant that excludes
the marker. Those would be new hypotheses and require independent evidence;
trying arbitrary variants after this exact negative would be parameter fitting.

The useful transferable result is methodological: an explicit developer-sized
25-cell spatial machine can be replayed exactly, but its authored output gives
no language or isomorph support. This public proposal is therefore archived as
a screened lead, not combined with Gate, Wall, or deck theories.
