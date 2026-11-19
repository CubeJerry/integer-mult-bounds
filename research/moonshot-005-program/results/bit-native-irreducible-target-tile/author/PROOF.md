# A paid native D4 tile for the irreducible target

## Exact result

On the admitted asymmetric bank-480 atlas, there is an explicit binary
whole-record word whose proper output at receiver 80 has, on its first
eight field coordinates,

    Y_80[0:8] + sum_(j in D12) P Bstar_(80,j) X_j.                 (1)

Here P selects coordinates 0 through 7, and Bstar is the S027 irreducible
algebraic target at b=480=60*8. The twelve genuine donors in D12 are

    0, 2, 5, 7, 38, 39, 40, 41, 42, 43, 44, 45.

Every original X is restored at Hub. The coefficient of the complete
arbitrary original Y bank is exactly identity at every output. All 106,560
original field inputs, or 532,800 binary input columns, remain in the
endpoint contract. No other source input is fixed to zero.

The exact additional local-operation invoice, on the full original-owner
routes, is 32,190 binary ADD, 340 INIT, 340 charged dirty CLEAR, and 340
additional peak binary owners. It adds no MOVE. The actual proper public
movement is 1,335,300 gap-one, 1,081,950 gap-two, and 57,600 gap-four binary
record moves. These are the entire bank-480 routes expanded by five bits,
not a price normalized by eight useful coordinates. The canonical return
bank is not part of this partial proper word.

This is a concrete source/H/D/K/F composition for one target tile. It is
**not** a complete receiver, a full 480-coordinate target, a simultaneous
all-receiver code, or a new kappa. In particular (1) omits the other fifty
foreign donors of receiver 80. Unselected output X-dependence is retained
in the exact word; only its Y baseline and the forty selected binary rows
are asserted here.

## 1. The actual two-wave interface

D12 and its dual D116 each have twelve genuine native lines and sixteen
full three-native A2 planes. All thirty-two planes are unselected in the
authenticated bank-480 phase certificate. Thus each physical flag has one
early X and one late Y field. At D12 there are sixteen early incoming and
sixteen early outgoing owners, sixteen late incoming and sixteen late
outgoing owners, and no middle closure or birth.

Receiver 80 sees exactly the right planes K370,K371,K372,K373. The actual
right-plane output quotas have fifteen early X visits and fifteen late Y
owners for this receiver. Consequently a selected D output can be placed
on a genuine owner reaching F80 by an invertible same-chart permutation.
No new flag or fabricated native owner is introduced.

Each donor j in D12 belongs to exactly four left planes H in D12. At each
of those planes it has fifteen genuine early source owners. We use two of
them for the source values below. If the literal X owner on H-to-D12
belongs to j, its value is chosen as the first one. The other source
values remain on their existing original-owner paths.

The route file SHA-256 after decompression is
`6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036`.
The layout and phase pins are recorded in RESULT.json. Every read/write
in the emitted word is checked against these actual source and terminal
labels and its chronological chart.

## 2. A Cauchy middle map with a prescribed target

Work over GF(32), represented by t^5+t^2+1. Order the sixteen left and
right planes by their literal labels. Let

    A_(r,c) = 1/(r + (16+c)),  0<=r,c<16,                       (2)

where the integers represent polynomial-basis field elements and addition
is XOR. The two node sets are disjoint and each contains sixteen distinct
elements. The Cauchy determinant formula therefore makes every square
submatrix of A invertible; the checker also checks the actual minors used.

On incoming early fields u and late fields v, the D action is

    early outputs = A u,
    late outputs  = A v + u.                                   (3)

The u in the second expression is a paid stationary copy of the actual
early incoming tuple. Both pure phase maps A are invertible. Their local
permutations are included when actual owner order differs from flag order.

Let R be the four right-plane indices visible to receiver 80, and C_j
the four left-plane indices containing donor j. Define

    S_j = [[A[R,C_j], 0], [I16[R,C_j], A[R,C_j]]].              (4)

It is an invertible 8-by-8 matrix. Let T_j=P Bstar_(80,j), an 8-by-480
matrix, and set

    F_j = S_j^(-1) T_j.                                        (5)

The source sends the first four rows of F_j X_j as its first values at
the four H, and the remaining four rows as its second values. All these
rows concern the same original X_j. They are not independent fictitious
inputs at different planes.

For clarity the target is specified without relying on a narrative name.
Order receiver 80's sixty-two native foreign neighbors. At the first use
Bstar=I+J on coordinates0..7, where J has ones at (r,r+1), r=0..6. At the
second use I+E, where E has its one at (7,0). At positions p=2..60 use
I+T_(p-1), where T_l maps coordinate 8*l+r to coordinate r, 0<=r<8.
The final neighbor has the identity. This is the row-star part of the
separately reviewed irreducible target, and suffices to identify (1).

