# Rigidity of the flat native fitting at the minimum return

Let O be the 111-role proper foreign-contact matrix of the original native chart system, over a field F of characteristic two. Put K=I+O. A b-dimensional fitting M has diagonal blocks I_b, zero blocks at all off-diagonal nonforeign positions, and arbitrary b-square blocks at its 6,470 ordered foreign positions. The canonical fitting is K⊗I_b. This package gives an obstruction for **all body sizes** and an exact cost for a useful family of non-flat perturbations. It supplies a global constraint on the ongoing search for a physical word.

**Rank-nine formal rigidity.** Let A be a commutative, separated, complete local F-algebra with maximal ideal m and residue field of characteristic two. Finite nilpotent local algebras are included. Suppose a fitting M over A reduces to K⊗I_b and every (9b+1)-minor vanishes. There are native basis changes G_i in GL_b(A), each reducing to the identity, such that

    M_ij = K_ij G_i G_j⁻¹  for every i,j.

Thus exact minimum rank permits only changes of native coordinates in the formal neighborhood of the canonical point. The theorem uses all native zero positions and all prescribed identity diagonals. It allows arbitrary matrix entries within foreign cells. Large deformations in other components and positive return excess are separate questions.

**Sharp square-zero price.** For any b-square matrix N with N²=0 and any 111-square F-matrix X supported on the directed proper positions, the admissible fitting M=K⊗I_b+X⊗N has

    rank M = 9b + rank(N) · rank(ker K → coker K, v ↦ Xv mod im K).

Every foreign block is invertible. The last factor is zero exactly when X_ij=(g_i+g_j)K_ij for some 111 scalars g_i. Otherwise its least possible value is one, attained by a single directed native edge. Consequently any non-gauge deformation of this scalar-copy form at bank 3,840, with the m=870 budget, must have rank N at most 128. The assertion concerns the 9b+128 return budget and does not bound how many different perturbations can cancel in a more general joint fitting.

## Native pivots and a scalar certificate

The geometry source gives K_ij=1 at the diagonal and at the orthogonal pairs of the 111 pinned roots. Fix the eight mutually nonforeign roles C=(1,29,28,37,36,65,63,73). For each role take the eight bits y_i=K_iC and append the bit 1+sum y_i. This gives a row T_i of length nine. On all 12,321 cells the checker verifies K=TTᵀ and rank(T)=9. In particular there is a fixed nine-role set J with T_J invertible, so K_JJ is invertible. This principal pivot works at all body sizes, even over a local algebra.

There is also substantial choice for a pivot which uses an actual foreign degree of freedom. Enumerate all maximal cliques in the nonforeign graph. There are 881 of size three, 80 of size six, 22,646 of size seven and 4,373 of size eight. For a size-eight clique C, take any foreign pair (i,j) outside it such that no c in C is foreign to both i and j. The block minor with rows (C,i) and columns (C,j) has Schur complement exactly M_ij, because each product through a clique role vanishes. The minor is invertible whenever M_ij is. All 6,470 foreign pairs admit such a pivot, with 140 to 437 cliques per ordered pair and 1,741,394 total choices. This also proves the lower bound 9b for any fitting with **at least one** invertible foreign block. Both sets of indices in the minor and the declared support are essential.

## The tangent calculation

At K the tangent to rank at most nine consists of U Tᵀ+T Vᵀ. One can see this without an algebraic-geometry assumption. Use the invertible nine-role pivot and the exact factor identity M=M_:J (M_JJ)⁻¹ M_J: when the higher minors vanish. Taking a first-order coefficient gives the stated form. Conversely every such expression comes from a product of two first-order factors. A zero variation is exactly a change of the internal basis, U=T A and V=T Aᵀ, since T has full column rank. This kernel has dimension 81.

For all 5,740 off-diagonal nonforeign cells and 111 prescribed diagonals impose

    u_i · T_j + T_i · v_j = 0.

