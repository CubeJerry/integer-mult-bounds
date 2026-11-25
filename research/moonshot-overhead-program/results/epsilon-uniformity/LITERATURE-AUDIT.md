# External primary-source audit and quantitative relevance

This is a record of the sources actually consulted during E001, not a
comprehensive priority search. The pinned November and September manuscripts
remain the main sources; their exact locations are in PARAMETER-LEDGER.md.
No stronger multiplication theorem is imported from a search excerpt.

## Cyclic matrix factorizations

R. Sheng and T. Tribone, *Tensor products of d-fold matrix factorizations*,
Nagoya Mathematical Journal261 (2026), e2; published online2025,
DOI10.1017/nmj.2025.12:
[primary PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/526C84981550C9E71BECB481DC4F9B18/S0027763025000121a.pdf/tensor_products_of_dfold_matrix_factorizations.pdf).

The root directly read Definition2.1, the graded tensor construction in
Definition3.1, Proposition3.2 and its integral-root argument, and the
equal-rank tensor-size statement. These supply the appropriate prior art
for adding cyclic factorizations. The session's construction also writes
out the Gaussian-binomial identity, product concatenation, constant handling
and finite scalar descent. A complex-field identity alone would not justify
odd-characteristic use; the integral identity and explicit basis are essential.
No decomposability or Ulrich-minimality theorem from the later sections is
used in the tape bound.

M. Bläser, D. Eisenbud and F.-O. Schreyer, *Ulrich complexity* (2017):
[DOI](https://doi.org/10.1016/j.difgeo.2017.06.001).
The primary search rendering supplied Theorem2.1 and related sum-of-products
discussion. Direct DOI retrieval failed. The session relies on the pinned
Fourier manuscript's complete integral proof of its matrix-root lemma,
which cites this work, and on the independently reconstructed cyclic
construction. The general literature citation does not establish a compact
bit-efficient generator for the source predictor.

## Formula size versus permitted query depth

P. Hrubeš and A. Yehudayoff, *Homogeneous formulas and symmetric polynomials*:
[author-hosted primary PDF](https://www.ias.edu/sites/default/files/math/csdm/08-09/phrubes_homogeneous_formulas_and_symmetric_polynomials.pdf),
[arXiv record](https://arxiv.org/abs/0907.2621).

The root read the precise Theorem1 statements and the interpolation
construction in Section3.1. The homogeneous multilinear lower bound has
restricted hypotheses and is not a lower bound for our matrix representation
or a tape algorithm. The interpolation formula illustrates a relevant
pitfall: cancellation may lower the output polynomial's degree even though
the displayed products still contain all variables. Such a formula does
not automatically give a pencil program with only the desired window-width
number of stages. The session uses its own explicit division-free,
degree-preserving balanced convolution formula; it needs no unverified
formula-complexity theorem.

P. Hrubeš and A. Yehudayoff, *Arithmetic Complexity in Ring Extensions*,
Theory of Computing7(8),119–129 (2011), DOI10.4086/toc.2011.v007a008:
[primary PDF](https://theoryofcomputing.org/articles/v007a008/v007a008.pdf).

The root read the ring-dimension definition and the quotient-ring existence
argument of Theorem3.2, as well as the stated small-formula consequence for
elementary symmetric polynomials. No explicit finite free dyadic algebra
with a verified multiplication table, controlled coefficient heights and
the required actual construction time was extracted from this argument.
Consequently it is not treated as proving MR or as permitting uncharged
noncommutative scalar operations. Extracting such data would require its
own proof. The balanced cyclic construction instead exposes every matrix
and scalar-basis operation directly.

## Selection, recurrences and prime search

M. Hutter, *The Fastest and Shortest Algorithm for All Well-Defined Problems*
(2002): [primary PDF](https://www.hutter1.net/ai/pfastprg.pdf).
The stated program-search/time-bound theorem was read as prior art for
separating discovery of a certified plan from its eventual execution.
Route B supplies a specific tape/region contract and charged bounded
preflight proof. It does not claim that the source multiplier automatically
satisfies Hutter-style efficient bound certification or the stronger
polylog-log family hypotheses.

D. Harvey, J. van der Hoeven and G. Lecerf, *Even faster integer
multiplication* (2015): [author-hosted primary PDF](https://www.texmacs.org/joris/mul/mul.pdf).
Section5 and Proposition5.3 were consulted for recurrence-solving prior
art. Route C's nonstationary recurrence and integer-boundary treatment are
written out with their own explicit local hypotheses; the literature is
not used to waive those hypotheses or the physical tape bill.

R. Baker, G. Harman and J. Pintz, *The difference between consecutive primes,
II* (2001): [primary article PDF](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/BakerHarmanPintz.pdf).
The root directly checked Theorem1 and the introductory effectivity
statement. Only its eventual prime-interval guarantee is used, with a
conservative exponent and a separately retained absolute cutoff. The
analytic proof was not independently reconstructed, and no numerical cutoff
is claimed. Route C proves its interval packing, compatibility scans and
integer volume estimates separately.

## Concurrent programme evidence

The root read S002's sharper profile, compact integral IP bridge and formal
Chow barrier at `4689161c5bc6c9e64536034d4fa6af033d26a3e0`, after previously
reading its complete coarse extraction and rational-address/minor proof at
`96028cba1342c02bdca1f537ae9a80485087bdf3`. The same-scale independent
results and the complementary representation scopes are credited. S002's
new characteristic-two physical components are preserved; E001 does not
claim a fresh complete independent audit of those proofs.

Canonical source heads were unchanged at the 15:16:37 UTC check on
25 November2026. Search coverage is incomplete, and no literature-priority
or claim to improve an unspecified published residual term is made.

Prepared with GPT-6 Astra Pro assistance for @CubeJerry. Primary proofs,
source applications, conditional hypotheses and finite checks retain
separate status labels.

## Concurrent formula result and final representation scope

At remote58c754b583815e4fe40d333ec9d71e4c254749ba, S002 independently
completed the same stronger formula-based envelope. Root read its B cyclic
linearization, C cyclotomic generator, A extraction and lead review in full.
S002 permits varying affine factors and selects its common repair algebra
before regular descent; E001 additionally forms one repeated dyadic root
by a final cyclic block. Both preserve every occupied coordinate and obtain
the same quantitative rate. The two constructions and review provenance
are retained without a priority claim or double-counted verification.

The further primary-source audit is route-a/mr-symmetry-literature.md, with
C's separate SYMMETRY-REDUCTION-REVIEW.md. Its tensor decomposition requires
cyclic shift symmetry not preserved by the formula's product concatenation.
Generic conversion to repeated pencils repays the apparent row saving.
Neither that audit nor the ring-extension existence theorem supplies MR's
actual finite free dyadic algebra and bit generator.

Hrubes--Yehudayoff's homogeneous multilinear formula lower bound is used
explicitly in route-c/FORMULA-RECIPE-LOWER-BOUND.md, independently reviewed
by A and root. This is a lower bound on a specified unreduced representation
recipe, not on all matrix roots or integer multiplication.
