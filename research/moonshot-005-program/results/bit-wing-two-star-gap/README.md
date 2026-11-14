# Two augmented stars force a44/5 wing rank bound

**proved all-field rank>=44V/5; characteristic-two widths1-4 exact9V; commuting blocks cannot beat9V. No new kappa.**

See [admission](ADMISSION.md), [full proof](author/PROOF.md), [independent review](review/REVIEW.md), and the frozen author/review receipts. Source pins and all scope restrictions are retained.

From the repository root with Node available:

```sh
P=research/moonshot-005-program
node "$P/results/bit-wing-two-star-gap/author/check.mjs" "$P/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json"
node "$P/results/bit-wing-two-star-gap/review/check.js" "$P/results/bit-proper-flat-cubic-generators/author/RESULT.json"
```

Expected PASS statuses and exact values are in the corresponding RESULT.json files. The pure mathematical functions were executed in cloud V8; the filesystem wrappers were not run through local Node after the outage. A finite receipt supplements the stated proof and does not establish an unimplemented supplier.
