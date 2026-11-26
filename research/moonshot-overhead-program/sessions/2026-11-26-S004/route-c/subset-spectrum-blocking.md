# Blocking a subset spectrum into regular cyclic pieces

Status: **new proved algebraic extension with exact controls; independent
review pending**. This addresses the actual order-five subset rather than
assuming five local eigenvalues. It extends the joint lead/C plurality
method by a finite grouping of the original spectral coordinates.

## 1. Finite blocking hypothesis and network model

Let K contain a primitive r-th root zeta, r>=2 fixed, and let the payload
space be a tensor product of finite-dimensional simultaneously diagonal
local query representations. The local target is the product of their
nonzero eigenvalues. Repeated eigenvalues retain their actual dimensions.
Group a bounded number of original coordinates at a time. Suppose each
group's joint eigenbasis can be partitioned into:

1. regular pieces of dimension r, with target eigenvalues
   c, c zeta, ..., c zeta^(r-1), all once, for a nonzero scalar c that
   may depend on the piece;
2. one-dimensional pieces on which every local query is scalar.

Each piece is spanned by selected simultaneous eigenvectors, so every
original local query preserves it. Let theta_j be the fraction of the
j-th group's actual dimension lying in its regular pieces. Assume
theta_j>=theta_*>0, uniformly in the number of groups M. Both the group
size and theta_* are fixed constants. Unused original coordinates may
be left as singleton strata.

The network model is the one in `lead-work/plurality-active-volume.md`:
W independent payload rows; spectrum-independent constant row maps;
direct and everywhere-invertible one-coordinate affine-query matrices;
and optional arbitrary K-linear ports of bounded actual rank. If the
payload dimension is D, a port of rank at most hD contributes h to H.
Let Q_d,Q_i sum the active row widths of direct and inverse occurrences.
Define E=rank_K(T I-P)/(DW), where T is the actual product target.

The decomposition and comparison bases used below are for a rank proof.
No efficient physical change of basis or free nonlinear selection is
asserted. Original queries and their occurrences are still the charged
operations.

## 2. How the original queries act on a regular piece

On a regular piece, diagonalize the target as c times
diag(1,zeta,...,zeta^(r-1)). The r-by-r Fourier change of basis identifies
it with c times multiplication by y in K[y]/(y^r-1). Every original
one-coordinate function restricted to this piece is an arbitrary
function of these r distinct y-values, hence a polynomial in y of
degree at most r-1. Its support degree in this one grouped variable is
at most one. The same function is constant on a singleton piece.

Consequently an original affine-query matrix becomes a support-degree-one
matrix on each tensor stratum. A support-degree-d original polynomial
matrix has grouped support degree at most d: a monomial touching d old
coordinates touches at most d groups. Coefficient matrices may be
nonsymmetric and need not commute. Because the original matrix preserves
every selected joint eigenspace, its inverse, when it exists, preserves
all these pieces as well.

## 3. Sector construction on the actual payload

A stratum chooses one piece in each group. Let k be the number of its
regular pieces. For k>0 it is an actual copy of
K[y_1,...,y_k]/(y_i^r-1), with target c_stratum product_i y_i. Use the
equivariant plurality phase on its monomial basis. Multiplication by the
target moves each phase to its successor, bijectively; the nonzero scalar
c_stratum does not affect this property. A stratum with k=0 belongs to
an exceptional sector.

Take the direct sum over all strata. The r good sectors have equal
dimension, and T cyclically permutes them. Write

    pi_0 = product_j (1-theta_j).

Their total dimension is (1-pi_0)D. The remaining pi_0 D-dimensional
exceptional sector is T-invariant. Every map preserving these r+1
sectors therefore differs from T I_W by rank at least

    (1-1/r)(1-pi_0)DW.                                    (SB1)

The kernel equation on the good cycle determines every component from
one component. The exceptional block contributes a nonnegative rank.
This is an actual-dimension argument, not an unweighted average over
the distinct physical eigenvalues.

