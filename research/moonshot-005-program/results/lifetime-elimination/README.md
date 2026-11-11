# Late reconstruction and owned-lifetime elimination

`PROOF.md` states the uniform deletion theorem, exact source cascade, four
conditional constructions and complete paid/ordinary reference accounting.
No new kappa or completed shared supplier is claimed.

From the repository root, with `$PACKET` pointing here:

```sh
python "$PACKET/build_and_verify.py" \
  --source research/shared-wire-split-composition/data/final.json.gz \
  --invoice research/shared-core-target-obligations/INVOICE-RESULT.json \
  --certificate research/moonshot-005-program/results/owned-difference-delivery/CERTIFICATE.json \
  --outdir /tmp/lifetime-normal
python -O "$PACKET/build_and_verify.py" \
  --source research/shared-wire-split-composition/data/final.json.gz \
  --invoice research/shared-core-target-obligations/INVOICE-RESULT.json \
  --certificate research/moonshot-005-program/results/owned-difference-delivery/CERTIFICATE.json \
  --outdir /tmp/lifetime-optimized
diff -r /tmp/lifetime-normal /tmp/lifetime-optimized
```

Expected status:
`PASS_OWNED_LIFETIME_ELIMINATION_AND_COMPLETE_CONDITIONAL_PROFILES`.
The two directories have identical receipts, deletion certificates and four
deterministic full transcripts: `seven.json.gz`, `eight.json.gz`, `ten.json.gz`,
`ten_preloaded.json.gz`. Each has its full program, frames, endpoint charts and
source-event map. `CERTIFICATE.json` records deletion waves and lifetime/read
dependencies. `RESULT.json` supplies complete profiles, exact intervals, actual
ownership accounting and controls. Source pins are in `SOURCES.json`.
