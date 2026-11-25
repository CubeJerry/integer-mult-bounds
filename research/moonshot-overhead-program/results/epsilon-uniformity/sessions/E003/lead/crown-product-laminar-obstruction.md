# Crown products obstruct a single ordering or laminar endpoint hierarchy

Status: **proved scoped graph theorem; independent review pending**.
This closes one concrete approach to S004's joint-rectangle hypothesis
JR. It does not disprove JR for arbitrary rectangles and does not
lower-bound multiplication time.

## 1. Graph and literature lead

Let C(q,k) have left and right copies of [q]^k, with x adjacent to y
when x_i differs from y_i for every coordinate. Write N=q^k and
d=(q-1)^k. Here q>=2 and k>=1 are arbitrary integers.

Cardinal, McCarty and Yuditsky, *Biclique decompositions from Welzl
orders*, arXiv:2606.09785v2 (14 October 2026), Lemma 2.1, constructs
a locally sparse exact partition from an ordering in which every
neighborhood has few intervals. Their Section 2 also relates total
interval counts to neighborhood symmetric differences. The lead read
the introduction and complete Section 2 argument, not all applications.
Primary source: https://arxiv.org/pdf/2606.09785 .

The following exact calculation for C(q,k) shows why that route cannot
supply JR's exp(O(k)) poly(log q) maximum-incidence target. A stronger
laminar-family obstruction follows by a separate tree calculation.

## 2. Exact minimum total interval count

For right words y,z at Hamming distance h,

    |N(y) intersect N(z)|=(q-2)^h (q-1)^(k-h),
    |N(y) symmetric_difference N(z)|
      =2[(q-1)^k-(q-2)^h(q-1)^(k-h)].                (LP1)

The notation N(y) means the left neighborhood; cardinalities are the
same on both sides. For distinct words h>=1, the last quantity is at
least 2(q-1)^(k-1). This includes q=2, with 0^h=0.

Fix any ordering y_1,...,y_N of the right side. Let r_x count maximal
consecutive runs of neighbors of the left vertex x in this order.
A zero-one string has twice its run count equal to its transition
count plus its first and last bits. Sum this identity over left x:

    sum_x r_x
      =d + (1/2) sum_(j=1)^(N-1)
                       |N(y_j) symmetric_difference N(y_(j+1))|.

Each endpoint has degree d, explaining the first term. LP1 yields

    sum_x r_x >= (N+q-2)(q-1)^(k-1).                 (LP2)

**Theorem LP1.** The minimum total run count over all right-side
orderings is exactly the right side of LP2.

To attain it, use a q-ary reflected Gray order. Construct the order
recursively by listing successive first-coordinate values and alternating
the suffix order and its reversal. Consecutive words differ in exactly
one coordinate, both inside a block and at block boundaries. Every
term of LP1 is then minimal, proving equality. No probability or
uncomputed optimum is used.

Consequently every order has some left vertex with at least

    ceil[(1+(q-2)/N)(q-1)^(k-1)]                     (LP3)

neighborhood intervals. Every interval-contained partition for that
order needs at least this many incidences at some source vertex.
The claim includes the canonical dyadic-interval construction; it is
not a reversal of its known upper bound.

## 3. A stronger one-sided laminar obstruction

A family of destination subsets is laminar if any two are disjoint
or one contains the other. Suppose all destination sides in a rectangle
cover of C(q,k) belong to one such family. Rectangles must be contained
in the graph. Repetitions, overlaps and scalar weights are allowed,
provided every edge is represented and no rectangle uses a nonedge.

**Theorem LP2.** The total number of source-vertex incidences in any
such cover is at least `(N+q-2)(q-1)^(k-1)`. Thus its maximum source
load satisfies LP3. The same statement holds with the sides reversed.

Proof. Extend the laminar family by the full set and all singletons,
then refine it to a full binary hierarchy on the N destination leaves.
Adding available subsets can only reduce the minimum cover count.
For a fixed neighborhood S=N(x), the minimum cover by hierarchy
clusters consists of its maximal clusters. Starting with |S| singleton
leaves, each internal node whose entire leaf set lies in S merges two
clusters and reduces their number by one. Therefore its cover count is

    |S|-#{internal nodes v : leaves(v) subset S}.

After summing over x, this is

    N d - sum_(internal v) |intersection_(y in leaves(v)) N(y)|.

Every internal cluster contains two distinct words. By LP1 its common
neighborhood has size at most `(q-2)(q-1)^(k-1)`. There are exactly
N-1 internal nodes. The displayed expression is therefore at least

    N(q-1)^k-(N-1)(q-2)(q-1)^(k-1)
      =(N+q-2)(q-1)^(k-1).

Any original collection of contained laminar sets covering S has at
least its minimum hierarchy cover count. Nested or repeated sets cannot
reduce that count, nor can weights create an uncovered edge. This proves
the claimed bound, even without requiring an exact partition. ∎

LP2 is a lower bound, not an assertion that every binary hierarchy
attains it. LP1's equality concerns interval counts in a linear order;
its intervals are not themselves a laminar family.

## 4. Consequence for the proposed graph mechanism

JR requests source and destination loads at most c^k(t+1)^c for
q=2^t, with an absolute c. For any fixed k>=2, LP3 grows as q^(k-1),
which eventually exceeds that bound for every fixed c. Thus JR cannot
be realized by rectangles with one globally laminar destination family,
or by a single common-order interval decomposition of all neighborhoods.
This remains true if one enlarges the finite constant c.

The finite example C(4,2) already separates the models: LP3 is four,
whereas S004's checked opposing-star partition has maximum load three
on both sides. General partitions can be better than any one-order
interval cover, and are not ruled out by this theorem.

Multiple hierarchies, nonlaminar endpoint sets, algebraic cancellations
using rectangles not individually contained in the graph, and different
label geometry remain outside the result. No tensorization of arbitrary
local partition numbers is asserted. The theorem identifies a failed
construction route; it leaves the finite JR question open.

Credits: @CubeJerry; S004's JR formulation and opposing-star example;
Cardinal/McCarty/Yuditsky for the ordering-based decomposition lead and
breakpoint viewpoint; substantial AI-assisted exact crown-product and
laminar calculations. No literature-priority, formal or human-review claim.
