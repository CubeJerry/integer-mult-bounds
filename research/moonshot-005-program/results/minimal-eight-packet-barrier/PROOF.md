# A sharp tariff barrier for any eight globally ordered pure Gram packets

**Proved subject to the exact source identities certified here. Independent
review pending. No new kappa.** The result permits any minimal factorization
of the104-row scaled E8 Gram block, not only an orthogonal decoder basis. It
permits arbitrary ambient delivery charts and arbitrary owned copy networks.
The actual late-two word attains its owned packet lower bound. The remaining
escape must change an explicit interface below.

## 1. Precise interface and theorem

Fix the native source SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
There are104 first-X/first-Y pairs. Write n_i in F2^9 for their distinct
weight3 or7 source normals, a_i in Q^8 for their integer E8 roots, and A for
the8-by104 matrix of root columns. Each actual first-Y output facet is
n_i-perp. Its raw path begins at the empty chart and only ascends. The
existing coupled receivers multiply the decoder row by c_i=1/2; ordinary
receivers have c_i=1. Let Lambda=diag(c_i). The packet block is

    K=Lambda A^T A/8,    rank K=8.

For every field F of characteristic zero and every positive field volume V,
consider exactly eight packets of dimension V and a factorization

    K tensor I_V = D E,
    D: F^(8V) -> F^(104V),   E: F^(104V) -> F^(8V).

Packet j starts at the dimension9 hub. It and any copies remain pure copies
of that packet, up to invertible transformations of its V coordinates. They
may use any finite nested owned moves, copies, tours and retirements. Each
informative move transports a whole dimension-V field and is charged r^t,
where r is its positive integer chart rank and t=199/200. There is no free
information source away from the hub. Mixing distinct packet payloads,
fractional-volume fragmentation and using funded raw fields to carry packet
information are outside this interface.

Packet j is delivered to each physical receiver i for which its decoder
block D_ij is nonzero. All deliveries of one packet finish before deliveries
of the next begin. Receiver fields retain their original identities and
endpoint facets and ascend monotonically; no recoding or swapping of their
independent endpoint duties is granted. The theorem allows all intermediate
and delivery charts in the ambient F2^9. In particular, delivery charts need
not lie in the binary span of an orthogonal root frame.

**Theorem.** Under this interface the eight owned packets have total moment

    P_packet >= 6*9^t +8^t +7^t +1.                         (1)

No more than two packets can cost strictly less than9^t. If two do, in their
order the first costs at least8^t and the second at least7^t+1. The actual
late-two construction attains the right-hand side as its owned packet
profile {9:6,8:1,7:1,1:1}. This is a sharp owned-packet bound within the stated
interface, not a lower bound for all multiplication algorithms.

All raw refinements, extra scalar operations, packet storage, precision and
compilation expenses can only increase a complete caller's costs. They are
granted free when deriving the optimistic impossibility statement in section8.

## 2. Source locality forces every cheap minimal packet to be an omitted root

For each nonzero binary chart line z, form the root matrix with columns a_i
such that n_i dot z=1. Exact calculation over the full104-source domain gives:

* It has rank8 for495 of the511 nonzero lines.
* It has rank7 for precisely the16 source-omitted E8 root normals
  [7,25,42,52,67,76,82,97,104,127,137,162,266,289,448,491].
* For each of those16 lines, its one-dimensional annihilator is the real root
  direction a(z).

The verifier checks all511 matrices. It does not rely on floating rank.
Every root row has Euclidean norm sqrt8; every k-by-k minor for k<=8 has
absolute determinant at most8^(k/2)<=4096. The verifier uses the prime65537,
which exceeds this bound, so its modular rank is exactly rational rank. The
rank7 null vector is checked with integer dot products. The conclusion
therefore persists under every characteristic-zero field extension.

Because the factorization has exactly8V intermediate coordinates and rank8V,
D has full column rank and its range equals range((Lambda A^T) tensor I_V).
Each packet block D_j has rankV. Hence there is a rankV map W_j into F^(8V)
with

    D_j=((Lambda A^T) tensor I_V) W_j.

Suppose its recipient facets have a common nonzero line z. All receivers with
n_i dot z=1 have D_ij=0. The locality matrices above therefore force z to be
one of the16 omitted roots, and force the range of W_j into

    span(a(z)) tensor F^V.

This space has dimension V, so equality holds. Thus

    W_j=a(z) tensor T_j

for an invertible V-by-V matrix T_j. Its recipient support is exactly the52
receivers where a_i dot a(z) is nonzero. Their facets intersect in exactly
<z>. Conversely a decoder block outside these16 root spaces has recipient
facet intersection {0}. Two packets cannot have the same omitted root space,
because D has full column rank. These conclusions allow arbitrary coordinate
mixing within each packet and do not presume an orthogonal encoder.

This step is where exactly eight full fields matters. For more than eight
packets the decoder range need not equal the Gram range, and individual
columns can have components that cancel in the full factorization.

