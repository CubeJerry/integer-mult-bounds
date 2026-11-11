# A main-demand prefix with four charged deliveries

**Proved finite encoded prefix. No full native, supplier or new κ.**
This changes the previous all-live virtual-helper interface. The physical first
copy remains exact, all entering information remains physically retained, and
specified second-copy main values are represented at their current charts.
Unneeded *virtual second-helper* states may be unavailable at their source
charts. They are not silently declared decodable or supplied by an oracle.

The literal source prefix through **cut 25897** has only four extra rank-one
MOVEs and eleven live parked/delivery fields. The old all-live construction
at the same cut used 32 rank-one and four rank-two deliveries and 43 fields.
This comparison is a prefix expenditure comparison. Future demands are deferred,
not erased. In particular it is not an improvement to a complete κ.

## 1. Exact contract

Let W be the pinned source, u its first virtual copy, v its second copy with
independent main inputs and the same arbitrary helper inputs, and q_i=y_i−x_i.
The physical programme satisfies:

1. Every live first-copy source role is represented exactly by its original
   physical holder and follows the source's actual chart and instruction order.
2. At each funded second-main MOVE, its carrier is set to the declared current
   virtual main difference v_r−u_r using current cochart observations, then
   takes the second main MOVE already present in the H4 profile.
3. At the final cut of the prefix, all 400 current second main fields have
   exact current-cochart decoders from the first copy and physical observations.
4. Every original q_i is still stored in a named physical holder at its initial
   chart. A main carrier's old code is snapshotted before rebasing or departure;
   all such snapshots are real, counted owners. Thus no entering information
   is discarded merely because the finite prefix has no immediate use for it.

There is deliberately no clause requiring every intermediate second-helper
value to be available at its current virtual chart. Since the first source
copy alone is physically executed, that absence cannot corrupt the actual
helper bank. It does impose a real continuation obligation whenever future
main data need the deferred information.

At this source prefix there is no source INIT/CLEAR, and all source SCALEs are
nonzero. Therefore the first-copy public prefix is invertible. Together with
the 400 physically retained q_i, the physical state retains all 1880 independent
entering arrays for every admitted array dimension. This is a structural
argument; the verifier additionally checks the exact row identities over Q.

## 2. Observation graph and backward dependency closure

Build a directed acyclic graph of possible difference observations. An input
node is q_i in its initial chart. A main arrival is a proposed current virtual
main row at the destination of a funded second-main MOVE. An auxiliary arrival
is a proposed homogeneous source row transported along that source auxiliary
MOVE. Each arrival carries an exact linear expression in earlier observation
nodes at its **source** chart. A node is inserted only when the normalized row
is available there; every graph expression is checked over Q.

For a selected horizon, roots are all main departure/arrival rows prescribed
by clause 2, and all current main rows prescribed by clause 3. Take the complete
backward dependency closure. Only auxiliary arrivals in that closure are
materialized. Inputs and all necessary old carrier versions remain physically
stored, including input differences absent from the immediate root closure.

### Why deleting an unmarked arrival is sound

Every materialized node's parents are themselves marked, earlier in time and
at the required source chart. The literal compiler allocates a distinct zero
owned field and snapshots the parent expression before transporting it. At a
main departure it first parks the old carrier, changes all later references to
that old node to the parked owner, zeroes and rebases the carrier, and performs
the funded public main MOVE. Thus graph nodes are represented by actual current
physical holders; graph persistence never means uncharged input rereads.

Induction on marked nodes proves every materialized observation row. The
current main decoder expressions then prove the required second main values.
An unmarked auxiliary arrival appears in none of those dependencies and can
be omitted for this declared horizon. This does not show it is unnecessary
for a later horizon, nor permit forgetting its original input information.

The generated first-copy instructions are retained literally, so arbitrary
helper inputs are preserved by the source copy. All extra owned MOVEs are
marked owned, all public main MOVEs public, and all snapshots have current
cochart operands and distinct ownership.

## 3. Exact constructed prefix

The four charged auxiliary difference deliveries are source events:

