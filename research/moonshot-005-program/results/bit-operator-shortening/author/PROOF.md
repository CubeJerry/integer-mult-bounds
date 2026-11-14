# Operator-valued receiver shortening and an eight-packet obstruction

**New universal linear theorem with exact native premises; independent review
pending. No new kappa.** The theorem applies to arbitrary operator-valued
historical spaces, without requiring a scalar code tensored across records.
It forces a specific kind of local direction in any eight-packet source.
A separate application excludes the fixed nineteen-dimensional scalar code
C+U, even when a computation inside its tensor extension uses noncommuting
blocks. It does not assert a dimension-only lower bound on arbitrary codes.

The native input is the same authenticated111-root BIT gzip, SHA256
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.

## 1. A fitting bound robust to eight omitted receivers

Let S be any subset of the111 native ports, omitting d=111-|S| ports. Over
any characteristic-two field F and for every integer V>=1, let A be a block
matrix on S with V-by-V blocks, identity diagonal, and zeros at all forbidden
native noncontacts. No symmetry, scalar, tensor, or commuting-block condition
is imposed. Then

    rank A >= (9-d/10)V.                                      (1)

In particular, omitting at most eight ports still leaves

    rank A >= (41/5)V > 8V.                                  (2)

An integer rank is at least the ceiling of the displayed rational bound.
This is a bound for every choice of omitted ports, not a sampled deletion
test. It also applies to a rectangular fitting with rows S and all111 input
columns, by restricting to its S principal submatrix.

### The native finite certificate

The credited minimum-rank-nine proof used nine independent eight-port frames
whose vertex incidences are all even. A frame here has pairwise REAL
NONorthogonal distinct roots, hence its fitting principal matrix is identity.
The present certificate supplies thirty such nine-frame configurations.
Within EACH configuration every vertex occurs an even number of times and
there are72 total incidences. Across the thirty configurations, each native
vertex has at most24 incidences. Every frame is checked directly against the
native rational roots; no symmetry or completeness of a frame search is
needed to accept this finite witness family.

### Proof allowing deleted vertices

Factor A=C R through an r-dimensional space. For each original frame f,
let f'=f intersect S. Then C_f' R_f'=I_(|f'|V), so

    P_f=R_f' C_f',       Q_f=I_r-P_f

are complementary idempotents of ranks |f'|V and r-|f'|V. Empty intersections
are permitted. Within one configuration, even incidence remains even after
deleting vertices, so sum_f P_f=0. There are nine frames; characteristic two
therefore gives sum_f Q_f=I_r. Rank subadditivity yields

    8r >= sum_f |f intersect S| V
       = (72 - lost_incidences_in_this_configuration)V.

Sum this inequality over all thirty configurations. Each omitted port costs
at most24 incidences in that sum. Thus

    240r >= (2160-24d)V,

which is exactly (1). Crucially, deleted vertices shorten their frames; the
proof never treats a shortened frame as an eight-dimensional identity.
This extends the credited parity-projector method with a balanced native
witness family. It is not a claim that the old single witness survives all
deletions unchanged.

## 2. The operator-valued local quotient principle

Use the admitted arbitrary-Y historical normalization and its actual route
model:111 original X records ascend from their root lines to Hub;111 original
Y records ascend from zero to their distinct final facets; q persistent
whole-V packets descend from Hub to zero. Zero-born stationary caches and
extra zero-born ascending records are allowed, but no uncounted descending
copies, packet restarts, nonmonotone paths, nonlocal initial values, or
cross-chart reads are granted. Original y inputs remain arbitrary. All value
operations may use arbitrary noncommuting V-by-V matrices.

Let the ambient X coefficient space be E=F^{1 by111V}. For a real chart C,
define Local(C) as the coordinate subspace of E supported only on those
original X root lines contained in C. This refers to full input block
columns; an arbitrary row may have rank-deficient or partial coefficients.

Let W be ANY linear subspace of E containing the X projections of the
actual historical coordinates G in the admitted normal form. It need not
be a scalar tensor code. Every actual history at a proper chart C then has
X coefficient rows in

    W + Local(C).                                            (3)

For any downset D of visited proper charts, define

    Q_D = sum_(C in D) [W intersect Local(C)]  subset W.       (4)

Only actually visited charts need appear in this finite sum. One may use a
larger downset of real charts as a relaxation. The word 'shortening' here
means the ordinary intersection in (4): global historical-code rows whose
input support is confined to that chart. Such rows need not be physically
available there; (4) grants all of them, so it is a necessary-condition
relaxation, not a free acquisition service.

If h=w+l is a representation from (3), the class w+Q_D is independent of
the representation, because two choices differ by W intersect Local(C).
Call it pi_C(h). These quotient classes agree along nested MOVEs inside D:
both decompositions can be compared at the LARGER chart, and their difference
lies in its shortened space. This works for downward as well as upward
MOVEs. Coframe operations take linear combinations of quotient classes.
Arbitrary unknown-Y feedback does not affect this X-coefficient argument;
it remains part of the required full source equations.

Original X inputs born in D have quotient class zero by choosing w=0;
original Y and zero-born records do also. Ascending carriers born outside a
downset cannot enter it. A persistent descending packet first enters a
downset at most once. Therefore, if all nonzero entering information comes
from q such first entries, the span P_bar of all quotient histories in D
has dimension at most qV. This is a statement about all chronological
histories, with no simultaneity assumption. Choose any linear lift P in W
of P_bar, with dim P=dim P_bar. Then every in-D history has X rows in

    P + Q_D + Local(C),       dim P <= qV.                    (5)

