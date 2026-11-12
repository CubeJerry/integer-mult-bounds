# A source-bound eight-packet endpoint prefix

**Proved finite partial construction. No new κ.** This package supplies a
literal 1,880-input prefix, not a complete shared native or a supplier.
Its output is an explicit endpoint code with a precisely identified residual.
The E8 rank-eight representation is established mathematical background; the
contribution here is the dyadic source binding, physical prefix, reservation
ledger and continuation contract for this programme's pinned word.

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
The source and earlier native/geometry contributors retain their credit.

## 1. Fixed source and input contract

The source is `research/shared-wire-split-composition/data/final.json.gz`,
SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`,
from programme baseline `be00a963d4a8c96681a9f6df691a694f1b4fc853`.
It has1,480 public fields and71,261 instructions. Let M be the union of
the104 first X roles, their Y roles X+112, and the96 hosted X2/Y2 pairs.
Then |M|=400. Begin with independent common fields u and independent second
main fields v_M, in the source's prescribed initial charts. Form the actual
differences q_r=v_r-u_r by400 cochart ADDs. This is an invertible change of
coordinates on all1,880 inputs, not a zero-common specialization.

For first ports i=1,...,104, write X_i for the actual live role and v_i for
its binary source-line vector. The source contains70 vectors of weight3
and34 of weight7. X_i ends in the full nine-dimensional chart127. Y_i=X_i+112
starts at the empty chart3 and ends at the hyperplane v_i-perp. These equalities
are checked as binary subspaces, not inferred from frame names.

For the96 ordinary ports let c_i=1; for the eight complementary indices of
`hosted.Dports` let c_i=1/2. The desired first Y endpoint is
c_i(q_Yi+q_Xi). The coupled X endpoint has a separate reverse duty. The full
native endpoint map and that duty are authenticated in the accompanying
endpoint-completion package; the prefix itself proves the displayed output
without assuming a source endpoint theorem.

## 2. Dyadic representation and exact conditional decoder

For any v in F2^9 of weight3 or7, define a(v) in Z^8 as follows. Coordinates
are numbered1,...,9 in this definition.

* Weight3, support containing9: put2 in its other two support positions and0
  elsewhere.
* Weight3, support excluding9: put1 on the three support positions and-1 on
  the other five positions.
* Weight7, missing i<j<=8: put2 at i,-2 at j and0 elsewhere.
* Weight7, missing i<9 and9: put1 at i and-1 in the other seven positions.

For every pair of distinct such vectors,

    a(v).a(v)=8,
    a(v).a(w)=0        if v.w=1 in F2,
    a(v).a(w) in{−4,4} if v.w=0 in F2.

Here is a proof over the rationals, rather than an inference from the finite
checker. In Q^9 put r(v)=1_support−(1/3)1 for weight3, and r(v)=e_i−e_j
for weight7 with missing i<j. Every r has coordinate sum0 and squared norm2.
For two triples with intersection size h, r(v).r(w)=h−1. Distinct triples
have h in{0,1,2}, giving exactly the stated binary-parity condition. For a
triple and a missing pair, the dot product is the difference of the two
membership indicators; it is zero when the binary intersection has odd
size and±1 otherwise. For two missing pairs it is zero for disjoint pairs
and±1 for a one-element intersection. Their binary intersections have odd
and even size respectively. For x,y with coordinate sum0, the map

    t(x)_k=x_k+x_9/2, 1<=k<=8,

is an isometry: expanding its dot product uses sum_{k<=8}x_k=−x_9 and gives
x.y exactly. Thus a(v)=2t(r(v)) has the displayed integer formula and Gram
identity. The rational1/3 occurs only in this proof; the literal construction
uses integer encoding and dyadic decoding coefficients. Exact elimination
checks rank8 on the actual104 columns.

For arbitrary V>=1 over a characteristic-zero scalar field, take q_i in F^V,
and form eight complete-field packets P_k=sum_i a(v_i)_k q_i. Let G_ij be
a(v_i).a(v_j). Then

    q_i = (a(v_i).P − s_i)/8,
    s_i = sum_{j!=i} G_ij q_j.

Only binary-orthogonal off-diagonal ports contribute to s_i. It is sufficient
to obtain this one weighted sum at receiver i; it is not necessary to obtain
every individual q_j separately. Conversely, possession of eight packets
alone does not supply any s_i. The source-specific side-information theorem
tests a particular funded way of obtaining them and excludes that way.

The fixed E8 Gram matrix and the rank13 window in upstream #7014 have opposite
zero masks. No rank13-window theorem or physical hosting result is used here.
Related root-code and fitting-matrix work, including #3040 and #3045, is not
claimed as new or contradicted by this prefix.

## 3. Literal construction with charged packet distribution

Retiming below is legal for the private rail because this prefix executes no
ordinary part of the common native. Its1,480 common fields remain untouched.
Every private carrier follows the same ordered proper nested charts as its
own source itinerary. A reservation is consumed once even though retimed.

1. Form all400 actual differences.
2. Hoist all104 q_X carriers along their own funded raw-main itineraries to127.
   Other raw carriers remain initial.
3. Scale each of the eight coupled raw Y fields by1/2 at chart3.
4. For k=1,...,8, initialize a fresh owned field at127, add the nonzero terms
   of P_k from the retained q_X fields, transport it127→3 by one newly paid
   rank9 call, and add c_i a(v_i)_k/8 times it to every applicable raw Y_i.
   Retire this packet at3 under the retained dirty-owned erasure contract.
   The next lifetime may reuse the same label, initialized at its declared
   chart127; allocation/reinitialization and physical positioning are not
   free machine services and remain in the eventual compiler tariff.
5. Execute each raw Y carrier's own remaining funded itinerary to its facet.

All scalar reads are cochart. All public movements ascend, and each packet
descent is explicitly owned. No receiver multicast transport is hidden:
the tailored packet combination rides in that receiver's own raw field.
The packet operations need one additional simultaneous owned field, eight
lifetimes, and eight INIT/CLEAR pairs. Common-owned fields are not live yet;
the prefix's peak1 is not a bound for a later assembled execution.

At the boundary every common row and chart is initial. Every q_X is unchanged
at127. Other raw fields outside the first104 X/Y pairs remain initial. Each
first Y is at its required facet with value

    z_i = c_i q_Yi + (c_i/8) sum_j G_ij q_Xj
        = c_i(q_Yi+q_Xi) + (c_i/8)s_i.

This proves the partial postcondition. The1,880-column exact replay verifies
the complete map, chart typing and reservation lineage. All input information
survives: q_X remains, so each q_Y is algebraically recovered as
z_i/c_i−sum_j G_ij q_Xj/8. This global inverse is an information statement,
not a free local recovery operation at the receiver.

## 4. Complete prefix invoice and what it does not fund

The literal word has2,362 instructions:

| Operation | Count |
|---|---:|
| ADD |1,440 =400 boundary +520 encoding +520 receiver mixing|
| SCALE |8|
| MOVE |898 =890 distinct raw-main reservations +8 new rank9|
| INIT / CLEAR |8 /8|

There are520 nonzero entries in the source root matrix. Of the1,710 total
raw-main reservations,820 are unexecuted. None of the47 second-owned
reservations is consumed or granted by this prefix. A complete continuation
must implement all of their former duties or pay for retained calls.

At κ=1/200 the new paid moment is exactly8·9^(199/200) per native. Relative
to the counterfactual H4 profile, the remaining allowance is about27.18574865
per native, before any additional paid route or restoration. This subtraction
does not supply H4, change its targets, admit physical scalar service, or
establish a uniform complex supplier. The H4 and S8 invoices cannot be mixed.
The companion exact budget certificate gives directed rational bounds.

## 5. Continuation and rigorous limits

To finish each forward endpoint, the actual value c_i s_i/8 must be subtracted
at its facet, or an equivalent version-safe correction must be made earlier
while the raw Y is accessible. A source-aligned correction needs a new schedule
if this fully hoisted prefix has consumed a route it would use. Every history,
common displacement, owned obligation and restoration must be accounted for.
The prefix does not grant any of these corrections, the96 reverse hosted
Y2→X2 duties, the eight coupled reverse duties, the common native execution,
400 final recouplings, or a complete all-size invoice.

The independently checked side-information obstruction shows that the simple
fixed timed transport graph cannot finish this code even with very favorable
information grants. It does not exclude changed common responses, receiver
processing, different reuse schedules, nonneutral joint substitutions, or a
different code. Those are the next physical obligations, not successful
constructions inferred from the favorable eight-packet arithmetic.

The five retained foundations remain visible: native_all_columns,
owned_erasure, compiler, precision_tape and analytic_recovery. This normalized
finite word inherits their physical meanings; no global foundational assumption
is discharged. Coefficient precision and ordinary/tape/allocation services
must be priced in a complete supplier. No complete κ is claimed.

## 6. Verification and open next question

`verify.py` authenticates the native, regenerates every instruction, verifies
all1880 input-column postconditions and proves the explicit information inverse.
It also checks all14,400 pairs of the120-port Gram identity as finite
corroboration of Section2, and rejects sign, missing-route, public-descent,
missing-input, normalization and repeated-reservation mutants. The independent
review must reconstruct the word and algebra separately, not import this code.

The next decisive proposition is an actual low-cost realization of the104
weighted corrections s_i under an access model stronger than the excluded
transport-only graph, with the full common endpoint restored and all reverse
duties and remaining costs charged. A single literal correction with a
composable shared mechanism is the first test.