## 3. Broadcast rank and the equality case

Consider one pure packet network. Its paid rank mass R is the sum of its move
ranks. A copy genealogy connects its hub source to every delivery chart.
Repeated routes or a merge of copies of the same pure value can be pruned
when obtaining a lower bound: select one nonzero ancestor for each pure copy,
retain every necessary delivery and collapse same-chart zero-cost edges.
Equivalently work with a rooted copy tree; discarding extra positive moves
can only reduce the claimed lower bound.

The codimension of the intersection of all delivery charts is at most R.
For a direct proof, begin with the full chart and traverse a rooted tree.
Adding a smaller nested chart reduces the current intersection dimension by
at most that edge rank; adding a larger nested chart cannot reduce it. Thus
R>=8 for a root packet and R>=9 for every other minimal-factor packet.
Concavity gives

    sum_e r_e^t >= (sum_e r_e)^t.

Call a packet cheap when its moment is strictly below9^t. Its integer rank
mass must be exactly8, and section2 makes it a unique omitted-root packet.

The equality R=8 has a useful rigid consequence. Write B(C)=C-perp in the
binary dual space. The52 recipient normals span the8-dimensional space
z-perp, because their facets intersect in <z>. Along a descending tree edge,
B(C) gains a subspace of dimension equal to the edge rank; an ascending edge
creates no new dual directions. The global span of all visited B(C) has
dimension at least8. Since the total rank budget is exactly8, all useful
edges must descend and every new edge subspace is independent of all edge
subspaces already introduced. There can be no additional paid cycle,
ascending move or unused branch. Their global dual span is exactly z-perp.
Consequently every visited chart contains z.

At a branching chart C, the dual increments in its distinct child subtrees
are therefore independent modulo B(C). The restriction to C of a receiver
normal delivered in one child subtree belongs only to that child's increment
space. At the first branch, receivers served on the preceding trunk restrict
to zero. Every retained child has some nonzero restricted receiver normal:
otherwise its independent cut directions would be absent from the span of
all52 source normals, contradicting equality of the two8-dimensional spans.
Thus a first useful branch forces a nontrivial direct-sum decomposition of
the projected receiver-normal configuration at C.

## 4. A small binary-code lemma rules out those projected decompositions

Fix an omitted root z and its52 recipient normals. Its binary evaluation code

    C_z={ (n_i dot u)_(i in support(z)) : u in F2^9 }

has dimension8, kernel <z>, and contains the all-ones word p. Its exact weight
spectrum, identical for all16 roots, is

    weight:     0  20  22  24  26  28  30  32  52
    count:      1   3  48  28  96  28  48   3   1.

The verifier evaluates all512 binary directions, deduplicates the256 words,
and checks this spectrum. There is a short universal consequence. If two
nonzero codewords u,v have disjoint supports, their sum has weight at least40.
The only such codeword is p, so u+v=p. In particular, every proper nonzero
codeword is support-minimal: splitting it into two disjoint nonzero codewords
would give weight at least40, contradicting its maximum weight32.

Let a subcode U of C_z have a disconnected nonzero coordinate matroid. This
means it splits into nonzero code summands on disjoint coordinate blocks.
Choose nonzero u and v in two summands. They must be complements, u+v=p, so
there can be no third nonzero summand. Keeping v fixed shows that the first
summand has only one nonzero word; keeping u fixed does the same for the
second. Thus

    a disconnected subcode has dimension2 and contains p.   (2)

Conversely a dimension2 subcode containing p decomposes into the two nonempty
parallel coordinate classes defined by any other nonzero word. The all-ones
exception must not be omitted. In particular every subcode of dimension at
least3 is connected, and a dimension2 subcode excluding p is connected.

The equivalence with the projected normal configuration is elementary: a
generator matrix for the evaluation subcode has those restricted normals as
its columns. A direct-sum decomposition of their span allows a basis change
to block support on disjoint coordinate sets, and conversely. Zero columns
are ignored when speaking of connectedness.

## 5. Every chart containing three distinct omitted roots is connected

For distinct omitted roots z,a,b, restrict attention to the52 receivers of z.
The pair of evaluations (n_i dot a,n_i dot b) takes all four binary values.
Each value occurs at least7 times. The verifier checks all16*C(15,2)=1680
source cases. This also shows a and b remain independent modulo <z>.

Let C be any ambient chart containing z,a,b. The restricted evaluation code
has dimension dim C-1, since its kernel is exactly <z>. If dim C>=4, section4
makes it connected. If dim C=3, then C=span(z,a,b). Its evaluation code is
span(eval(a),eval(b)) and does not contain p: a receiver with both evaluations
zero defeats every combination. Thus it is connected in this case as well.

This proves the needed assertion for every ambient chart, without enumerating
subspaces or restricting charts to a fixed root frame. As separate exploratory
corroboration, an exhaustive implementation checked1,770,352 distinct charts
from4,746,000 containing-pair cases and found the same result. That large
census is not needed as a dependency of this proof; the tiny spectra and1680
pattern checks establish the complete finite source input to the argument.

