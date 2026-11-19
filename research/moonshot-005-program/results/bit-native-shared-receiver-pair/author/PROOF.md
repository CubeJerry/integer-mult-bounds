# A shared two-receiver D4 tile using true late source taps

**Proved local construction and proved local cut obstruction. No complete
supplier, full receiver endpoint or new κ.**

This package changes the source interface of the preceding D12 tile.
Four early source parities are completed to a reversible original-X chart;
four late parities are captured at each real native line before that chart
change, then injected through genuine late Y visits. The late parities may
be dependent on the early parities. They are not incorrectly promoted to
eight independent original-X coordinates.

## 1. Exact stacked-image criterion and the 8+8 obstruction

For fixed local matrices S_a,S_b mapping the same m source messages to two
receiver targets, a common source matrix F satisfies

    S_a F=T_a,  S_b F=T_b

if and only if every column of [T_a;T_b] lies in the image of [S_a;S_b].
Equivalently, every row relation annihilating [S_a;S_b] annihilates
[T_a;T_b]. This follows column by column from linear solvability, with all
original source columns retained. If F is also required to have row rank
m, that is a separate condition; solvability alone does not imply it.

At native D12, every one of its twelve donors belongs to four left H
planes. The pinned b=480 schedule supplies one early and one late field
slot per H-to-D12 flag. Thus information from one donor into this D chart
passes through at most eight field symbols, including both waves and all
stationary information retained at D. Any pair of targets produced using
only this donor-to-D12 interface must have stacked rank at most eight.
This bound permits arbitrary local maps and any amount of computation or
storage after the eight source messages arrive.

Take receivers 80 and 1 in D12's dual D116. Donor 5 belongs to D12 and is
the third foreign neighbor of receiver 80. In the S027 irreducible target,

    P_8 B*_(80,5) X_5 = (X_5[0:8] + X_5[8:16]),
    P_8 B*_(1,5) X_5 = X_5[0:8].

Their stacked 16-by-480 matrix has rank sixteen over every field. Hence
no choice of source or D coefficients realizes these two full eight-row
targets through the D12-only interface. This is not merely a failed
Cauchy minor. The same cardinality argument excludes deterministic
nonlinear encoders over finite alphabets: 16 independent field symbols
cannot be recovered from eight. Field extension and tensor repetition do
not remove the factor-two deficit.

The scope is essential. A full construction may send additional
contributions through other D charts, choose other distributed coordinate
decompositions, or change the physical interface. This theorem does not
exclude those repairs or the irreducible target itself.

## 2. A general four-early plus four-late local constructor

Use the exact b=480 routes and D12. Its sixteen left and sixteen right
planes are full unselected planes, hence have one actual early and one
actual late owner per flag. All twelve donors and all twelve dual
receivers are native. Let a and b be any two distinct native receivers in
D116. For each donor j in D12 prescribe matrices T_(a,j),T_(b,j) with four
rows and 480 columns over GF(32), with T_(a,j) of row rank four. No rank or
independence assumption is imposed on T_(b,j) or on their stacked matrix.

There is a literal paid local word producing, in four designated rows of
each receiver,

    Y'_a[0:4]=Y_a[0:4]+sum_(j in D12) T_(a,j) X_j,
    Y'_b[0:4]=Y_b[0:4]+sum_(j in D12) T_(b,j) X_j,                (1)

while restoring every original X, preserving the coefficient of every
original Y as identity, and retaining exactly the pinned public MOVEs.
Other X-dependent outputs are unprescribed and remain part of the actual
word. The printed instance uses a=80,b=1 and the corresponding first four
rows of B*; its binary invoice is exact below.

Let A be the Cauchy16 matrix

    A_rc = 1 / (r XOR (16+c)),  0<=r,c<16,

over GF(32), modulus t^5+t^2+1. Its row and column labels are disjoint, so
every square submatrix is nonsingular. Index columns by the sixteen H
planes and rows by the sixteen right K planes. Let C_j be the four H
indices containing donor j, and R_a,R_b the four K indices containing the
respective receivers. Define

    U_j = A[R_a,C_j]^(-1) T_(a,j),
    V_j = A[R_b,C_j]^(-1) T_(b,j).                              (2)

The four independent rows of U_j can be completed to a basis of the full
original-X bank and placed on four actual X owners, one departing into
each H in C_j. At H the three contributions are summed by an invertible
shear onto the actual H-to-D12 early owner. Applying A at D produces the
four desired early packets for a. Each is carried by an actual X owner
through its K to F_a and captured in one stationary F_a cache.

Before the original-X source chart changes, capture the four rows of V_j
in stationary owned registers at the real native line j. The actual late
line schedule supplies fifteen Y visits for each j-to-H branch. Inject
the appropriate cache into one of these true visits and dirty-clear it.
Choose the actual H-to-D12 Y carrier as this holder whenever its native
line is j. At H, the three chosen native contributions are summed onto
that carrier by another invertible shear. Applying A at D again produces
the four desired late packets for b. They are routed by actual K and F_b
permutations into b's four target coordinates.

No source parity has been obtained from a later chart and assigned
retroactively to a native line. The chronological source-interface change
is what permits dependent U_j and V_j. The four early source rows still
require the stated rank-four hypothesis.

## 3. Shared owners, unavoidable side outputs and both baselines

The concrete receivers 80 and 1 share right plane K370. The early value
for 80 and late value for 1 use different actual owners at their different
times, so the two permutations do not conflict. The construction shares
all sixteen left H planes, the actual D12 chart and the full set of twelve
source banks. It is not a juxtaposition of disjoint one-receiver tiles.

