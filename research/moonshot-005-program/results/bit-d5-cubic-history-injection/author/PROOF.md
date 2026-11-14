# A reversible D5 cubic-history injector on the actual BIT source

**A source-bound partial interface, an exact finite code theorem, and an endpoint control. No complete supplier and no new kappa.**

## 1. What is established

Let D=F92 intersect F54 intersect F38 in the source-pinned native geometry. It has real rank5 and contains18 native source lines. Let C be the rank9 canonical binary row code, Q2 its coordinatewise degree-at-most-two closure, and Q3 its degree-at-most-three closure.

The exact local code

    L = Q3 intersect {vectors supported on the native lines in D}

has dimension5. It has zero intersection with Q2 and is a punctured, doubled even-Eulerian code of K5. In particular every z in L has equal coefficients at inputs1 and18.

For each of the31 nonzero binary z, a literal source word acquires z at D, reversibly inserts it into two original ascending carriers, supplies the two incomparable fork caches, restores all111 original X VALUES, and completes original Y92,Y54,Y38. It leaves the same two descending packet lifetimes co-located at D with

    P=h'+z, Q=u'+z,
    h'=x36+x23+x18, u'=x55+x1.

Their initial Hub values and their XOR are unchanged. No owned record ascends, and no additional owned record moves. Source routes consumed by acquisition are explicitly recorded and retained point copies are actual records.

This is a change of carried code, not a prefix rank increase: G_z and the prior G_0 both have dimension4, their intersection has dimension3, and their combined span has dimension5. Their new quotient direction is exactly z modulo G_0. The source does not yet use that direction to complete a global decoder.

A separate control removes z at D and executes the admitted second fork, completing the original eight targets. Its transient carried history has dimension7 rather than6. That unused transient mode earns no supplier or decoding credit.

## 2. The graphic code inside the D5 root section

Here are five mutually orthogonal double-coordinate vectors:

    a0=(1,0,1,0,1,-2,-1,0)
    a1=(1,0,1,0,-1,0,1,-2)
    a2=(1,0,-1,-2,-1,0,-1,0)
    a3=(1,2,-1,0,1,0,1,0)
    a4=(1,-2,-1,0,1,0,1,0).

Their Gram matrix is8I. The20 lines represented by (a_i+a_j)/2 and (a_i-a_j)/2, 0<=i<j<5, form the standard D5 root-line configuration. Eighteen are actual native lines. One sign is absent on edge{0,4}, and one sign is absent on edge{1,2}. Every edge still has at least one native sign.

Index the ten unordered pairs by the edges of K5. An edge vector c belongs to the even-Eulerian code E if every vertex has even incident c-sum and the total edge c-sum is even. Over F2 this says its selected edges form an Eulerian subgraph with an even number of edges. The incidence constraints have rank4; the edge-parity constraint is independent, as witnessed by an odd triangle. Thus dim E=10-5=5.

Map an edge coefficient to BOTH of its signed D5 root lines, then delete the two absent sign coordinates. This is PUNCTURING the doubled code, not shortening it at the omitted coordinates. The map is injective because every edge retains a native coordinate. Its image has dimension5.

The31 nonzero full edge codewords are the15 four-cycles, their15 six-edge complements, and all ten edges. A doubled four-cycle has real support in four coordinate axes and spans that rank4 space. This remains true after the native puncture: every cycle edge remains present and at least one retains both signs, so those two axes are obtained first and connectivity supplies the others. The six-edge complements and full graph analogously span all five axes. The native weight enumerator is

    1 + 2 t^6 + 8 t^7 + 5 t^8 + 5 t^10 + 8 t^11 + 2 t^12 + t^18.

The source-bound code certificate proves that this image is exactly L. Starting from the actual111 canonical rows, exact binary elimination gives

    dim C=9, dim Q2=36, dim Q3=84,
    rank(projection of Q3 outside D)=79.

Hence dim L=5. Every doubled even-Eulerian generator belongs to Q3, checked against the full coordinatewise-product span. Since the image also has dimension5, equality follows. The combined rank of Q2 and L is41, so Q2 intersect L=0. CODE-CERTIFICATE.json retains the full binary bases and projected echelon certificate; code-check.js reconstructs every rank and membership from the authenticated integer roots.

Native inputs18 and1 are the two signed roots of edge{3,4}. Therefore

    z18=z1

for EVERY z in L. This equality is the reversible source-acquisition condition, not a numerically fortunate choice of one mode.

