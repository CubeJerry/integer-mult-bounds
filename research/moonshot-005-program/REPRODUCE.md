# Reproduce the scoped results

Run from repository root. Python3.12 was used; primary capacity uses NumPy2.3.5.
The four temporal verifiers and independent capacity/endpoint checks use the
standard library. Receipts do not establish unimplemented suppliers.

```sh
P=research/moonshot-005-program
S=research/shared-wire-split-composition/data/final.json.gz
python3 -B "$P/results/shared-core-temporal/verify.py" --source "$S"
python3 -B "$P/results/shared-core-temporal/verify_two_switch.py" --source "$S"
python3 -B "$P/results/shared-core-temporal/verify_endpoint_repair.py" --source "$S"
python3 -B "$P/results/shared-core-temporal/verify_coded_lift.py"
python3 -B "$P/results/owned-cut-capacity/verify.py" --source "$S"
python3 -I -B "$P/results/owned-cut-capacity/review/independent.py" --source "$S" --certificate "$P/results/owned-cut-capacity/CERTIFICATE.json"
python3 -I -B "$P/results/shared-core-temporal/review-endpoint/independent.py" --source "$S"
```

Expected JSON PASS markers establish the scoped checks. Key values: residual
rank≥275, two-switch all-cut nullity sum≤260, endpoint deficiency208, public
rank1479, main-on-main rank338, owned-only complement7, balanced full-input
complement63, arbitrary-helper lower bound62. The coded-interface check covers
algebra and negative controls, not an all-event observation witness. Normal
and optimized receipts are preserved beside each verifier.

The independent temporal [review README](results/shared-core-temporal/review/README.md)
documents its optional denser NumPy sweep. The
[BIT package](results/bit-selector-boundary-floor/) has its author replay and
separate lead reverse-source/Newton-root check. Imported packages retain their
own reproduction instructions. [VERIFICATION.md](VERIFICATION.md) records actual
executions; session receipts are in `sessions/2026-11-11-S001/`.

[PROVENANCE.json](PROVENANCE.json) binds imported files. SCIENTIFIC-FILES.json
freezes new scientific evidence; integrity checks do not prove mathematics.
No complete selected supplier cold replay, formal kernel or physical multiplier
was run this session.


For a fast read-only check of imported bytes, scientific manifests and reviewed
hashes, run `python3 -B research/moonshot-005-program/verify_checkpoint.py`.
Capture its stdout outside this tree before saving a new receipt here, so the
JSON syntax check does not inspect a file concurrently being written.

## S002 causal arrival theorem

```sh
python3 -B research/moonshot-005-program/results/causal-arrival-floor/verify.py
python3 -I -B research/moonshot-005-program/results/causal-arrival-floor/review/review_deliveries.py --author-certificate research/moonshot-005-program/results/causal-arrival-floor/CERTIFICATE.json
```

Expected: 984 innovations, complete record agreement and explicit payload controls.
Normal and optimized receipts are retained in the package.
