# Integration and independent review

This package was integrated during session S007 from the frozen author and
review artifacts listed in STAGING-PROVENANCE.json. Those scientific bytes and
the review's original source/proof pins are preserved. README gains integration
links. Staging paths are provenance, not reproduction requirements.

The independent review is in [review/REVIEW.md](review/REVIEW.md). Its checker
uses absolute staging locations internally. The added `review/run_review.py`
loads that unchanged checker and supplies repository, package and output paths.
For the eight-packet composition it resolves the unchanged, pinned independent
channel helper from the published sibling package. No mathematical or
verification routine is replaced.

Reproduce the independent check from any directory:

```sh
python3 -B review/run_review.py --repo /path/to/integer-mult-bounds \
  --output /tmp/foreign-history-channel-review
```

Expected receipt: byte-identical to `review/REVIEW-RESULT.json`. This is
independent AI mathematical/source review, not human or formal-kernel approval.
No complete supplier or new kappa is claimed. All five source foundations remain.

The frozen proof's phrase "dyadic source coefficients" is corrected explicitly
by DOC-ERRATUM.md: the retained source uses exact rational coefficients, including
2/3 and 4/3. Only this new channel's added coefficients are dyadic. All checks
already use exact rationals; no instruction, proof identity or source pin changes.