The 5,851 binary equations on 1,998 factor variables have exact rank 1,807. This gives a 191-dimensional factor space. Subtracting its 81-dimensional kernel leaves 110 dimensions of genuine tangent. The [finite certificate](output/RESULT.json) identifies 1,807 independent equations by native cell, retains T, and verifies every remaining row by exact elimination. Binary rank remains the same over every characteristic-two field. The native foreign graph is connected. Therefore the tangent variations X_ij=(g_i+g_j)K_ij already span 110 dimensions. They exhaust all possible variations with this support. Releasing a single prescribed diagonal lowers the equation rank by one and enlarges the tangent. This checks a substantive hypothesis.

For b-dimensional blocks, differentiate the same rank-9b factorization at (T⊗I_b)(Tᵀ⊗I_b). For each ordered pair of internal row and column coordinates the linear constraints are the scalar system above. There are no linear equations mixing distinct pairs. Hence every permissible tangent is K_ij(G_i+G_j) for b-square matrices G_i; one common matrix can be subtracted from all of them. The same proof works with coefficients in any vector space over the residue field by tensoring a finite linear system.

## Lifting and the scope over fields

Suppose the fitting has been brought to canonical form modulo m^s. Over A/m^(s+1), its next correction takes values in the square-zero residue vector space m^s/m^(s+1). The fixed minor is a unit. The vanishing minors imply the exact pivot factorization over this quotient (expand each bordered minor). Its first-order correction lies in the computed block tangent, so equals K_ij(G_i+G_j). Independent native changes I+G_i kill that term while keeping the identity diagonals. Start at s=1 and continue. The products converge m-adically, with invertible limits reducing to I. Completeness and separatedness yield the claimed equality over A. Nilpotence terminates this proof in finitely many steps.

Over an algebraically closed field the gauge orbit of K⊗I_b is even an isolated connected component inside the space of rank-at-most-9b fittings with all foreign blocks invertible. Fix an oriented spanning tree on the connected native graph and normalize all its forward blocks to I. Fix the root change to I. Solving along the tree gives a unique normalization, regular on the open set of invertible blocks, with regular inverse. The space is the product of 110 copies of GL_b and the tree-normalized slice. At the canonical point the slice has zero tangent because any tangent gauge vanishing on tree edges is constant. Its finite-type local ring has m/m²=0 and hence m=0 by Nakayama's lemma. The canonical rational point is isolated and closed on the slice: on a finite set of affine generators one can localize away from their annihilators at the point to isolate it. Since GL_b is connected the orbit is a connected component. Nothing in this argument enumerates other components or excludes isolated noncanonical flat fittings.

## Exact excess for square-zero directions

Write N in rank-s square-zero Jordan form. There are s mutually independent two-coordinate Jordan pairs and b−2s zero directions. Each pair contributes a matrix with diagonal copies of K and off-diagonal X. Project its image onto the second output. This projection has dimension rank K. On its kernel the first output runs over im K + X(ker K). The rank of the pair is therefore 18 plus the rank of the indicated map to coker K. Zero directions contribute nine each, giving the formula.

That induced map vanishes precisely when X lies in the full rank-nine tangent: in bases reducing K to diag(I₉,0), vanishing says exactly that the lower-right block of X is zero. The same space was characterized above on the native support. For a single allowed directed edge the induced rank is at most one; a single directed edge cannot be a vertex potential, since those are symmetric. Its induced rank is therefore one. The binary check constructs the entire two-bank matrix of this example and obtains rank 19. For a gauge variation and a general N, native changes I+g_i N have the stated effect exactly because N²=0.

A separate proof run can regenerate the scalar certificate.

    python -B PATH/check.py --repo REPO --out FRESH

This theorem restricts the algebraic target before the physical source problem is solved. Neither the localized coefficient result nor the native clique pivots supply an implementable word. No new complete κ. Credit @CubeJerry, the native geometry and rank-nine canonical predecessors. This proof and its computation used substantial OpenAI assistance.
