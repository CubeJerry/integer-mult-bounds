# Lead review of changing prepared Fourier bases

Disposition: **accept the lexicographic and round-trip Gray schedules as
source-compatible local refinements**. The complete multiplication
envelope remains unchanged. Reviewed proof SHA-256:
`10e4edb81ce05aea7f5eabea93e039b273b95d79d74ae57bbe6f344e5b142aa8`.

The lead read the complete proof and verifier, supplied the support-block
Gray traversal after reviewing the lexicographic construction, and
independently invoked the exact partial-basis overlap checks. The receipt
`state-walk-transition-replay.json` pins the proof and both verifier files:
4,774 subspace pairs and 1,165,984 matrix entries passed. This replay did
not independently repeat every endpoint-rank or Gray-path case; A's own
receipt records those additional checks. B supplies a separate proof review.

## Why the transition can be shared

A partial Fourier basis consists of normalized characters on cosets of
its transformed subspace. Choose coordinates adapted to U intersection V,
then the two disjoint complements in U+V, and finally the ambient space.
The common transforms cancel. This gives exactly
`dim U+dim V-2dim(U intersection V)` one-axis calls in the stated
factorization, with paid monomial coordinate changes. It requires no
nondegeneracy of the restricted forms. Different coset representatives
and character labels change the basis only monomially.

The auxiliary endpoint phases are fixed by the source or destination
label and cancel in consecutive changes. Distinguished phases remain in
the middle. Each label has one source incidence and one destination
incidence in a canonical state. It is therefore legitimate to keep one
prepared source collection and one live destination collection, changing
both before processing the next state. The ordinary charged contribution
stays in its own accumulator until the final ordinary-coordinate flush.

The transition ranks are independent of the actual label. They can be
batched across the original full-rate row volume with the same child
width. State controls, binary bases and physical coordinate maps remain
polynomial in the local arity, and a fixed number of numerical arrays is
reused. The earlier polynomial routing and numerical-gain allowances
remain charged. No improved tape-time coefficient is inferred from a
smaller Fourier-call list alone.

## Exact ranks and the stronger traversal

For q>=4 the possible opposite-prefix sets of one source coordinate are
disjoint and the union of any two is proper, including q=4. Thus no
nonzero coordinate constant can conceal their disagreement in the Gram
quotient. A common norm-one vector is impossible at a changed coordinate;
the intersection consists exactly of the unchanged difference spaces.
At a destination, the sets instead nest around its own letter. These
facts give A's distinct source and destination transition formulas W3--W5.

For the Gray traversal, fix each odd support S, visit its t^|S| levels
by a reflected Gray walk from the all-t state, and return on the reverse
path. Add rectangle contributions on first forward visits only. The
weighted one-coordinate path costs q-2, and its j-coordinate recurrence
is `R_j=t R_(j-1)+(q-2)`. Between supports all side ranks are one;
the source transition costs four calls and the destination is unchanged.
The initial source and final destination calls total 2D. Hence

    F_gray=2D+4(B-1)+8(q-2)(lambda-B)/(t-1),
    B=2^(L-1),  t>=2.

The reverse traversal changes the live arrays directly and needs no
saved numerical snapshots. It does not duplicate any rectangle summand.

There is a useful uniform strengthening of the comparison in A's note.
The positive incidence polynomial gives `lambda>=tB` and `lambda>=Lt`.
Also `q/2<=q-2<=q` and `Lq/2<=D<=Lq`. Therefore

    4q lambda/t <= F_gray <= 19q lambda/t.             (R1)

For the upper bound, the last term is at most `16q lambda/t`, the
boundary at most `2q lambda/t`, and `4B<=q lambda/t`. The lower bound
uses `(lambda-B)/(t-1)>=lambda/t`. Thus the original `2D lambda`
free bill is reduced by Theta(Lt), uniformly for L,t>=2. Compared with
the independently proved destination-weighted bill, the improvement is
Theta(L). These comparisons concern the free component; charged work
and ordinary routing may dominate the full executor.

The lexicographic bound is a separate, weaker construction. Its
`O(q(t+1)^(L-1))` estimate must not be used to claim the Gray order's
factor-L improvement over destination weighting.

## The changed invoice has a fresh lower argument

For q>=4 every distinct source state has a distinct span, so a walk
visiting all lambda states pays positive transition cost at least
proportional to lambda-1. Boundary calls contribute at least D. The
highest charged coefficient is unchanged and nonzero. This supplies
the new positive subinvoice J_walk in A's W9, independently of the old
`D lambda` endpoint argument.

With x=log2 m, b=log2 J_walk and u=L-1, its actual terms give
`b>=t`, `b>=u log2(t+1)`, and `b>=x-ut/2`. The stated split at
`b=x/2` and `t=sqrt(x)` proves the half-Psi bound for x>=16. At q=2
all free states collapse to the same two gauges and only four free calls
remain; the charged term is at least m. This exception is a useful
positive control against mistaking the earlier literal invoice for a
universal runtime lower bound.

The result admits a concrete improvement of the local implementation.
It does not prove that every endpoint-sharing strategy is a single
prepared-basis walk, or lower-bound arbitrary Walsh algorithms. A better
state tree or another geometry requires its own pricing. No full
multiplier, formal proof kernel or human refereeing is claimed.
