# Harmonic evidence and three-part arranging

These synthetic materials contain a working first-order weighted-chain analyzer
and an ordinary per-beat nearest-note arranger. Run `python demo.py` after
installing the requirements. No model download or audio device is used.

Parameters are scores, not row-normalized transition probabilities. The baseline
does not support linked unknown-chord annotations. Its arranger uses a local
most-likely chord and nearest notes; it has no global voice-leading solver.
The task text defines the requested interfaces and numerical semantics.
