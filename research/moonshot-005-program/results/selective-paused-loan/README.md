# Selective paused-common loan

Same exact partial endpoint and73791-instruction bill as the predecessor, but
only four raw-main source occurrences are hoisted:30832,30848,42670,43452.
All1880 input columns, all common cut state, and all400 raw cut states are checked.
No new kappa; no composition with the remaining1481 or eight-current duties.

From repository root, with P pointing to this directory:

```sh
python3 -B "$P/verify.py" \
 --source research/shared-wire-split-composition/data/final.json.gz \
 --packet "$P" --output /tmp/selective-paused.json
python3 -O -B "$P/verify.py" \
 --source research/shared-wire-split-composition/data/final.json.gz \
 --packet "$P" --output /tmp/selective-paused-opt.json
cmp /tmp/selective-paused.json /tmp/selective-paused-opt.json
```

Expected `PASS_EXACT_SELECTIVE_PAUSED_COMMON_ENDPOINT_LOAN`.
The word already exists; `--write-word` deliberately regenerates it and should
be used only in a separate reproduction copy, not in the frozen package.
