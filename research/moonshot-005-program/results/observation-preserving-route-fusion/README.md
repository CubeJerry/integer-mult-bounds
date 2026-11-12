# Observation-aware private route fusion

The actual 17-shear partial word can preserve every scalar read and shorten
1,710 private MOVEs to 405. Its common computation, private output contract,
scalar operations and ownership history remain unchanged. Read PROOF.md for
the exact transport-composition premise and the revised conditional invoice.

```sh
python3 -B build.py \
  --source /path/to/research/shared-wire-split-composition/data/final.json.gz \
  --parent /path/to/results/unit17-precompensation/WORD.json.gz \
  --invoice /path/to/results/eight-packet-budget-and-reverse/INVOICE-SOURCE.json \
  --output /tmp/route-fusion
```

Expected: 79,469 instructions, 405 raw MOVEs, 1,305 removed MOVEs, saved
t-moment about 19.80836257162453 at t=199/200. The resulting source remains a
partial construction with 191 missing private dependencies and no new kappa.

See [INTEGRATION.md](INTEGRATION.md) for the independent review and portable reproduction.