The example used in the emitted words is the four-cycle0-1-3-4-0:

    z=x1+x11+x18+x23+x35+x41+x57.

Its four source coordinates outside the eight-target predecessor are11,35,41,57. Its support has rank4, but the simultaneous acquisition/continuation paths below meet at D of rank5. Support rank alone is not an invoice.

## 3. The reversible two-carrier recoding

Let x denote the vector of all original X values, let u=e18+e1, and let z also denote the binary row defining the local form. Since zu=z18+z1=0, the rank-one operator

    T=I+u z

satisfies T^2=I over every characteristic-two field. Explicitly T adds the SAME z(x) to coordinates18 and1. It preserves the entire original input vector invertibly; it is not the noninvertible operation of replacing two independent records by two pure copies of z.

This remains an ordered algebraic identity for block forms Z with Z1=Z18: U has identity blocks at18 and1, ZU=0, and (I+UZ)^2=I. The emitted costed words use binary coefficient1 and lift componentwise to every widthV. A more general weighted block implementation would need its own ordinary-operation invoice.

The actual source uses the two carriers only after acquiring one stationary Z=z at D while all participating originals are still pure. It first makes the predecessor accumulator X18=x18+x23. Then it adds Z to that accumulator and to original X1. Their values are

    X18=x18+x23+z,   X1=x1+z.

They follow DIFFERENT actual upward branches:

    X18: D -> E_A -> F92 -> Hub,
    X1:  D -> E_B -> F92 -> Hub.

They consequently supply S1 at E_A and S4 at E_B. Their z contributions cancel in p at D and W at F92. No single unchanged original is assumed to visit both incomparable rank6 charts.

At Hub undo X18+=X23 first. The remaining original recoding is exactly T. It is undone without a Hub ancilla by an ordered conjugated shear. Put S=I+e1 e18^T; then S e18=u and S u=e18. The conjugated row zS has zero coefficient at18. In literal ADD order:

    X1 += X18;
    X18 += X_i for every i in supp(z) except18;
    X1 += X18.

This is T again and therefore restores the originals. The exclusion of18 is legitimate because z18=z1. All inputs read here are actually at Hub. The order is fixed; no noncommuting blocks are exchanged.

If the two binary coefficients at18 and1 differ, then zu=1, so T u=0 and T is singular. The current two-carrier restoration cannot be extended to such a row by wishful cancellation. The code condition is therefore doing real work.

## 4. Literal acquisition and original access

The construction extends the already emitted nested fork whose eight selected inputs are

    92,36,54,38,55,23,1,18.

Original X23, X18 and X1 first supply their pure future correction caches on their predecessor routes, then wait at D. Every additional original X in supp(z) also ascends from its actual source line to D. Before each such extra original moves, the word initializes a stationary point copy on that line and copies the actual input into it.

Only when all required originals are co-located at D is Z acquired by the displayed sum of source ADDs. Then Section3's recoding and branching occur. Unchanged extra originals continue D->Hub, the two modified carriers take their distinct branches, and the Hub inverse restores every original X before either packet is born.

The example consumes precisely four additional original paths:

    X11, X35, X41, X57: line1 -> D5 -> Hub8.

Their point copies remain at the original lines. A stationary owned point copy cannot later ascend to an arbitrary correction chart. Thus this is not a promise that the original higher-chart access remains available. Such future acquisitions must already have been prepared or be newly paid.

The first fork's initial packet values remain

    P0=x92+x36+x55+x23+x18+x1,
    Q0=x92+x36+x54+x38+x55.

They do not contain the four new inputs. The actual fork acquires their cubic combination through its later cache exchanges. It completes Y92,Y54,Y38 exactly and clears the seven old stationary owners. At the final injected handoff:

* P=h'+z and Q=u'+z are actual live records at D.
* Z=z is retained at D.
* The five actual pure second-fork caches from the predecessor are still present, including its off-D x55 cache.
* The extra point copies are still present.
* Every original X value is unchanged; the eight predecessor sources and the explicitly listed extra sources are at Hub.
* Every other original X is untouched on its source line.
* Only the three declared Y targets are completed. All other Y records retain their original values at ground.

For the example this means12 original X paths have reached Hub and99 are untouched. There are12 live owners. Both packet lifetimes are continuous; no new full packet has been created.

## 5. Exact effect on the carried code

Let

    h=x36+x23+x18,  u=x55+x1,
    A=P0, B=Q0.

The complete post-Hub carried X rowspace through the injected handoff is

    G_z=span(A,B,h+z,u+z).

