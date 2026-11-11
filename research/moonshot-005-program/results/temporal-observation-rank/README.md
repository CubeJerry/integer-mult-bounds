# Timed four-observation rank obstruction

See PROOF.md for exact source-calendar, return-decoding and linear-field scope.
This result shows why funded main/owned channels and the existing quiet-loan
family cannot alone supply the four remaining historical return obligations.
At most3 additional paid messages require at least2 other helper messages with
indispensable difference information. This is a necessary interface condition,
not a complete construction or new kappa.

From repository root, with PACKET this directory:

```sh
python3 -B PACKET/verify.py --source research/shared-wire-split-composition/data/final.json.gz --certificate research/moonshot-005-program/results/historical-owned/WITNESSES.json --budget research/moonshot-005-program/results/prepaid-historical-budget/BUDGET.json --output /tmp/temporal-observation-rank.json
```

Expected:1710main/47owned grants;354quiet windows/141arcs;134unreachable input
coordinates; target rank4;2221nonquiet helper-source intersections allzero;
paid-extra ceiling3. All graph capacities are over-granted, so no passing
reachability or rank condition is a physical implementation certificate.
