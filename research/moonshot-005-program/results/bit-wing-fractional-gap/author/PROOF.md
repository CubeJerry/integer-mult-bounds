# A weighted augmented-star gap for every block fitting on the 76 native wings

**Proved from exact source incidence and general rank inequalities. No new kappa.**

For the actual 76-wing graph and every field k, every V-block fitting M satisfies
\[
 \operatorname{rank}_k M\ge \frac{161}{19}V.
\]
For V=2 the stronger integral bound is rank M >= 18. In characteristic two the canonical fitting supplies rank 9V, so
\[
 \frac{161}{19}\le\mathcal H_f(G_W;k)\le9,
\]
and widths one and two both have minimum exactly 9V. The lower bound uses 28 actual roles. It is not a statement about moving-packet lifetimes.

## 1. Provenance and graph convention

The source BIT gzip SHA-256 is 51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78. We use the independently reconstructed 111-root geometry in Git blob 8eba43d142c819c206dce5df87ea4571aaead287, derived from the admitted 84-flat certificate SHA-256 4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc. This is authenticated derived-source verification, not a fresh native-gzip execution during the local executor outage.

The preceding wing seed and strict obstruction are in research/moonshot-005-program/results/bit-wing-no-eight-modes/author/: PROOF.md blob 01f0c19a354b7aab7c7234664291a3072b0c11d7, RESULT.json blob b981225c500cb654701be80c296e5af019673ac5. The inherited general star proof is results/bit-saturated-star-rigidity/author/PROOF.md, blob f9f0b56e2a06231fba611ab248819ab2543a480b.

Credit DreamingOfClouds and CrocSwap/integer-mult-bounds#7114 for the original LR star inequality; the programme's S011 equality proof; the S013 construction worker for the new wing seed and singleton augmentation; and the adversarial worker for the weighted gap, width-two argument, and relaxation boundary. Prepared for @CubeJerry with substantial OpenAI assistance.

The graph G_W has the 76 native wing roles relative to A2 carrier axes {92,15,106}. Two distinct roles are adjacent exactly when their real roots are orthogonal. A fitting has V by V identity diagonal and zero blocks at nonadjacent pairs. It may be nonsymmetric and its blocks need not commute.

The fractional Haemers notation is the ordinary infimum of rank(M)/V over all positive widths and such fittings. The matrix and subspace formulations appear in Boris Bukh and Christopher Cox, *On a fractional version of Haemers' bound*, Section 2.1, https://arxiv.org/html/1802.00476v2. We use their definition, not an unproved inference from scalar minrank to fractional minrank.

## 2. The 28-role source certificate

The seven frame roles are
\[
 F=(0,14,30,31,60,69,70).
\]
They are pairwise nonadjacent, so their principal fitting block is I_(7V). There are nineteen actual wing roles whose frame contacts are exactly two points. Their endpoint graph is K7 with the two edges (0,3) and (4,6) deleted. Degrees are
\[
 (5,6,6,5,5,6,5).
\]
Two edge roles sharing an endpoint are nonadjacent. All incidences are reconstructed from the integer real roots; the complete role mapping is in the receipt.

Role 77 contacts only frame point 0, and is nonadjacent to every edge role incident to that point. Role 107 has the corresponding properties at frame point 3. These two roles are the augmentations, each with an identity own block.

There are 7+19+2=28 roles. The extra isotropic role 3 from the earlier strict eight-mode proof is not used in this lower bound. Its independent review is recorded separately.

## 3. The augmented LR inequality

Let rank M = 7V+j and factor M=CR through that many coordinates. The identity frame permits a factor-basis normalization with the seven point rows and columns equal to the coordinate projections and inclusions. The remaining coordinate space has dimension j.

An edge e={a,b} has row and column support only at a,b,last. Write
\[
 \alpha_e(a)=C_{ea}R_{ea},\quad
 S_e=C_{e,*}R_{e,*},\quad
 \gamma_e(a)=\alpha_e(a)+S_e,\quad
 g_e(a)=\operatorname{rank}\gamma_e(a),\quad
 G_a=\sum_{e\ni a}g_e(a).
\]
The diagonal identity is alpha_e(a)+alpha_e(b)+S_e=I_V, so
\[
 \alpha_e(a)=I_V-\gamma_e(b).                         \tag{1}
\]

Restrict the incident edge rows and columns to the V+j coordinates a,last. Denote these by A_e,B_e. Stack all A_e and concatenate all B_e. At a=0 or 3, include also its singleton augmentation's full row and column, whose support lies in these coordinates. Put m_a=1 for a=0,3 and m_a=0 otherwise. The resulting product is block diagonal, with gamma_e(a) blocks and m_a identity blocks. Its rank is G_a+m_a V.

Let ell,rho be the stacked row and column ranks and lambda_e,mu_e the ranks of A_e,B_e. The kernel-of-product argument gives
\[
 \lambda_e-g_e(a)\le\ell-(G_a+m_aV),\qquad
 \mu_e-g_e(a)\le\rho-(G_a+m_aV).
\]
Indeed A_e annihilates every other column block, including the singleton when present, so its restricted kernel embeds into the full product kernel. Sylvester's rank inequality gives
\[
 \ell+\rho\le V+j+G_a+m_aV.
\]
By (1), each of lambda_e and mu_e is at least V-g_e(b). Combining these statements proves
\[
 G_a+(1+m_a)V\le j+2\bigl(g_e(a)+g_e(b)\bigr).        \tag{LR+}
\]
This is valid for every directed edge incidence and every field. It uses no characteristic-two equality classification.

