# Interleaving still cannot fund the eight-packet fresh-return architecture

**Proved from the pinned source identities and predecessor lemmas below.
Independent review pending. No new kappa.** This extends the minimal-eight
packet barrier to arbitrary interleaving and retained stationary copies. Its
conclusion includes a mandatory raw refinement fee. It does not falsely carry
over the earlier owned-only tariff bound after removing global packet order.

## 1. Interface and dependencies

Retain the exactly-eight pure full-field minimal factorization interface in
`minimal-eight-packet-barrier/PROOF.md`, pinned SHA256
`184428adb93a4c62b14a106566bb7a5b6d358ef91fdc230c59159d9098853bfe`.
Use its full104-source locality theorem, field-volume extension, binary code
spectrum, and rank-eight copy-tree saturation argument. Those lemmas do not
require global packet order. This extension removes that order hypothesis.

Each of the eight packets may retain arbitrary stationary invertible copies
at earlier charts while another copy descends. Different packets may be
interleaved arbitrarily. Their physical receivers retain their independent
identities and their original monotone paths from the empty chart to distinct
dimension8 facets. Every informative owned move is paid; pure packet copies
remain invertible copies of the original full-field payload. Lower-rank
projections followed by reassembly, mixing distinct payloads, funded raw
piggyback, overcomplete factorizations and changed receiver representations
remain outside the interface.

Write t=199/200. A packet is cheap when its moment is strictly less than9^t.
The predecessor establishes that every cheap packet has rank mass exactly8,
is supported on the52 receivers of one omitted E8 root z, and has all visited
charts containing z. Its nonzero moves descend, and their dual cut spaces
are globally independent. Distinct cheap packets have distinct omitted roots.
These facts hold for every characteristic-zero field and every positive field
volume under the full-field transport hypothesis.

The new conclusions are:

1. At most three of the eight packets can be cheap, even with interleaving.
2. If any packet is cheap, at least51 actual raw first-Y paths must split at a
   proper nonzero intermediate chart, costing at least
   `51*(1+7^t-8^t)` beyond400 direct raw rank8 paths.
3. The combined unavoidable extra packet/raw price is at least

       5*9^t+3*8^t+51*(1+7^t-8^t).                         (1)

The complete favorable H4 caller still falls short of the exact-distance42
fresh-return requirement by more than0.329751467288311 per native.

## 2. Cheap packet broadcasts have only two spatial topologies

Let p=511, the all-ones vector of F2^9. Every source receiver normal has odd
weight, so every receiver facet excludes p.

The predecessor's52-coordinate evaluation code has proper nonzero weights
between20 and32, and the only larger word is the all-ones word. Therefore a
projected code is disconnected only when it has dimension2 and contains the
all-ones word. For a chart C containing z, its projected code has dimension
dim C-1 and contains the all-ones word exactly when p belongs to C.

Apply this to the first useful branch of a rank-eight copy tree. Independent
child cut spaces make its projected normal configuration disconnected.
Consequently that branch chart must have dimension3 and contain z,p. There
are only two rank units left after the trunk's six rank units. A useful branch
has at least two children, so it has exactly two rank1 children and no further
positive moves. Every trunk chart contains p and can serve no receiver.
Both children have dimension2. Among the three planes of C containing z,
the one containing p serves no receiver. The remaining two are

    <z,u> and <z,u+p>,    C=<z,p,u>.

Thus every cheap broadcast is one of the following:

* A spatial descending chain ending at the root line <z>, with optional
  stationary copies at any of its visited charts.
* One parity fork: a descending trunk to <z,p,u>, then the two dimension2
  leaves <z,u> and <z,u+p>. All52 deliveries occur at those leaves.

A spatial chain is not a chronological delivery order. A retained copy at a
larger chart may deliver after another copy has already descended and served
a smaller chart. The proof below uses only spatial comparability, never that
invalid temporal inference.

## 3. Every four omitted roots expose six exact-pair receiver classes

