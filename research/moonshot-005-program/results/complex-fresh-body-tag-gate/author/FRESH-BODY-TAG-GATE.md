# Fresh body tags prevent graph-local head/body fission

**Scoped theorem candidate, pending independent review.** Unique fresh seven-axis blocks cannot repair the two-head native by simply omitting common-body idles or choosing different one-shot body recipients. Under the model below the Gaussian deficit is at least m(1+7^t-8^t)>0 for 0<t<1. Reused/interleaved bodies, head/body mixing and changed sources are excluded. **No new kappa.**

## 1. Failed optimistic relaxation

One native plus two rank-one queries on four roles has optimistic targets 2[7]+2[2] and price 3[1]+[7]+[8]. The raw margin at t=199/200 is about 0.00113. It assumes native heads can be transferred into roles without the native's fresh body tag. This is favorable arithmetic, not a circuit.

## 2. Exact tag model

There are R independent retained banks and m canonical halves. Stage s introduces F_s on seven axes disjoint from heads and all other stages. F_s is applied once to the two native roles and optionally once to i_s idle roles, in one combined stage before another role-mixing step. Put k_s=2+i_s and I=sum i_s. No other operation uses F_s; repeated separated applications are outside scope.

The head stage is N_s. Its k_s body recipients have coordinate projector P_s, with N_s-I supported inside P_s, and the complete stage is

    E_s(f_s)=(I+(f_s-1)P_s)N_s.                  (1)

Other operators act on heads or have coefficients in the fixed finite algebra of COLLECTIVE ordinary body translations X_w^(tensor V). Per-column or width-growing translation families are excluded. They do not mix head/body coordinates. There are q1 rank-one and q2 rank-two head queries, with the full finite monomial Clifford ordinary family of `FULL-CLIFFORD-CONSERVATION.md`.

Every independent endpoint is a head Gaussian G_i, rank r_i in {0,1,2}, times a subset of whole seven-axis blocks in either orientation. Its body degree d_i gives total rank 7d_i+r_i. Partial body-block use or nontrivial body recharting is not assumed to satisfy this contract.

Each F_s is the product of the seven fresh square-root-of-translation Gaussians Q_w. The signs f_s=+/-1 below are actual simultaneous spectral evaluations: two identical body-frequency columns make each chosen individual body Gaussian -1 with square +1; unchosen axes have sign +1. Pad to any larger width. Every collective translation X_w^(tensor V) has eigenvalue +1 on duplicated columns, since its two signs multiply to +1. An odd-weight duplicated frequency within block s gives F_s=-1, and zero weight gives +1, independently across disjoint blocks. Thus all coefficients in the stated collective translation algebra agree at these comparisons, while the head input remains arbitrary. No fictitious independent phases are granted.

Absorb ordinary outer encodings into the word so the required endpoint is diagonal. At the all-positive body point the exact head word is invertible.

## 3. Each stage tags exactly k_s final roles

Hold other body signs positive and compare f_s=-1 with f_s=+1. If U_s is the full suffix after this stage at that reference point, (1) yields

    M_- M_+^(-1)=U_s(I-2P_s)U_s^(-1).

The diagonal endpoint gives I-2P_s^target, where P_s^target selects final roles containing block s. Both Gaussian orientations have the same sign at these evaluations. Hence

    U_s P_s U_s^(-1)=P_s^target.                 (2)

Ranks agree, so exactly k_s final roles contain this tag. Consequently sum_i d_i=2m+I.

## 4. Bodyless outputs receive no native contribution

Let E select final roles with d_i=0 and r_i>0. Then E P_s^target=0 for every s. From (2), E U_s P_s=0, hence E U_s(N_s-I)=0. Work backwards through the word: each native acts as identity on these selected row trajectories. Removing natives in reverse order preserves the selected suffix rows, so

    E M_head = E K,                              (3)

where K is the word with all native halves removed and all ordinary/head queries retained. K has exactly q=q1+q2 queries. This is a row identity on every original input, not merely a dimension count.

Write h1,h2 for the bodyless rank-one/rank-two target counts, H0=h1+2h2. Applying the full two-head auxiliary rank representation to (3) and telescoping the query-only word gives

    H0 <= q1+2q2.                                (4)

Also h1+h2<=q. Here is a separate proof of the count bound. In K, impose zero source/affected-bank constraints at each query after its ordinary-only prefix. Their common right kernel has dimension at least (R-q)D, and on it K agrees with the invertible ordinary-only word O. The kernel projector P belongs to the finite *-closed ordinary algebra. Since all selected endpoint heads have positive Gaussian rank, pi_0(EK)=0. Bimodularity and EKP=EOP give EOP=0. But EO has rank (h1+h2)D, so dim ker(EO)=(R-h1-h2)D. Comparing dimensions gives the count bound. The projector is a proof device, not a physical service.

## 5. Complete invoice

Let a=8^t-7^t, 0<t<1. For d>=1 and r in {0,1,2}, concavity gives

    (7d+r)^t <= d 7^t+r a.

The global head word at all-positive body signs obeys H_b+H0<=2m+q1+2q2 by the full two-head conservation theorem. Thus the body-bearing target moment is at most

    (2m+I)[7]+a(2m+q1+2q2-H0).

For the bodyless part, put c1=1-a and c2=[2]-2a. Its moment less aH0 is c1 h1+c2 h2. Rewrite this as

    (2c1-c2)(h1+h2)+(c2-c1)(h1+2h2).

Both coefficients are nonnegative: 2c1-c2=2-[2]>0 and c2-c1=[2]-1-a>0 by decreasing concave increments. The two query-only bounds therefore show

    T0-aH0 <= c1 q1+c2 q2.

Combining terms gives the total target bound

    T <= (2m+I)[7]+2m a+q1[1]+q2[2].

The actual Gaussian price is

    P=m([1]+[7]+[8])+I[7]+q1[1]+q2[2].

Hence

    P-T >= m(1+[7]-[8])=m(1-a)>0.               (5)

Every ordinary/precision/layout expense worsens this deficit. The source heads cannot be moved into independent bodyless outputs for free, which was the missing condition in the favorable fission relaxation.

## 6. Scope, verification and continuation

This proof requires one-shot independent body tags, a whole-block Gaussian endpoint, head-only ordinary mixing (plus commuting body translations), fixed two-head Clifford algebra and complete independent inputs/outputs. A construction with reused body axes, genuinely interleaved repeated body applications, head/body recharting, extra head coordinates or a different source is not excluded. The result is not a general multiplication lower bound.

Independent review must check the actual sign-point construction, coefficient/tag comparison, backwards deletion on selected rows, query-only rank/count bounds and the final concavity combination. This candidate has a written universal argument; it is not inferred from finite search. Source and head-representation dependencies are the pinned canonical half and `FULL-CLIFFORD-CONSERVATION.md`. Credit @CubeJerry, the native/compiler and representation authors, and S014 Worker B with OpenAI assistance. No new kappa.
