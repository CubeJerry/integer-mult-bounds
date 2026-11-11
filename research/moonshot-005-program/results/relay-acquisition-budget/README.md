# Relay acquisition budget comparison

Independent exact arithmetic and source-geometry audit for the two candidate relay acquisitions. Read `PROOF.md` for scope. No new κ and no full S8 composition claim.

From any directory, with `REPO` pointing to the programme checkout and `PACKETS` to the S003 bridge packet parent:

```sh
python "$PACKETS/relay-acquisition-budget/verify.py" \
  --repository "$REPO" \
  --lifetime "$PACKETS/lifetime-elimination" \
  --source-rows "$PACKETS/review-source-relay/SOURCE-ROWS.json" \
  --output /tmp/relay-budget.json
python -O "$PACKETS/relay-acquisition-budget/verify.py" \
  --repository "$REPO" \
  --lifetime "$PACKETS/lifetime-elimination" \
  --source-rows "$PACKETS/review-source-relay/SOURCE-ROWS.json" \
  --output /tmp/relay-budget-optimized.json
cmp /tmp/relay-budget.json /tmp/relay-budget-optimized.json
```

Expected status: `PASS_TWO_ACQUISITION_TARGET_BUDGETS`. Normal and optimized committed receipts are byte-identical. Source pins and every paid/target histogram are in `RESULT.json`. The source row packet was independently reverse-replayed in this session; no author construction module is imported here.

Research by @CubeJerry with AI assistance; source construction and predecessor credit remain in the programme dependency records.
