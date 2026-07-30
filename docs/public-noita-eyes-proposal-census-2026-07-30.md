# Public noita-eyes proposal census (2026-07-30)

The current public repository at https://git.ignore.pl/noita-eyes contains
several independent sketches. I classified each by whether it actually
consumes the canonical Eye streams:

- automaton/machine.lua and graph.lua consume the Eye streams. The exact
  25-cell replay is negative; the graph encoder's alternate source seed is
  also negative. See public-automaton-screen-results-2026-07-30.md.
- data/disk plus disk-simple-mask.lua consumes the Eye streams. The exact
  17/20/24 three-ring mask is punctuation-only. disk-variations.lua only
  counts value coverage over disk combinations; it is not a decoder.
- wadsworth/data.lua and wandstreaming/data.lua operate on the repository's
  Hermetic sample text, not data/eyes. They supply no Eye key or prediction.
  The separate project Wadsworth/Earthquake screen is already frozen
  negative.
- cube/presets/cube.lua operates on data/hermetic with a 24-state Rubik-style
  alphabet, not the 83-state Eye corpus. It is a calibration/example cipher,
  not an Eye route.
- apotheosis.lua is a separate later dataset and does not consume the Eye
  arrays.

This census prevents those examples from being accidentally combined as
corroboration. Only the first two bullets are direct Eye-mechanism leads, and
both now have exact replays and clean negative dispositions.
