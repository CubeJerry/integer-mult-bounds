# Frozen commands and claim limits

Run from `/workspace/scratch/19b21bdb3d72`:

```sh
python3 -B worker-a/public-carrier943/check.py --out worker-a/public-carrier943/RECEIPT.json
python3 -B -O worker-a/public-carrier943/check.py --out worker-a/public-carrier943/RECEIPT-O.json
python3 -B worker-a/public-carrier943/import_gate.py --seconds 60 --out worker-a/public-carrier943/IMPORT-RECEIPT.json
python3 -B -O worker-a/public-carrier943/import_gate.py --seconds 60 --out worker-a/public-carrier943/IMPORT-RECEIPT-O.json
```

The exact source hash is checked by both programs. The one-injection
receipts compare exactly. The import receipts compare after dropping only
`seconds` and `prefix_seconds`; all domains, literal ranks, controls, directed
budgets and decisions compare exactly. The source-prefix replay and all67
one-import cases complete well within the60-second cap. `CHECKS.json` binds
the proof, code, receipts, frozen constructor and signed moment inputs.

All controls use explicit exceptions and run identically under `-O`.
The rational computations have no floating-point rank or sign decision;
floating elapsed times only enforce the declared research cap. No source word
was changed, no paid child was emitted, no public zero-reframe was admitted,
and no complete κ or unconditional multiplication theorem is claimed.

This is local research evidence with retained predecessor attribution.
Relevant original source notices remain at `reference/pr7481/NOTICE`.
The no-extra-observation one-ADD argument covers all common-empty-frame
insertion cuts by proof, not by replaying35427 edited native words. The
67-domain import test covers only the latest injection cut, one imported
arbitrary history combination and actual available canonical source frames.
The strict-history and one-import restrictions are essential.
