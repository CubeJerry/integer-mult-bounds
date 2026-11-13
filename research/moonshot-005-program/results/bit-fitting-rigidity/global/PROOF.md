# Global scalar BIT fitting rigidity and the invertible-Schur block stratum

Author exact theorem with finite source witnesses; independent review pending. This goes beyond the previously frozen local/formal theorem. Arbitrary noncommuting block fittings with singular Schur blocks remain open. No new complete Q or kappa.

## Complete target budget and theorem statement

Use the actual111-port rational-chart BIT source, SHA256 `51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`. Here a foreign contact is REAL root orthogonality. For characteristic-two coefficients, a fitting has K_ii=I_V and K_ij=0 at every offdiagonal NONcontact. The proved nine-frame theorem gives minimum rank9V. The canonical K0=J+(v_i dot v_j/2 mod2) has rank9,111 diagonal ones and6470 foreign ones. The complex96/104 graph is different and is not identified with this source.

The existing complete fixed-even-m sharing caller has conditional private-rail allowance

    Q_paid(t) < (N-H)(t) + m*(T2-P2)(t)/(36*(m-1)).

Its limiting allowance is1621.750880211152... at t=199/200. The baseline all-Hub partial canonical nine-packet rail costs1610.208873484099... and leaves limiting correction allowance11.542006727052..., or7.430310278604... at m4. Its6470 foreign coefficients and rank108 residual K0+I are unpaid. These are baseline allowances; any changed acquisition receives a new complete profile. No rank or matrix-density saving is granted a transport price here. Any fitting alternative must supply its literal acquisition, correction and every original endpoint within the complete invoice.

**Scalar theorem.** Over EVERY field k of characteristic two, every rank9 fitting on this source has

    K_ij = u_i K0_ij u_j^(-1),  u_i in k^*.

Thus all6470 foreign entries are mandatory and nonzero. Over F2, K0 is the unique rank9 fitting. No SAT result is a premise. The ordered proof also works over characteristic-two division rings.

**Block theorem.** Fix the actual eight-frame F below. For an arbitrary rank9V fitting, define27 intrinsic Schur diagonal blocks S_e below. If ALL27 are invertible, the same formula holds with u_i replaced by U_i in GL_V(k), with no symmetry or commutation assumptions. Hence every foreign block has full rank V in this stratum. A counterexample outside vertex gauge must have a singular S_e.

A further global corollary covers normalized nine-coordinate factorizations whose block coefficients all lie in a common COMMUTATIVE characteristic-two algebra: their Schur blocks are automatically units, so they are vertex gauge. The unrestricted noncommuting singular-Schur case is not covered.

## 1. Actual sparse-edge seed

Let F=[0,16,17,32,36,38,67,71], in this order. Its principal fitting block is I_(8V). A rank factorization K=CR at dimension9V can be put in the legitimate gauge

    C_(F_a)=e_a^T tensor I_V,  R_(F_a)=e_a tensor I_V, a=0,...,7.

Indeed im R_F and ker C_F are complementary subspaces of dimensions8V,V; choose a basis of the latter as the ninth coordinate. This is a source-frame gauge, not a simultaneous normalization of the nine complementary parity projectors.

The canonical matrix has an exact symmetric factor K0_ij=x_i dot x_j, x_i in F2^9, x_(F_a)=e_a. The source verifier reconstructs all111 vectors and checks all12321 products. Exactly27 source roles have canonical vector e_a+e_b+e_last. Their endpoint pairs form the graph

    G = K8 minus edge(0,4).

The role/edge dictionary is retained in CERTIFICATE.json. Every degree is6 or7, and every four vertices induce at least five edges, hence two adjacent edges. For distinct edge roles e,f, the prescribed fitting entry is zero exactly when their endpoint pairs intersect.

For ANY fitting in the F gauge, each edge role e={a,b} therefore has the sparse factor form

    C_e=(c_ea at a, c_eb at b, u_e at last),
    R_e=(r_ea at a, r_eb at b, v_e at last).

The other first eight coordinates are exactly zero by the prescribed zeros to F. The displayed coordinates may initially be singular or zero. For adjacent e,f sharing a, the only overlap is a and last, so

    c_ea r_fa + u_e v_f = 0.

The edge diagonal is c_ea r_ea+c_eb r_eb+u_e v_e=I. The intrinsic last-coordinate Schur diagonal is

    S_e=u_e v_e=I_V+sum_(a=0..7) K_(e,F_a) K_(F_a,e).

Only its two endpoints contribute. This formula makes invertibility independent of the auxiliary factor basis and invariant under vertex gauge.

## 2. Invertible Schur blocks force the sparse seed, at every volume

