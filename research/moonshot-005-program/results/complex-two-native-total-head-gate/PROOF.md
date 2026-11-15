# Two native halves cannot amplify total endpoint head rank

**Proved within the stated exact finite-Clifford interface; independent review pending. No new kappa.** Two native halves, with any number of independent retained roles and arbitrary invertible ordinary encodings, have total independent Gaussian endpoint head rank at most four. Rank-zero endpoint jobs are allowed. The head dimension is any fixed finite dimension admitted by the source. This closes the tempting two-native three-role targets(3,1,1) and(3,2,0), and makes three native halves the first possible no-query count for this source family.

## 1. Exact model and statement

Use the actual canonical native and its admitted common-head gauges. Each half, up to ordinary role permutations and scalar sign conjugation, has one of the forms

    L(a)=[[a,I],[0,a]],     U_c(a)=[[a,c a²],[0,a]],

where a is an actual source-bound rank-one Gaussian Clifford unit whose square a² is pure Gaussian rank TWO, c is a nonzero scalar (the physical source uses c=+/-1), and all other retained roles are idle. Literal inverse changes L to a square-cross form and U to an ordinary-cross form, with a replaced by a^-1 and signs changed. This is an algebraic operation on an asserted identity; it does not supply a free physical inverse call.

Fix a finite phase-exact Clifford group algebra on a fixed number of head coordinates. Its ordinary subalgebra is the span of the computational-monomial Clifford subgroup. At a sufficiently large faithful tensor width let D be the physical dimension of a role, E_r its Gaussian-rank components, F_s=sum_(r<=s) E_r, and pi_r their ordinary-bimodule projections. All physical scalar phases are retained. Products obey F_s F_t subset F_(s+t), and invertible ordinary matrices have ordinary inverses by finite-dimensional inverse closure.

Let R>=2 independent retained roles carry two native halves, with arbitrary invertible ordinary matrices before, between and after them. There are no additional nonordinary queries. The independent endpoint, up to the ordinary outer encodings, is diag(G_1,...,G_R), with each G_i a Gaussian Clifford unit of rank h_i>=0. Every input is arbitrary; a head-rank-zero endpoint is a real independent ordinary job, not an erased or clean ancillary role. Write n_r=#{i:h_i=r} and H=sum_i h_i.

**Theorem.** H<=4 for every such exact all-width caller. The source-square premise is essential: the theorem is not stated for arbitrary rank-one Clifford a, whose square can have rank zero or one. Every a_j² used here has the pinned actual source's pure rank-two cross, and inverses preserve that rank.

The proof uses the retained two-role one-native/two-rank-one-query theorem only in one equality case. It does not assume linear head-rank conservation in higher head dimension, which is precisely what remains open for larger native/query inventories.

## 2. Degree, the unique rank-three job, and the missing-rank-two implication

Invert the entire asserted identity if both native halves have square crosses. Native and Gaussian endpoint inverses have the same Gaussian ranks, ordinary inverses remain ordinary, and both inverse natives then have ordinary crosses. Otherwise leave the word unchanged. We have therefore arranged that at most one half is U-type.

If both halves are L-type, the head word lies in F_2, so there is no endpoint of rank above two. If one is U-type and one is L-type, the word lies in F_3. Its rank-three component lies in the single affected output row of U when U is last, or in its single affected input column when U is first. Ordinary outer encodings preserve physical component rank. Hence

    h_i<=3 for all i,      n_3<=1.                         (1)

The mixed case also satisfies

    pi_2(M)=0  implies  pi_3(M)=0.                         (2)

To prove (2), first put U last. Absorb the intervening ordinary matrix into W=C L, so W belongs to F_1. Relabel U's active roles as1,2. The two corresponding output block rows are

    M_1=a W_1+c a² W_2,      M_2=a W_2.

If pi_2(M)=0, then M_2 lies in F_1, since it already lies in F_2. Thus

    M_1=a W_1+c a M_2

lies in F_2 as well. Every idle row already lies in F_1, so pi_3(M)=0. Transpose the complete word to handle U first. Transposition preserves Gaussian ranks and ordinary matrices; exchanging its two active labels restores the same form. The proof permits noncommuting ordinary coefficients and zero divisors.

For an independent Gaussian endpoint, (2) says

    n_3>0  implies  n_2>0.                                (3)

The implication is unavailable for an arbitrary nonlinear rank statistic; here it follows from the actual native square-cross coefficient.

## 3. The rank-one count with rank-zero jobs retained

Relabel each native active pair separately to the first two coordinates, absorbing the relabelings into ordinary encodings. Put p=R-2 and write the middle ordinary matrix as

    C=[[C_aa,C_ai],[C_ia,C_ii]],

with active block size2D and idle block size pD. For p=0 the arguments below are read with empty idle blocks.

The idle-idle block of M=N_2 C N_1 is C_ii, which is ordinary. The active-idle and idle-active blocks of pi_1(M) are exactly

    X=diag(a_2,a_2) C_ai,
    Y=C_ia diag(a_1,a_1),

and its idle-idle block is zero. Each native cross is either rank zero or rank two, so it contributes nothing to these rank-one cross blocks. Consequently

    rank(pi_1(M)) >= rank(C_ai)+rank(C_ia).                 (4)

Indeed the image from idle inputs contains an upper-block subspace of dimension rank(X), while the projection of the whole image onto idle outputs has dimension rank(Y). These dimensions add, irrespective of the active-active block.

Invertibility of C implies

    rank(C_ai)>=pD-rank(C_ii),
    rank(C_ia)>=pD-rank(C_ii).                             (5)

