# Seven joint E8 residual corrections

The literal 76,060-operation word combines the retained eight-packet prefix with five actual donor controllers and six causal common-history decoders. Seven specified residual terms are removed, all 4,985 others are unchanged, and every common native output is restored. All 400 final recouplings and all 1,710 original raw MOVE reservations are included.

At receiver172 the decoded correction is the single aggregate `-(q37+q47)/4`; the two donor columns are not independently observable. The correction adds five stationary caches, 1,207 ADDs and five INIT/CLEAR pairs over the existing complete common/raw/boundary/E8 bill, with no new MOVE. Peak owned occupancy remains43.

```sh
python3 -B /path/to/package/verify.py \
  --source research/shared-wire-split-composition/data/final.json.gz \
  --output /tmp/e8-seven-corrections
python3 -O -B /path/to/package/verify.py \
  --source research/shared-wire-split-composition/data/final.json.gz \
  --output /tmp/e8-seven-corrections-optimized
```

`PROOF.md` gives all cuts, routes, receiver weights, interference, identities, and costs. `RESULT.json` records the complete 1,880-input replay. `PINS.json` authenticates the final artifacts. This is a partial construction; all remaining residual and private reverse duties remain open. Prepared with OpenAI assistance.
