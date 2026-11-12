# Sharp retained-difference record counts with raw duties

**Proved field-linear interface; no source word, route saving, supplier, or new kappa.**

This follows the programme's [joint restoration](../joint-hub-restoration/PROOF.md), [single-overwrite loss](../single-overwrite-loss/PROOF.md), and [chronological difference-carrier](../difference-carrier/PROOF.md) proofs. It counts actual retained difference records when specified raw outputs must also be recovered.

## Interface and feasibility

Over any field F, let u be the common inputs and q in F^p the independent raw inputs. The k actual chronological differences satisfy

    T delta = Qq - Hu,    T = I + L,
    Y = Wu + Z delta,

where L is strictly lower triangular and Q is any k-by-p matrix. The real supplied records are n=Nu and r=Rq. Assume H=Lambda W+Gamma N and initially assume [W;N] has independent rows. Targets are Wu and Dq; D must include every claimed raw duty. Additional records have the form K delta. Put G=T-Lambda Z. Then

    Qq = G delta + Lambda Y + Gamma n.                  (1)

Before record counting, the necessary gate is

    row(D) contained in row([Q;R]).                     (2)

If (2) fails, choose s in ker Q intersect ker R with Ds nonzero. Changing q by s with u fixed changes no delta value or observation, even when all differences are retained. No decoder of those data can recover the raw target.

When (2) holds, choose A,B with D=AQ+BR. Let [U,V] have rows spanning all left relations of [Q;R], so UQ+VR=0, and set C=UG. Observations already determine

    C delta = -U Lambda Y - U Gamma n - V r.            (3)

Targets satisfy

    Wu = Y-Z delta,
    Dq = A Lambda Y + A Gamma n + B r + AG delta.       (4)

Set M=[Z;AG]. Neither G nor Q need be invertible.

## Exact criterion and attained record count

Universal recovery from Y,n,r,K delta is equivalent to

    row(M) contained in row([C;K]).                     (5)

Consequently the minimum unrestricted number of complete-field difference records is

    r_min = rank([C;Z;AG]) - rank(C).                   (6)

Here unrestricted means choosing arbitrary linear combinations of actual difference values, without granting physical acquisition or transport.

For sufficiency, solve M=F[C;K], use (3) to obtain C delta, and apply F and (4). To attain (6), select rows of M extending row(C); those rows form K. These records are explicit sums of actual difference carriers.

For necessity, failure of (5) gives t with Ct=Kt=0 and Mt nonzero. Since Ct=0, [Gt;0] is annihilated by every left relation of [Q;R]. Hence there exists s with Qs=Gt and Rs=0. Row independence of [W;N] gives v with Wv=-Zt and Nv=0. Then

    Qs-Hv = Gt + Lambda Zt = Tt,

so the actual difference variation is t. The observations Y,n,r,K delta are unchanged, while the target variations are -Zt and Ds=AGt, at least one nonzero. This excludes arbitrary decoders of the stated linear data. Each additional record contributes at most one dimension modulo row(C); selected extending rows attain the bound.

The answer is independent of A,B: two decompositions of D differ by left relations of [Q;R], so their AG rows differ only by rows in row(C). It is also independent of the relation basis. Tensoring by the identity proves the V-coordinate version for every admitted field volume.

## Full raw recovery: coordinates are optimal in count

For D=I_p, feasibility is rank([Q;R])=p, and (6) becomes

    r_min = k-rank(C).                                 (7)

Indeed I_p=AQ+BR implies [I_k-QA,-QB] is a left relation of [Q;R]. Thus the rows of (I_k-QA)G belong to row(C), and

    T = Lambda Z + QAG + (I_k-QA)G

has every row in row([C;Z;AG]). Since T is invertible, that row space is all F^k.

For full common/raw recovery, arbitrary combinations cannot improve record count over optimally retained difference coordinates. Extend row(C) to F^k using standard coordinate rows e_i. Exactly k-rank(C) suffice. Equivalently, reduce C to row echelon form and retain delta at the nonpivot columns; solve the pivot coordinates from known C delta. This is not a transport-optimality result: valid choices can have different route costs.

