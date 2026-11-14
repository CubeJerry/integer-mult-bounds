# Two augmented stars force a44/5 fractional rank floor on the native wings

**Proved source-bound matrix-compatibility theorem. No new kappa.**

Every block fitting M on the actual76-wing graph, over every field and at every positive width V, satisfies
\[
 \operatorname{rank}M\ge\frac{44}{5}V.
\]
The canonical characteristic-two fitting gives rank9V. Thus the fractional Haemers interval is [44/5,9] in characteristic two, and widths1,2,3,4 all have minimum exactly9V. The first remaining width is5, where rank44 has not been constructed or excluded.

The new ingredient is a rank inequality coupling two edge roles through their shared endpoint. It uses their actual matrix-zero equations, beyond the earlier augmented-LR relaxation. No packet lifetime, movement, or supplier bound is inferred.

## 1. Sources and the new29-role seed

Native BIT gzip provenance: SHA-256 51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78. The exact normalized root recovery is Git blob8eba43d142c819c206dce5df87ea4571aaead287, from the admitted84-flat certificate SHA-2564ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc. This is a derived-source check during the executor outage, not a new gzip replay.

Dependencies:
- results/bit-wing-fractional-gap/author/PROOF.md, blob7902a81b50b33d744fc0de7a0c699803b1e1e709: augmented LR and its rank-kernel proof.
- results/bit-wing-no-eight-modes/author/PROOF.md, blob01f0c19a354b7aab7c7234664291a3072b0c11d7: earlier wing seed and geometry convention.
- results/bit-saturated-star-rigidity/author/PROOF.md, blobf9f0b56e2a06231fba611ab248819ab2543a480b: original normalized-star notation and ordered factor conventions.
- DreamingOfClouds, CrocSwap/integer-mult-bounds#7114: inherited LR inequality.

Prepared for @CubeJerry with predecessor credit and OpenAI assistance. The fractional-Haemers definition is the standard block-matrix infimum, as in Bukh and Cox, Section2 of https://arxiv.org/html/1802.00476v2.

The76-wing set consists of native roles distinct from92,15,106 and real-orthogonal to exactly one of those carrier roots. Contacts are distinct real-orthogonal pairs. Fittings have identity own blocks and zero blocks at noncontacts.

Use the seven-point frame
\[
 F=(0,14,39,41,60,63,70).
\]
It is an independent set in the contact graph. The twenty roles with exactly two frame contacts form all edges of K7 except(0,3), with degree pattern
\[
 (5,6,6,5,6,6,6).
\]
Edge roles sharing a frame endpoint are noncontacts. The exact edge-role list is reconstructed in the receipt.

There are two singleton augmentations: role85 contacts only frame point0 and is a noncontact of every incident edge; role107 has the same property at frame point3. Define
\[
 A=\{0,3\},\qquad B=\{1,2,4,5,6\}.
\]
The seed has7+20+2=29roles. The loops85,107 are also an actual noncontact pair. That last zero is verified but is not used in the44/5 inequality.

## 2. Normalized factors and the intermediate17/2 bound

Factor M through rank M=7V+j coordinates and normalize the identity point frame. Every edge e={a,b} has row/column factors only at a,b,last, with last dimension j. Put
\[
 \alpha_e(a)=C_{ea}R_{ea},\quad S_e=C_{e*}R_{e*},\quad
 \gamma_e(a)=\alpha_e(a)+S_e,\quad
 g_e(a)=\operatorname{rank}\gamma_e(a),\quad
 G_a=\sum_{e\ni a}g_e(a).
\]
The identity diagonal implies alpha_e(a)=I-gamma_e(b).

Let A_e=[C_ea,C_e*], B_e=[R_ea;R_e*], and lambda_e(a),mu_e(a) be their ranks. Stack all incident edge factors at a, and include its singleton when a lies in A. The product has rank G_a+m_aV, where m_a=1 on A and0 elsewhere. The same kernel/Sylvester proof as in the predecessor gives
\[
 \lambda_e(a)+\mu_e(a)
 \le V+j-G_a-m_aV+2g_e(a).                         \tag{1}
\]
Using lambda_e(a),mu_e(a) >= V-g_e(b) gives
\[
 G_a+(1+m_a)V\le j+2(g_e(a)+g_e(b)).                \tag{LR+}
\]
Set h=j-V, so rank M=8V+h.

Weight LR+ by2 at A-to-B incidences, by1 at B-to-B incidences, and by0 at B-to-A incidences. Each A point has outgoing weight10; each B point has outgoing weight4. The total weight is40 and the weighted singleton contribution is20V. After collecting gamma ranks, only6(G_0+G_3) remains:
\[
 40h\ge20V+6(G_0+G_3).                             \tag{2}
\]
This alone gives h>=V/2, or rank>=17V/2. It is an intermediate bound, strengthened below.

## 3. A new cross-edge compatibility inequality

