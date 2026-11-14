# A minimum-rank skew repair with an actual two-moment forward service

**Proved source-specific partial construction; independent review pending.
No new kappa.**

A rank-two skew change of the eight Gram modes repairs the old twenty-target
relay over `S=Z[1/30]` while preserving every diagonal fitting equation. The
literal preload uses 28 dyadic ADDs and two explicitly retired ground moment
owners, with no additional MOVE or peak record. A separate actual extension
pays two rank-nine descents to supply every new forward skew term. The old
76 D restorations, old forward component, residual helper and compatible
caller remain unconstructed.

The perturbation rank is minimal among all S-linear modal changes that repair
this exact old terminal D map. This rank statement is a theorem from the
old modulo-127 kernel, not a conclusion from the discovery search.

## 1. Pinned source and the changed preload

The predecessor is `proper-chart-relay/author/20/WORD.json.gz`, SHA256
`0edf81ca8f6a7e60e5a01d4acdcaefdb74882180b8d12c408513bc91cd625b1c`.
Its original native source has SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Credit the original source, proper-chart relay, signed-phase review and
smooth-ring obstruction. This package changes the preload; it does not
invalidate those predecessor results.

Let P be the actual 104 ports, H its 96 hosted ports, T the 20 restored
ports and S0=H minus T the 76 remaining ports. Let g_h be the unit root row
in the old omitted frame Z=[7,25,42,52,76,82,97,127]. All entries are zero
or signed halves. The old word genuinely acquires

    q = sum_(h in H) g_h^T d_h

on eight owned records at ground, before it changes any public D value.
Define the following column vectors in that exact mode order:

    u = (1, 1/2, 2, 1/2, 9/2, -3/2, 1/2, -5/2)^T,
    v = (0, 1, 0, -1, 1/2, 1/2, -1/2, 1/2)^T,
    K = u v^T - v u^T,
    Lambda = I_8 + K.

They satisfy u^T v=0, u^T u=69/2 and v^T v=3. Hence K has rank two,
K^T=-K, and det(Lambda)=1+(69/2)*3=209/2. Lambda is invertible over Q,
but is deliberately not a unit matrix over S. The source below uses actual
temporary owners, rather than claiming a nonexistent in-place factorization
into smooth-unit scalar gates.

The changed preload is

    z = Lambda q,
    r_h = -d_h + g_h z                  (h in H),
    r_m = g_m z                        (the seven old mode ports).

Every old relation g_h=sum_m beta_hm g_m still proves

    d_h = -r_h + sum_m beta_hm r_m.                        (1)

Therefore the old 20-target relay induction, original-data swaps, public
permutation, proper stops and all final charts remain valid. No q, z or
modal value is supplied for free. Invertibility of Lambda over Q also
preserves the predecessor's outside-row rank witnesses.

## 2. The literal 32-event insertion

Insert the following macro immediately before old event 432. Records
400,...,407 then hold the eight acquired q values at ground chart 3, and
record slots 408 and 409 are inactive.

1. INIT two ground owners alpha and beta.
2. Actually acquire alpha=u^T q and beta=v^T q by 14 ADDs.
3. For i=0,...,7 perform q_i += u_i beta and q_i -= v_i alpha, omitting
   zero coefficients. These are another 14 ADDs. Both moments retain their
   original acquired values throughout these updates.
4. CLEAR the two actual input-dependent moment owners.

There are two INITs, 28 ADDs and two CLEARs. Later mode births reuse the same
slots only after these lifetimes have ended. Every new coefficient is dyadic,
within the retained literal magnitude bound, and legal for ADD. No SCALE,
COPY or MOVE is introduced. The two nonzero retirements are counted.

The new core word has 2219 events:

| ADD | SCALE | MOVE | INIT | CLEAR | Peak owned |
|---:|---:|---:|---:|---:|---:|
| 1366 | 230 | 571 | 26 | 26 | 15 |

Its public and owned MOVE histograms are identical to the old 20-target
source. The total owned slot count and peak remain unchanged; the two new
lifetimes and their ordinary work do not disappear from the accounting.

## 3. Exact arithmetic repair

Let C=g_S0^T g_S0 and A0=I_8-C. Its exact source matrix is in
`ARITHMETIC.json`; equivalently, four times A0 is

    [[-34,-5,-4,-5, 1, 0, 1, 0],
     [ -5,-34,-5,-4, 0, 1, 0,-1],
     [ -4,-5,-34,-5,-1, 0,-1, 0],
     [ -5,-4,-5,-34, 0,-1, 0, 1],
     [  1, 0,-1, 0,-34,-1, 0,-1],
     [  0, 1, 0,-1,-1,-34, 1, 0],
     [  1, 0,-1, 0, 0, 1,-34, 1],
     [  0,-1, 0, 1,-1, 0, 1,-34]].