Let tau_d(k) be the fraction of r-ary k-tuples whose largest count minus
runner-up is at most 2d. Set tau_d(0)=0; for degree zero one may and will
use tau_0(k)=0 because constants preserve every sector. Under the
dimension-weighted distribution on strata, the number of regular pieces
has the distribution

    K_* = sum_(j=1)^M Bernoulli(theta_j),
    eta_d = E[tau_d(K_*)].                                (SB2)

The Bernoulli variables are independent: tensor dimensions multiply.
All singleton labels and all regular-piece copy labels are counted with
their actual multiplicities. Applying the column-boundary argument in
each stratum shows that a degree-d h-row query differs from its
sector-diagonal part by rank at most hD eta_d.

## 4. Matrix, inverse-query and rational conclusions

The block completion and telescope from the plurality note now give

    E + H/W + eta_1 (Q_d+2Q_i)/W
        >= (1-1/r)(1-pi_0).                               (SB3)

Ports may mix distinct strata or phases: zeroing them costs their
actual rank, after which the comparison network preserves sectors.
No restriction of the original port network to one stratum is assumed.
Arbitrary finite intermediate widths and actual shared port values are
allowed, with repeated operations charged separately.

For an arbitrary matrix predictor P of original support degree d,

    E(P) >= (1-1/r)(1-pi_0)-eta_d.                         (SB4)

For A,B of original support degrees a,b and invertible B, either
P=AB^-1 or P=B^-1 A satisfies

    E(P) >= (1-1/r)(1-pi_0)-eta_a-2eta_b.                  (SB5)

If instead A=PB or A=BP with a singular denominator, add its normalized
actual nullity eta_B to the left side. These statements require no
commutation between numerator and denominator. They follow by projecting
the numerator to sectors and completing the denominator sector blocks
to invertibility, precisely as in PA6–PA8.

Here are explicit asymptotics, without a random-walk assumption. Put
mu=sum theta_j>=theta_* M. Chebyshev gives
Pr[K_*<mu/2]<=4/mu. On the complement, the plurality atom bound gives

    tau_d(K_*) <= C_r(d+1)/sqrt(mu),
    eta_d <= min(1,4/mu+C_r(d+1)/sqrt(mu)),                 (SB6)

for d>=1; eta_0=0. Also pi_0<=exp(-mu). Thus when M=Theta(m),

    d=o(sqrt(m))             => E(P)>=1-1/r-o(1),
    Q_d+Q_i=o(W sqrt(m))     => E+H/W>=1-1/r-o(1),          (SB7)

and the fraction statement has the same limit if a+b=o(sqrt(m)).
If each original local spectrum lies in a fixed coset a_i mu_r, so the
global target coset is fixed independently of the stratum,
constant scalar prediction attains error 1-1/r+o(1): conditioned on
at least one regular piece, the product is exactly uniform on that
coset, and the all-singleton exceptional mass is at most pi_0.
Hence the limiting error constant is sharp in these cases.

## 5. The actual order-five subset

### Uniform distribution on {1,zeta,zeta^-1}

Group two original coordinates. Among their nine spectral points select

    (zeta^-1,zeta^-1), (zeta^-1,1), (1,1),
    (1,zeta), (zeta,zeta).

Their products are zeta^-2,zeta^-1,1,zeta,zeta^2, exactly the five roots.
They form one regular piece. Treat the other four points as singleton
pieces. Thus theta=5/9 and M=floor(m/2), with a final coordinate handled
as a direct sum of scalar strata. SB3–SB7 prove the sharp 4/5 limit for
this three-value subset. No five-value local spectrum was assumed.

### The two-value nontrivial spectrum {zeta,zeta^-1}

Group four coordinates. Choose one binary word of each weight j=0,...,4,
where weight counts zeta rather than zeta^-1. The products
zeta^(-4+2j) run through all five roots. These five points give one
regular piece and the remaining eleven points are singleton pieces.
Here theta=5/16, M=floor(m/4). The same 4/5 limit follows.

