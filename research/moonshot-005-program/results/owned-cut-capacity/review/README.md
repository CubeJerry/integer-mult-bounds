# Independent capacity verification

From the repository root, replace REVIEW and PACKAGE with the review and
owned-capacity package paths:

```sh
python3 -I -B REVIEW/independent.py \
 --source research/shared-wire-split-composition/data/final.json.gz \
 --certificate PACKAGE/CERTIFICATE.json
```

Expected: PASS_INDEPENDENT_OWNED_CAPACITY_REVIEW. The implementation uses
only the standard library and imports no author's scientific code. Normal
and optimized receipts agree. REVIEW.md distinguishes exact ranks, abstract
observation counts, live/allocated fields, and unbuilt physical delivery.
REVIEWED-FILES.json binds the author evidence examined.
