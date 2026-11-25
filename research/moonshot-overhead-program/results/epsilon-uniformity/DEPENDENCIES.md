# Dependency map and remaining proof obligations

This map describes E001's dyadic theorem, conditional representation routes and
restricted obstructions. The detailed numerical profile is in
[PARAMETER-LEDGER.md](PARAMETER-LEDGER.md). Every claimed time includes actual
tape movement; every claimed space bound concerns the union of visited cells.

## 1. Admitted complete dyadic path

Write `Z_j=(j+2)^3 log_2(j+3)` and `E_r` for a tower of `r` twos.
The following interfaces compose in order; none of the conditional rows in
Section 2 is a premise of this path.

| Interface | Established output | Proof and scope |
|---|---|---|
| Source labels and recurrence slack | `log m_I=O(Z_j)`; binary Fourier arity is smaller; strict uniform contraction margins | [Route A extraction](route-a/elementary-tower-extraction.md), Sections 2–3. Constants depending on characteristic are explicitly bounded. |
| Integral predictor and full-row repair | Balanced formula and cyclic factorization give a dyadic affine root on every input row; complete budget `Q_m<=E_2(C log²(m+2))` | [Algebra and generator](route-c/FORMULA-FACTORIZATION-COMPRESSION.md), [complete transfer](route-a/formula-template-transfer.md). All shifts and both transform branches are included. |
| Finite scalar and geometric preparation | Total finite budget `S_j<=E_2(C Z_j²)` | Formula transfer and refined rational geometry: all rows, coefficients, role lists, address integer values, radix, generation time and workspace are counted. |
| One physical candidate | `a_j,c_j<=S_j^c`, `log U_j<=S_j^c+O(1)`; exact outputs and all-length space `c_j(u+1)` | [Compiler invoice](route-a/compiler-invoice.md). Sequential head scans, triangular rotations, precision, actual setup clock, scratch marks and immutable-input fallback. |
| Common-space attempt | `A_j<=S_j^c`, `log N_j<=S_j^c+O(1)` | [Chunk lemma](route-b/linear-chunk-overhead.md): `r^2 t(ceil(n/r))+O(rn)` with reused candidate workspace, then the fixed outer fence. |
| One fixed weighted schedule | `O(n+2^{i_j}(t+1))`, `i_j=O((j+log S_j)^2)` | Source `uniformity.tex` and [CERTIFICATE.md](CERTIFICATE.md). Generation, clocking, failed attempts, cleanup and output are charged. |
| Joint profile and inversion | `d_j,b_j<=E_1(C Z_j²)` and the envelope in [THEOREM.md](THEOREM.md) | Integer parameter choice proves both feasibility and cost; the optimizing index is an analysis witness, not machine advice. |

The earlier [baseline](BASELINE-THEOREM.md) path had two height-three expenses: the literal
monomial tensor predictor and the conservative address-value estimate.
[Rational geometry](route-a/rational-geometry-height.md) sharpens the latter
to `2^{m^{O(1)}}` numerical values using fixed-depth minor formulas. Its
independent review is [RATIONAL-GEOMETRY-REVIEW.md](route-c/RATIONAL-GEOMETRY-REVIEW.md).
The balanced-formula representation separately removes the predictor layer. Both improvements are used in the current theorem; baseline files retain their historical profiles.

## 2. Further dyadic routes and exact outstanding interfaces

| Route | Proved implication or component | What is still required for a stronger complete multiplier |
|---|---|---|
| Sound bounded preflight | [Theorem P2](route-b/preflight-selection.md): one fixed machine has `H=O(x^a)`, including bounded overhead at `a=0`, under the stated joint family bounds | Construct the actual physical plan family with the `j^a` execution bill, linear-in-`j` threshold coordinate, and charged generation/checking bound. These conditions are not established for the source family. |
| Singly-exponential full-rate predictor (MR) | [Complete conditional transfer](route-a/single-exponential-root-hypothesis.md) gives `H<=2^{O(x(log(z+2)/z)^(1/3))}` under an actual `exp(poly(m))` matrix-root generator | Establish MR with all independent rows, stages, basis data and bit costs. The present formula construction has the larger `E_2(O(log²m))` budget. |
| General formula-size improvement | [Formula-size transfer](FORMULA-SIZE-TRANSFER.md) maps degree-preserving formula bounds into complete overhead rates | Supply a valid uniformly generated family with the stated coefficient and syntactic-degree bounds. Multilinear formula optimization alone cannot reduce the current unreduced matrix-rank scale. |
| Additive macro dispatch | [M1–M3](route-b/macro-dispatch-transfer.md) separate description traversal from the physical primitive costs | Supply the complete fixed opcode library with actual movement, numerical error, shape and fixed-origin region contracts. Dense row maps and coefficient access remain charged. |
| Variable-arity endpoint recurrence | [Route C recurrence theorem](route-c/NONSTATIONARY-RECURSION.md) proves the endpoint interchange under summable local excesses and subcritical tolls | Realize those one-level contracts with a uniform compiler; additionally control the separate Walsh and multiplication tolls. The interchange implication is not a multiplication theorem. |
| Input-dependent radix | [Constructive radix lemma](route-c/INPUT-DEPENDENT-RADIX.md) provides compatible primes, bounded or summably small padding loss and a charged search | Generate the compatibility data and implement the resulting varying-radix address maps within the complete recurrence and visited-space budget. |

