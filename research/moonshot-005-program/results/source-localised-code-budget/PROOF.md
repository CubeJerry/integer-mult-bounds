# A paid obstruction for source-localised linear endpoint codes

**Scoped exact theorem for wholly newly paid packet transport. No new κ.**

Any code in the interface below, with every packet transport leg newly paid,
has newly paid moment at exponent199/200 at
least **98.992356 per native**. The full conditional H4 allowance is strictly
below98.399076950198. Thus this interface cannot complete the target even when
all reverse duties, common restoration, side-information acquisition, scalar
work, storage, erasure, precision and compiler work are granted free.

This is stronger than the earlier43-message result only in its new *paid,
source-localised one-stage* interface. It is not obtained by charging43 packets
at a uniform rank. Arbitrary numbers of packets, arbitrary linear code factors,
arbitrary cancellations between packets, and different encoder/decoder charts
are allowed. Multiple acquisition stations, multiple distribution stations, or transit of
these packets on existing funded reservations are outside the interface.

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
Retain the native/shared-wire lineage and the programme's source, E8 and
side-information contributors. The rank inequality used below is elementary;
the contribution is its exact source-specific weighted certificate and scope.

## 1. Fixed source and deliberately generous access

The immutable native is
`research/shared-wire-split-composition/data/final.json.gz`, SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
It has1480 arbitrary common inputs and104 first donor/receiver pairs. Let q_i
be the104 independent donor differences in the source's `live` order. After
normalizing the nonzero factors1 or1/2 and subtracting the receiver's own
initial difference, its forward demand is exactly q_i.

Let S be the reviewed `main_reuse_retimed47` matrix in
`results/endpoint-side-information/EXPANDED.json.gz`. This grants neutral
helper-coordinate paths, all47 clean second-owned paths, and arbitrary reuse
and retiming of every original raw-main path. In particular the47 clean-owned
paths are granted for free here although H4 pays for none of that second-owned
rail. This is an information relaxation, never a reservation credit.

Receivers22,44,72,89,109 have granted self-delivery. Fix those five donor
coordinates to zero and grant all their demands for free. This leaves99
independent active coordinates. Every lower bound on this restriction is a
necessary bound for the original104-coordinate problem.

For each binary source chart c, define:

- D_c: active donor roles whose original X itinerary visits c;
- R_c: active receivers whose original Y itinerary visits c.

We grant all those original q values to their donor charts forever, and grant
arbitrary retiming, caching and simultaneous availability. This removes
chronology, competing uses of reservations and the cost of snapshots. Canonical
charts are exact binary subspaces; duplicate labels are identified. There
are352 donor charts and283 receiver charts, giving99,616 chart pairs.

### Allowed new packets

A packet p chooses one encoding chart c_p and one decoding chart d_p. It is an
arbitrary linear function of the q_j with j in D_(c_p). Every leg of its transport is newly paid. It is transported by any sequence
of proper nested owned chart moves, then supplied in arbitrary
linear combinations to any receiver in R_(d_p). All receiver coefficients
are allowed; the packet's actual coefficient supports may be smaller than
these chart-based sets. Multiple packets may interfere and cancel.

Each packet has the full common field volume V. All statements hold over any
characteristic-zero coefficient field and every positive V. Arbitrary V by V
coordinate maps within a packet or its decoder are allowed; scalar maps are a
special case. The target is exact recovery on every independent donor input.
Side information consists of the q_j with S_ij=1. Those existing routes are
not granted as free transit for a coded packet in this model. In particular,
a hybrid path using one new move plus an old funded move need not cost g(c,d)
in new paid moment and is not covered. No altered dirty-common
history is silently added to it.

The one encoding and one decoding chart conditions are substantive. The
packet cannot accumulate new q contributions at later source stations or
serve receiver groups at distinct decoding stations under this theorem. A
later code using those operations requires a new paid test. This theorem also
does not cover retargeted raw itineraries, common-response codes, retained
common records, changed native words, or data received by an encoder outside
its declared D_c.

## 2. Exact lower price between two charts

For binary spaces U,W, put m=dim(U intersect W). Any nested path from U to W
has total downward rank at least dim(U)-m and total upward rank at least
dim(W)-m. For the first claim, project every intermediate space modulo W:
its starting image has dimension dim(U)-m, its final image is zero, an upward
step cannot decrease that image, and a downward step decreases it by at most
that step's rank. The other claim follows by projection modulo U.

For0<t<=1, subadditivity gives sum r_j^t >= (sum r_j)^t separately for upward
and downward steps. Hence every such packet transport has price at least

    g(U,W)=(dim(U)-m)^t+(dim(W)-m)^t,       t=199/200,

where a zero term contributes zero. The route through U intersect W attains
this price if arbitrary intermediate charts are granted. Granting that chart
only makes this lower price more favorable than an actual fixed-frame word.

Thus the checker can price every allowed chart pair using its exact binary
intersection, without assuming that the two endpoints are nested. It never
charges a dimension difference between incomparable spaces as one call.

## 3. Weighted acyclic rank inequality

Let the code's packet matrices be A_p B_p. Each has rank at most V, its row
support is contained in R_(d_p), and its column support is contained in
D_(c_p). Exact decoding can be written

    I-K = sum_p A_p B_p,

