# Independent review of scalar local-linearity gluing

**Verdict: accepted in its stated scalar characteristic-zero interface. No new κ.**

## Reviewed immutable artifacts

Repository: CubeJerry/integer-mult-bounds.

- Author proof: cb494fe6ccaa369d1adca4bd71e63cf0c61cde6c.
- Source verifier: bdebc1879a26ae35df73c8a013d225fbdd2016c8.
- Source certificate: cbf27dc258f7f8e4ec7a595564ee64f369bf1262.
- Exceptional rank-two verifier: d346dd32dd525273cce4b0b0a85f31a6edbabe70.
- Exceptional rank-two result: 1c74e0e0d8037bc30240609493ca804e551cf7d0.

The author proof and checker were read. Neither author checker was imported or executed. The independent verifier uses the rational nine-coordinate root model, exact integer row elimination with gcd normalization, and recursively evaluated Laplace minors. Its row selection runs in reverse source order, producing different witnesses. The available JavaScript engine executed the complete independent verification.

The native inventory is the published 104 roots obtained from all weight-three/weight-seven nine-bit normals minus the sixteen omitted roots. Root separately authenticated the native gzip and checked this exact inventory. That source binding is not a claim that the reviewer re-read unavailable filesystem bytes.

## Mathematical review

The source span assertions are correct: each forbidden donor set spans the seven-dimensional orthogonal hyperplane, and the common forbidden set of each distinct pair spans the six-dimensional orthogonal complement of the two roots. Distinct projective roots are independent, so the displayed annihilators provide exact upper bounds; the independent integer witnesses give matching lower bounds.

For each active scalar decoder row, division by its nonzero coefficient defines its local representative. Agreement on the common forbidden donors puts the difference of two representatives in the span of their two root directions. The associated affine lines therefore meet pairwise. The affine-line lemma is valid over any characteristic-zero field: three independent directions force concurrence, after which another line meeting all three must pass through the same point. No positivity or ordering of the coefficient field is used here.

The common point yields one globally removable Gram-row component of h. Its remaining vector g is supported in the intersection of the allowed donor sets. The forbidden-span lemma then makes every residual Gram component proportional to its own root. Enforcing the unit diagonal gives precisely

\[
 K=\operatorname{diag}(1-t\odot g)\,G+t g^T.
\]

The inactive rows are exactly G. The converse follows entrywise and its rank bound is eight plus one. The support argument gives at most 49 active rows for a genuine single extension. The claim is about a scalar extension of the fixed eight-dimensional row space, not an arbitrary rank-nine fitting matrix whose row space need not contain or lie in that extension.

The small exceptional span is handled correctly. Rational root ranks are unchanged on characteristic-zero field extension. In the real plane, the allowed root directions have mutual projective angle at least sixty degrees, so at most three can occur. The proof retains this exception.

## Independent exact evidence

All 104 single-forbidden sets have size 55 and rank seven. All 5,356 distinct pairs have rank-six common-forbidden span. Every independent witness has a nonzero integer minor. The overlap histogram agrees in all six cells with the author's certificate.

The rank-two counterexample uses the actual normals 13,505,11 and the root relation c=a+b. In the independent Q9 model the norm squared is 18 and a dot b is minus nine. The same fitting matrix is represented without fractions as 18K:

- All 10,816 entries satisfy the unit diagonal and forbidden zeros.
- Every inactive row equals its original Gram row.
- The full matrix has exact rank nine.
- A newly chosen minor, with row normals 508,506,505,502,494,478,446,416,382 and column normals 13,11,21,14,19,26,35,69,131, has determinant -6,198,727,824.
- The author's quoted minor, converted to the 18K scaling, has determinant 12,397,455,648. This equals (9/4)^9 times 8,388,608, as required.
- The inactive roots still span eight dimensions.

The three affine lines are pairwise intersecting without concurrence. Thus no common Gram component can remove all three local restrictions. The example establishes that the active-span hypothesis cannot simply be deleted.

Negative controls independently confirm a rank-seven self-pair; rank-five overlap after the explicit ten-root deletion; a zero determinant after duplicating a witness row; failure of the unit diagonal after changing the exceptional diagonal coefficient; and forbidden-entry failure after deleting the third local correction.

## Scope and publication status

This review accepts the scalar algebra and finite source-span certificates. It does not admit a physical word, a new source invoice, restoration of original endpoints, an arbitrary operator-valued factorization, or an all-volume algorithm. In particular, nonzero singular block decoders cannot be divided by as in the scalar proof. The approximate 118.29307104377714 optimistic new-architecture envelope is an allowance, not a realization.

An independently proved sharp perturbation corollary appears separately in RANK-EIGHT-COROLLARY.md. Its computational corroboration is included in the independent receipt; it is an extension of the review, not a claim already made by the author's frozen proof.

Credit: @CubeJerry programme. Global-code authored the gluing package and exception; global-adversary performed this independent proof review and reconstructed the exact evidence. AI-assisted research.
