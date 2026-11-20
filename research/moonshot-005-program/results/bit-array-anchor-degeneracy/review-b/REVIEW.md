# Independent review of the array-anchor degeneracy theorem

## Verdict and exact scope

**Accepted.** Under the retained separated-source, proper-route and exact
S028 target contract, the stated rank criterion excludes an arbitrary
array-linear anchor even when the other source maps and all subsequent
functions are arbitrary, with the original source banks kept separated.
A whole-bank bijection at the
anchor and independent bijective quotient labels do not evade the
argument.

The explicit determinant schema gives a necessary equation
`Delta_j(F)=0` for each eligible array anchor. For every positive integer
quotient width t this is a **nonzero homogeneous polynomial of degree
7200*t*t-434*t**. When all 99 eligible source systems are represented as
arrays, the 99 equations use disjoint coefficient blocks. Their common
zero locus has codimension exactly 99 in the unrestricted ambient affine
coefficient space over the algebraic closure of GF64. The feasible set is
contained in this locus; its own codimension may be larger, or it may be
empty.

This is a necessary algebraic obstruction. It neither rules out every
exceptional source nor supplies a source-change price, global return
bound, complete endpoint or improved exponent. The polynomial test is
coordinate dependent and weaker than the invariant rank criterion.

## Retained finite contract and roles

The review authenticates `SOURCE-PINS.json` and all its dependencies,
including the admitted single-anchor proof, its independent review and
the literal 99-anchor certificate. That earlier independent audit checked
all actual source and mixed-phase H cut capacities against the original
routes. Those unchanged physical premises are reused here, rather than
silently replaced by a scalar model.

The new checker independently rebuilds the native geometry, all 28-plane
source stars, all 6,470 native source views, and the reflected triangles
used by this theorem. It checks each propagation's fifteen distinct
receivers, actual simultaneous H/Q/R visibility, the reflected plane map,
and complete coverage of the final fifteen off-centre observations at
each leaf. The final transported sets each have fifteen planes, with
intersection ten and union twenty.

The anchor and both leaves are ordinary donors, excluding donor 10 and
the eleven singleton donors. Propagation and final receivers must be
native and different from 80. They need not have ordinary donor labels:
all eleven singleton-donor labels occur as receivers in the certificates.
The author corrected the corresponding wording in section 1.2 during
review. No mathematical change was required, and the corrected proof is
the version pinned by this review.

## Nonlinear propagation and source tightness

Write q=|K| and identify each original bank with V=K^(16t). For an ordinary
source and a native receiver other than 80, the exact target demands the
entire source input when other independent inputs are fixed. Its sixteen
source observations, each of capacity q^t, must therefore distinguish
q^(16t) inputs. Their joint map is a bijection onto the full product.
Consequently every individual quotient fibre has size q^(15t), and every
fibre obtained by fixing fifteen observations has size q^t. This argument
uses no linearity at the leaf.

At a shared H cut, fix all other inputs and both donors' off-H observations.
Let A and B be the corresponding q^t-element input fibres. The complete
mixed-phase H information available at the receiver has capacity q^t,
whereas the identity target distinguishes all sums in A+B. Thus
`|A+B| <= q^t`. Translation gives the reverse inequality, so equality
holds. The finite-group equality lemma makes A and B cosets of a common
additive subgroup of order q^t.

This is a statement about the **entire partitions**, not only fibres
through zero. For a fixed A, its stabilizer is independent of which B is
paired with it; the same holds after fixing B and varying A. All pairs of
fibres are attainable because the original banks are independent. Hence
both off-H partitions are the same coset partition in the original input
coordinates. The prior source-cut contract is essential here: there is
no inter-source preload, extra observation or bypass of the charged cut.

At the anchor, invertibility of the actual native matrix M_r follows
from the same source-tightness argument. Pullback by a bank bijection
psi and bijective output labels preserves injectivity. The linear off-H
fibre is `L_r = im(M_r^-1 E_H)`. Its dimension is t, and actual visibility
of R puts it inside `ker F_R`.

For one propagation record, the leaf's Q quotient is constant on each
of the fifteen off-H partitions: Q is among the fixed observations at
every listed receiver. The shared-H argument identifies these with the
anchor partitions pulled back by the same psi. A bijection preserves
joins of equivalence relations. The join of linear coset partitions is
the coset partition of the sum of their subspaces. If the span has
dimension 15t, it equals `ker F_R`; F_R has rank t because it belongs to
an invertible native source view.

