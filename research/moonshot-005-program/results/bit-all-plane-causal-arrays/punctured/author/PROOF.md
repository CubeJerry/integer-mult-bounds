# Explicit causal array interfaces at all 227 two-donor native planes

## Claim and scope

Every actual A2 plane H with two native donors in the pinned balanced
source has an explicit causal, invertible local map on its early and late
public holders over `F128=F2[z]/(z^7+z+1)`. For every native receiver
seeing H, its fifteen actual D4 ports determine a 360-dimensional target
whose projection onto either donor's complete 360-dimensional quotient
is invertible. The same physical port is used for every receiver seeing
it; no private receiver output or extra movement is introduced.

The coefficient table materializes all 227 maps and verifies all 15,098
native receiver/donor projection determinants. The cache and all local
ordinary operations are charged. Together with the full-three-donor
Vandermonde construction, this supplies explicit local port interfaces
on all 1,108 nonsingleton native A2 planes, using one common field F128.

This is a positive **local** result. It does not construct globally
compatible quotient maps from each donor's same original input, solve
the later D-to-K-to-F transport, handle the eleven singleton planes,
restore the global X labels, or finish the supplier. No new kappa.

## Real holder counts and an actual stripe partition

The balanced source has `x_H=6`, `e_H=8`, `h_H=12` at a two-native-donor
plane. Each H-D flag therefore has six early holders from each donor,
two late holders visiting each donor, and eight genuine late holders
arriving directly from ground. There are twelve early and twelve late
holders per port, with 45 actual ports.

Each donor consequently supplies 270 early and 90 late quotient symbols.
Partition both phases into six stripes. In an early stripe, use one
actual early holder from each donor at each port. This gives 90 inputs,
45 from each donor, and two outputs per port.

For the late stripe partition, give every port its local ordinal
`p=0,...,44` in the sorted list of H's actual D4 exits. A donor j=0,1
has two late holders at that port; number them `s=0,1` and assign holder
s to stripe `s+2*((j+p) mod3)`. Fill each stripe to two holders per port
using the eight real direct-ground Y holders. Across all45 ports every
stripe has fifteen source additions from each donor and sixty additional
arbitrary-Y baseline holders. Every holder is used exactly once.

Thus in a single stripe write the early source coordinates as
`E=(E_0,E_1)` with each `E_j` in F^45, and the late public input as
`Y=(L_0,L_1,Z)` with `L_j` in F^15 and Z in F^60. All90 late fields have
independent arbitrary-Y baselines. On the source-only slice, only the
first30 receive the corresponding actual native source additions.

## The causal block map

Choose the ninety distinct nonzero field elements with polynomial
representatives 1,...,90, and let

    V[r,t] = (r+1)^t,     0<=r,t<90.

Set `A=B=V`. Capture the90 actual early inputs in stationary owned
holders before applying A. The local two-wave map is

    early output = A E,
    late output  = B Y + C E,

where the explicit C depends on H. The early map uses no late data.
The C term is added from the retained early cache only when the actual
late holders have arrived. Both A and B are invertible Vandermonde
matrices, so the whole public input/output map is invertible and
preserves the arbitrary late baseline. Its inverse is not free; the
global construction must pay its actual Hub and ground inverse maps.

For each actual D port, place output rows `2p,2p+1` there in both phases.
One receiver sees fifteen ports, hence a30-row index set S in each phase.
On donor j's60 coordinates its source transfer is

    [ A[S,45j..45j+44]                 0 ]
    [ C[S,45j..45j+44]  B[S,15j..15j+14] ].

The top-left block has rank30 and the bottom-right block has rank15:
each is a nonzero diagonal scaling of a rectangular Vandermonde matrix.
Let N be a45-by15 matrix spanning the former's right kernel, and let L
be a15-by30 matrix spanning the latter's left kernel. The displayed
60-by60 matrix is invertible exactly when

    det( L C[S,45j..45j+44] N ) != 0.

To see equivalence, a vector in the full kernel first has early part
Nq. The lower equation can be solved for the late part exactly when
`L C[S,j] Nq=0`; the late block has trivial kernel. Thus the full kernel
is zero exactly when the15-by15 reduced matrix has trivial kernel.

## Existence and the explicit finite certificate

For a fixed receiver and donor, the map from the relevant30-by45 C
submatrix to `L C N` is surjective: both L and N have rank15 and admit
the appropriate one-sided inverses. Its determinant is therefore a
nonzero polynomial in C's independent entries. The product for all
actual receiver/donor pairs at H is nonzero. A single C entry has a
rank-one effect in every determinant, so each individual variable has
degree at most36, the maximum number of complete root-line receivers
seeing H. It belongs to only one donor's column block.

