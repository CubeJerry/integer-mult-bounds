# Near-minimum return rank still forces genuine late source information

**Proved for linear proper transfers on the retained native mask and balanced
routes; no new κ.** Allow the return bank itself to change. A return bank close
to the native rank minimum still forces every foreign proper block to have
large rank. This extends the late-source-line obligation beyond the old fixed
canonical bank, whose exact identity-block conclusion no longer applies.

## 1. Statements and scope

Let A be a fitting on the authenticated111-role native graph over a field of
characteristic two. Each block has arbitrary positive dimension b, diagonal
blocks are I_b and every noncontact block is zero. No symmetry, commutativity,
Schur invertibility or foreign-block invertibility is assumed. Write

    rank A=9b+h,              h>=0.

The rank minimum9b is the retained native theorem. Put B=A-I. Its foreign
blocks agree with those of A, and it is zero at every nonforeign pair.

**Theorem 1 (all native foreign blocks).** Every one of the6470 directed
foreign blocks satisfies

    rank B_ij >= b-floor(9h/2).                         (1)

The finite native certificate actually gives stronger coefficients for most
pairs. For2967 of the3235 unordered pairs the coefficient is3; for261 it is
7/2. The remaining certified coefficients are recorded below. The constant
9/2 is a valid uniform upper bound, not asserted optimal.

**Theorem 2 (replacement-bank late-source gate).** Fix a linear proper
programme on the retained balanced routes, with its genuine early X stage,
invertible pure-Y map and source restorations. Permit an arbitrary replacement
Hub-to-ground return bank, including nonlinear encoders and preloads for that
fixed linear proper word. If every proper contribution from donor77 is acquired
only after its early X records have left the native line, then completion of
all native outputs requires at least

    q >= 9b+ceil(b/6)                                  (2)

return field-symbol records, on an integral replication of the b=5760 atlas.
In particular an entirely post-line source acquisition scheme has the same
lower bound. At b=5760 this is960 excess symbols, whereas the target limiting
movement allowance is only202 excess symbols. The exclusion does not assume
the return bank is the retained canonical one.

More generally, at the admissible screen h<=202 with b=5760, all native
foreign pairs require positive information beyond their early first cut.
The full certificate gives at least1554 additional independent source
dimensions for every pair, and2274 for receiver5 from donor77. These are
dimensions on overlapping source cuts, not new MOVE counts or additive
independent costs across receivers.

## 2. The inherited star inequality in an eight-point frame

Take any eight native roles F having pairwise noncontacts. Since A_FF=I_8b,
normalize a rank factorization A=C R so their factors are coordinate
projections and inclusions on eight b-dimensional point blocks. The
remaining factor space has dimension b+h. A role with contacts to precisely
two frame points a,b has row and column factors supported on a,b and this
remaining space. Call it an edge role e={a,b}. If two such edge roles share
one point, the certificate checks that their mutual native blocks are zero.

For the selected edge roles define, as in the retained saturated-star proof,

    alpha_e(a)=C_ea R_ea,
    S_e=C_e,* R_e,*,
    gamma_e(a)=alpha_e(a)+S_e,
    g_e(a)=rank gamma_e(a),
    G_a=sum_(e incident to a) g_e(a).

The diagonal condition gives

    alpha_e(a)=I-gamma_e(b).

The LR inequality, credited to DreamingOfClouds PR#7114 and rederived in the
reviewed saturated-star package, is

    G_a <= h+2(g_e(a)+g_e(b)).                          (3)

It holds for any selected star subgraph within the frame. Its proof uses
only the prescribed shared-point zeros and elementary rank inequalities:
stack the edge factors on the point-plus-last space, where the pair product
is block diagonal with ranks g_e(a), then compare the row/column kernels.
The last space is rectangular of dimension b+h; it need not identify with
a physical record or supply an invertible Schur factor.

Both actual point-edge contact blocks have rank at least rank alpha_e(a).
Therefore

    b-rank A_(a,e) <= g_e(b),
    b-rank A_(e,a) <= g_e(b).                          (4)

