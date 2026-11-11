# Fourteen-return quotient and history interface

Source-bound proof and conditional observation reduction; no new kappa.
The certificate has rank10, an exact nonzero minor,13 history/entry reductions,
and the explicit event37606 functional row[0]+row[20] with target response4.
No physical decoder or complete tariff follows from symbolic membership.

From repository root, reproduce to temporary outputs:

```sh
P=research/moonshot-005-program/results
python3 -B "$P/quotient-history/verify.py" \
  --source research/shared-wire-split-composition/data/final.json.gz \
  --current "$P/owned-difference-delivery/CERTIFICATE.json" \
  --historical "$P/historical-owned/WITNESSES.json" \
  --budget "$P/prepaid-historical-budget/BUDGET.json" \
  --certificate /tmp/quotient-history-certificate.json \
  --output /tmp/quotient-history-result.json
```

Expected PASS_FOURTEEN_RETURN_QUOTIENT_AND_HISTORY_REDUCTION, rank10, history
counts10/3/1, dual response4 and a positive rank4 fresh-delivery price exclusion.
Use the actual integrated directory name if the orchestrator renames this folder.
