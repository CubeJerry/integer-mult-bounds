# Fixed BIT query-layer target barrier

Even all four free QUERY deletions leave a negative margin at1/200, with deficit
about0.06321643234. Source-specific invoice result only; no new kappa.

```sh
python3 -B PACKET/verify.py --repository . --output /tmp/bit-query-target.json
python3 -B -O PACKET/verify.py --repository . --output /tmp/bit-query-target-opt.json
cmp /tmp/bit-query-target.json /tmp/bit-query-target-opt.json
```

Expected PASS_ENTIRE_BIT_QUERY_LAYER_TARGET_EXCLUSION; queries196,198,201,349;
445 minimum total unit credits,334 beyond freeQUERY349. No network required.
