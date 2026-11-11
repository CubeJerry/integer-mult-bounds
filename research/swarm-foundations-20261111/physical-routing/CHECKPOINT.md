# Whole complement routing: retained result and remaining interface

**Wave 4, tracks 55/86; completed novelty-negative checkpoint.** No new
kappa, primitive, counterexample to a retained theorem or assumption
discharge. The proposed fixed-template whole-row routing implication is
already covered by the elementary stream lemma and the merged compiler
occurrence-layout argument. No duplicate router was implemented.

Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`.
Selected conditional kappa: `0.00363005817`.
[SOURCES.json](SOURCES.json) authenticates six canonical texts and pins the
frozen working source-port proof. This is a recovery note, not a proposed PR.

## Exact source-specific instantiation

Freeze one finite compiler instance: rank N, true-source counts S_s,
S=sum_s S_s, replication a, and supplied widths B_(N-s), with
B_(N-s) dividing a*S_s for every nonempty positive-complement bucket.
Put W=a*S. These are constants of the eventual finite machine; tensor
multiplicity, payload length and ordinary input size may grow afterwards.

The source-port proof, section 5, maps old role j=b*S+r(u) to

    x=b*S_s+r_s(u),
    (s,invocation,slot)=(s,floor(x/B_(N-s)),x mod B_(N-s)).

For s=N it returns the distinct NoComplement label (N,x). Choose a fixed
order of the complete qualified labels, preserving invocation/slot
boundaries. Their union has W elements, so the exact map and inverse define
a permutation pi of [W]. It can cross replica boundaries; dividing the old
row number directly by a smaller width does not give this map.

Suppose the actual physical ABI supplies

    [P] x [R] x [B],  R=W*Q,  P,Q,B>=1,  V=P*R*B,

with role j carried by complete rows r=W*g+j. Each row has the same complete
B-bit suffix, including every spectator, control and record bit belonging
inside that row. The row class is external to the native coordinate frame.
This physical layout/divisibility premise is not a consequence of metadata.

The canonical `upstream/build/sections/02-streams.tex`,
`lem:elementary-streams` item 4, splits these rows into W streams, each of
shape [P] x [Q] x [B] in unchanged suffix order. Its fixed-order merge
implements pi, and the same lemma implements pi inverse. Therefore the
source-complement grouping and ungrouping have **O_template(V) routing
overhead** on a fixed finite number of tapes. NoComplement fields undergo
no supplier invocation; W=1 is trivial.

This directly instantiates an existing theorem. Pi can be fixed program
data: no runtime random access, sorting or source-index lookup is required
for this existence implication. The metadata algorithms construct/check
that data; their host accesses are not tape operations. If N, a, the widths
or pi vary with ordinary input size, the constant is no longer justified
without a separate uniform complexity bound.

## Complete costs and history

The stream proof pays collapsed-descriptor arithmetic, local counters and
resets, every payload transfer, copy, rewind and clearing of visited work
intervals. A fixed number of canonical lengths costs poly(log(2V))=O(V).
This does not pay construction from an arbitrary longer descriptor list or
conversion from a different external ABI.

Let J index the finitely many positive complement calls, with complete
input volumes V_j. The source partition gives sum_j V_j<=V. The honest bill
including actual work is

    T <= c_template*V
         + sum_j (T_entry,j + T_child,j + T_return,j)
         + T_external_header.

The linear assertion concerns routing overhead, not arbitrary children or
whole-job coordinate normalizers. Transferring to the callee's fixed ports,
suspending the other fields and erasing copies require charged scans and
the actual ownership ABI. Work copies gain no productive-input credit.

If the wrapper uses at most c_template*V cells above its supplied local
guards, its new visited-cell bill is O_template(V). Retained backing K0
includes historical blank tails. A safe composed history bound is
K0+c_template*V plus the incremental histories of adapters and children.
O(V) total growth needs their own O(V_j) premises or a stronger reuse proof;
cleanup cannot delete historical terms.

Ancestor preservation is a trace-level contract. A local guard return avoids
ancestor scans only when every callee respects that boundary and restores
its heads uniformly over ancestor height. The literal complete-row parking
caller makes these premises explicit. Across ordinary recursive levels,
the retained global bank/parking protocol is still needed; the finite word
does not authorize new tapes at each runtime depth.

## Whole-role permutation versus growing native frame

`FINITE-PRECOMPILATION.md` section 1 hypothesis 3 requires priced whole-job
embeddings at every tensor multiplicity. Rank equality is insufficient.
Sections 4 and 6 use those embeddings and explicitly forbid treating an
arbitrary growing address permutation as a linear scan.

The port map identifies which complete fields meet, not their native frames.
A fixed frame on N abstract blocks lifts to f selected positions per block.
That address domain grows with f. Declaring the template fixed does not make
this a fixed radix or whole-role permutation.

Merged [CrocSwap/integer-mult-bounds#6878](https://github.com/CrocSwap/integer-mult-bounds/pull/6878)
already constructs ordered active sets, complete complements and inverse
return routes for compiler occurrences. Its `COST.md` pays whole-field role
swaps, alignment, setup, parking, copying, owned scans and returns. Its
retained complete ordinary tariff is

    C_template*V*((e*G)^tau+1),  G=4*ceil(log2 p)+6,

with fixed-rho selected-bit routes. The current selected #7000 application
review, section 6, retains each movement-record bill

    C_move*V*((f*log p)^tau+1),

and requires final route/owner/setup counts to replace old raw constants.
These are upper bounds under admitted primitive contracts, not a lower-bound
obstruction against a future linear adapter. No retained statement is shown
false by this investigation.

## Remaining interface and stopping decision

A complete binding still needs an actual smaller-program library and its
normalizers, common selected-bit plane, equal complete within-row shapes,
all unreleased row-divisor stock, canonical descriptors, disjoint initialized
owned banks, and successful child trace/precision/cleanup/history contracts.
Every resulting finite event count and workspace inventory enters the full
source budget. Source-group metadata alone supplies none of these premises.

Complement divisibility is only one obligation. Separate chronological exit
cuts retain their own integrality and return order. Source grouping cannot
authorize pooling those exits. Actual native manifest/adapters remain beyond
the metadata theorem; all five selected assumptions remain.

The bounded overlap check read the canonical research index, three targeted
live PR searches, actual #6878 merged metadata and source, the literal
complete-row caller and the retained #6719 routing summary. This suffices to
stop this narrow task; no exhaustive archive-search claim is made. No finite
simulation is presented as a new universal proof.

Next action: independently review the compiler worker's concrete smaller-
library recurrence, focusing on full costs and chronological exit denominators.
Do not reopen generic role routing without a changed physical interface.

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance.
Credit the original elementary streams manuscript, Jacob Alan Sussman's
integer compiler and retained transfer, zxv's finite closure, @CubeJerry's
#6878 occurrence-layout/complete-cost work, the whole-row parking predecessors
including JoyboyBrian, and the source-port index's stated predecessors.
