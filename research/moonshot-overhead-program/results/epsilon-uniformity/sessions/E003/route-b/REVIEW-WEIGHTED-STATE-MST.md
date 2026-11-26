# Independent review of the weighted state-tree invoice

Disposition: **pass for the exact component count, minimum spanning-tree
weight, factorial upper bound and fixed-array closed-tree schedule**.
This independently checks the lead's proposed refinement and A's written
construction, `ROUTING-STATE-TREE-SHARING.md`, SHA-256

`4958f7396176546c8929ee4a6e8d1faf4e4c471a9781e41415c993115b25c6b8`.

The physical transition supplier is A's separately reviewed
`ROUTING-STATE-WALK-SHARING.md`, hash
`10e4edb81ce05aea7f5eabea93e039b273b95d79d74ae57bbe6f344e5b142aa8`.
The present note assumes t>=2, q=2^t and L>=2. At q=2 the actual
source transitions collapse and the free bill is four; the nonzero
metric below must not be substituted for those physical transitions.

## 1. Threshold components, including the parity boundary

States s in `{0,...,t}^L` have odd nonzero support. Their number is
`lambda=[(1+t)^L-(1-t)^L]/2`. Put a(0)=1 and a(b)=2^(t-b) for b>0.
The two-endpoint transition supplier charges four times

```
c(s,s')=1+sum_(i:s_i!=s'_i)[max(a(s_i),a(s'_i))-1]
```

for distinct states. Fix a threshold w with `2^k<=w<2^(k+1)` and
0<=k<=t-1. Any symbol of size greater than 2^k is frozen along every
threshold edge. Indeed, changing it gives one summand plus the leading
one at least 2^(k+1)>w. The high symbols are b=1,...,h, where
h=t-1-k. Their positions and identities are invariants of a component.

Conversely fix those high data. Replace every remaining nonzero symbol
by t, one coordinate at a time. The support parity is unchanged, and
each move costs at most 2^k. The remaining coordinates are binary 0/t.
Two such words of the same required parity differ in an even number of
positions, so double-coordinate flips join them. Every double flip
has cost one, since all affected symbols have size one. This covers
00-to-tt and 0t-to-t0 changes; restricting the graph to parity-preserving
single-coordinate changes would incorrectly disconnect it.

If at least one coordinate is free, both required parity possibilities
have a nonempty class, and the preceding argument proves connectedness.
With one free coordinate its parity simply fixes its binary value.
If every coordinate is high, the state is admissible exactly when L
is odd. Hence the component count is exactly

```
C(h)=(h+1)^L                         for odd L,
C(h)=(h+1)^L-h^L                    for even L.       (R1)
```

The even-L subtraction removes the all-high assignments, which are not
vertices. The same assignments must remain singleton components for odd
L. This proves the delicate boundary cases directly. It also proves
that no additional component mergers occur between powers of two,
although the numerical metric can take other integer values.

## 2. Exact minimum spanning-tree weight

At threshold one the lambda isolated vertices merge to C(t-1)
components. At threshold 2^k the count becomes C(t-1-k), ending at
C(0)=1. Kruskal's cut argument therefore gives

```
M=lambda-C(t-1)
  +sum_(h=0)^(t-2) 2^(t-1-h)[C(h+1)-C(h)].            (R2)
```

This is exact. Every spanning tree must connect the threshold components,
giving the same weighted lower sum. Choosing forests of the newly
connected components at each threshold attains it. Intermediate edge
weights cannot lower the sum because they merge no further components.
The sparse low-symbol reset and double-toggle graph from section 1 has
the same threshold components and thus the same minimum tree weight.

As an independent algebraic check, R2 telescopes to

```
M=lambda+2^(t-1)[sum_(j=1)^(t-1) C(j)/2^j-1].         (R3)
```

Formula R2 is nonnegative term by term and preferable for exact
construction. Formula R3 exhibits the geometrically weighted moment
that replaces repeatedly charging the largest state levels.

## 3. Closed traversal and physical arrays

