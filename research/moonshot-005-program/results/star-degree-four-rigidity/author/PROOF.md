# Minimum degree four suffices for saturated block-star rigidity

**Complete proposed proof for independent review. No new kappa.**

This sharpens the minimum-degree-five sufficient condition in research/moonshot-005-program/results/bit-saturated-star-rigidity/author/PROOF.md (Git blob f9f0b56e2a06231fba611ab248819ab2543a480b) to minimum degree four. The predecessor's degree-three example remains a counterexample, so four is the sharp uniform minimum-degree threshold. All fields and all positive block widths are allowed.

Credit DreamingOfClouds, CrocSwap/integer-mult-bounds#7114, for the LR inequality and rank floor, and S011 for ordered factor gauges. The new step is the degree-four equality analysis using a shared kernel and its last-coordinate projection. Prepared for @CubeJerry with OpenAI assistance.

## 1. Statement and notation

Let Gamma be a finite simple graph on n points, every degree at least four. Its star configuration has those point roles and one edge role for each edge. Distinct points are noncontacts. An edge contacts precisely its two endpoints among the points; edge roles sharing an endpoint are noncontacts. Disjoint edge pairs may be contacts. A V-block fitting M over any field k has identity diagonal blocks and zero at these prescribed noncontacts.

**Theorem.** If rank M=(n+1)V, then M is a vertex gauge of the canonical signed star fitting. Every intrinsic edge Schur block equals -I_V in a normalized point-frame factorization. Canonical edge rows have I at a,b,last; columns have I at a,b and -I at last. Point factors are coordinate projections and inclusions.

No symmetry or commutativity is assumed. Disconnected Gamma is permitted.

Normalize M=CR at the identity point frame. The first n coordinate blocks have size V and the last block has size V. An edge e={a,b} has factors only at a,b,last. Put
\[
 \alpha_e(a)=C_{ea}R_{ea},\quad S_e=C_{e*}R_{e*},\quad
 \gamma_e(a)=\alpha_e(a)+S_e,\quad
 g_e(a)=\operatorname{rank}\gamma_e(a),\quad
 G_a=\sum_{e\ni a}g_e(a).
\]
The edge diagonal gives
\[
 \alpha_e(a)+\alpha_e(b)+S_e=I,\qquad
 \alpha_e(a)=I-\gamma_e(b).                           \tag{1}
\]

At a point a, let A_e=[C_ea,C_e*] and B_e=[R_ea;R_e*] in the a,last coordinates. Stack the A_e vertically and B_e horizontally to obtain A,B. Their product has diagonal blocks gamma_e(a) and all off-diagonal blocks zero. Set ell=rank A, rho=rank B, lambda_e=rank A_e, mu_e=rank B_e. The inherited kernel and Sylvester inequalities are
\[
 \lambda_e-g_e(a)\le\ell-G_a,\quad
 \mu_e-g_e(a)\le\rho-G_a,\quad
 \ell+\rho\le2V+G_a.                                 \tag{2}
\]
For example, the kernel of multiplication by B on row A has dimension ell-G_a. The kernel on row A_e has dimension lambda_e-g_e(a), since A_e annihilates every other B_f, and lies in that full kernel. Transpose for the second inequality.

Also lambda_e,mu_e >= rank alpha_e(a) >= V-g_e(b). Thus
\[
 G_a\le2(g_e(a)+g_e(b))                               \tag{LR}
\]
at every directed incidence.

## 2. Equality propagates through each component

The sum of the nonnegative LR slacks is
\[
 4\sum_aG_a-\sum_a\deg(a)G_a
 =-\sum_a(\deg(a)-4)G_a\le0.
\]
Therefore every LR is equality, and G_a=0 wherever degree(a)>4. For every edge,
\[
 G_a=G_b=2(g_e(a)+g_e(b)).
\]
G is constant on each connected component. A component containing degree>4 has G=0 everywhere.

It remains to treat a four-regular component. Write its common G=2t, where t=g_e(a)+g_e(b) is a nonnegative integer. We will prove t=0.

## 3. Individual equality forces complementary projectors

Fix e={a,b} in the four-regular component. From (2),
\[
 \lambda_e+\mu_e-2g_e(a)\le2V-G_a=2V-2t.
\]
Because lambda_e,mu_e >= V-g_e(b) and t=g_e(a)+g_e(b), equality holds throughout:
\[
 \lambda_e=\mu_e
 =\operatorname{rank}C_{ea}
 =\operatorname{rank}R_{ea}
 =\operatorname{rank}\alpha_e(a)
 =V-g_e(b).                                         \tag{3}
\]
The analogous statement holds with a,b exchanged.

For any square X, rank X + rank(I-X)=V implies X squared=X: the two images have direct sum equal to the full space, while X(I-X)=(I-X)X has image in their intersection. Apply this to each gamma, using (1),(3). Thus gamma_e(a) and gamma_e(b) are idempotents.

