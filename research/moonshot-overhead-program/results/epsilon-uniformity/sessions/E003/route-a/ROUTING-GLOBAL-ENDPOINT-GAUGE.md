# A triangle prevents complete one-gauge endpoint sharing

Status: **proved restricted endpoint-sharing obstruction; independent
review pending**. It concerns the source-compatible partial-Fourier
model below. Multiple gauges, residual transforms, general nonmonomial
bases and new label decompositions are not excluded.

Sources: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier
`build/kernel.tex`, full endpoint subsection, and `build/binary.tex`;
the E003 star normal form and destination-gauge sharing note. This asks
whether one preparation per label can make every free middle transfer
monomial. The successful weaker destination-sharing scheme leaves
residual transforms and does not meet that requirement.

## 1. The exact partial-basis criterion

For a subspace U of a nondegenerate paired binary space D, a partial
Fourier basis B(U) consists of characters on each affine coset of U:

    |U|^(-1/2) sum_(u in U) (-1)^xi(u) e_(c+u).

Full normalized Fourier sends this to a character supported exactly on
an affine coset of U^perp. It is monomial from B(U) to B(V) if and only if

    V=U^perp.                                         (G1)

Sufficiency follows by summing `(-1)^(xi(u)+<u,y>)` over u. For
necessity, every B(V) vector has support a V-coset; equality up to a
nonzero scalar forces its difference space to equal U^perp. Degenerate
restricted forms cause no exception. Changing representatives and basis
coordinates only permutes or rescales these partial-basis vectors.

## 2. The declared sharing model

At source v choose one U_v subset d_v^perp for the two partial transforms;
at destination w choose one V_w subset d_w^perp. Dimensions zero through
D-1 are allowed. Input and output choices may differ, but each is fixed
across all rectangles and queries.

Treat phases as in the source: auxiliary quadratic phases belong to the
endpoint; distinguished phases are constant on its cosets and remain
pointwise middle factors. After stripping those factors, the cross kernel
is full paired Fourier. Therefore a free edge v->w with no residual
Fourier work requires

    V_w=U_v^perp.                                     (G2)

The source rectangle chooses U_v=H, V_w=H^perp. Our extra restriction is
one gauge per label across all rectangles. G2 is not asserted for general
basis changes outside this model.

## 3. The triangle obstruction

**Theorem G2.** If three norm-one label directions have all six directed
edges between them free, no choices satisfy this model and G2 on all
six edges.

The edges 1->3 and 2->3 imply U_1=U_2 by taking complements; other edges
give U_1=U_2=U_3=:U. All V_i equal U^perp. Since both U and U^perp are
contained in d_i^perp, d_i belongs to U intersection U^perp. It has
self-pairing zero, contradicting the norm-one condition.

For native labels [q]^L with q>=4, vary one coordinate among 0,1,2 and
fix the others. These three directions are pairwise orthogonal with
self-pairing one. The retained free correction has nonzero weight at
distance one, since `p(1)=product_h(1-1/(2h))!=0`. Thus all six directed
edges occur. Changing dimensions or separating input/output gauges does
not evade the theorem. Moving edges to a new charged part, using several
gauges, or retaining residual transforms falls outside it.

## 4. The q=2 exception has a charged-rank cost

At q=2, Gamma(v,w)=1-parity(distance(v,w)). The two parity classes E,O
each have N/2 labels, N=2^L. Their quotient directions are e_1,e_2 in
dimension two. The free graph is complete bipartite. Choosing
U_v=V_v=d_v^perp satisfies G2 on every free edge, as in the star normal
form. This special case can share both endpoints globally.

**Theorem G3.** If I=C+F and F is supported only on those free edges,
then rank(C)>=N/2 over any field. Consequently a rectangle decomposition
of C needs at least N/2 nonzero weighted rectangles.

The E-by-E block of C is I_(N/2), since F vanishes on it. A matrix has
rank at least its submatrix rank, and each weighted rectangle has rank
at most one. These facts prove the claim. It is sharp: pair the two
parity classes and use one all-ones two-label square for each pair.
Their sum has blocks [[I,I],[I,I]] and rank N/2. Negative-weight free
cross edges correct it to the identity.

Under the retained charged-rectangle routine, every rectangle uses its
2D-axis kernel for every query. Here D=2, so N/2 rectangles cost at least

    (2D)m(N/2)/N = 2m

calls per original label row per pencil. Thus the q=2 exception does not
give a square-root local call invoice while retaining that charged
routine. This is a representation and declared-invoice obstruction,
not a lower bound on other charged/free implementations or tape runtime.

## 5. Scope and next questions

`ROUTING-verify-endpoint-gauge.py` checks exact small partial bases,
triangle gauge assignments and the sharp q=2 rank construction. Its
receipt states the finite coverage; the proofs above are unbounded.

The destination-gauge schedule already shows why the model limitation
matters: it shares one endpoint globally and pays smaller residual work.
Further mechanisms may use related gauges with priced transitions,
new rectangle decompositions, or general changes of basis. This note
does not exclude them.

Credits: @CubeJerry; pinned OpenAI endpoint construction; E003 routing
work; substantial ChatGPT assistance. No new complete bound, general
Clifford obstruction, runtime lower bound, formal proof or human review
is claimed.