The exact replay confirms rank4 for every one of the31 nonzero binary modes. At z=0 this is the admitted predecessor's rank4 handoff.

The common three-dimensional space is span(A,B,h+u). Every nonzero element of L has native weight at least6. Yet D intersects the predecessor's eight input coordinates only in{1,18,23}. Therefore L is disjoint from every space supported on those eight coordinates. In particular z is not in G_0 for nonzero z.

It follows that G_z and G_w, z!=w, intersect precisely in the common3-space, have combined dimension5, and differ by the quotient direction z+w. The32 actual binary choices including the predecessor form an affine family of4-spaces in the9-space G_0+L. CODE-FAMILY.json checks all496 distinct pairs.

This is a rank-preserving change of code. It does not claim five simultaneous new widthV transmissions, a rank9 fitting for the full111 graph, or a complete global broadcast. One selected z is injected per literal call. The five-dimensional local code describes the available choices.

## 6. Complete incremental bill

Let w=weight(z), alpha=z1=z18 in{0,1}, beta=z23, and

    e=w-2 alpha-beta

be the number of additional source originals outside the predecessor eight.

At the injected handoff, relative to the predecessor handoff, the source adds:

    e+1 INIT, e retained point copies plus one Z record;
    e+2w-alpha+4 ADD;
    2e original upward MOVEs, with profile e[4]+e[3];
    no additional CLEAR yet and no additional descending MOVE.

The prefix itself has

    INIT=15+e, ADD=48+e+2w-alpha+4,
    MOVE=39+2e, CLEAR=7, live-owned=8+e.

The two original packet values at Hub and all three completed Y endpoints are unchanged. All31 modes have been replayed against all222 independent original input columns.

For an endpoint control, add Z to P and Q at D, clear Z and the retained point copies, and execute the predecessor's second fork. This completes the original eight targets, clears every owner, and owes no dirty endpoint on those targets. Its total ordinary/ownership bill is

    INIT=CLEAR=15+e,
    ADD=69+e+2w-alpha+6.

After closing the remaining original endpoints, its complete profile is

    Q_control = Q_nested + e([4]+[3]-[7]).

Rank length stays1570. This does not say extra originals moved for free: their two upward jumps replace the direct rank7 jump in the CLOSED accounting control. Their earlier consumption remains a continuation limitation.

For the preferred mode w7,alpha1,beta1,e4, the literal prefix uses19 INIT,69 ADD,47 MOVE,7 CLEAR and retains12 owners. The endpoint control uses19 INIT/CLEAR,92 ADD and closed profile

    31[1]+5[2]+15[3]+4[4]+3[5]+3[6]+205[7].

At t=199/200, its movement moment is enclosed at

    1555.433407295959919337971473189038...

The increment over the nested control is

    4(4^t+3^t-7^t)
    =0.094850311389818684582407690250...

with exact rational interval endpoints retained in RESULT.json. The preferred word's ordinary increment is23 ADD and five INIT/CLEAR. No ownership, storage or erasure duty is omitted.

## 7. Verification and remaining theorem

The author checker validates exact source charts, every actual ADD location, monotone direction, restoration before packet birth, all222 original columns, every retained owner value and every dirty retirement. It passes for every nonzero binary mode, not just the displayed example. It rejects omission of either carrier injection, source capture, point-copy capture, a conjugating restoration ADD, the endpoint uninject, or the carrier-equality hypothesis.

The endpoint control deliberately removes the useful new quotient direction before finishing. It is a correctness and accounting control, not productive decoding. The consequential next obligation is to use the injected cubic direction in a complete joint code/decoder while retaining the unserved original access and paying all routes. Independent repetition of these small forks cannot satisfy the complete target budget.

The construction does not establish a new movement exponent, covered BIT saving, completed BIT saving, compatible complex supplier, uniform compiler, precision service or unconditional theorem. All five foundational assumptions remain explicit.

Source qualification: the integer roots are the exact reconstruction in Git blob8eba43d142c819c206dce5df87ea4571aaead287 from the admitted84-signature certificate, ultimately pinned to native gzip SHA25651203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78. This session's local executor was unavailable; no fresh gzip replay is claimed.

Credit @CubeJerry, retained native/caller and fork contributors, Worker C for independent D5/source review and the preceding off-D correction chart, and the construction worker for the graph-code identification, paired involution, literal injection source and full bills. Substantial OpenAI assistance; no independent human or formal proof-kernel audit is claimed.
