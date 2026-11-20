# Worker B review of the outside-control rank corollary

**Acceptance:** the root's corollary is mathematically correct under the hypotheses of the accepted conditional source-hub theorem. It is a necessary condition for a successful completion, not a certificate that a candidate circuit succeeds.

Let C have 909 columns and full column rank, with row blocks C_a and C_z. A completed circuit has C_a U=E_ax. The independently reconstructed source matrix E_ax has rank 376. Therefore

    rank(C_a) >= rank(C_a U) = 376.

On ker(C_a), the map C_z is injective. Indeed, C_a v=0 and C_z v=0 together give Cv=0, so v=0 by full column rank of C. Consequently, for W=C_z(ker C_a),

    dim W = dim ker C_a = 909 - rank(C_a).

The completion theorem requires the 370 columns of L to be independent and their span together with W to equal the 902-dimensional stock space. Hence

    902 <= 370 + dim W
        = 370 + 909 - rank(C_a),

which gives rank(C_a) <= 377. Combining the bounds proves

    376 <= rank(C_a) <= 377.

There are two exact boundary cases. If rank(C_a)=377, then dim W=532 and span(L) intersects W only at zero. If rank(C_a)=376, then dim W=533 and the intersection has dimension exactly one. These follow from the dimension formula once the completion theorem's rank and spanning conditions hold.

The argument works over Q and any field on which the stated source ranks and invertibility hypotheses hold. It does not assume numerical conditioning or use a rank tolerance.

## Distinction from current exploratory observations

A modular replay giving rank 376 modulo 1000003 is a rational **lower bound** when every source denominator is nonzero modulo that prime. It becomes a rational equality only after a separate exact upper bound is supplied. Numerical singular values close to zero give neither an exact upper bound nor an exact rank certificate.

The two current numerical fits have not been certified as complete rational circuits. Their small trailing singular values do not satisfy the corollary by themselves and do not discharge the other completion conditions. No positive supplier or new kappa follows from this review.

Reviewed by S031 worker B, 2026-11-20.