Notice the opposite endpoint in (4). The exact native certificate records
this index, rather than silently interchanging the two incidence variables.

## 3. Complete-six and complete-seven incidence bounds

Here all g variables are nonnegative ranks and satisfy (3). The following
averages do not assume symmetry of the actual matrix or its factors.

### Six-point clique: g_e(a)<=7h/2

Fix a directed edge e={a,b} in a complete K6 of edge roles, and let T be its
four other points. Write x=g_e(a), y=g_e(b). Let A,B be the averages of
g_(a,t)(a),g_(a,t)(t) over t in T; let C,D be the analogous averages on
b-to-T edges. Let E be the average of g_(t,u)(t) over directed incidences
inside T. The average G at a point of T is B+D+3E.

Averaging (3) on four incidence classes gives

    x+2A-2B <= h,
    B+D-E   <= h,
    B+3E-2C-D <= h,
    y+2C-2D <= h.

Weight these by1,3/2,1/2,1/2. Their sum is

    x+2A+y/2 <=7h/2.

Thus x<=7h/2. This constant is sharp for the LR relaxation: with h=1,
the nonnegative values

    (x,y,A,B,C,D,E)=(7/2,0,0,5/4,1/2,0,1/4)

satisfy every directed LR inequality of the complete K6. They are not
asserted to be ranks of an actual matrix representation.

### Seven-point clique: g_e(a)<=3h

For a complete K7, T has five points and its average G is B+D+4E.
Two averaged inequalities suffice:

    x+3A-2B <=h,        B+D<=h.

Adding twice the second to the first yields x+3A+2D<=3h, so x<=3h.
Again the coefficient is sharp for the LR relaxation: take x=3h,
B=h, and all the other displayed averages zero.

The frame still has eight independent point blocks. The six- or seven-
point clique selects edge roles within that frame; it does not remove
point coordinates or replace b+h by a different uncharged last space.

## 4. A finite native cover for every contact

`CERTIFICATE.json.gz` contains621 actual eight-point frames and eight
rational LR duals. Its uncompressed SHA256 is
`e7015bd9e1111ec8d4c3ebaa30460d767b66ea1d7e8a33279b9f033c0053dc57`.
The checker reconstructs point/edge incidence using exact integer root dot
products. For each frame it checks eight distinct original native points,
all their mutual noncontacts, every listed edge role's exact two contacts,
uniqueness of those edge roles, and all shared-point zero blocks.

Complete K6/K7 subgraphs give the preceding symbolic coefficients. The
eight additional certificates use the same LR system directly. Let its
nonnegative variables be g_e(a), and put its inequalities into Mg<=h1.
For the desired opposite-endpoint variable with objective vector c, a
certificate supplies rational lambda>=0 such that

    lambda^T M>=c^T.

Then c^Tg<=h sum lambda. Verification uses exact fractions, not an LP
solver or numerical tolerance. The chosen residual certificates are:

| Unordered foreign pair | Certified coefficient |
| --- | ---: |
| (7,80) | 9/2 |
| (10,81) | 9/2 |
| (41,80) | 27/8 |
| (42,51) | 19/5 |
| (51,53) | 7/2 |
| (80,96) | 35/9 |
| (81,95) | 35/9 |
| (99,103) | 19/5 |

Every native unordered contact is covered, and (4) covers both directions.
Integer ranks give the floors in (1). The cover is a sufficient certificate,
not an enumeration of all frames or a claim that the eight pairs lack other
possible clique witnesses. No impossibility is inferred from the discovery
search that found these certificates.

## 5. One explicit native witness survives a changed return bank

The critical frame is

    F=[9,30,37,46,52,77,92,101].

Its frame positions0 through6 form a complete K7 of native edge roles.
Native role5 is the edge joining positions0 and5, namely points9 and77.
Equation (4) and the K7 bound therefore give

    rank B_(5,77) >= b-3h.                             (5)

The literal balanced early cut for this donor/receiver pair is exactly

    E_(5,77)=b/2.

