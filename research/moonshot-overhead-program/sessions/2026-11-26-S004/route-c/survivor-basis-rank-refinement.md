# A survivor basis for full-root spectral prediction

Status: **proved scoped algebraic refinement; independent review requested**.
This strengthens Route B's quotient-space rank bound when the whole local
root alphabet is present. It gives a sharp low-degree limiting error, not
a general tape-time lower bound or a new multiplication envelope.

## 1. Full alphabet and matrix model

Let r>=2, m>=1 and W>=1. Let K contain all r-th roots of unity and have
characteristic not dividing r. Put

    A=K[x_1,...,x_m]/(x_1^r-1,...,x_m^r-1),
    Omega=mu_r^m,    N=r^m,    chi=product_i x_i.

Every reduced monomial has exponents in {0,...,r-1}. Its support weight
counts nonzero coordinates. Let P be any W-by-W matrix over A of support
degree at most t. Coefficient matrices need not commute, be diagonal, or
be symmetric. Define the average normalized rank error

    E(P)=(NW)^-1 sum_(omega in Omega) rank(chi(omega)I-P(omega)).

For a reduced exponent alpha let n_j(alpha) count its coordinates equal
to j. Define its survivor condition by

    n_h(alpha)<=n_0(alpha)+h t    for every 1<=h<r.             (S1)

Let S_(r,m,t) be the set of all such exponents.

**Theorem S.** Every P in this model satisfies

    E(P)>=1-|S_(r,m,t)|/r^m.                                  (S2)

Equivalently, if (N_0,...,N_(r-1)) is the uniform multinomial count
vector of m independent r-valued draws, the lower bound is

    Pr[there exists h>=1 with N_h-N_0>h t].                    (S3)

## 2. Matrix quotient and terminating reductions

Let D=chi I-P and Q=A^W/im D. Since D is A-linear, its image is an
A-submodule. Scalar chi commutes with P, so PD=DP and P preserves im D.
It therefore induces an endomorphism of Q. On Q, chi=P, hence
chi^h=P^h for every nonnegative h. This uses no pairwise commutativity
of the coefficient matrices of P.

For any monomial vector x^alpha e_j and 1<=h<r, reduce alpha-h*1
coordinatewise modulo r, calling the result beta. In Q,

    x^alpha e_j=x^beta P^h e_j.                               (S4)

The representative on the right has support degree at most

    wt(beta)+ht=m-n_h(alpha)+ht.

If alpha violates S1 for this h, this degree is strictly less than
wt(alpha)=m-n_0(alpha). Thus x^alpha e_j is a linear combination of
strictly lower-weight monomial vectors. Induction on the integer weight
shows that survivor monomial vectors span Q. Reduction need not be
confluent or yield a unique normal form; strict descent is enough.
Consequently dim_K Q<=W|S_(r,m,t)|.

The roots are distinct, so evaluation gives A as the product of N copies
of K. Therefore dim_K Q=sum_omega nullity D(omega). Subtracting from NW
proves S2. The quotient argument itself is algebraic; semisimplicity is
needed to identify its dimension with the stated spectral average.

## 3. Relation to the earlier rank bounds

Summing S1 over h gives

    m-r n_0<=t r(r-1)/2.

Every survivor consequently has support weight at most
floor((r-1)m/r+(r-1)t/2). The survivor set is contained in Route B's
single averaged-cut spanning set. Thus S2 always strengthens that
particular support-degree quotient bound. For r=2 the two bounds agree.

For r=3 the exact survivor count is

    sum_(a+b+c=m, b<=a+t, c<=a+2t) m!/(a!b!c!),             (S5)

so S2 is a finite explicitly computable multinomial tail in the actual
characteristic-two order-three alphabet. E003's weighted two-point
binary tail remains a separate valid bound; take the maximum of the two.
Neither dominates the other at all parameter scales. In particular the
two-point theorem gives the stronger previously recorded rare-error
leading constant. The present refinement concerns the constant-error and
sub-square-root-degree regime.

