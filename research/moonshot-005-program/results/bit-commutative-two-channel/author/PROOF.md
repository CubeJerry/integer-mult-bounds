# Two independent mutable channels cannot decode an odd nonorthogonality cycle

**Proved universal structural theorem; independent review pending. No new
kappa.** This is a theorem about the evolving-code mechanism, not an inference
from a failed search. It permits arbitrary local resets and local information
injections, and applies over every nonzero commutative characteristic-two ring.
Thus replacing F2 by a larger characteristic-two field does not repair this
mechanism. General coupled packet/Y histories and noncommuting block operations
remain outside the theorem's scope.

## 1. Exact interface

Fix target source roots r_i and terminal facets F_i=r_i^perp in a real chart
geometry. Define the nonorthogonality graph H on these targets: distinct i,j
are adjacent exactly when r_i dot r_j is nonzero. Let the independent target
inputs x_i take values in a nonzero commutative ring R with1 and2=0.

Two moving scalar records P_1,P_2 descend monotonically through nested charts
and eventually reach ground. They may start at Hub with arbitrary linear
combinations of the source inputs. Proper births are also allowed if their
initial values are acquired from actual information local to their birth chart.
Each channel evolves independently in the following PRECISE sense: at chart C,
every update of its X coefficient row has the form

    P_p <- alpha P_p + l_C,                                (1)

where alpha belongs to R and l_C is supported only on original source lines
contained in C. Alpha may be zero or a zero divisor. There may be arbitrarily
many local updates, resets, stationary history copies and local acquisitions.
Terms independent of the selected x_i do not matter to their coefficient
equations and may be retained as arbitrary nuisance inputs.

The interface excludes a nonlocal X-bearing contribution from the OTHER
channel or from a receiver/ascending history carrying earlier nonlocal packet
information. Such a contribution changes(1). This is the essential scope
restriction. Direct local X reads, and reads of histories whose selected-X
projection is still local to C, are permitted. The theorem does not assume
that every granted local form is physically available for free: it rules out
the relaxed model even if all those acquisitions have been supplied and paid.

Every receiver i is generously given all local original X information in F_i
and all channel histories inside the downset of F_i. Its demanded X row is
exactly x_i. Initial global observations whose coefficients vanish on every
selected target column may also be granted. They disappear upon restricting
to the independent selected inputs; they supply no missing selected-X rank.
Arbitrary original Y inputs remain part of the full problem, but this necessary
X-coefficient theorem does not assume their physical values are zero.

## 2. First-entry observations suffice in this interface

Let a_p,ij be the coefficient of x_j in channel p's actual first value inside
the downset of F_i. If the channel is born there, use its actual birth value.
Once inside, every later local term in(1) is supported inside F_i. On columns
outside F_i, all later observations are scalar multiples of the first one.
Thus even a decoder granted every historical cache needs only one first-entry
row per channel, together with local X information. There exist decoder
coefficients lambda_p,i in R satisfying

    lambda_1,i d_1,i + lambda_2,i d_2,i = 1,                 (2)
    lambda_1,i a_1,ij + lambda_2,i a_2,ij = 0               (3)

for every edge ij of H, where d_p,i=a_p,ii. Equation(2) is the own-input
coefficient. Equation(3) follows because a nonorthogonal foreign input x_j is
not local to F_i. This only grants the decoder more access than an actual
single ascending Y path may possess, so impossibility here remains necessary.

## 3. The reciprocal edge identity

Fix a nonorthogonal pair i,j and one channel p. Suppose it first enters F_i's
downset no later than F_j's. At that first entry both x_i and x_j are nonlocal:
neither source line belongs to F_i. Every later chart on the descending path
lies inside F_i. Consequently no local update can add either input column.
Between the two first entries both coefficients are multiplied by the SAME
product t of through coefficients. Therefore

    a_p,ji = t d_p,i,       d_p,j = t a_p,ij.

Commutativity, without any division or invertibility assumption, gives

    a_p,ij a_p,ji = d_p,i d_p,j.                            (4)

If the order is reversed the same argument gives the same identity. Equal
first entries also satisfy it directly. Zero resets and zero divisors cause
no exception. A channel born inside the first downset has zero coefficients
on both inputs under its local-birth rule, again preserving(4).

## 4. A forced alternating decoder weight

Set u_i=lambda_1,i d_1,i. By(2), the second channel's own contribution is1-u_i.
Apply(3) at i and at j. Multiplying the two cross-cancellation equations and
using(4) for the two channels gives

    u_i u_j = (1-u_i)(1-u_j).

Expand the right side in the commutative ring and cancel u_i u_j. Hence

    u_i + u_j = 1                         for every edge ij. (5)

