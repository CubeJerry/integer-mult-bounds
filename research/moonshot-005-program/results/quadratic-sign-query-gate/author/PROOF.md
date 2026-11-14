# Quadratic spectral cuts and an all-exponent two-head chain obstruction

**Proved in the stated commuting coefficient model. No new kappa.**
The universal argument has an independent text review by Worker B. Exact finite
controls were executed in the separate orchestration V8 runtime after the local
workspace became unavailable. No local Python or Node execution after that
outage is asserted.

## 1. Native, caller and quantifiers

Fix p,r>=1 and a finite ambient binary dimension d>=2. Each field is indexed by
(F2^d)^V. For a single column define
C_w=((1+i)I+(1-i)X_w)/2 and Q_w=C_w^(tensor V), where X_w is translation by w.
All Q_w commute. On a Walsh character (z_1,...,z_V), the eigenvalue of Q_w is
i^(sum_c ell_w(z_c)), with ell_w(z)=w dot z in{0,1}.

The canonical native uses two head axes e0,e1 and seven body axes. Put
a=Q_e0, b=Q_e1 and F=product of the seven body-axis Qs. Its four independent
input fields have exact output equations

    X'=FbX,
    Y'=FaY+FX,
    U'=FbU-FabV,
    V'=FaV.

There is a literal eight-event source: X,U start on line e0; Y,V start at
ground. Move V to line e0, ADD U-=V, move V to facet e1-perp; move Y to line
e0, ADD Y+=X, move Y to facet e1-perp; move X and U to Hub. All contacts are
real nested coordinate charts. The six MOVE ranks are1,7,1,7,8,8, with no
owners. At body eigenvalue1 the field matrix is

    H(a,b)=[[b,0,0,0],[1,a,0,0],[0,0,b,-ab],[0,0,0,a]].

The full120 Eisenstein native has a separately developed moving-gauge
equivalence to this control. That unpublished linkage is not required for
the present canonical-control theorem and is not silently promoted here.

A caller in this theorem satisfies all the following:

1. It uses exactly2r calls of p copies of this native or its inverse, charging
   the complete price2p(1+7^t+8^t) per call.
2. Its productive body profile has2p independent targets of body rank14r and
   4p targets of each rank7j,1<=j<=r. It pays at least4p whole idles of each
   rank7j for1<=j<r. Every target may independently include neither, either or
   both heads, in either Gaussian orientation. All body directions are
   coordinate axes other than e0,e1.
3. Ordinary linear port matrices have coefficient functions of the collective
   squares Q_w^2, or more generally have the same defined scalar values at
   all spectral points constructed below. Coefficients must be defined when
   all these squares equal1. Arbitrary nonunitary port mixing and initially
   zero ancillas restored to zero are allowed. Spatial coordinate permutations
   outside this commuting algebra, column-specific ordinary coefficients,
   nonlinear and adaptive operations are not included.
4. Additional queries apply G=(product_w C_w^epsilon_w)^(tensor V), with
   integer exponents, directly on a field or in a nonself query shear. Put
   B=sum_w(epsilon_w mod2)ww^T over F2 and rho=rank(B). Their declared invoice
   charges at least rho^t per independent field queried. Rank-zero factors
   are ordinary. This is the primitive Gaussian-query accounting contract,
   not a lower bound on every conceivable implementation or improved supplier.
5. No additional productive-helper credit or uncharged head source is
   subtracted. The claimed original target inputs are independent.

**Theorem.** For every0<t<1, every fixed p,r,d and every all-width caller
satisfying1--5, the Gaussian moment surplus is strictly negative.
The same proof applies at every finite width
V>=2d+5*binomial(d,2). If d or r grows with V, this condition must be
checked; arbitrary growth is not covered by the uniformity argument.

The result fails before ordinary work, precision, erasure and all remaining
foundational/recursive expenses are charged. It is a source/interface
obstruction, not an integer multiplication lower bound.

