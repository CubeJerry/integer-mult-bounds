# Three mixed-Y acquisitions on one cyclic shared schedule

## Exact result

**Proved finite construction; no complete supplier and no new κ.** In the pinned actual 111-root BIT source, there is an explicit monotone source word with public map

\[
X_j\mapsto X_j\quad(0\le j<111),\qquad
Y_i\mapsto Y_i+X_i\quad(i=0,1,2),
\]

and all other original Y unchanged. The word has 1578 unit-rank MOVEs, 391 ADDs, three INIT, three CLEAR, and peak one simultaneously live owned field. It uses no additional ascending owned record, no pure local cache and no restarted original route.

Every original Y is arbitrary and independent. Every original X is restored at Hub before the first packet is born. The construction extends the preceding pair acquisition by a genuinely joint three-receiver schedule; it does not repeat a pair and start the originals again.

## Dependencies and credit

The compressed native source SHA256 is `51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`. The source pins, exact facets and 111 roots are inherited from the programme's retained BIT model. The author geometry/replay machinery extends `../mixed-y-joint-acquisition/build_mixed.py`, SHA256 `10c182a4998884037c607ac8c694a361ba0d7b4fc6e6afbc15119c317ba7ca1e`.

The two-ADD mixed-Y exchange comes from the earlier programme `bit-y-feedback-normalization/review-b` motif, specialized by Worker C during S011. The present cyclic acquisition schedule and actual word are Worker A's contribution. Original source and mathematical predecessor credit remain with @CubeJerry and their cited predecessors. This package is AI-assisted. Its author replay does not count as independent mathematical review.

## Local support partition

Let F_i=e_i^⊥ for i=0,1,2, and let

\[
C_{012}=F_0\cap F_1\cap F_2=\operatorname{span}(e_3,\ldots,e_7).
\]

For a noncoordinate original root r_j, write its zero mask on the first three coordinates as the subset of {0,1,2} on which it vanishes. The actual 103 noncoordinate source roots partition as follows.

| Zero mask | Number of roots | Required receivers | Aggregate location |
|---|---:|---|---|
| empty | 7 | none of 0,1,2 | sent directly to Hub |
| {0} | 12 | 0 | coordinate flat omitting 0 and 3 |
| {1} | 16 | 1 | coordinate flat omitting 1 and 3 |
| {2} | 16 | 2 | coordinate flat omitting 2 and 3 |
| {0,1} | 15 | 0,1 | C₀₁=F₀∩F₁ |
| {0,2} | 15 | 0,2 | C₀₂=F₀∩F₂ |
| {1,2} | 15 | 1,2 | C₁₂=F₁∩F₂ |
| {0,1,2} | 7 | 0,1,2 | C₀₁₂ |

Every claimed inclusion and rank is checked on exact rational source vectors. In particular, each singleton-mask group is supported on the stated rank-six flat. No original root belongs to two groups, so all donor routes are disjoint assignments.

Define

\[
K_i=\sum_{j=0}^7x_j+\sum_{j\ge8:r_j\perp e_i}x_j,
\qquad H_i=K_i+x_i.
\]

The goal of the ascending prefix is to acquire the actual original-Y values y_i+H_i at their facets.

## Shared prefix

Move Y₀,Y₁,Y₂ from zero to C₀₁₂. At this chart, original X₃ accumulates the other four coordinate inputs X₄,…,X₇ and the seven triple-mask noncoordinate inputs. Each donor reaches C₀₁₂, is read by the carrier and then proceeds unchanged to Hub. All three Y records read the resulting twelve-term aggregate at C₀₁₂. The carrier then reaches Hub and is restored by those eleven donors.

The three Y records next diverge, but remain at rank-six charts:

\[
Y_0\text{ waits at }C_{01},\quad
Y_1\text{ waits at }C_{12},\quad
Y_2\text{ waits at }C_{02}.
\]

Orient the triangle of pair demands as 0→1, 1→2, 2→0. For each directed edge i→j, let k be the third index. Original X_k, which is local to C_ij, accumulates all fifteen noncoordinate inputs with zero mask {i,j}. Thus it holds

\[
x_k+\sum_{r:\mathrm{zero\ mask}(r)=\{i,j\}}x_r.
\]

Y_i reads this actual carrier at C_ij. The carrier then ascends exactly one rank into F_j and waits there. No operation yet requires Y_j to have reached F_j.