The rank equality rank[C_ea,C_e*]=rank C_ea implies image C_e* is contained in image C_ea. The latter equals image alpha_e(a), since these matrices have equal rank and alpha_e(a)=C_ea R_ea. As alpha_e(a)=I-gamma_e(b), this image is the kernel of gamma_e(b). The column-factor version gives the corresponding row-space containment. Both endpoints yield
\[
 \gamma_e(a)C_{e*}=\gamma_e(b)C_{e*}=0,\qquad
 R_{e*}\gamma_e(a)=R_{e*}\gamma_e(b)=0.               \tag{4}
\]
Therefore gamma_e(a)S_e=S_e gamma_e(a)=0. Substituting
S_e=gamma_e(a)+gamma_e(b)-I and using idempotence gives
\[
 \gamma_e(a)\gamma_e(b)=\gamma_e(b)\gamma_e(a)=0.
\]
Their sum is an idempotent of rank t. Hence
\[
 P_e=I-\gamma_e(a)-\gamma_e(b)
\]
is an idempotent of rank V-t and S_e=-P_e. Equation (4) confines the image of C_e* and the row space of R_e* to the corresponding P_e spaces. Their product already has rank V-t, so
\[
 \operatorname{rank}C_{e*}
 =\operatorname{rank}R_{e*}
 =\operatorname{rank}S_e=V-t.                       \tag{5}
\]
No noncommuting factors have been exchanged.

## 4. A shared kernel forces a common residual row space

At a star a, (2),(3) imply ell,rho >= V+t. Since ell+rho <= 2V+2t, both equal V+t. Define
\[
 K_a=\{z\in\operatorname{row}A:zB=0\}.
\]
Its dimension is ell-G_a=V-t. The analogous product kernel within row A_e has dimension
\[
 \lambda_e-g_e(a)=V-g_e(b)-g_e(a)=V-t.
\]
It is contained in K_a, so it equals K_a for every edge incident to a.

Project K_a onto its last V coordinates. For any row vector x, replace x by x(I-gamma_e(a)). Its product with A_e lies in K_a, because
\[
 x(I-\gamma_e(a))A_eB_e
 =x(I-\gamma_e(a))\gamma_e(a)=0
\]
and A_e annihilates every other B_f. Its last part equals xC_e*, by (4). Thus the projection contains row C_e*. Conversely K_a lies in row A_e, so the projection is contained in row C_e*. Therefore
\[
 \pi_*(K_a)=\operatorname{row}C_{e*}.                \tag{6}
\]
Both sides have dimension V-t, so this projection is an isomorphism.

Consequently all edge last-row spaces agree at a point. The same C_e* occurs at both endpoints of an edge, so connectivity gives one common last-row space L of dimension V-t across the component. The transposed argument gives one common last-column space. Their pairing is nondegenerate because C_e*R_e* has rank V-t.

Only the common row space is needed for the rank contradiction. All point rows have last component zero, and all edge rows in the component have last component in L. The principal fitting on this component, with n_c points, therefore has rank at most
\[
 n_cV+(V-t).                                       \tag{7}
\]
Its other point-coordinate blocks vanish by the point/edge mask.

The ordinary degree-four star rank floor is (n_c+1)V. Indeed, normalize a rank factorization of that component with residual dimension j_c and sum the general LR inequality
G_a+V <= j_c+2(g_e(a)+g_e(b)).
At degree four the G terms cancel, giving j_c>=V. Comparing with (7) forces t=0.

Thus every component has G_a=0, including the purely four-regular ones. For each edge both gamma blocks vanish, and the diagonal identity gives S_e=-I_V.

## 5. Ordered gauges and sharpness of the degree threshold

Write the now invertible last blocks as u_e,v_e, with u_e v_e=-I. Apply the edge vertex gauge C_e -> u_e^{-1}C_e, R_e -> R_e u_e. Its last blocks become I,-I. For edges e,f sharing a, their prescribed zero is
\[
 A_{ea}D_{fa}-I=0.
\]
Each endpoint block is invertible. A third incident edge exists at every point, and ordered right cancellation shows all A_ea coincide with one A_a, and D_ea=A_a^{-1}. The common factor-basis change diag(A_1^{-1},...,A_n^{-1},I), followed by compensating point vertex gauges, gives the canonical signed factors. This is the predecessor's ordered argument; minimum degree four exceeds its required degree three. The theorem follows.

The inherited degree-three counterexample is exact. Let Gamma=K4, with point coordinates 0,1,2,3 and last coordinate *. Keep point factors canonical and set both row and column factors of its edges to these coordinate units:
\[
 01\mapsto1,\quad02\mapsto0,\quad03\mapsto*,\quad
 12\mapsto*,\quad13\mapsto3,\quad23\mapsto2.
\]
Adjacent edges use different units; every edge unit lies within its two endpoints or last. Thus it is a fitting of rank five over every field. Four edge Schur blocks vanish, while only 03 and12 have Schur block one. This violates the saturated conclusion at minimum degree three.

Tensoring the example with I_V gives the same counterexample at every positive width. Therefore degree four is the sharp uniform minimum-degree sufficient threshold; this does not classify every graph with a lower-degree vertex.

## 6. Scope and verification status

The proof is abstract linear algebra. It requires neither native source geometry nor a finite-field search. The exact control checker verifies the inherited degree-three fitting, the sharp change in the LR summation coefficients, and exhaustive small-matrix checks of the idempotent rank lemma. Those finite checks are controls, not substitutes for the all-field/all-width proof.

This extends a structural equality theorem. It gives no source price, physical transport schedule, recursive supplier, or new multiplication exponent. The separate rank-excess problem j>V is still open: the equalities used above no longer hold there, so no quantitative near-equality conclusion has been asserted.

The independent review and any admission decision belong to the integrator. Prepared for the persistent programme without changing earlier evidence or silently upgrading its published theorem.