## 6. No third cheap packet can occur in global delivery order

Suppose three cheap packets occur, with distinct omitted roots a,b,z in that
order. All charts visited by the first two packets contain their respective
normal lines by section3. The receiver paths ascend, and all earlier packet
deliveries finish before the current packet begins.

Among z's receivers there is one that receives a but not b, and another that
receives b but not a. At their z deliveries, the first current chart contains
a and excludes b; the second contains b and excludes a. Both contain z. The
exclusions follow from their actual endpoint facets, not a chosen retiming.
These two delivery charts are incomparable. A descending rank8 copy tree
cannot put them on one trunk, so it has a useful branch. Its first useful
branch chart C contains both receiver charts below it, hence contains a,b,z.

Section3 says this first branch makes the projected normal configuration at
C disconnected. Section5 says every such C has a connected configuration.
This contradiction proves that a third cheap packet cannot exist. Notice
that this argument imposes no prior alignment assumption on arbitrary
packets: alignment of a cheap packet follows from rank saturation itself.

## 7. The exact price of the two permitted cheap packets

The first cheap packet costs at least8^t. If a second exists, one of its
receivers has already received the first, so its current delivery chart has
dimension at least2. The second packet cannot use just one positive-rank move:
then every receiver would be served at that single chart, contradicting the
fact that all52 facets intersect only in its own normal line. It therefore
has at least two positive integer move ranks with sum at least8.

For 0<t<1, a fixed integer rank sum distributed over at least two positive
parts has smallest power sum when the parts are as unequal as possible.
Consequently its price is at least7^t+1. All other packets cost at least9^t.
At the fixed exponent,9^t>7^t+1 and9^t>8^t; directed rational power bounds
verify both inequalities. Fewer cheap packets therefore cannot lower (1).
The actual late-two word supplies the matching paid profile.

The decoder roots need not be orthogonal. For any invertible root-column
matrix W, the scalar factorization

    D=Lambda A^T W/8,    E=W^(-1) A

is exact. The verifier independently counts8,766 independent8-root bases from
the16 omitted directions and checks one genuine nonorthogonal example
[25,42,52,67,76,82,97,127] with a full rational inverse and all104^2 decoder
identities, including the coupled half factors. The theorem is more general
still: section2 reduces every cheap block of any exactly-eight factorization
to an omitted-root direction without prespecifying its basis.

## 8. End-to-end consequence under the fresh Gram-return interface

Use the existing complete H4 invoice with SHA256
`b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248`.
Remove its exact native raw histogram and grant all400 raw fields direct
rank8 paths. Add only the packet lower bound (1), charging all other new
expenses zero. This is more favorable than the actual source caller.
Its remaining moment per native has value

    49.03359816976095....

The independently proved exact-distance42 fresh unchanged-source Gram-return
theorem requires at least10*5^(199/200), with value49.599255119493925.... The
strict deficit exceeds0.5656569497329735 per native. The verifier records
rational directed enclosures from200th-power integer comparisons; no decimal
rounding determines acceptance.

Hence replacing the present eight forward Gram packets by another globally
ordered exactly-eight pure-packet factorization cannot make that complete
fresh-return architecture affordable. This statement retains both interfaces:
the new theorem is about the forward minimal packet mechanism; the separate
distance42 theorem is about fresh unchanged-source reverse packets. It does
not say that the current partial rank88 word already has only a rank8 reverse
residual, and it does not bypass either strict supplier or any foundation.

## 9. Verification and remaining escapes

Run:

    python3 verify.py --repo REPOSITORY --distance42 DISTANCE42_PACKAGE --output OUTPUT

The script verifies the exact source and invoice pins, all511 locality ranks,
all16 code spectra, every preceding-pair pattern, one nonorthogonal dual
factorization, the complete omitted-root basis census and the favorable
invoice. Negative controls preserve the actual disconnected rank2 all-ones
exception and exhibit a non-root decoder with no shared nonzero chart.
Mathematical review of the copy-tree saturation and code-decomposition steps
is separate from running this verifier.

Meaningful escapes remain: interleave deliveries of different packets; use
more than eight packets; mix distinct packet payloads during transport; use
funded raw information or actual retained common history; fragment field
volumes under a correctly changed invoice; alter the receiver representation
while retaining all independent endpoint duties; or change the target map.
These are obligations, not admitted constructions. No new complete kappa
follows from this scoped obstruction.

Prepared for @CubeJerry with OpenAI assistance. The lead agent supplied the
weight-spectrum shortcut and the extension from root bases to arbitrary
minimal Gram factorizations. This worker supplied the rank-saturation/copy-
branch obstruction, the exact source certificates, the independent spectrum
check and the large optional quotient census. Existing source, late-two and
exact-distance42 packages retain their predecessor credit.
