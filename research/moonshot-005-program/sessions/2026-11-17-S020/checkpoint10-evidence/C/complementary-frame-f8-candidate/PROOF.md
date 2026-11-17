# A conditional extension-field escape and its exact compiler boundary

**An algebraic three-round network exists with three-bit block coefficients.
This is not an admitted BIT primitive word. In fact the existing whole-record
ADD and within-record coordinate-permutation primitives alone cannot compile
these coefficient maps. No completed diagonal output or supplier is claimed.**

Worker C, S020. This package is a precise scope control and a conditional
constructive interface for the complementary-frame gate. It must not be
reported as a completed physical source.

## 1. Exact field and pair maps

Use K=F2[lambda]/(lambda^3+lambda+1). The cubic has no root in F2, hence is
irreducible; K is F8. More generally the formulas work in any characteristic-two
field with lambda nonzero, lambda!=1, and lambda^2+lambda+1!=0. Put

    f=1/(lambda+1),       g=lambda/(lambda+1).

Use the same two-record matrix at every pair in each successive round:

    T1=[[1,1],[1,lambda]],
    T2=[[1,f],[g,1]],
    T3=[[1,1],[1,lambda^-1]].

Their determinants are respectively

    lambda+1,
    (lambda^2+lambda+1)/(lambda+1)^2,
    lambda^-1+1,

all nonzero. The nontrivial elements of F4 do not work in this particular
family because they make the middle determinant zero. F8 supplies valid
choices. All three maps become invertible six-by-six binary maps on two
three-bit records.

## 2. Native seeds and actual meeting geometry

Let A_i,B_i, i modulo4, be the two frames with physical roles
[14,17,19,20] and [96,99,101,102]. Their eight native lines are mutually
orthogonal and form the real ambient basis. Initially put one native-unit
seed into each record:

    A_i reads x^A_(i+1),       B_i reads x^B_(i-1).

These are native accesses at actual retained native owners. The three matching
rounds pair A_i with B_i, then B_(i+1), then B_(i+2). At the first round let
P_i be the source pair {x^A_(i+1),x^B_(i-1)}. A second-round meeting spans
P_i union P_(i+1), and a final A_i/B_(i+2) meeting spans
P_i union P_(i+1) union P_(i+2). The omitted block is P_(i+3), precisely the
own sources {x^A_i,x^B_(i+2)}. Thus every final chart lies in both final
receiver facets, and every earlier chart lies in the later chart.

The public path ranks are exactly 0,1,2,4,6,7 for every record. Conditional
on local coefficient maps being admitted, the eight public routes have
profile24[1]+16[2], replacing8[7], with no owned movement. This is a route
invoice only; a local compiler and its costs remain missing.

## 3. Exact correction coefficients and arbitrary baselines

Direct propagation gives all three own-frame coefficients equal to1:

    l e a=1,
    l f c+m g a=f+g=1,
    m h c=1

for the A output, where T1=(a,b;c,d), T2=(e,f;g,h), T3=(l,m;n,o).
For the B output the corresponding coefficients are

    n e b=1,
    n f d+o g b=f lambda+lambda^-1 g=1,
    o h d=1.

The cross-frame middle coefficients cancel. After restoring each arbitrary
initial baseline y by the ground preconditioning below, the full new X parts
are therefore

    A_i: sum_(k!=i) x^A_k + x^B_(i-1) + lambda x^B_(i+1),
    B_j: sum_(k!=j) x^B_k + x^A_(j-1) + lambda^-1 x^A_(j+1).

Every listed input line lies in the actual final chart; the source's own
coordinate never appears. Each output has five native foreign terms.

Let M be the resulting eight-record K-linear network, including the three
rounds but not the unit seeds. Each layer is invertible, so M is invertible.
While all eight Ys are still ground, apply M^-1 to their arbitrary initial
values. Then acquire the eight native seeds and run the three rounds. The
final baseline contribution is M M^-1 y=y exactly; it does not require zero
Ys or erase any baseline direction. Existing axis preloads can be treated as
part of these arbitrary baseline values and are restored with them.

The checker records M, M^-1, the seed permutation, every meeting and chart
mask, and the complete final X matrix. It expands all K coefficients into
three-by-three binary matrices and verifies the full24 independent Y columns
and24 independent X columns. All12 single omitted pair interactions fail the
required own-frame triples.

## 4. The local BIT compiler obligation is substantive

This algebra does not authorize K-linear SCALE as a new BIT primitive. The
positive source interpreter currently uses scalar binary record ADD and its
declared source/movement operations. The Gaussian-dyadic complex-prefix
compiler is in a different characteristic and cannot be transplanted here.

There is even a direct obstruction to implementing this candidate using only
whole-record ADD and within-record coordinate permutations, with arbitrary
equal-width borrowed records restored. The subspace in which each record is
a constant binary vector is invariant under every such primitive. It is also
invariant under the inverse words. A local reversible two-record map built
from them restricts to an invertible scalar binary two-by-two map on the two
constant-vector coefficients. Consequently the complementary-frame binary
gate applies to such compiled local maps, even if their action on general
bit vectors is more complicated.

In the displayed polynomial basis, multiplication by lambda sends the
three-bit constant vector (1,1,1) to (1,0,1). It leaves the constant-vector
subspace, so it has no implementation by those primitives alone. For equal
widths divisible by3, repeating the same blocks has the same obstruction on
the all-ones input. Restored borrowed records do not remove the invariant.

Thus this package supplies an exact block-linear escape from the *unrestricted*
block-map version of the route gate, but does not escape the gate for the
strict whole-record ADD/permutation compiler. A broader local service would
need explicit authorization from the retained model, a literal implementation,
inverse/restoration, and its complete costs. None is supplied or assumed here.

## Reproduction and status

Run `python -B check.py --native NATIVE.json --out RESULT.json`.
The checker uses only standard-library exact integers. The finite field
representation uses modulus x^3+x+1; every nonzero field element is checked to
have an inverse. Physical source roots are pinned. No author or root checker
is imported. This is a conditional algebraic candidate and a compiler-scope
control, not an admitted BIT word, a new completed value, a full supplier, or
an improved multiplication exponent.
