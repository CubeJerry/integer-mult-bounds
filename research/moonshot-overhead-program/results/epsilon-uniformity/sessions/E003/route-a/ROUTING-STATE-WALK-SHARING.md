# Reusing partial Fourier bases while walking through rectangle states

Status: **proved source-compatible schedule and exact call invoice;
independent review pending**. This changes the executor beyond the
destination-only gauge. It retains the optimized Psi loss and does not
improve the admitted complete multiplication rate.

Sources: pinned OpenAI Fourier `kernel.tex` and `binary.tex`; E003
`ROUTING-DESTINATION-GAUGE-SHARING.md`, the RW fixed-array executor, and
the lead's exact binary Gram/invoice theorem. The new mechanism orders
rectangles by their canonical state and changes prepared bases between
states instead of recomputing every endpoint from ordinary coordinates.

## 1. A normalized basis transition

For subspaces U,V inside one auxiliary vector space, put

    delta(U,V)=dim U+dim V-2dim(U intersection V).       (W1)

Changing from the partial-Fourier basis on U to that on V needs exactly
delta(U,V) one-axis transforms in the following chosen factorization,
plus coordinate/sign maps. Choose a basis of U intersection V, extend
it separately through U and V, and complete a basis of U+V and of the
ambient space. In these coordinates the common Fourier directions
cancel; only the two disjoint complements remain. Alternative coset
representatives and character coordinates are monomial changes. This
argument uses abstract paired-dual coordinates and permits degenerate
restricted forms. For the two-half source kernel, the bill is 2delta.

The fixed auxiliary initial phase cancels when changing between source
preparations. The fixed auxiliary final phase cancels when changing the
coordinate system of an accumulated destination. Distinguished phases
remain in the query middle, as in the source endpoint proof. Therefore
W1 applies without paying a new query-dependent transform.

## 2. Canonical states and the constant-array schedule

Write q=2^t and let a state s belong to {0,...,t}^L. Zero means an equal
coordinate; b>0 selects first differing bit b. Retain precisely states
with an odd number of nonzero coordinates. Their number is

    lambda=[(1+t)^L-(1-t)^L]/2.

For one state, its rectangles partition the labels on the source side
and also on the destination side. A fixed label belongs to exactly one
rectangle on each side: its prefix and bit orientation determine it.
Consequently all source rows and destination accumulators can be
prepared in one state at a time.

Keep the original input, a prepared source collection, an accumulated
destination collection in its current prepared coordinates, and an
ordinary accumulator for charged/pointwise terms. Begin with the first
odd state in lexicographic order. Prepare its source endpoints, and
process all its rectangles using the original shared-query middle.
Before the next state, change each source's basis by W1. Change each
destination accumulator from its old inverse-endpoint coordinates to
the new ones, also by W1, then add the next state's contributions.
After the last state, apply that state's final endpoints once and add
the ordinary contributions.

Each state processes every rectangle exactly once with its original
nonzero weight. Query sharing is unchanged. The input prepared array
is not overwritten by query work; copies use reusable scratch. No new
independent input rows or metadata-inflated child volumes are counted.
There are a fixed number of numerical collections, and sibling calls
reuse marked regions. State descriptions, basis changes and the actual
operation count are still polynomial in the local arity. Thus RW's
physical and precision allowances apply. This statement changes Fourier
call counts; it does not erase the paid middle coordinate changes.

## 3. Exact transition ranks

Put a(0)=1 and a(b)=2^(t-b) for 1<=b<=t. Every side span in state s has

    r_s=1+sum_i(a(s_i)-1),                             (W2)

by the proper-letter-set rank lemma. For a fixed source label, its
possible destination letter sets at one coordinate are the singleton
containing its own letter and the t opposite-prefix halves. These sets
partition the q letters. When q>=4, the union of any two distinct such
sets is proper.

