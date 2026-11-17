#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--workers', type=Path, required=True)
a = p.parse_args()
pins = {
    'R/proper-basis-coupling/PROOF.md': '206733c52a7dc86914c0ca9bd4260082c17886c43d5166e2f4ff1b6213b5aad1',
    'R/proper-basis-tradeoff/PROOF.md': '23baa438c0b33ca7f7dd60a1e65bbc2d2c8f20559efd70a21759f9341153158a',
}
for name, expected in pins.items():
    assert hashlib.sha256((a.workers / name).read_bytes()).hexdigest() == expected, name
print(json.dumps({'status': 'PASS_FINAL_AUTHOR_PROSE_PINS', 'pins': pins}, indent=2))
