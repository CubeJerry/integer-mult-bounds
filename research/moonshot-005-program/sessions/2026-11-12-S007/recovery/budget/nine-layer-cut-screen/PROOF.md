# Exact ceiling for the nine-layer spatial-cut family

## Conclusion

There are exactly 369 hosted eight-port sets with every binary dot product equal to one. For each set S, all nine cuts

D_k(S) = D_min(S) union {C in D_max(S): dim(C) >= k}, for k=1,...,9,

have an exact eight-field deficit. However, no nonnegative weighting of these 3,321 cuts, normalized against all allowed nested binary-chart MOVEs, proves an additional moment lower bound of 39. An explicit 53-edge fractional cover bounds the dual objective above by

26.361114 + 5.608709 * 2^(199/200),

which is strictly less than 39. The inherited optimistic E8 profile retains more than 39 moment units after charging its eight coupled returns, so this cut family alone cannot close that remaining gap.

This is a limitation of the lower-bound method. The fractional edge cover is not an implementation, an achievable transport invoice, or a supply of encoded payloads at its endpoints. It does not provide acquisition, chronological access, decoding, or common-output restoration. In particular many chart pairs are legitimate possible new calls despite having no native payload at those charts.

## Source and complete family

The pinned archive is `research/shared-wire-split-composition/data/final.json.gz`, SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.

The checker performs exhaustive bitset Bron–Kerbosch enumeration on the 96 hosted port vectors. Adjacency means odd binary dot product. The maximal-clique size census is:

| Size | Number |
|---:|---:|
| 4 | 67 |
| 5 | 229 |
| 6 | 598 |
| 7 | 672 |
| 8 | 369 |

There is no larger clique. Thus the 369 listed size-eight maximal cliques are the entire hosted eight-frame family. For each such S, the checker also tests that an active port has odd dot product with every member of S if and only if that active port belongs to S. This includes the eight unhosted active ports; none is an additional common odd neighbor.

For any binary chart subspace C, define:

- D_min(S): C contains at least one selected port.
- D_max(S): C is not contained in any selected port's perpendicular facet.

Both definitions apply to arbitrary new charts, not only to native chart IDs. Both sets are upward closed, and D_min is contained in D_max because selected ports pair oddly. Every D_k above is therefore upward closed and lies between those two extremes.

The selected first-X and X2 input lines are inside every D_k. Every other active X line is outside. The selected first-Y and Y2 final facets are outside, and every other active Y facet is inside. The zero chart is outside, the full hub is inside. Thus the 400 raw endpoints have the same membership as in the independently reviewed single-cut package: 16 inside-to-inside, 16 outside-to-outside, and 368 outside-to-inside.

## Exact deficits

Use independent common inputs u and private inputs q=v-u. The initial and final coordinate changes are local because each raw field is cocharted with its corresponding common field. The target is the direct sum of the native common target T and its restriction to the 400 private main roles.

The checker freshly authenticates the full common T, on all 1,480 outputs and all 1,480 inputs. Its nonidentity blocks are the 96 hosted first shears, eight unhosted coupled pairs, and 96 hosted reverse shears. All other common roles are identities. It also verifies that all public MOVEs ascend and all raw endpoints have net dimension increase eight.

Write Delta for the number of inside common final fields minus the number of inside common initial fields. Identity helper roles contribute their endpoint growth to the conditional rank. Every nonselected two-field main block has both its initial inputs outside and both its final outputs inside, so it contributes two dimensions. Each selected hosted first pair contributes zero, and each selected hosted reverse pair contributes one extra dimension beyond its zero endpoint growth. Consequently the conditional common target rank is Delta+8. The private conditional rank is 368+8=376.

Public native paths are monotone, so their inward MOVE count is exactly Delta. The checker counts exactly eight inward owned MOVEs for every one of the 3,321 cuts. Every common cut is therefore saturated. The 400 monotone raw paths add 368 inward fields, leaving total deficit eight. The 104 direct first-Y packet legs and eight unhosted facet-to-hub legs add no inward capacity; the eight E8 hub-to-zero legs are outward and add none either.

Arbitrary nested raw detours are also compatible with a normalized weighted cut bound. A raw path has ascending rank sum 8+d, where d is its descending rank sum. By subadditivity at 0<t<=1, its ascending moment is at least (8+d)^t>=8^t. Its moment above the direct baseline therefore pays for all its descending MOVEs. For upward cuts, weighted inward crossings beyond the endpoint net equal weighted outward crossings. If every edge's weighted crossing load is at most r^t, descending transport pays for those extra crossings. This refinement was supplied by the parent/root analysis; it does not alter the already frozen valid single-cut proof.

## The exact cover and its dual implication

`COVER.json` lists 53 strictly nested chart pairs. Forty-five have rank one and eight have rank two. Each has a positive integer coefficient numerator at common denominator 1,000,000. These coefficients were rounded upward from a numerical candidate, then checked entirely with integers.

For every one of the 3,321 cuts, the sum of coefficients of cover edges entering that cut is at least eight. The sum of rank-one coefficients is exactly 26.361114; the sum of rank-two coefficients is exactly 5.608709. Integer 200th-root enclosures at denominator 10^24 certify the stated moment ceiling. No floating-point comparison is used by the frozen checker.

To see the implication, let w_C be any nonnegative cut weights, and suppose every possible new nested MOVE e of rank r_e satisfies

sum_{C entered by e} w_C <= r_e^t.

The 53 cover edges are among those allowed edges. Multiply each of their inequalities by its cover coefficient lambda_e and sum. Since each cut receives cover at least eight,

8 * sum_C w_C <= sum_e lambda_e * r_e^t.

The right side is the exact displayed value below 39. This proves the ceiling for arbitrary independent weights on all 3,321 cuts, not only uniform frame or layer weights. Allowing additional binary charts only adds normalization constraints and cannot weaken this ceiling.

## Negative control and next boundary

The checker removes a positively weighted cover edge and exhibits a cut whose residual cover falls below eight. It reports that failed coverage as a negative control. Normal and optimized Python runs use explicit exceptions and produce identical deterministic receipts.

The next untested family consists of all upward sets D with D_min(S) contained in D and D contained in D_max(S), without a dimension-threshold restriction. Their source conditional deficit is 16 minus the inward native-owned count. A proposed paid-edge cover can be separated against these cuts by a finite minimum-cut problem: reverse-containment arcs enforce upward closure, selected facets are forced outside, selected lines inside, and capacities are native owned upward slots plus the proposed new edges. This is a different family. The 53-edge ceiling here is not claimed to cover all such cuts.