Choose an all-singleton odd root, such as `(0,...,0,t)`, with side rank
one. Traverse each tree edge twice and return to that root. Add each
state's rectangle contributions only on its first visit. Reverse visits
change both prepared arrays by inverse transitions but add no contribution.
No numerical snapshot at a tree node is required. Boundary transforms
cost two source calls and 2(D-1) destination calls. Therefore

```
F_tree=2D+8M.                                        (R4)
```

The state-transition phase cancellations, separate ordinary accumulator,
constant number of payload arrays, normalized child volume and complete
spectator ranges are unchanged from the reviewed walk. All labels follow
the same tree, with label-independent ranks. Tree descriptors, first-visit
flags and a traversal stack are finite control data. Since the canonical
state count, basis dimensions and transition lists are polynomial in the
retained local arity, explicit graph generation or the sparse forest
construction fit the already charged polynomial finite-data allowance.
This control storage is not a separate numerical collection per state.

Unitarity of completed transitions and the polynomial number of local
operations preserve the existing precision supplier. Ordinary middle
routing remains charged. Nothing in the tree proof makes those physical
coordinate changes free.

## 4. The factorial upper bound

For even L,
`lambda=[C(t)+C(t-1)]/2<=C(t)`. For odd L the same upper bound is
immediate. Dropping the negative initial term in R2, bounding each
positive difference by C(h+1), and using the h=t-1 term to pay lambda
gives

```
M<=(q/2) sum_(h>=0) 2^(-h) C(h+1).
```

Since C(h+1)<=(h+2)^L, the sum is bounded by
`4 sum_(k>=1) k^L 2^(-k)`. The elementary product inequality

```
k^L<=k(k+1)...(k+L-1)=L! binom(k+L-1,L)
```

and the binomial generating function give

```
sum_(k>=1) binom(k+L-1,L) z^k=z/(1-z)^(L+1),
M<=2q 2^L L!<=2q(2L)^L,
F_tree<=2D+16q(2L)^L.
```

This proves every constant in A's T5-T6. It replaces the Gray bound's
large power of t by a factorial bound depending on L. Exact small
comparisons should still use R2: a doubled tree is not always cheaper
than an open Gray path or the destination-only schedule. Minimum tree
weight does not mean minimum cost among every possible endpoint
executor. Choosing the cheapest separately established schedule is valid.

## 5. Scope of the surviving invoice barrier

Every tree edge costs at least one, so M>=lambda-1. Together with the
boundary charge 2D, R4 dominates D+lambda. The unchanged highest charged
Newton term therefore supplies exactly the fresh lower subinvoice from
the reviewed W9-W11 proof. The local Psi obstruction survives this tree
refinement on its own terms. It does not rely on the older D-lambda
or rank-weighted free invoices, both of which have been replaced.

The coupled Walsh/toll theorem can use the new sufficient call bill
containing F_tree; it must not replace that sufficient bill by the lower
subinvoice. Its separate positive normalized polynomial routing toll
remains an explicit premise. The tree proof does not establish a lower
bound on all physical routing methods or on multiplication time.

## 6. Finite evidence

A's receipt was read and is attributed to A, without claiming a separate
replay here. It pins verifier
`beb3882f3c988b153cb705a7b2794b0418fae12d42a532094c3a69e74154f8e1`
and helper
`b10468a3835b72c57fb4c40e91bc1e21176d1ad4f97a9a467ad0f211dbd8f879`.
Its fifteen complete graphs contain 2,336 states and 368,280 edges;
the resulting trees have 2,321 edges and closed walks 4,657 visits.
It also records 6,241 integer guards and a rejected even-L all-high
pattern count. These are finite metric and scheduling checks, not a
complete source pencil, tape multiplier, timing run or proof kernel.

Credits: @CubeJerry; pinned OpenAI endpoints; A's prepared-basis
transition and fixed-array executor; the E003 lead's weighted-threshold
MST proposal; A's written tree and factorial proof; substantial ChatGPT
assistance.