## 2. Actual realization of every quadratic sign pattern

Let q(w)=sum_i a_i w_i+sum_(i<j)b_ij w_iw_j be any Boolean polynomial of
degree at most two, with no constant term. There is an actual Walsh character
on at most2d+5*binomial(d,2) columns such that simultaneously for every w,

    Q_w=(-1)^q(w), and Q_w^2=1.

For the monomial w_i, use two columns e_i. For w_iw_j, use one column e_i,
one e_j and three copies of e_i+e_j. The identity

    ell_w(e_i)+ell_w(e_j)-ell_w(e_i+e_j)=2w_iw_j

and3=-1 modulo4 prove the latter assertion. Concatenate the blocks for the
nonzero coefficients and pad with zero columns. Pad every q to the SAME
width bound, and then to any larger V. The all-zero character evaluates every
Q_w to1. Thus these are actual tensor-spectrum evaluations, not fictitiously
independent formal variables.

For cut0 fix the linear part w0; for cut1 fix w1. In each cut choose every
quadratic coefficient b_ij independently and uniformly. Then the native
heads are respectively(-1,1) or(1,-1), all body axes evaluate to1 and all
ordinary coefficient matrices agree with their values at the zero character.

## 3. True query rank, including dependent directions

For one column let g(z)=sum_w epsilon_w ell_w(z) modulo4. Then

    g(z+y)-g(z)-g(y)=2 z^T B y modulo4.

The inverse Walsh kernel of i^g is supported on an affine translate of im(B),
with exactly2^rho nonzero entries of magnitude2^(-rho/2). Here is a direct
proof. For y in ker(B), g(z+y)=g(z)+g(y), and g(y) is even. A nonzero kernel
entry at x requires (-1)^(x dot y)=i^g(y) on ker(B). This is a character of
ker(B), so it extends to a linear functional and defines a nonempty affine
space of size2^rho. The squared unnormalized Gauss sum is

    2^d sum_(y in ker(B)) i^g(y)(-1)^(x dot y),

equal to2^(2d-rho) on that space and0 elsewhere. Consequently the true
Gaussian rank is rho, even when B is alternating or displayed directions
cancel. Tensor powers have rank rho*V.

This is standard binary quadratic-form mathematics, consistent with Dehaene
and De Moor, Phys.Rev.A68(2003)042318,
https://arxiv.org/abs/quant-ph/0304125. The needed argument is supplied above;
no quantum computation or quantum speedup is being imported.

At the spectral sign pattern q, the query multiplier is (-1)^L_B(q), where

    L_B(q)=sum_i a_i B_ii+sum_(i<j)b_ij B_ij.

It depends only on B. Orientation signs and even exponents do not affect it.
A direct query or query shear has rank difference at most1 when this
multiplier is-1, and0 when it is+1. Multiplicity scales rank and price.

Let s(B) be the sum of the flip probabilities in the two random cuts.
If B has any nonzero off-diagonal entry, both probabilities are1/2 and
s(B)=1. If B is diagonal, s(B)=B_00+B_11 in{0,1,2}. Therefore, for0<t<1,

    rho^t >= 2^(t-1) s(B).

For s=1, rho>=1; for s=2, B has at least two nonzero diagonal entries and
rho>=2. The s=0 case is immediate. A single nonaxis rank-one query has
averaged weight1, not two free head incidences.

## 4. Averaged exact rank cuts

Changing either head sign alters H, or H^-1, by rank2 per port. The inverse
claim follows also from A^-1-B^-1=A^-1(B-A)B^-1. Product telescoping bounds
the rank of an endpoint difference by the sum of gate differences.
Ordinary factors remain unchanged. Restricting to original inputs and
projecting to demanded outputs cannot increase rank; restored zero ancillas
do not defeat the argument.

