#!/usr/bin/env python3
"""Optional NumPy replay of PR598's direction discovery order, not the proof.

Tested with NumPy 2.3.5. The default verify.py does not require NumPy and
reconstructs every direction directly from the bundled exact source pairs.
The generator recipe is DominikScholz's PR598 norm6_centers.py, not new work.
"""
from pathlib import Path
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
ns = {"__name__": "direction_reproduction", "__file__": str(HERE / "verify.py")}
exec(compile((HERE / "verify.py").read_bytes(), str(HERE / "verify.py"), "exec"), ns)
model = ns["model"]
expected = ns["read_pairs"](ns["read_json"](HERE / "DIRECTIONS.json"))
rng = np.random.default_rng(6242600)
seen = set()
found = []
while len(found) < 2601:
    i, j = map(int, rng.integers(0, model.LINES, size=2))
    x, y = model.line(i), model.line(j)
    t = model.dot(x, y)
    sign = 1 if t == -8 else -1 if t == 8 else 0
    if not sign:
        continue
    a = model.direction((i, j, sign))
    if a in seen:
        continue
    seen.add(a)
    found.append((i, j, sign))
model.require(found == expected, "source generator prefix differs")
print("PASS_LEECH_NORM6_DIRECTION_RECIPE seed=6242600 pairs=2601")