Assume all27 S_e are invertible. Then each u_e,v_e is an invertible V-by-V matrix. Apply the edge vertex gauge C_e -> u_e^(-1) C_e, R_e -> R_e u_e. Its last coordinates become1 and h_e=v_e u_e, with h_e invertible. Write A_ea,D_ea for its normalized endpoint blocks. Adjacent edges e,f at a satisfy

    A_ea D_fa = h_f, e!=f.

Every endpoint block is invertible: each product on the left equals a unit, and these are square matrices over a field. At a vertex a there are at least three incident edges. For any two e1,e2 choose a third f. Right cancellation of D_fa gives A_(e1,a)=A_(e2,a). Denote this common invertible block A_a. Consequently

    D_ea = A_a^(-1) h_e.

For e={a,b}, the diagonal identity becomes

    I = A_a A_a^(-1)h_e + A_b A_b^(-1)h_e + h_e
      = h_e+h_e+h_e = h_e

in characteristic two. Thus every h_e=I. This is an ORDERED calculation and never interchanges operator factors.

The global factor-basis change diag(A_0^(-1),...,A_7^(-1),I) makes every edge factor exactly e_a+e_b+e_last in both row and column. It changes the frame factors by A_a^(-1),A_a; a compensating frame-vertex gauge A_a restores them. Hence the35 seed roles F plus the27 edges have canonical factors after legitimate vertex and ambient-basis changes.

For each of the remaining76 source roles i, the finite certificate gives EIGHT noncontact seed roles j whose canonical x_j span rank8. Their annihilator in nine coordinates is the one-dimensional line spanned by x_i. All binary8-minors used for this claim are nonzero. In characteristic two those same scalar equations hold for arbitrary matrix blocks, and imply

    C_i = U_i x_i^T,   R_i = x_i V_i.

Because x_i dot x_i=1, the diagonal is U_i V_i=I, so U_i,V_i are inverse square matrices. Applying the corresponding vertex gauge makes both factors canonical. Every role is now canonical, proving K_ij=U_i K0_ij U_j^(-1) for the original fitting. In particular all6470 foreign blocks have full rank V. This proves the all-V invertible-Schur theorem.

## 3. Scalar Schur degeneracy is impossible over every characteristic-two field

Now V=1, with coefficients in an arbitrary characteristic-two field. Suppose an edge e={a,b} has u_e=0. Its diagonal gives c_ea r_ea+c_eb r_eb=1, so at least one endpoint product is nonzero; choose a. Thus c_ea and r_ea are nonzero.

For every other incident edge f={a,c}, the prescribed zero K_ef=0 gives c_ea r_fa=0, hence r_fa=0. For distinct such f,g, their own shared-endpoint zero is therefore

    u_f v_g = 0.

Let U be the incident edges f!=e with u_f!=0, and Vset those with v_f!=0. No member of U can differ from a member of Vset. Hence either U is empty, or Vset is empty, or both consist of the SAME single edge h. In the first case all the at least deg(a)-1 other edges have u_f=0; in the second all have v_f=0. In the last case delete h and all the remaining at least deg(a)-2 edges have both zero. Since deg(a)>=6, choose a family of at least FOUR edges f={a,c}, all with u_f=0 or all with v_f=0. For every chosen f the diagonal simplifies to

    c_fc r_fc = 1,

because r_fa=0 and u_f v_f=0.

Let W be their private endpoints c. It has size at least4. The graph induced by W has two adjacent edges. First consider the case all chosen u_f=0. For ANY source edge g={c,d} in G[W], the zeros from f={a,c} and f'={a,d} give r_gc=r_gd=0, since their private endpoint coefficients c_fc,c_f'd are nonzero. Thus the diagonal of g forces u_g v_g=1. This holds for every edge in G[W]. Take two adjacent ones g,h; their shared endpoint term is zero, so their prescribed zero says u_g v_h=0, contradicting that both factors are nonzero.

If instead all chosen v_f=0, use the reversed zero equations K_gf=0. They give c_gc=c_gd=0 for every edge g in G[W]. The same diagonal u_g v_g=1 and adjacent-edge contradiction follows. Thus u_e cannot be zero. Reversing all row/column roles proves v_e cannot be zero either. Every S_e=u_e v_e is consequently invertible. Section2 now proves global scalar rigidity.

The scalar zero-propagation uses only cancellation and absence of zero divisors. The same ordered proof works in a division ring (or apply the reversed argument in its opposite ring). Thus minimum-rank scalar rigidity holds over every characteristic-two division ring as well. This does NOT let one treat a full matrix algebra as a division ring; singular matrix blocks are the remaining obstruction.

## 4. Global commutative-factor corollary

Suppose a nine-coordinate factorization in the normalized F gauge has all coefficient blocks in a common commutative unital F2-algebra A. This includes scalar extensions, commuting idempotents and commuting nilpotent operators, provided the normalized factors lie in that algebra.