More generally, for a pair {a,b} with b/a of order r, group r-1
coordinates and select one word of every weight 0,...,r-1. This gives
theta=r/2^(r-1) and proves the sharp 1-1/r limit on that pair spectrum.
This is a derived subset extension; directly identifying that pair
space with the full r-point regular representation would be false.

## 6. Actual field-pair multiplicities, including fixed points

For a pair of fields with q>=2 possible values, the physical order-five
local gate has q equal-field fixed vectors, and q(q-1)/2 copies of each
of zeta,zeta^-1. Its total dimension is q^2. Choose eigenbases of the two
nontrivial eigenspaces and pair their equal-sized multiplicity labels.
The fraction at either nontrivial eigenvalue is

    p_q=(q-1)/(2q)>=1/4.

In a group of four field pairs, select the five binary words just
described for every tuple of multiplicity labels. Each selected product
root has exactly the same retained multiplicity. Their combined regular
fraction is

    theta_j=5 product_(i in group j) p_(q_i) >=5/256.      (SB8)

All unselected eigenvectors are singleton pieces. The q_i may vary with
the input and with the field pair. The lower bound is uniform, so SB3
and SB7 hold for the actual physical dimension, not merely for the
uniform measure on its distinct spectral values. The discarded final
one to three field pairs can be placed in scalar strata, without changing
the regular fraction of the complete groups.

The order-three nontrivial pair has the analogous grouping of two
coordinates, with theta=3/4 for a uniform pair. With physical fixed
points the same multiplicity argument gives theta_j>=3/16. It therefore
recovers the sharp 2/3 limit at that actual linear spectral interface.

The order-five conclusions also hold for each target power F_1,F_2,F_4
in the actual closed repair family. Raising the five selected products
to any of these powers permutes the fifth roots, and every original
query remains a function of one grouped root.

These applications require the declared common-spectrum query model.
Free address-dependent maps that mix the chosen joint eigenspaces,
nonlinear input-dependent suppliers, or unpriced converters are not
introduced by this proof. In particular it is not a lower bound for
all multitape algorithms, nor a complete multiplication construction.

## 7. Provenance and verification

This finite spectral grouping was derived in S004 Route C to answer
the lead's protected actual-order-five subset question. It composes
the lead/C equivariant-sector theorem, the independently checked block
completion, and B's network telescoping. E003's weighted two-point rank
theorem remains complementary for rare-error finite thresholds.

The earlier statement that the full-root r=5 theorem cannot be directly
imported for the three-value gate remains correct. SB1–SB8 provide the
additional invariant decomposition that was missing. No priority claim
or new complete time bound is made. The physical gate source is E003's
`route-c/ORDER-FIVE-ONE-TRANSFORM-CONVERTER.md`, Sections 1–2, published
at programme commit df91e4c8e31b1020e05056db5b0eb16169ef3421. Its
F16 eigenvalues, identity action at equal fields, and disjoint-pair
tensor structure were reread for the multiplicity assertion above.

`verify_subset_spectrum_blocking.py` and its JSON receipt pass exact F4
and F16 checks: 4,808 local-query invariant entries, 161 actual target
sector transitions, three actual subset inverse completions, six
explicitly noncommuting left/right fraction bounds, three rank-one ports
mixing regular and exceptional strata, 256 unequal physical-multiplicity
blocks, and 192 exact Poisson-binomial boundary profiles. The basis
changes are constructed and conjugated explicitly. F16 arithmetic uses
X^4+X+1 and checks all 4,096 distributivity triples.

Negative controls reject selecting five points with repeated target
products, and reject replacing actual unequal multiplicities by a
uniform measure on three distinct eigenvalues. The finite checks verify
the decomposition and rank identities; the unbounded asymptotic theorem
rests on the proof and elementary concentration bound above.