After all three first reads have occurred, every Y_i ascends to F_i. Each reads the already parked incoming edge carrier. That carrier then goes to Hub and is restored using its fifteen original donors.

This two-phase schedule resolves the apparent cyclic wait. In the first phase, every Y is already at its own rank-six chart and every edge carrier has its donors available independently of the other Ys. In the second phase all Ys ascend, then the parked carriers are read. There is no cyclic data dependency and no simultaneous duplication of a pure edge sum.

Finally, each singleton-mask group is aggregated into one of its own original X fields at its stated rank-six flat. Donors proceed unchanged to Hub. Its carrier ascends into the one corresponding receiver facet, is added to that Y and continues to Hub, where the same donors restore it. The remaining originals then finish their ascent to Hub.

For every i, the acquired terms are exactly: coordinates 3 through 7 and the triple-mask roots; the other two coordinates and both pair-mask groups incident to i; and the singleton-mask group {i}. These are disjoint, and their union is precisely H_i. Consequently the prefix ends with all X originals individually restored at Hub and Y_i=y_i+H_i for i=0,1,2.

## Packet operations

Create each of three packets sequentially at Hub. The actual restored originals there supply K_i. Descend to F_i and perform

\[
Y_i\mathrel{+}=P_i,\qquad P_i\mathrel{+}=Y_i.
\]

The local map on independent incoming values is (Y,P)↦(Y+P,Y), so it is invertible and has zero packet-through coefficient. At the acquired values it gives

\[
Y_i^{\rm out}=y_i+H_i+K_i=y_i+x_i,
\qquad P_i^{\rm out}=y_i+H_i.
\]

The packet continues to zero and is explicitly CLEARed before the next packet is born. CLEAR operands include the arbitrary original y_i values. Their exact rows are recorded; the package retains the programme's owned arbitrary-content erasure interface and does not prove a foundational erasure theorem.

The word is scalar over F₂. Tensoring every addition with I_V proves the same local algebra and public map over any characteristic-two field and every positive record dimension V. This observation does not itself certify a uniform compiler or recursive supplier.

## Full partial-source accounting

Every original X and Y ascends by exactly seven ranks on one route. Every packet descends eight ranks. All jumps are split into rank-one MOVEs, yielding

\[
Q=(222\cdot7+3\cdot8)[1]=1578[1].
\]

The ADD count is exact:

- Common aggregate: eleven additions into the carrier, three Y reads and eleven restoration additions, for 25.
- Pair aggregates: fifteen additions, two Y reads and fifteen restoration additions per edge, for 96 total.
- Singleton aggregates of sizes 12,16,16: respective costs 23,31,31, for 85 total.
- Packet acquisition: canonical rows of sizes 57,61,61, followed by two exchanges each, for 185.

Their sum is 391. There are three packet lifetimes, with peak one live owned field. Borrowed original X carriers are included among the 222 original routes and are restored explicitly.

Unused donor continuations use a flag containing e₀+e₁+e₂, so they avoid all three receiving facets. The only original-X arrivals at the served facets are {1,8} at F₀, {2,14} at F₁ and {0,22} at F₂. Each receiving Y arrives with a nontrivial previously acquired local prefix; two facet X arrivals therefore do not contradict the three-predecessor-support result for pure L acquisition.

Adding five bare packet paths would arithmetically give 1618[1]. That number is not a constructed eight-packet source: the remaining 108 target operations, any additional acquisitions and their compatible chronology are absent.

## Verification and remaining obligations

The emitted `WORD.json.gz` includes every field operation and exact rational chart. Replay checks all 222 independent input columns, all physical cochart reads, chart ranks and perpendicular complements, every monotone rank-one inclusion, original endpoints, all owned lifetimes, arbitrary-Y packet and CLEAR values, and prefix restoration before packet birth. Eighteen negative controls reject omitted common/pair/singleton deposits, omitted carrier restoration, reversed packet exchanges and a prematurely ascended Y that would make the scheduled rank-six read unavailable.

The author replay extends predecessor machinery; it is not an independent verifier. Newly generated rational flags are explicit and every transport is charged, but their full precision/compiler/recursive admission remains a downstream obligation. The remaining 108 Ys are unchanged, not completed. The eight-coordinate idealized history span is known from Worker C's `multicast-cut` package to leave 103 noncoordinate fitting conditions unsatisfied; a complete architecture must generate additional sign-sensitive history and account for its actual acquisition and use.
