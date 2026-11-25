# Stable checks for finitely many known exceptional sets

Status: **proved algebraic construction with explicit finite search**, pending
independent review. This is a characteristic-zero repair improvement, not a
full tape theorem. No novelty is claimed for the standard concentration/net
method. Source interface: `lem:hermite-repair`, November Fourier manuscript,
OpenAI `math` `3344da59991ed94f9ba711217b29c1d760badfa6`.

The source proof only requires a fixed check matrix with left inverses on the
known exceptional columns and right inverses for their transposes. It does
not require a Vandermonde matrix or exactly s checks.

## 1. Stable check existence

Let F be a family of at most 2^m subsets of [M], each of size at most s.
Set `r=512(4s+2m+4)`.

**Theorem H9.** An r-by-M sign matrix H exists such that for every nonempty
J in F,

    (r/2) I < H_J^T H_J < (3r/2) I,                         (S1)
    ||H||_2 < 8 sqrt(M+r).                                 (S2)

The inequalities are strict positive-definite inequalities. Deterministic
exhaustive search with exact rational tests finds H in
`2^{O(rM+m)} poly(M,r,m)` time and polynomial space, apart from any supplied
enumeration cost/space for F.

### Existence proof

Choose independent uniform signs. For a fixed unit vector x in R^j and one
row, X=sum_i epsilon_i x_i has EX^2=1 and EX^4<=3. For 0<=t<=1/4,

    E exp( t(X^2-1)) <= exp(2t^2),
    E exp(-t(X^2-1)) <= exp(2t^2).                         (S3)

For the first bound, an independent standard Gaussian Z gives
E_Z exp(sqrt(2t)ZX)=exp(tX^2). The inequality cosh(u)<=exp(u^2/2) then
gives E exp(tX^2)<=(1-2t)^(-1/2). Finally
-t-(1/2)ln(1-2t)<=2t^2. For the second bound use
exp(-u)<=1-u+u^2/2 for u>=0, then
exp(t)E exp(-tX^2)<=exp(t)(1-t+3t^2/2)<=exp(3t^2/2).

Independence over rows and Chernoff with t=delta/4 give

    Pr[ | ||H_J x||^2/r-1 | >=delta ]
      <= 2 exp(-delta^2 r/8),  0<delta<=1.                 (S4)

A 1/4-net of the unit sphere in R^j has size at most 9^j: disjoint
radius-1/8 balls around a maximal separated set lie in the radius-9/8 ball.
For a symmetric A, ||A|| is at most twice max |x^T A x| on this net.
Using delta=1/8 in (S4), the probability that any J violates
||H_J^T H_J/r-I||<=1/4 is at most

    2^{m+1} 9^s exp(-r/512)
    = exp((m+1)ln2+s ln9-4s-2m-4) < 1/8.                (S5)

The stronger eigenvalue interval [3r/4,5r/4] implies (S1).

For (S2), take 1/4-nets in R^r and R^M. For fixed unit u,v,
u^T H v is subgaussian with variance proxy
sum_(a,b)u_a^2 v_b^2=1. At t=4sqrt(M+r), its union-bound failure
probability on both nets is at most
2 exp(-(8-ln9)(M+r))<1/8. Passing from the nets to the operator norm costs
at most (1-1/4)^(-2)=16/9, hence
||H|| <=(64/9)sqrt(M+r)<8sqrt(M+r). Both properties hold with positive
probability.

### Effective construction

Enumerate the 2^(rM) sign matrices. For every J test positive definiteness
of 2H_J^T H_J-rI and 3rI-2H_J^T H_J by exact Sylvester minors or rational
elimination. Test 64(M+r)I_r-HH^T similarly. Integer entries have
O(log(M+r)) bits; determinant bit lengths are polynomial in dimensions by
the determinant expansion. Strict inequalities avoid singular boundary
ambiguity. Existence ensures that a matrix passes. Enumeration and tests
reuse polynomial workspace, proving the stated finite-search bounds. ∎

## 2. Exact Hermite repair

For one exceptional set put V=H_J, G=V^T V, and

    L=G^(-1)V^T,  R=V G^(-1),
    D_z=diag(-(p_i+2z)/2),  A=R D_z L.                    (S6)

Then LV=I and V^T R=I. On checks (u,v)=(H PX,H X), return

    (A(u-zv), zA(u-zv)).                                  (S7)

The source proof applies with r checks: four predictor applications and 4r
full conversions repair all M independent inputs exactly. Extra positions
in J with p_i=z are harmless, and no inverse discrepancy is needed.

By (S1), ||L||=||R||<sqrt(2/r). If |p_i|<=2m^D as in the compact real
predictor, ||D_z||<=2m^D. Therefore

    ||A|| < 4m^D/r,
    ||the full 2r-row table|| < 8m^D/r.                   (S8)

Check and lift norms are at most 8sqrt(M+r). Partial sums of dense row maps
have only additional polynomial factors in M,r, since their coefficients
are bounded by (S8) (or by 1 for H). Grouping each dense map as a linear
stage, and accounting for its partial-sum rounding separately, bounds the
logarithm of the entire one-level gain by

    O(D log(m+1)+log(M+r)).                               (S9)

There are only a fixed number of dense maps in the repair; the four
predictor applications contribute O(D log m). Multiplying a maximum norm
once per individual scalar addition would give a much worse bound and is
not the argument for (S9).

## 3. Exact rational heights

For j=|J|, G is an integer matrix with
`1<=det G<(3r/2)^j`. Cramer's rule gives a common denominator det G for
its inverse. Because count-predictor values p_i are integers, A has common
denominator dividing `2(det G)^2`. Together with (S8), every numerator and
denominator has

    O(j log(r+1)+D log(m+1)+log(r+1)) bits.                (S10)

Constructing a table and approximating these rationals to a requested
precision use exact integer arithmetic in polynomial time in the dimensions
and these bit lengths. Coefficient preparation remains charged.

## 4. Compact rare-tail application

There are at most 2^m binary frequency patterns. The compact shift family has
M=2^{O(log^2 m)} and s=floor(M/(2m^3)). For m>=32 and
M>=32768(m+2),

    r/M <=1024/m^3+1024(m+2)/M <=1/16.                    (S11)

Thus the checks still use a vanishing fraction of independent inputs.
Their full-conversion charge per input row is
`4r/M=O(m^-3+m/M)`. If one conversion costs m query calls, this becomes
`O(m^-2+m^2/M)`. Its finite constants must be retained.

Compared with integer-node Vandermonde repair, log norm decreases from
O(s log M+D log m) to O(D log m+log M). Exact coefficient heights decrease
from O(s^2 log M+D log m) to O(s log r+D log m). These are one-interface
improvements. The explicit matrix search may take `2^{O(M^2+m)}` time, so
the construction is not being supplied for free.

Remaining obligations: compose the new check width with routing and the
fixed-tape caller; account for coefficient preparation, live streams and
generator workspace; apply the grouped-stage precision argument carefully.
No H(n) or kappa_ov is claimed.

Credits: OpenAI Hermite repair; standard Rademacher concentration, nets and
least-squares inverses; @CubeJerry; AI-assisted quantitative application.
