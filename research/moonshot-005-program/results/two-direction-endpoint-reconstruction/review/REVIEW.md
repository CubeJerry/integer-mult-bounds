# Independent forward source and endpoint audit

Root independently reviewed the reconstructed endpoint and complete invoice. `review.py` imports none of the author's code. It starts with1,480 independent source inputs, executes every source instruction forward over exact rationals, checks every common/helper output, and verifies the COPY destination is identically zero at event31737. This differs from the author's backward-adjoint source audit.

The new word is executed on1,880 independent inputs and compared with an independently constructed two-bank E8 matrix, including all eight coupled aliases. The16-by-16 coupled block is invertible and P-I has rank104. No helper or private input is set to zero. Every cochart access, monotone public route, owned descent, lifetime and final chart is checked. Four actual-word mutations fail. Normal and assertion-disabled results agree in scientific content; elapsed time is nondeterministic.

The invoice correction is accepted: the replacement removes both6,310 old common-native MOVEs and1,710 separate old raw-main MOVEs. Its1,912 actual MOVEs give42,480 complete paid positions. The reconstructed S007 numbers were already correct; its displayed formula needed the missing subtraction. ERRATUM.md preserves that distinction.

## Reproduction

```sh
PKG=research/moonshot-005-program/results/two-direction-endpoint-reconstruction
python3 -B "$PKG/review/review.py" \
  --source research/shared-wire-split-composition/data/final.json.gz \
  --word "$PKG/output/WORD.json.gz" \
  --invoice research/moonshot-005-program/results/eight-packet-budget-and-reverse/INVOICE-SOURCE.json \
  --output /tmp/endpoint-independent.json
```

Expected marker: `PASS_INDEPENDENT_FORWARD_ENDPOINT_REVIEW`. The292 chart-map checks are credited to the retained compiler/phase engines and pinned author run, not a new root implementation. All uniform and physical obligations remain. The19,968 residual coefficients are not discharged by this partial word. Its terminal completion is separately reviewed in `../../two-direction-terminal-completion/review/`. No new kappa.

Prepared for @CubeJerry with substantial OpenAI assistance; Apache-2.0. Preserve all source, E8, H4 and S007 credit.
