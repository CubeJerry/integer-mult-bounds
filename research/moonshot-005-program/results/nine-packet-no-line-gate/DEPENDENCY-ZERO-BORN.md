# Nine fresh packets: an arbitrary-volume zero-chart bound

**Author theorem; independent review pending. No new κ.** This extends the
scalar quotient argument to arbitrary linear mixing of the V coordinates.
Its physical scope excludes nonzero one-dimensional birth charts. Those
charts have a different shortened-space dimension and require separate work.

## Source premises and interface

Use the programme's pinned hosted96 E8 root directions g_i in E=K^8, for any
characteristic-zero field K. The native gzip SHA256 is
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
The following proved source facts are inherited, not new discoveries:

1. The target pure Gram row space W has dimension8V at volume V>=1.
2. For every chart C of dimension at least2, its shortening W(C) is zero.
   This is the S008 all511 chart theorem.
3. The symmetric tensors g_i*g_i span Sym^2(E), of dimension36. This is
   the source projector-span certificate in minimum-rank-fitting-rigidity.
4. A real root-spanned subspace of ranks0,1,2,3,4,5 contains at most
   0,1,3,6,12,20 projective E8 root directions. The root-system argument in
   coordinate-return-optimum proves these bounds. Rational root ranks and
   spans are unchanged by extension to any characteristic-zero K.

There are exactly nine returned whole-field packets, each of dimension at
most V. Each packet is formed completely at one birth chart from unchanged
original D fields that actually visit that chart, then transported to the
Hub. No useful d-dependent Hub side observation or other moving informative
field is granted. Original D paths ascend monotonically from0 to their own
facets. Birth charts are either0 or have dimension at least2. Let z be the
number born at0. Coefficients may be arbitrary V-by-V operators, with no
commutation or scalar-tensor assumption. The packet rows together must
contain W.

**Theorem.** At least six of the nine packets must be born at0: z>=6.

## 1. Incomparable nonzero births without a saturation assumption

Let L be the span of all packet row spaces and k=dim(L)-8V. Since W is a
subspace of L and nine packets have capacity9V, 0<=k<=V. If dim(C)>=2,
the quotient map L -> L/W is injective on L(C), because W(C)=0. Thus
dim L(C)<=k.

If two birth charts are comparable, with smaller C of dimension at least2,
both packet row spaces lie in L(C). Their union has dimension at most k;
the other seven packets contribute at most7V. This would give
dim L<=k+7V<k+8V=dim L, a contradiction. Hence all nonzero birth charts are
pairwise incomparable, even when L has dimension strictly between8V and9V
or some packet uses less than its full capacity.

An unchanged D path can visit at most one such chart. Consequently the
sources supplying nonzero packets form disjoint groups S_1,...,S_l, where
l=9-z. Sources supplying no nonzero packet form S_0. Assigning a source
with a zero coefficient to S_0 only strengthens the following argument.

## 2. Exact decoder quotient

Replace the Gram target by its eight independent source-coordinate forms,
whose source-i coefficient is g_i tensor I_V. A linear decoder expresses
these forms using the nine packets. Let U be the image in E tensor K^V of
all z zero-born packet decoder columns, so dim U<=zV. For each nonzero group
put E_j=span{g_i:i in S_j}; also put E_0=span{g_i:i in S_0}. Since only one
nonzero packet can depend on a source in S_j, its decoder has capacity V:

    dim((E_j tensor K^V+U)/U)<=V,       E_0 tensor K^V subset U.

In particular r_j=dim E_j<=z+1 and dim E_0<=z. These statements allow U to
be fully entangled across the eight source coordinates and V field columns.

## 3. A saturated group forces a contradiction for z<=5

Suppose some E_1 has rank z+1. The preceding quotient bound forces
dim U=zV and U subset E_1 tensor K^V. For any E_j not contained in E_1,

    dim(E_1 intersect E_j)=r_j-1,
    (E_1 intersect E_j) tensor K^V subset U.

Indeed the intersection with U must have dimension at least(r_j-1)V, while
the intersection with E_1 tensor K^V has at most that dimension when E_j
is not contained in E_1. Define F to be the sum of these scalar intersections
over the outside groups, and f=dim F. Then F tensor K^V subset U, so f<=z.

After quotienting E by F, every source root lies either in E_1/F, of
dimension z+1-f, or in one of at most l-1 additional lines. The roots in
S_0 are included in E_1 because E_0 tensor K^V subset U. But their symmetric
tensors span Sym^2(E/F), since the original projectors span Sym^2(E).
Therefore

    binom(9-f,2) <= binom(z+2-f,2)+(l-1).

For f<=z<=5, the left-minus-first-right term is at least
`binom(9-z,2)-1`, which is strictly larger than `l-1=8-z`.
This contradiction excludes any rank(z+1) nonzero group when z<=5.

## 4. No saturated group cannot cover all96 roots

All nonzero groups now have rank at most z, as does E_0. For z=0,...,4 the
inherited projective root counts give total source capacities at most

    (10-z)*M_z = 0,9,24,42,72,

respectively, all below96. Thus z>=5.

If z=5, there are four nonzero groups of rank at most5, each with at most20
source roots. If E_0 has rank at most4, at most12+4*20=92 roots are covered.
Otherwise E_0 has rank5. Then dim U<=5V and E_0 tensor K^V subset U force
U=E_0 tensor K^V. Each nonzero group projects to a scalar line in the
three-dimensional quotient E/E_0. Its four projected root directions can
span at most four dimensions of Sym^2(E/E_0), whereas that space has
dimension6 and is spanned by all projected source roots. Contradiction.
Therefore z>=6, proving the theorem for every V and every characteristic-zero K.

## 5. Scope, useful continuation, and controls

This theorem needs no false assumption that nine whole fields are linearly
independent or that an arbitrary decoder's zero-born image factors as a
scalar subspace tensor K^V. That factorization is derived only in the
saturated cases where dimensions force it.

At an eligible one-dimensional chart, W(C) has dimension V, not zero. The
incomparability proof therefore does not apply to a line and its descendants.
At most two of the nine births can lie above one eligible line: three would
have union dimension at most k+V and the other six at most6V, again below
8V+k. This is a separate necessary bound, not a proof that all line cases
are covered. Copied or precombined moving raw information, useful actual Hub
records, multi-chart packet accumulation, and changed source representations
are also outside the theorem.

The result narrows nine-packet acquisition to at least six expensive zero-born
packets when all other births have dimension>=2. It does not alone exclude
the remaining z=6,7,8,9 price cases or construct any packet schedule. The next
step is to classify their actual source groups and full raw-refinement bill,
or find a coherent mixed/line-birth mechanism. All physical services, both
strict suppliers above.005 and the five foundational assumptions remain.

Credit: root arbitrary-volume proof building on worker B's scalar quotient
idea and the programme's independently verified source geometry. AI-assisted
research for @CubeJerry; predecessor credit and exact source pins retained.
