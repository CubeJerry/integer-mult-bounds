# Complete cyclic three-head caller conservation

**Proved scoped algebraic theorem; independent review pending. No new kappa.** This result closes the scalar/cyclic first attempt at a three-native four-role construction. It does not exclude genuinely noncommuting ordinary head services. Its proof is separate from the unsuccessful bounded numerical searches.

## 1. Actual source and exact algebra

Use the admitted spectator-lifted canonical three-head source at programme baseline eefa411ebab86271d50b56b6953af3a157366bdb. Its actual head is A=C_b S, where S maps a to c, b to a, c to b. At one column,

    A^3=C_a C_b C_c,  A^6=X_a X_b X_c=:Z,  A^12=I.

The Gaussian ranks of its powers modulo six are r_k=(0,1,2,3,2,1). At width V, write a=A^(tensor V), z=Z^(tensor V), and D=8^V. Thus a^6=z, z^2=I. In particular a^6 is an actual ordinary translation, not a scalar set equal to one.

The two actual forward halves, after the proved ordinary source gauge and optional role swap, are

    L(a)=[[a,I],[0,a]],   U(a)=[[a,-a^2],[0,a]].

L is the actual lower half [[a,0],[I,a]] conjugated by the ordinary role swap; it is not obtained by charging a free inverse. The native field-level minus remains outside every tensor power. Literal inverse halves and sign/role gauges are allowed when their actual services are charged. Their physical Gaussian price remains [1]+[7]+[8], with fresh seven-axis body for each stage. Positive-body inversion also retains the two ordinary body translations identified by the source interface.

Fix any finite number R of independent retained roles, any m native halves and any finite inventory of in-place or distinct-role shear queries with coefficient a^k times a nonzero scalar. A query of this form has Gaussian head rank r_k in {0,1,2,3}; rank-zero queries are ordinary. All interstage and outer ordinary matrices are invertible matrices over C[z]={alpha I+beta z}. Coefficients may depend on V. This is an algebraic enlargement, not a claim that the matrices are free physical circuits. The source's fixed ordinary gauges are internal to the actual source interface, and are not granted as arbitrary additional interstage generators.

The independent endpoint is, up to such ordinary outer encodings, diag(a^k_1,...,a^k_R). Let H=sum_i r_(k_i). Every original input is arbitrary; no role is clean, discarded or omitted.

## 2. A phase-exact six-cycle auxiliary representation

Let rho(A) be the six-cycle e_j -> e_(j+1 mod6). Let P be diagonal with signs (+,+,+,-,-,-). Since rho(A^6)=I, P commutes with rho(Z). For each integer k,

    rank_C(rho(A^k)-P rho(A^k)P)=2 min(k mod6,6-(k mod6))=2r_k.       (1)

Indeed the difference is a permutation matrix with its entries multiplied by zero or plus/minus two. Exactly twice the circular displacement, capped at three, crosses the cut between the two three-point arcs. This proves (1) for all powers, not just sampled widths.

The twelve actual unitaries A^k are pairwise nonproportional. Their tensor Gram matrix has diagonal one and off-diagonal entries of modulus at most gamma^V for some fixed gamma<1. For every sufficiently large V its rows are strictly diagonally dominant, so the physical map phi_V:C[C12] -> End(C^D), A^k -> a^k, is injective. Any claimed all-width caller therefore holds at such a faithful width. This is the retained finite-catalogue tensor-separation argument.

At that width define

    Psi_0(A^k)=rho(A^k) tensor a^k,
    Psi_1(A^k)=P rho(A^k) P tensor a^k.

Both are genuine representations of the ACTUAL cyclic group of order twelve. The physical factor retains every scalar phase and the nontrivial translation a^6. No eigenvalue sector a^6=+I or -I has been deleted. The representations agree on C[z], and (1) gives

    rank(Psi_0(a^k)-Psi_1(a^k))=2r_k D.             (2)

An ordinary role matrix invertible in the faithful physical image has its inverse in the same finite-dimensional ordinary algebra, by its minimal polynomial. Its common auxiliary image is consequently invertible. The inverse is only an algebraic proof device unless a physical inverse service has separately been supplied.

## 3. Native difference rank and conservation

Set X=Psi_0(a), Y=Psi_1(a), E=X-Y. By (2), rank(E)=2D. For L the auxiliary difference is diag(E,E), of rank4D. For U it is

    [[E,-(X^2-Y^2)],[0,E]].

The identity X^2-Y^2=X E+E Y reduces this by invertible block row/column operations to diag(E,E), again of rank4D. Permitted C[z] role gauges and literal inversion preserve the difference rank. The fixed internal source gauges authenticate the displayed L/U operators; they are not arbitrary extra interstage generators of this cyclic model. Inactive roles contribute zero. A rank-r query changes one diagonal or off-diagonal block, so contributes difference rank2rD.

Apply both representations to the complete word and telescope its product difference. Ordinary factors contribute zero; each native contributes4D; each rank-r query contributes2rD. Independent endpoint roles contribute2HD. Rank subadditivity therefore proves

    H <= 2m + q_1 + 2q_2 + 3q_3.                 (3)

No finite search, determinant-only heuristic or unproved positivity assumption is used. The theorem holds at every sufficiently large faithful width, and therefore constrains every asserted uniform all-width caller.

## 4. Complete common-body consequence

Suppose each native introduces a fresh independent rank-seven body and every retained role receives it, so the m(R-2) inactive-role rank-seven idles are paid. Put [x]=x^t and delta=[8]-[7], with 0<t<1. The actual Gaussian movement price is

    Price=mR[7]+m(1+delta)+q_1[1]+q_2[2]+q_3[3].

Each endpoint has rank7m+r_i. Concavity and subadditivity give

    Target=sum_i [7m+r_i] <= mR[7]+delta H.

Using (3),

    Price-Target >= m(1-delta)
                     +q_1(1-delta)
                     +q_2([2]-2delta)
                     +q_3([3]-3delta) >0          (m>=1).

All coefficients are positive: delta<t*7^(t-1)<r^(t-1) for r=1,2,3, since t<1 and r<=7. This excludes every complete common-body inventory in the stated cyclic ordinary family for every 0<t<1, before adding the required ordinary, precision, ownership, layout and recursive costs.

In particular the three-native four-role target ranks(3,3,1,1) has H=8>6 and cannot be obtained in this family. Its favorable raw movement invoice is not a construction. Adding genuinely noncommuting ordinary phases/permutations or changing the body/source contract leaves this theorem's scope; those changes still require actual proof and accounting.

## 5. Verification and provenance

The exact checker verifies the actual one-column A, its twelve powers, the six-cycle difference ranks, ordinary agreement on A^6, source orientations including the role swap, and source difference-rank reductions. Width-one/two comparisons retain A^6 and reject replacing it by I; a source field-sign control rejects tensoring the native minus. Those checks are diagnostics for the explicit formulas, whereas the tensor-separation and telescoping arguments establish the universal statement.

Dependencies are the admitted three-head source and the retained tensor-separation lemma, pinned in DEPENDENCIES.json. Credit @CubeJerry and the canonical native/compiler, S014 source/tensor authors, and S015 Worker B with substantial OpenAI assistance. Independent review is a separate gate. All five foundations remain; no new complete kappa.
