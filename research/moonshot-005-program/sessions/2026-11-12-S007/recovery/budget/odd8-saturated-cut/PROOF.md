# An eight-field saturated spatial cut

## Result and exact scope

Keep the pinned native's common MOVE chart endpoints and multiplicities, the 400 raw carriers' initial and final charts, and the 112 packet legs of the direct first-family comparison: 104 hub-to-first-Y facet legs and eight unhosted facet-to-hub returns. All payloads, local operations, and chronology may be changed. In this interface the complete common/private target needs eight more inward fields than the funded monotone paths provide. At exponent 199/200, arbitrary nested raw detours cannot supply this capacity for less than eight additional moment units. The comparison has less than 6.293071043777141379854 units left.

This permits common-dependent dirty payloads, mixed raw carriers, feedback, and joint decoding of all inside observations. No fixed-original-history premise is used. It retains the stated transport skeleton; changing the common MOVE endpoints or the reserved packet endpoints requires a new count. It is not a global native or kappa impossibility result.

## Source and target convention

Source: `research/shared-wire-split-composition/data/final.json.gz`, archive SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.

Let u denote the 1,480 independent common input fields in normalized coefficient coordinates. The 400 main roles also have independent raw inputs v_j, initially cocharted with u_j. The change q_j=v_j-u_j is invertible and local. At the endpoints, (u'_j,v'_j) can similarly be replaced locally by (u'_j,q'_j=v'_j-u'_j). The target therefore is the direct sum u'=T u and q'=T_M q, where T_M is T restricted to the 400 main roles. Its blocks are:

- Hosted first pair (x,y=x+112): x'=x and y'=x+y.
- Unhosted first pair: x'=x-y and y'=(x+y)/2.
- Hosted reverse pair (X2,Y2): X2'=X2-Y2 and Y2'=Y2.
- Other common helpers: identity.

The checker freshly propagates all 1,300 inside public-output adjoints backward through every native instruction, on all 1,480 common inputs, and compares to these target rows. Invertible chart coordinate maps do not change conditional rank. If one field has coefficient dimension B, multiply both target ranks and field capacities below by B.

## Cut geometry

The eight chosen hosted ports have binary dot product one for all 64 ordered pairs, including the diagonal.

| Port index | Binary port as integer | First X | X2 | Y2 |
|---:|---:|---:|---:|---:|
| 24 | 38 | 27 | 799 | 907 |
| 103 | 191 | 111 | 881 | 987 |
| 0 | 11 | 0 | 772 | 882 |
| 32 | 146 | 36 | 808 | 915 |
| 97 | 367 | 105 | 875 | 981 |
| 72 | 502 | 79 | 849 | 955 |
| 37 | 322 | 42 | 814 | 919 |
| 86 | 475 | 94 | 864 | 970 |

Define D as every binary chart subspace containing at least one chosen port. This definition includes arbitrary newly introduced charts; it is not restricted to source chart IDs. D is upward closed. The source has 377 chart IDs in D. Hub 127 is inside; zero chart 3 is outside. A selected port's final facet is perpendicular to that port, so it contains no selected port and is outside. Exact source enumeration checks that every other active first-Y facet is inside. All eight unhosted return facets are consequently inside.

## Conditional target rank and funded capacity

Condition on all common and private initial inputs inside D, and grant joint access to every desired final output inside D.

| Block | Inside initial fields | Inside final fields | Rank on outside inputs |
|---|---:|---:|---:|
| Common | 53 | 1,300 | 1,255 |
| Private | 16 | 384 | 376 |
| Direct sum | 69 | 1,684 | 1,631 |

The common and private outside inputs are independent, so these ranks add even if a proposed implementation mixes their payloads. Exact rational elimination certifies both ranks. `RESULT.json` contains the inside input/output sets, every restricted matrix row, and input/output minor pivots with determinant. Processing every row also verifies the upper ranks.

After conditioning on inside initial inputs, every inside state is a linear function of the inward communication transcript. Each inward MOVE carries one field, so the conditional output rank is bounded by the number of inward MOVEs. Arbitrary local operations, initialization, erasure, outward communication, and feedback cannot evade this inductive rank bound.

The common skeleton has exactly 1,255 inward MOVEs: 1,247 public and eight owned. There are eight outward owned MOVEs. Its common target alone saturates the inward capacity. This does not earmark those slots for particular payloads: all may carry mixed common/private data, and the full target still has rank 1,631.

Of the 400 raw carriers, 16 start and finish inside, 16 start and finish outside, and 368 start outside and finish inside. Every raw endpoint pair is nested with dimension increase eight. A monotone path can enter an upward-closed set only once, so every monotone replan has exactly 368 inward entries, regardless of its intermediate stops or payloads.

