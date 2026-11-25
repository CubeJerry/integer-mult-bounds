# Independent Route B review of the survivor quotient refinement

Reviewed `route-c-work/survivor-basis-rank-refinement.md` in full on
2026-11-25. **Pass**, including arbitrary matrix width, the strict descent,
the exact full-alphabet scope, and the sharp sub-square-root limit.

The image of `chi I-P` is an A-submodule because the matrix is A-linear.
P preserves it because `P(chi I-P)=(chi I-P)P`. Thus every power used in
the quotient is legitimate even when P's coefficient matrices do not
commute. Multiplying the quotient identity by a monomial is likewise
legitimate. For a violation `n_h>n_0+h t`, the resulting degree bound is
strictly below the original monomial weight. Recursion terminates on
integer weight; uniqueness or confluence of the reduction is unnecessary.

The survivor vectors therefore span the quotient, and semisimple
evaluation identifies quotient dimension with the sum of pointwise
nullities. Summing all survivor inequalities recovers the earlier
averaged-cut support bound. For r=2 the sets coincide exactly. For larger
r this refinement retains simultaneous count constraints that the
average had discarded.

The asymptotic proof is uniform in W. Conditional on
`J=N_0+N_h`, the difference has a binomial point mass bounded by
`1/sqrt(J+1)`, including both parity cases and J=0. On `J>=m/r` this
is at most `sqrt(r/m)`; Chebyshev contributes at most `2r/m` on the
complement. When `m>=r`, their sum is at most `3sqrt(r/m)`, while
the trivial bound one handles the remaining range. Thus (S7) holds.

A survivor for which n0 is not the unique maximum has some count
difference in `[0,h t]`. The union bound includes the tie value zero
and gives exactly `t r(r-1)/2+(r-1)` possible atom charges. The
unique-maximum event for n0 has probability at most 1/r by symmetry.
This proves (S8), and its error tends to zero for each fixed r and
`t=o(sqrt m)`. The constant scalar predictor has error exactly `1-1/r`,
so the limiting infimum is sharp, uniformly over every matrix width.

The separate finite t=0 argument is also sound: distinct eigenspaces of
a constant matrix are linearly independent, their dimensions sum to at
most W, and chi is uniform on the r roots. It removes the tie loss of
the raw survivor count without pretending that ties yield strict descent.

The full-root hypothesis is material. The order-five physical alphabet
`{1,zeta,zeta^-1}` is not the whole fifth-root set; r=5 cannot be
substituted there. For a physical payload whose joint spectral
multiplicities are unequal, the abstract uniform spectral average also
must not be silently identified with normalized rank of the entire
physical operator. The port-width application remains valid through its
pointwise all-spectra guarantee, and a regular representation has exactly
the stated normalized rank identification.

No lower bound on unrestricted nonlinear suppliers, arbitrary basis
changes, inverse expressions with no degree bound, or multiplication
running time is implied. This is a genuine strengthening of the prior
quotient estimate in its stated full-alphabet setting and is correctly
credited to Route C.

Prepared for @CubeJerry with substantial ChatGPT assistance.

The checker and its two helper modules were copied into
`route-b-work/survivor-replay/` and run there. The isolated replay passed
all recorded counts: 31,697 strict-descent predicates, 98 count identities,
66 quotient spanning/rank-sum comparisons (41 with noncommuting matrix
coefficients), 1,335 spectral ranks, 1,001 central-atom bounds, 800
count-difference bounds, and 18 multinomial profiles. Both omission
controls failed as intended. Initial runs lacked the helper modules;
the successful replay included the exact local helper files and records
their hashes. This is finite algebra evidence, not a tape simulation.
