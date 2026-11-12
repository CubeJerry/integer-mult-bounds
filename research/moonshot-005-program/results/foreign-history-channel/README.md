**Correction:** read [DOC-ERRATUM.md](DOC-ERRATUM.md) with the frozen proof.

# Neutral foreign-history channel

`PROOF.md` gives the exact source cuts, physical schedule, all-input endpoint identity, cost, and scope. `WORD.json.gz` is the literal73,914-op word. `RESULT.json` records its exact replay. `INPUT-CERTIFICATE.json` supplies candidate coefficients, authenticated and reconstructed by the verifier. `PINS.json` pins these artifacts.

Run from a checkout of the source repository:

```sh
python3 -B /path/to/package/verify.py \
  --source research/shared-wire-split-composition/data/final.json.gz \
  --output /tmp/foreign-history-replay
python3 -O -B /path/to/package/verify.py \
  --source research/shared-wire-split-composition/data/final.json.gz \
  --output /tmp/foreign-history-replay-optimized
```

Final common output equals the source native output. The private difference bank has the single shear `q172 += q47`, and all400 final recouplings are included. Only143 ordinary additions are added; no MOVE or owned lifetime is added. This is a partial private-native construction, not a complete multiplication bound. The source relation was discovered by the programme's budget worker; this package performs physical lowering and complete symbolic replay. Prepared with OpenAI assistance.

See [INTEGRATION.md](INTEGRATION.md) for the independent review and portable reproduction.
