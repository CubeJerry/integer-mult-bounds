# Canonical basis adaptation gives chronological MDS correction at every native receiver

**Proved parametric finite-source construction, independent review requested.
No simultaneous all-receiver decoder or new κ.** Choosing all nonanchor pivots
from one actual source root makes the canonical projection surjective for a
structural reason. An adapted canonical basis then reads each held pivot
through its own descending field. No auxiliary D copies are needed.

## 1. Precise all-receiver-index construction

Fix any native receiver i, any characteristic-two field k and positive original
record width V. Use b=16 GF32 design coordinates, d=5 separately paid binary
banks per coordinate, and B=bd=80 independent native copies. All111B original
X and111B original Y inputs are arbitrary. These are distinct physical records,
not uncharged subdivisions of a wider record.

The independently admitted atlas has28 proper rank-six charts C_a inside F_i;
every actual foreign root belongs to exactly16. The foreign degree f_i lies
between55 and62, and each chart has at least27 actual native contributors.
Let D be the16-by28 Vandermonde decoder on28 distinct GF32 nodes. For each
foreign source l, encode its b coordinates by D_(J_l)^(-1), where J_l is its
16 containing charts, and route each encoded coordinate to its selected chart.

Choose ONE foreign root j. Select12 of its16 containing charts as nonanchors;
the other16 charts are anchors. On every nonanchor chart use that chart's
actual encoded coordinate of X_j as the original-X pivot. These12 field
coordinates are distinct and have h=12d=60 physical binary pivot records.
This choice is always possible and does not invent any source record.

Every GF32 coefficient and inverse expands to a binary matrix. The identities
overF2 remain valid over every characteristic-two k and every V. GF32 is a
finite design device, with no physical extension-field or lane-selection oracle.
All original banks use ordinary whole-record ADDs and actual chart MOVEs.

## 2. Actual prefix while all Y remains at ground

Use B stationary owned anchor caches, each initialized at its actual E6 chart.
After source-root preencoding, an anchor contribution is added to its cache
and that original X moves to Hub. At a nonanchor chart, sum all other assigned
contributions into the chosen X_j pivot and send those contributors to Hub.
Retain the h pivots. Every nonforeign original X goes directly to Hub.

The resulting X transformation z=P x is invertible. It consists of invertible
source-root encodings followed by ADDs into distinct pivots; no pivot is itself
a source of another aggregation. The actual current Hub rows span H of dimension
111B-h, and the actual held rows span D_hold of dimension h. These spaces are
complementary. Encoded Hub values may be read before they are restored.

Let Q_j be the binary B-by-B source preencoder at root j. The inverse column
for held coordinate a is exactly e_j tensor Q_j^(-1)e_a: undoing aggregation
changes contributor columns but leaves the pivot inverse column itself alone.
Consequently all held inverse columns have support on j, and their bank
vectors are h distinct columns of one invertible matrix.

## 3. A canonical basis with one actual pivot read per exceptional field

The scalar canonical code C has dimension9 and K_j has entry1 at j. Choose
K_j together with eight independent canonical rows E_1,...,E_8 vanishing at j.
They span C. Across B independent copies, retain every E_l on each standard
bank, giving8B basis rows. Replace the B bank rows of K_j by

    c_a = sum_k Q_j[a,k] K_j^(k),       a=1,...,B.

This is still a basis of C_can=C tensor k^B of dimension r=9B. Evaluating a
row on a held inverse column gives

    c_a (e_j tensor Q_j^(-1)e_p) = delta_(a,p),
    E_l^(k) (e_j tensor Q_j^(-1)e_p) = 0.                 (1)

Thus exactly h canonical basis rows have a single unit coefficient on the
held values, and the other r-h basis rows have none. For every row c compute
its finite coefficients cP^(-1). Initialize one owned field at Hub and seed
its Hub part using the actual current original-X rows there.

The r-h Hub-only canonical fields descend directly Hub→ground (rank8).
For each of the h exceptional fields, descend Hub→its pivot's E6 chart
(rank2), ADD that ONE actual original pivot into the field, then descend
to ground (rank6). The pivot is not changed and remains available for MDS
correction. Now all r canonical basis fields are exactly present at ground,
while EVERY original Y is still at ground and all h pivots remain below Hub.
No owned record ascends, no future X value is read, and no D helper is used.

The basis change is an actual source-access construction. It does not delete
history modes: completed seeds/transport span r+h, final fields span r, and
partial Hub seed ADD histories can span the full111B. The latter are charged
operations at Hub, not free information at lower receiver charts.

## 4. Preload, local correction and complete endpoints

Express K_i on each original bank in this actual canonical basis and add it
to Y_i at ground. At most r ADDs per Y bank suffice; all are charged. Clear
all r canonical owners after use for the closed word. Preencode Y_i by the
anchor16-column inverse at ground. Move each field coordinate's d banks to
its anchor chart, read its stationary cache, and clear that cache. Move those
original Y records to F_i and apply the anchor postencoding.

