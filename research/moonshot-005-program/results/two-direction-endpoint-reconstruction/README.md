# Two-direction endpoint reconstruction

**Exact partial word; no new kappa.** This reconstructs the interrupted S007 recipe, finishes a fresh all1,480-output source audit, preserves the exact1,880-input candidate map, and corrects the written full-invoice formula. It does not supply the19,968 missing residual coefficients.

- PROOF.md: construction, input preservation, exact source targets and limits.
- ERRATUM.md: precise correction to the reconstructed S007 invoice formula.
- output/WORD.json.gz: newly reconstructed6,952-event word.
- output/RESULT.json: exact word, inverse, mutation and conditional invoice results.
- output/SOURCE-AUDIT.json and SOURCE-ENDPOINTS.json.gz: fresh complete backward-adjoint source audit, including all1,080 helpers and the actual COPY guard.
- output/CHART-MAPS.json:292 introduced pairs checked with credited retained exact engines.
- SOURCES.json: exact predecessor bytes.
- VALIDATION.json: this S008 execution coverage; independent root review is separate.

## Reproduce

From repository root, after placing this package at results/two-direction-endpoint-reconstruction:

```sh
REC=research/moonshot-005-program/results/two-direction-endpoint-reconstruction
SRC=research/shared-wire-split-composition/data/final.json.gz
INV=research/moonshot-005-program/results/eight-packet-budget-and-reverse/INVOICE-SOURCE.json
python3 -B "$REC/audit_source.py" --source "$SRC" --output "$REC/output"
python3 -B "$REC/reconstruct.py" --source "$SRC" --invoice "$INV" --outdir "$REC/output"
python3 -B research/moonshot-005-program/results/complete-first-family/check_chart_maps.py \
  --repo . --parent "$SRC" --word "$REC/output/WORD.json.gz" --output "$REC/output/CHART-MAPS.json"
```

Expected source marker: PASS_FULL1480_SOURCE_ENDPOINTS_AND_COPY_GUARD.
Expected reconstruction marker: PASS_RECONSTRUCTED_TWO_DIRECTION_PARTIAL_WORD.
The inherited map checker retains the legacy FIRST_FAMILY status label; its actual receipt binds this candidate word and all292 new pairs.

The constructor also passes under python3 -O; canonical decompressed word and residual payloads agree. Timings are nondeterministic metadata. The unavailable historical gzip hash is retained as provenance, not treated as a mandatory regenerated-container hash.

The subsequent two-direction-terminal-completion package proves that cheap repair appended to this exact boundary fails, and supplies an attaining but too costly completion. Earlier joint encoding remains open.

Prepared for @CubeJerry with OpenAI assistance; Apache-2.0. Retained source, E8, native, caller, compiler and chart-engine contributors keep their attribution.

