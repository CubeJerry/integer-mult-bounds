# Every extendable array anchor must satisfy an exceptional rank condition

**Author theorem pending independent review. No new complete κ.**

The earlier single-RS-anchor obstruction extends to a criterion on arbitrary array-linear source observations. The other source banks and downstream computation may still be arbitrary separated functions. At every one of the 99 eligible ordinary donors, one fixed native triangle supplies an explicit nonzero polynomial which must vanish on any extendable array source. Consequently a generic array source cannot be repaired by redesigning its neighbours alone. This is a necessary algebraic condition, not a new paid lower bound or an impossibility theorem for deliberately degenerate sources.

## 1. Interface, arrays and the fixed triangle certificates

Retain exactly the separated-source, actual proper-route and exact S028 target contract of the [admitted single-anchor theorem](../../bit-single-rs-anchor-obstruction/ADMISSION.md). In particular, there is no informative inter-source preload, additional source observation, extra proper path or return descent. All bank inputs are independent. Target row80 and donor10 are excluded whenever identity demands are used. The eleven singleton donors are excluded from anchor and leaf roles. Actual source and shared-H capacities are the independently reconstructed ones in that theorem.

Let K be any finite extension of GF(64), let t≥1, and let V=K^(16t). One ordinary donor j supplies28 observations

    F_R x,     F_R in Mat(t,16t;K),

one for each native plane R through j. At physical bank3840 the quotient width is t=240; the statement also covers positive proportional repetitions. The whole tuple may be pulled back by an arbitrary bank bijection ψ:V→V, and every observation may have its own bijective output labels. The criterion concerns the underlying linear tuple F. Other donors need not be linear.

For each eligible j, use its literal triangle (j,k,l;H1,H2,H3;i) and the30 quotient-propagation records in the frozen99-anchor certificate. Each record (H,Q,R; r1,...,r15) says:

1. H contains j and one leaf, Q is an off-H plane at that leaf, and R is its reflected plane at j.
2. The fifteen distinct receivers are native receivers other than80, perpendicular to H, Q and R.
3. At each receiver r, j has exactly16 visible source planes, including H and R.
4. At final receiver i, the fifteen off-H3 quotients at the two leaves transport to two sets A and B of15 distinct anchor planes. Their intersection has10 planes, so their union has20.

These are fixed combinatorial facts, separately reviewed in the preceding theorem. Their dependence does not require any RS coefficients in the new source.

## 2. Rank criterion for one arbitrary array anchor

Let M_r be the16t-square matrix stacking the anchor's sixteen visible F_R blocks at receiver r in increasing plane order. A completed computation forces each M_r to be invertible: fixing all other original inputs, its source view must distinguish the entire anchor bank. A bank bijection or bijective output labels do not change that requirement.

For a record with centre H, write E_(H,r) for the16t-by-t coordinate insertion at H's block of M_r, and put

    L_(H,r) = im(M_r^(-1) E_(H,r)).

This is the t-dimensional kernel of the other fifteen visible anchor observations. It lies in ker F_R for every receiver in the propagation record, because R is one of those other observations. Define the propagation sum

    S_(H,Q) = sum over its fifteen receivers r of L_(H,r).

If dim S_(H,Q)=15t, it equals ker F_R. Here F_R has rank t because it is a block of an invertible native view.

**Anchor criterion.** Suppose all30 recorded propagation sums have dimension15t, and the stacked observations on A∪B have rank greater than15t. Then the source tuple at j cannot occur in any completion under the retained contract, even after arbitrary bank/output bijections and even if all other source maps and downstream functions are redesigned.

To prove this, the finite-alphabet tightness argument from the preceding theorem makes each leaf's sixteen-message view a bijection. Its individual quotient fibres have size |K|^(15t), and each off-H fibre has size |K|^t. The shared-H capacity and additive identity demand force the entire off-H fibre partitions at j and that leaf to agree. This applies to all fibres, not only to their linear fibres through zero.

The join of the anchor partitions for the fifteen receivers is the coset partition of S_(H,Q), pulled back through ψ. Saturation makes it the anchor R-quotient partition. The leaf's Q-message is constant on every partition being joined, hence on the join. Both quotient fibres have the same size, so the two quotient partitions coincide.

Repeat for the30 records. At final receiver i, the two leaf off-H3 partitions are therefore the pullbacks of the anchor partitions with kernels ker F_A and ker F_B, where F_A and F_B stack the respective15 observations. Tightness forces each kernel to have dimension t. The H3 cut forces the two pulled-back partitions to coincide. The same bijection ψ preserves their equality, so ker F_A=ker F_B. Their common kernel has dimension t, giving rank F_(A∪B)=15t, a contradiction.

