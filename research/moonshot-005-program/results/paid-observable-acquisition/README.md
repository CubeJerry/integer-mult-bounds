# Two source-authentic observables acquired from actual inputs

Both prefixes form the actual 59-term δ1481 and 26-term current δ130 at 541 from all 1,880 independent physical inputs. Every dirty common input remains unchanged; all 400 raw q values are formed and preserved. Their chronology changes, and full continuation remains open.

- Direct:52 retimed donors,233 reserved calls, paid profile{7:2,2:2},730 instructions.
- Facet lifts:60 retimed donors,262 reserved calls, paid profile{1:8,2:2},783 instructions.

[PROOF.md](PROOF.md) gives both constructions, full counts, rank controls and limits. Exact prefixes and receipts are `ACQUISITION-PREFIX.json`/`RESULT.json` and `LIFTED-PREFIX.json`/`LIFTED-RESULT.json`. Matching optimized receipts accompany each. Two owned outputs still require use and retirement. **No new κ.**

From this directory:

```sh
python3 -B verify.py --source SOURCE --output /tmp/direct-acquisition.json
python3 -B verify-lifted.py --source SOURCE --output /tmp/lifted-acquisition.json
```

Expected statuses are `PASS_ACTUAL_TWO_OBSERVABLE_ACQUISITION` and `PASS_ACTUAL_TWO_OBSERVABLE_ACQUISITION_VIA_FACET_LIFTS`. `SOURCE` is the repository's `research/shared-wire-split-composition/data/final.json.gz`. The price interval files cover new Gaussian moments only; ordinary and lifecycle fees remain explicit in the complete invoice.
