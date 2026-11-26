# A sharp gate for nonnegative bilinear mixed-error suppliers

Status: **proved scoped obstruction; exact finite controls passed;
independent review pending**. This tests the most direct way to obtain the
coefficientwise lower candidate needed by the sound hybrid certificate:
evaluate only nonnegative bilinear pieces. The proof uses the classical
monotone convolution rectangle argument; the mixed-error count below
is an elementary corollary, with no priority claim.

## 1. Candidate model

Fix h>=1 and U>0. The input vectors a,b range over `{0,U}^h`. Write

    c_i(a,b)=sum_(j+k=i) a_j b_k,       0<=i<=2h-2.

Consider a fixed bilinear candidate represented by Q nonscalar products

    C_i(a,b)=sum_(ell=1)^Q gamma_(i,ell)
                   (sum_j alpha_(ell,j) a_j)
                   (sum_k beta_(ell,k) b_k),                (Mono1)

where all alpha,beta,gamma are nonnegative real constants. Arbitrary
sharing of these products among output rows is allowed. Zero or unused
products may be deleted. The candidate must satisfy `0<=C_i<=c_i` on
every allowed input, so it is a structural lower candidate.

Choose `0<M<=U^2` and `0<=S<=2h-1`. Suppose every input has at most S
outputs with residual `c_i-C_i>=M`. All other residuals may be nonzero
and dense. This is the one-sided mixed promise from the hybrid repair
note. The exact output is unrounded; a nonlinear or input-dependent
candidate is outside the present model.

**Theorem Mono.** The number of products obeys

    Q >= h^2-Sh+floor(S^2/4)
       = floor((2h-S)^2/4).                                (Mono2)

This bound is attained in the stated model. In particular S=o(h)
forces Q=(1-o(1))h^2, even though the corresponding repair stage can
be much cheaper. S>=2h-1 permits the zero candidate, so the lower bound
is then zero after capping S.

## 2. One-hot lower candidates force singleton rectangles

Expand C_i as `sum_(j,k) g_(i,j,k) a_j b_k`. Nonnegativity in (Mono1)
implies g>=0. On the one-hot input `a=U e_j,b=U e_k`, the lower-bound
condition gives

    0<=g_(i,j,k)<=1 if i=j+k,
    g_(i,j,k)=0 if i!=j+k.                                 (Mono3)

For a product ell used in row i, its nonzero support is the rectangle

    {j:alpha_(ell,j)>0} x {k:beta_(ell,k)>0}.

Every pair in that rectangle must satisfy j+k=i: otherwise its strictly
positive coefficient in C_i contradicts (Mono3), and nonnegative terms
cannot cancel it. A nonempty rectangle contained in one antidiagonal
has exactly one pair. Indeed fixing one k forces the only possible j,
and fixing that j forces the only possible k. Thus every used product
is a scalar multiple of one monomial a_j b_k and can be used only in
output j+k. At least one product is required for each pair with a
positive candidate coefficient.

This argument charges the actual shared products; it does not separately
sum unrelated output matrix ranks. Arbitrary nonnegative pre- and
post-linear maps in (Mono1) cannot evade the singleton property.

## 3. The all-U input and exact extremal count

At the all-U input, the residual in output i is

    U^2 sum_(j+k=i) (1-g_(i,j,k)),

with all summands nonnegative. If any coefficient on that antidiagonal
is absent, the residual is at least U^2>=M. Therefore every output
whose residual is below M must contain all its monomials with positive
coefficient, each requiring a product by Section 2.

There are at most S exceptional outputs at this single allowed input.
The antidiagonal lengths, in decreasing order, are

    h, h-1,h-1, h-2,h-2, ..., 1,1.

For S=2t the largest S sum to `2th-t^2`; for S=2t+1 they sum to
`(2t+1)h-t(t+1)`. Both expressions equal `Sh-floor(S^2/4)`.
Deleting at most S antidiagonals therefore removes at most that many
of the h^2 monomials. This proves (Mono2).

For equality, set C_i=0 on the S longest antidiagonals and compute all
other outputs by their ordinary individual products. The residual is
nonnegative and supported on those S outputs for every input, so it
satisfies the mixed promise for any M>0. Its Q is exactly (Mono2).
Thus allowing dense small errors yields no reduction in the minimal
product count beyond the optimal omitted-output construction in this
nonnegative model when M<=U^2.

## 4. Interpretation and limits

For b-bit digit inputs one may take U=2^b-1. A small-modulus budget
M=2^a with a much smaller than b satisfies M<=U^2. A candidate built
by the fixed nonnegative bilinear mechanism then needs almost h^2
products when S=o(h). Any implementation that executes those arithmetic
products separately incurs at least that many steps. Packed operations,
signed cancellations, nonlinear rounding, comparisons and input-adaptive
branching are not treated as free implementations of (Mono1), and are
not excluded by this gate. This is not a lower bound for arbitrary
integer multiplication or for arbitrary structural lower candidates.

The threshold hypothesis is real: when h=1 and M>U^2, the zero
candidate has no outlier and uses no product, violating the S=0 formula
if that hypothesis were omitted. Likewise signed intermediate products
can cancel rectangle entries, and the usual two-digit three-product
identity evades the nonnegative factorization premise. Output rounding
would also require a separate argument.

## 5. Primary-source scope and attribution

The singleton-support argument belongs to established monotone arithmetic
complexity. The primary paper S. B. Gashkov and I. S. Sergeev,
*A method for deriving lower bounds for the complexity of monotone
arithmetic circuits computing real polynomials*, Sbornik: Mathematics
203:10 (2012), 1411--1447, DOI
<https://doi.org/10.1070/SM2012v203n10ABEH004270>, was read at Section 2,
Lemma 16 and its proof on p. 1443, and the following convolution
application on p. 1444. Its accessible author/researcher-hosted primary
PDF is <https://web.vu.lt/mif/s.jukna/boolean/Gashkov-Sergeev-Sbornik.pdf>.
It explicitly gives the exact h^2 monotone nonscalar-product count for
convolution and credits earlier work by C. P. Schnorr. Schnorr's 1976
full paper was not accessed. The present note proves its own restricted
bilinear form and mixed-error extension and makes no new claim for the
classical h^2 fact.

## 6. Exact finite controls

The self-contained checker exhausts all 66,066 zero/one subcandidates
for h<=4 and confirms the sharp optimum at every budget. It also checks
21,343 nonempty support rectangles, 4,160 exact extremal antidiagonal
sums, 162 fractional-coefficient candidate bounds through 2,592 corner
evaluations, and 256 two-digit signed-cancellation controls. The
large-threshold zero-candidate counterexample is explicit. The JSON
records the exact counts; no general tape-time simulation is claimed.

Prepared for @CubeJerry with substantial ChatGPT assistance.
