# Gate Guardian derived artifacts

These images are reproducible views derived from the user's installed Noita
data.  They are retained as audit aids; the repository does not copy the raw
game-data tree.

- `veska-8x.png`, `molari-8x.png`, `mokke-8x.png`, `seula-8x.png`: nearest-
  neighbour enlargements of the four static boss sprites.
- `veska-mark-layer-10x.png`, `seula-mark-layer-10x.png`: isolation of exact
  RGBA `(60,57,65,255)`.
- `assembled-static.png`: raw-resolution, dimension-derived assembly with
  Seula above, Molari/Veska/Mokke along the bottom.
- `assembled-static-6x.png`: nearest-neighbour enlargement of that assembly.
- `historical-filelist.txt`: the single-file filter used for the attempted
  historical Steam depot request.  Anonymous access was denied; no Steam
  credentials were requested or stored.

The raw sprite SHA-256 values and all numerical measurements are printed by
`scripts/analyze_gate_guardian.py`.  See `docs/gate-guardian-audit.md` for the
evidence assessment.
