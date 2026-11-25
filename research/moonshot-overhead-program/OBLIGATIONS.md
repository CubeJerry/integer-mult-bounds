# Proof obligations

- **A1 (open):** Effective quantitative bound for template generation, parameter search, number/size of instructions and interpreter, uniform in exponent index j.
- **A2 (open):** Uniform candidate runtime A_j and threshold N_j with all numerical precision, CRT, movement, padding, regeneration, interchanges and constant tape counts charged.
- **A3 (partially established from source):** Scheduler upper bound in terms of a *successful* fixed indexed attempt. See TARGET-OVERHEAD.md.
- **B1 (open):** Construct a family admitting constant-fraction predictor failures with exact identification and recovery at full rate; specify information and input-output contracts.
- **B2 (open):** Prove the entire recursive repair caller is strictly cheaper after routing, conversions, erasure and head travel; linear visited-cell space uniform in n.
- **C1 (open):** Establish sharp lower bounds for the actual central spectral predictor model, specifying field, weights, exceptional set structure and repair; do not generalize to arbitrary algorithms.
- **G1 (open):** Prove any new conditional or unconditional overhead claim from a complete exact recursion with a single uniform machine.

## S002 refinement

| ID | Status | Exact obligation or result |
| --- | --- | --- |
| S2-A1 | Proved component; independently reviewed/replayed | Prefix-weighted schedule including legal finite caps and fallback; see Route A A1-A2. |
| S2-A2 | Proved component; independently reviewed/replayed | Diagonal chunk convolution and carry propagation in O(nr) wrapper work, O(n) extra cells. |
| S2-A3 | Open global dependency | Explicit profiles (a_j,c_j,d_j,g_j,U_j) for source candidates, with all generator, compiler, precision, routing, padding and tape work. |
| S2-P1 | Proved characteristic-zero component | Compact limited-independence shifts and a scalar factored count predictor; not a finite-field implementation. |
| S2-L1 | Partial/enabling | Parameter-explicit interchange-label upper bounds; global physical costs are not eliminated. |
| S2-B1 | Proved rational component; independently reviewed/replayed | Pairwise shifts, exact Newton interpolation and discrepancy division with actual support handling. |
| S2-B2 | Proved finite recurrence component; recovered with provenance | Finite batch contraction has O(sqrt(m)(R_m+1)) recursive calls per input row. |
| S2-B3 | Open global dependency | Dense check/lift arithmetic, growing-parameter coefficient tables, routing, tape layout and common linear space. |
| S2-C1 | Proved scoped obstruction; independently reviewed/replayed | Exact ordinary-count-polynomial defect bound and rare-error degree; characteristic-zero scope is essential. |
| S2-C2 | Under review | Incompatibility between small-characteristic count-only prediction and the published interchange contraction. |
| G1 | Open | A complete exact fixed-machine overhead theorem. No new complete overhead bound. |

## Focused epsilon-uniformity E001

- **EU-GRAM (proved, scoped):** retained interchange Gram dimension is at least `2^(2p-1)+1`. Its reserve contraction forces a count window longer than characteristic p. A scalar function of the reduced count cannot predict parity on that window. See [proof](results/epsilon-uniformity/INTERCHANGE-OBSTRUCTION.md) and separate review. This does not invalidate multivariate integral prediction.
- **EU-SELECT (open):** construct a fixed-tape preflight that certifies complete execution costs and common space before direct selection; no free interpreter or omitted compilation.
- **EU-REC (complete conditional component):** a uniform one-level binary reduction with near-critical child-volume mass, polynomial local work and the stated stack contract yields `O(V sqrt(e))` interchange. See [contract](results/epsilon-uniformity/route-c/NONSTATIONARY-RECURSION.md). These hypotheses are not supplied by the current paper.
- **EU-PAD (proved, scoped):** literal fixed-radix padding under a power-selected growing template violates uniform linear space. Input-dependent radix selection or a different representation remains open.
- **EU-TOLL (proved invoice obstruction):** a nonvanishing normalized Walsh routing toll accumulates across unbounded depth; summable homogeneous excess alone is insufficient. No runtime lower bound is asserted.