Its determinant is 24387048=2^3*3^3*7*127^2. Put
M=C(C-I_8)^(-1), a symmetric rational matrix. Applying the determinant
lemma to the rank-two change gives the exact identity

    det(I_8-(I_8+K)C)
      = det(A0) * [1+(u^T M u)(v^T M v)-(u^T M v)^2].    (2)

One way to check the sign is to write K=[u,v][v,-u]^T and reduce the
matrix determinant lemma to the resulting two-by-two determinant. It has
diagonal entries 1+u^T M v and 1-u^T M v, with opposite-sign off-diagonal
quadratic terms.

Literal source reconstruction gives

    u^T M u = 102784/2667,
    v^T M v = 3862/1143,
    u^T M v = 1/127.

Consequently

    det(I_8-Lambda C) = 3200000000 = 2^13*5^8.             (3)

The checker verifies both (2) and a separate full eight-by-eight rational
elimination. The determinant is an S-unit. The small inverse has denominator
lcm 3200000000, containing only 2 and 5.

After the restored D rows and the known remaining carrier permutation are
put in order, the complete public D map is block triangular. Its T block is
identity and its S0 block is -I_76+g_S0 Lambda g_S0^T. By the determinant
lemma this latter determinant is (3), since 76 is even. The X/Y part retains
the old invertible coupled shear, and each B output retains its independent
original b input. Thus the complete 400-input public map is invertible over
S, and over S[i]. Tensoring the scalar word with I_V proves this statement
for every positive whole-field width V.

This proves an arithmetic inverse exists. It does not give free physical
access to that inverse's operands at distinct charts.

## 4. The modal change has minimum possible rank

**Theorem 2.** For any V>=1, let Delta be an 8V-by-8V matrix over S. If

    I_(8V) - (I_(8V)+Delta)(C tensor I_V)

is invertible over S, then Delta has rank at least 2V over Q. Our scalar
K tensor I_V attains equality.

**Proof.** The literal old source has rank(A0 mod 127)=6, hence
rank(A0 tensor I_V mod 127)=6V. Every S coefficient has a defined reduction
modulo 127. The rank inequality for adding Delta(C tensor I_V) gives

    8V <= 6V + rank_(F_127)(Delta).

Thus the residue rank is at least 2V. A nonzero residue minor is also a
nonzero rational minor, so the rational rank is at least 2V. Our wedge K
has rank two, and (3) makes its repaired matrix invertible over S. QED.

This permits arbitrary operator blocks and makes no symmetry assumption
on Delta. Its scope is the fixed old source matrix and the smooth arithmetic
interface. It is not a lower bound for all source representations.

## 5. Diagonal preservation and the paid new forward terms

Skewness gives g_h K g_h^T=0 for every row g_h. Since the old roots are unit,

    g_h Lambda g_h^T = 1  for all 104 actual ports.         (4)

All old diagonal fitting equations therefore survive. The old off-diagonal
contact zeros generally do not: the independent fitting-rigidity companion
shows that no nontrivial modal matrix can preserve that entire pattern.
We explicitly supply the new terms instead of treating those contacts as
free. Put

    G = g_P g_P^T,
    Gamma = g_P K g_P^T
          = (g_P u)(g_P v)^T - (g_P v)(g_P u)^T.           (5)

Gamma is skew and has rank two. The formal forward companion of the reverse
matrix -I+G+Gamma is I-G+Gamma. Thus adding Gamma to the actual Y service
leaves exactly the old I-G forward component as the outstanding matrix debt.
This is a matrix identity and the endpoint claim below; it does not certify
a full native caller or import an old forward compiler automatically.

At the end of the core word all X values can be moved to Hub before any Y
leaves ground: the final 208 public MOVEs are independent X-to-Hub and
Y-from-ground steps. Reorder them as all X MOVEs, the following actual
service, then all Y MOVEs. The literal X rows are

    a_h=x_h for hosted h,
    a_h=x_h-y_h for the eight old coupled h.

At Hub initialize two zero owners and acquire

    beta_X = sum_(j in P) (g_j v) a_j,
    alpha_X = sum_(j in P) (g_j u) a_j.

These are real ADDs from the already arrived X records. Move both owners
from Hub to ground, with rank drop nine each. While every Y is still at
ground, perform

    Y_h += (g_h u) beta_X - (g_h v) alpha_X  for all h in P.