The 104 reserved forward legs go from the hub to first-Y facets. Ninety-six remain inside and eight leave; none enters. All eight reserved unhosted returns remain inside. Thus the 112 reserved legs give zero inward capacity even if arbitrarily recoded. Funded capacity is 1,255+368=1,623, against required rank 1,631. Eight additional inward fields are necessary.

Negative controls authenticate the cause of the gap. Deleting all 96 private hosted-reverse coefficients lowers private rank to 368 and removes the deficit. Deleting just the first selected coefficient lowers private rank to 375 and leaves deficit seven. The checker also verifies eight rank-one selected-Y2-facet-to-hub legs that would fill this cut's capacity deficit; this is not a construction completing all 96 duties.

## Arbitrary nested raw detours

Every new raw chart may be any binary subspace in the same nine-dimensional ambient space. Consider an arbitrary nested-MOVE raw path with the same endpoints. Let d be its total descending rank. Its total ascending rank is 8+d. Let k be its inward entries beyond the zero or one forced by its endpoints. Since D is upward closed, every outward crossing is descending. Inward minus outward crossings equals the endpoint indicator, so k is exactly the outward crossing count and k<=d.

Set t=199/200 and c=9^(t-1). If d=0, subadditivity gives route cost at least 8^t. If d>=1, each MOVE rank is between one and nine, so r^t>=c*r and the total route cost is at least c*(8+2d). Exact integer-root bounds verify

10*c-8^t-1 > 0.9734867904000519693307496,

and 2*c-1 > 0.

For every integer d>=1,

c*(8+2d)-8^t-d = (10*c-8^t-1)+(d-1)*(2*c-1) > 0.

Thus each route costs at least 8^t+k. This covers multi-rank up/down excursions, not only unit steps. If K extra inward crossings are supplied by raw detours, their cost beyond the direct-raw baseline is at least K. If m other newly paid inward MOVEs are used, the cut requires K+m>=8 and they cost at least m. Total extra moment is therefore at least eight. Additional carrier branches or copied fields must have their cross-chart MOVEs included in m; they are not free paths.

## Retained H4 invoice

Invoice: `research/moonshot-005-program/results/eight-packet-budget-and-reverse/INVOICE-SOURCE.json`, SHA256 `b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248`.

The profile has 18 native occurrences. Retain every other source transport reservation. Replace only the raw histogram {1:990,2:360,3:105,4:112,5:133,6:8,7:2} by 400 rank-eight legs per native; both have rank mass 3,200. Add the 104 rank-one deliveries and eight rank-one returns. The resulting full paid count is 130,860.

Integer 200th roots at denominator 10^24 enclose the per-native remaining moment between

6.2930710437771413798499171111111111111111111111111

and

6.293071043777141379853578.

The eight-unit necessary cost exceeds this margin by more than 1.706928956222858620146422. No floating-point sign decision is used. Ordinary operations may be granted for this obstruction; charging them cannot repair its transport-moment failure. The H4 conclusion applies to substitution of this native interface into the retained profile, not unrestricted joint coding across outer template invocations.

## Reproduction

Run `python check.py --repo /path/to/integer-mult-bounds`. The standard-library checker uses explicit exceptions and remains effective under `python -O`. Its JSON output is deterministic. It checks the full source adjoints; all binary memberships and 64 pairings; all 400 endpoint gaps; every common and reserved crossing; both exact conditional ranks; the two target mutations; the cut-filling legs; the complete moment profile; and both detour inequalities.

## A universal edge limits weighting of this cut family

All 104 active port vectors, including all 96 hosted ports, have odd Hamming parity. Let E be the even-parity hyperplane, with normal 511 and binary basis `[257,258,260,264,272,288,320,384]`. E contains no active port. For every nonempty upward-closed cut generated by any collection of active port lines, E is outside and the full hub is inside. Therefore the single nested rank-one MOVE E to hub enters every such cut.

Suppose a family of independently verified eight-deficit cuts is assigned nonnegative weights w_C, normalized so that every newly paid rank-r MOVE crosses weighted cuts of total weight at most r^(199/200). This normalization must apply to E to hub, even if E was not a source chart. Consequently sum_C w_C <= 1 and the weighted deficit 8*sum_C w_C <= 8. Enumerating more eight-deficit odd-port cuts cannot raise this unrestricted spatial-cut dual above eight.

This is a limitation of the lower-bound method. It does not give useful independent payloads at E and does not make an eight-call full algorithm attainable. A stronger bound needs to price acquisition of those payloads, use time-dependent observations, or introduce other cut geometry. Restricting the dual to source chart pairs would evade the universal edge only by imposing that additional architectural restriction, which is not used here.