At b=5760 it consists of2880 actual early source symbols. It is obtained by
summing45x_H over the sixteen source planes through77 inside receiver5's
facet, using the pinned balanced factor. This is a first-cut capacity;
every proper path from77 to5 begins through one of those branches.

If no genuinely new information about X_77 is read at its native line after
the early departures, every later plane/middle/facet cache is a function of
information that already crossed those early branches. Arbitrary linear
recoding and same-chart snapshots cannot increase the transfer rank past
E_(5,77). Thus a post-line-only proper word satisfies

    rank B_(5,77)<=b/2.

Together with (5) this forces h>=b/6.

Why can the replacement bank not be hidden inside this cut? For a fixed
linear proper word write the late endpoint map as Gz+Bx, with G invertible.
The new X-dependent ground bank affects z; B is its zero-ground-input proper
transfer. Exact completion needs the ground bank to determine (I+B)x.
The separately proved replacement-bank theorem gives q>=rank(I+B)=9b+h,
even for nonlinear return encoders and preloads. Hence q>=9b+ceil(b/6).
The return channel has been counted independently, rather than neutralized
by an invalid receiver-by-receiver canonical-zero argument.

This proof assumes the retained proper route interface and no additional
informative descents to other charts or uncharged raw source access. Such
changes need their own physical source and invoice. Nonlinear proper
transfers are outside this rank argument.

## 6. All-pair late dimensions and the target cost

For each foreign pair the checker computes its exact early first-cut
capacity E_ij, between2880 and3600 at b5760, and its certified coefficient
c_ij. A fitting of rank at most9b+202 must satisfy

    rank B_ij >=5760-floor(202c_ij).

Consequently the proper information entering from genuine late source-line
taps must contribute at least

    5760-floor(202c_ij)-E_ij

dimensions beyond the early cut. The smallest value across all6470 pairs
is1554. For the explicit pair(5,77) it is2274. These quantities do not add
across different pairs: the same late information can be shared, and the
proof makes no new MOVE tariff.

In the replacement-bank price, h excess field symbols add(h/b)[8] to the
normalized balanced movement, with [8]=8^(199/200). A post-line-only code
requires h/b>=1/6. This costs at least[8]/6>7/6, whereas the entire retained
limiting room is less than279/1000. The exact inequality [8]>7 follows from
8^199>7^200. The checker also constructs rational200th-root enclosures for
the retained limiting room. It also verifies T_2-P_2<0 and the retained
identity B_m=B_infinity+(T_2-P_2)/(36(m-1)); every finite paired budget is
therefore below that limit. Thus this model fails the target movement
comparison at every even m>=2, before any ordinary, precision, storage or
recursive costs.

At b5760 the rank lower bound is960 excess symbols. The same comparison
that permits only202 gives a strict failure. Replicating field copies or
tensoring with a body identity preserves the ratios; no normalization by
successful output coordinates is used.

## 7. Verification and next step

Run `python3 check.py --repo REPOSITORY --out OUTPUT`. Expected status:
`PASS_NATIVE_NEAR_MINIMUM_FOREIGN_RANK`. No optimizer is used. The exact
native cover, opposite-endpoint indices, rational dual inequalities,
all6470 early cuts, the critical frame and the elementary K6/K7 duals are
checked. Negative controls reject corrupted dual weights and a coefficient
below the sharp LR-relaxation value.

The new constructive requirement is quantitative: a promising low-rank
replacement-bank code must still integrate genuine late line information
with its early source maps. The earlier local array constructions and
global source gluing remain relevant. This result does not prove their
compatibility, materialize a low-rank B, discharge a foundation, provide
the complex supplier or establish a complete κ bound.

Credit @CubeJerry, the retained native and balanced-route authors,
DreamingOfClouds for the LR inequality in PR#7114, and the reviewed S011
saturated-star derivation and S023 first-cut analysis. This extension was
developed by S026 Worker C with substantial OpenAI assistance. Independent
review is recorded separately; no human or formal-kernel review is claimed.
