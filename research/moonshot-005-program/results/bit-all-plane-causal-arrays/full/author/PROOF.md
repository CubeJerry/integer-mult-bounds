# An explicit causal array interface for all 881 full native planes

## Positive local theorem

Every A2 plane containing three native donors in the pinned balanced
source admits an explicit, invertible, causal array map on its actual
early and late fields, over `F64=F2[z]/(z^6+z+1)`.

The plane has 45 actual D4 output ports, each of 24 field symbols. Its
three donor quotient inputs each have 360 field symbols. For every native
receiver seeing the plane, its fifteen actual ports define a 360-dimensional
target space whose projection onto **each** of the three donor inputs is
invertible. The 45 port spaces are independent, and every receiver's
target is their exact direct sum. Consequently every actual shared-port
rank inequality is satisfied. Receiver target spaces have intermediate
intersections: 72 or 144 field dimensions for distinct native receivers,
instead of the zero-or-full intersections of identical scalar stripes.

The construction is fully explicit, uses the same `F64` for all 881 full
planes, and is compiled to whole-record binary ADDs. It consumes no extra
MOVEs, INIT or CLEAR at the H layer. It is a local source-quotient/port
interface, **not** a construction of globally compatible native source
quotients or the subsequent D-to-K-to-F transport. All three whole-bank
input maps and the timing/counting conditions are part of the theorem;
global diagonal cancellation and the complete supplier remain open.

## The exact colour counts

At a full native H the balanced integer factor gives `x=4,5,6` early
holders per donor per H-D flag. Set

    e=3x,       l=24-3x=3(8-x).

Each of the three donors contributes `45x=15e` early symbols and
`45(8-x)=15l` late symbols. Each of the 45 D4 ports carries e early and
l late symbols. Both phases therefore have equal input and output
dimensions separately: `45e` early, `45l` late. All late holders visited
one of these three real source lines; no synthetic or padding donor is
introduced.

The three actual cases are:

| Planes | x | Early symbols per D port | Late symbols per D port |
| ---: | ---: | ---: | ---: |
| 709 | 4 | 12 | 12 |
| 84 | 5 | 15 | 9 |
| 88 | 6 | 18 | 6 |

Within either phase, partition the real holders into e or l stripes of
45 field symbols. Every stripe has fifteen symbols from each donor and
one output holder at each D port. Such a partition respects the literal
flag origins: give each D its **local port ordinal p=0,...,44** in the
sorted list of this H's forty-five actual D4 exits. This is not the global
D4 index. For each donor j, number its x early holders by s=0,...,x-1
and give them stripe `s+x*((j+p) mod 3)`. Across the 45 D flags, each stripe has fifteen from
each donor. Use `8-x` instead of x for the late phase. These are only
indices on genuine existing holders.

## One explicit 45-by-45 map

Choose the 45 distinct nonzero field elements alpha_D with polynomial
representatives 1 through 45. Define

    V[D,t] = alpha_D^t,        0<=D,t<45.

Columns 0..14 belong to donor zero, 15..29 to donor one, and 30..44 to
donor two. Apply this same V separately to every early stripe and every
late stripe. The early matrix reads only genuine early inputs; the late
matrix reads only genuine late inputs. Thus no late input is used before
its physical arrival, and no stationary cache is needed for this local
interface.

V is invertible because its determinant is the nonzero Vandermonde
product `prod_(D<E)(alpha_E-alpha_D)`. Let S be a native receiver's
fifteen actual D ports. Its projection onto donor j is

    V[S,15j .. 15j+14]
    = diag(alpha_D^(15j) : D in S) * V_15(S).

Every alpha is nonzero and the fifteen nodes are distinct. The displayed
15-by-15 matrix is therefore invertible, with an explicit nonzero
determinant. Tensoring it with the e early stripes and l late stripes
gives an invertible 360-by-360 projection onto each complete donor
quotient. This proves the result for every such fifteen-port set, not
only the sets numerically sampled by a search.

