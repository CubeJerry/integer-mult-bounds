# Fused seven-return reference

Read `PROOF.md` for the exact conditional construction. The paid profile is
unchanged from S7, but its26 observer terms become22 and its71294 instructions
become71286. No new kappa and no completed shared supplier are claimed.

From the repository root, with `$PACKET` pointing to this directory and `$S7`
pointing to the seven-rewrite packet:

```sh
python "$PACKET/build_and_price.py" \
  --source research/shared-wire-split-composition/data/final.json.gz \
  --invoice research/shared-core-target-obligations/INVOICE-RESULT.json \
  --certificate research/moonshot-005-program/results/owned-difference-delivery/CERTIFICATE.json \
  --seven-result "$S7/RESULT.json" \
  --transcript /tmp/fused-seven.json.gz --output /tmp/fused-seven.json
```

Repeat with `python -O` and separate output names; both receipts and deterministic
transcripts should match. Expected status:
`PASS_FUSED_SEVEN_REFERENCE_AND_UNCHANGED_CONDITIONAL_PRICE`.

`fused-reference.json.gz` contains the full typed71286-instruction reference
word, source-index module map, all frames and endpoint chart declarations.
Its 400-input q domain is explicit. `RESULT.json` provides the complete integer
profiles, exact margin bounds, operation/lifecycle accounting and controls.
