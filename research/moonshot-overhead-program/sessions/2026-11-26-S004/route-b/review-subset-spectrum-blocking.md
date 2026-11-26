# Independent review: subset spectra and actual multiplicities

Reviewer: S004 Route B. Reviewed the complete Route C
`subset-spectrum-blocking.md` and the lead/C
`lead-work/plurality-active-volume.md`, including the direct, inverse,
fraction, exceptional-sector and actual-multiplicity cases.

**Verdict: SB1--SB8 pass the mathematical audit.** The finite blocking
step supplies the missing bridge from the order-five three-value or
two-value local spectrum to a sharp 4/5 limiting error constant in the
declared common-spectrum linear-network model. It does not identify a
pair spectrum directly with a five-dimensional regular representation,
and does not assert an efficient physical change of basis.

## Invariant regular pieces

A selected set of simultaneous eigenvectors is invariant under every
original local query. On a selected r-point piece whose target values
are c times all r-th roots, the target's eigenvalues are distinct; every
restricted original local function is therefore a univariate polynomial
in the grouped root. Its grouped support degree is at most one, however
large its ordinary reduced degree may be. A degree-d original monomial
touches at most d groups. Row-matrix coefficients do not affect this
argument, and need not commute. An everywhere-invertible query restricts
to an invertible map on every invariant piece, so its inverse also
preserves the decomposition.

One can split unused eigenvectors into one-dimensional pieces even if
they share eigenvalues. Keeping their multiplicity labels is essential
for the later actual-rank normalization. Residual one to three original
coordinates are also a direct sum of scalar strata; their nonzero target
scalar does not change the good-sector cycle.

## Sector rank and mixture accounting

On a stratum with k>0 active pieces, the Fourier basis gives a regular
r-ary algebra, and the target is a nonzero scalar times its full shift.
The tie rule using the first exponent is exactly equivariant under this
shift. Thus all r sectors have equal dimension and are permuted
cyclically. For any sector-preserving comparison map, the kernel equation
determines the components successively backwards from one chosen
component, even when its diagonal blocks are singular. The resulting
rank loss is at least the fraction 1-1/r on the good subspace.

Taking the direct sum of all strata preserves that rank statement.
The all-singleton exceptional space is invariant and contributes a
nonnegative extra rank. Its dimension fraction is exactly
`pi_0=product(1-theta_j)`. The count of regular groups is a sum of
independent Bernoulli variables with parameters theta_j because actual
tensor dimensions multiply. Repeated regular pieces and singleton labels
are included in those fractions; no uniform distribution on distinct
eigenvalues is substituted for physical dimension.

Outside the top-count-gap boundary of width 2d, a degree-d grouped
monomial cannot change the unique plurality winner. Thus only the stated
boundary columns can cross sectors. Sum their actual dimensions over
strata to obtain hD eta_d, including the degree-zero value eta_0=0.
Chebyshev's `Pr[K<mu/2]<=4/mu` and the elementary atom bound on the
complement give SB6 with a constant depending only on fixed r.

## Inverse queries, arbitrary ports and fractions

The sector completion argument is valid over every field: the projected
diagonal block map has nullity at most the rank discarded, and filling
its rank-normal-form zero block costs exactly that nullity. Hence the
completed invertible comparison differs by at most twice the boundary
rank. Multiplying by its inverse preserves the rank of the inverse
difference. Rectangular constant row maps preserve the same sectors.

Arbitrary ports are removed globally by setting them to zero. Their
rank costs remain valid even when they mix different strata or the
exceptional sector. The proof never restricts such a port network to
one stratum. Telescoping with arbitrary prefix/suffix maps cannot
increase local rank, which proves SB3 under changing row counts and
shared previously computed port values.

For either numerator/denominator order, the difference of fractions is
a sum of a numerator error and a denominator-completion error, with
prefix/suffix multiplication. This proves SB5 without commuting either
matrix. The singular-denominator version pays its actual normalized
nullity once, as claimed.

## Concrete order-five pieces and physical multiplicities

The five specified ternary pairs have product exponents -2,-1,0,1,2
modulo five, all distinct. They yield one regular five-dimensional piece
out of nine. The five binary words of respective weights zero through
four have exponents -4+2j modulo five, also all distinct. They yield one
regular piece out of sixteen. Their complements are invariant singleton
pieces, so theta=5/9 and 5/16 respectively are exact.

For the physical gate, each of the two nontrivial eigenspaces has
dimension q(q-1)/2 and the fixed eigenspace has dimension q. In a
four-coordinate group, choose a tuple of nontrivial multiplicity labels
and then one word of each weight. This produces five different selected
vectors with one of each target product eigenvalue for every label
tuple, without overlaps between tuples. The regular fraction is
`5 product_i ((q_i-1)/(2q_i)) >= 5/256`, uniformly for all q_i>=2.
The analogous order-three two-coordinate construction gives 3/16.
Target powers 1,2,4 permute the five target roots, so preserve the same
construction. The sharp upper example requires the stated common
target coset; conditioned on any regular piece the target product is
uniform on that coset, while the exceptional mass vanishes exponentially.

## Scope

This is an actual-dimension rank theorem for the given linear query and
port model. It is not a tape-time lower bound. Free changes of the
physical payload basis, address-dependent mixing and nonlinear later
candidate maps need separate invoices or arguments. Within the declared
interface, it closes the previously explicit unequal-multiplicity gap
for applying ordinary image-dimension obstructions such as Route B's
proper-recurrence supplier gate.

## Isolated exact replay

Copied the author checker and its three helpers into
`route-b-work/subset-spectrum-replay/` and ran it there independently.
All checks passed with the author's counts unchanged: 4,096 F16
distributivity triples; 13 local target-cycle columns; 4,808 local-query
invariant entries; 161 global sector transitions; three actual-subset
inverse completions; six noncommuting left/right fraction bounds;
three ports mixing actual strata; 256 unequal physical-multiplicity
blocks; and 192 Poisson-binomial boundary profiles. The three checked
physical dimensions were 64, 81 and 16, with the expected regular
fractions 3/4, 5/9 and 5/16. Both stated negative controls passed.

The replayed main checker SHA-256 was
`8b95262bdb69817d96f048253b1e2b005624e3b0344109f7d6e4cb965980422a`.
This receipt covers the stable SB1--SB8 core. Later ratio-subgroup and
constant-sharpening additions are separate claims pending their own
review.

Prepared for @CubeJerry with substantial ChatGPT assistance.