For every four-element subset Q of the16 omitted roots, and every pair a,b
in Q, the actual source contains a receiver whose cheap-root support within
Q is exactly {a,b}. The finite source certificate checks all1,820 quadruples
and all10,920 pair classes. Each class has at least two receivers.

The source also has at least seven receivers common to every three distinct
omitted roots. In particular p cannot lie in the span of any such triple:
a common receiver normal annihilates all three roots but evaluates p to one.
Both facts are checked directly from the104 actual source normals. No random
sample or assumption about a generic root system is used.

## 4. Four cheap packets would assign six pairs to four capacity-one packets

Suppose four cheap packets existed, with root set Q. For every pair a,b in Q,
choose an actual receiver in its exact-pair class. Among that receiver's a
and b packet deliveries, choose the later one. Its current chart contains
both a and b: the earlier delivery occurred at a chart containing the earlier
root and the raw receiver only ascended. Its chart excludes the other roots
of Q because its endpoint facet excludes them. Extra packets outside Q and
any intervening operations cannot remove this containment requirement.

A cheap chain packet a cannot be chosen for two different pair types {a,b}
and {a,c}. The first delivery chart contains b and excludes c; the second
contains c and excludes b. They are incomparable, whereas every chart of a
spatial chain is comparable. Retained stationary copies do not change that.

A cheap parity-fork packet a also cannot cover two such pair types. A leaf
serving as the later delivery for {a,b} has dimension2 and contains a,b, so
must equal <a,b>. Covering {a,c} at the other leaf would make the fork's
3-space equal <a,b,c>. But every parity fork contains p, whereas section3
excludes p from every three-root span. This is a contradiction.

Every cheap packet therefore has capacity at most one distinct exact-pair
type. The six pair types of Q must be assigned to their four packet endpoints,
which have total capacity four. Six is greater than four, proving that four
cheap packets are impossible. This argument permits arbitrary interleaving,
retained copies and simultaneous operations linearized at their common chart.

The count is not secretly two. Section7 gives a three-packet retained-copy
schedule that evades the earlier global-order obstruction.

## 5. One cheap packet already forces51 paid raw refinements

Fix any cheap packet. It has52 distinct receivers, each with initial chart
of dimension0 and a distinct final facet of dimension8.

A cheap chain visits at most one dimension8 chart, and that chart can equal
at most one of these distinct receiver facets. Every other delivery occurs
at a chart of dimension1 through7. A parity fork delivers only at dimension2,
so it has no endpoint-facet exception. Thus at least51 receivers have a
proper nonzero intermediate delivery chart.

If such a delivery chart has dimension d, the receiver's monotone raw route
has total ascent d before that observation and8-d afterward. Concavity gives
raw moment at least d^t+(8-d)^t. The symmetric concave function of d is smallest
on the integer interval1..7 at d=1 or d=7, so this is at least1+7^t. Relative
to the most favorable direct rank8 route, the excess is at least

    f=1+7^t-8^t =0.01497014607566438....

The51 affected raw fields are distinct. All other raw fields still cost at
least8^t because their fixed endpoints differ by eight dimensions. No unrelated
baseline raw fragmentation is charged here. The proof grants every other raw
path its direct rank8 price, every extra scalar operation free, and every other
new physical cost zero.

## 6. Complete favorable caller remains below the required return price

At most three packets are cheap. If at least one is cheap, the eight packet
moments are bounded below by5*9^t+3*8^t: granting three cheap packets is more
favorable than charging only one or two. Add the51 mandatory raw fees to obtain
(1). If none is cheap, the packet price is at least8*9^t, which exceeds (1)
at the fixed t; the exact directed verifier checks this case separately.

An equivalent positive histogram for the lower invoice is:

| Part | Rank counts |
|---|---|
| Raw fields | 349 at rank8,51 at rank7,51 at rank1 |
| Eight owned packets | 3 at rank8,5 at rank9 |

