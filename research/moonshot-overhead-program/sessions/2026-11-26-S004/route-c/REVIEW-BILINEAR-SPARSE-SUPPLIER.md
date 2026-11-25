# Independent review: fixed bilinear sparse-error suppliers

Reviewer: S004 Route C. Result: **accepted as a scoped algebraic supplier
restriction**, including the sharpened constant 16 and the lead's
finite-field counterpart. This does not establish a multiplication-time
or total bilinear-rank lower bound.

Reviewed `route-b-work/bilinear-sparse-supplier-gate.md` in full, followed
by its strict-event revision and finite-field paragraph. The exact
finite replay is in `replay-bilinear-supplier/`.

## Proof checks

S1 uses a genuinely nonzero product in the real polynomial ring. Its
individual variable degrees are at most s+1, strictly below the grid
cardinality. Induction on variables proves the stated grid fact, so the
exceptional output support is fixed for exact unrounded bilinear values.
The rational variant correctly charges the error numerator after clearing
the nonvanishing denominator. It does not give the same conclusion for
rounded values or adaptive nonlinear algorithms.

S2's conditional fourth-moment expansion includes the constant coefficient.
The inequality with factor three is valid; conditioning on the other sign
block and applying Cauchy--Schwarz gives the stated factor nine. This is
the separately affine structure, not a generic assertion for all
degree-two polynomials under arbitrary distributions.

The mixed-sign coefficients in S3 are U^2 M_jk/4, so Parseval yields the
uncentered second-moment lower bound U^4 ||M||_F^2/16. The original
Paley--Zygmund argument gave a valid 1/36 error probability. This review
supplied the adopted strict-event improvement: with Y=F^2, mu=EY>=1,
and Bad={Y>1/4}, Cauchy--Schwarz gives

    mu<=1/4+sqrt(EY^2 Pr(Bad)),   EY^2<=9 mu^2,
    Pr(Bad)>=(mu-1/4)^2/(9 mu^2)>=1/16.

The strict inequality in the event makes every nearest-integer tie rule
irrelevant. Linearity of expectation gives at most 16s inaccurate output
forms under the worst-case s-error premise; no independence of output
errors is used. The note correctly calls mu a second moment, not a
centered variance.

For the rank consequence, the active column subspace of H_i has dimension
r_i and H_i is an isometry on it. If rank G_i<r_i it meets ker G_i
nontrivially, proving ||H_i-G_i||_op>=1 and hence the Frobenius bound.
Because U>=2, all these outputs satisfy the S3 threshold. This constrains
each output form; shared convolution algorithms can still share products
among many full-rank forms.

The finite-field formula is exact: a^T M is zero with probability q^-r,
and otherwise its dot product with independent uniform b is uniform.
Thus each nonzero error form fails on fraction
(1-q^-r)(1-q^-1)>=(1-q^-1)^2. Summing probabilities gives the stated
constant-factor support conclusion over F_q, separately from rounding.

## Finite replay and limits

The isolated initial replay passed 200 separately affine fourth-moment
tests, 500 exact Walsh second-moment identities, 419 rounding probability
checks, 373 large-norm checks and 90 grid-product families, over 193,442
input evaluations. It rejected the insufficient factor-three and missing
individual-degree controls. Route C then changed both probability assertions
in its isolated copy from 36 to 16 and reran the same exact cases; all
passed. The replay directory contains this strengthened checker and receipt.

These checks support arithmetic identities and constants. The written
argument supplies the general theorem; the receipt does not test tape
complexity or provide the required fast sparse-error supplier.