Let n_i be the number of independent productive targets containing head i.
In cut i the demanded diagonal endpoint difference has rank n_i. The2r
native calls contribute at most4rp. Set e_i=max(0,n_i-4rp). Averaging the
two inequalities gives

    e0+e1 <= sum_queries s(B),
    total query price >= 2^(t-1)(e0+e1).

No independence between query events is assumed. There is no restriction on
their number, directions or ranks. Linearity of expectation is sufficient.
Nonunitary ordinary port mixing is included; the spatial coefficient
restriction remains essential.

## 5. Head allocation and all-exponent majorization

Every productive body rank is at least7. By strict concavity, adding a head
has marginal reward at most delta=8^t-7^t, and

    delta < t*7^(t-1) < 2^(t-1)               (0<t<1).

Delete e0+e1 incidences until each head appears at most4rp times. The reward
lost is smaller than the necessary query price. It is favorable to grant
the remaining head assignment with zero queries, without claiming that such
a caller exists.

The at most8rp remaining incidences are allocated most profitably by putting
both heads on all4rp shorter targets and neither head on the2p long targets.
Even the second head of the longest short target starts at7r+1<=14r, the
first-head starting rank of a long target. Both separate axis caps are met.
Thus the favorable allowance, divided by p, is

    W_r=2(14r)^t+4 sum_(j=1)^r(7j+2)^t
                     -4 sum_(j=1)^(r-1)(7j)^t.

Its first difference is
2[(14r+14)^t-(14r)^t]+4[(7r+9)^t-(7r)^t], strictly decreasing in r.
Hence J_r=rW_(r+1)-(r+1)W_r decreases.

For every0<t<1, J1<0 follows from strict concavity and majorization:
A=(28,28,16,16,16,16,0,0,0,0,0,0) majorizes
B=(14,14,14,14,9,9,9,9,7,7,7,7). Both sums are120; sorted partial-sum
differences are14,28,30,32,39,46,37,28,21,14,7,0. Therefore
J1=sum A_i^t-sum B_i^t<0. It follows that W_r/r is globally maximized at r1.

At r1 the favorable per-native allowance is14^t+2*9^t. The equal-sum vectors
(14,9,9,0,0,0) and(8,8,7,7,1,1) have sorted partial-sum differences
6,7,9,2,1,0. Strict concavity gives

    14^t+2*9^t < 2(1+7^t+8^t),

the full native price. At t=1 equality holds; no strict endpoint statement
is made. At t=199/200 the independently enclosed predecessor gap is
0.0791417694912... per native/port, but this numerical value is not needed
for the new universal obstruction.

## 6. Verification, next construction and attribution

The exact JavaScript checker verifies all8,64,1024 quadratic sign patterns
in dimensions2,3,4; all8,64,1024 symmetric matrices; exact Gaussian integer
Walsh sums; the two averaged cut weights; and both majorization witnesses.
Controls demonstrate that a nonaxis query does not count twice, an
alternating rank-two B is not ordinary, and a single column does not support
every quadratic sign pattern. These finite controls supplement the written
all-d, all-width-qualified, all-exponent proof.

Independent Worker B review explicitly checked the spectrum construction,
query phase, rank bounds, averaging, both majorizations and quantifiers.
It required defined ordinary coefficients and either fixed finite d or
the stated V bound; those qualifications are now explicit. That is an
independent mathematical text review, not a second implementation run.

This closes nonaxis commuting-query repair of the retained chain. Changed
body incidence, noncommuting spatial permutations, productive helpers,
changed sources and legitimately improved query services remain live
construction directions, with all their physical costs owed. Both strict
suppliers and all five programme foundations remain open. No new complete
kappa or upstream PR is claimed.

Root developed the quadratic-sign and majorization extension after reviewing
Worker B's moving-head analysis. Credit @CubeJerry, the native/compiler and
caller predecessors, Dehaene--De Moor for the classical quadratic context,
and substantial OpenAI assistance.
