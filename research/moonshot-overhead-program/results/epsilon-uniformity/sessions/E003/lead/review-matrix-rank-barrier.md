# Lead review: matrix prediction and spectral ports

Disposition: **M1--M4 accepted as written theorems in their stated
algebraic/invoice model**. This is independent AI-assisted mathematical
review and an isolated exact replay, not Lean certification or human review.

Reviewed artifact: `../route-c/MATRIX-PREDICTION-RANK-BARRIER.md`.
Source pin: OpenAI `3344da59991ed94f9ba711217b29c1d760badfa6`.

## Mathematical checks

1. For arbitrary characteristic, the weights
   `alpha=a/(a-b)`, `beta=-b/(a-b)` satisfy both `alpha+beta=1` and
   `alpha/a+beta/b=0`. The centered product basis has diagonal nonzero
   Gram entries `product alpha_i beta_i`. There is no invalid division
   by 2 or use of positive field-valued probabilities.
2. The bound `t+2k<m` implies each monomial in every tested matrix entry
   misses a coordinate. The weighted moment of `f^(-1)` times that
   monomial vanishes. Hence the full block moment is `G tensor I_W`.
   Rank subadditivity yields the claimed integer sum of ranks in every
   field. Counting nonzero diagonal entries is never substituted for rank.
3. Restricting arbitrary one-coordinate query functions to two distinct
   eigenvalues makes each affine-query stage degree at most one. Fixed
   row mixing, extra finite rows and feed-forward linear combinations
   preserve the stated path-degree bound. Averaging uniform two-point
   slices produces the uniform measure on any finite local spectrum.
4. The ordered telescoping identity is correct even when port terms and
   surrounding factors depend on the spectrum. Each difference term
   factors through its charged port dimension. Every use is charged;
   the theorem does not assume disjoint error supports or a single table.
5. The binomial-tail exponent is `-c^2/2`, with natural logarithms and
   threshold displacement `(c/2)sqrt(m ln m)`. A band of
   `floor(sqrt(m/ln m))` levels supplies the required lower estimate;
   integer rounding and odd parity affect only bounded factors.
   The resulting invoice lower limit `sqrt(2 gamma-1)` follows by the
   stated two-case argument. It is not an unrestricted complexity bound.

## Source interface

The lead read the complete pinned Fourier `build/repair.tex`, including
`eq:repair-pencil`, `lem:hermite-repair`, `thm:repair`, and
`cor:swap-repair`. The paper uses a spectral table on `2s` rows with
`4s` forward/inverse row conversions, and its direct swap converter uses
up to `m` swaps per row. Thus `4ms` is a literal implementation invoice.
It is an upper-cost specification for that implementation, not a theorem
that every converter must pay `m` steps. M4 is valid only for the declared
invoice or for another model that independently proves such a price.

The source binary repair uses at most four predictor applications. The
degree `t` in M3 is the depth of the entire surviving program after all
port updates are zeroed, so it cannot silently be set to the first
predictor's degree. The note explicitly maintains this distinction.
Distinct `omega,omega^2` in `F4` avoid the coincident-sign failure of
characteristic-two parity. Recursive constant-tail correction changes the
price premise and is not excluded by M4.

## Isolated replay

The lead inspected the entire verifier and copied it to
`replays/matrix-rank/`, with its SHA-256 in `source-receipt.json`, then ran

```
python3 research/moonshot-overhead-program/results/epsilon-uniformity/sessions/E003/lead/replays/matrix-rank/verify_matrix_prediction_barrier.py
```

It passed 252 matrix-rank cases over fields of orders 3, 4, 5 and 7;
120 complete block Gram identities; 19,782 exhaustive scalar polynomial
cases; 24 ternary average-rank cases; and 80 product-telescoping identities.
The finite field arithmetic, Gaussian elimination and explicit moment
construction were inspected. Adverse controls distinguish diagonal
nonzero count from rank, coincident characteristic-two signs, and degree-m
exact prediction. Finite invoice values are diagnostics, not the proof
of the asymptotic tail estimate.

## Outcome

The old count/window obstruction now extends to nonsymmetric predictors,
nondiagonal full-rate output matrices, arbitrary shift choices and multiple
interacting low-rank spectral ports under the stated affine-query model.
This closes a real escape clause in that model. It leaves the costs of
implementing a pencil and recursive repair open and implies no lower bound
on arbitrary integer multiplication or actual universal-search runtime.

Credit and classical Razborov--Smolensky prior art remain in the theorem
document. This review does not certify literature priority.
