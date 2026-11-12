# Dyadic eight-packet prefix for the persistent programme

The [proof](PROOF.md) and literal `PREFIX.json.gz` provide a2,362-instruction,
1,880-input partial construction on the pinned native. It charges eight rank9
calls and all prefix ordinary/lifecycle work. Required weighted corrections
and the complete shared execution remain open. **No new κ.**

From repository root after integration:

```sh
python3 -B research/moonshot-005-program/results/eight-packet-prefix/verify.py \
  --source research/shared-wire-split-composition/data/final.json.gz
python3 -O -B research/moonshot-005-program/results/eight-packet-prefix/verify.py \
  --source research/shared-wire-split-composition/data/final.json.gz
```

Expected status: `PASS_ACTUAL_DYADIC_EIGHT_PACKET_PREFIX`.
Use `--write-word` only for intentional regeneration; compare the decompressed
payload, not a newly generated gzip container. The published source gzip is
byte-pinned. Exact arithmetic uses Python's standard library.

Prepared for @CubeJerry with OpenAI assistance. Apache-2.0. The E8 Gram
representation and earlier native/caller work retain predecessor credit;
this package does not claim a new rank-eight representation or supplier.
