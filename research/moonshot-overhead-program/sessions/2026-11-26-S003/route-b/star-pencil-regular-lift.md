# A regular lift of the joint star pencil, and its full-rate cost

Status: **proved construction and scoped occupancy obstruction; independently accepted by Route A and the lead**. See `../route-a/review-star-pencil-regular-lift.md` and `../lead/review-final-components.md`. This is a distinct joint-delivery attempt, prompted by A's exact numerical endpoint audit. It does not improve AQ or rule out other joint-address executors.

Source: S003 A `separated-numerical-address-audit.md`, SN-A7--SN-A9, pinned to OpenAI math `3344da59991ed94f9ba711217b29c1d760badfa6`. A and B independently observed the common conjugation in Section 1. B's addition is the cyclic regular lift, its actual independent-row obstruction, and the optimistic recurrence invoice.

## 1. The signs admit one common conjugation

A's smallest unresolved middle operator is

    sum_(j=1)^m b_j M_j, M_j=D_j P_j D_j,
    P_j: X_j<->Z_0, Z_j<->X_0,
    D_j(x)=(-1)^(<X_j,Z_j>).

All slots have width f; coefficients depend only on a seed row, not the physical address. Let D_0 be the corresponding auxiliary sign and R_0 exchange X_0,Z_0. Since P_j interchanges D_j and D_0,

    D_j P_j D_j=D_0 P_j D_0.

Let S_j be the ordinary transposition of complete pairs (X_j,Z_j) and (X_0,Z_0), and put U_0=D_0 R_0. Then U_0^2=I and

    M_j=U_0 S_j U_0,
    sum_j b_j M_j=U_0(sum_j b_j S_j)U_0.                (SL1)

Thus the joint core is a weighted star-transposition sum, up to one common monomial change. This removes the query-dependent phases from the problem exactly. The elementary auxiliary exchange remains a paid operation; it is not declared free.

Write V=K^Omega for the physical data space and S_b=sum_j b_j S_j. Treat the m distinguished pairs as leaves, with the auxiliary pair the central slot. Let C cyclically permute the leaves and fix the central slot. With T=S_1, label the cycle so

    S_j=C^(j-1) T C^(-(j-1)).                           (SL2)

## 2. One joint query computes the sum on one embedded input

On m row fibres define

    U=diag(I,C,...,C^(m-1)),
    B=U(I_m tensor T)U^(-1)=diag(S_1,...,S_m).

Embed one arbitrary input x as E_b x=(b_1x,...,b_mx), and let L sum all row fibres. Then

    L B E_b x=S_b x.                                   (SL3)

Algebraically this uses one common central/leaf transposition T, surrounded by two controlled leaf rotations and scalar row operations. Even if the controlled rotations were free, however, SL3 takes one independent physical input into m correlated fibres. It is a partial-output computation, not an identity on m independent inputs.

The rest of this note grants zero cost to the controlled rotations and all scalar mixing. This deliberately optimistic assumption strengthens the rejection of the following full-rate implementation. No fast physical compiler for the controlled rotations is asserted.

## 3. Actual star operators are linearly independent

Assume each complete pair alphabet contains at least two values. Fix an address with a nonzero value in the central slot and zero in all leaves. The m images under S_j are distinct addresses, each with that nonzero value in exactly leaf j. Their basis vectors are independent. Therefore

    sum_j c_j S_j=0 implies every c_j=0                 (SL4)

over every coefficient field. This uses the actual star-permutation operators, not hypothetical independent black-box replacements.

## 4. A sharp independent-row obstruction to scalar compression

Suppose all b_j are nonzero. We want S_b on R arbitrary independent input rows. Consider h uses of the lifted B, combined only by scalar pre/post row mixing and addition:

    sum_(l=1)^h (A_l tensor I) B (B_l tensor I)
                        =I_R tensor S_b,              (SL5)

where A_l has size R-by-m and B_l has size m-by-R. This includes arbitrary scalar input encodings and output decodings for each call, and permits singular maps and zero scratch. It does not include products of lifted calls interleaved with new physical operators.

**Theorem SL.** Every realization (SL5) has h>=R. This bound is sharp. More generally a target sum_j C_j tensor S_j requires h>=max_j rank(C_j), by the identical proof. In particular actual seed-dependent nonzero diagonal signs C_j have rank R and give the same h>=R conclusion.

**Proof.** The coefficient of S_j on the left is

    sum_(l=1)^h (A_l e_j)(e_j^T B_l),

a sum of h rank-one R-by-R matrices. By actual operator independence SL4, it must equal b_j I_R, of rank R. Hence h>=R. Equality is achieved by using one call for each independent input row: B_l writes b_j times that input into fibre j; A_l sums the returned fibres into output row l. QED.

Each lifted call applies T on m full physical fibres. In the original separated-half layout, T is executed as two width-f exchanges; the argument needs no assumption that a pair occupies contiguous physical fields. Relative to the R original independent fibres, its total queried volume is therefore at least

    h m/R >= m.                                        (SL6)

For R=m, exposing the lifted row index from existing independent leading rows avoids adding initial payload, but h>=m still forces m lifted calls. Expanding to m copies of every independent input and processing all copies at once gives the same m-fold call volume and an m-dependent payload coefficient. Serializing those copies restores the space cap but retains the time price. The full-rate loss cannot be removed merely by calling the controlled operator once on a larger batch.

If only r coefficients b_j are nonzero, the same construction restricted to those r leaves has price at least r. The actual Newton seed coefficients motivating the all-query core are nonzero signs; a sparse special case would need its own complete predictor budget.

## 5. Optimistic recurrence and the remaining escape

Grant the two controlled rotations zero cost, all row work zero cost and an absolute payload cap via serialization. One central/leaf pair swap still has width proportional to f. Thus the full-rate regular-lift supplier has normalized call mass at least m on width-f children. Inserting it into each degree-Theta(sqrt(m)) numerical predictor does not remove the distinct-query factor identified by SN-A. The complete optimistic local bill is at least that of separately applying m width-f permutations, before any actual controlled-rotation cost is added.

For a regular exact-width recursion f>=e/(C m), the corresponding positive invoice satisfies B(e)>=m B(f). For AI-style adaptive logarithmic descent this gives B(e)>=e/(log e)^C1; fixed large arities give a fixed exponent above one half. These are invoices for this proposed realization, not runtime lower bounds for the joint star sum. They are already incompatible with the desired replacement by a subpower-m multiple of a width-e interchange.

The useful next target is now precise: apply the weighted star sum directly to all independent physical data, without evaluating its m diagonal lifted blocks separately and without recovering full rate only through scalar compression of SL3. Products with genuinely useful group-algebra cancellation, a direct orbit transform with fully priced regrouping, or another joint-address construction are outside SL5. This note supplies no fast implementation of them.

`verify_star_pencil_lift.py` checks the common signed conjugation, actual operator independence, the lifted partial-output identity, failure of full-rate single-call scalar compression, and a matching R-call construction. Finite cases do not certify a tape-machine runtime or a general lower bound.

Prepared for Jerry Chen (@CubeJerry), with substantial OpenAI AI assistance. A's endpoint identity and the independently convergent common conjugation are credited explicitly; the full-rate lift audit is B's protected discovery wave.
