# Rational heights and norms for binary Hermite repair

Status: **proved one-level bounds**, pending independent review. These apply
over characteristic zero to `compact-complex-predictor.md`; they do not apply
to finite-characteristic interchange or price the full recursive caller.

Source: OpenAI `math` commit `3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier
manuscript `build/repair.tex`, `lem:hermite-repair`. We quantify its binary
case using integer nodes instead of all-characteristic cyclotomic nodes.

## Explicit inverses

Take M independent rows, nodes 1,...,M, and check matrix H_(a,i)=i^a,
0<=a<s. At a frequency let J be the known exceptional set, j=|J|<=s, with
nodes alpha_1,...,alpha_j. If j=0 the table is zero. Otherwise let V be the
first j rows of H_J. Put

    Delta_l = product_(v != l) (alpha_l-alpha_v),
    R_l(X) = product_(v != l) (X-alpha_v).

The coefficients of R_l/Delta_l form row l of V^(-1), by evaluation at the
nodes. Every Delta_l is a nonzero integer, and

    1 <= |Delta_l| <= M^(j-1),
    max_a |[X^a]R_l| <= (M+1)^(j-1).                         (H1)

The coefficient bound follows by expanding the product and summing absolute
coefficients. Each inverse entry has numerator and denominator bit lengths
O(j log(M+1)) and absolute value at most (M+1)^(j-1).

## Explicit binary table

For z in {+1,-1}, the source Hermite polynomial satisfies

    g(y) = 3y/2-y^3/2,
    g(y)-z = -(y-z)^2(y+2z)/2.

Thus D_z(y)=-(y+2z)/2. With exceptional predictor values p_l, form

    A = V^(-T) diag(-(p_l+2z)/2) V^(-1).                     (H2)

Embed A in the first j rows/columns of an s-square zero matrix. On spectral
checks (u,v)=(H PX,H X), the table returns

    (a,za) = (A(u-zv), zA(u-zv)).                            (H3)

The first inverse recovers exceptional error values from the first j checks;
the transpose inverse supplies a right inverse for H_J^T. This is precisely
the source identity with explicit inverse choices. It works if J contains
extra rows where p_i=z and never divides by p_i-z.

## Norm and coefficient bounds

The compact predictor has degree 1<=D<=m, D real roots in [0,m], and leading
coefficient of absolute value <=2. At every integer count c in [0,m],

    |p_i| <= 2 m^D.                                         (H4)

Each p_i is an integer, since the Newton formula uses integer generalized
binomial coefficients, also when c-u is negative. Hence the diagonal entries
of (H2) have denominator at most 2 and magnitude at most 2m^D. Consequently

    |A_ab| <= 2j m^D (M+1)^(2(j-1)),
    ||A||_2 <= 2j^2 m^D (M+1)^(2(j-1)),                     (H5)
    ||H||_2 <= sqrt(sM) M^(s-1).                            (H6)

The full table (H3) has norm 2||A||_2: its 2-by-2 block factor is
(1,z)^T(1,-z), of norm 2. Partial sums in a serial dense-map implementation
are also bounded by the number of terms times the maximum coefficient.
Thus log2 of these one-level norms is
O(s log(M+1)+D log(m+1)+log(M+1)).

A common positive denominator for all entries of A is

    Q = 2 product_l Delta_l^2 <= 2 M^(2j(j-1)).              (H7)

Combining (H5) and (H7), every numerator and denominator has

    O(j^2 log(M+1)+D log(m+1)+log(j+1)) bits.                (H8)

Elementary polynomial multiplication and integer arithmetic compute all
R_l, Delta_l, Q and A in polynomial time in M,m,D and the bound (H8).
This requires no numerical elimination or unproved conditioning estimate.

Listing the table at all 2^m binary frequency patterns costs at most
2^m poly(M,m,D) bits and bit operations. For the compact construction,
log2 M=O(log^2 m), D=O(sqrt(m log m)), this is 2^{O(m)}. It bounds only
these repair tables, excluding routing and other template instructions.
Computing tables on demand is an alternative, but its per-record arithmetic
and movement must be charged before claiming a tape improvement.

The logarithm of a repair norm and the coefficient bit length are each
2^{O(log^2 m)} for the compact batch. Lemma P2 can move those gains into a
threshold k>=2^{O(log^2 m)}, allowing fixed linear-in-k precision above that
threshold. This does not make conditioning uniformly bounded in m or prove
that every other growing-parameter condition is met.

Open next questions: compose with the routing list; compare precomputed and
on-demand tables; price live streams, coefficient preparation and interpreter
cost. Credits: OpenAI Hermite repair, standard Lagrange interpolation,
@CubeJerry, and AI-assisted quantitative extraction during this session.