For two distinct states s,s', the source span intersection is exactly
the sum of the unchanged-coordinate difference spaces. To verify this,
a norm-one vector in either span has odd coefficient sum in every
coordinate's letter set. Equality of two representations forces their
coordinate functions to differ by constants. A changed coordinate has
disjoint sets with proper union, so the constant is zero and odd sums
cannot match. Hence an intersection vector has self-pairing zero.
Its difference-space components then agree only in unchanged coordinates.
Therefore, if K={i:s_i!=s_i'},

    delta_source=2+sum_(i in K)(a(s_i)+a(s'_i)-2).      (W3)

At a fixed destination, its own-side prefix sets are nested and all
contain its letter. The common base vector is d_w; intersections of
the coordinate difference spaces use the smaller sets. Thus

    delta_destination=sum_i |a(s_i)-a(s'_i)|.          (W4)

Both formulas are independent of the actual label. Together they give
the exact chosen transition bill

    2delta_source+2delta_destination
      =4[1+sum_(i in K)(max(a(s_i),a(s'_i))-1)].        (W5)

The first lexicographic odd state has one nonzero coordinate equal to
1, so r_first=q/2. The last has only zero or t coordinates, so r_last=1.
For q>=4 the exact declared free invoice is consequently

    F_walk=q+2(D-1)
       +4 sum_(consecutive odd states s,s')
          [1+sum_(i:s_i!=s'_i)(max(a(s_i),a(s'_i))-1)]. (W6)

At q=2, the source spans of every odd state are the same opposite-parity
line; destination spans are also constant. There are no basis-transition
calls. The entire free correction uses exactly four calls per label row,
independently of L. The q>=4 hypothesis in W3 is essential.

## 4. A quantitative walk bound

For distinct states define c(s,s') to be the bracket in W6, and c(s,s)=0.
This is a metric: it is the discrete metric on whole states plus a sum
of coordinate pseudometrics. For distinct coordinate symbols the latter
distance is max(a,b)-1; it satisfies the triangle inequality, including
the two symbols of size one. Hence deleting all even-support states
cannot increase the total variation of the full lexicographic walk.

Set n=t+1. For one coordinate, the nonwrap transitions 0,1,...,t have
total coordinate weight

    (q/2-1)+sum_(b=1)^(t-1)(2^(t-b)-1)
      =3q/2-t-2.

The wrap t->0 has weight zero. Summing the lexicographic carry counts
over all L coordinates, and adding its n^L-1 discrete transitions,
gives full-walk variation

    [(3q/2-2)/t] [(t+1)^L-1].                         (W7)

The metric bound and W6 prove

    F_walk <= q+2D-2
       +4[(3q/2-2)/t][(t+1)^L-1]
       <= 20q(t+1)^(L-1).                            (W8)

The last constant is deliberately conservative. Use D<=Lq, t>=1,
`(t+1)/t<=2`, and `L<=(t+1)^(L-1)` for L>=2. This is a new executor
bound, not merely a different estimate of the old independent-endpoint
schedule. In the retained even-L optimized regime t/L->infinity,
the old free invoice is Theta(L^2 q t^(L-1)), whereas W8 is
O(q t^(L-1)). Thus it saves at least an order L^2 factor there. The
destination-only sharing bound may be combined by taking the cheaper
proved schedule; no claim that W8 is its exact optimum is made.

### A better order: round-trip Gray walks within each odd support

The lead supplied a better ordering after reading the lexicographic
construction. For each odd support S of size j, traverse [t]^j in a
reflected Gray order starting at the all-t state, then reverse that
walk back to all t. Process rectangle contributions only on the first
forward visit. Reverse steps only change the prepared source and
accumulator coordinates; they do not add the same contribution twice.
Move between odd supports at their all-t states, in any fixed order.

Within a support, one level changes at each step. W5 is then
`4 max(a(b),a(b'))`. The one-coordinate reflected path has weight
`sum_(b=1)^(t-1)2^(t-b)=q-2`. Recursing through j coordinates gives
weight `(q-2)(t^j-1)/(t-1)`; reversal doubles it. Between supports,
every side letter set is a singleton, so the source transition has
delta two and the destination transition is zero. Each such move costs
four calls. There are B=2^(L-1) supports, while the boundary calls sum
to 2D. Hence, for t>=2, the exact chosen invoice is

    F_gray=2D+4(B-1)
       +8(q-2)(lambda-B)/(t-1).                       (W12)

This equals O(D+(q/t)lambda) with absolute constants. It improves the
destination-weighted Theta(Lq lambda/t) free bill by a factor of order
L whenever that term dominates the common D term. The lex order has
the weaker W8 estimate; the factor-L statement here belongs to W12.
At q=2 all source and destination gauges are constant across supports,
so the earlier exact four-call exception remains.

The fixed-array schedule is unchanged. Returning along the prepared
basis path does not need saved numerical snapshots: apply the inverse
basis transition to the live source and destination arrays. Its operation
list reverses and inverts coordinate maps and uses inverse normalized
axis transforms, which are self-inverse in the binary setting. The
extra state visits and scalar work remain polynomial in m.

## 5. The new walk still has a Psi invoice obstruction

For q>=4, W3 is at least two at every distinct consecutive state. W6
therefore retains a positive source transition charge of at least
4(lambda-1), as well as boundary charge q+2D-2. Its full call invoice
dominates the subinvoice

    J_walk=D+lambda
       +mD binom(L,floor(L/2)) q^(-ceil(L/2)).          (W9)

The charged term uses the same nonzero highest Newton coefficient as
the previous schedules. This is a lower bound on this chosen positive
invoice, not on general Walsh algorithms or tape running time.

The same subinvoice applies to W12. Its walk visits all lambda distinct
source subspaces, so at least lambda-1 nonzero transitions occur. Its
boundary charge is 2D. More generally, every canonical side rank is at
most D/2, so any starting/ending states have boundary charge
`2r_first+2(D-r_last)>=D`. Reordering such a single prepared-basis walk
does not evade this declared-invoice lower bound.

Put x=log2 m, b=log2 J_walk and u=L-1. Exact rank, incidence and the
charged term imply

    b>=t,       b>=u log2(t+1),       b>=x-u t/2.       (W10)

For x>=16, these yield

    b >= (1/2)sqrt(x log2 x).                          (W11)

Indeed, b>=x/2 already suffices. Otherwise ut>x and adding the first
two inequalities gives `2b>=t+(x/t)log2(t+1)`. For t<=sqrt(x), the
decreasing quotient log2(t+1)/t gives
`2b>=sqrt(x)log2(x)/2>=sqrt(x log2 x)`. For t>=sqrt(x), AM--GM gives
`2b>=sqrt(2x log2 x)`. At q=2, the charged term alone is at least m,
by `binom(L,floor(L/2))>=2^floor(L/2)` and D=2, so that exception is
also bounded below at the displayed scale despite its constant free bill.

Conversely, W8 is at most an absolute multiple of the old free invoice:
D>=q and lambda>=(t+1)^(L-1). The charged part is unchanged, so the
retained optimized labels give logarithmic loss O(Psi(log m)). The
leading optimized scale remains Theta(Psi(log m)) for this walk invoice.
The proof explicitly checks the changed schedule instead of importing
the old D lambda lower bound.

## 6. Verification and remaining questions

`ROUTING-verify-state-walk.py` checks exact source/destination span
intersections, full partial-basis transitions, lexicographic invoices,
the q=2 collapse, and finite arithmetic guards. It does not execute a
tape multiplier. The written physical argument retains RW's source
contracts and fixed-array executor; a new smaller routing-time bound
is not assumed.

More general combinations of several prepared bases, cancellation-based
transforms or a different state grammar remain possible. Within this
walk, a better visiting order can change the finite invoice but still
visits lambda distinct source subspaces when q>=4, so its retained
positive transition count leaves the same asymptotic obstruction.

Credits: @CubeJerry; pinned OpenAI partial endpoints, canonical labels
and normalization; E003 destination gauge, exact Gram/invoice and RW
components; substantial ChatGPT assistance. No improved complete H,
formal-kernel proof, human refereeing or exhaustive priority claim.