The same reasoning gives a general cut theorem when other paid entering
channels exist: add their actual full information dimensions to qV. No
unlisted channel may be treated as a zero-cost seed.

## 3. A positive shortening requirement for every eight-packet source

Choose D to contain all visited STRICT subspaces of any native receiver
facet F_i. It is a downset, consisting of charts of dimension at most six.
Every original X root is in D: the native checker verifies that every port
has a distinct orthogonal partner facet containing its line. Every original
Y begins at zero in D. All proper predecessors of every terminal Y path
are in D.

Let S be the receivers whose terminal facets are visited by NO descending
packet. Each packet visits at most one seven-dimensional facet, so at most
q receivers are omitted from S. At F_i for i in S, all incoming nonzero
information comes from ascending histories at proper predecessor charts
in D. Stationary births are zero, and there is no packet arriving directly
from outside D. Equation (5) and local operations therefore express the
final X coefficient e_i tensor I_V as

    e_i tensor I_V = A_i + B_i,
    row(A_i) subset P+Q_D,    row(B_i) subset Local(F_i).

The A_i are fitting rows: their own diagonal block is I_V because the own
root lies outside F_i, and all forbidden noncontact columns are zero. Stack
these rows for i in S. Then

    rank A_S <= qV+dim Q_D.                                 (6)

For q=8, the robust bound (2) applies to this rectangular fitting. Combining
(2) and (6) gives the universal necessary condition

    dim Q_D >= V/5.                                         (7)

Thus every complete eight-packet source in this route model must have at
least ceil(V/5) independent X-coefficient directions in the span of its
historical-code shortenings at proper receiver predecessors. It is not
enough for all nonzero local intersections to first appear at terminal
facets. This conclusion allows arbitrary operator-valued W, noncommuting
blocks, deficient ranks, interleaving, arbitrary Y feedback, and extra
ascending zero-born records. It is not obtained by extrapolating a scalar
dimension threshold to general block codes.

The result does not say that these shortened directions have already been
acquired, that they each cost a whole additional packet, or that their
ordinary/owned work is free. It identifies a structural property that the
actual historical code of a successful construction must possess.

## 4. Application: the full canonical-plus-class code cannot supply q8

Let C be the native canonical nine-code and U the fifteen-class indicator
code. The admitted source identities give dim(C+U)=19 over F2. Write
W_star=C+U. A fresh exact restriction check establishes for every native
receiver i

    W_star intersect Local(F_i) = span{L_i},
    L_i=K_i+u_class(i).                                     (8)

Each L_i has support spanning its ENTIRE seven-dimensional real facet F_i.
The certificate supplies seven independent actual root lines from its
support for every i. Consequently, for EVERY proper real C'<F_i,

    W_star intersect Local(C') = 0.                         (9)

This universal real-subspace statement follows from (8) and the seven-line
rank witness; it does not enumerate only hosted chart IDs. Binary ranks and
identities persist over any characteristic-two field. Tensoring with F^V
preserves the intersections with these coordinate-support subspaces, so
(9) holds in W_star tensor F^V as well.

If an actual eight-packet source has its historical X-code contained in
this FIXED tensor code, take W=W_star tensor F^V in the quotient theorem.
Then Q_D=0, contradicting (7). Thus q8 is impossible for ANY historical
subspace of this canonical-plus-class tensor code, even if the computation
uses arbitrary noncommuting block operations and arbitrary Y feedback.
The subspace need not contain U or equal one of the earlier W_c candidates.

This is not an exclusion of arbitrary19V-dimensional spaces or of all
eight-packet sources. A changed code with appropriate lower-dimensional
local shortenings can escape. The masked-coordinate representation from
the preceding package provides a concrete example of the relevant change:
K_i and H_i=K_i+x_i together generate the coordinate direction x_i, which
is local already on a line. Its current one-exchange history still fails
the103 noncoordinate fitting requirements, so that example is a mechanism
lead rather than a complete source.

Nine and ten packets remain outside this q8 conclusion. The separate
retained caller cap excludes eleven or more packets in the stated target
envelope; it must not be used to claim that this theorem also excludes the
two remaining counts.

## 5. Verification, evidence, and next construction

`CERTIFICATE.json` contains the thirty native parity configurations.
`verify.py` authenticates the native input and checks every frame, even
incidence within each nine-frame group, the aggregate maximum24, all
111 class-code local nullities, and all111 seven-root support witnesses.
It reconstructs the classes and canonical code directly from native roots.
The exploratory witness search is not imported by the verifier. Exact
binary and rational arithmetic is used; there is no numerical tolerance.

Controls reject a shortened frame falsely counted as full, missing or
duplicated frame data, an understated incidence ceiling, a corrupted native
input, and a proper-support claim obtained by dropping a necessary root.
The written factorization and quotient arguments supply all-field/all-width
quantifiers; finite checks establish their named source premises only.

The next constructive question is to design an actual historical code with
enough locally supported predecessor directions, including sign-sensitive
directions that the masked-coordinate trial lacks, then acquire and use
those directions on the same eight descending paths. No codeword is a
physical read until its chronology, restoration, ownership, precision,
compiler, and complete supplier invoice have been proved.

Credit the programme's native minimum-rank-nine parity projector argument,
the arbitrary-Y historical normalization, and the original BIT/E8 and
class-code authors. The new pieces are deletion-robust parity balancing,
the operator-valued shortening quotient principle, and the source-wide
canonical-plus-class q8 consequence. Prepared for @CubeJerry with
substantial OpenAI assistance. No independent human/formal-kernel review,
new supplier, foundational-assumption closure, or new kappa is claimed.