Let a be an augmented point, e={a,b}, and f={b,c}, with c distinct from a. The two edge roles share b and are actual noncontacts. Their two matrix-zero equations are
\[
 C_{eb}R_{fb}+C_{e*}R_{f*}=0,\qquad
 C_{fb}R_{eb}+C_{f*}R_{e*}=0.                       \tag{3}
\]
Since C_eb R_eb=I-gamma_e(a), both square matrices C_eb and R_eb have nullity at most g_e(a). The first equation gives
\[
 \operatorname{rank}R_{fb}
 \le \operatorname{rank}C_{e*}+g_e(a)
 \le\lambda_e(a)+g_e(a),
\]
and the second gives
\[
 \operatorname{rank}C_{fb}
 \le \operatorname{rank}R_{e*}+g_e(a)
 \le\mu_e(a)+g_e(a).
\]
Meanwhile both ranks on the left are at least
rank alpha_f(b) >= V-g_f(c). Apply (1) at the augmented point a, where m_a=1. It follows that
\[
 2(V-g_f(c))
 \le j-G_a+4g_e(a).
\]
Equivalently,
\[
 2g_f(c)+4g_e(a)\ge V-h+G_a.                      \tag{CE}
\]
This is valid over every field, without symmetry, commutativity, invertibility of the endpoint factors, or an equality assumption. The nullity terms explicitly retain the possible singularity.

## 4. Summing the two augmented stars

Take a=0,c=3 and let b range over their five common neighbors B. Summing CE gives
\[
 2G_3+4G_0\ge5(V-h)+5G_0,
 \quad\text{hence}\quad
 2G_3-G_0\ge5(V-h).
\]
Reverse the two endpoints to obtain
\[
 2G_0-G_3\ge5(V-h).
\]
Adding yields
\[
 G_0+G_3\ge10(V-h).                                \tag{4}
\]
Combining (2),(4),
\[
 40h\ge20V+60(V-h),\qquad100h\ge80V.
\]
Thus h>=4V/5 and rank M>=44V/5. The bound remains valid if h>=V, when the intermediate right side in(4) is nonpositive.

In characteristic two the source's canonical binary fitting has rank9, independently checked on all76 roles. Tensoring with I_V supplies the9V upper bound over every characteristic-two extension field. For V=1,2,3,4, taking integer ceilings of44V/5 gives9V, proving exact equality at those widths.

## 5. What a surviving fractional code must change

The following consequence is a representation restriction, not an extra numerical lower bound.

Suppose all blocks of a fitting preserve a common flag in the V-dimensional block space, with successive quotient dimensions at most4. After the same basis change in every vertex block, the complete fitting is block upper triangular by those flag layers. Each diagonal layer is a fitting of the same graph at its quotient width, so has rank at least9 times that width. The rank of a block upper triangular matrix is at least the sum of its diagonal ranks. Therefore the complete fitting has rank at least9V.

In particular, commuting blocks cannot yield a fractional improvement. Over an algebraic closure they are simultaneously triangularizable, so the quotient layers all have dimension1; scalar extension preserves rank. This statement holds over every field, with the same all-field scalar lower bound.

Any code beating9V must therefore contain an irreducible common-invariant quotient of dimension at least5 after scalar extension. Merely changing to a larger scalar field, or composing small simultaneously triangular block modules, cannot provide it. This identifies a concrete representation requirement; it does not construct the needed module.

## 6. Exact boundary of the retained rank relaxation

Set V=5,h=4,j=9. Assign
\[
 g_{A\to B}=1,\quad g_{B\to A}=2,\quad g_{B\to B}=1.
\]
Then G_A=5 and G_B=8. Every augmented LR inequality is satisfied. Every CE inequality starting at an A point, including both A-to-B-to-A and A-to-B-to-B paths, is equality. The weighted sum(2) and bound(4) are also equalities.

The checker verifies all40 LR incidences and all50 CE paths. This is an exact integral feasible point of the stated rank relaxation, with ratio44/5. It is **not an actual fitting**. Realizing all these numbers by compatible kernels, images and matrix products is open. The loop-loop zero and all further matrix compatibility remain available to strengthen the theorem.

Thus no better asymptotic bound follows solely by reweighting these LR+ and CE inequalities with nonnegative rank variables. A stronger proof needs another matrix relation; a positive result needs an actual high-width code.

## 7. Verification and programme boundary

Run
\[
 \texttt{node check.mjs /absolute/path/to/RECOVERED-NATIVE-ROOTS.json > RESULT.reproduced.json}.
\]
The CLI pins Git blob8eba43d142c819c206dce5df87ea4571aaead287. Expected status: PASS_TWO_AUGMENTED_STARS_WING_GAP.

The exported checker was actually executed using the pure-JavaScript tool. It reconstructs the76 wings, new frame, all20 edges, both singleton masks, weighted coefficients, ten paths needed for(4), the full formal50-path CE control, and the canonical binary rank. Local Node CLI execution is not claimed during the executor outage.

The theorem is the written universal rank proof, not an extrapolation from the source check or the formal rank-variable point. Independent review must be recorded separately by the integrator.

**No new kappa.** Rank history, physical field lifetimes, source acquisition, reversible restoration, ownership, precision, uniform coefficients, the complete BIT/complex supplier interface, recursion and foundational assumptions remain separate obligations.