The raw profile has total rank3200, as required. It gives the entire benefit
of replacing every other original raw route by a direct rank8 call. The owned
profile grants each cheap packet a single rank8 call, even when its true chain
needs several legs. Both grants favor the proposed architecture.

Use the pinned H4 invoice
`b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248`,
remove the exact native raw profile and insert the above lower profiles. The
remaining moment per native is at most

    49.26950365220561....

The independently reviewed exact-distance42 fresh unchanged-source Gram-return
theorem, proof SHA256
`77c996ff9233f087a0e024c107b552f022adeca51cf5540c2487ef80cb2a2506`,
requires at least

    10*5^t =49.599255119493925....

Thus the strict deficit is greater than0.329751467288311 per native. Rational
200th-power bounds, not printed decimals, establish the inequality. This
excludes composing that return interface with any exactly-eight pure minimal
forward Gram-packet mechanism satisfying the present source contracts, even
when all packet deliveries interleave.

It does not exclude a changed return interface, useful source information at
the hub, mixed packet transport, more than eight packets, or genuine changes
to the source/current-row representation. All suppliers and foundations remain.

## 7. Three retained chains demonstrate the importance of the corrected scope

Take the three compatible omitted frame normals A=97,B=42,C=82 and let
U=<A,B,C>, dimension3. Retain a copy of each pure packet at U. Its moving copy
then descends to a cyclic pair plane and retains another copy there, before
descending to its own line:

    A: hub -> U -> <A,B> -> <A>
    B: hub -> U -> <B,C> -> <B>
    C: hub -> U -> <C,A> -> <C>.

Each has paid ranks6,1,1, hence rank mass8 and moment6^t+2<9^t. The stationary
upper copies may deliver later. Receivers requiring all three packets ascend
directly to U and receive all three retained copies. Pair-only AB receivers
receive B on its line and then A at the retained AB plane; similarly BC gets
C then B, and CA gets A then C. A singleton receives at its root line. Every
receiver then ascends to its original facet. These are valid exact source-chart
inclusions, and each required coefficient is delivered once.

The actual104 source has pattern counts {0:8,1:44,2:44,3:8}. Keeping the other
five root packets early gives owned profile {9:5,6:3,1:6}, whose moment is
68.3477920236882.... This has three cheap packets and costs less than the
previous globally ordered owned-only lower bound. It is not a counterexample
to that theorem: the deliveries interleave through stationary copies.

This is an exact abstract source-chart/copy schedule, not a claim of a fully
admitted physical word with all Clifford phases and lifecycle accounting.
Its explicit three-packet route budget, using the current actual prefix stops,
requires raw refinement fee2.147230098766814.... Even after unrelated raw
expenses are granted free, that particular candidate's fresh-return deficit
is about1.80120619817 per native. The universal bound in section6 is more
favorable and already rules out the complete architecture. Therefore no full
physical word for this particular candidate is built here.

## 8. Reproduction, review and next obligation

Run:

    python3 verify.py --repo REPOSITORY --minimal-eight MINIMAL_EIGHT_PACKAGE \
      --distance42 DISTANCE42_PACKAGE --output OUTPUT

The verifier pins the predecessor and exact source, checks all560 triple and
1,820 quadruple source cases, verifies the104 distinct empty-to-facet receiver
endpoints, constructs the retained-three abstract routes and proves the exact
complete invoice inequality. Mathematical review must independently examine
the chain/fork classification, the six-pairs/four-packets assignment and the
51-field raw-fee argument. Repeating this verifier alone is not that review.

The next consequential escape is no longer merely interleaving the same eight
pure packets. An overcomplete factorization, mixing distinct packet payloads,
funded current-row information, or a changed receiver/return representation
must be investigated with its full additional costs. The programme has ruled
out a substantial natural class without claiming a new complete exponent.

Prepared for @CubeJerry with OpenAI assistance. The predecessor preserves the
lead's spectrum/minimal-factor insights; this extension adds cheap-broadcast
classification, exact-pair capacity, mandatory raw accounting and the retained-
copy scope counterexample. No human or formal-proof review is implied.
