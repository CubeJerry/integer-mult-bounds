# Independent review of the routing-lift barrier

Reviewer: Route C, 2026-11-25. Status: **pass**.

Reviewed `results/interchange-lift-barrier/PROOF.md` and its verifier
against the pinned source `build/interchange.tex`. I also read the
concurrently preserved E001 `results/epsilon-uniformity/PADIC-LIFT-OBSTRUCTION.md`
to compare scope and preserve independent provenance. No priority claim
is part of this review.

## 1. Same-field and prime-power arguments

The integer identity `P_* entrywise (pJ-K)=pI` follows directly from the
source definitions: K is zero on the diagonal and equals p on every
allowed off-diagonal transfer. The matrix `(pJ-K)/p` is exactly the
first-generator principal block of the rational source Gram matrix.
Consequently its rational rank d is at most the source reserve quotient
dimension D. The independent bound `d<=1+h q^h` is also correct.

The entrywise product of factorizations of widths r,d has a factorization
of width rd by taking the tensor products of their row vectors. Over a
field, the resulting nonzero diagonal matrix has rank N. This proves the
same-field obstruction without symmetry assumptions on the transfers.

The crucial ring lemma is valid: over Z/p^e, e>=2, a factorization of pI_N
through r<N coordinates would allow invertible row reduction of the left
factor to create a zero row. Smith reduction over this principal ideal
ring supplies that row reduction even when every pivot is a nonunit.
But every row of an invertible matrix has a unit entry, so multiplying it
by the nonzero scalar p cannot produce a zero row. This is a contradiction.

The same proof works for any diagonal matrix whose diagonal entries are
all nonzero, including different p-adic valuations. It justifies the
spectral inner-rank count later in the proof. Reduction modulo p alone
would lose precisely this information.

An integer rank-d factorization of pJ-K exists by integer Smith normal
form: its unimodular factors have integer inverses. Thus it remains a
width-d factorization modulo every p^e, without assuming rational
denominators are invertible. Combining this with the entrywise product
and the pI lemma proves `r d>=N` for every support-preserving lift with
unit diagonal. The proof covers all e>=2 and all transfer entries allowed
by K=p, not only the literal zero/one source matrix.

The inference for `D(1+lambda)(1+mr/N)` is correctly scoped. That displayed
source cost certificate is at least m because `D>=d` and `rd>=N`.
This invalidates an unpaid use of that certificate after the field change;
it is not a lower bound on the minimum time of arbitrary implementations.

## 2. Rational full rank and spectral checks

For q a power of two, the labels form an elementary abelian two-group,
and the two-level relation is translation invariant. Its off-diagonal
degree is `binom(2p-1,p)^(p+1)(q-1)^(p^2)`. The binomial coefficient is
even for every odd p>1. The stated binary-digit argument identifies a bit
present in p and absent in 2p-1, proving the coefficient is zero modulo
two via the product factorization of `(1+x)^(2p-1)`.

Squaring a convolution in characteristic two on this group cancels
cross terms and sends every group element's square to the identity.
The kernel has odd total weight, so `P_*^2=I mod 2`. Hence its integer
determinant is odd and it is nonsingular over Q. No eigenvalue approximation
or positivity claim is involved.

The q-ary Krawtchouk eigenvalues and multiplicities in the verifier are
correct for the elementary binary-group character basis. The outer
operator has eigenvalue `1+e_p(kappa(t_1),...,kappa(t_h))`, since it chooses
the p far coordinates and fixes every other coordinate. The character
matrix is invertible modulo p^e: its dimension is a power of two, a unit
for odd p. The inner rank is therefore exactly the count, with
multiplicity, of eigenvalues nonzero modulo p^e. The integer Gram rank
formula used by the verifier separately counts the constant and one-active
outer-character eigenspaces and agrees with the source tensor structure.

## 3. Independent replay and scope comparison with E001

I replayed the unmodified verifier with its output directory redirected
under Route C. The result is in `lift-review-replay/verification.json`.
It passed 499 odd-binomial parity cases, 1,024 entries each of the
Hadamard identity, mod-two involution and exact character equations,
10,913 exhaustive width-one factorizations over three prime-power rings,
and five sets of 7,776 full spectral type tuples. The full outer matrices
were not materialized. All three advertised negative controls passed.

The concurrently preserved E001 proof has a sharper explicit lower bound
for the *literal* matrix modulo p squared:
`r>=h binom(h,p-1)(q-1)^(h^2-p)`. Its large-q consequence is stronger than
the generic `N/d` fraction for that literal matrix. The newly reviewed
proof has broader scope: arbitrary supported unit-diagonal lifts, every
e>=2, and no large-q condition. These are complementary results.
Neither should be described as a priority claim or as simply superseding
the other in every quantitative respect.

This review found no algebraic gap in Sections 1--6. The exclusions for
new off-support entries, nonlinear/graded corrections and changed routing
geometry are essential and should remain in any condensed statement.
