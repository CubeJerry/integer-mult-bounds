# Independent review of full-parabolic Lagrangian cut potentials

**PASS in the stated representation and potential families. No new κ.** Reviewed Worker B's proof SHA256 `930eecd13fbb0bcdab1fe0bd5662d76b025016cb731b7902f7287832e47217ea` and the exact source/certificate pins recorded in `RESULT.json`. This review does not claim a conservation theorem for arbitrary full-ordinary callers.

## Independent reconstruction

The author enumerates unordered isotropic bases. I instead enumerate every reduced-row-echelon three-dimensional subspace of F2^6:1395 distinct subspaces, of which135 are isotropic. The complete135-space list matches the published certificate exactly after adding the zero vector. No author generator or checker is imported.

I independently implement six GL3 transvections and six symmetric shears. These generate the full stabilizer of a Lagrangian: a stabilizing symplectic matrix factors into its invertible GL3 block and a symmetric shear; elementary transvections generate GL3(F2), and the six symmetric basis matrices generate every shear. My reference is the x-coordinate Lagrangian, conjugate by the full coordinate swap to the author's z-coordinate reference. The exact action has four orbits of sizes1,14,56,64, classified by intersection codimension. All generators preserve the symplectic form and the reference Lagrangian.

The eight radial cuts up to complement give exactly the published table. In my convention the cuts omit shell0; complementing them matches every author's positive-shell row. Every nontrivial cut has h1>0 and satisfies h2<=h1 and4h3<=5h1. The inequalities therefore separate the complete nonnegative cone from nonzero rank-two additivity. This is exhaustive for the specified H-invariant diagonal sign operators, not for all H-intertwiners.

All63 lines are independently recovered as intersections of their15 containing Lagrangians. This proves faithfulness of the group action exactly as stated. It does not prove faithfulness of the associated group algebra, and the author correctly retains that distinction.

## Mathematical proof audit

For a permutation matrix, each mismatched sign column of rho(g)−Jrho(g)J has one nonzero coefficient in a distinct row. Its rank is therefore the cut symmetric difference. H invariance makes the length constant on double cosets; the full H shell orbits and stabilizer property justify classifying these by Gaussian rank r=3−dim(Z intersect gZ).

The native square-cross rank calculation is valid without commuting X and Y. With E=X−Y, the upper-right block is −(XE+EY). Adding X times the second block row to the first leaves −EY, then adding the first block column times Y to the second removes it. Both operations are invertible. The difference rank is twice rank(E). This is an algebraic method calculation; the proof properly does not infer a physical free inverse or unproved phase-algebra transfer.

The coarea extension to real radial L1 functions follows from threshold cuts with nonnegative weights. The specified63-point cut independently has values(4,6,7), so its nonnegative mixtures with the Lagrangian cuts satisfy2h2<=3h1 and4h3<=7h1. No claim about every63-point sign function is imported.

The Hilbert three-space argument is correct. Commuting coordinate swaps have a joint orthogonal eigenspace decomposition, giving D2=2D1−8||P_{--}f||². The three actual isotropic spaces have distance tuples(0,1,1,2),(1,2,2,3),(1,2,2,1); their mixed-difference equations force all radial values equal. The argument concerns an attempted endpoint-detection family. Squared displacement is not asserted to be subadditive.

## Additional exact review supplement

`HILBERT-SUPPLEMENT.md` records an independently derived quantitative bound in the same representation. The exact orbit intersection matrices satisfy

    3q1−2q2 = ||v0−3v1+2v2||² +8||v1−3v2+2v3||²,

where q_r is half the total squared displacement. Thus q2<=3q1/2 for arbitrary Hilbert-valued radial orbit values. The constant is sharp at scalar values(7,3,1,0), with q1=96,q2=144. This optional strengthening remains within this representation and does not close the full-ordinary caller obligation. Worker B separately reviewed the supplementary normalization and requested two verbal corrections, both incorporated: nonzero displacement rather than merely nonzero function, and distinct notation s1,s2 for individual swaps.

## Verification and controls

The independent artifacts check all135 spaces, all12 parabolic generators, all eight radial cuts, all63 line intersections, complements, a nonradial singleton that fails the free-H condition, the constant cut, the combined63-point separator, the three Hilbert witness spaces, and the exact positive-square matrix identity. Reproduce:

    python check_author.py --author AUTHOR_PACKAGE

The checker runs only the independent RREF implementation, then compares published certificates and exact pins. The all-field symplectic enumeration is not claimed: this is the fixed finite group Sp(6,2), with subsequent real/complex representation arguments exactly as stated. Different representations, non-diagonal H-intertwiners, marked-factor mechanisms and genuinely entangling physical callers remain open.

Independent review by Worker C; credits and OpenAI assistance retained. No mathematical correction to the reviewed author proposition was required.