The certificate checks the actual geometry for all 29,354 full-plane
receiver incidences and records all 88,062 donor-projection determinant
values. These are finite prerequisites for the explicit universal
Vandermonde argument.

## Exact shared-port subspace arrangement

The 45 rows of V form a basis. With both colour phases included, each
D port spans a 24-dimensional space U_D, and all 45 U_D are independent.
For a receiver with visible set S its target space is

    W_S = direct sum_(D in S) U_D.

For any collection of receivers, intersection of their target spaces is
the direct sum over the intersection of their port sets. In particular

    dim(W_S intersect W_T) = 24 |S intersect T|.

For the actual full-plane geometry, two distinct visible native receivers
share either three or six ports, producing dimensions 72 or 144. For any
subset J of one receiver's ports, `dim(sum_(D in J) U_D)=24|J|`; all
joint independent-representatives inequalities hold with equality. Each
U_D lies in the target of every receiver that actually sees D.

All 45 outputs together retain all `45*24=1080` source field dimensions.
This explicitly avoids the repeated-scalar gate's collapse to a single
360-dimensional aggregate. The maps mix the fifteen source subcoordinates
inside each quotient; they are not identical scalar target lines repeated
over the full quotient width.

## Actual ordinary implementation

Expand each field symbol into its six polynomial-basis binary records.
The exact V map becomes a 270-by-270 invertible binary matrix. The supplied
`ADD-WORD.json.gz` contains a literal 31,355-ADD in-place implementation,
obtained by recording and reversing binary Gaussian row reduction.
Every operation has two distinct co-located records. It needs no spare
record, INIT, CLEAR, MOVE, field-multiply oracle or uncharged scalar unit.
The checker independently replays every one of the 270 original columns.
Reversing the ADD word implements the inverse.

A physical stripe may require permuting its incoming field-holder order
to the stated donor-column order. At most 44 field swaps suffice; each
uses three binary ADDs on each of six lanes. This costs at most 792
additional ADDs per stripe and uses no helper. With exactly 24 stripes
across both phases, a conservative H-layer bound is

    24*(31,355+792) = 771,528 binary whole-record ADDs per plane.

For all 881 full planes together the corresponding bound is 679,716,168
ADDs. These finite costs are additional to source encoding, later chart
maps, global inverses, canonical formation/descent, every ordinary body
pass and recursive accounting. They are not yet charged into a complete
supplier theorem. Existing actual movements keep their invoice; scalar
extension to F64 still costs six binary native copies everywhere.

The early map preserves the complete early X bank invertibly, and the
late map preserves the complete arbitrary Y-baseline bank invertibly.
They do not individually restore each original label. The retained
whole-program construction must pay for its actual Hub X inverse and
ground Y preload gauge, incorporating these local maps. Invertible local
maps allow that interface; they do not make those operations free.

All matrices are fixed finite lane maps. Tensoring the literal binary
word with any positive body identity gives the same implementation at
every body width. This is different from inferring a general compiler
foundation from one finite test.

## Exact remaining compatibility problem

The three donor inputs at H are independent quotient coordinates in this
local theorem. A global native construction must produce them from the
same original X_j at each of its 28 incident planes. For each receiver i
the sixteen visible source quotient maps must have compatible fibres,
and their inverse lifts must agree with the explicit H target coefficients
above. Those equations couple different planes and cannot be solved by
choosing each H's inputs independently.

The 227 two-native-donor planes and eleven singleton planes also require
their own time-compatible interfaces; the full-plane formula does not
silently create a third genuine source at a punctured plane. Finally the
shared D-to-K and terminal maps must transport these common port spaces
with all endpoint and source restorations and the fixed capacities.

The positive result supplies an explicit maximum-information shared-port
interface on the dominant 881-plane family, so a constructive source
search can now use concrete matrix equations instead of an existential
local-plane black box. A compatible global atlas, both suppliers, all five
foundations and the complete kappa theorem remain open.

Credit @CubeJerry, the native geometry and balanced route/factor authors,
the retained outgoing-plane rank criterion, and S023 Worker A with
substantial OpenAI assistance. No new kappa.
