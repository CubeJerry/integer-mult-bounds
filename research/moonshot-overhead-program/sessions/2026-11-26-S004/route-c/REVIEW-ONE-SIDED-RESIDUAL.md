# Independent review: one-sided residual certificate

Reviewer: S004 Route C. Verdict: **accepted as a sound component under
coefficientwise nonnegative residuals**, without a sparsity premise for
acceptance. Fast completion still needs a small support or a successful
partial-isolation union. No fast one-sided sparse supplier is provided.

Reviewed `route-b-work/one-sided-residual-certificate.md` in full. The
predecessor sparse-residual proof and actual modular scan bill were
independently reviewed earlier in this session.

The new radix guard covers all D terms, including i^2 weights, rather
than the guessed support budget. Every true cyclic fold coefficient is
below R/8 even for dense residuals, and its packed value lies inside the
centered residue interval. Reduction modulo the product M and balanced
decoding therefore recover all three true folds. No CRT coprimality is
assumed.

The Euler square identity contains the required cross term
`2(Theta A)(Theta B)`. The exact identity

    u w-v^2=sum_(i<t) E_i E_t(i-t)^2

vanishes in a positive bin precisely when only one exponent is present,
under E_i>=0. Each certified record is a true residual term, regardless
of collisions in other bins. Deduplication by exponent is essential.
Thereafter equality with mass `A(1)B(1)-C(1)` forces the nonnegative
unrecovered residual to vanish. Nonnegativity of C alone is not the
structural assumption. Signed residuals remain outside this certificate.

The collision-free family now separates S exponents, since soundness no
longer compares two signed S-sparse candidates. Its stated K suffices.
At most K(K+1)/2 bins create records even for dense actual residuals,
so storage does not become proportional to D records. Weighted streams,
Theta-squared products, exact mass, division and variance comparisons
have O(beta)-bit operands and are all charged. The fixed number of long
modular scans retains `V log^alpha(k+1)+k^6`; the k>V schoolbook branch
fits this coarse bill and uses O(V) visited cells.

First-moment-only and signed-residual controls correctly expose necessary
assumptions. The component supplies no complete multiplication-envelope
improvement. The isolated `replay-one-sided-residual/` run passed 32,760
variance identities, 39,745 nonnegative-bin variance checks, 3,276
exhaustive residuals, 518 decoded fold families and 30 modular operand
product cases. Fifteen inputs deliberately used false sparsity guesses;
none produced a false acceptance. It exercised partial isolation with no
single separating modulus, dense-positive budget failure, the first-moment
false candidate, and a signed J-cubed witness across all four moduli.
These are arithmetic controls, not a physical timing simulation.