Then retire both actual moment owners and execute the deferred original Y
MOVEs. No public field is returned or granted a nonlocal read. The exact
endpoint becomes

    X_h = a_h,
    Y_h = y_h + sum_j Gamma_hj a_j,
    B_h = b_h-d_h+sum_(j in H)(G_hj+Gamma_hj)d_j,
    D_h = d_h for h in T; the old remaining permutation of r for h in S0.

The X/Y block is still invertible, being the old entry shear followed by an
additive Y shear. The terminal arithmetic repair therefore survives this
extension.

This service has 350 added events: 344 ADDs, two INITs, two MOVEs and two
CLEARs. The complete extended partial word has:

| Events | ADD | SCALE | MOVE | INIT | CLEAR | Peak owned |
|---:|---:|---:|---:|---:|---:|---:|
| 2569 | 1710 | 230 | 573 | 28 | 28 | 15 |

Public MOVEs remain {1:96,2:20,5:20,7:76,8:304}. Owned MOVEs become
{1:47,6:1,7:7,9:2}. All 28 retirements are genuinely dirty and recorded.

The two-moment count is also minimal for this isolated late service in the
whole-field linear model: at its entrance arbitrary current a and ground Y
are independent, and the demanded cross-map Gamma tensor I_V has rank 2V.
If the only new source-dependent information reaching ground consists of q
whole V-fields, that cross-map factors through at most qV dimensions, hence
q>=2. This argument does not exclude earlier mixed histories, other routes,
or a joint completion that reuses paid information.

## 6. Exact grids, chart phases and the movement screen

Every new scalar prefix remains dyadic. The full extended replay checks
maximum binary denominator exponent four and maximum scalar row absolute
sum 757/2. There is no new odd entrance-grid factor. These are finite source
bounds; full uniform multiplication precision and recursion are not claimed.

The core has exactly the old chart maps. The extension adds only the existing
Hub chart 127 to ground chart 3. `phase.py` authenticates the retained
Clifford generation and independent equality engines, constructs the literal
rank-nine map, verifies its exact signed action, and rejects a wrong global
phase. This is finite signed-chart evidence with inherited compiler and
uniformity foundations retained.

At t=199/200 the extra MOVE cost is exactly

    2 * 9^t = 17.8033320750990728357304434498... .

Subtracting this from the old incomplete limiting profile screen yields

    28.7046794479154571281233967223... .

`price.py` certifies directed rational intervals by integer-power comparison,
not floating extrapolation. The old finite-m correction and old caller proof
are not transferred. The new ordinary work, four additional dirty lifetimes,
precision guards, recursive service and changed residual helper all require
complete accounting before a supplier theorem.

The remaining 76 D fields still need an actual decoder. One algebraic formula
makes the missing physical access explicit. Write s_T=d_T and s_S0=r_S0,
undoing the known permutation only in notation. Then

    b = g_T^T s_T - g_S0^T s_S0,
    q = (I_8-C Lambda)^(-1) b,
    d_S0 = -s_S0+g_S0 Lambda q.                           (6)

The inverse in (6) is over S by (3); no division by 11 or 19 from Lambda's
own inverse is required. However b needs eight aggregates of values at
separate charts. Formula (6) is not physical cochart access. A competitive
completion must share preterminal history, replace paid routes or otherwise
construct those aggregates and deliveries within the complete budget.

## 7. Reproduction, discovery status and controls

`build.py` authenticates the old source, inserts the actual 32-event macro,
replays every one of the 400 arbitrary-input columns, checks legal scalars,
actual cocharts, nested MOVEs, active owner lifetimes and final charts, and
checks the new inverse and old residue defects. `algebra.py` certifies the
rank-two determinant formula, minimal-rank witness and fitting changes.
`forward.py` supplies the literal two-moment extension and replays all 400
columns again. `phase.py` and `price.py` provide the exact additional phase
and restricted movement evidence.

Controls change a captured moment coefficient, insert the right macro after
the actual preload boundary, retain the failing isotropic-quarter matrix,
and remove a real forward moment acquisition. The source or advertised map
fails in each applicable control; the phase checker also rejects a wrong
signed lift.

The coefficient vectors were discovered by reducing the determinant goal to
a positive quadratic form and solving a bounded exact representation search.
That search is not a proof of completeness or optimality. Equation (2),
the literal source replay and Theorem 2 establish the stated results without
an assumption about unsearched coefficients.

Credit @CubeJerry, predecessor native/relay authors and independent reviewers,
the programme's original smooth-ring obstruction, and substantial OpenAI
assistance. The rank-four skew specimen remains a separate fallback; it is
not added to this source's progress or invoice. No full supplier, new complete
kappa or foundational discharge is claimed.
