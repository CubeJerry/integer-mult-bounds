# Stationary terminal caches remove a canonical preload ordering obstruction

**Proved rescheduling lemma and literal four-copy chronological control.**
The control completes native receiver 3 in four separately paid copies,
using all 888 original input columns. It does not construct simultaneous
source formation for all 111 receivers and gives no new complete kappa.

The mechanism is to capture each last original-X contribution at its actual
receiver facet before releasing that original to Hub. These terminal copies
remain stationary. Together with stationary proper-chart anchor sums, they
allow all original-X computation and restoration to finish while every
original Y remains pure at ground. Canonical formation then uses actual raw
Hub inputs; no held-coordinate query or source-space surjectivity is needed.

## 1. Rescheduling lemma, with exact source restrictions

Consider a finite literal whole-record ADD/MOVE circuit on public X and Y
records. Permit stationary zero-born owned accumulators. Assume:

1. The X evolution is independent of Y: every data-changing operation on an
   X record reads only another X record or a separately specified X-only
   source. In the elementary version used here, these are invertible ADDs
   among original X records. No Y-to-X operation occurs.
2. Every read from X into Y occurs at the actual common chart of those
   records. At the end, all original X records reach Hub. Their X-only
   transformation is invertible and is restored by an explicit Hub word,
   included in the invoice. The local control already contains that inverse.
3. Apart from X-to-Y reads, Y operations read only Y records. Their locations
   and operations are fixed independently of input values. Their final map
   is Y -> Y + B X on arbitrary initial Y, for a specified binary block map B.
4. A zero-born stationary owner may be retained at an actual read chart until
   its deferred Y read. Every such owner is initialized, captured, read and
   finally cleared in the new word.

Then the circuit can be rescheduled so that all X are restored at Hub before
any Y leaves its initial location. The same final map is obtained with the
same public movement multiset and no additional cache MOVE.

For the elementary construction, introduce one owner per X-to-Y read. In
the X-only phase, at that original read's chronological position, initialize
the owner at the actual source chart and ADD the current X value into it.
Leave the owner there. Execute all X operations, including restoration,
without performing any Y operation. In the second phase, execute the original
Y subsequence in its original order, replacing each X-to-Y read by a read of
the corresponding stationary owner. At that point Y is at the same chart as
in the original circuit. Clear every cache after its last read.

The source at each capture has exactly its original value: deleting Y
operations cannot change an X-only computation. The deferred Y computation
therefore sees exactly the same sequence of added values, and its internal
operations and chart paths are unchanged. This proves the map and legality.
The generic construction adds one INIT, one capture ADD and one dirty CLEAR
per original cross read; the original cross ADD is retained as the cache
read. It does not charge those owners as movement-free memory without also
listing their ordinary and retirement costs.

Several copies can be consolidated when exact chronological identities
permit it. Consecutive contributions to one Y anchor, with no intervening
use or change of that Y value, may be summed in one stationary owner and
later read once. Several reads of an unchanged X pivot at one facet may use
one snapshot. The literal control checks these conditions by replaying the
actual X rows at every capture; it does not infer them from abstract ranks.

### Canonical preload corollary

Suppose a desired correction has I = K + B in characteristic two and the
row space of K has dimension g in the physical binary-bank model. Once all
X restore, initialize g owned fields at Hub, form a real basis of K from
the present raw X records, and move those fields to ground. Their actual
ground reads preload K X into Y before the deferred Y phase starts.
Because the original Y coefficient map is the identity, the final value is

    Y + K X + B X = Y + X.

All g descents, source ADDs, preload reads, INITs and dirty CLEARs are
additional invoices. In dimension eight the direct descents cost g[8].
This is a chronological theorem conditional on the specified X-only source
circuit, not a theorem that such a circuit exists for the full native.

If a proposed source really needs moving public Ys to form its X-side
packets, its source computation is not independent of the deferred Y phase
and this lemma does not apply. Likewise, a suffix starting after all X have
already passed their terminal facets cannot retroactively install these
caches. The construction changes the earlier history.

## 2. Pinned local circuit and actual cache placement

Native root table SHA256:

    8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e

Reviewed local four-copy MDS word SHA256:

    831ac2f8ba647a50866af61461f9f378c76a443801f372154745520b4caa96fa

The predecessor is the four-chart decoder of
`results/bit-shared-facet-mds/author/four-chart-word/WORD.json`.
Its receiver is 3 and its proper charts are

    C0 = F3 intersect F76; C1 = F3 intersect F81;
    C2 = F3 intersect F91; C3 = F3 intersect F96.

Every Cj has real rank six. Four physical binary banks implement two GF4
coordinates; all arithmetic remains ordinary full-record binary ADD.

There are exactly eight new stationary source caches:

| Caches | Actual chart | Captured information |
| --- | --- | --- |
| ANCHOR_Y3_0, ANCHOR_Y3_1 | C0 | Actual incoming encoded source sums |
| ANCHOR_Y3_2, ANCHOR_Y3_3 | C1 | Actual incoming encoded source sums |
| TERMINAL_X1_2, TERMINAL_X1_3 | F3 | Actual nonanchor pivots after their C2-to-F3 ascent |
| TERMINAL_X2_2, TERMINAL_X2_3 | F3 | Actual nonanchor pivots after their C3-to-F3 ascent |

The terminal pivots follow their original paid routes, including the real
rank-one ascent to F3. Their four cache capture ADDs occur there. The pivots
then continue to Hub on their already invoiced rank-one ascents. The original
inverse aggregation and per-source preencoding inverse restore all 444 X
records. No original X is released before its last needed value is captured.

