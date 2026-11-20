# Global rigidity and stability at the native minimum return

Let M be a matrix on 111 labelled input and output roles over a field F, with b by b blocks. Its diagonal blocks are I. Off the diagonal only the 6,470 directed native foreign positions may be nonzero. A particular set of 221 of these blocks forms the certified spanning tree of the bipartite graph of native inputs and outputs. Put K=I+O for the native foreign-contact matrix O.

**Exact classification.** If the 221 tree blocks are invertible and rank M≤9b, then in characteristic two there are native G_i in GL_b(F) such that M_ij=K_ij G_i G_j⁻¹ everywhere. Conversely all such fittings have rank 9b. In odd characteristic no fitting satisfies these hypotheses. The other 6,249 foreign blocks are allowed to be singular in the hypothesis. No continuity with the canonical point is required.

**Rank stability.** If rank M≤9b+h with h≥0 and the same 221 tree blocks are invertible, separate native input and output bases put those blocks at I. In those bases 4,668 additional foreign blocks differ from I by rank at most h, 405 by at most 2h and 1,176 by at most 3h. In characteristic two a single change per native role puts every foreign block within rank 14h of I. In odd characteristic h≥b/8.

At b=3,840 and m=870 the allowed h≤128 therefore forces agreement with separate native coordinate transports on at least 3,712, 3,584 and 3,456 dimensions on the corresponding edges. Simultaneous native bases give agreement on at least 2,048 dimensions at each edge. Each agreeing subspace may depend on the edge. The odd-characteristic floor h≥480 also exceeds the limiting allowance of 134. This theorem applies to square linear native fittings on the specified support. The admissible characteristic-two target still requires a physical word.

## Eight pivots force a rectangle

For each certified rectangle {i,j}×{a,b} take the indicated eight mutually nonforeign roles C. None is an exterior row or column. No c in C is foreign to both endpoints of any of the four cells. In the submatrix on rows (C,i,j) and columns (C,a,b), the first eight diagonal blocks are invertible. Eliminating them leaves all four exterior entries unchanged, since every correction through c has a zero factor. The conclusion survives separate invertible changes of row and column basis. Thus each certified exterior rectangle has rank at most b+h.

Use separate input and output changes along the 221-edge tree to put each seed at I. If three entries of a certified rectangle differ from I by ranks e_1,e_2,e_3, replace them by I in the proof at a total rank cost of at most their sum. Permute block rows and columns to put the unknown U in the final corner. The resulting rank is b+rank(U−I). Hence

    rank(U−I) ≤ h+e_1+e_2+e_3.

This step needs no invertibility of the three approximations and is valid for noncommuting blocks.

The witness lists one clique and three preceding edges for each of the 6,249 implications. Give the tree edges cost zero and a new edge cost one plus the sum of its three preceding costs. The certificate reaches all 6,470 proper cells with maximum cost three. It was found by enumerating compatible rectangles of nonforeign eight-cliques and closing a native spanning tree. Verification checks the chosen consequences directly from the root dot products.

Even a singular tree entry of defect δ_e is within rank δ_e of an invertible matrix, by completing its rank normal form. Use these approximations only to choose bases. If the largest tree defect is δ, the same propagation gives error at most c h+(2c+1)δ on an edge of cost c. A ternary proof with c internal vertices has 2c+1 leaves counted with multiplicity. The actual fitting is never modified by these choices.

## Recovering all native diagonals

Write D_i for the transformed diagonal at i. For each i the witness supplies disjoint nine-role sets R,C outside i. The ordinary zero-one core K_RC has odd determinant. Adding row and column i gives even determinant. Over characteristic two the core is invertible and the scalar bordered Schur complement with K_ii=1 is zero.

Replace each foreign entry of the indicated ten-by-ten block submatrix by I, retaining D_i. It is the only self cell. The sum of the edge costs is eight for 46 native roles, nine for 60 and ten for five. Thus the resulting rank is at most 9b+(1+cost)h. Its actual rank is 9b+rank(D_i−I) by the scalar pivot tensored with I_b. Consequently rank(D_i−I)≤11h at every role.

If the separate changes act by L_i and R_j on the two sides then D_i=L_iR_i. A further right change D_j⁻¹ restores the native diagonal and yields L_i M_ij L_j⁻¹. Its error has rank at most 3h+11h. At h=0 this proves the simultaneous equivalence to K⊗I_b. The canonical rank is 9b by the verified binary factorization.

## An odd-characteristic obstruction

The last witness gives ten rows disjoint from ten columns. The zero-one submatrix of O has integer determinant exactly 2. All occupied entries together have cost seven. In any odd characteristic the corresponding canonical block matrix has rank 10b. The normalized fitting differs on this submatrix by rank at most 7h. Therefore 10b≤9b+h+7h, or h≥b/8. The result applies to the stated invertible tree and permits arbitrary values in the other foreign blocks.

## Verification

    python -B PATH/check.py --repo REPO --out FRESH

The [witness](output/WITNESS.json.gz) contains every tree edge and exact rectangle, the 111 disjoint diagonal recoveries and the odd-characteristic minor. The [receipt](output/RESULT.json) retains the computed costs and four rejected mutations. This conclusion strengthens the earlier formal rigidity theorem to a global one under the stated native invertibility test. The five framework obligations and both strict suppliers remain open. No new complete κ. Credit @CubeJerry and the native geometry and canonical and covariant fitting predecessors. Substantial OpenAI assistance.
