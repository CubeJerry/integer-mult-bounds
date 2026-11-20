# Worker B review of incoming-message elimination

**Accepted as a conditional fixed-surrounding refinement.** I checked the equations in `root-review/INCOMING-MESSAGE-REDUCTION.md` against the admitted source-hub completion theorem. They are correct over Q, under the stated full-column-rank and causal-circuit hypotheses.

With the surrounding circuit fixed, an incoming contribution through the existing chart-3 export coordinates has the form `M=N+C z ell`. Consequently its contribution to every pinned right-hand side belongs to `col(C)` and cannot change the truth of any pinned membership test. Full column rank then makes the shift of the unique pinned preimages exactly `-z alpha`, including the stated division by the nonzero source inverse coefficient `r_j`.

Substitution in the stock matrix gives `S_0(M)=S_N+(C_z z)(ell R_yb-alpha R_xb)`. On a free singleton stock coordinate, `R_yb` is zero and the only nonzero row of `R_xb` is a free source row, where `alpha` is zero. Thus all 532 free baseline stock columns remain zero, and the remaining 370 columns receive precisely the claimed rank-at-most-one update. The necessary baseline rank bounds 369 and 901 follow directly from the rank-one update inequality, including when the second matrix is augmented by any fixed basis of W.

The outside equality `E_ay-N_a=(C_a z)ell` gives the stated support, rank and column-space conditions. For a nonzero rank-one defect its row space fixes the incoming form up to scaling. These are necessary tests only; the eleven fixed-coordinate equations and the complete stock conditions remain required.

The reduction does not cover changes to surrounding forms, new feedback, or nonlinear maps. It excludes no endpoint pair by itself, and establishes no positive supplier or new kappa. Numerical residuals and numerical rank thresholds are not exact certificates.

Reviewed by S031 worker B, 2026-11-20.
