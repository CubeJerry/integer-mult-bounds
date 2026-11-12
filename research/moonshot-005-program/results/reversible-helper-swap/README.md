# Reversible dirty-helper swap

An exact73,807-instruction source word sends q60 to raw receiver213 through
original helper MOVE41779, retains the displaced260-term common row in the
original donor carrier, returns the pure signal through one new rank-1 owned
MOVE, and restores every common datum. All1,880 input directions,1,710 raw
reservations, and400 entry/final recouplings are included.

Added cost:32 ADDs, one SCALE, one rank-1 MOVE, and one INIT/CLEAR lifetime.
Peak owned storage remains43. The final raw update is q213+=q60; the remaining
private-native endpoint duties stay open. This route is already granted in the
pure-source graph, so it does not evade54/43 packet bounds or yield a new kappa.

Read PROOF.md for the chronology, exact endpoint identity, cost and limits.
Run verify.py with the pinned source and a fresh output directory. RESULT.json
and WORD-PIN.json are generated; SWAP-WORD.json.gz is the full physical word.

Independent source adjoints, typed-word comparison and universal composition review are in [review/REVIEW.md](review/REVIEW.md). The author performs the full1880-column replay; the independent reviewer reuses the authenticated native baseline and separately checks the new source cut, pulse, word and restoration.

From repository root:

```sh
python3 -B research/moonshot-005-program/results/reversible-helper-swap/verify.py --source research/shared-wire-split-composition/data/final.json.gz --output /tmp/moonshot-swap-replay
python3 -B research/moonshot-005-program/results/reversible-helper-swap/review/check.py
python3 -B research/moonshot-005-program/results/reversible-helper-swap/review/check_census.py
```
