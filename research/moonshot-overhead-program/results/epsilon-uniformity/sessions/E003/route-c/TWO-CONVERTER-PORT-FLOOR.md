# A finite rank-derived floor after the order-five converter shortening

Status: **proved within the stated full-batch recursive invoice;
independent review pending**. The zero-query repair was suggested by the
E003 lead; the exact parity-dependent scalar potential below sharpens it.
This is not a lower bound on physical tape movement or multiplication.

The order-five word changes the number of complete target applications
per spectral port from four to two. Thus the earlier q=4 theorem cannot
simply be reused. A degree-zero boundary correction gives a valid q=2
floor, including all finite arities. Integer degree effects matter here:
the q>2 normal-tail potential cannot be extended to q=2 by substitution.

## 1. Model and zero-query correction

Use the full-batch stage and full-rate finite-tree model of
`RECURSIVE-PORT-COST-FLOOR.md`, with q=2. Each port of width h incurs
two sequential complete h-row child target transforms. A node's
nonrecursive invoice is at least Wt, where t is the degree after every
spectral port is zeroed. Children are correct on arbitrary independent
inputs; leaves compute their targets directly with at least m stages.

One harmless extension is needed for O5: a child may use any target in
a fixed family of products of m local nonzero distinct eigenvalues.
The degree/rank theorem is uniform in these values. The O5 family
F1,F2,F4 satisfies this condition on every nontrivial two-point cube.
The proof below therefore applies to all members with the same potential.

**Lemma Z.** If P is a constant W-by-W matrix and
`f(x)=product_i f_i(x_i)` with each f_i taking two different nonzero
values, then

    sum_(x in {0,1}^m) rank(f(x)I-P) >= 2^(m-1) W.       (Z1)

Pair each tuple with the tuple differing in its first coordinate.
The two target scalars differ. The difference of the two defect matrices
is a nonzero scalar times I, of rank W. Rank subadditivity therefore
makes the sum of their ranks at least W. Summing over disjoint pairs
proves Z1. This is a matrix-rank argument and does not count merely
nonzero diagonal entries.

The spectral-port telescoping identity M3 then gives
`sum h_r>=W/2` at every degree-zero node. At positive degree retain
the earlier bound

    delta_m(t)=2^-m sum_(j<=floor((m-t-1)/2)) binom(m,j),

with delta=0 for t>=m. Define

    delta_hat_m(0)=1/2,
    delta_hat_m(t)=delta_m(t) for t>=1.                  (Z2)

The ordinary binomial bound at t=0 is strictly smaller than 1/2 for
even m. Replacing it by Z1 is essential; otherwise a fictitious zero-cost
contracting repair defeats every positive potential in the relaxed model.

## 2. Exact best scalar potential from these bounds

Let `p_j=2^-m binom(m,j)` and `M_m=p_floor(m/2)`. Put

    L_m = 1/(2 M_m),                              m odd;
    L_m = 2/(M_m+2 p_(v-1)),  v=m/2,              m even. (Z3)

Equivalently, for even m=2v,

    L_m = 2(v+1)/[(3v+1) M_m].

**Theorem Z.** For every integer m>=1, every W and every finite admitted
q=2 repair tree,

    total row-stage invoice >= W L_m
                             >= (sqrt(6)/4) W sqrt(m).   (Z4)

Furthermore L_m is exactly

    min_(1<=t<=m) t/[1-2 delta_m(t)].                    (Z5)

It is the best scalar subsolution using Z2 alone. This does not assert
that an actual predictor attains the rank bounds or that an actual
algorithm attains this relaxed potential.

### Odd m=2v+1

Symmetry gives `sum_(j<=v)p_j=1/2`. For t=2r-1,

    1-2delta_m(t)=2 sum_(h=0)^(r-1) p_(v-h)
                  <=(t+1) M_m.

