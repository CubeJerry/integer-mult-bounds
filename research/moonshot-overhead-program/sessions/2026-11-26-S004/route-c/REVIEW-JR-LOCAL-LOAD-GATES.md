# Independent review: joint-inequality local loads

Reviewer: S004 Route C. Verdict: **accepted**, with the stated cover,
partition and literature-parameter distinctions preserved. This neither
proves nor refutes JR and gives no multiplication-envelope improvement.

Read the lead's `jr-local-load-gates.md` in full. JL1 is exactly the
incidence factorization of a partition, including arbitrarily correlated
sides. Over Q the adjacency tensor has full rank q^k, so an exact weighted
rank-one expansion needs at least q^k nonzero summands. This lower bound
is on total summands and cannot be reinterpreted as the local load.

For every valid rectangle, its coordinate projections are disjoint.
Thus |A||B|<=product_i |pi_i A||pi_i B|<=(q^2/4)^k, even when A and B
are not products. Counting covered edges, applying this capacity to each
rectangle, then Cauchy--Schwarz to the two incidence totals proves JL2
exactly. Its first step uses only coverage, so the claim correctly holds
for overlapping covers too.

In the crown restriction, S_a and T_a are disjoint but every cross pair
intersects. For two different permutation events, chosen intersection
elements u in S_a intersect T_b and v in S_b intersect T_a are distinct
because S_a intersect T_a is empty. The two events impose opposite
orders on u and v. They are therefore disjoint, giving the set-pairs
inequality and JL3. Binomial monotonicity in both size arguments is the
correct step for unequal side loads. The common-load logarithmic bound
and exclusion of an exponential base c<2 follow as stated.

The opposing-star partition at k=2 assigns each edge to (y_1,x_2)
uniquely and has side load q-1. At q=4 the cover lower bound rounds
9/4 up to three, proving global load optimality; rank gives optimal
rectangle count sixteen for an exact partition. The same check at q=3
gives load two. Product constructions multiply incidences but do not
remove the growing-alphabet logarithm.

## Primary-source scope check

Independently opened Block et al., ITC 2021, DOI
10.4230/LIPIcs.ITC.2021.16, and read the relevant definition, Theorem 8,
Claims 16--18, the inequality construction in Section 5.4, and the
embedding discussion in Section 7. Its subgraphs are disjoint unions
of bicliques. A partition into d such subgraphs yields local load at
most d, and its inequality result plus tensor-product upper bound gives
the already available (log2 q)^k bound. It does not prove JR. No reverse
transfer of a global partition-count lower bound to a local membership
lower bound is justified here, and none is asserted.

Also independently opened Pinto's 2014 paper, read the local definitions
and Section 4 crown argument. The note uses that source for established
context while supplying its actual inequalities directly. No novelty claim
or inference from a generic cover/partition gap to JR is present.

Primary URLs:

- https://drops.dagstuhl.de/storage/00lipics/lipics-vol199-itc2021/LIPIcs.ITC.2021.16/LIPIcs.ITC.2021.16.pdf
- https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i1p19/pdf/

This was a written proof and primary-source review. No new full-machine,
asymptotic solver, or formal-kernel verification is implied.
