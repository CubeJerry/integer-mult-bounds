# Reproduce the terminal-reuse source

Run from repository root, using fresh scratch outputs instead of changing frozen evidence.

```bash
python3 research/moonshot-005-program/results/bit-common-terminal-reuse/author/build_reprogram36.py --repo . --out /tmp/moonshot-terminal36
python3 research/moonshot-005-program/results/bit-common-terminal-reuse/author/closure36.py --repo . --out /tmp/moonshot-terminal36
python3 research/moonshot-005-program/results/bit-common-terminal-reuse/independent-review/check.py --repo . --base research/moonshot-005-program/results/bit-composed-coded-source/author/output/WORD.json --word /tmp/moonshot-terminal36/WORD.json --engine research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py --author-price /tmp/moonshot-terminal36/PRICE.json --closure /tmp/moonshot-terminal36/CLOSURE.json --out /tmp/moonshot-terminal36-review.json
```

Expected markers: PASS_ACTUAL_NEW_COMMON_TERMINAL36, PASS_ACTUAL36_FROZEN_INFORMATION_AUDIT, PASS_INDEPENDENT_ACTUAL36_SOURCE_AND_PRICE. Rebuilt word SHA256: `af51d0d7c872dbf3fa3744b582769d4c7763e0747e57c74005d091d19b7da474`.

The review imports only separate interpreter functions from the leaf-capacity checker, not its theorem. There is no circular mathematical dependency.
