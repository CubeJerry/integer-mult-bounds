# Independent review of the prepared-basis state walk

Disposition: **pass for the stated source-compatible executor, its exact
Fourier-axis invoice, and its fresh scoped lower bound**. This is a
constructive improvement to the previous endpoint schedules. It does not
change the admitted complete multiplication scale. The invoice lower
bounds below are not machine-time lower bounds.

Reviewed A file `ROUTING-STATE-WALK-SHARING.md`, including the lead's
round-trip Gray improvement W12, SHA-256:

`10e4edb81ce05aea7f5eabea93e039b273b95d79d74ae57bbe6f344e5b142aa8`.

The complete proof and the earlier exact lexicographic verifier and
receipt were read. Primary sources remain OpenAI math
`3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier `kernel.tex` and
`binary.tex`. Source hashes and the endpoint phase audit are recorded in
`REVIEW-DESTINATION-GAUGE-AND-RANK.md` and
`REVIEW-RATIONAL-WALSH-SPACE.md`. This review independently derives the
transition, intersection, ordering and lower-bound calculations.

## 1. Exact change between partial Fourier bases

A normalized partial Fourier basis along U consists of characters on
affine U-cosets. Changing a basis of U, character coordinates, or coset
representatives only permutes these vectors and changes their signs.
Choose a basis of U intersection V, extend it through U and V separately,
and complete it through the ambient space. The two separate extensions
are independent modulo the intersection. In these common coordinates,
the Fourier transforms on shared axes cancel. The remaining axes number

```
delta(U,V)=dim U+dim V-2dim(U intersection V).
```

This constructs the specified factorization with exactly delta
one-axis calls and monomial maps, without claiming optimality among
all circuits. Character/coset coordinates do not assume that either
subspace is nondegenerate or complementary to its orthogonal space.
The paired two-half source endpoint uses twice this invoice.

The phases have the required order. A source preparation has its fixed
auxiliary initial phase on the original-input side, so that this phase
cancels between preparations. A destination endpoint has its fixed
auxiliary final phase on the ordinary-output side, so that it cancels
when the accumulator changes inverse-endpoint layout. Distinguished
phases remain in the query middle, as in the primary construction.
No query-dependent dense map is commuted past a phase.

## 2. The two state-space intersection formulas

Let q=2^t and a(0)=1, a(b)=2^(t-b) for b>0. A product side with coordinate
letter sets A_i has span dimension `1+sum_i(|A_i|-1)`. Represent a linear
combination of label Gram rows by coordinate functions f_i supported on
A_i. Their coefficient sums have a common value C; its self-pairing is
C. Equality of two representations implies that the coordinate
functions differ by constants, since functions on separate coordinates
can sum to zero only this way.

For a fixed source label, the t+1 destination sets in one coordinate
partition the alphabet: its singleton and the opposite prefix halves.
If q>=4, any two distinct members have proper union. This includes
q=4, with sizes 1,2,1. At a changed coordinate, disjoint supports with
proper union force the difference constant to vanish and both functions
to be zero. Hence C=0. At unchanged coordinates the proper support also
forces the difference constant to vanish. Exactly the unchanged
coordinate difference spaces remain. Thus for distinct states s,s',

```
delta_source=2+sum_(i:s_i!=s'_i)[a(s_i)+a(s'_i)-2].
```

At a fixed destination, own-side prefix sets are nested and contain its
letter. Their common base is the same norm-one label vector, and their
difference-space intersections use the smaller sets. Consequently

```
delta_destination=sum_i |a(s_i)-a(s'_i)|.
```

Final endpoints transform orthogonal complements inside the fixed
auxiliary space. Orthogonal complementation preserves this subspace
distance, so the side-span calculation applies to those endpoints.
These are different intersection problems; swapping their formulas
would be wrong. Combining the paired halves gives exactly

```
4[1+sum_(i:s_i!=s'_i)(max(a(s_i),a(s'_i))-1)].
```

For q=2 the proper-union argument fails. All odd source states give
the same opposite-parity line, and destination spans are constant.
Transitions then cost zero axis calls; the boundary costs four.
A's separate q=2 treatment is necessary and correct.

## 3. The prepared-array schedule

For a fixed odd-support state, canonical rectangles partition the labels
on each side. Each label therefore has one source preparation and one
destination layout in that state. The source collection is retained
while query work uses scratch copies. The destination holds all previous
contributions in its current inverse-endpoint layout. Changing its basis
transforms that entire value before the next contributions are added.
The final ordinary-coordinate endpoint is essential.

A fixed number of collections suffices: original input, prepared source,
current destination, ordinary charged/pointwise contributions and reusable
scratch. No per-state collection is needed. Row matrices retain their
independent row-factor action. Complete spectator ranges and independent
input volume are unchanged, preserving full-rate batching and the
constant-array storage contract. State enumeration, bases and monomial
changes remain polynomial in local arity, with physical routing paid.
Completed basis transitions are unitary; the polynomial number of other
local operations fits the earlier polynomial logarithmic-gain allowance.
The existing guarded precision supplier therefore applies. This does
not infer smaller physical routing time from the smaller axis count.

## 4. Lexicographic and round-trip Gray invoices

The first odd lexicographic state is `(0,...,0,1)`, of side rank q/2.
The last contains only 0 or t, of side rank one. Hence the boundary cost
is q+2(D-1). The bracket in the transition formula is the whole-state
discrete metric plus coordinate pseudometrics with nonzero distance
`max(a,b)-1`. If endpoint symbols differ, their larger size occurs on
at least one leg through an intermediate symbol, proving the triangle
inequality. Size-one symbols can have zero coordinate distance. Deleting
even states from the full lexicographic walk cannot increase variation.

One coordinate's nonwrap sum is `3q/2-t-2`, and its t-to-0 wrap has
zero weight. Summing lexicographic carry multiplicities, then adding the
whole-state discrete transitions, gives the exact full variation

```
[(3q/2-2)/t][(t+1)^L-1].
```

D<=Lq, `(t+1)/t<=2`, and `L<=(t+1)^(L-1)` imply the stated conservative
bound `F_walk<=20q(t+1)^(L-1)`. In the retained even-L regime t/L tends
to infinity, this is an order-L^2 improvement of the old free upper
invoice. It is not an order-L^2 improvement of the complete time bound.

For the lead's better order, fix an odd support of size j. A reflected
Gray path on `[t]^j` changes one level at a time. The one-dimensional
weight is `q-2`; the j-dimensional path weight R_j satisfies

```
R_1=q-2,       R_j=t R_(j-1)+(q-2),
R_j=(q-2)(t^j-1)/(t-1).
```

Reversing the path doubles this weight. It does not duplicate any
contribution: contributions are added only on their first forward visit.
Both live arrays are returned by inverse basis transitions; numerical
snapshots are unnecessary. At the all-t corners, changing odd support
costs four calls because the source distance is two and destination
distance zero. There are B=2^(L-1) odd supports, and both boundary
states have rank one. Therefore

```
F_gray=2D+4(B-1)+8(q-2)(lambda-B)/(t-1).
```

This independently proves W12. For t>=2, lambda>=tB and
`q/2<=q-2<=q`, so its growth is Theta(D+(q/t)lambda), with absolute
constants. Compared with the previously rank-weighted free bill, it
gives an order-L improvement whenever the nonconstant term dominates
the common D term. The q=2 four-call exception remains separate.
The extra visits and ordinary routing still have polynomial arity cost.

## 5. Fresh lower bound for the changed invoice

For q>=4 there are lambda distinct source states, and every nontrivial
transition costs at least four. The lex and Gray schedules therefore
retain at least lambda-1 such transitions. All side ranks satisfy
`r<=1+L(q/2-1)=D/2`; thus any single prepared-basis walk has boundary
charge at least D. The full declared call invoice dominates

```
J_walk=D+lambda+m D binom(L,floor(L/2)) q^(-ceil(L/2)),
```

using the retained nonzero highest charged Newton term. Let x=log2 m,
b=log2 J_walk and u=L-1. The actual terms give

```
b>=t,       b>=u log2(t+1),       b>=x-ut/2.
```

If b>=x/2, the half-Psi lower bound follows for x>=16. Otherwise ut>x,
so `2b>=t+(x/t)log2(t+1)`. For t<=sqrt(x), decreasing
`log2(t+1)/t` gives `2b>=sqrt(x)log2(x)/2`, which is at least
sqrt(x log2 x). For t>=sqrt(x), AM--GM gives the stronger
`2b>=sqrt(2x log2 x)`. This independently proves W11.

At q=2, D+lambda is no longer a valid free subinvoice. Instead the
charged term alone is at least m: D=2 and
`binom(L,floor(L/2))>=2^floor(L/2)`. A explicitly separates this case.
The new upper invoices are bounded by an absolute multiple of the old
optimized invoice, because D>=q and lambda>=(t+1)^(L-1). Thus the new
schedule's optimized logarithmic loss remains Theta(Psi(log m)). The
old D-lambda lower bound has not been reused after its mechanism changed.

The coupled Walsh/toll theorem applies after normalizing this new positive
invoice, **only if its separate positive normalized routing toll is
retained**. Neither fewer Fourier-axis calls nor the abstract theorem
proves that every physical implementation must pay that toll.

## 6. Finite evidence and limits

The pre-Gray receipt was read without claiming an independent replay.
It pins verifier
`5da19e85248fd5f224f09165d649276fb986552a9ef2c7aa34704bd7509dcc99`
and helper
`fc556c3cd12d921a406e51d525fc796d325523b5ec1f035140cdb02dc5029681`.
It records 4,774 exact partial-basis pairs, 1,165,984 matrix entries,
69,584 endpoint ranks, 33,341 adjacent state pairs, 4,572 all-state
pairs, 30 lexicographic variations and 3,003 rounded lower-bound guards.
The q=2 formula rejection and final-coordinate flush are explicit
controls. W12 is independently proved in section 4; this review does not
represent an unfinished updated verifier as having run.

These checks support finite identities; they are not a tape multiplier,
timing experiment or proof-kernel run. The reviewed schedule and fresh
invoice proof pass. Multiple prepared-basis dictionaries, cancellation,
different labels and shared physical routing remain outside this
single-walk retained-invoice barrier.

Credits: @CubeJerry; pinned OpenAI endpoint construction; E003 A's
state-walk mechanism and verifier; lead's improved Gray ordering;
substantial ChatGPT assistance.
