# Eye-mystery repository instructions

## Resume without loading the archive

Read these files in order:

1. `docs/working-set/current-state.md`
2. `docs/working-set/next-actions.md`
3. `docs/working-set/evidence-map.md` only when locating supporting detail

Do **not** read `docs/research-log.md`, `docs/open-leads.md`, or the whole
historical README to resume work. They are provenance archives and contain
many closed, superseded, and deliberately speculative branches. Search them
with `rg` for a named topic only when the working set points to a gap.

Read individual freeze/result documents only for the specific lane being
continued. Treat result documents as evidence; do not silently generalize
their conclusions.

## Maintain the working set

After a material experiment:

- update `current-state.md` only if a promoted fact or important rejection
  changes the model;
- update `next-actions.md` by replacing the completed action, not by appending
  another chronological section;
- add or revise one compact entry in `evidence-map.md`;
- write detailed method/results in a dedicated dated document;
- do not append routine work to the giant research log or legacy lead ledger.

Keep each working-set file within the line budget enforced by
`scripts/check_working_set.py`. Prefer replacement and synthesis over
accumulation. Run that checker before committing.

## Evidentiary rules

- Keep observation, frozen test, measured result, and interpretation separate.
- Disclose retrospective target selection; do not multiply dependent tails.
- Require a planted positive control for a new detector.
- Prefer held-out prediction or exact re-encryption over language score.
- Preserve clean negative results and obey their stop rules.
- Treat every fringe or later-asset theory as an isolated, binary hypothesis.
  It must supply its own complete reproducible clue/decoder chain and held-out
  consequence. Partial matches from separate theories never corroborate one
  another. A reusable technique or raw observation may transfer only with its
  original provenance and without transferring evidential weight.
- Later in-game clues may help decode an older Eye puzzle, but information
  required to construct a proposed source/key must predate construction or
  have been privately available to the developers.

## Persistent project constraints

- Discord access is strictly read-only. Never send a message, reaction, or
  call/join request. Searching and opening linked material are allowed.
- The installed Noita assets and local CrossOver installation are read-only
  evidence unless the user explicitly asks for modification.
- Practice-puzzle writeups must state the cracking method and place as much of
  the full verified solution as copyright permits directly in the document.
- Keep commits focused and push completed work to the configured repository.
