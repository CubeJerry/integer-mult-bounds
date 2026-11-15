# Local flag placement halves the five-mask transport invoice

**Proved source refinement; no new κ.** This is a separate literal word in
`local-mask-output`, derived from the independently auditable construction in
`COUPLED-HISTORY-PROOF.md`. The earlier words remain unchanged.

## A precise flag-placement lemma

Let k independent facets have cyclic order0,...,k-1. For a source cohort
with nonempty membership J, a pure donor mask is born at C_J, of dimension
8-|J|. Suppose the mask is needed by only query i. Its fixed packet/receiver
flag visits the cyclic prefix charts C_{P_i(l)}, where P_i(l) contains the
first l indices starting at i. Put

    ell_i(J) = min{l : J is a subset of P_i(l)}.

The actual mask owner can descend from C_J to C_{P_i(ell_i(J))}, then the
query reads it at that actual cochart. Its required rank decrease is
ell_i(J)-|J|. Every later prefix is contained in that destination, so this
placement respects both monotonicities. Within the fixed flag and a single
unchanged mask owner born at C_J, this is the earliest possible flag chart:
independence of the normals makes containment equivalent to J being a
subset of the prefix. This is a scoped optimum, not a lower bound on other
source representations, new flags, shared recodings or jointly coded masks.

For the five-facet construction each branching cohort has a run of length2
and a singleton run. Assign the aggregate carrier to the length2 run and the
masked internal donor to the singleton. The donor mask is then needed by
only that singleton query. Its cohort has |J|=3 and first covering prefix
has length4. Thus each mask moves dimension5 to dimension4, rather than
dimension5 to the common dimension3 chart. All five rank decreases are one.
The masked singleton queries are respectively3,0,2,4,1 for patterns
11,13,21,22,26. Every one of the five queries reads exactly one mask.

The source's internal donor restoration is unchanged: restore the donor
from the intact aggregate at Hub, then restore the aggregate. Changing which
cyclic run receives which original does not alter correctness. The actual
raw cache coefficients change and are checked in the new word. Each query
adds its mask at the newly declared cochart, including Y34 on its upward
flag; there is no free remote read.

## Exact resulting construction

The source pins, eight initial seeds, seven proper acquired modes, original
endpoints, two-ADD public-Y exchange and arbitrary-y34 ground cancellation
are unchanged. All111 X originals are restored before packets; Y34 is
y34+x34; the other110 Y values remain unchanged. Full222-column packet
history has rank33, contains W15, has Y projection rank1 and pure-X
intersection32. Terminal packet rank remains8. The five masks remain
additional actual downward-moving source copies, and Y feedback remains a
separate departure from the earlier scattering theorem's interface.

There are159 INITs,642 ADDs,407 MOVEs,159 CLEARs and peak159 owned records.
Compared with the previous construction, three redundant mask reads are
removed and exactly five rank2 mask MOVEs become five rank1 MOVEs:

    Q = 118[1]+27[2]+38[3]+49[4]+28[5]+29[6]+117[7]+[8],
    sum_r r Q_r = 1618+5 = 1623.

Directed rational bounds at t=199/200 give movement moment
1610.1482472133852958596667524664..., leaving limiting room
11.6026329977670593865793979005.... The exact improvement is
5(2^(199/200)-1). Every owner, ADD and MOVE is included; this is the price of
a partial one-target word, not a completed supplier.

## Verification and remaining problem

```sh
python research/moonshot-005-program/work-in-progress/2026-11-15-S014/worker-a/coupled_local_masks.py
```

Expected status is `PASS_LOCAL_MASK_SINGULAR_Y_CELL_WITH_FULL_W_HISTORY`.
The actual `mask_routes` list records every source chart, destination,
recipient and rank drop. Seven semantic negative controls are retained,
including omission of a real mask descent and its later invalid read.
Independent verification belongs to the separate worker-C artifact.

The next useful composition can reuse these now-retained nonlocal masks as
literal receiver payloads, or prepare further shared receiver corrections.
Every such continuation must use the actual mask charts and preserve all
earlier reads. The remaining110 target values, strict suppliers, physical
compiler, precision, recursion and five foundations remain open. No new κ.

Credit: @CubeJerry, retained cyclic-source and exchange authors, worker A's
local flag mask-routing refinement, and separate worker-C verification.
OpenAI-assisted research.
