# Seven corrections with fused private routes

The actual seven-correction E8 word is rewritten from 76,060 to 74,757 instructions by replacing unobserved private MOVE chains with direct nested calls. All decoder/control accesses, common operations, corrected coefficients, remaining 4,985 coefficients, and final endpoints are unchanged. Raw calls drop from 1,710 to 407, with total raw rank 3,200 unchanged and peak owned occupancy 43.

The conditional caller invoice is `P4 + 18*(R_new-R_source) + 18*8*{rank9}`. Its rigorously bracketed remaining moment is approximately 46.9617948198138 per native. This is a partial construction with unresolved residual and private reverse duties, not a new complete multiplication bound. Removed source stops are unavailable as free access.

```sh
python3 -B build.py \
  --source /path/to/research/shared-wire-split-composition/data/final.json.gz \
  --parent /path/to/eight-packet-seven-corrections/WORD.json.gz \
  --invoice INPUT-INVOICE.json --output /tmp/seven-fused
python3 -B replay.py \
  --source /path/to/research/shared-wire-split-composition/data/final.json.gz \
  --parent /path/to/eight-packet-seven-corrections \
  --word /tmp/seven-fused/WORD.json.gz \
  --output /tmp/seven-fused/TYPED-REPLAY.json
python3 -B check_chart_maps.py \
  --repo /path/to/integer-mult-bounds \
  --parent /path/to/eight-packet-seven-corrections/WORD.json.gz \
  --word /tmp/seven-fused/WORD.json.gz \
  --output /tmp/seven-fused/CHART-MAPS.json
```

The chart compiler requires assertions enabled; do not run that last command with `-O`. The builder and typed integration replay are also checked under optimized Python. `PROOF.md` explains the exact reuse of root's reviewed rewrite and the parent interpreter, the new provenance, and the exact invoice. `CHART-MAPS.json` contains the 209 verified introduced maps. Prepared with OpenAI assistance.
