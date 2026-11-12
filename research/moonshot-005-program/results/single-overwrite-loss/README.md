# Single neutral-overwrite information loss

[PROOF.md](PROOF.md) proves the scoped all1,472-occurrence statement. Every
single pure-q overwrite loses exactly one independent common field unless
an additional common record is retained. It does not exclude changed
processing, swaps or joint codes. **No new κ.**

After integration, from repository root:

```sh
python3 -B research/moonshot-005-program/results/single-overwrite-loss/verify.py \
  --source research/shared-wire-split-composition/data/final.json.gz \
  --neutral research/moonshot-005-program/results/endpoint-side-information/RESULT.json.gz
```

The exact source and neutral-certificate payload are pinned. The checker
regenerates the full certificate; use `--write-certificate` only for an
intentional update. Compare decompressed bytes, not new gzip containers.