Set h=j-V, so rank M=8V+h. Then
\[
 G_a+m_aV\le h+2\bigl(g_e(a)+g_e(b)\bigr).            \tag{2}
\]

## 4. An exact weighted sum

Partition the seven frame positions as
\[
 A=\{0,3\},\qquad B=\{4,6\},\qquad C=\{1,2,5\}.
\]
The endpoint graph has all edges between different classes, all edges inside C, and none inside A or B. Give the directed inequalities (2) these nonnegative integer weights:

| Incidence category | A to B | A to C | B to A | B to C | C to A | C to B | C to C |
|---|---:|---:|---:|---:|---:|---:|---:|
| Weight | 3 | 4 | 1 | 2 | 0 | 2 | 2 |

The sum of outgoing weights is 18 at each A point and 8 at every other point. Thus the total weight is 76, and the total weighted singleton contribution is 36V.

For a variable g_e(a), its coefficient in the weighted left side after moving the right-side gamma terms left is
\[
 \sum_{f\ni a}w_{a,f}-2(w_{a,e}+w_{b,e}),
 \qquad e=\{a,b\}.
\]
It is 10 at A endpoints and zero at all other endpoints. Therefore
\[
 76h\ge36V+10(G_0+G_3)\ge36V.                       \tag{3}
\]
This gives h >= 9V/19 and rank M >= 161V/19. The argument is valid for nonsymmetric, noncommuting block fittings over every field.

In characteristic two, the independently checked canonical binary fitting on all 76 roles has rank nine. Scalar extension preserves that rank, and tensoring with I_V supplies rank 9V. This upper bound is only asserted in characteristic two.

## 5. Width two has no fractional saving

**Corollary.** Over every field, a width-two fitting on the wing graph has rank at least 18. In characteristic two its minimum is exactly 18.

Suppose its rank were at most 17. The preceding bound forces rank 17, so V=2, j=3 and h=1. Equation (3) implies
\[
 76\ge72+10(G_0+G_3).
\]
The G quantities are nonnegative integers, hence G_0=G_3=0.

For an edge incident to A, LR+ gives 4 <= 3+2g_e(b), since its A-end gamma rank is zero. Thus the opposite gamma rank is at least one. Every non-A point has two A neighbors, so its G is at least two.

For every edge, choose a non-A endpoint b; all edges have one. Its ordinary LR inequality implies
\[
 2\bigl(g_e(a)+g_e(b)\bigr)\ge G_b-1\ge1.
\]
The edge gamma-rank sum is an integer, so it is at least one. Summing over nineteen edges yields sum_a G_a >= 19.

On the other hand, sum LR+ with weight one over all 38 directed incidences. This gives
\[
 \sum_a(\deg(a)-4)G_a+10V\le38h.
\]
At V=2,h=1 the first term is at most 18. Every degree is at least five, so sum_a G_a <=18, a contradiction. The characteristic-two canonical fitting attains 18. Square.

The scalar lower bound is likewise nine by integrality. This does not establish minimum 9V at arbitrary width.

## 6. The weighted bound is sharp for these rank inequalities alone

A precise formal witness prevents mistaking an optimized rank inequality for an actual vector code. Set
\[
 V=38,\quad h=18,\quad j=56.
\]
Assign the directed gamma ranks by category:

| Category | A to B | A to C | B to A | B to C | C to A | C to B | C to C |
|---|---:|---:|---:|---:|---:|---:|---:|
| Formal g value | 0 | 0 | 10 | 6 | 10 | 4 | 5 |

Their star sums are G_A=0 and G_B=G_C=38. Every one of the 38 inequalities LR+ is equality; all ranks are nonnegative integers no larger than V. This realizes h/V=9/19 in the numerical relaxation.

Consequently the stated LR+ inequalities, the G sum identities, nonnegativity, and even integral rank variables do not by themselves imply a larger asymptotic ratio. Any stronger universal bound needs additional matrix compatibility, another source seed, or another rank inequality. There is **no claimed fitting** with these formal ranks. Simultaneous matrices realizing their kernels, images and prescribed zeros remain unresolved.

## 7. Reproduction and remaining obligation

Run the supplied module on the exact root-recovery JSON:
\[
 \texttt{node check.mjs /absolute/path/to/RECOVERED-NATIVE-ROOTS.json > RESULT.reproduced.json}.
\]
Its CLI checks Git blob 8eba43d142c819c206dce5df87ea4571aaead287 before parsing. Expected status: PASS_WEIGHTED_WING_FRACTIONAL_GAP.

The exported checker was actually run through the available pure-JavaScript tool. It reconstructs all 76 wings, the seven-point frame, nineteen edge roles, singleton incidences, all weighted coefficients, the formal equality assignment, the predecessor isotropic anchors, and the characteristic-two rank-nine upper bound. No local Node CLI execution is claimed during the executor outage.

The proof supplies the all-field/all-width result; the finite source checks alone do not. Author execution and the independent predecessor review are separate from independent review of this new theorem.

The surviving fractional question is whether the actual wing graph has a block fitting with normalized rank strictly below nine. The interval [161/19,9] is genuine, and width two has now been excluded. A candidate must construct compatible row and column spaces, not only a feasible list of rank numbers.

No physical source, complete decoder, uniform arithmetic implementation, packet lifetime saving, or new kappa follows from these results. The full supplier, recursive costs, ownership, compiler, precision and retained foundational assumptions remain visible.
