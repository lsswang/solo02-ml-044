"""Existing nearest-note arranger, useful for a supplied simple chord sequence."""
import math
import numpy as np


def arrange(chords, melody, single, pair, policy):
    previous = [lo for lo, hi in policy["ranges"]]
    choices, notes = [], []
    for t, probabilities in enumerate(single):
        chord_id = int(np.argmax(probabilities))
        pcs = set(chords[chord_id])
        row = []
        for voice, (lo, hi) in enumerate(policy["ranges"]):
            candidates = [p for p in range(lo, hi + 1) if p % 12 in pcs]
            if not candidates:
                return {"status": "infeasible", "chords": [], "pitches": []}
            row.append(min(candidates, key=lambda p: (abs(p - previous[voice]), p)))
        row[2] = int(melody[t])
        choices.append(chord_id)
        notes.append(row)
        previous = row
    evidence = -sum(math.log(single[t][c]) for t, c in enumerate(choices))
    motion = sum(abs(notes[t][v] - notes[t - 1][v])
                 for t in range(1, len(notes)) for v in range(3))
    return {"status": "ok", "chords": choices, "pitches": notes,
            "cost": evidence + policy["motion_weight"] * motion}
