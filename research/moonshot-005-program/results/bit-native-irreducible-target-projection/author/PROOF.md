# A literal paid eight-row projection at one complete native receiver

**Proved for the stated finite native atlas, with arbitrary original inputs and all operations paid. No new supplier or κ.**

This extends the S027 D12 tile from twelve source donors to all 62 foreign
donors of receiver 80. The claim is a complete **eight-field-row projection**,
not a 480-row receiver endpoint or the full 111-receiver proper map. The
explicit word is universal in its inputs. Independent bitwise replication
gives the same identity for every positive body width, with every invoice
entry multiplied by that width.

## 1. Statement and exact dependencies

Let F=GF(32), in the polynomial basis defined by t^5+t^2+1. Use the literal
b=480 native public owners and paths from
`bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz`, decompressed
SHA-256 `6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036`.
The native layout and phase pins are recorded in `output/RESULT.json`.
Use the preceding D12 tile word, decompressed SHA-256
`42b701dfce05e108dfafc4db5dcf813f92c42d74f0416e6d37a1d7bb301459e1`.

Order the 62 foreign neighbors of receiver 80 increasingly. On their
480-dimensional banks, put U=span(e_0,...,e_7), let J shift U down one
coordinate, E=e_7 e_0^T, and T_l=sum_{r=0}^7 e_r e_{8l+r}^T for 1<=l<=59.
In that neighbor order let B*_{80,j} be I+J, I+E, I+T_1,...,I+T_59, I.
These are precisely the receiver-80 blocks of S027's irreducible target.
Let P select coordinates 0,...,7.

For **every** X=(X_j) and Y=(Y_i) in F^(111*480), the published literal
binary ADD/INIT/CLEAR word, on the unchanged public owner paths, returns
every original X owner to its original value at Hub, and produces a proper
linear map Y'=Y+B_actual X with

    P Y'_80 = P Y_80 + sum_{j foreign to 80} P B*_{80,j} X_j.       (1)

All arbitrary original Y columns have coefficient exactly identity across
all final outputs. The other 472 rows of receiver 80 and the other receivers
have the explicitly determined but unprescribed X response B_actual. All
extra owners are initialized, remain at their declared charts, and are
charged for dirty clearing. No informative return or extra MOVE is used.

## 2. The preserved twelve-donor tile

D12 contains native donors 0,2,5,7,38,39,40,41,42,43,44,45; its dual is
D116. Its 16 left H planes and 16 right K planes are full, unselected
planes in the b=480 schedule, with one early and one late actual owner on
every flag. The tile source maps, Cauchy16 early and late D maps, stationary
H/D caches, four early F80 caches, and full Hub inverse are retained.
Its four selected right planes are 370,371,372,373. Its established transfer
to coordinates 0,...,7 is the sum in (1) over those twelve donors.

The extension changes the late routing permutation at the selected right
planes and at F80, while preserving the four required late tile packets.
It does not assume that a local target matrix is a physical gate: the source
maps and all early operations remain the literal paid predecessor word.

## 3. Four hundred actual late paths, with shared-chart conflicts excluded

For each of the remaining 50 donors j and each r=0,...,7, initialize one
stationary native-line field owner c_(j,r) and compute

    c_(j,r) = (P B*_{80,j} X_j)_r.

Every such parity uses one or two original fields. Those donors are outside
D12, so none of the preserved tile's source transformations changes their
original values before capture. The cache later adds once into an actual Y
owner that visits the real native line j; the cache is then dirty-cleared.

`flow.py` constructs an integral flow in the actual late layered graph

    native line -> H -> D -> K -> F80.

Each edge's capacity is the number of actual Y owners traversing that edge.
D12 is excluded. Every D is contained in F80 and every used K contains 80.
The four preserved tile destinations at K are excluded from the flow's
K-to-F80 destination set and from D-to-K outgoing carriers. The sixteen
D12 outgoing owners are also reserved. The published certificate contains
400 paths: eight per remaining donor, using 50 H, 184 D and 28 K charts.

This is a finite exact existence certificate, not an inference from the
terminal capacity. `build.py` checks every path's four actual owner records,
native containment relations, all reservations, each donor-coordinate
pair, and pairwise distinct carriers at every layer. In particular, a used
H cannot be one of the tile's H planes: it contains its source donor j,
whereas every tile H lies within D12 and j lies outside D12.

At each shared H, D or K, the path certificate specifies a partial
bijection from distinct incoming owner values to distinct outgoing owners.
Such a bijection extends to a permutation of the union of its source and
destination owner labels, fixing the complement. The `permute` routine
constructs that extension by swaps and checks every prescribed image.
Each field swap is exactly fifteen binary ADD gates. All involved fields
are physically present at the same chart at the time of the permutation.
The four K tile mappings are included in the **same** partial permutation
as the flow packets, rather than composed as potentially conflicting swaps.

Consequently each native parity follows its one certified actual path.
There is no duplicated value or shared-carrier collision. The flow H
permutations are disjoint from the tile H operations, and flow D
permutations are disjoint from D12. These facts justify retaining the tile
source transfer unchanged.

## 4. Final accumulation and arbitrary-Y restoration

At F80 a single permutation places the four tile late packets into output
coordinates 4,...,7 and the 400 flow packets into coordinates 8,...,407.
These are distinct destinations. Each flow packet from coordinate r is
added into output coordinate r. The four retained tile early caches add
into coordinates 0,...,3 and are dirty-cleared. This proves (1) on zero Y.