| Event | Original helper role | Extra rank |
|---:|---:|---:|
| 25489 | 830 | 1 |
| 25729 | 812 | 1 |
| 25853 | 320 | 1 |
| 25880 | 355 | 1 |

Seven main departures use their already-funded second-main MOVEs. The compiler
parks the old main code at each departure. At the cut there are four delivery
fields and seven parked fields, all live and explicitly counted. Nothing has
been erased. The transcript's complete operation counts are:

| Operation | Original source prefix | Physical encoded prefix |
|---|---:|---:|
| ADD | 24,433 | 24,860 |
| SCALE | 1,380 | 1,380 |
| MOVE | 84 | 95 |
| INIT | 0 | 11 |
| Total | 25,897 | 26,346 |

The eleven added MOVEs are seven funded second-main MOVEs plus four newly
charged owned deliveries. Their **extra paid moment is exactly 4** at every
exponent, since each new rank is one. The 427 extra ADDs and eleven INITs still
need actual positive physical/tape/precision tariffs in any complete supplier.
The new fields occupy additional named labels in this conservative transcript;
no global reuse of the original source-owned inventory is presumed.

For comparison, the same compiler at cut25747 needs no extra MOVE; immediately
following source event25747 (`main40 += helper812`), the current main contract
requires the rank-one delivery represented by event25729. This locates the
first concrete spatial main demand in the new representation. It differs from
the first all-live-helper delivery at event25489 because that helper is not
read into a main until later.

### Explicit deferred information

At cut25897, virtual helper332 is in chart381, with difference

\[
\delta_{332}=(-q_{33}+q_{109}+q_{108})/2.
\]

That row is not in the span of the current difference observations at chart381
in this transcript. The verifier checks this failure. It is an intentional
example of the weaker contract, not a missed transport counted as zero.
The original q33 and q109 remain physically stored at their initial charts.
Any later need for this virtual helper row must obtain and pay for an actual
causal delivery, or change the representation so the original helper state
is no longer needed. This packet supplies no free future resolution.

## 4. The fixed observation graph still fails the full budget

The favourable prefix does **not** make backward pruning alone a sufficient
H4 architecture. At the full 71,261-event source horizon, the same fixed
expressions and all main departure/final-main roots retain 2,879 auxiliary
MOVEs, with profile

```
rank 1: 1894
rank 2: 329
rank 3: 466
rank 4: 82
rank 5: 100
rank 6: 4
rank 7: 1
rank 8: 3
```

Every positive rank contributes at least one at t=199/200, so its extra moment
is at least 2879, already far beyond the H4 allowance below98.399076951 even
before new scalar, storage and precision costs. The first-prefix omitted routes
are generally needed again under the fixed full-horizon graph. A full literal
implementation of this losing policy was not pursued.

This is a failure of this specific fixed-expression graph, not a proof against
all future-demand algorithms. To progress, change the actual offered row
channels, their timing, or the source/main/helper coding. In particular a
future code may repurpose an existing paid main/helper MOVE rather than add
another sidecar arrival. Such a change requires a new dependency graph and a
complete invoice; its savings cannot be inferred from this finite prefix.

## Verification and next step

`demand_graph.py` authenticates the source and independently checks every graph
parent identity, chart and causal order. `demand_prefix.py` emits a literal
instruction sequence, main decoders and all retained-input holder witnesses.
`verify_demand_prefix.py` replays the physical word on all1880 formal inputs,
separately executes the two original source prefixes, verifies all first-copy
rows and400 second-main decoders, and checks400 original input differences
remain in current physical holders. Owned-flag, sign and false-input-retention
mutants must reject. The missing helper332 decoder is also verified.

The next concrete task is a source-safe use of an already funded transport
that removes one of these actual charged deliveries while retaining its dirty
common payload and the old main-code information. Prove that one complete
loan/coding block, including source versions, cochart restoration and future
consumer readiness, before expanding to a full native.

All five global assumptions remain. The exact new result is a finite
source-bound implementation of a weaker, explicitly stated observation
interface, plus a scoped full-budget failure of its straightforward extension.
Prepared for @CubeJerry with substantial OpenAI assistance and retained source
and programme attribution.
