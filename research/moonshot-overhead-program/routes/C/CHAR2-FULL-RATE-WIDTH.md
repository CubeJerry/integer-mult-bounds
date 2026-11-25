# An exact two-stage width barrier in characteristic two

Status: **proved scoped algebraic result, independent review pending**.
This concerns square full-rate matrix pencils over the nilpotent query
algebra. It does not bound arbitrary branching programs with initialized
workspace, longer programs, or physical correction algorithms.

Let K be a field of characteristic two and

    R_m=K[x_1,...,x_m]/(x_1^2,...,x_m^2),
    P_2=1+e_1(x)+e_2(x).

An affine pencil of width R is an R-by-R matrix with entries affine in
the x_i. A full-rate two-stage evaluation is an identity

    L_2(x)L_1(x)=P_2(x) I_R                              (W1)

in Mat_R(R_m). Every one of the R input coordinates is independent.
An identity on the faithful regular query module is equivalent to this
ring identity. Constant row operations may be included and absorbed.

## 1. Exact minimum width

**Theorem W1.** For every m>=1, the minimum possible width in (W1) is

    R_min=2^floor((m-1)/2).                              (W2)

The lower bound holds over every characteristic-two field. The upper
bound has coefficients in F_2 and is explicit.

### Lower bound

The constant matrices multiply to I, so they are invertible. Absorb them
to write

    L_1=I+sum_i x_i A_i,   L_2=I+sum_i x_i B_i.

The linear coefficients give B_i=I+A_i. The coefficient of x_i x_j,
i!=j, then gives

    A_i A_j+A_j A_i=I+A_i+A_j.                           (W3)

Fix the last index and set E_i=A_i+A_m for 1<=i<m. Adding the three
instances of (W3) for (i,j),(i,m),(j,m) gives

    E_i E_j+E_j E_i=I,   i!=j.                          (W4)

The associated alternating form on m-1 formal generators has zeros
on the diagonal and ones elsewhere. Its rank is
`2r=2 floor((m-1)/2)`. Take a symplectic basis for its nondegenerate
part. The corresponding matrix combinations U_1,V_1,...,U_r,V_r satisfy

    [U_i,V_j]=delta_ij I,
    [U_i,U_j]=[V_i,V_j]=0.

Brackets are ordinary commutators, which equal anticommutators in this
characteristic. Each U_i^2 and V_i^2 commutes with all these matrices:
`[U_i^2,V_j]=U_i[U_i,V_j]+[U_i,V_j]U_i=0`, and similarly for every pair.

Extend scalars to an algebraic closure. The commuting squares have a
nonzero simultaneous eigenspace W; it is preserved by every U_i,V_i.
On W their squares are scalar. Subtract scalar square roots from U_i,V_i
to arrange U_i^2=V_i^2=0 without changing the commutators.

One such pair U,V generates two complementary idempotents UV and VU:
`UV+VU=I`, `(UV)^2=UV`, `(VU)^2=VU`. U and V give inverse isomorphisms
between their images, so those images have equal dimension. Every other
pair commutes with the idempotents and restricts to each image. Induction
on r shows that the nonzero space W has dimension divisible by 2^r.
Therefore R>=dim W>=2^r, proving the lower bound.

This is the characteristic-two matrix-algebra version of a Clifford
representation argument. It does not use the characteristic-zero count
root bound or divide by two.

### Matching construction

Put r=floor((m-1)/2) and use R=2^r coordinates. On tensor factor i take

    U_i=[[0,1],[0,0]],   V_i=[[0,0],[1,0]],

tensored with identities elsewhere. Thus `[U_i,V_i]=I`, and different
pairs commute. For 1<=i<=r define

    E_(2i-1)=sum_(j<i)(U_j+V_j)+U_i,
    E_(2i)  =sum_(j<i)(U_j+V_j)+V_i.

All distinct E's obey (W4). If m is even, append
`E_(2r+1)=I+sum_(i=1)^(2r) E_i`. Its commutator with every earlier E
is I because 2r-1 is odd. For r=0 this simply appends E_1=I.

