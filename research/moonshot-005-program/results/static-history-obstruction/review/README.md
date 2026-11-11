# Independent static-history review

`REVIEW.md` records the proof audit and its exact scope. `REVIEWED-FILES.json`
pins all seven files of the proposed static-history packet.
`verify_independent.py` imports neither that implementation nor any predecessor
verifier. It uses actual chart spaces, backward graph traversal, a reverse
touch scan, literal prefix replay and exact source adjoints.

After integration, from the repository root:

```sh
P=research/moonshot-005-program/results
python3 -B "$P/static-history-review/verify_independent.py" --repository . --packet "$P/static-history-obstruction" --output /tmp/static-review.json
python3 -B -O "$P/static-history-review/verify_independent.py" --repository . --packet "$P/static-history-obstruction" --output /tmp/static-review-optimized.json
```

Expected: `PASS_INDEPENDENT_STATIC_HISTORY_CUT_REVIEW`, identical normal and
optimized JSON outputs. Review accepts the source-specific 44-field-unit
information lower bound and the current-profile requirement of at least
36 informative original-helper crossing units when at most eight new paid
full-field calls fit. No new κ or complete native is claimed.