All late operations, after deleting additions from stationary X-dependent
caches, are invertible operations solely on original Y owners. Let their
product be A. It includes every H/D/K permutation, the D12 Cauchy map,
the final packet placement, and **all 400 final accumulation shears**.
The ground preload applies the reverse binary word A^(-1) while every
original Y owner is at Ground. With caches restored, the final response is

    A A^(-1) Y + B_actual X = Y + B_actual X.

Thus the ground correction handles arbitrary original Y, not just zero Y.
The source caches read original X without changing it. All inherited X
transformations are still inverted in reverse order at Hub. These two
inverses are actual charged ADD words on the real original owners.

The stage order is X_NATIVE, X_H, X_D, X_K, X_F, HUB_RESTORE,
GROUND_PRELOAD, Y_LINE, Y_H, Y_D, Y_K, Y_F. Native caches stay at their
native lines between X_NATIVE and Y_LINE; inherited caches stay at their
H, D or F charts. Public owners follow the exact pinned routes. A locality
check applies to every operand of every gate, not just its input/output
matrix. INIT precedes every use of an extra owner; CLEAR follows its final
use. The full word contains no uncharged copies or free zero inputs.

## 5. Literal invoice and actual limits

For one body bit in each of the five polynomial-basis bits:

| Item | Exact count |
|---|---:|
| Binary ADD | 88,560 |
| Binary INIT | 2,340 |
| Binary dirty CLEAR | 2,340 |
| Peak additional binary owners | 2,340 |
| Public binary owners | 532,800 |
| Peak total binary owners | 535,140 |
| Proper MOVE, gap 1 | 1,335,300 |
| Proper MOVE, gap 2 | 1,081,950 |
| Proper MOVE, gap 4 | 57,600 |
| Additional MOVE | 0 |

There are 400 new native field caches and 68 retained tile field caches;
they coexist before the late wave, giving 5*(400+68)=2,340 extra owners.
The ADD count includes source captures, every swap and matrix word, both
global inverses, every cache injection, and final accumulation. The MOVE
invoice is inherited without modification from the exact public routes.
The table excludes a canonical return, because no complete return for
B_actual is being asserted.

In fact, exactly 420 final field coordinates have a nonzero X response in
this partial word. Since rank(B_actual)<=420, its own return requirement
satisfies

    rank(I+B_actual) >= 111*480 - 420 = 52,860.

This is much larger than the b=480 programme ceiling 9b+16=4,336. The
construction must therefore be completed or changed jointly before it
can be a supplier. The small target projection does not itself certify
the irreducible target's favorable return rank.

Nor can one repeat the construction sixty times while keeping the same
invoice: the 400 late paths and four late tile packets already consume
404 distinct actual F80 fields. Repetition on independent native banks
enlarges the bank and all physical costs. Simultaneous rows and receivers
require shared information, compatible source maps and joint middle
decoding. No such extension follows from this theorem.

## 6. Relation to previous programme work

S023 `bit-native-cycle-and-inlet-gates/author/PROOF.md`, section 3, already
proves that an everywhere invertible foreign block assignment can be
gauged to align an entire chosen receiver, retaining any shared common
rows. Prescribed invertible receiver blocks can likewise be obtained by
choosing the donor gauges appropriately. This package does not claim the
first abstract one-receiver feasibility result.

Its additional content is an explicit paid word in the smaller b=480
atlas, including a coupled D12 source/decoder tile and an exact
conflict-free shared-chart routing certificate, with all original X/Y
columns, owner chronology and scratch costs checked. It is a compilation
and composition result for a specified irreducible-target projection.
The consequential next obligation is simultaneous multi-receiver
compatibility or a global low-return-rank interior factorization; repeated
one-receiver examples would not discharge that obligation.

## 7. Reproduction, negative controls and classification

Run from a source checkout, with TILE naming the predecessor's published
`output/WORD.json.gz` and OUT an empty result directory:

```sh
python3 -B build.py --repo REPO --tile TILE --out OUT
python3 -B controls.py --repo REPO --word OUT/WORD.json.gz --routing OUT/ROUTING.json.gz --out CONTROLS
```

Expected: `PASS_COMPLETE_EIGHT_FIELD_ROW_NATIVE_TARGET_PROJECTION` and
`PASS_SEVEN_NEGATIVE_CONTROLS`. The word decompressed SHA-256 is
`f44c57a64afed9bc2bc3b8abca4ccb2ed6c08df9638baec02bd456e1707d1b7e`;
the routing certificate decompressed SHA-256 is
`f7d7e6cf9c53d141607f6abf26a11794a4f40bd965e353698dcc78806ad2d050`.

Symbolic bit-row propagation checks all 532,800 original binary columns,
including untouched columns represented by their exact basis identity.
The five omission controls remove the Hub inverse, Ground inverse, one
native injection, final accumulation, or one H permutation. Each fails its
specified semantic requirement. Two additional controls move a native
injection or D permutation to a chart that does not own its operands;
both are rejected by the physical locality check.

The certificate is finite, but the stated all-input identity follows from
the explicit linear word and exact basis verification. Repeating the
author's verifier is not independent review. Independent review is
maintained separately by the programme orchestrator. No whole supplier,
new complete κ, or foundational assumption is established here.

Credit: @CubeJerry persistent programme; the prior atlas, tile, S023
gauge/cycle and S027 irreducible-target packages and their cited
predecessors. Constructed with substantial OpenAI assistance during S027.