Along a path these weights alternate between u and1-u. An odd cycle forces
u=1-u, or2u=1. Characteristic two makes the left side zero, contradicting
1!=0. We have proved:

**Theorem.** If H contains an odd cycle, two independent channels satisfying
(1) cannot complete every selected target, even under the generous decoding
and local-acquisition relaxation above.

Conversely, if H is bipartite, the relaxed algebraic interface has two static
class-sum channels: each receiver subtracts the other inputs in its own color
class, whose roots are pairwise orthogonal and hence local to its facet.
Actual acquisition, movement, storage and erasure of these local sums remain
separate. Thus bipartiteness exactly characterizes the TWO-channel relaxed
commutative interface, not complete efficient physical source construction.

## 5. Actual native pentagon and the early-local-information deadline

The pinned111-root source contains the orthogonality cycle(92,36,54,38,55).
Its exact Gram matrix in that order has rows

    (4,0,2,2,0), (0,4,0,2,-2), (2,0,4,0,-2),
    (2,2,0,4,0), (0,-2,-2,0,4).

Its real rank is5. The nonorthogonality graph is the complementary pentagon,
with cycle order(92,38,36,55,54), so the theorem applies. All five indices
are pivots of the independently reviewed halfclass gauge: its three R core
rows vanish on them. Donor units8,9,16 also vanish there. Neither those
observations nor full stationary source-line retention removes the theorem's
selected-input hypothesis. The latter supplies local information already
granted by the relaxed model.

There is a field-independent geometric deadline. Each selected source line
is orthogonal to exactly TWO of the selected receiver normals. A chart
contained in three distinct selected receiver facets therefore contains NONE
of the five selected source lines. Once a descending packet has entered three
of these receiver downsets, no later pure local read can acquire a fresh
selected-X direction. Earlier nonlocal history imported from another packet
or ascending Y carrier is different and remains a possible coupled service.
Root independently identified this early/late geometry during the search.

## 6. Commuting blocks are covered; arbitrary blocks are not

If every coefficient block lies in one commutative characteristic-two matrix
algebra, apply the proof in that algebra with its identity matrix. This covers
scalar replication, larger characteristic-two field representations and
singular maps in a commutative algebra. It does not cover arbitrary blocks.

For a precise negative control, take two nonorthogonal targets with V=2.
Packet1 carries the first coordinate of each input, and packet2 carries the
second coordinate of each input. Each receiver takes its own coordinate from
each packet. This is an exact two-channel two-target decoder. Packet1's own
contribution is U=diag(1,0) at BOTH receivers, so U_i+U_j=0, not I_2.
The selector and embedding blocks do not commute. The verifier checks all
four source-to-output blocks and this failure of the commutative deduction.
It is not a noncommuting pentagon construction.

## 7. Consequence, evidence and attribution

A two-packet pentagon construction must leave a stated premise: for example
use cocharted packet mixing, Y-mediated nonlocal histories, noncommuting
blocks or more paid channels. None is assumed sufficient. This is discovery
milestone A, a universal structural result with an exact native application.
It is not milestone B: no complete source, supplier exponent or kappa follows.

An earlier exact exploratory search found2162 independent scalar profiles
and no pair, but that enumeration is no premise of this proof. A separate
random search allowing genuine coupling found no hit in its finite sample;
that failure proves nothing about coupled algorithms, coupled larger fields
or noncommuting blocks.

`verify.py` checks the native pentagon, edge-decoder cases over F2, F4 and
F2[t]/(t^2), odd-cycle inconsistency, a bipartite positive control and the
noncommuting negative control. Finite tests support rather than replace the
universal argument. Native SHA256:
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.

Credit the existing source/history normalization and Root's isolated-channel
theorem for the first-entry framework. Worker C developed reciprocity and
the alternating decoder weight. Worker A independently reviewed Sections1–4;
its distinct review is recorded separately. Native geometry and halfclass
authors retain their credit. Prepared for @CubeJerry with OpenAI assistance.
No new kappa.

Reproduction from the session root, substituting integrated paths as needed:

```sh
python worker-c/commutative-two-channel/verify.py --native worker-c/block-rigidity/BIT-NATIVE-WORD.json.gz --pivots worker-a/half-class-gauge/PIVOT-SEARCH-RANK2.json --output worker-c/commutative-two-channel/RESULT.json
python -O worker-c/commutative-two-channel/verify.py --native worker-c/block-rigidity/BIT-NATIVE-WORD.json.gz --pivots worker-a/half-class-gauge/PIVOT-SEARCH-RANK2.json --output worker-c/commutative-two-channel/RESULT-OPTIMIZED.json
```