Let `A_0=sum_i(U_i V_i+U_i+V_i)`. Direct multiplication gives
`[E_i,A_0]=I+E_i`, including the appended E when present. Set
`A_m=A_0`, `A_i=A_0+E_i` for i<m, and `B_i=I+A_i`.
These matrices satisfy (W3), hence the two affine pencils have precisely
the constant, linear and quadratic coefficients of P_2 I_R. There are
no higher-degree terms, and x_i^2=0 removes diagonal quadratic terms.
This proves (W1) and the matching upper bound.

The two pencils commute: both orders have the same scalar constant,
linear and quadratic coefficients. Thus the block pencil
`[[0,L_2],[L_1,0]]` has square P_2 I_(2R). A repeated-pencil square root
exists within a factor two of the optimal two-factor width.

## 2. A weaker bound for an arbitrary number of stages

**Theorem W2.** Suppose t>=2 affine square pencils of common width R
multiply to P I_R in R_m, where P has constant term one and coefficient
one on every x_i x_j, i!=j. Then

    (t-1)R >= floor(m/2).                               (W5)

In particular this applies to every truncation P_(d-1) with d>=3.
It is only a polynomial width bound when t grows with m.

Normalize all constant matrices to I. If C_s is the s-th constant and
T_s=C_s...C_1, replace L_s by `T_s^(-1)L_s T_(s-1)`; these replacements
telescope and T_t=I. Write the new coefficients as A_(s,i). The
coefficient of x_i x_j in entry (1,1) is

    sum_(r>s) e_1^T (A_(r,i)A_(s,j)+A_(r,j)A_(s,i)) e_1.

Let U_r be the m-by-R matrix with i-th row e_1^T A_(r,i), and V_r
the R-by-m matrix with j-th column sum_(s<r) A_(s,j)e_1. The matrix
`M=sum_(r=2)^t U_r V_r` has rank at most (t-1)R. Its symmetrization
M+M^T has zero diagonal and every off-diagonal entry one. That matrix
has rank 2 floor(m/2), at most twice rank M, proving (W5).

For t=O(sqrt(m)) this only gives R=Omega(sqrt(m)). It does not exclude
polynomial-width evaluation in the degree range needed by the rank
approximation. The exponential theorem is specifically about two stages.

## 3. Consequence and limitations

The truncation's rank error can be small while its full-rate evaluation
is difficult. Already the degree-two member requires exponential width
at exactly two affine stages. A polynomial-width branching program is
compatible with this result: it computes a selected matrix entry with
initialized workspace, not P I on every coordinate.

There is nevertheless a generic characteristic-p full-rate root. For b
a power of p, use cyclic b-by-b weighted shifts S_i for the monomials of
P, one tensor factor per monomial. They commute because the factors are
different, and Frobenius gives `(sum_i S_i)^b=sum_i S_i^b=P I`.
No primitive b-th root or division by p is needed. Width remains
`b^(number of monomials)`, potentially enormous. This is existence, not
a compact evaluator or inexpensive correction.

The theorem is a scoped application of standard Clifford/commutator
representation ideas. No priority claim for those ideas or a global
algorithmic lower bound is made. The next target is a tradeoff for a
growing number of stages, or a full-rate evaluator compatible with the
actual address-space extraction and correction maps.

## 4. Verification

The accompanying checker constructs the matching F_2 matrices and checks
all constant, linear and quadratic coefficients. It exhausts the small
width-one and width-two coefficient compatibility graphs and includes
negative controls. These finite checks supplement the proof; they do not
prove the general lower bound by enumeration or test a tape implementation.

Actual run: `verify_char2_full_rate_width.py` passed and saved
`char2-full-rate-width-verification.json`. It constructed all m=1,...,16
examples (width through 128), checked 680 quadratic and 680 reverse-product
coefficient pairs and 560 commutator pairs, and exhausted both small-width
graphs. At width two the clique counts at m=1,...,5 were 16,20,8,2,0,
matching the maximum m=4 from the theorem. Omitting the linear correction
in A_0 failed in 14 cases; omitting the identity in the even-m generator
failed in eight cases.
