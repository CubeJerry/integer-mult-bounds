# Independent review of the nonclean idle wrapper and two-bank reduction

Accepted subject to the scope clarification below and the final proof hash
recorded in `control/RESULT.json`. The reduction isolates a genuine rank1
job on an independent third input. It does not claim the remaining two-bank
equation has been solved or that its component ranks alone would suffice.

For beta=a^-1 b a ordinary, literal multiplication gives middle row
(a,b a,a)=a(I,beta,I) in LCU. The stated last row of Q cancels both first
columns exactly and leaves the third column a. The other two rows have
zero third column, and their active2x2 block is exactly

    diag(a,I) [[I,b],[u,f+u b]] U_A Q_A L_A.

This is a free noncommuting identity using only b a=a beta. No inverse
source query, commuting block shortcut or discarded scalar phase appears.
C is a unit by its two-bank shear/scale factorization and the displayed
three-bank implementation; Q is a unit by its actual Q_A and two row shears.
Exact ordinary input/output gauges taking this2x2 operator to independent
heads(4,2) would therefore give the full independent(4,2,1) endpoint.

The physical C sequence is correct on three arbitrary independent banks:
the b shear, swap of banks1/2, ordinary bank1 ADD, f service and u shear give
the declared matrix. Root lowers a literal instance to primitive unweighted
ADD, sign SCALE and monomial services, with a separately lowered inverse.
For b=D_c, beta=D_d, u=S^-1 D_b and f=X_a, the forward word uses6 ADD,
3 SCALE and5 monomial services; the inverse uses6 ADD,9 SCALE and5 services.
The source of each monomial shear is restored by the actual inverse service.
The3-ADD/3-sign-SCALE swap and negative inverse ADDs are fully included.

The Q wrapper adds two actual signed shears after an explicit two-shear Q_A
control. The complete control and inverse each use4 ADD,4 sign SCALE and
6 monomial services. This is one Q_A example, not the unknown42 solution.
Root verifies both two-sided inverses, the exact isolated middle row, every
literal root-four service table and omitted-ADD failures. The four primitive
words are emitted and pinned. Safe width-independent triangle-inequality
prefix bounds for these words are8,13,6,3 respectively. The generic bounds
64 for C and4 for the Q wrapper remain conservative.

The general statement requires **the full Q** outside the square algebra in
the clean-top-two case. It need not require Q_A outside that algebra: for
b=D_c, the beta=D_d wrapper is already a literal outside-square control,
since A² beta A^-2 has support2. By fixed finite tensor separation its tensor
lift cannot be a hidden finite linear combination of square-class lifts at
sufficiently large faithful widths. For b=0 the wrapper is scalar ordinary,
so the outside-square condition does reduce to Q_A. This qualification
preserves useful construction freedom and must be retained in the admission.

No monomial service is free: each needs the admitted coordinate/phase recipe
and full field-volume tariff. All ordinary signs/scales, inverse work, source,
ownership, layouts, precision/tape and recursive costs remain. The branch-free
reduction is all-width; necessary component gates separately use their faithful
width threshold. The global five foundations, strict suppliers, exact42 gauges
and complete target theorem remain open. No new kappa.
