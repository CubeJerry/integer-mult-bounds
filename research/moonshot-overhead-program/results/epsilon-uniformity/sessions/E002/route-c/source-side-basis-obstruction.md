# No single coordinate basis for all canonical source-side variations

Status: **proved scoped linear-algebra obstruction; independent review
requested**. This tests one possible way to simplify the endpoint layouts.
It does not rule out cheap endpoint maps, alignment of the larger full
endpoint spaces, sparse representations, or improved routing algorithms.

Source pin: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`interchange.tex`, rational Gram geometry and endpoint preparation.
The characteristic-two label version and canonical rectangles are those
of the prior programme and `canonical-incidence-exactness.md`.

## 1. The exact strategy being tested

For a source side L of a canonical directed rectangle, fix `v0 in L`.
Its one-sided variation space is

\[
E_L=\operatorname{span}_{\mathbb Q}
 \{x_v-x_{v0},\ y_v-y_{v0}:v\in L\}
\]

inside the rational address space D, the quotient of the Gram generators
by the radical. A tempting strong simplification would choose one fixed
basis of D such that **every** E_L is spanned by a subset of that basis.
Then these variation spaces could all be selected by coordinate subsets.
The theorem below disproves exactly that simultaneous coordinatization.

The source endpoint space includes differences from both oriented sides,
and is generally larger than E_L. The theorem does not assert that
coordinatizing those larger spaces is equivalent to this stronger strategy.

## 2. Four canonical source sides

Let d>=2, `h=2d-1`, and `q=2^t>=4`. In the inner word space
`[q]^h`, let u_ab have all coordinates zero except its last two,
which are a,b in {0,1}. Write w0 for the all-zero inner word and set

\[
v_{ab}=(u_{ab},w_0,\ldots,w_0)
\]

in the outer label space. The four two-label sets

\[
\{v_{00},v_{10}\},\quad \{v_{01},v_{11}\},\quad
\{v_{00},v_{01}\},\quad \{v_{10},v_{11}\}             \tag{SB1}
\]

are source sides of canonical outer rectangles.

To verify this directly, first make an inner side that varies in one of
the last two coordinates. Choose d differing positions including the
first coordinate and the desired varying coordinate. At the first fix
the ordered letters (0,1). At d-2 other selected coordinates use a
last-bit rectangle with source singleton {0} and destination singleton
{1}. At the varying coordinate use the dyadic rectangle with source
{0,1} and destination {2,3}; it is present for every q>=4. Fix all
unselected letters to the prescribed corner values. The resulting source
side is exactly the required inner edge.

At the outer level choose d differing positions including the first.
Use this edge in the first position and canonical inner rectangles with
singleton source w0 in the other selected positions. Set every remaining
inner word to w0. Such singleton inner sides use fixed (0,1) at the first
selected coordinate and last-bit singleton rectangles at the others.
This constructs all four sides in SB1 within the retained partition.

## 3. Their three independent directions survive the Gram quotient

The rational Gram blocks give

\[
\langle x_v,x_w\rangle=1-k(v,w)/d,\qquad
\langle x_v,y_w\rangle=k(v,w)/d.
\]

Consequently `x_v+y_v` has the same pairing with every generator for
every v, so these sums are equal in D. Hence y-differences are the
negatives of x-differences, and each side in SB1 has a one-dimensional
variation space if its x-difference is nonzero.

For each r,s in {0,1}, choose a probe inner word z_rs that has d-2
ones in fixed positions preceding the last two coordinates, zeros in all
other preceding positions, and last two coordinates r,s. There are enough
preceding positions because `h-2=2d-3>=d-2`. Let
`w_rs=(z_rs,w0,...,w0)` be the outer probe label. Then

\[
k(v_{ab},w_{rs})
=\mathbf 1_{a\ne r,\ b\ne s}.
\]

Indeed the inner distance is `d-2+[a!=r]+[b!=s]`, and all other
outer coordinates are equal. For coefficients with `sum c_ab=0`,

\[
\left\langle\sum_{a,b}c_{ab}x_{v_{ab}},x_{w_{rs}}\right\rangle
=-c_{1-r,1-s}/d.                                    \tag{SB2}
\]

If the zero-sum combination vanished in D, all these pairings would
vanish, forcing all four coefficients to vanish. Thus the three vectors

\[
p=x_{v_{10}}-x_{v_{00}},\quad
q'=x_{v_{01}}-x_{v_{00}},\quad
r'=x_{v_{11}}-x_{v_{00}}
\]

are linearly independent in the actual rational quotient, not merely in
an ambient formal one-hot representation.

## 4. The four-line obstruction

**Theorem SB.** No single basis of D makes every canonical source-side
variation E_L a coordinate subspace, for any d>=2 and q=2^t>=4.

**Proof.** The four sides in SB1 have variation lines

\[
\langle p\rangle,\quad \langle r'-q'\rangle,\quad
\langle q'\rangle,\quad \langle r'-p\rangle.
\]

These are four distinct lines in the three-dimensional span of
`p,q',r'`. If all were coordinate subspaces in one basis, each would
be the span of one basis vector. Distinct coordinate lines correspond to
distinct basis vectors and are linearly independent, a contradiction.
Equivalently their oriented edge vectors have the four-cycle relation
`p+(r'-p)-(r'-q')-q'=0`, with no two lines equal. ∎

The relevant characteristic-two geometry uses d a power of two, which
is contained in this theorem. The address algebra here is rational;
the argument does not divide by two in the characteristic-two data field.

## 5. What remains possible

A common basis with uniformly sparse, rather than coordinate, descriptions
is not excluded: these four lines already have two-sparse descriptions in
the displayed three-vector basis. Nor does the theorem exclude different
bases for different rectangles, coordinating larger full endpoint spaces,
shared transforms between bases, or an improved rectangle family.

The test is useful because it prevents replacing the source's family of
endpoint changes by an unproved assertion that every canonical source box
is a coordinate subset in one universal basis. Any such replacement must
use a weaker and explicitly priced structure. It establishes no running-
time lower bound and is not a premise of the positive envelope theorem.

Credits: @CubeJerry; the pinned rational Gram construction; the canonical
rectangle partition; substantial ChatGPT multi-agent assistance. This is
a complete written scoped proof, not a formal build or tape execution.

## 6. Finite supporting checks

`verify_source_basis_obstruction.py` checks d in {2,3,4,8,16} and
q in {4,8,16}. For all 15 pairs it constructs the four source sides
and destination witnesses, checks their far-count Gram conditions, and
computes the exact rational probe rank. All 60 three-edge subsets have
rank three, while the full four-edge set has rank three and its stated
cycle relation. All 15 wrong-probe-offset controls lose the required
rank. The receipt is `source-basis-verification.json`. These are finite
supporting checks; SB2 and the four-line argument prove the universal
statement in the specified model.