The unused native late inputs remain real original Y owners carrying
additional X dependence after the H summation. These side outputs are
not erased or silently set to zero. There are at most 48 original Y fields
with late X dependence: exactly 48 native injections occur, every H
summation destination is one of those 48 fields, and the D map acts on
sixteen such fields. Later K/F permutations preserve this upper bound.
Thus at least 480-48 fields at F_a have zero late X dependence. A paid
permutation chooses four of them as a's designated output coordinates,
before the four early F_a caches are added. In the printed word this
choice uses a conservative bit-support calculation and the full symbolic
replay verifies the resulting zero dependence exactly.

Let G be the complete invertible product of pure-Y late operations,
including H shears, D Cauchy mixing, K/F permutations and this isolation
permutation. Apply its literal reverse binary word G^(-1) at Ground before
the late wave. Every Y response is then G G^(-1)Y=Y. The native cache
injections add only X-dependent terms and produce (1). Likewise, the
complete early original-X word is inverted at Hub. All source chart
changes, native captures, destination captures, inverses and dirty clears
are paid. A gate-by-gate owner-location check verifies the chronology

    X_NATIVE -> X_H -> X_D -> X_K -> X_F -> Hub restoration
      -> Ground preload -> Y_LINE -> Y_H -> Y_D -> Y_K -> Y_F.

The general all-input claim follows by these linear identities. Direct
replication proves the same claim for every positive internal body width;
costs and source/cut ranks scale with that width.

## 4. The explicit irreducible-target instance and invoice

The early receiver80 target is the first four rows of its actual S027
irreducible-target blocks. The late receiver1 target is the first four rows
of identity for each D12 donor; none of these donors is the altered column
star center10. The [T_(80,j);T_(1,j)] stacked ranks are only four for donor2,
five for donor0, and eight for the other ten donors. A source chart that
mistakenly demanded eight independent original-X rows would reject or
misrepresent the first two cases. The true late line taps permit them.

| Item | Exact binary count |
|---|---:|
| ADD, including both inverses | 23,754 |
| INIT | 260 |
| Dirty CLEAR | 260 |
| Peak additional owners | 260 |
| Public owners | 532,800 |
| Peak total owners | 533,060 |
| Proper MOVE at gap1 | 1,335,300 |
| Proper MOVE at gap2 | 1,081,950 |
| Proper MOVE at gap4 | 57,600 |
| Additional MOVE | 0 |

The additional owners are 48 stationary native field caches and four
stationary F80 field caches, each five bits. They coexist before the late
wave. There are no H or D caches in this new pair tile. This is an actual
invoice for the printed target, not a universal cost claim for arbitrary
dense prescribed target matrices in the general lemma.

Exactly 52 final field coordinates have nonzero X dependence. Therefore
the actual partial word satisfies rank(I+B_actual)>=53,280-52=53,228.
It is far outside the target's return allowance, and most receiver/donor
contributions remain missing. No canonical return is included in the
invoice. The package resolves a shared-source causal construction issue;
it does not solve the global fitting or admission problem.

## 5. Evidence, provenance and next obligation

Run `python3 -B build.py --repo REPO --out OUT`. Expected status is
`PASS_LITERAL_SHARED_D12_TWO_RECEIVER_TILE`, with both receiver target
checks and both global baseline checks true. The exact word decompressed
SHA-256 is
`2b5f5dd5cefc36523787191b359d04d00a38cfa3ef025044c78e32314d86f794`;
the matrices pin is
`a6b6a8780f8680c3032987c0c0096bbff2477462a2a160f1badb30f20d210971`.
The native layout, routes and phase certificate pins are in
`output/RESULT.json` and agree with the prior paid tiles. The exact replay
uses all 532,800 original binary input columns, with untouched columns
represented by their basis identity. A finite literal linear word plus
exact basis evaluation proves the stated identity for all inputs.

Run `python3 -B gates.py --repo REPO --out OUT` for the exact eight-channel
cut witness and the four/five/eight stacked-rank checks. Expected status:
`PASS_SOURCE_CUT_AND_DEPENDENT_LATE_INTERFACE_GATES`. Its controls remove
one demand, repeat the same flat demand, or retain only four rows per
receiver; each has rank eight, so the rank-sixteen obstruction is not
being applied outside its stated scope.

Run `python3 -B controls.py --repo REPO --word OUT/WORD.json.gz --matrices
OUT/MATRICES.json.gz --out CONTROLS` for seven negative controls. They
remove the Hub inverse, Ground inverse, one native late capture, one early
source chart, or one late H summation. They also move a native capture
after its source chart change (which corrupts the late target) and move
the late D operation into the early phase (which violates owner location).
Expected status: `PASS_SEVEN_SHARED_PAIR_NEGATIVE_CONTROLS`.

The earlier S023 one-receiver gauge theorem remains prior art. The new
property here is compatible source processing for two genuine receivers
sharing H/D/K geometry, including a singular stacked-demand case handled
by actual late source taps. This is still only one D chart. Completing the
first four target rows at both receivers requires the other native donors;
achieving the target return rank requires a global completion in which
all prescribed 480-row block identities and unintended outputs are
controlled jointly.

Credit: @CubeJerry persistent programme, the authenticated b480 atlas,
S027 irreducible-target and previous tile authors, and their cited
predecessors. Substantial OpenAI assistance in S027. Independent reviews
are separate evidence maintained by the orchestrator, not repetitions of
the author checker.