The elementary finite-grid polynomial lemma therefore guarantees a
joint nonzero assignment over F128. The larger field is also large
enough for the ninety nonzero Vandermonde nodes. This argument supplies
existence independently of a randomized search claim.

The supplied deterministic xorshift64 enumeration materializes such
assignments. Its arithmetic is reduced modulo `z^7+z+1`; the checker
verifies the inverse of every nonzero field element. All coefficients
are retained explicitly as ninety hexadecimal rows per H, with their
seed and attempt number. Each candidate is checked against every
actual native receiver. Across227 planes the first successful trials
have distribution `{1:128,2:55,3:23,4:10,5:11}`, totaling402 trials.
All15,098 reduced determinants are retained and nonzero.

The exact row reduction also verifies `A_S N=0` and `L B_S=0`, including
the claimed kernel dimensions. These checks establish the conditions
for the reduction rather than treating an arbitrary15-by15 test as the
original transfer determinant.

## Shared ports really are shared

Let U_D be the span of the24 source forms physically output at D across
all six stripes and both phases. For every receiver S, the span
`W_S=sum_(D in S) U_D` has dimension360 because its projection onto
either donor is invertible. Consequently all fifteen U_D have their
full24 dimensions and form a direct sum for that receiver. Every U_D
is contained in every W_S whose receiver sees D.

For any subset J of S the sum of the actual U_D has dimension24|J|.
In particular the common-function/outgoing-plane independent-
representatives inequalities are satisfied by these explicitly chosen
subspaces, including simultaneous reuse of each port by all receivers.
The global collection of45 ports retains all720 source dimensions,
because A reveals the540 early dimensions and B's native late columns
have rank180. No repeated-scalar collapse is imposed.

## Literal whole-record implementation and invoice

Expand every F128 symbol into seven binary records. The V90 map is a
630-by630 invertible binary matrix, compiled to a literal167,325-ADD
in-place word. Each ADD has two distinct co-located public records.
Gaussian elimination and its reverse require no helper, MOVE, INIT or
CLEAR. The same word is used for each early and late stripe.

The C term uses the explicit binary multiplication matrix of each field
coefficient. It is implemented by additions from the630 stationary
binary cache records to the630 real late output records. Depending on
H, this takes196,376..200,103 ADDs per stripe. Capturing and retaining
the90 early fields costs630 INIT and630 copy-ADD per stripe, followed
by630 dirty CLEAR after the late additions. There are six stripes.

Allowing at most89 field swaps to put each phase's physical holders in
the specified input-column order adds at most `89*3*7=1869` ADDs per
phase per stripe. All swaps are co-located at H and use three XORs per
binary lane; they do not introduce movement. This gives:

| Charged local item | Per H | All227 H |
| --- | ---: | ---: |
| ADD, including cache copies and holder permutation bound | 3,212,364..3,234,726 | 731,944,362 |
| INIT of stationary cache records | 3,780 | 858,060 |
| Dirty CLEAR of the same owners | 3,780 | 858,060 |
| Additional MOVE | 0 | 0 |

`replay.py` replays the complete two-wave binary word on all1,260
independent original columns for one actual H stripe, including an
arbitrary independent late baseline. It checks all cache owners remain
dirty and that the desired triangular matrix is obtained. Omitting a
cache copy or the crosswave stage changes the output and is rejected.
With C=0 each donor projection has rank at most45 instead of60, so the
stationary cache is mathematically necessary for this displayed design.

The companion replay also compiles the full-three-donor V45 interface
over the same F128, so one field can be used on all1,108 ordinary H.
Those combined local costs are recorded in `REPLAY-RESULT.json`. The
source encoding, remaining chart maps, all global restoration and
preload operations, the existing true MOVE profile, ordinary body
passes and recursive caller costs remain separately chargeable.

## Open next questions

The immediate global compatibility problem is to realize each H's two
or three formal source quotient banks as actual maps of each donor's
same5760-dimensional original bank, with the inverse lifts agreeing at
each receiver. The positive local maps do not solve that coupled
problem. They supply concrete array-valued target spaces for attempting
it. The eleven singleton planes and later D-to-K-to-F interfaces also
need a separate construction. A complete diagonal native transfer and
all five foundations remain open.

Dependencies: pinned layout SHA256
`9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72`,
the retained `bit-all111-balanced-causal-atlas/author/BALANCED-PROOF.md`
holder formula, the balanced-quotient theorem of this session, and the
retained outgoing-plane common-function criterion. Credit @CubeJerry,
the native-source/chart authors, and S023 Worker A with substantial
OpenAI assistance.
