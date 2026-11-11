# Independent active-helper observation review

The review accepts 31 separate exact source observation modules and the
literal 1,880-input partial word. It independently verifies all common and
raw input columns, source history, gain, route reservations, COPY validity,
ownership and costs. Sixty off-hub common residuals remain after the
372 hub corrections;400 final recoupling ADDs remain owed. No new κ.

After integration, from repository root:

```sh
P=research/moonshot-005-program/results
python3 -B "$P/active-helper-observation/review/verify_independent.py" --repository . --packet "$P/active-helper-observation" --output /tmp/active-helper-review.json
python3 -B -O "$P/active-helper-observation/review/verify_independent.py" --repository . --packet "$P/active-helper-observation" --output /tmp/active-helper-review-optimized.json
```

Expected `PASS_INDEPENDENT_31_OBSERVATIONS_AND_1880_INPUT_CORE` and matching
receipts. `REVIEWED-FILES.json` binds the exact packet reviewed.
