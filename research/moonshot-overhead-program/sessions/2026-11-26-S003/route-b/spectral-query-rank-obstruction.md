# Spectral identities do not evade separately billed query rank

Status: **proved extension; independent review requested**. The telescoping insight was proposed by the session lead after B's formal determinant-degree theorem. B independently checked it and derives the finite-spectrum, approximate-output and linear-program versions below. This replaces the earlier suggestion that dropping a formal identity alone might escape the separate-query invoice.

This is an algebraic query-budget obstruction. It is not a lower bound for physical interchangers that jointly mix address coordinates, and not a lower bound for multiplication. Source context and pins are those of `direct-rank-routing-obstruction.md`.

## 1. Product differences need no formal identity or invertibility

Let K be a field, Omega a finite subset of K, and

    P(q)=F_l(q)...F_1(q),
    F_t(q)=A_(t,0)+sum_j sum_h g_h(q_j) A_(t,j,h),       (SQ1)

where all matrices are W-by-W and g_h are arbitrary scalar functions on Omega. The coefficients are fixed, independent of q. For the retained order-three pencils h=1,2 and g_h(z)=z^h. Define the declared separate-query rank price for coordinate j by

    R_j=sum_(t,h)rank_K(A_(t,j,h)).                     (SQ2)

If q,q' differ only at j, telescoping gives

    P(q')-P(q)=sum_t F_l(q')...F_(t+1)(q')
                 [F_t(q')-F_t(q)]F_(t-1)(q)...F_1(q).

Ranks do not increase under left/right multiplication, and rank is subadditive. Thus

    rank(P(q')-P(q))<=R_j.                              (SQ3)

Singular factors, cancellations, arbitrary stage count and finite-spectrum-only correctness are all allowed.

**Theorem SQ-E.** If P(q)=p(q)I_W for every q in Omega^m, and coordinate j is essential for p on that finite product, then R_j>=W. If all m coordinates are essential, sum_j R_j>=mW.

Indeed choose one pair differing only at j with p(q')!=p(q). The output difference is a nonzero scalar times the identity, hence has rank W. No degree or polynomial-extension argument occurs.

The power-two count predictor has every coordinate essential after the shifted Boolean specialization in DR5. Its values are gamma omega^((c-u) mod T). If counts c=0 and c=1 happen to give the same value, the wrap is at that step and counts c=1 and c=2 give different values. For m>=2 either comparison can be realized while varying any designated coordinate and fixing all others. For the admissible bounded case m=1 the condition D=T-1<=m forces T=2, and its two values differ directly. Hence the finite-only version of that scalar predictor still pays mW in this invoice.

## 2. Approximation in rank and the actual shifted predictor

Suppose instead that

    rank(P(q)-p(q)I_W)<=epsilon W                       (SQ4)

for all q, with 0<=epsilon<1/2. For an essential-coordinate pair q,q', write E(q)=P(q)-p(q)I. The rank inequality applied to their difference gives

    rank(P(q')-P(q))>=W-rank E(q)-rank E(q')
                            >=(1-2epsilon)W.           (SQ5)

Combining with SQ3 and summing gives

    sum_j R_j>=(1-2epsilon)mW.                          (SQ6)

This also holds for an average-rank error promise when the target is p(q)=product_j q_j and Omega consists of at least two distinct nonzero scalars. Choose q uniformly and q_j' uniformly among other symbols. Both marginals are uniform, and every target difference is nonzero. Averaging SQ5 yields the same lower bound from mean_q rank E(q)<=epsilon W.

The structured-shift block predictor is within rank W/32 of product_j q_j times the identity at every allowed tuple: at most W/32 rows are exceptional and each scalar block occupies its full independent module. Thus any separate-query rank execution of that completed matrix predictor has price at least (15/16)mW. This uses the actual matrix error rank, not a claim that each scalar shifted block succeeds everywhere.

## 3. Arbitrary linear query programs, including temporary rows

The same argument applies beyond square affine factorizations. Consider a fixed linear straight-line program on input K^W. It may copy, add, discard, retain and mix arbitrarily many temporary registers by q-independent K-linear maps. Its only q-dependent primitives multiply a designated block of r registers by a scalar function of one coordinate q_j. Charge that primitive r units to query j. Initial injection and final projection may be rectangular. The executed instruction sequence is fixed independently of q.

Pad the varying register sets to one common state space. Each primitive's matrix changes by rank at most r when q_j changes; q-independent primitives do not change. Apply the same telescoping identity, then the fixed input injection and output projection. If the output map is p(q)I_W, the total charge to every essential coordinate is at least W. The rank-approximation version gives (1-2epsilon)W under SQ4. Thus free scalar mixing, zero-initialized scratch and a partial-output implementation alone do not evade this algebraic query bound.

What fails for the geometric executor is precisely the restriction that all free processing is q-independent scalar-row mixing. Its endpoint maps jointly alter physical addresses and need not preserve an individual joint spectral fibre. The argument therefore does not assign it the separate-query price. A direct joint spectral diagonal table likewise lies outside this model unless its physical preparation is separately reduced to these allowed primitives.

## 4. Corrected discovery boundary and complete optimistic recurrence

The earlier counterexample p=1+sum_j(q_j^3-1) equals one on the order-three spectrum. Its constant implementation has no essential coordinate there. It correctly shows that a formal determinant-degree hypothesis cannot be inferred from equality on a finite set, but it does not bypass SQ-E or SQ6. This distinction closes the proposed spectral-only separate-rank escape.

Even granting zero scalar setup/time and absolute payload space, the retained predictor therefore has normalized separate-query mass at least (15/16)m. On a regular width split f>=e/(C m), the optimistic positive invoice is

    B(e)>=(15/16)m B(f).                                (SQ7)

For AI's logarithmically geometric adaptive path, the number of levels is O(log log e). Multiplying the inequalities and using product m>=e/(C^r e_base) gives B(e)>=e/(log e)^C1, for an absolute C1. This is larger than the admitted sqrt(e) subexponential-log invoice. Adding scalar work cannot repair it.

A productive next mechanism must change the physical sharing of queries or another explicit premise: jointly delivered address operations; useful nonlinear intermediate algebra; or a decomposition whose inter-level state is not governed by this linear scalar-query program. This note does not claim that any of those mechanisms succeeds. Finite-spectrum-only correctness is no longer considered an escape by itself.

`verify_spectral_query_rank.py` checks exact F4 telescoping ranks, singular/rectangular programs, rank-error comparisons and the essential-coordinate scope control. The finite tests supplement the rank proof and do not lower-bound a general tape machine.

Prepared for Jerry Chen (@CubeJerry), with substantial OpenAI AI assistance. The lead supplied the key telescoping observation; B independently verified, scoped and extended it to average rank error and arbitrary linear query programs.
