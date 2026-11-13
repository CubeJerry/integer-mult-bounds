# Frozen odd-parity bilateral half-unit finite gate

## Scope lock

This frozen receipt covers only:

- \(H_4/2\), integer Gaussian coordinates, error cap one.
- Odd-total-parity inputs and outputs, with exact absolute radial change at
  most \(1/2\).
- Complete odd-parity balls \(R=5,9,11\).

The exact integer filter, quotient capacities, all positive orbit-pair flow
certificates, complete source-side Hall neighborhoods, and orbit-key
predicates are in RESULT.json. All three flow values saturate the input
universe. No radius other than 5, 9, and 11 was evaluated.

## Frozen hashes

| Artifact or replay | SHA-256 |
|---|---|
| RESULT.json | 497c020ddf7b24094e173e68cb899a313dcf5e1b8eb1deb506332296d0193432 |
| Normal isolated sweep output | 497c020ddf7b24094e173e68cb899a313dcf5e1b8eb1deb506332296d0193432 |
| Optimized isolated sweep output | 497c020ddf7b24094e173e68cb899a313dcf5e1b8eb1deb506332296d0193432 |
| Normal isolated verifier output | 6ebc4d99f1a2a4681bf806a1a16fbb3f9679a1f3e14526a408bea1dcc5e29804 |
| Optimized isolated verifier output | 6ebc4d99f1a2a4681bf806a1a16fbb3f9679a1f3e14526a408bea1dcc5e29804 |
| sweep.py | e487750ad13d69e6aae2e94f86d975fd5c8a5bc9ae838fd1453a9416ab3b9086 |
| verify.py | 93e751bfe9972dc7ed86c7a9a3582061dacb967b01874a6ebe8bf34320b6fa4b |

Both sweep modes produce byte-identical receipts, and both verifier modes
produce identical summaries. The verifier rejects an incremented flow edge
and a deleted neighborhood orbit for every tested radius.

## Source pins

- Canonical CrocSwap analysis base: e54523517d0f03e58352e647c403a5af3e525a57.
- PR #6509 and #6619 source heads and blobs: SOURCES.json and NOTICE.md.
- Biregular quotient-flow lift theorem: adjacent frozen package
  finite-radii-orbit-sweep/PROOF.md.

## Replay

Run from this directory:

~~~~sh
python3 -I -B sweep.py > /tmp/odd-half-normal.json
python3 -I -O -B sweep.py > /tmp/odd-half-optimized.json
cmp /tmp/odd-half-normal.json RESULT.json
cmp /tmp/odd-half-optimized.json RESULT.json
python3 -I -B verify.py
python3 -I -O -B verify.py
~~~~

verify.py loads the sibling sweep.py bytes directly with compile/exec, so
isolated replay does not depend on ambient import paths or cached bytecode.
CHECKSUMS.sha256 pins each package file except itself.

This finite gate establishes no unbounded Hall condition, global map,
radius pattern, or multiplication-bound claim.
