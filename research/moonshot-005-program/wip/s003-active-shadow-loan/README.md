# Active scalar reads and writes during a helper loan

A one-field owned shadow and exact coefficient debts permit source scalar reads and writes while a helper carries a difference payload. When the donor escrow and all nonzero debt fields reunite, the common state is restored exactly. Two full 1,880-input instances add no Gaussian MOVE.

- [PROOF.md](PROOF.md): general lemma, two instances, complete costs and limits.
- [active-shadow-word.json.gz](active-shadow-word.json.gz):73,794 typed instructions with all 800 boundary ADDs.
- [verify.py](verify.py), [RESULT.json](RESULT.json), [RESULT-OPTIMIZED.json](RESULT-OPTIMIZED.json): exact all-column verification and negative controls.
- [census.py](census.py), [CENSUS.json](CENSUS.json): scoped 80-candidate/34-closure census. Granting all 34 does not reduce the 102 missing endpoint coefficients.

From the integrated repository root:

```sh
python3 -B research/moonshot-005-program/results/active-shadow-loan/verify.py \
 --source research/shared-wire-split-composition/data/final.json.gz \
 --output /tmp/active-shadow.json
python3 -B research/moonshot-005-program/results/active-shadow-loan/census.py \
 --source research/shared-wire-split-composition/data/final.json.gz \
 --output /tmp/active-shadow-census.json
```

Expected statuses: `PASS_EXACT_ACTIVE_SHADOW_LOANS` and `PASS_SCOPED_IMMEDIATE_CLOSURE_CENSUS`. This is a partial linear primitive on a raw difference bank. Full difference continuation and supplier/precision admission remain open. **No new κ.**
