# Sharp finite Gaussian outward slack

This package proves and checks the exact radius-five finite optimum
\(\beta=\sqrt{21}-\sqrt{19}\) for injective integer-output rounding of
\(H_4/2\) at Euclidean error at most one. A signed-permutation identity
transfers the finite optimum and global necessary lower bound to #6509's
actual ideal Gaussian pair map.

## Files

- `PROOF.md`: the finite matching, strict Hall obstruction, and exact native
  pair transfer.
- `R5-OPTIMUM.json.gz`: compact, exact certificate containing the 3,121-pair
  injection and Hall witness. Its expansion is pinned by SHA-256 in
  `SOURCES.json`.
- `replay.py`: deterministic exact expansion of the compressed certificate;
  the default command verifies and prints a receipt without writing files.
- `verify.py`: independent exact checker for the injection, Hall neighborhood,
  signed-permutation transfer, and negative controls. It imports no search or
  author checker.
- `RESULT.json`: receipt from the standard-library checker.
- `SOURCES.json`, `NOTICE.md`, `VERIFY.md`, `OPEN-NEXT-QUESTIONS.md`, and
  `PR-DRAFT.md`: provenance, credits, replay instructions, scope, and draft
  publication text.
- `CHECKSUMS.sha256`: freeze manifest for package files, excluding itself and
  transient Python caches.

## Reproduction

Requires Python 3.10+ and only the standard library. From this directory:

```sh
python3 -B replay.py
python3 -B verify.py
python3 -O -B verify.py
```

To write the expanded certificate to a chosen path, use
`python3 -B replay.py --write-certificate /tmp/R5-OPTIMUM.json`. To refresh
the committed checker receipt, redirect the exact verifier output to
`RESULT.json` explicitly. Normal verification is read-only.

The result establishes the exact optimum on the complete finite ball \(S_5\)
and a necessary global lower bound. At the global error cap one, the available
interval is only \([\sqrt{21}-\sqrt{19},1]\). No global map attaining the
lower endpoint is provided.