Each nonanchor original-X pivot moves up to F_i, adds its D-column contribution
to the cocharted Y_i banks, and continues to Hub. Undo every nonanchor original-X
aggregation and every source-root encoding at Hub. All X originals are now
restored. All other original Y records move directly to their own final facets
and retain their arbitrary initial values. The MDS identity gives

    (y_i+K_i)+M_i = y_i+x_i

independently in all80 copies. Source, geometry, inverse and arbitrary-Y
identities therefore prove the construction for every i,k,V. This computes
ONE chosen native receiver in each copy, not all111. Other productive outputs
must not be counted as completed.

## 5. Exact physical movement and finite ordinary bounds

For a receiver of foreign degree f, the underlying local MDS routes cost

    (B+2h)[1]+(fB-h)[2]+fB[5]+B[6]+(221-f)B[7].          (2)

Every unused original X and Y route is included. The adapted canonical fields
add h[2]+h[6]+(9B-h)[8]. Dividing all terms by the same B=80 copies gives

    Q_i=(5/2)[1]+f_i[2]+f_i[5]+(7/4)[6]
        +(221-f_i)[7]+(33/4)[8].                       (3)

At t199/200 the maximum is at f62, since [2]+[5]-[7]>0. Exact directed price
intervals give Q_max=1611.533586578727361... and movement room
10.217293632424994... against the retained1621.750880211152355... ceiling.
The corresponding hypothetical COMPLETE-native comparison first passes at
even m4. Its all111 endpoint premise is absent here; no caller is admitted.

All non-movement operations have explicit finite upper bounds. Put
L_B=B²+2B; this safely bounds binary Gauss-Jordan reduction, including at
most B(B-1) elimination ADDs and3(B-1) ADDs for swaps. Source/Y encoding and
inversion use at most2(f+1)L_B ADDs. Aggregation/restoration use at most2fB.
Hub seeds use at most r(111B-h) ADDs, pivot patches h, canonical Y preload
Br, anchor reads B, and nonanchor decoding Bh. Hence

    ADD <= 2(f+1)L_B+2fB+r(111B-h)+h+Br+B+Bh.            (4)

For the worst f62 this upper bound is7,249,420; it is intentionally loose.
Exactly INIT=CLEAR=r+B=800 owners are used, all charged as dirty clears.
The number of MOVEs is (232+f)B+2h=18680+80f, at most23640. No allocation,
source read, restoration or copied bank is omitted. Each coefficient table
and finite instruction word is constructible independently of V. Actual
field-operation, control, storage, precision, compiler and recursive costs
remain in the complete supplier interface beyond the movement screen (3).

## 6. Information accounting and exact verification boundary

Every D_hold row is supported inside F_i. The retained canonical local-kernel
property implies C_can intersects that local input space trivially: a canonical
row supported on {i} union foreign(i) is a multiple of K_i, and its own entry
cannot vanish unless the multiple vanishes. Thus C_can intersects D_hold=0.
The projection of C_can into held current coordinates is surjective by (1).
Its kernel has dimension r-h. Completed Hub seeds have rank r; the h changes
on their routes recover independent D_hold rows, so completed seed/transport
history has rank exactly r+h=780. Final ground canonical rank is720. These
statements tensor by V. All partial Hub accumulation states may span8880V;
no hidden use of those unexported states is allowed by this accounting.

The source recipe is proved for every receiver and width. The finite certificate
checks all111 exact atlas/pivot/basis choices, binary decoder/encoder inverses,
canonical dimensions, movement formulas and rigorous prices. It does not claim
that111 enormous80-copy literal words were emitted or independently replayed.
The separate four-copy source is a literal chronological control, with its own
all888-column and rational-chart reviews. Finite checks supplement the explicit
parametric algorithm; they do not establish asymptotics by extrapolation.

## 7. The remaining global composition theorem

This construction resolves canonical preload chronology for each local MDS
receiver. It does not simultaneously form every receiver's chart channels
from the SAME original trajectories. Running111 local words on independent
copies, resetting originals from Hub, or duplicating whole source arrays
changes productive output count or cost and cannot be treated as a complete
replacement native. Those operations require an explicit compatible invoice.

The one-hop and clipped rectangular source gates continue to constrain such
an assembly. A global construction must supply actual overlapping source
interactions, additional deliverable histories, another fully costed source
interface, or a different representation. A finite positive movement margin
for one receiver does not complete the strict BIT/complex supplier chain.
All compiler/precision/recursive costs and five foundational assumptions remain.

Dependencies: shared-facet MDS/28-16 geometry, canonical rank/local kernel,
ordinary whole-record bank expansion, and the literal cached canonical/MDS
source. Credit @CubeJerry, C's local decoder and adapted-field construction,
root's one-root pivot normalization and general all-index composition,
A's independent review, and retained native/source/compiler predecessors.
Developed with OpenAI assistance. No new complete κ.
