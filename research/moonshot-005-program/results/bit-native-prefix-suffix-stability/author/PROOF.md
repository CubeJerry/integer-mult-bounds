# Both fixed halves separately force return rank at least 35,109

At bank b = 3,840, fixing the genuine source, H and D words forces every full-foreign fitting to have return rank at least 35,109, even after replacing every K and F. Independently, fixing D and the checked K/F words gives the same lower bound after replacing every source and H word. The second result holds for all four combinations of spread and mixed K with RS and minimum-storage F. At return rank 34,688, retaining both ends requires at least 26 changed actual D nodes, thirteen in each of two disjoint sets. The same conclusion holds at 34,694.

Use the native nine-bank rectangle stability certificate. Write the return rank as 9b+h. There are independent invertible input and output gauges V_j,U_i with U_i B_ij V_j = I+E_ij and rank E_ij at most c_ij h. The weighted rectangle certificate fixes c_ij and assumes every proper foreign block is invertible. The physical bank has eight real copies. The gauges can mix all its sectors and copies.

## Fixed D, K and F

Take receivers u=0,v=14 and donors J=(1,3,5,7,10,11,12,47). The sixteen weights sum to seven, grouped by donor as 0,1,1,1,1,1,1,1. There are 120 pairs (j,d) where d receives j and serves both receivers, on 45 distinct actual D nodes. For each i,j the 60 visible D outputs supply exactly 480 body fields. From those outputs to i let R_ij be the existing square K/F map. The invertible D restriction C_ijd sends eight genuine H inputs from j to eight outputs at i. In common (j,d) order vertically stack

    A_i = stack C_ijd^(-1) pi_d R_ij^(-1).

Each A_i is 960 by 480. The two ranks are 480,480 and their column concatenation has rank 960 in all four terminal choices.

For the original one-donor experiment V_j x, both receivers recover the same actual packet delivered by the new prefix from j to d. The j groups of A_i U_i^(-1)(I+E_ij) thus agree. The packet may be any function of the input. On stacking, the rank of the difference of A_u U_u^(-1) and A_v U_v^(-1) is at most the sixteen error ranks' sum. Each error is counted once across all its D entries. The difference has rank at least the dimension of the union of the two column spaces minus the smaller individual rank, even after the independent gauges. Eight copies yield 3,840 <= 7h and h >= 549. Restriction of scalars gives the same inequality for linear bit gauges in six-bit field-record units.

## Fixed source, H and D

Take donors 1,8 at the eight receivers 0,3,5,6,16,17,18,19. Their weights sum to seven. Let M_ij send the original source to all sixty actual D exits seen by i. On the d-only exit coordinate let W_ijd = M_ij^(-1) inc_d. Stack W_ijd transposed by (i,d) for each donor. The two 960-by-480 matrices have ranks 480 and 480 and joint rank 960.

For either donor, the genuine source variation W_ijd z supplies exactly z on d and zero on every other D output visible to i. Both downstream experiments see the same tuple of exits. Thus (I+E_ij)V_j^(-1) W_ijd agrees across the two donors. Transpose and group by receiver. Each of the sixteen error ranks is counted once. The dimension bound yields h >= 549 independent of the replacement K and F.

## Changes confined to middle words

Omitting a label deletes eight joint body rows. Since the joint matrix is row-independent, every subset remains independent. The individual ranks remain at most 480. On surviving, unchanged d the equality persists when other D words change. In the suffix proof R_ij^(-1) still recovers the actual exits independently of how they were formed. In the prefix proof the fixed S/H gives zero inputs on the other visible D charts, so any changed zero-response contributes the same baseline to the two experiments. At h=128 at least ceil((3840-7h)/64)=46 labels must touch changed D words. The same count holds at h=134. In both constructions the twelve highest chart multiplicities cover fewer than 46 labels. The 45 prefix charts and 45 suffix charts are disjoint. Thus changing only middle words must modify at least 26 real charts. This counts physical word changes without charging movement.

The author and second forward replay use the earlier genuine H, D, K, F and weighted-rectangle data. The conclusion constrains refinements of those words, with simultaneous physical changes at both ends still open. Credit @CubeJerry, the weighted rectangle and native H/D/K/F programmes, and OpenAI assistance.

