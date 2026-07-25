# Compact working set

This directory is the authoritative resumption layer for the Noita Eye
Mystery project. It exists to prevent the chronological archive from becoming
the model's working memory.

## Load order

1. [`current-state.md`](current-state.md) — what is established now.
2. [`next-actions.md`](next-actions.md) — what to do next and what not to
   reopen.
3. [`evidence-map.md`](evidence-map.md) — where the exact proof, code, and
   negative result live.

The three files answer different questions. Do not merge them into another
long narrative.

## Archive boundary

The following are searchable provenance, not startup context:

- `docs/research-log.md` — chronological experiment archive;
- `docs/open-leads.md` — legacy breadth portfolio containing live and closed
  branches interleaved;
- the long root `README.md` — historical project narrative and command index;
- dated `freeze`, `results`, `horizon`, and `audit` documents — exact
  experiment records.

Use `rg` with a concrete noun, result name, or number to enter the archive.
Avoid reading any of those large files from top to bottom.

## Update discipline

The working set is state, not history:

- replace obsolete statements;
- keep only decision-relevant numbers;
- link to evidence instead of reproducing full reports;
- move completed actions out of the queue;
- keep speculative leads explicitly labeled;
- never erase the underlying dated result document.

Run:

```text
PYTHONPATH=src python3 scripts/check_working_set.py
```

before committing. The checker enforces file presence, local-link integrity,
and a small line budget.

