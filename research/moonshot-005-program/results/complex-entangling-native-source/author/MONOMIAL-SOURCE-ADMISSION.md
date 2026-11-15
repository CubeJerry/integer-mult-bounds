# Exact monomial criterion for a physically admissible common native head

**Proved algebraic source-admission theorem, independent review pending.** This characterizes the entire common-head gauge family used by the new order-nine and entangling order-fifteen constructions. It gives an ordinary circuit for the apparently Gaussian inverse expression and shows that every admitted head retains the rank-one/rank-two premises of earlier generic obstructions. No new kappa.

## 1. Proposition with actual phases

Fix any head dimension d≥2 independent of tensor width, two distinct axes a,b, and an actual unitary monomial Clifford S. Let

    C_v=((1+i)I+(1−i)X_v)/2,
    A=C_b S,          R=C_a^-1 S C_b S.

Write the conjugated Hermitian Pauli as

    q=S X_b S^-1=ε i^(v·w) X_v Z_w,

where ε∈{+1,−1}, v,w∈F2^d and v is nonzero. Then R is ordinary monomial **if and only if**

    v=e_a,       w_a=0.                                  (1)

If (1) holds, q=ε X_a Z_w, and R has the explicit physical implementation

    R=J S²,
    f(x)=(1−ε(−1)^(w·x))/2 ∈{0,1},
    J|x⟩=i^f(x)|x+f(x)e_a⟩.                            (2)

This is an ordinary controlled coordinate permutation and unit-phase pass; it evaluates no Gaussian inverse. Since w_a=0, the control f is invariant under the conditional X_a, so the map is bijective and its inverse is equally explicit. For every admitted S,

    r(A)=1,       r(A²)=2.                               (3)

All identities tensor with their actual phases to every width V. Preapplying S,R and postapplying S^-1 gives the original independent native halves [[A,0],[I,A]] and [[A,−A²],[0,A]], with the cross minus outside tensor powers.

## 2. Necessity and sufficiency of the criterion

Use Pauli labels (x,z), with Gaussian rank the binary rank of the upper-right symplectic block. Conjugation by C_q has transvection matrix

    T_q=I+(v,w)(w,v)^T.

The sign ε changes actual phases but not this symplectic matrix. The inverse of C_a has the same symplectic transvection as C_a, since transvections are involutions in characteristic two. Right multiplication by the ordinary S² preserves Gaussian rank. Therefore R is monomial exactly when the upper-right block of T_(e_a,0) T_(v,w) vanishes. That block is

    B_R=e_a e_a^T + v v^T + w_a e_a v^T.                (4)

If v=e_a, it is w_a e_a e_a^T, which vanishes precisely when w_a=0. If v and e_a are independent, (4) factors as

    [e_a,v] [[1,w_a],[0,1]] [e_a,v]^T.

The outer matrices have column/row rank two and the middle matrix is invertible, so its rank is two. This proves the iff statement, including zero-divisor-free finite-field rank reasoning.

Under (1), the commuting involutions X_a,Z_w permit a direct actual phase calculation. On εZ_w=+1, C_a^-1 C_q=I; on εZ_w=−1, C_a^-1 C_q=iX_a. This is exactly (2). Since S C_b S^-1=C_q, multiplying by S² proves R=J S².

Finally A=C_b S has rank one by ordinary right invariance. Its square is C_b C_q S². In the corresponding version of (4), the independent x-vectors are e_b and e_a, so its upper-right block has rank two for either value of w_b. This proves (3). In particular no admitted phase gauge evades the earlier generic two-native or query-count gates by changing the rank of A².

## 3. Actual source, uniformity and full costs

The exact identities C_b S=A, S^-1 C_a R=A and C_a C_b R=A² prove both source halves on every original input. The literal three ordinary boundary services S,R,S^-1 are finite monomials. For fixed d their tables and inverses have fixed size; tensor phases admit the same amortized odometer generation and exact norm-one arithmetic as PROOF.md. Keep three coordinate-permutation services, three phase passes, all native MOVE/ADD work, precision and recursive costs, and every real compiler/layout/tape expense. Additional d−2 spectator axes multiply the full source and target array volumes by2^((d−2)V). This is not a zero-cost change of the source array.

In three heads, the symplectic ordinary subgroup has168 binary invertible coordinate maps times64 symmetric phase matrices. Condition (1) chooses24 maps with P e_b=e_a and32 phase matrices with the relevant diagonal zero, hence768 symplectic ordinary gauges. There are768 excluded rank-one residual gauges and9216 excluded rank-two residual gauges. Actual Pauli signs and centre phases are retained by (2); this symplectic census is not a declaration that their physical tables coincide.

The order-nine source uses w=0, ε=+1, hence J=I. The order-fifteen source uses w=e_c, ε=+1, hence J is the explicitly paid controlled-X_a and quarter-phase on c. Its entangling operation is an actual gauge consequence of the native source.

## 4. Classification and continuation

This source-admission theorem does not construct a retained-role caller. It provides a complete, rigorously delimited way to generate and authenticate more powerful common heads, with all inherited generic obstructions still visible. A proposed S outside (1) incurs a nonordinary residual R of rank one or two and must pay for it; it cannot be called an ordinary boundary normalization.

Source and scalar conventions are pinned in DEPENDENCIES.json, and the general tensor/rank invariance dependency is pinned in LOCAL-WREATH-DEPENDENCIES.json. Credit @CubeJerry, the real native/source and Gaussian-rank predecessors, and Worker B's actual-phase admission criterion with OpenAI assistance. No complete new kappa.
