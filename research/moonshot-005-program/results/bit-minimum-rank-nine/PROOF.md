# Exact rank9V on the actual BIT graph and a chronological network cut

Status: proved source-bound algebra; independent review pending. This is the
actual111-port BIT native's graph, distinct from the complex native's96/104
graph. Each has its own certificate; no transfer between them is assumed.

## Precise fitting theorem

Use the111 real root lines L_i and final orthogonal facets F_i=L_i^perp from
the native gzip SHA256
51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78.
For every field k of characteristic two and every positive integer V,
consider111-by111 block matrices with V-by-V blocks satisfying

    K_ii=I_V;
    K_ij=0 whenever i!=j and L_j is not contained in F_i.

No symmetry, positivity, scalar-tensor or commuting-block hypothesis is made.
**The minimum possible rank is exactly9V.**

### Lower bound

The certificate gives nine sets of eight actual source roles. Within each set
every pair of distinct real roots is NONorthogonal. Its principal fitting
matrix is therefore I_(8V). Every used source role occurs evenly:18 roles
twice, six roles four times and two roles six times, totaling72 incidences.
These are exact rational-source facts, not finite-size extrapolations.

Take a rank-r factorization K=CR. For a frame f, C_f R_f=I_(8V), hence
P_f=R_f C_f is an idempotent of rank8V. Q_f=I_r-P_f has rank r-8V.
Even incidence gives sum_f P_f=0 in characteristic two. Nine frames then
give sum_f Q_f=I_r. Rank subadditivity yields

    r <= 9(r-8V), so r >= 9V.

This proves every stated field and volume; it does not assume r is a multiple
of V. The finite certificate supplies only the graph/parity premise.

### Attainment

Normalize the native roots g_i to unit norm. The vectors v_i=2g_i are integral,
have norm4 and even pairwise inner products. Over F2 define

    B_ij=(v_i.v_j/2) mod2,    K0=J+B.

Distinct lines have inner product0 or +/-2, so K0_ij=1 exactly on allowed
real-orthogonal contacts. The diagonal is1. Exact binary elimination gives
rank(B)=8 and rank(K0)=9; all111 rows and an explicit nonsingular9-minor
are retained. Rank stays9 over every characteristic-two extension: the minor
stays nonsingular and the same nine-row factorization persists. K0 tensor I_V
attains9V. Integer division by two precedes reduction; no 1/2 scalar is used.
Arbitrary block coding therefore cannot reduce this fitting dimension below9V.

## Chronological cut corollary

Consider a finite chronological linear network over k. Independent x_i of
dimension V start at L_i. Requested y_i end at F_i, with x_i coefficient I_V
and all other x_j coefficients zero. Other independent inputs may exist;
fix them to zero for the proof. Owned initializations are zero.

Outside a specified set E of cut transfers, every operation is linear
same-chart processing, copying, erasure, whole (chart,value) role relabeling,
or movement to a containing chart. Arbitrary block coefficients are allowed.
Cut transfer e has output information dimension w_e; a whole-field downward
MOVE has w_e=V. No free initial cross-chart encoding or unlisted
input-dependent source is granted.

**Every complete network in this interface satisfies sum_e w_e>=9V.**

Cut E in the time-unrolled network and replace each cut output by an
independent variable z_e. The output is

    y=M0 x+sum_e A_e z_e.

Setting every z_e=0 leaves only monotone chart paths. Dependence of final y_i
on initial x_j then requires L_j contained in F_i. Thus M0_ii=0, since a
nonzero real root line is outside its own orthogonal facet; forbidden
nonorthogonal offdiagonal blocks also vanish.

In the original word each actual cut output is some linear z_e=C_e x after
other inputs are zeroed. Later cuts may depend on earlier cuts: C_e denotes
their full actual input dependence, so no independence is assumed. Hence

    I-M0=sum_e A_e C_e.

The left side is a fitting, and therefore

    9V<=rank(I-M0)<=sum_e w_e.

Every actual transfer is counted once. The proof uses no disjoint-downset
assumption, and permits local coding, field reuse and chronological feedback.
This is an information-dimension bound, not a priced transport theorem. It
does not force rank8 physical routes, prove nine transfers sufficient, or
admit fragmented interfaces without their actual dimensions and cost. An
honestly funded common native can supply cut capacity; it cannot be charged
again as newly paid capacity by this corollary.

## Programme consequence and limits

The rank-nine private packet candidate uses nine rank8 downward MOVEs. Its
packet dimension is optimal for the fitting interface, even against arbitrary
block coding. Its actual map still has residual K0+I of rank108 and6470 foreign
coefficients. Fitting dimension does not establish causal encoding, decoding,
minimum paid moment or complete Q. All fixed-even-m caller, route, ordinary,
erasure, precision and compiler obligations remain separate.

The companion complex-source theorem uses REAL ORTHOGONAL frames because
its forbidden-zero convention is different. Here the frames are REAL
NONorthogonal. Substituting one witness for the other would be invalid.

Run verify.py --repo REPO --output OUT. It authenticates the native, checks
actual line/facet geometry and576 ordered frame products, reconstructs K0
and its minor, and rejects frame deletion, duplication and an orthogonal
replacement. Search completeness is unnecessary: one valid witness suffices.
Both strict suppliers and all five foundations remain. No new complete κ.

Credit: @CubeJerry programme, actual BIT native/caller authors and retained
predecessors; root's fitting, parity witness and cut proof; independent worker
review pending. Substantial OpenAI-assisted research disclosed.