The restriction of every T_j to the first eight input columns is I+J,
I+E or I, hence invertible. Therefore F_j has rank eight and can be part
of an invertible source map on the actual 480 original coordinates. The
word changes the first eight coordinates by F_j, retains the other
coordinates, and then permutes the eight changed values onto the chosen
real source owners. That matrix is invertible because its leading block
is S_j^(-1) times an invertible matrix. Its binary inverse is paid at Hub.

## 3. H coding and the endpoint identity

At a left H, the three native donors each provide a first value u_j and a
second value v_j. Replace the actual early H-to-D12 carrier's u_j by the
sum of the three u values, using two ADDs and leaving the other two
original holders intact. This is an invertible shear. Copy the three
second values into stationary owned fields at H before their actual X
owners depart. In the late wave add their sum to the actual late H-to-D12
Y owner, preserving its arbitrary baseline.

The selected eight D output values contain the donor-j contribution
S_j F_j X_j=T_j X_j. Summing the contributions of all twelve original
donors proves (1) algebraically. The field calculation is checked on all
480 columns for each donor, including the target's cross-bank entries.

At each of K370--373, an actual early output is swapped into an X holder
whose proper trajectory visits F80, and an actual late output is swapped
into a Y holder whose true native destination is F80. These are local
three-ADD binary swaps. Cache the four early selected values at F80.
An invertible permutation of the real Y bank at F80 places the four late
selected values at coordinates4..7. Coordinates0..3 have no proper late
contribution from this module. Add the four stationary early values into
those coordinates. This gives the ordering in (4), without an early value
being read after its X owner has departed.

## 4. Original restoration, arbitrary Y, and actual compilation

The early X transformations consist of the invertible native source maps,
the H shears, the D Cauchy map and the K swaps. Every true original X
reaches Hub on its retained path. Apply the exact inverses there in reverse
order. This restores all X labels and values before any original Y leaves
ground. Stationary H, D and F snapshots retain their earlier values.

The pure late map consists of the D Cauchy map, the K swaps and the F80
permutation. Apply its full inverse at ground to the arbitrary original Y
bank. The forward late transformations then restore every Y baseline.
All X-dependent contributions are introduced after this preload through
the paid stationary snapshots. Ground preprocessing reads only Y; it is
not an uncharged original-X input channel.

Every field matrix is expanded in the displayed five-bit polynomial
basis. Invertible binary matrices are implemented in place by XOR
elimination and three-XOR swaps. The emitted word uses only binary ADD,
INIT and CLEAR locally. There is no free field multiplication or SCALE
primitive. Each compiled matrix is replayed on its complete binary basis;
the whole emitted word is then symbolically replayed on all532800 original
binary input columns. Untouched columns stay identity by construction.

There are48 H field snapshots,16 D field snapshots and4 F snapshots.
They all coexist before the late wave, so the peak is68*5=340 new binary
owners. Each is initialized, copied, used at its real chart and charged
for a dirty CLEAR. H snapshots retire after their late injections, D
snapshots after the cross term in (3), and F snapshots after the final
additions. No owned field moves.

The exact public movement counts come from all106560 pinned field-owner
routes, expanded by five binary coordinates. The 32190 local ADD count
includes both source and Hub operations and both ground and forward late
operations. The code works at every positive body width by tensoring each
fixed binary operation with that body identity. This is a uniform finite
word statement for this tile, not a discharge of the general compiler or
complete recursive supplier obligations.

## Verification and next construction

Run:

    python3 -B build.py --repo REPOSITORY --out OUTPUT
    python3 -B controls.py --repo REPOSITORY --word OUTPUT/WORD.json.gz --out CONTROL_OUTPUT

Expected main marker is PASS_LITERAL_NATIVE_D4_TARGET_TILE. The full
word, all source matrices, actual owner choices, target supports and exact
invoice are preserved. Omission controls separately remove Hub restoration,
the arbitrary-Y ground inverse, a genuine H late injection, a selected D
cross addition and a final early correction. Each loses the corresponding
endpoint condition. These are mathematical failure controls, not additional
claims of independent review.

The next obligation is to compose additional source/D tiles without
requiring inconsistent early source bases or exceeding shared K/F capacity.
One native input cannot be assigned an independent basis separately for
every tile. A target row split also needs all its remaining donor terms.
Those are explicit global alignment obligations. Neither this word nor the
separate algebraic low-return-rank target proves that they can be met.

Credit @CubeJerry, the native geometry and balanced-atlas authors, S026
Worker B's bank480 owner atlas, S027 Worker C's irreducible target, and
S027 Worker A's paid tile construction, with substantial OpenAI assistance.
No new complete kappa or foundational discharge is claimed.
