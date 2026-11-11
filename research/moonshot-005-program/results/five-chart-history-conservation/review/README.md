# Independent review and exact receipts

The reviewer uses `check.py` for its own sparse rational source replay.
`causal_review.py` and `verify_duals.py` import this module, neither author
extractor. Independent AI review is not human or formal-kernel acceptance.
REVIEWED-FILES.json pins reviewed bytes; ORIGINAL-REVIEW-PINS.json preserves
original locations. From repository root:

```sh
python -B research/moonshot-005-program/results/five-chart-history-conservation/review/check.py --source research/shared-wire-split-composition/data/final.json.gz --output /tmp/global-intersection-review.json
python -B research/moonshot-005-program/results/five-chart-history-conservation/review/causal_review.py --source research/shared-wire-split-composition/data/final.json.gz --output /tmp/causal-review.json
python -B research/moonshot-005-program/results/five-chart-history-conservation/review/verify_duals.py --source research/shared-wire-split-composition/data/final.json.gz --certificate research/moonshot-005-program/results/five-chart-history-conservation/CERTIFICATE.json --output /tmp/dual-review.json
```

Full global/causal row receipts are deterministic gzip files; their uncompressed
SHA256, sizes and original names are in COMPRESSED-RECEIPTS.json. Decompress
and compare payloads with fresh outputs. Normal/optimized receipts agree.
Code uses only the standard library and pinned source, not exploration caches.
FEEDBACK-REVIEW.md covers the root proof; its exact reviewed draft is retained.
The parent FEEDBACK-INTERFACE.md updates only status/source navigation.