Concurrent S002848fbf1 establishes the MR displayed rate by a different characteristic-two IP4 construction. The dyadic MR premise itself remains open. See the current programme links in [README.md](README.md).

The generic preflight implication has stronger possible conclusions than the
admitted source extraction, but also stronger unresolved family hypotheses.
Its status should not be summarized as an unconditional polylog-log bound.

## 3. Restricted obstructions and what each forces us to change

| Result | Precisely ruled-out inference or construction | Routes left open |
|---|---|---|
| Growing certificate constants | `d_j->infinity` implies the sufficient envelope `F(x)->infinity`; the specified full diagonal order also gives `F(x)>=c x^(2/3)` | Tighter analysis of the same machine, different schedules, direct selection, or different algorithms. No actual-runtime lower bound follows. |
| Characteristic/reserve conflict | [Gram dimension and reserve](INTERCHANGE-OBSTRUCTION.md) force a count window containing aliased residues of opposite parity | Multivariate integral predictors retaining the individual queries, changed labels, or changed repair. |
| Literal transfer modulo `p^2` | [Factor-rank theorem](PADIC-LIFT-OBSTRUCTION.md) shows a large rank for the retained zero/one transfer; S002 proves a complementary support-preserving rank-product inequality | Transfers with different support/corrections, different coefficient mechanisms, or a different routing interface. These are not lower bounds on all multiplication machines. |
| Exact Hamming-window depth | [W1–W2](route-c/WINDOW-PREDICTOR-DEPTH.md): degree and affine-pencil depth are at least window width, regardless of row enlargement | Compact row representations at the same depth, different error promises or repairs, or independently proved cheaper stage accounting. |
| Window versus full conversion | In the stated all-shift, window-marked protocol, the minimum of `D+m Pr(outside)` is `Theta(sqrt(m log m))` | A different shift distribution, a smaller actual marked set, changed repair, or different conversion. The assertion concerns a specified two-resource invoice. |
| Unreduced multilinear formula recipe | [Matching rank theorem](route-c/FORMULA-RECIPE-LOWER-BOUND.md) gives `K>=E_2(c log²m)` for the exact retained predictor and literal cyclic composition | Nonmultilinear cancellation, quotient identities, invariant summands, different composition, or changed predictor/repair. No arbitrary matrix-root lower bound follows. |
| Literal fixed-radix padding | [The plateau obstruction](route-c/SOURCE-PADDING-BARRIER.md) violates a common linear-space budget for the specified power-selected materialization | Input-dependent compatible radices, alternative layouts, compression, or a different template selector. |

These obstructions cannot be added together as a lower bound without a common
model and a proof that every candidate mechanism satisfies all their premises.
In particular, S002's pairwise-independent constant-tail repair changes the
window/repair interface and is not excluded by the window-marked tradeoff.

## 4. Review and reproducibility boundaries

The current formula theorem passed separate Route A algebra, Route C composition, root complete-proof and [Route B final synthesis](route-b/formula-synthesis-review.md) audits. The complete original extraction passed independent compiler and synthesis
reviews. [Route B's synthesis review](route-b/global-synthesis-review.md)
records hashes matching checkpoint `0961d2083f80429dde4b6ec5197585f727c7f87b`.
Exact Python checks cover finite algebraic identities, scheduling, carries,
integer selectors and negative controls; they do not prove the asymptotic
theorem by testing it. No complete astronomical template has been executed.

The source prime-gap cutoff and absolute compiler constants are left as
mathematical constants. The machine uses checked shapes and fallbacks rather
than receiving these constants as advice. A numerical crossover, practical
implementation, Lean formalization of this refinement and independent human
refereeing remain outside the established result.

Credits: @CubeJerry; the pinned OpenAI manuscripts and cited predecessors;
the original moonshot programme; concurrent S002 results; and the separate
E001 construction, uniformization and obstruction workers. Substantial
OpenAI GPT-6 Astra Pro assistance is disclosed throughout the proof records.