The ratio in Z5 is at least `t/[(t+1)M_m]>=1/(2M_m)`.
Equality holds at t=1. For even t=2r the same central sum occurs,
and its bound is t M_m; the ratio is at least 1/M_m. This proves
Z5 for odd m, including m=1.

### Even m=2v

For odd t=2r-1,

    1-2delta_m(t)=M_m+2 sum_(h=1)^(r-1) p_(v-h)
                  <=t M_m.

Its ratio is at least 1/M_m. For even t=2r,

    1-2delta_m(t)=M_m+2 sum_(h=1)^r p_(v-h)
                  <=M_m+2r p_(v-1).

The function `2r/(M_m+2r p_(v-1))` increases with r, so the minimum
is achieved at r=1, giving Z3. This is no larger than 1/M_m because
`p_(v-1)/M_m=v/(v+1)>=1/2`. The t=m case includes delta=0 and is
consistent with the same formulas.

### Subsolution and finite-tree induction

At t=0, `2delta_hat=1`, so
`t+2L_m delta_hat=L_m`. For `1<=t<=m`, Z5 gives the same inequality;
for t>=m, use t>=m>=L_m. Thus at every node

    Wt +2L_m sum h_r >=W[t+2L_m delta_hat_m(t)]>=W L_m.

Induct over the finite tree. Direct leaves cost mW and satisfy the same
bound. Node-dependent depths, port sizes and target choices in the
admitted family cause no change.

The elementary central-binomial estimate R2 gives
`M_m<=sqrt(2/(3m))`. For odd m, Z3 is therefore at least
`sqrt(3m/8)=(sqrt(6)/4)sqrt(m)`. For even m, it is at least
`2/(3M_m)>=sqrt(2m/3)`, a stronger bound. This proves Z4 without an
asymptotic cutoff or a numerical approximation.

## 3. Why the q=2 endpoint is discrete

Central-binomial asymptotics give

    L_m/sqrt(m) -> sqrt(pi/8),                    m odd;
    L_m/sqrt(m) -> (2/3)sqrt(pi/2),               m even. (Z6)

The minimum is at the bounded integer degree t=1 or t=2, respectively.
Consequently a normal-tail approximation at t=c sqrt(m), with fixed
positive c, misses the active endpoint. It would suggest the larger
limiting value sqrt(pi/2) as c decreases to zero. Uniform convergence
of tails alone does not justify that inference because the denominator
`1-2delta` also vanishes there. This explains why the earlier R2 proof
correctly requires q>2 and a strictly positive compact margin.

For comparison, the relaxed scalar finite-depth recurrence

    B_0=m,
    B_(h+1)=min_(0<=t<=m) [t+2delta_hat_m(t) B_h]

decreases to L_m: it never goes below the subsolution, and repeatedly
using t=1 or t=2 gives the matching limit. This is only a statement
about the relaxed numerical recurrence. No existence of a real matrix
predictor attaining its rank entry is claimed.

## 4. Meaning for the order-five construction

The O5 forward and inverse converters each cost one complete target.
Its check table has full converted width 2s, so it fits q=2 with a
port of width 2s. That width is distinct from the table's algebraic
rank, which can be smaller. A rank-sensitive implementation would need
its own converter contract; this theorem does not identify port width,
number of exceptional original rows and table rank with each other.

Z4 shows that merely shortening the word to q=2 does not make the
stage invoice smaller than order sqrt(m). Its constant is below one,
so it is not the previous q=4 assertion of a fixed factor above the
normalized root scale. Neither result lower-bounds actual shared-pencil
tape work without an additional stage-pricing lower premise.

Open next questions: exploit low rank of a concrete check map in its
converter implementation; share spectral conversions across ports; or
use a predictor cost below the full-batch Wt invoice. These mechanisms
are outside the theorem and are not excluded.

Credits: the lead's zero-query rank pairing and initial positive q=2
potential; the M1--M3 degree/rank proof and its cited predecessors;
the O5 gate and finite repair; @CubeJerry; AI-assisted derivation of
the exact parity-dependent potential and finite verification.