where K has block entries only at side-information positions S_ij=1. If the
entire rectangle R_(d_p) by D_(c_p) lies in S, absorb this packet's contribution
into K. Such a packet transmits only data already granted at every recipient;
it need not consume a constraint in the lower-bound certificate. There are
12,537 chart pairs of this kind. In particular every zero-distance chart pair
is absorbed.

For any acyclic vertex subset U of the directed side-information graph, a
topological order makes (I-K)_(U,U) block triangular with I_V on its diagonal.
Its rank is |U|V. Subadditivity of rank therefore gives

    |U| <= sum_p 1[D_(c_p) intersects U and R_(d_p) intersects U].

This inequality is valid for arbitrary linear packet factors and arbitrary
cross-packet cancellations. It does not require any packet support to be a
clique, and it does not require the displayed E8 decoder.

Now choose nonnegative rational weights lambda_U such that, for every chart
pair not absorbed above,

    sum_U lambda_U 1[D_c intersects U and R_d intersects U] <= g(c,d).

Multiplying the rank inequalities and summing yields

    sum_p paid_moment(p) >= sum_U lambda_U |U|.

`CERTIFICATE.json` supplies74 acyclic subsets with positive integer numerators
and common denominator10^6. Their weighted size is exactly

    98,992,356 / 1,000,000 = 98.992356.

The standalone checker verifies each subset's acyclicity, reconstructs the
original donor and receiver itineraries from the native, and checks all87,079
remaining paid chart-pair inequalities. All arithmetic after source parsing
is integer or rational. Powers r^(199/200) are enclosed by integer200th-root
brackets with denominator10^24. The smallest scaled constraint slack is
positive. The exploratory LP is not imported or rerun by the checker; its
floating point solution is not proof evidence. Flooring its positive weights
produced a rational witness that is independently checkable.

## 4. Complete H4 comparison

Use the authenticated full T4 and P4 in
`results/eight-packet-budget-and-reverse/INVOICE-SOURCE.json`. There are18
native repetitions,27,344 target positions and152,424 base paid positions.
For a new per-native profile h, the entire profile is

    T=T4,      P=P4+18h.

The permitted added moment per native is

    H = (sum_r T4[r]r^t - sum_r P4[r]r^t)/18.

Directed exact arithmetic gives

    H < 98.399076950198,
    98.992356 - H > 0.593279049802464556683907.

Consequently every code in Section1 fails the complete H4 target before
charging any remaining native obligation. The eight coupled reverse returns,
96 hosted reverse shears, common restoration and all nontransport costs were
granted free; no additional lower bound needs to be added. S8's retained
second-owned reservations or lifetime savings are not mixed into this invoice.
The absence of a complete source supplier, compatible BIT improvement and the
five inherited foundational assumptions remain unchanged.

## 5. Sharp special case: one-packet clique covers

There are exactly1,268 nonempty cliques in the mutual side-information graph
on the99 active demands:99 of size1,346 of size2,319 of size3,280 of size4,
176 of size5 and48 of size6. A clique packet is one sum of its donor values,
formed at a chart shared by all donors and decoded at a chart shared by all
receivers; each receiver subtracts its granted other coordinates.

Exhausting all actual common encoder/decoder stops shows that every such
clique costs at least its cardinality, except {67,80}. This pair can use
encoder chart749 of dimension3 and decoder chart105 of dimension1. The
spaces are nested and the price is2^t. No other chart pair discounts this
clique, and no other clique has any discount.

Therefore the exact fractional and integral weighted clique-cover optimum
in this relaxation is

    97 + 2^(199/200) = 98.993080525655735668457964...

The upper bound uses the one discounted pair and97 singleton packets. For
the matching dual, give every active demand weight1 except demand67, which
gets2^t-1. The exceptional pair's total weight is2^t; every other clique's
weight is at most its cardinality and hence at most its paid price. This
proves optimality for fractional covers too. It is a relaxed code, not a
simultaneously schedulable source implementation of the free S observations.

The general linear certificate of Section3 is slightly weaker numerically,
but covers arbitrary linear codes across these stations rather than only
clique packets. It suffices to exclude H4 without a sharp general optimum
claim.

## 6. Controls and remaining questions

Positive controls check99 rank-one coordinate packets and the exact two-user
clique decoding. Rejecting controls show that: a rank-one broadcast from the
full hub to every receiver violates the paid certificate; doubling its weights
violates a true rank-one coordinate route; the mutually informed pair67,80 is
not an acyclic set; and assigning unit weight to both pair members violates
the discounted clique constraint. Source pins and itinerary continuity are
checked explicitly. Normal and optimized executions must agree.

This excludes one-stage source-localised replacement codes whose entire
packet transport is newly paid, including arbitrary weighted clique covers in
that same tariff model. The next useful extensions
have concrete new operations: use a restored, available funded reservation
as coded-packet transit; let one packet collect source contributions at
several stations, let it serve different receiver stations along one charged
route, or use physically retained/common-response information beyond S. A
first test should price one such packet or response and preserve every raw
and common endpoint, before constructing a larger family.