The joined blocks therefore have size q^(15t). Every block lies in a
leaf Q fibre, which has the same size by source tightness. The partitions
are equal. This establishes the quotient propagation without assuming
linearity, affineness, or a common coordinate chart at either leaf.

After all thirty propagations, a leaf's final off-H3 partition is the
common refinement of its fifteen quotient partitions. On the anchor side
this is the pullback of the coset partition of `ker F_A` or `ker F_B`.
The leaf's source tightness forces both kernels to have dimension t.
The final shared H3 cut forces the two partitions to agree. Canceling
the same bijection psi makes the two linear coset partitions equal;
their classes containing zero, and hence their kernels, are equal.
Therefore `rank F_(A union B) = 15t`, contradicting the stated rank
criterion. Nonlinearity at the leaves or in the remaining computation
cannot invalidate this partition argument under the retained contract.

The same argument permits any finite family of admissible propagation
receivers whose span saturates `ker F_R`; exactly fifteen receivers are
not essential to the invariant criterion. Every selected receiver must
still be native, differ from 80, and see H, Q and R. This observation
does not change the frozen polynomial schema, which uses its original
fifteen-column-block certificate. Applications to other frozen arrays
or larger receiver families require their own finite rank certificates.

## Polynomial construction and degree

For each native view, `C_r = adj(M_r) E_H` has polynomial entries of
degree 16t-1. In a completion `det M_r` is nonzero, so multiplying an
inverse basis by that determinant does not change its column space.
Concatenating the fifteen blocks gives 15t columns. The minor after
deleting the first t rows is homogeneous of degree
`15t*(16t-1)`. If this minor is nonzero, the span has dimension 15t;
actual R visibility bounds that dimension above by 15t.

The final minor stacks sixteen distinct planes chosen in increasing
order from the twenty-plane union. It is homogeneous of degree 16t.
Nonvanishing forces final union rank 16t, which is stronger than the
criterion's required rank greater than 15t. Thus a completion cannot
make all thirty propagation minors and this final minor nonzero.
Their product is necessarily zero. No determinant denominator is
retained in this equation, and no assumption about generic inversion is
used at a singular tuple: feasibility itself supplies the required
native invertibility.

The product's exact degree is

\[
30\,(15t)(16t-1)+16t=7200t^2-434t.
\]

All factors are homogeneous in the same donor's independent source
entries. Repeated use of an entry in different native views does not
alter this degree calculation. The nonzero witness below excludes
complete cancellation. The scalar degree is 6766; at the physical
quotient width t=240 the degree is 414,615,840. This large degree is an
algebraic description, not a communication charge.

## Exact nonzero witness, including all positive widths

At scalar width one, the checker obtains each adjugate column by dense
Gauss-Jordan inversion of the actual sixteen-plane evaluation matrix.
This is independent of the author's annihilator-polynomial and
interpolation formula. The only reused arithmetic is the pinned earlier
independent stdlib GF64 multiplication table. Matrix inversions use
last-available pivots; selected determinants use reverse column order.
No author Python module is imported or executed.

All **4,422 distinct native matrices** are inverted. All **5,960 distinct
adjugate columns** satisfy the literal identity `M C = det(M) E_H`.
The checker independently evaluates every one of the **2,970 selected
propagation minors**, all **99 final sixteen-plane determinants**, and
all **99 complete scalar polynomial values**. Every value agrees with
the published receipt and is nonzero. Duplicate propagation-column and
duplicate final-plane controls produce zero determinants as required.

For completeness, the infinite-width extension follows from a precise
tensor identity, rather than those finite checks. Write D_r for the
scalar native determinant, c_r for its scalar adjugate column, and d_1
for one selected scalar propagation minor. At the tensor RS tuple,

\[
M_r(t)=M_r(1)\otimes I_t,\qquad
\det M_r(t)=D_r^t,
\]

and hence

\[
\operatorname{adj}(M_r(t))E_H
=D_r^{t-1}(c_r\otimes I_t).
\]

The chosen deletion removes exactly the t constant-coefficient rows.
It therefore gives the scalar selected minor tensored with I_t, with
each group of t columns additionally scaled by D_r^(t-1). Its determinant
is exactly