At t=0 the exact optimum is E(P)>=1-1/r, attained by any constant
scalar matrix P=lambda I with lambda an r-th root. Indeed, distinct
eigenvalues of a constant matrix have independent eigenspaces, whose
dimensions sum to at most W, while chi is uniform on the r roots.
The raw survivor count includes ties among the largest n_j; the exact
constant-matrix argument removes that harmless finite tie loss.

## 4. Sharp limiting error below square-root degree

For every fixed r and every sequence t=o(sqrt(m)),

    inf_(W>=1, support-degree(P)<=t) E(P)=1-1/r+o(1).          (S6)

Here the infimum is over arbitrary matrix widths and nonsymmetric row
mixing. The upper bound is the constant scalar predictor above. A short
elementary anti-concentration argument supplies the lower bound.

For h!=0 the count difference N_h-N_0 is a sum of m independent steps
with probabilities 1/r at +1 and -1, and 1-2/r at zero. Condition on
J=N_h+N_0, distributed as Bin(m,2/r). The largest conditional atom is
at most 1/sqrt(J+1); this follows from the central-binomial ratio
induction, for both parities. On J>=m/r it is at most sqrt(r/m).
Chebyshev bounds Pr[J<m/r] by 2r/m. Hence the largest unconditional
atom is at most

    beta_(r,m)=min(1,3 sqrt(r/m)).                            (S7)

For m<r the trivial atom bound gives the same statement. If alpha is a
survivor and n_0 is not the unique maximum, some h>=1 satisfies
0<=n_h-n_0<=ht. The event that n_0 is the unique maximum has probability
at most 1/r by symmetry. A union bound over those short difference
intervals therefore yields

    |S|/r^m<=1/r+[(r(r-1)/2)t+(r-1)] beta_(r,m),

and thus

    E(P)>=1-1/r-[(r(r-1)/2)t+(r-1)] beta_(r,m).               (S8)

For fixed r and t=o(sqrt m), the error term tends to zero, proving S6.
This proof requires no central limit approximation or positivity in K;
the probability counts ordinary finite sets independently of the field.

## 5. Multiple ports and necessary scope

Route B's rank telescoping applies unchanged: if replacing all spectral
ports in an exact linear network by their constant references leaves a
support-degree-t P, then total normalized port width is at least S2.
For an inexact final target, add its average normalized rank error to
that port width. Every table occurrence is charged, and the complete
table-free path degree is used. A second predictor pass is not free.

These are full-root-alphabet statements. The actual order-three gate has
the three values 1,omega,omega^2, so its spectrum supplies this hypothesis.
E003's order-five two-by-two gate, with fixed points added, has only
1,zeta,zeta^-1. It does not expose all five roots. Applying the r=5
version to that physical gate would require a separate all-five contract
and is not justified by its name or order. Inverse targets or coprime
powers of chi on a full root alphabet follow by relabeling coordinates.

The theorem also needs strict weight descent. An equality in the degree
estimate may rewrite a monomial into itself. Nonlinear input-dependent
operations, gates mixing the common spectrum, and uncharged inverse
expressions with no polynomial-degree bound lie outside this model.

## 6. Exact finite controls

`verify_survivor_basis.py` and `survivor-basis-verification.json` check
31,697 strict-descent predicates and 98 survivor/count-cut identities.
For 66 arbitrary F4/F5 matrix predictors, the columns of chi I-P together
with the proposed survivor vectors span the entire regular module. These
include 41 cases with noncommuting coefficient matrices. All 66 regular
ranks agree with summed spectral ranks (1,335 pointwise rank calculations).
There are also 1,001 exact central-binomial atom bounds, 800 count-difference
atom bounds and 18 exact multinomial comparison profiles. Strict-descent
and full-alphabet omission controls fail as required. These checks support
the finite algebra; the written proof gives the unbounded theorem.

Credits: Route B's independently reviewed matrix quotient construction;
E003's complementary weighted two-point theorem; S004 Route C's survivor
reduction and full-alphabet low-degree limit; the OpenAI source interfaces;
Jerry Chen (@CubeJerry); substantial ChatGPT assistance. No literature
priority, formal-kernel verification, or general runtime lower bound is
claimed.
