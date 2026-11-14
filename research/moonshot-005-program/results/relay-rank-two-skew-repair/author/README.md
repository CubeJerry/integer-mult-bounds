# Minimum-rank skew repair and a paid two-moment forward extension

This is a source-specific partial construction, pending independent review.
It repairs the twenty-target relay's arithmetic map with a rank-two skew
preload, keeps all 104 diagonal fitting equations, and actually supplies the
new forward skew terms using two rank-nine transfers. It leaves 76 original
D outputs and the original forward/caller duties unresolved. No new kappa.

Run from this directory, replacing PREDECESSOR with the original pinned
`proper-chart-relay/author/20/WORD.json.gz`:

```
python3 -B build.py --source PREDECESSOR --out .
python3 -B algebra.py --source PREDECESSOR --output ARITHMETIC.json
python3 -B forward.py --source WORD.json.gz --out forward
python3 -B phase.py --engines PATH_TO_PROPER_RELAY_AUTHOR_DEPENDENCIES \
  --word forward/WORD.json.gz --output forward/PHASE.json
python3 -B price.py --old-price PATH_TO_PREDECESSOR_20_PRICE_JSON \
  --output forward/PRICE.json
```

Expected determinant: `3200000000 = 2^13 * 5^8`.
Core: 2219 events, unchanged movement, two additional ground lifetimes.
Forward extension: 2569 events, two additional rank-nine owned descents.
Every scalar prefix is dyadic; peak owned records remains 15.

`PROOF.md` supplies the universal rank and algebra arguments. The finite exact
checks do not constitute a complete multiplication theorem. The nominal
28.7046794479 movement room is a limiting profile screen, with no transfer of
the old finite-m or caller certificate.