For each maximal ideal m of A, reduce all equations modulo m. They are a valid scalar nine-coordinate fitting over the characteristic-two residue field A/m, with the same normalized frame. Its rank is at most9 by the factorization and at least9 by the parity theorem. The scalar proof shows every reduced u_e and v_e is nonzero. Thus u_e and v_e belong to no maximal ideal of A, so they are units: otherwise their proper principal ideal would lie in a maximal ideal. The ordered proof of Section2 now works over A. Products equaling units have unit factors in a commutative ring; all binary anchor minors remain units; and U_i V_i=1 makes both units. Hence

    K_ij=U_i K0_ij U_j^(-1),  U_i in A^*.

This is global within the commuting-factor class, including remote and nonsemisimple strata; it is not merely a formal-neighbourhood statement. In particular commuting scalar bundles cannot reduce foreign block support. This does not claim that every fitting with pairwise commuting matrix ENTRIES automatically has an admitted nine-coordinate factorization over that same algebra. The stated factor condition is explicit. Over a field, the usual rank factorization and frame gauge always exist.

## 5. An explicit global component selector at every volume

For any fixed V, take the reduced affine variety X_V of fitting block matrices of rank at most9V over an algebraically closed characteristic-two field. The previously proved minimum-rank bound makes every point have rank exactly9V. Define the polynomial

    p(K)=product_(27 edge roles e) det S_e(K).

If p(K) is nonzero, Section2 makes K vertex gauge of K0 tensor I_V. For every such gauge, each Schur diagonal S_e is EXACTLY I_V, since its two endpoint round-trip products are both I_V. Hence p(K)=1. Otherwise p(K)=0. Thus the canonical vertex-gauge orbit is both

    O_V = X_V intersect D(p) = X_V intersect V(p-1).

It is OPEN AND CLOSED, with complementary singular-Schur stratum X_V intersect V(p). The contact graph is connected (checked exactly), so fixing one vertex gauge identifies O_V with GL_V raised to the110th power: inverse coordinates are obtained by ordered products along a fixed contact spanning tree. Consequently O_V is an entire irreducible and connected component, of dimension110V^2. Any nongauge minimum fitting lies in a disjoint component with at least one singular Schur block. This is a global component statement, stronger than the earlier formal-neighbourhood result; it does not prove that the complementary component set is empty for V>1. No assertion about nonreduced scheme structure is needed.

## 6. Consequence, certificate and precise remaining task

There is no scalar rank9 fitting over ANY characteristic-two field with fewer than6470 foreign nonzeros. Over F2 the canonical fitting itself is unique; field extensions supply only vertex gauge, not deleted contacts. Conjugating by the block diagonal matrix diag(U_i) also preserves K+I, so its foreign residual has rank108V throughout the block stratum (rank108 in the scalar case). This is an algebraic rank statement, not a claim that108 recursive calls are necessary. The root's earlier F2/GF4 solver screens are consistent with this theorem but are not used in its proof.

For arbitrary V, the invertible-Schur theorem forces all foreign blocks to be full rank. Thus any genuinely different minimum fitting with a removed or rank-deficient foreign block must enter a SINGULAR Schur stratum among the27 explicitly listed edge roles. If its normalized factors all lie in a commutative algebra or a division algebra, it is again gauge canonical. The remaining fitting escape requires noncommuting operators with zero divisors; it is not excluded here. The nine equality-projector decomposition and other rank constraints might still rule it out, but that proof is owed.

Run `python3 -I -B verify.py --repo REPO --output OUT`. This reads only the authenticated native, not an author search or SAT output. It normalizes the111 rational source roots, constructs K0, checks the exact9-factor on all12321 entries, lists the27 sparse roles and their K8-minus-one endpoint dictionary, checks all70 four-vertex subsets and endpoint degrees, and records76 independent eight-anchor extension certificates. Every indicated binary8-minor has determinant1. Deleting one anchor lowers that witness rank to7, a negative control against claiming uniqueness without all eight constraints. Python -O is rejected before checks. The finite PASS supplies these exact source premises; the scalar no-zero argument and block gauge proof above provide the universal quantifiers.

The source9V lower bound is independently established by the retained nine-frame parity theorem, `bit-minrank-nine/PROOF.md`, SHA256 `669c8441a7f5d65e4c483f2d444160d365f754dbe5789b5588c3c0d6dad7e1cc`. No numerical rank search, SAT result, characteristic-zero fitting theorem or actual complex-source geometry is imported as a rigidity premise. All remaining physical acquisition, main/correction map, endpoint, owned-erasure, compiler/storage/precision and analytic obligations remain. Both strict suppliers and all five programme foundations remain open. No new complete kappa is claimed.

Credit: @CubeJerry programme and retained BIT/native authors; root's canonical fitting and parity lower bound; worker B's sparse-edge classification, scalar zero propagation, ordered all-V open-stratum proof, commutative-factor extension and exact anchor certificate; OpenAI-assisted mathematical research. Retained predecessor credit is preserved.