\[
d_t=d_1^t\prod_{r=1}^{15}D_r^{t(t-1)}.
\]

All factors are nonzero. The selected final determinant similarly equals
the scalar final determinant to the power t. If B_j is the product of
the 450 scalar native determinants occurring in the thirty records,
counting repeated occurrences, then at the tensor RS tuple

\[
\Delta_j(t)=\Delta_j(1)^t B_j^{t(t-1)}\ne0
\quad\text{for every integer }t\ge1.
\]

The proof applies over GF64 and every finite extension, including widths
divisible by the characteristic. No exponent is divided by t. The first
coordinate of every scalar RS evaluation row is one, so deleting the
constant coordinate is injective on its fifteen-dimensional kernel;
this also explains why the selected scalar row minor is appropriate.

As an ordering control, the checker directly constructs and inverts all
fifteen tensor native matrices for one propagation at t=2 and t=3. It
verifies every tensor adjugate column and the complete selected minor
against the displayed scaling formula. These controls corroborate the
implementation; the algebraic identity proves the assertion for every
positive width. The algebraic schema itself does not claim a physical
compiler at every abstract width.

## Codimension and quantifiers

For a fixed positive t, one eligible donor has 28 independent t-by-16t
coefficient blocks: its unrestricted ambient affine space has dimension
448t^2. The witness shows Delta_j is a nonzero polynomial. Its positive
homogeneous degree makes it nonconstant and ensures it vanishes at the
origin. Over the algebraic closure, its zero set is therefore a nonempty
proper hypersurface of dimension 448t^2-1.

When all 99 eligible donors are array systems, the variables of their
necessary equations are disjoint. The simultaneous zero locus is the
Cartesian product of these 99 hypersurfaces. Dimensions add, giving
dimension `99*(448t^2-1)` inside dimension `99*448t^2`, hence codimension
exactly 99. Additional unrestricted donor parameters can be appended as
free factors without changing that codimension. A subset of m array
anchors gives the corresponding m necessary disjoint-variable
conditions; unrestricted nonlinear source maps at other donors are not
being assigned nonexistent array-coordinate variables.

This is a statement about the common zero locus in the **unrestricted
ambient coefficient space**. Restricting to a deliberately structured
construction family may make some equations identically vanish on that
family. Restricting to native-invertible tuples is an additional open
condition; its intersection with the necessary locus can be empty.
Neither operation justifies claiming codimension 99 inside that smaller
family. Nor does the theorem assert that the feasible set itself has
codimension exactly 99.

There is no asserted sampling probability over a fixed finite field.
Nonzero polynomials of high degree need not exclude a prescribed large
fraction of finite-field tuples. Here the explicit RS evaluations prove
nonzeroness, while the codimension conclusion is taken over the algebraic
closure. No characteristic-zero genericity is asserted.

## Practical interpretation and limits

If the actual thirty spans saturate, a successful source must make the
two final transported kernels agree. If they do not agree, at least one
propagation must remain genuinely unsaturated. Merely changing source
coefficients or making a chosen determinant vanish is insufficient:
a coordinate-dependent selected minor can vanish while the invariant
span still has full dimension. Conversely, failing this chosen test
does not certify extendability.

All target, source independence, finite alphabet, actual route and
capacity assumptions remain in force. The result does not cover a
general nonlinear anchor outside the stated array information system,
informative inter-source preparation, enlarged cuts, a different target,
or an altered route contract. No application to the frozen general,
hybrid, or all-donor constructions is admitted by this review alone;
those applications require separate pinned rank witnesses.

## Replay and attribution

From the repository root:

```sh
python -I -B research/moonshot-005-program/results/bit-array-anchor-degeneracy/review-b/check.py --repo . --out /tmp/independent-array-anchor
```

`RESULT.json` contains all independently evaluated scalar polynomial
values, tensor scaling factors, controls and source pins. The checker
uses only exact standard-library field arithmetic. The finite receipt
and the unbounded-width/algebraic proof audit above are distinct parts
of the review.

Independent OpenAI-assisted review by Worker B, session S030. The reused
independent GF64 implementation and single-anchor audit retain their
prior attribution and repository license. No author constructor or
checker was imported as an implementation dependency, and no author file
was edited by this reviewer.
