# Route A: quantitative source costs and the complete template transfer

The current complete formula-compression bound is stated in
[`../THEOREM.md`](../THEOREM.md). Its construction and physical transfer
have passed separate root, Route A and Route C reviews; the complete
additional Route B audit is saved in
[`formula-synthesis-review.md`](../route-b/formula-synthesis-review.md).
This directory also preserves the preceding baseline, independently
useful components, a stronger conditional target and scoped negative
results. These statuses are distinct.

## Complete profiles

Let `Z_j=(j+2)^3 log_2(j+3)`, `L=1+log_2 n`, `x=log_2 L`, and
`z=log_2(x+16)`. Write `E_1(t)=2^t`, `E_2(t)=2^(2^t)`, and
`E_3(t)=2^(2^(2^t))`.

| Result | Complete finite and scheduler profiles | Status and scope |
|---|---|---|
| [Formula template transfer](formula-template-transfer.md) | `S_j<=E_2(CZ_j^2)`, `d_j,b_j<=E_1(CZ_j^2)` | Uses Route C's explicit integral cyclic factors in **both** source branches, refined rational geometry, all-shift repair, numerical bounds and the physical compiler. Gives `H<=2^{O(x(log_2^2(z+2)/z)^(1/6))}` with uniform `O(n)` visited cells. |
| [Literal source extraction](elementary-tower-extraction.md) | `S_j<=E_3(CZ_j)`, `d_j,b_j<=E_2(CZ_j)` | Earlier independently admitted baseline. It proves the sharper `log m=O(j^3 log j)` source arity and complete original-construction invoice. Its historical theorem is preserved in [BASELINE-THEOREM.md](../BASELINE-THEOREM.md). |
| [Physical compiler](compiler-invoice.md) | `a_j,c_j<=S_j^c`, `log U_j<=S_j^c+O(1)` | Source-by-source physical proof reused by both profiles. Counts fixed-tape scans, instructions, rotations, numerical precision, actual preparation microsteps, fallback and all-length scratch bounds. |
| [Refined rational geometry](rational-geometry-height.md) | Rational bit heights `poly(m)`; address values and actual generator `2^{poly(m)}` | Fixed-depth minors and shared quotient bases prevent an extra tower. Independently reviewed; overlaps and credits S002's earlier rational-height result. |
| [MR conditional transfer](single-exponential-root-hypothesis.md) | If MR holds, `S_j<=E_2(CZ_j)`, `d_j,b_j<=E_1(CZ_j)` | The transfer is proved and independently reviewed. Existence of the required `exp(poly(m))` full-input matrix root remains open. Its conditional envelope is `H<=2^{O(x(log_2(z+2)/z)^(1/3))}`. |

The full parameter map, including generation, chunk count, enumeration
index, both certificate coordinates and integer inversion, is in
[`../PARAMETER-LEDGER.md`](../PARAMETER-LEDGER.md). Absolute constants
and practical crossover lengths are not numerically evaluated. The
proofs specify efficient finite generators; they do not bound every
merely computable implementation of the source scheme.

## Local components and representation limits

- [explicit-binary-kernel.md](explicit-binary-kernel.md) gives explicit
  characteristic-zero binary parameters and a quarter-margin normalized
  call inequality. It credits the concurrent S002 compact predictor and
  is not, by itself, a complete multiplication bound.
- [repair-table-compiler.md](repair-table-compiler.md) proves a fixed
  common denominator, coefficient-height and on-demand exact bit
  compiler for that compact binary Hermite repair. Its wrapper norm
  bound is distinct from a physical query-pencil norm bound.
- [count-mod-p-obstruction.md](count-mod-p-obstruction.md) lower-bounds
  the error of a **count-residue-only** predictor in odd characteristic.
  It does not lower-bound multivariate predictors or multiplication.
- [mr-symmetry-literature.md](mr-symmetry-literature.md) audits primary
  representation results and the precise gap in a cyclic-shift
  decomposition lead. Its tensor-decomposition checks passed
  [Route C review](../route-c/SYMMETRY-REDUCTION-REVIEW.md). It records
  no additional MR construction or claim of literature exhaustiveness.

## Independent reviews and finite checks

- [FORMULA-FACTORIZATION-REVIEW.md](FORMULA-FACTORIZATION-REVIEW.md)
  checks Route C's cyclic algebra, integral descent, degree control,
  generation and independent-row identity.
- [FORMULA-RECIPE-REVIEW.md](FORMULA-RECIPE-REVIEW.md) checks the
  matching lower bound for the **unreduced syntactically multilinear
  formula recipe**, using the primary Hrubes--Yehudayoff theorem.
- [FORMULA-SIZE-TRANSFER-REVIEW.md](FORMULA-SIZE-TRANSFER-REVIEW.md)
  checks the root's general conditional formula-size transfer and its
  full coefficient/threshold inversion.
- [verify_route_a.py](verify_route_a.py) and
  [verification.json](verification.json) contain exact finite Hermite,
  predictor, odd-characteristic, cyclotomic-unit and integer-parameter
  controls. The last replay passed 1,252 repair cases, 40,329 predictor
  values, 924 unit identities and 276 specialized window values, plus
  the reported negative and integer-majorant controls. The report's
  proof hashes identify its recorded snapshot; the tests do not prove
  the asymptotic theorem.

The universal claims rest on the written constructions and cost proofs,
with independent AI-assisted reviews. No complete astronomical template,
practical benchmark, Lean refinement or independent human referee report
is claimed.

## Provenance

All source extraction uses OpenAI `math` at
`3344da59991ed94f9ba711217b29c1d760badfa6`. Concurrent S002 checkpoints
are credited where used: `bbfd1086...` for the compact binary predictor;
`96028cba...` and `4689161c...` for the earlier complete extraction,
rational heights and conditional bridge; and
`58c754b583815e4fe40d333ec9d71e4c254749ba` for an independently derived
balanced-formula full-rate construction and the same stronger envelope.
The formula composition uses the cited matrix-factorization literature.
No priority claim is made. Credit to @CubeJerry and the source authors;
developed with substantial GPT-6 Astra Pro assistance.
