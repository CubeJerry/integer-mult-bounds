# Itinerary-control obstruction

The proof and103 exact dual certificates show that the listed single
helper pulses cannot be repaired by arbitrary future controls at any
station on the donor's remaining raw itinerary. Controls may be jointly
chosen; stationary snapshots and coordinate mixing are granted. This is
a source-specific obstruction, not a global impossibility theorem.

From the repository root:

```sh
python research/moonshot-005-program/results/itinerary-control-obstruction/verify.py \
  --repository . --output /tmp/itinerary-control.json
python -O research/moonshot-005-program/results/itinerary-control-obstruction/verify.py \
  --repository . --output /tmp/itinerary-control-optimized.json
```

Expected output: `PASS_103_EXACT_ITINERARY_CONTROL_DUALS`. The two receipts
must agree. The verifier directly checks the certificate against the
native word, without reproducing the author's control-space search.

Files: `PROOF.md`, `CERTIFICATE.json`, `verify.py`, the two receipts, and
`SOURCES.json`. All displayed duals use final public outputs only, with
support at most three. `No new κ`.
