# Causal 9- and 36-port words on the actual H owners over GF(64)

On the pinned bank-480 routes repeated eight times, the split into marked
and unmarked D charts admits explicit H operations on every native plane.
The formal source coordinates at an ordinary donor/H incidence have widths
48 and 192. Every visible receiver projection is invertible on these two
complete donor inputs with other donors held at zero. At each of the eleven
singleton H planes the projections have ranks 48 and 192 on inputs of widths
72 and 288. The two pure phases are invertible on the actual owners, including
all arbitrary original Y baselines. These are local ranks. The theorem does
not identify the simultaneous inverse fibres required for the prescribed
two-sided endpoint.

## Actual owner interpretation

Work over the polynomial field GF(2)[z]/(z^6+z+1), in ascending power-basis
bit order. At each of the 1,120 H charts sort the 9 marked D ports and the 36
unmarked ports separately by their actual D ID. Each port in one component
has 16 actual owners. For a component of n ports put k=n/3. Each of its 36
geometric receiver views, including the views of nonnative completion roots,
sees k of those n ports. The S028 orthogonal-spread theorem proves this
incidence. The verifier recovers it on all 40,320 views from the pinned
layout and spread.

For the isolated H operation, the actual early owners are original Xs
travelling through H. An incoming late owner is an actual Y with an
arbitrary baseline. Its proper component can come from an actual source
line, or can be zero at a direct ground birth. The allocation below uses
the local chronological margins of the asymmetric atlas. Columns in a stripe
are formal inputs delivered on these owners.

| H type | Count | Early/late owners per port | Per-stripe early sources | Per-stripe late sources |
| --- | ---: | ---: | --- | --- |
| Full selected | 65 | 16/0 | k from each of three donors | none |
| Full ordinary | 816 | 8/8 | k from each donor | k from each donor |
| Two donors | 227 | 8/8 | 2k from the designated large donor and k from the small | k from the small donor and 2k direct ground |
| Singleton | 11 | 8/8 | 3k from the donor | 3k direct ground |
| Empty | 1 | 0/16 | none | all direct ground, identity |

A stripe has one owner at each component port. In each donor/ground group,
take real owner IDs in lexicographic order (native role, owner coordinate,
copy). Assign inputs by component, polynomial column, then lane. Assign
outputs by ascending D, then ascending owner ID within its phase flag.
This prescribes an actual owner permutation at H before each nonempty
phase. Its forward in-place XOR swaps are paid. The proof does not require
a donor to have supplied marked packets on its unaltered outgoing holder
IDs. The source interface must assign the specified coordinates to the
designated input holders. The verifier enumerates every one of these H/phase
permutations, replays the cycle swaps on the owner labels, and checks that the
true early counts are 768 and 3,072 at *each* of the 111 donor lines.

On the fully early H263, use the ordered donors 0,61,62 and put each in its
contiguous k-column block. For n=9,36 the resulting field matrix is
V_n tensor I_16 in port-major/column-major order. The nine marked IDs are
120,353,720,825,1046,1603,2033,2621,2835. This fixes a reproducible
formal interface. Any previously unspecified source constants must be
checked against these actual nodes, labels and frames.

## Phasewise maps and proof of rank

At each component take the n distinct, nonzero field nodes whose
power-basis integers are 1 through n. Let V[p,t]=a_p^t for 0<=t<n.
The determinant is the product of the nonzero differences of the nodes.
Apply V on every active early and late stripe, after the paid owner shuffle.

At a full H, with donor d in consecutive degrees dk through (d+1)k-1,
any k visible rows give a k-node Vandermonde matrix times the invertible
diagonal with entries a_p^(dk). This proves the desired conditional rank
on each donor within each phase. Full selected H uses all 16 early stripes.
Full ordinary H uses eight early stripes and eight late stripes.

