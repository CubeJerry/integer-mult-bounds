# Recovered all-pair history conservation

Every first donor's original chart route has endpoint-determined receiver
histories. Restoring the 104 common Y outputs removes every receiver response
under arbitrary controls in that donor's original access set. This extends
the formerly published 77-to-189 binding to all 104 pairs. **No new kappa.**

[PROOF.md](PROOF.md) gives the exact interface and proof. S005 reported the
investigation but lost its artifacts; this package freshly reconstructs them.

```sh
python3 -B research/moonshot-005-program/results/all-pair-history-conservation/verify.py --source research/shared-wire-split-composition/data/final.json.gz --output research/moonshot-005-program/results/all-pair-history-conservation
```

Expected `PASS_ALL104_PAIR_HISTORY_IDENTITIES`: 104 pairs, 2,846 arrivals,
71,262 cuts and maximum six endpoint terms. Independent review is in `review/`.
The access condition is pairwise, not a union of all stations. Changed access,
processing and correlated receiver records remain open. All five foundations
remain. Prepared for @CubeJerry with OpenAI assistance and predecessor credit.
