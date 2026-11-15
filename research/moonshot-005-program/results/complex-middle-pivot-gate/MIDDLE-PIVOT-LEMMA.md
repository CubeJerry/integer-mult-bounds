# A middle Gaussian pivot cannot supply an additional independent high-rank pair

**Exact structural lemma and three-native same-orientation corollary; independent review pending. No new kappa.** This is a written consequence of the actual retained-role source, not an interpretation of a failed numerical search. Mixed ordinary-cross/square-cross native words remain open.

## 1. Ordinary Gaussian-pivot lemma

Work in the same finite phase-exact ordinary-bimodule algebra as the admitted source gates. Split four roles into two active and two idle roles; all displayed blocks below have physical dimension2D. Let K=G+E act on the middle active pair, with E ordinary and G invertible and pure of one positive Gaussian rank. The middle source is diag(K,I). The left and right outer nonordinary blocks N_L,N_R act on the active pair, with identity on the idle pair; suppose their entries belong to F_s and F_t, respectively.

Let

    W=C_L diag(K,I) C_R,
    M=diag(N_L,I) W diag(N_R,I),

where C_L,C_R are invertible ordinary matrices. Assume:

1. The idle-idle block W_ii=M_ii is invertible and pure of the same rank as G, and its corresponding rank component is obtained solely from the active G block of the middle source.
2. M_ai M_ii^-1 is ordinary. This is necessary whenever an ordinary output encoding separates the high active endpoint jobs from the independent idle jobs.

Then the Schur complement

    M_aa-M_ai M_ii^-1 M_ia

belongs to F_(s+t). Thus any independent active endpoint which has no components of ranks<=s+t contradicts these hypotheses.

**Proof.** The relevant homogeneous component of W_ii is A G B, where A=(C_L)_ia and B=(C_R)_ai. Its invertibility forces both square ordinary blocks A,B invertible. By ordinary row/column normalization on the idle pair, which commutes with the outer active sources, arrange A=B=I. Write

    C_L=[[P,Q],[I,D]],     C_R=[[E_0,I],[F,H]].

Since W_ii=G+E+D H is pure of G's positive rank, E+D H=0 and W_ii=G. Put R=Q-PD and S=F-H E_0. Invertibility of C_L,C_R forces R,S invertible, although the following degree argument does not require their inverses. Direct noncommutative multiplication gives

    W_ai=P G+R H,
    W_ia=G E_0+D S,
    W_aa-W_ai G^-1 W_ia=R(I-H G^-1 D)S.           (1)

The ordinary left elimination coefficient is

    M_ai M_ii^-1=N_L P+N_L R H G^-1.

As N_L P belongs to F_s, hypothesis2 implies N_L R H G^-1 belongs to F_s as well. Now(1) yields

    Schur(M)=N_L R S N_R-(N_L R H G^-1)D S N_R,

which belongs to F_(s+t) by ordinary-bimodularity and the filtration product inequality. Every inverse here is an algebraic proof device; no inverse source/query or physical projection is provided. QED.

The proof handles arbitrary singular ordinary blocks D,H and noncommuting coefficients. In particular E+D H=0 does not imply that either D or H is invertible.

## 2. Three actual ordinary-cross natives on four retained roles

Consider three actual native halves, each with an ordinary cross, on any fixed finite Clifford head family and four arbitrary retained roles. Relabel each active pair to the first two coordinates, absorbing all role changes into ordinary interstages. Each native has active block L_j=a_j I_2+E_j in F_1, where a_j is a rank-one Gaussian unit and E_j is ordinary; its idle block is I_2.

Suppose their independent endpoint were two rank-three Gaussian jobs and two rank-one Gaussian jobs, up to arbitrary invertible ordinary encodings. The rank-three component must use all three rank-one source components. Therefore its output lies entirely in the active pair of the last source, and its input row space lies entirely in the active pair of the first source. Its physical rank is exactly2D, so these containments are equalities.

Writing the ordinary endpoint encodings in active/idle block form now gives

    U=[[U_h,U_hi],[0,U_l]],
    V=[[V_h,0],[V_lh,V_l]],

with all four diagonal blocks invertible ordinary. Thus M_ii=U_l diag(G_1,G'_1)V_l is invertible pure E_1; M_ai M_ii^-1=U_hi U_l^-1 is ordinary; and the active Schur complement equals

    U_h diag(G_3,G'_3) V_h,

an invertible pure E_3 block.

Apply the lemma to the middle native, with G=diag(a_2,a_2), E=E_2, N_L=L_3 and N_R=L_1. Its E_1 block is obtained solely from G because all other middle coefficients are ordinary. The lemma gives Schur(M) in F_2, contradicting pure E_3. Therefore three ordinary-cross native halves cannot produce the target(3,3,1,1).

The same conclusion holds when all three native halves have square crosses: invert the entire asserted identity. Each inverse native has an ordinary cross, each endpoint Gaussian inverse has the same rank, and all ordinary inverses remain in the ordinary algebra. This is a proof reduction, not a free physical inverse.

## 3. Remaining constructive case and cost boundary

Consequently the no-query, three-native, four-role target(3,3,1,1) must use a mixture of ordinary-cross and square-cross orientations. Up to whole-word inversion, exactly one square-cross source remains. Its position and genuine noncommuting ordinary interstages matter. This lemma does not close that mixed case and does not assert an all-native conservation theorem.

The complete optimistic invoice remains3[1]+9[7]+3[8] versus2[24]+2[22], including six paid rank-seven idles. All actual source gauges, scalar phases, the2^V spectator volume factor, ordinary/precision/ownership/compiler work and recursive supplier admission remain. A favorable invoice and the surviving mixed-source normal form do not constitute a caller.

Dependencies: admitted source/rank-bimodule model; elementary noncommutative block algebra; independent endpoint contract. The lemma adds no numerical or foundational assumption. Credit @CubeJerry, predecessor component/source authors and S015 Worker B with substantial OpenAI assistance. Independent review is separate.