The build records every cache birth, every actual source row at a capture,
every deferred read row, and every dirty retirement in
`output/CACHE-LIFETIMES.json`. Owners do not move. The four terminal cache
values are the current encoded pivot values, not fictitious raw coordinates.

## 3. Canonical formation and all-column milestones

The original-X subsequence contains only invertible ADDs. Its explicit
inverse is part of the retained local word. At operation 1728 of the new
word, before canonical formation, all 444 X are their independent original
coordinates at Hub. All 444 Y remain their independent original coordinates
at ground. The eight stationary caches retain their actual X-only values.

For each physical copy, use the nine native canonical basis roles

    0, 1, 2, 4, 8, 9, 14, 30, 59.

Here K_i = x_i + sum_(j orthogonal to i) x_j. Each of the 36 canonical fields
is initialized at Hub and formed by explicit reads of the raw original X
records. The 2140 source ADDs are present in the word. Each canonical field
then descends directly Hub-to-ground, with gap eight.

At operation 3940, all 36 fields have their exact canonical rows at ground,
all X remain raw at Hub and all Y remain pure at ground. The all-column
replay checks these three assertions separately. In particular, the code is
now contained in the actual Hub record space before departure; there is no
unavailable held projection hidden behind a rank-nine statement.

The exact relation K3 = K0 + K1 + K2 gives 12 actual preload ADDs. The
original Y preencoding, chart ascents and postencoding then execute. The
four anchor records are read at C0/C1. The four terminal caches supply the
same ten binary decoder reads that the nonanchor X pivots supplied earlier.
Thus receiver 3 ends with y3 + K3 + M3 = y3 + x3 in each copy. Every other Y
is unchanged. All X restore, every public endpoint is correct, and all 44
owners are explicitly retired.

All 888 initial columns are represented independently. The finite binary
identities act coordinatewise for every positive whole-record width V and
every characteristic-two coefficient field. No within-record lane operation
or field extension is granted as a new primitive.

## 4. Full ordinary and movement invoice

The complete word has

    44 INIT, 3210 ADD, 1164 MOVE, 44 dirty CLEAR.

Peak ownership is 44. The ADD breakdown is:

| Purpose | ADDs |
| --- | ---: |
| Retained X encoding, aggregation and inverse | 894 |
| Actual X reads accumulating proper anchor caches | 142 |
| Terminal pivot captures at F3 | 4 |
| Canonical formation from raw Hub originals | 2140 |
| Canonical Y preload | 12 |
| Deferred Y-only encoding/decoding and cache reads | 18 |
| Total | 3210 |

The final line of 18 consists of four Y-to-Y operations, four anchor reads
and ten terminal-cache decoder reads. Relative to the original 1050-ADD
local correction, the extra cache cost is eight ADDs: four terminal captures
and four anchor reads. The further 2152 ADDs are canonical source formation
and preload. All source restoration operations remain included.

The physical movement profile is

    12[1] + 228[2] + 232[5] + 4[6] + 652[7] + 36[8].

The first five terms are exactly the original local word's movement
multiset. The last term is the real canonical supply. There are no cache
MOVEs. Divide every native body and caller term by the same four productive
copies to obtain

    Q = 3[1] + 57[2] + 58[5] + [6] + 163[7] + 9[8].

At t=199/200, exact integer-root directed intervals give

    Q = 1611.435449971746502549787725437447229919418...,
    limiting room = 10.315430239405852696458424929547756528497... .

This is the complete invoice of a partial source. It is not a full native
supplier and no caller profit is inferred from its movement room. Its
ordinary owner cost differs from the earlier direct-query word: 44 owners
here versus 40 there. The useful result is the source-independent chronology
mechanism, not the small movement difference between local controls.

## 5. Consequence for the simultaneous-source problem

For a future global X-only recoding network, stationary captures can be
installed simultaneously at every actual source-to-receiver read, including
terminal facets. Each capture is locally legal and the proof preserves its
chronological X value. The resulting source may finish and restore before
any Y begins. Therefore an X-only global construction does not additionally
need to concentrate the canonical held projection into a few accessible
pivots: it can retain the decoder contributions locally, release all X,
and form the canonical code from the restored originals.

The missing global obligation is still substantial. One must construct the
compatible overlapping X recoding network and all its simultaneous receiver
channel values, prove invertibility/restoration, and count every ordinary
operation, cache and public route. The retained one-hop and disjoint-cohort
obstructions still apply to their original source interfaces. This lemma
does not defeat those rank bounds or turn a list of individually feasible
receiver words into a compatible all-receiver circuit.

The argument is also separate from the frozen current F4/F8 cuts: those cuts
already have every X at Hub and do not contain these earlier terminal cache
captures. Installing them would require a changed chronological source.

## 6. Reproduction, controls and credit

Run

    python -B build.py --repo REPO --out OUTPUT

The author replay uses exact rational chart containment and all 888 columns.
Eight omission controls reject missing proper capture, terminal capture,
terminal retirement, the actual pivot-to-facet visit, original-X inverse,
canonical source read, canonical descent and canonical preload. These are
finite verification controls; the rescheduling proof supplies the universal
width statement. Independent review remains separate from author execution.

Credit @CubeJerry and the native programme; the retained shared-facet MDS
construction; the preceding stationary-anchor and direct-query chronology
packages; root's insistence on actual global source formation and arbitrary
input columns; and OpenAI assistance. No foundational assumption, strict
supplier or new complete kappa is discharged.
