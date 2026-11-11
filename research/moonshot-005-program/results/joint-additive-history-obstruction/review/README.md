# Independent verification of the 220-station history certificate

Run from any directory, supplying the three package paths:

```sh
python3 -B review.py --repository /path/to/integer-mult-bounds --package /path/to/joint-additive-history-obstruction --cut /path/to/static-history-obstruction --output RESULT.json
python3 -O -B review.py --repository /path/to/integer-mult-bounds --package /path/to/joint-additive-history-obstruction --cut /path/to/static-history-obstruction --output RESULT-OPTIMIZED.json
```

Expected: `PASS_INDEPENDENT_220_CHART_HISTORY_REVIEW`, 1,065 observations,
rank 1,056, nine complete relations, 220 station charts, 142,524 simultaneous adjoint
checks, and both adversarial controls pass. Normal and optimized receipts match.
See REVIEW.md for the mathematical proof review and restrictions.