At a two-donor H, put the large early donor in degrees 0,...,2k-1,
the small early in degrees 2k,...,3k-1. In the late phase put small late
inputs in degrees 0,...,k-1, the remaining direct-ground Ys above them.
After the late V, add evaluations of the formal derivative of the large
donor polynomial retained on the early inputs. On the small donor, the
early and late diagonals of each view are invertible k-by-k Vandermonde
blocks. On the large donor the complete observations are the values and
first derivatives of a polynomial of degree below 2k at k nodes. If they
vanish, each (X-a_p)^2 divides the polynomial. Their product has degree 2k
and is coprime across nodes, forcing the polynomial to be zero. This works
in characteristic two, including when higher derivative coefficients vanish.
Each stripe therefore provides rank 2k on both donors.

At a singleton chart, evaluate a degree-below-3k polynomial early and add
its first derivatives on the genuine late ground Ys after their own V.
The restriction to degrees below 2k is injective by the same double-root
argument. The 2k observations thus have full row rank. This alone does not
give a factorization through a predetermined singleton quotient when all
3k input coefficients vary. At the empty chart the late identity preserves
every Y baseline.

Across H, each derivative uses only the odd-degree early coefficients of its
specified polynomial. Before V on the early owners, snapshot the six binary
coordinates of each used field coefficient by stationary INIT and ADD.
Read those values after the late arrivals and dirty-CLEAR them after their
last use. For fixed early data the late map is an invertible V on every real
Y, followed by a translation. No early evaluation reads a late value.

## Exact H-only charges

The compiler of V works over the six-bit expansion. Reversing a row-XOR
elimination gives the explicit ADD word on the true owners. The verifier
checks each primitive and its inverse on all binary basis inputs, and checks
both derivative words with independent arbitrary early and late basis inputs.
A scalar swap takes three XORs on each of the six coordinates. The exact word
and independent-label permutation enumeration give the following totals across
all H charts.

| Payment | Binary whole-record count |
| --- | ---: |
| Vandermonde ADD | 375,697,536 |
| Actual owner-permutation ADD | 11,323,296 |
| Delayed derivative ADD | 14,940,112 |
| Copying genuine early snapshots | 175,056 ADD plus 175,056 INIT |
| Dirty CLEAR | 175,056 |
| Forward H ADD | 402,136,000 |
| Pure-X/every pure-Y inverse ADD reserve | 387,020,832 |
| Forward and reserved pure inverses | 789,156,832 |
| Additional MOVE | 0 |

Peak extra snapshot owners at one H are 1,056. At most 175,056 are live
across all H even if every snapshot lifetime overlaps. The inverse reserve
is the sum of the reversed pure H permutations/V words at Hub for X and
Ground for Y, conditional on the existing global preload/restore order.
It excludes other stages and does not claim a complete invoice. Existing
movement on all 852,480 genuine original owner copies, field expansion, any
source selection and all downstream work remain payable.

## Evidence and further work

From the repository root, run the accompanying build script with
`--repo . --out /tmp/spread-h-replay`. Compare RESULT.json and compare the
decompressed WORDS.json.gz. The word specification contains the six-bit
ADD pairs, field matrices and the active stationary snapshot columns.
The reduction checks every three-node set occurs on the nine-port component
and all actual 12-node incidences satisfy distinct nonzero-node hypotheses.
The 36-port all-subset theorem follows from interpolation. A repeated node
drops the two-donor jet rank by two. Omitting the delayed derivative drops
that rank from 2k to k. The all-H local word must next be composed with
the *same* actual source, common D rows, K word and final decoders, including
the chosen endpoint for all foreign pairs. Five foundations and the strict
BIT/complex suppliers and outer caller remain open. No new κ.

Source data are pinned by decompressed SHA256 in RESULT.json, with starting
programme commit 914097a04bb93f730b805e9d4f036b46707c8675. Credit @CubeJerry,
the asymmetric native atlas and GF16 Hermite module authors, and the
orthogonal-spread port construction. This GF64 spread-specific word,
owner packing and cost analysis used substantial OpenAI assistance.
