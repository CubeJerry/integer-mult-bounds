# Verification of the numerical integer multiplier

The [all-length statement](all-lengths.md) and [final piecewise threshold](routing-label-walsh.md) are written proofs about one fixed physical program. The entries below distinguish source-level kernel theorems, deterministic executions and independent reconstruction of the full invoices.

| Part | Evidence and scope |
|---|---|
| Finite tape semantics | [Handoff](recount-handoff.md), [binary indexed access](compiler-binary-port.md) and [width screen](node-root-parameter.md). Selected rules use the pinned original tape rule, trace relation and absolute visited-cell predicate. |
| Recursive mass | [Volume count](child-volume.md), [ordinary costs](node-root-parameter.md), [formal child-weight inequality](native-contraction.lean). The written count includes every repeated child and full reserve. Lean verifies the analytic decrease from that mass supplier. |
| Selected Walsh | [Physical solver](walsh-node.md), [typed interpolation](walsh-repair-compiler.md), [ancestral joins](walsh-joins.md). The kernel modules establish concrete scalar, seed-rank, interpolation and rounding identities. Full recursive dispatch is written. |
| Arithmetic, phases and guards | [Toom word](word-toom.md), [independent word checks](recount-toom.md), [occupied-transform audit](address-review-outer.md), [coprime sieve](address-axis-window.md). The actual fixed-tape steps and the high-precision host oracles are distinguished in each supplier. |
| Exact integer product on a small box | At the full \(72k/80k/2048k\) precision formulas, the composite schedule recovered all 210 coefficients and the complete 2,000-bit output on four input pairs, including zero, the all-one square and an isolated bit product. Omitting inverse CRT corrupted 204 rows of the dense reference case. This host-array execution is distinct from the full-length physical clock. [System audit](recount-system-audit.md) |
| Earlier input lengths | [Schoolbook](schoolbook.md), [dyadic transform](address-dyadic-caller.md), [analytic branches](all-lengths.lean). Independent checks cover raw output, every convolution coefficient and every guarded length range. |
| Numerical threshold | [Smooth implication](full-cutoff.lean), [profile accounting](whole-profile.lean), [piecewise proof](routing-piecewise-walsh.md), [sharp certificate](recount-label-cutoff.lean). The mathematical implications hold for all subsequent lengths. Adjacent endpoints certify a threshold of a stated sufficient inequality. |
| Rate experiment | [New incidence proof](routing-cross-anchor.md), [independent reconstruction](address-review-cross.md). The two lower bounds have explicit routing-model restrictions. |

## Reproduce the claims

Use Lean 4.34.1, Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612` and OpenAI/math `3344da59991ed94f9ba711217b29c1d760badfa6`. Put the compiler and Lake on the executable search path and supply the two checkout paths below. The scripts check the revision or the immutable blobs they use.

```bash
export S008_OPENAI_DIR=/path/to/openai-math
export S008_MATHLIB_DIR=/path/to/mathlib4

bash check-clock-lean.sh "$S008_MATHLIB_DIR"
bash address-check-sieve.sh "$S008_MATHLIB_DIR"
bash address-check-staircase.sh "$S008_MATHLIB_DIR"
bash routing-check-lean.sh "$S008_MATHLIB_DIR" --label
bash recount-check-sharp.sh "$S008_MATHLIB_DIR" label
bash recount-check-lean.sh product
bash recount-check-carry.sh "$S008_MATHLIB_DIR" "$S008_OPENAI_DIR"
bash compiler-check-lean.sh
bash node-check-lean.sh "$S008_OPENAI_DIR" "$S008_MATHLIB_DIR" width
bash walsh-check-lean.sh "$S008_OPENAI_DIR" "$S008_MATHLIB_DIR"

python -I -B routing-label-walsh.py
python -I -B address-review-profile.py
python -I -B compiler-review-refined-label.py
python -I -B coefficient-53.py
python -I -B recount-system.py
python -I -B recount-system.py --inputs boundaries
```

The [lead receipt](lead-receipt.json) records selected kernel and functional replays. The final compiler suite compared 734,400 literal transition rows over four tables and 105,049 occupied test cases. The full [five-head butterfly stream](compiler-butterfly.md) has a kernel proof of its values, exact time, exact visited space and restoration of all heads. The [carry and output proof](recount-carry.lean) covers all staged coefficient rows, alternating carry banks and the actual raw result. Its input starts after the numerical transform and the separately priced formatter.

The compilers distinguish ordinary module kernel replays from the optional examination of full transitive imports. The common Mathlib axioms in the designated declarations are propositional extensionality, classical choice and quotient soundness. The cost supplier for the complete recursive machine remains a written proof. The aligned interpolation harness copies the published Fourier kernels without modification and uses the original token definition with a narrowed import. The finite-rule harnesses use the original source rule, one-step relation, raw output and cumulative visited-cell semantics. Exact table, trace, or real-variable theorems have the scopes stated in their linked modules.

The lead rebuilt and replayed the natural-input branch join, native contraction, effective 53 outer charge, axis-sieve components, literal width dispatch, signed word access, group-alignment components, exact fresh output, and endpoint comparisons. Independent reconstructions inspected the physical costs through complete return. The 1,000-bit coprime box is exercised deliberately below the production switch to test its arithmetic and ordering. It runs the full stated precision formulas; it does not observe the physical time of the asymptotic multitape machine.

The [source-level carry](recount-carry.md) counts the alternating banks and the [source audit](node-source-review.md) records which direct, gather, scatter and context-installation theorems hold at arbitrary widths. [Full true-label estimate](address-refined-label.md) · [Coefficient-53 review](compiler-review-refined-label.md) · [Final threshold and all-later extension](routing-label-walsh.md)

The optional 81-independent-bit native trace has a complete executable symbolic result. Its standalone all-kernel replay was stopped after 138 of 421 generated modules. Four other positive native fixtures completed their separate kernel proofs. The all-length and fixed-exponent theorems use the separately reviewed structural native cost; their evidence is indexed above. [Native source review](node-source-review.md)