For the first bound, the stacked map (C_ai,C_ii) is injective on idle inputs. The row-dual argument gives the second. Since C_ii is a submatrix of pi_0(M),

    rank(C_ii)<=rank(pi_0(M))=n_0 D.                       (6)

Independent endpoint jobs and ordinary-bimodularity give rank(pi_1(M))=n_1 D. Combining(4)--(6) yields n_1>=2p-2n_0. Using R=n_0+n_1+n_2+n_3 and(1), we obtain

    n_1+2n_2+2n_3<=4.                                    (7)

This is the extension missing from the old no-rank-zero two-half statement. It keeps arbitrary rank-zero endpoint jobs explicitly; it does not delete them or charge them as absent inputs.

Equations(1) and(7) already give H<=4+n_3<=5. If H=5, then n_3=1. Equation(3) forces n_2>=1, and(7) then forces exactly

    n_3=1,  n_2=1,  n_1=0,  n_0=p.                      (8)

Thus only one equality case remains.

## 4. Ordinary stable cancellation in the equality case

Under(8), pi_1(M)=0. Its active-idle and idle-active blocks X,Y vanish, so C_ai=C_ia=0. Since C is invertible, C_aa and C_ii are both invertible. The whole head word splits as

    M=diag(B,C_ii),      B=N_2 C_aa N_1,

where B acts on exactly two roles and is invertible. Since rank(pi_0(M))=pD and C_ii is invertible, pi_0(B)=0.

We must still justify that the two high endpoint jobs can be separated by actual ordinary matrices on the active two-role space. This cannot simply be assumed from their ranks.

Write the asserted ordinary endpoint equivalence as

    M=U diag(G_3,G_2,G_0) V,

where U,V are invertible ordinary matrices and G_0 is the direct sum of the p ordinary Gaussian jobs. Its pi_0 component is

    diag(0,C_ii)=U diag(0,0,G_0) V.

The kernel of the left side is exactly the active input space; the image is exactly the idle output space. Since G_0 is invertible, the low endpoint input rows V_0 therefore annihilate the active input space, while V_high maps that space isomorphically onto the two high endpoint input roles. Likewise U_0 has image exactly the idle output space, and projection of U_high onto the active output space is an isomorphism. All these restricted square matrices are ordinary, because they are blocks of U,V and their inverses belong to the same finite ordinary algebra.

Taking the active-active block of M now proves

    B=U_active,high diag(G_3,G_2) V_high,active,             (9)

with both displayed outer factors invertible ordinary two-role matrices. This is a genuine two-role independent(3,2) endpoint. No free physical projection, clean input or cancellation of a nonordinary service has been performed; the restriction is only a consequence of an asserted exact caller identity.

## 5. Reduction to the admitted one-native/two-query gate

Every head-only native factor has an exact factorization into two rank-one in-place queries and an ordinary shear. With D_1(a)=diag(a,I), D_2(a)=diag(I,a),

    U_c(a)=D_1(a) [[I,cI],[0,I]] D_2(a),
    L(a)=D_2(a) [[I,I],[0,I]] D_1(a).

Both are direct all-column identities in any associative coefficient algebra. The equality case has a rank-three job, so Section2 forces a mixed U/L pair. Replace the SQUARE-CROSS U half of B in(9) by its two-query factorization, leaving the ORDINARY-CROSS L half as the exact F1 native base. We obtain a two-role word with that F1 base, two rank-one in-place queries and arbitrary invertible ordinary interstages, producing independent endpoint ranks(3,2).

The admitted `complex-inverse-native-query-gate/worker-b/INVERSE-NATIVE-TWO-QUERY-GATE.md` excludes precisely that word, in every query placement and physical phase sector. The replacement is a mathematical inclusion in the excluded class, not a new physical invoice or a claim that two queries can replace the native more cheaply. The equality case(8) is impossible. Therefore H<=4, proving the theorem.

## 6. Complete common-body invoice and the next construction

If each of the two natives introduces a fresh rank-seven body and every retained role receives it, all2(R-2) inactive-role rank-seven idles are paid. Let [x]=x^t, delta=[8]-[7], 0<t<1. The Gaussian price and target satisfy

    Price=2R[7]+2(1+delta),
    Target=sum_i [14+h_i] <=2R[7]+delta H.

Thus

    Price-Target >=2(1-delta)>0.

Any ordinary, precision, layout, ownership or recursive cost worsens this deficit. The theorem excludes all two-native, no-query, common-body inventories in the stated family, for every fixed head dimension and every retained-role count. Source-volume growth from real spectator axes remains in both physical source and target; cancelling a common normalization in this inequality does not waive it.

It does not exclude three native halves, added nonordinary queries, changed body incidence, non-Clifford ordinary encodings, approximate circuits or width-growing source representations outside the fixed group model. The current three-native four-role target(3,3,1,1) is not settled by this theorem. It has a separate favorable optimistic movement invoice but still lacks a source-bound caller and all complete supplier admissions.

## 7. Dependencies and verification status

The universal proof uses the actual square-cross source, finite-algebra tensor separation and ordinary-bimodularity, the old two-half block argument as a credited predecessor, and the admitted independent(3,2) gate. Exact source pins are in DEPENDENCIES.json. The attached diagnostics check the block identities, rank inequalities including singular ordinary blocks, the native two-query factorization and the necessity of endpoint independence. They do not replace the written argument or count as independent review.

Credit @CubeJerry; canonical native/compiler and caller authors; S013 two-half component work; S014 tensor and inverse-native query gates; and S015 Worker B with substantial OpenAI assistance. All five global foundations remain. No new complete kappa.
