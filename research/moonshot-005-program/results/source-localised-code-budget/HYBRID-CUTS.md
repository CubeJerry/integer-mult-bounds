# Two valid extensions to hybrid paid/funded transport

**General algebraic accounting lemmas, not a new source-bound numerical exclusion.**

A geometric endpoint price cannot be charged wholly to new work when an actual packet uses funded edges. For nested spaces A⊂B⊂C with each adjacent rank difference1, a funded A→B MOVE followed by a new B→C MOVE costs only1 newly paid unit, while the geometric price between A and C is2^t>1. This counterexample already has one encoder, one decoder and an unchanged packet payload.

## 1. Retain the one-stage packet model and change its tariff

Fix a directed transport graph whose vertices include the required location and time/version data. A funded usable edge has new-price0. Each possible new complete-field MOVE has its own new-price r^t. Uncharged storage and local computation are included explicitly. The graph may overgrant capacities or retime selected funded occurrences, but those choices must be stated and must match its source-side-information grant.

Let h(c,d) be a lower bound on the minimum newly paid cost of an admitted path from a permitted encoding occurrence at c to a permitted decoding occurrence at d. If encoding or decoding may be chosen at several times, minimize over those allowed occurrences. For one fixed encoder and decoder chart per unchanged packet, the original acyclic rank proof remains valid with g(c,d) replaced by h(c,d): require, for every unabsorbed chart pair,

    sum_U lambda_U 1[D_c meets U and R_d meets U] <= h(c,d).

Then the new paid moment is at least sum_U lambda_U |U|. Each packet's actually new legs pay at least h; funded legs have not been charged. The sum argument requires every charged edge use to belong to that packet's priced transport. If one transmission is shared between several coded packet descriptions, use the actual transmitted field as the packet or a network-capacity argument instead.

A shortest-path calculation on a sufficiently permissive graph supplies a suitable lower tariff: rounding all positive edge prices downward before taking shortest paths remains conservative. A proposed lower tariff can also be certified by source-dependent distance potentials phi: phi(v)-phi(u)<=price(u,v) on every allowed edge. Funded edges require phi(v)<=phi(u). Thus a positive potential jump may never be assigned to a free edge.

For the present source, the expanded S certificate does NOT retime neutral public helper MOVEs. It retains their original event times and freely retimes only the stated owned/main arcs. A timeless graph that also retimes neutral helpers is a further relaxation and needs a correspondingly enlarged side-information analysis. In particular, new zero-price coded paths can supply individual coordinates; their effects cannot be hidden by retaining an older, smaller S matrix.

This extension still does not allow a packet to collect new source terms at later stations or use changing versions to serve several decoder stops. Such operations need the network theorem below. No claim is made that the old74 weights satisfy the hybrid tariff constraints.

## 2. Weighted information cuts with finite funded capacities

Use a fixed causal linear dataflow network for the proposed component. Its independent input vector is x. Vertices include physical location/time and the actual retained data versions. A directed edge carries at most c_e complete V-coordinate fields. Unlimited local computation, storage or granted information must be represented as genuinely free connections or as explicitly available initial data.

For a receiver-side vertex set Omega, let B_Omega x be all initial or granted information present on that side. Let D_Omega x be the collection of required output rows at terminal vertices on that side. Choose cuts so that every other entering connection is accounted for as a finite-capacity funded or new edge; no uncounted local/storage edge may enter the cut.

Define the conditional target rank deficit

    d_Omega(V) = [rank([B_Omega;D_Omega]) - rank(B_Omega)] / V.

For scalar source matrices tensored with I_V this is an integer independent of V. Every cut satisfies

    d_Omega(V) <= sum_(funded e entering Omega) f_e
                    + sum_(new e entering Omega) x_e,                 (1)

where f_e is the actual available funded capacity and x_e is the number of new complete-field uses. To prove (1), grant the receiver side the entire transcript of every entering edge. All its internal values and required outputs are then linear functions of that transcript and B_Omega x. Each incoming V-field increases rank by at most V. Outgoing feedback does not change this argument: the causal transcript is still the only extra information entering the receiver side.

Take nonnegative weights lambda_Omega. Define the load of an edge by

    w_e = sum_(Omega crossed into by e) lambda_Omega.

If every allowed new edge satisfies w_e<=r_e^t, summing (1) yields the rigorous new-price bound

    sum_(new e) x_e r_e^t
       >= sum_Omega lambda_Omega d_Omega(V)
          - sum_(funded e) f_e w_e.                                  (2)

Every funded edge is explicitly credited once through its capacity term. It is never billed as new work. If a funded occurrence has already been consumed, its remaining capacity is0. If it is reserved for another duty, either omit it or include that duty in the complete joint network. Merely finding the same geometric arc does not create another funded use.

The proof permits arbitrary linear coding, several acquisition stops, several receiver stops, mixing, splitting, changing packet versions and causal feedback. Its units are actual edge transmissions, so it does not incorrectly limit a changing packet lifetime to rank V.

## 3. Unlimited free edges and side-information cautions

If a class of funded edges is granted unlimited reuse, its f_e is unbounded. For a finite useful bound from (2), every positive-weight cut must have w_e=0 on those edges. Equivalently, its receiver side must be closed under incoming unlimited free connections. Contracting strongly connected free components is useful, but directed predecessor closure is still needed after contraction. This is the cut analogue of the monotonicity condition on free-edge distance potentials.

The deficit d_Omega is not automatically the cardinality of an acyclic side-information set. A cut grants the entire receiver-side region joint use of its initial data; this may include more side information than any one receiver has in the original index-code model. The correct conditional rank must use the actual B_Omega. Conversely, using |U| without proving a triangular fitting-matrix reduction for this particular cut can overstate its deficit.

One example: receiver1 initially knows q2 and wants q1; receiver2 knows nothing and wants q2. Their side-information graph is acyclic and ordinary shared-broadcast index coding needs two scalar dimensions. If the new network freely lets receiver1 send q2 to receiver2, only one broadcast q1 remains necessary. A receiver-side cut containing both receivers must account for its local knowledge q2 and this free link; it cannot simply demand two additional dimensions. The original source S graph already incorporates specific coordinate reachability overgrants, but further coded transit must still respect the declared network.

## 4. What would constitute a source certificate

A hybrid certificate should pin: the source occurrence list and their remaining capacities; the allowed new MOVE types; physical times and chart inclusion; initial/granted input rows B_Omega; required output rows D_Omega; nonnegative rational cut weights; and every new-edge load inequality. Verify the inherited-capacity subtraction and all target ranks exactly. For an unrestricted geometry, a finite list of tested new edges is insufficient unless an additional geometric argument bounds every other admissible edge.

The present review proves (1)-(2) and the shortest-path replacement principle. It does not supply positive cut weights giving an H4 exclusion for the actual hybrid source model. That remains a concrete next optimization and certificate task. The wholly paid98.992356 bound may be retained in its narrowed model while the hybrid architecture is tested separately.

Prepared with substantial OpenAI assistance. This is a new scoped accounting lemma and handoff, with no source construction, complete supplier or kappa claim.
