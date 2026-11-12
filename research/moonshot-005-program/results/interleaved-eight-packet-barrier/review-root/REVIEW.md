# Independent review of the minimal eight-packet obstructions

**Accepted within the stated interfaces. No new kappa.** The lead independently
read both proofs, reconstructed the finite source facts without importing the
author's verifier, and checked the complete caller inequality with separately
implemented directed rational arithmetic. This is review by a separate AI
agent, not a human or formal proof-assistant certification.

## Claims and exact limitations

The first theorem concerns exactly eight pure, full-field packets factoring
the scaled 104-row Gram block, with global packet delivery order. Its sharp
owned lower invoice is `6*9^t+8^t+7^t+1`, where `t=199/200`.
The second removes global delivery order and permits arbitrary retained pure
copies. Its combined owned/raw lower invoice is
`5*9^t+3*8^t+51*(1+7^t-8^t)` beyond the 400 direct raw routes.
Neither is a lower bound for mixed payloads, lower-volume fragments,
overcomplete factorizations, funded raw information, changed endpoint duties,
or a different reverse interface. A fresh unchanged-source Gram return is a
separate premise needed for the complete cost obstruction.

Finite exact identities and the arguments below establish the source-specific
universal claims. Tests alone are not being promoted to a transport theorem
or to an asymptotic multiplication theorem.

## Minimal factorization and all-volume reduction

For any characteristic-zero field and positive field dimension V, the
intermediate dimension 8V equals the target rank. Thus the decoder is
injective and its image is exactly the Gram image. Every V-column decoder
block is injective. If its recipient facets share a nonzero binary direction
z, the outside-facet rows annihilate its corresponding E8-coordinate map.
The independently computed rational locality ranks show that this is possible
only at one of the 16 omitted roots. Its annihilator has dimension one, so
the entire V-dimensional block equals that root direction tensored with an
invertible coordinate map. Its 52 recipients and facet intersection are forced.
Two cheap packets cannot share that root space, since this would contradict
injectivity of the full decoder. This reasoning does not presume scalar-only
packets or an orthogonal root basis. It would fail for an overcomplete space.

## Pure-copy genealogy and rank saturation

The pruning argument requires every transported copy to be invertibly
equivalent to the same full V-field. At a same-chart merge of such copies,
one incoming copy generates the outgoing pure copy by an invertible coordinate
transformation. Selecting that ancestor can remove moves but cannot introduce
an information source at a new chart. Retain all deliveries and regard later
copies as branches. This yields a rooted transport tree for a lower bound.

Intersecting visited charts loses at most one dimension per unit of descending
rank; ascending ranks cannot help. The 52 recipient normals span the entire
eight-dimensional annihilator of the omitted root. Total rank eight therefore
leaves no room for an ascending edge, redundant positive move, or dependent
new dual cut. The cut increments are independent globally, and every visited
chart contains the root line. At a first useful branch, normals delivered in
different branches occupy disjoint increment spaces modulo the branch chart's
annihilator. Thus a nontrivial branch decomposes the projected normal set.
A child without a nonzero projected normal would waste an independent cut
direction and contradict saturation of the eight-dimensional source span.

This does not justify pruning singular projections that later reassemble a
field, or mixtures of different packet payloads. Those remain explicit escapes.

## Binary spectrum and the parity exception

I independently obtained all 256 codewords for each of the 16 root supports,
with spectrum `0:1,20:3,22:48,24:28,26:96,28:28,30:48,32:3,52:1`.
Two nonzero disjoint codewords must sum to all-ones: their sum has weight at
least 40 and no other such nonzero codeword exists. Fixing one summand then
shows a decomposable subcode has exactly two one-dimensional summands. It
has dimension two and contains all-ones. Conversely that exception really
is disconnected. The equivalence to column-matroid decomposition follows
by an invertible row change of a generator matrix; zero columns are ignored.

For a chart containing the root line, projected-code dimension is chart
dimension minus one. All-ones occurs precisely when the chart contains
binary direction 511, because the kernel is the root line. Thus a useful
branch must be at dimension three, after six descending rank units, with
two rank-one children and no remaining positive movement. Its trunk contains
511 and cannot serve any odd source normal. Each leaf is a plane. This proves
the chain/parity-fork classification, including the disconnected exception.

## Temporal and raw-cost arguments

For global packet order, a third cheap packet requires two incomparable
delivery charts, retaining different earlier roots and excluding the other.
Their first common branch contains three omitted roots. The complete prior-pair
source patterns make that projected code connected, contradicting branching.
A second cheap packet needs at least two positive integer legs, giving the
sharp `7^t+1` price by concavity.

For arbitrary interleaving, all 10,920 quadruple/pair classes were checked
directly from the 104 source normals. Each has at least two actual receivers.
Choose a receiver in each class and orient its root pair toward the packet
read last. Monotonicity forces its later chart to contain both roots and
exclude the other two. A chain has capacity one distinct pair, since two
require incomparable charts. A parity fork also has capacity one: two pair
types identify its leaf planes and put 511 in the span of three omitted roots.
The common receiver independently checked for every triple excludes this.
Four packets cannot cover six pair requirements. This proves at most three
cheap packets without equating spatial order with time order.

A chain visits at most one distinct dimension-eight chart. At least 51 of
its 52 receivers therefore pass through a proper nonzero intermediate chart;
a parity fork has no facet exception at all. Those fields are distinct and
their endpoints differ by eight ranks. At intermediate dimension d in 1..7,
price is at least `d^t+(8-d)^t`, minimized at `1+7^t`. This proves the mandatory
raw fee. All other raw routes receive direct rank-eight cost. The zero-cheap
case is separate: no 51-field fee is asserted there, but eight rank-nine
packet prices exceed the combined lower invoice by a positive exact interval.

## Independent verification and negative controls

`check.py` imports no author verifier. It uses Fraction row reduction for all
511 locality matrices, unlike the author's modular-rank route; enumerates
all root spectra, preceding-pair patterns, 560 triple common classes and
10,920 quadruple/pair classes; verifies the actual 104 distinct receiver
endpoints and all 400 raw endpoint differences; and reconstructs the H4
caller from its pinned original invoice. Decimal-base integer 200th-power
bracketing supplies directed rational bounds independently of the author's
dyadic implementation. `output/RESULT.json` pins the reviewed proofs and
records both strict complete deficits. `PAIR-WITNESSES.json` records an actual
source role for each exact-pair class.

Negative controls retain the disconnected rank-two parity exception and
construct three retained chains with 156 deliveries on nested raw routes.
This has three cheap packets, disproving any unqualified extension of the
old owned-only global-order statement. The new combined invoice still holds.
The zero-cheap case is checked separately so the raw fee is not used without
its premise. An endpoint bug in this independent checker's initial power
bracket at rank one was caught by its exact inequality assertion and fixed
by choosing a strictly larger upper endpoint; no theorem or author artifact
was affected.

The fresh-return lower bound is an independently reviewed predecessor, not
reproved here. Under that interface the new arbitrary-order forward bound
leaves a deficit greater than 0.329751467288311 per native call. The programme
should prioritize mixed/current source information or a different representation,
rather than further retiming of the same pure minimal eight packets.