No step assumes linearity at either unrestricted leaf. The characteristic-two additive group supplies the sumset equality, and the anchor's linear coordinates are used only for its partition joins.

## 3. An explicit necessary nonzero polynomial

Fix the standard original-coordinate ordering at j. For each record, replace the rational inverse basis by the polynomial matrix

    C_r = adj(M_r) E_(H,r).

Whenever det M_r is nonzero, C_r has the same column space as M_r^(-1)E_(H,r). Concatenate its15 blocks into a16t-by-15t matrix C. Let d_(H,Q)(F) be the determinant after deleting the first t rows of C. A nonzero d certifies the required saturation. A zero d need not mean the span is deficient: this deliberately chosen minor gives a sufficient obstruction test.

Choose the first16 planes in increasing order from A∪B, and let e_j(F) be the determinant of their16t-square stacked observation matrix. Define

    Δ_j(F) = e_j(F) times the product of all30 d_(H,Q)(F).

Every exact completion with an array anchor satisfies **Δ_j(F)=0**. Indeed, all needed native views are invertible in any completion. If Δ_j were nonzero, every propagation would saturate and the final union rank would be16t, contradicting the criterion.

The polynomial is homogeneous of degree

    30(15t)(16t−1)+16t = 7200t²−434t.

This is an explicit algebraic schema; expanding its coefficients is unnecessary. It uses only determinants, adjugates, insertion matrices and the finite native certificate. The denominator-free form is useful because the necessary vanishing statement is a genuine polynomial condition in the28 independent t-by-16t source blocks.

## 4. Nonzero witness at every positive width

Use the actual node assignment a_R=1,...,28 in increasing source-plane order and the tensor RS tuple

    F_R = (1,a_R,...,a_R^15) tensor I_t.

Every native view is Vandermonde tensor I_t and invertible over GF(64). At t=1 the15 off-H kernel directions in each propagation record have rank15 by the existing independently checked certificate. Their common annihilator F_R has first coordinate1, so deleting the constant coefficient gives an isomorphism from ker F_R to K^15. Thus the chosen15-by-15 minor is nonzero. Scaling each kernel column by the nonzero det M_r leaves it nonzero.

For general t, after grouping tensor coordinates, the relevant matrix is the scalar one tensor I_t, with each adjugate column additionally scaled by a nonzero power of its scalar Vandermonde determinant. The selected minor remains nonzero. The final16 chosen planes are distinct, so e_j is also a nonzero Vandermonde tensor determinant. Therefore **Δ_j is not the zero polynomial for any positive t**, over GF(64) or any of its extensions.

The accompanying checker separately evaluates the scalar adjugate-column formula, verifies M_r C_r = det(M_r) E_H, computes every one of the2,970 chosen minors and all99 final16-node determinants, and evaluates each Δ_j. It checks duplicate-column and duplicate-final-plane faults. The proof by tensor products extends the result to unbounded positive width; finite-width experiments are not used as its substitute.

## 5. Consequences and limits

For each of the99 eligible donor labels, extendability of an array-linear information system requires a nontrivial exceptional condition Δ_j=0 in that donor's own coefficient blocks. In the ambient affine coefficient space over the algebraic closure of GF(64), these99 conditions involve disjoint donor variables. Their common zero set has codimension99: each nonzero positive-degree polynomial defines a hypersurface, and the product dimensions add. The feasible source set is contained in that common zero set and may have still higher codimension or be empty. This codimension statement is about the unrestricted ambient source arrays, not about every deliberately constrained construction family or about a finite-field sampling probability.

The invariant rank criterion is stronger than the particular chosen polynomial test. A successful source can escape a chosen minor by a coordinate accident while still failing the rank criterion. To escape the criterion itself, at least one required propagation span must be unsaturated, or the two final transported15-plane kernels must agree. These give concrete structured design requirements. The local hybrid construction's unsaturated quotient flags illustrate the relevant kind of freedom, but no claim that it satisfies every anchor condition is made here.

The result does not price a source change, exclude all exceptional arrays, prove a new global return lower bound, or rule out larger informative cuts, different routes, inter-source preparation, different targets or general nonlinear sources not equivalent to the stated array observations. All111 changed source banks can still fail this stronger test; changing information alone is insufficient. No strict supplier, complete κ or foundational discharge follows. Credit @CubeJerry, the native geometry, source-cut, array-source and prior single-anchor authors/reviewer; substantial OpenAI assistance.