## Singular-contact extension

Only the 221 normalized tree blocks need be invertible in the preceding rank bounds. All other foreign actions may be singular. If the tree blocks instead have corank at most delta, the rectangle proof gives each contacted error rank at most c*h+(2c+1)*delta. Both explicit sixteen-edge witnesses therefore give 3,840 <= 7h+30delta. With the checked prefix or suffix, attaining h=128 requires an actual tree-block corank of at least 99. At h=134 it requires corank at least 97. A prescribed invertible foreign target has delta=0.

## Census and exact counting certificate

On each of the 1,108 true A2 planes with at least two native points, choose one pair of sources and one pair of receivers independently. For each choice use eight opposite native roles minimizing the sum of the sixteen rectangle weights. Compute the two isolated inverse stacks separately in the marked 96- and unmarked 384-body sectors. If their sector ranks are r0,r1,joint, put g equal to the sum over both sectors of joint−min(r0,r1). The triangle inequality above gives

    sum_d m_d x_d >= ceil((8g - c*h)/64),

where c is the summed weight, m_d counts selected labels through d and x_d is one when its middle word changes. Removing packets lowers joint rank by at most eight body fields per omitted label. This applies also at the few planes whose joint stacks have one-dimensional dependencies. Prefix constraints allow every K/F word to change freely. Suffix constraints here use the original spread K and RS F, and allow every source/H to change freely.

For h=128 the resulting lower bounds are 712 real D changes with S/H fixed, 707 with spread K/RS F fixed, and 764 when both ends are fixed. The compact chart data contains all 2,216 true sectional rank records and labelled multiplicities. The checker rebuilds each from the native GF(64) matrices and weighted rectangles. Every numerical chart-change bound uses only exact integer arithmetic. For a cap k, minimize the sum of min(m_d,k) over subsets whose original weight reaches the required threshold t. A one-dimensional integer dynamic program gives its minimum t_k. Each actual changed set satisfies the truncated inequality with that right side. Multiply these inequalities by the nonnegative integer weights in COUNT.json. If a physical d receives over the common denominator M in total coefficient, subtract the excess from the right-hand side, using x_d<=1. Every remaining column has coefficient at most M. Divide by M, round up, and obtain the claimed number of distinct real D words. The optimization used to find integer weights is unnecessary for verification.

## Simultaneous changes at source and receiver stars

For a prefix witness only the two named donor stars must implement their old map into the physical H-to-D rows, up to an arbitrary invertible local donor coordinate change. For a suffix witness only the two named receiving stars must implement their old K-to-F map from the D exits, up to an arbitrary invertible local receiving coordinate change. The coordinate changes are absorbed in the rectangle gauges. All remaining stars on both sides may operate differently. This observation makes the pair bounds apply to simultaneous alterations.

In the spread-K/RS-F case, repeat the exact rank test on all 2,870 unordered nonorthogonal native pairs at each end. Each pair lies in a unique native A2 plane. A pair without sufficient changes to its incident D words cannot retain both original stars. Thus if too few D nodes are modified globally, the original stars surviving at each end form a set of mutually orthogonal real roots. Their nonzero vectors lie in eight-dimensional space, so there are at most eight. The resulting requirement is simultaneous, at least 103 source/H donor stars and at least 103 K/F receiving stars must genuinely change beyond invertible endpoint gauges. At h=128 or 134 every pair requires at least five D changes to escape its constraint, so four or fewer global D replacements leave the entire pair conflict graph intact. The arithmetic thresholds occur in PAIR-RESULT.json. The eight coordinate roots themselves show the geometric upper bound of eight is sharp. A physical H or K word can affect more than one star, so the count refers to actual star transfer functions, not changed gate counts.

Each original source or facet belongs to one star, and each native H or K plane has at most three proper native members. The 103-star requirement at each end therefore implies at least 35 distinct changed source/H operations and at least 35 changed K/F operations under the same bound on middle replacements. The 31-centre packed source uses 78 donor stars and leaves another 33 in the original form. Reaching the near-rank boundary under that middle-change bound requires genuine changes to at least 25 of those 33 additional donor stars, even if all 78 packed stars and every receiving word are free.