For Q=I_k, take U=-R,V=I, obtaining row(C)=row(RG) and r_min=k-rank(RG). With no supplied raw records, k independent original donor inputs require k retained difference dimensions regardless of rank(Z). With all q supplied, the count is nullity(G), possibly much smaller. Single-overwrite losses cannot be added without checking the surviving observations.

## Distinguishing examples

### Chronology and redundant raw caches

Start H=u,Q1=q1,Q2=q2 and execute

    Q1 -= H; H += Q1;
    Q2 -= H; H += Q2.

Then delta1=q1-u, delta2=q2-q1 and Y=q2. Matrices are

    T=[[1,0],[1,1]], Q=I2, Lambda=[[1],[1]],
    Z=[[1,1]], G=[[0,-1],[0,0]].

One retained sum delta1+delta2=q2-u restores u but loses q1. The original-input variation (du,dq1,dq2)=(0,1,0) leaves Y and that sum unchanged. Full recovery with no raw cache needs two difference records. A cache of q2 leaves RG=0 and does not help, since q2 was already Y. A cache of q1 gives rank(RG)=1 and lowers retention to one dimension. Providing both q1,q2 also leaves one record needed for the erased common u. Raw cache count alone is insufficient.

### A partial target favors combinations over coordinates

Take T=Q=I2, Lambda=0, Wu=u, Z=(1,1), no N or R, D=(1,1). Then delta=q and Y=u+q1+q2. One actual retained sum s=delta1+delta2 gives u=Y-s and Dq=s. Neither single coordinate suffices, so coordinate-only retention needs two records. Adding both individual raw outputs to D removes this advantage and requires two records by (7). This partial-output example does not authorize discarding independent inputs whose other raw outputs remain caller duties.

### Repeated signals and missing raw modes

For k=2,p=1, Q=(1,1)^T, T=I2, Lambda=I2, Z=I2 and no R, two independent common fields have been replaced by the same q. G=C=0 and recovery of both common fields and q needs two delta records. Counting one raw input misses the erased common modes.

Conversely Q=(1,1), R empty, D=I2 has an invisible raw direction (1,-1). No amount of delta retention recovers both raw inputs. This fails the feasibility gate before any cost question.

## Dependent common records

Independence of [W;N] cannot simply be omitted. If [J,K0] spans its left relations, observations additionally give

    JZ delta = JY + K0 n.

Provided H=Lambda W+Gamma N still holds, replace C by C_all=[UG;JZ] everywhere. The same criterion, counts and full-recovery simplification then hold. In the necessity proof JZt=0 is exactly the condition for existence of v with [W;N]v=[-Zt;0]. This also makes the result independent of the chosen decomposition of H: changes in Lambda,Gamma contribute only known JZ combinations.

## Physical formation and scope

If the participating actual delta carriers are cochart at a legal collection cut and remain unchanged during formation, each selected K row can be made in a fresh owned field using one ADD per nonzero coefficient. The direct construction uses nnz(K) ADDs and r_min INIT/CLEAR lifetimes, with eventual retirement charged. An optimal coordinate selection can instead retain the corresponding existing carrier versions without mixing ADDs.

These are explicit acquisition premises, not a proved source schedule. The theorem does not establish that carriers meet, that unselected fields may legally be erased, or that records may retire before other outputs and observations are produced. Every value used in (3)-(4) must retain its indicated version. Mixed common/raw histories or further access enlarge the observation interface.

Source guards, off-hub responses, all raw duties, paid reservations, scalar service, ordinary work, peak storage, erasure, precision, compiler and recursive costs remain independent obligations. The field-general theorem does not instantiate a rational source in an incompatible characteristic. Rational rank feasibility supplies neither a division algorithm nor a multiplication bound.

## Open next questions

1. Authenticate Q,H,L,Z,N,R,D at source cuts and form the attaining records on actual routes. A small rank does not supply a channel.
2. Minimize route/lifecycle cost among valid optimal coordinate bases for full recovery; (7) already settles their minimum cardinality.
3. Recheck every partial-target compression after appending all remaining raw caller outputs to D.
4. If H is outside row([W;N]), supply missing common records or use the full observation criterion. The source's 648 non-hub-recoverable payloads do not satisfy the no-N specialization.

Prepared for programme review with substantial OpenAI assistance. Prior joint restoration and chronological difference-carrier work retain their attribution. This result is independently reviewed in review/REVIEW.md. The source-specific physical construction remains open.
