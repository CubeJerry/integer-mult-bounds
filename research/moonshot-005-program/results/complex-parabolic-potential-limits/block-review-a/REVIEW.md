# Independent review of full-parabolic radial block commutator ranks

**Verdict: accepted within the stated representation interface. No correction requested. No new κ.** Worker A independently reviewed the universal argument, rebuilt the finite geometry without importing author code, and checked Worker C's scalar diagonal corollary as a subcase.

## Exact scope and pins

The principal proof is root's `full-parabolic-block-potential/PROOF.md`, SHA256 `d17f439fec8a24f75ba6402f8bc32a7a213ee11dcc30afb5408b14f31b120959`. The scalar corollary is Worker C's `DIAGONAL-RANK-COROLLARY.md`, SHA256 `7829b804ddee4d5d85028770d21bfc48963c4111e51e13df8ce37aebcb88beec`. Its independently enumerated intersection table has SHA256 `b61e133e1de39a4c6731097c4b5a6126c486473e886d2023abcf08273f36727d`. `MANIFEST.json` pins the reviewed source and this independent package.

The theorem allows every coefficient field F, every finite block size k≥1, and arbitrary square matrices A0,...,A3 over F. The group acts as its permutation on the135 Lagrangian positions tensored with the identity on the k-dimensional auxiliary fiber. D is block diagonal in those positions and constant on each H shell. It does **not** cover an arbitrary off-diagonal H-intertwiner, a nontrivial group action on that auxiliary fiber, another representation, or every physical caller. The physical phase-aware representation transfer remains a separate obligation.

## Universal argument independently checked

For any matrices A,B,C of the same size, rank(A−C)≤rank(A−B)+rank(B−C), over every field. Thus δij=rank(Ai−Aj) is a pseudometric; commutativity, invertibility and spectral assumptions on Ai are unnecessary. The conjugated block-diagonal matrix has, at position L, the block from g⁻¹L. Consequently its rank difference is the sum of the ranks of those individual block differences, without cancellation between distinct positions.

The independently rebuilt orbit-intersection matrices are symmetric for the involutions w_r. After dividing this direct-sum rank by two, their upper-triangular coefficients give

    q1 = δ01 + 12δ12 + 32δ23,
    q2 = δ02 + 3δ12 + 8δ13 + 24δ23,
    q3 = δ03 + 7δ12 + 7δ13 + 28δ23.

The two displayed triangle decompositions in the reviewed proof are exact coefficient identities. In particular the distance-three term δ01+δ12+δ23−δ03 is nonnegative by two applications of the triangle inequality. Therefore q2≤q1 and4q3≤5q1 hold for every allowed field and block size. Since the positive coefficients of q1 connect all four shell labels, q1=0 forces all four matrices equal, and then every group commutator vanishes. The choice A0=A1=0, A2=A3=I gives(12k,12k,15k), proving simultaneous sharpness.

Double-coset invariance follows from D commuting with H and rank invariance under multiplication by the invertible permutation operators. The four double cosets follow from H transitivity on the four possible images of Z, classified by the intersection dimension. Nothing in this step uses characteristic zero for the coefficient field; the finite symplectic indexing geometry remains over F2.

For the63 nonzero symplectic vectors, I independently recovered precisely the two H orbits of sizes7 and56. The number leaving Z under w_r is8−2^(3−r). Hence arbitrary two-block operators give q_r=(8−2^(3−r))rank(B0−B1), including over characteristic two. Nonnegative combinations with the135-position family satisfy2q2≤3q1 and4q3≤7q1. A nonzero combination has q1>0, so the intended linear rank-two calibration fails.

The legitimate commutator-length interpretation is also correct. Rank([D,UV])≤rank([D,U])+rank([D,V]) for invertible U,V. With E=[D,X], the square-cross native commutator is M=[[E,−EX−XE],[0,E]]. Multiplication on both sides by the invertible block shear [[I,X],[0,I]] reduces M to diag(E,E). This calculation works in every characteristic and does not even require X to be invertible for the reduction; actual native inverses separately use the usual invertible-commutator identity. Ordinary group-algebra coefficients act trivially on the auxiliary fiber, so their role matrices commute with the repeated D. This statement supplies no free physical inverse, phase quotient or caller.

## Scalar diagonal corollary

Worker C's level-set proof is valid over every value field. For scalar diagonal D, a position with unequal old/new values belongs to exactly two level-set symmetric differences, while a position with equal values belongs to none. Thus rank(D−PDP⁻¹)=Σ_a |S_a Δ gS_a|/2. Each S_a is H-invariant. This is a nonnegative sum of the proved combinatorial cut potentials; it does not require ±1 to remain distinct in characteristic two. I independently reconstructed all15 equality patterns of four values and obtained the exact same rank vectors as `DIAGONAL-RESULT.json`.

## Independent computations and negative controls

`check.py` uses a new incremental isotropic-closure enumeration: extend each isotropic subspace by every perpendicular new vector. It finds1,63,315,135 subspaces in dimensions0,1,2,3. Exhaustiveness follows because every nonzero isotropic subspace admits such a codimension-one chain. Fresh symplectic generators fixing Z recover the shell sizes1,14,56,64 and all four intersection matrices, agreeing with the independently pinned table. The same generators recover the63-point orbit sizes and half-crossings(0,4,6,7).

The checker verifies both coefficient identities before imposing numerical distances. It then checks all65,536 ordered quadruples of2×2 matrices over F2 and512 deterministic quadruples of3×3 matrices over F3. These are finite controls only; the all-field/all-size theorem follows from the preceding direct-sum and triangle argument. All15 scalar equality patterns are compared to C's frozen receipt, with the level-set identity separately reconstructed from actual sets of Lagrangians.

Controls retain constant blocks, demonstrate that the nonmetric assignment δ02=1 with every other distance zero reverses q2≤q1, and exhibit a nonradial singleton moved by the stabilizer. Thus the pseudometric and H-radial hypotheses are substantive. Squared Hilbert distances cannot be substituted into this metric proof; the reviewed principal proof correctly retains that qualification.

For committed sibling packages `block-root` and `independent-c`, reproduce with:

    python check.py --source /path/to/block-root --out /path/to/output

For any other layout, explicitly supply `--diagonal /path/to/review-lagrangian-potential`. The synonym `--author` is accepted for `--source`. Expected status: `INDEPENDENT_BLOCK_RADIAL_REVIEW_PASS`.

## Attribution and programme consequence

Credit @CubeJerry, root's block-rank extension, Worker B's original Lagrangian cut enumeration and source interpretation, Worker C's independent orbit table and scalar/Hilbert extensions, and all retained source/phase predecessors. This review and independent checker were produced by Worker A with OpenAI assistance.

The result closes a substantially larger invariant family than scalar sign cuts. It is a scoped proof-method obstruction, not a proof of conservation for all entangling ordinary callers, a new profitable caller, a uniform supplier, a foundational discharge or a multiplication exponent improvement.
