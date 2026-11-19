# Exact ground repair for a low-rank balanced native defect

**Proved within the fixed causal interface below; no new κ.**

The seventy-coordinate construction leaves 5,690 field coordinates unsynchronized.
This note gives a different completion target: a balanced causal code need not
already have every proper block equal to identity if its entire remaining defect
has sufficiently small rank modulo the nine existing canonical banks. That
quotient rank is exactly the number of additional Hub-to-ground field symbols
needed by a fixed-code ground repair. The target movement budget permits at most
202 such symbols per 5,760-coordinate bank. No balanced code meeting that rank
target is constructed here.

The same note proves that actual codes in the retained seventy-coordinate
affine construction can have maximum possible defect on every foreign block.
Those codes need at least 5,690 additional symbols and cannot be repaired within
the movement budget. This is a statement about actual members of that physical
code family, rather than an arbitrary matrix assignment on the native graph.

Sources and hashes are in `SOURCE-PINS.json`. The programme baseline is
`d8544284cbd0527cd03a0aad576a2d2c6eddcc0e` and canonical upstream is
`e54523517d0f03e58352e647c403a5af3e525a57`.

## 1. Fixed-code interface and the new integer target

Work over a finite characteristic-two field F. Let b be the field-bank width,
N=111b, and let O be the native orthogonality matrix on the 111 genuine roles.
Write K=(I+O) tensor I_b. Let H have 9b independent rows spanning row(K).
These are the real canonical records already formed at Hub and paid to ground.

Fix an actual finite balanced causal programme with the following properties:

1. Every original X bank has arrived at Hub and is restored to its original
   coordinates before any original Y leaves ground.
2. The unchanged late programme, on an arbitrary vector z of its genuine ground
   Y owners, has endpoint map Gz+Bx. The square matrix G is invertible. B is the
   complete proper-path X contribution, including retained early snapshots and
   actual late line taps. It vanishes on nonforeign blocks.
3. The paid original programme transports Hx to ground. It would ordinarily
   preload G^{-1}(y+Kx), giving y+(K+B)x at the final endpoints.

All three properties are established by the balanced causal theorem. No extra
source read, synthetic original holder, changed proper chart path or uncharged
canonical record is included in this interface.

Define E=B-(O tensor I_b), and define its **canonical quotient rank** by

    r(B) = rank([H ; I_N-B]) - rank(H)
         = rank([H ; E]) - 9b.                         (1)

The second equality holds because K belongs to row(H), so adding K to the rows
of I_N-B does not change the row span after adjoining H. In characteristic two
the minus signs may equivalently be written as plus signs.

This invariant uses all original donor columns and all receiver rows. It is not
the number of incorrect displayed coordinates, a sum of individual edge ranks,
or the rank of E before accounting for already paid canonical information.

## 2. Exact completion theorem, including nonlinear repair messages

**Theorem 1.** Fix the interface above. Keep the early and late programme and
their proper maps B and G unchanged. Permit additional one-way information from
the restored X at Hub to ground, and permit a changed ground preload on the same
genuine Y owners. Then exactly r(B) additional F symbols are necessary and
sufficient to complete every native output y_i+x_i. The lower bound also holds
for arbitrary deterministic nonlinear additional messages and nonlinear ground
preloads over the same finite alphabet.

Here “exactly” counts information symbols. The explicit linear construction
below realizes them as owned records with individually paid movement, INIT,
ordinary operations and dirty CLEAR. It does not make those operations free.

### Sufficiency and physical ordering

Choose rows L that extend a basis of row(H) to a basis of row([H;E]); L has r
rows, independent modulo row(H). There are matrices A and D with

    E = A H + D L.                                     (2)

When the actual X owners have been restored at Hub, form Lx in r newly owned
field records there. MOVE each of those records from Hub to ground, a rank-eight
descent. The original X owners are only read and remain restored at Hub.

All original Y owners are still at ground. The canonical owners Hx are also
there, before their previously charged final use and retirement. Change the
preload to

    z = G^{-1}(y+Kx+E x)
      = G^{-1}(y+Kx) + G^{-1}A(Hx) + G^{-1}D(Lx).      (3)

All terms in (3) are now available at one real chart. The same genuine Y owners
are updated in place; no target bank is replaced by a new public bank. The
inverse G^{-1} is already required by the balanced construction on arbitrary
initial Y, and the two additional fixed linear maps in (3) are ordinary
co-located ADD computations. No field multiplication oracle is assumed.

After adding the syndrome contributions, retire the r new ground records using
paid dirty CLEARs. Continue precisely the original late word. Its endpoint is

    Gz+Bx = y+(K+E+B)x = y+x.                          (4)

This identity holds on every original X and every arbitrary original Y column.
The early source-restoration word and all proper movement routes are unchanged.

### Necessity for arbitrary deterministic repair

Suppose h new F symbols are sent, by any deterministic encoder s(x), and the
ground procedure uses only y, Hx and s(x) as its X-dependent inputs. The late
map is still Gz+Bx. Exact correctness therefore forces

    z = G^{-1}(y+(I_N-B)x).                            (5)

Fix y=0 and one value of Hx. On that affine fibre, (I_N-B)x takes exactly |F|^r
values. To see this, its image on ker H has dimension

    rank([H; I_N-B])-rank(H)=r.

One elementary derivation is to choose a basis of ker H, extend it to a basis of
the whole input, and row-reduce the joint map. These |F|^r target values require
distinct new-message transcripts, while h F symbols have at most |F|^h values.
Thus h≥r. This argument does not assume linear encoding or decoding.

It does assume that B and G are fixed and that ground receives no other new
X-dependent information. Changing the later source/port code, adding informative
descents to other charts, or leaving new ground side information outside H is a
different architecture and must be priced separately.

### Binary records and arbitrary body width

If F=GF(2^w), expand every field lane into w binary whole-record lanes. For any
positive body width V, the fixed binary coefficient maps act tensor I_V. The r
field syndromes use rw actual binary records. On an H-fibre the necessary
information has rwV bits, so arbitrary nonlinear binary messages of V bits each
also require at least rw records in this interface. Field extension and body
width do not divide away the correction cost.

## 3. An explicit complete incremental invoice

Put M=111bw, C=9bw and R=rw, all in actual binary records. A direct binary
implementation of (2)–(3), in addition to the original finite balanced word,
has the following conservative invoice:

| Additional operation | Bound or exact count |
| --- | ---: |
| INIT at Hub | R |
| ADD to form the new syndromes from restored X | at most MR |
| MOVE from Hub to ground, gap eight | R |
| ADD at ground to reuse canonical records under the new decoding | at most MC |
| ADD at ground from new syndrome records | at most MR |
| Dirty CLEAR at ground | R |
| Extra simultaneous owned records | at most R |

Thus the additional ADD bound is M(C+2R). Coefficients of G^{-1}A and G^{-1}D
are fixed before execution and expanded into binary matrices. A one bit in
those matrices costs an ADD into the actual Y record from the corresponding
canonical or syndrome owner. Syndrome formation similarly uses at most M ADDs
per new binary record. The canonical owners were already paid; their lifetime
is extended only through these co-located additions before they are cleared.

This bound may count redundant canonical additions and is not optimal. It is
an explicit finite compiler for the new repair interface. For r=0, proper
support and the injectivity discussed below force E=0, so no extra operation
is needed. This special case need not pay the loose MC term.

At b=5,760 and w=30, M=19,180,800 and C=1,555,200. For r=202, R=6,060. Every
one of these new owners is additional to the seventy-coordinate theorem's
original 97,459,200 INIT/dirty-CLEAR bound and its other owned records. The
complete invoice has not been admitted through the ordinary, precision,
erasure, compiler or recursive contracts.

## 4. Exact retained movement gate

At t=199/200 write [a]=a^t. The base source profile is

    Q_0 = (4451/8)[1] + (7213/16)[2] + 24[4] + 9[8].

The repaired source uses

    Q_r = Q_0 + (r/5760)[8].                           (6)

All 5,760 field lanes and all w extension copies remain charged. The limiting
allowable source moment from the unchanged paired-caller comparison is

    B_inf = (37[127]+74[64]-74[1]
             +74 sum_(j=1..8)([1+7j]-[7j])) / 6.

Exact rational enclosures of every 200th root prove

    B_inf-Q_0 = 0.27810691512567620767639272311179888…,
    5760(B_inf-Q_0)/[8] = 202.329744960032041975945569… .

Consequently **r≤202 is necessary and sufficient for the strict limiting
movement comparison at b=5,760 within this repair interface.** It is not
sufficient for a supplier theorem. For r=202 the remaining limiting room is only
0.00045324207585427318865269183188580… . For r=203 the room is negative.

This integer is not a universal cap after replication. If the same normalized
paid atlas is used on b=5,760s field lanes, for a positive integer s, the exact
criterion is

    r < 5760s(B_inf-Q_0)/[8]
      = 202.329744960032041975945569… * s.              (6a)

Equivalently the maximum integer rank is the ceiling of that real number minus
one; use a strict comparison if an endpoint is in question. The binary view
uses R=rw real records and B=bw paid records, leaving the ratio R/B=r/b
unchanged. A genuinely binary-linear jointly coded source may use its own
binary quotient rank and the same ratio criterion; it need not have field rank
integral in a larger claimed extension field. Taking a literal direct sum of s
copies simply multiplies the canonical quotient rank by s and does not improve
the normalized repair expense. A new cross-copy code would require its own
rank and physical-realization proof.

For the exact finite comparison retain

    N0={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10},
    H0={2:1,4:25,6:1,8:410},
    P2=36 N0+444[1]+444 sum_(j=1..8)[7j],
    T2=36 H0+222[127]+444 sum_(j=1..9)[1+7j].

Here each histogram denotes its t-moment. For fixed even m≥2,

    Delta_m(r)=T_m-P_m
      = (m/2)(T2-P2) +18(m-1)(N0-H0-Q_r).             (7)

Its slope in m is 18(B_inf-Q_r). The exact interval checker checks both the last
nonpositive even m and the first positive even m, so a finite search failure is
not being substituted for the all-m claim.

| Repair symbols r | First even m with positive retained movement gap |
| ---: | ---: |
| 0 | 46 |
| 1 | 46 |
| 70 | 70 |
| 100 | 90 |
| 200 | 3,854 |
| 202 | 27,218 |
| 203 or larger | none |

The last row follows from negative slope and a negative m=2 gap, together with
monotonicity in r. The listed passing cases still require every ordinary and
recursive charge, a compatible complex supplier, and all retained foundations.

## 5. Canonical information cannot hide a large single-receiver defect

The native exact source has the following verified property: for each receiver
i, restriction of row(H) to the input columns outside N(i) is injective.
It persists under field extension and bank tensoring. Each row of the receiver
block E_i is supported only on N(i). Therefore

    row(E_i) intersect row(H) = {0},
    r(B) ≥ rank(E_i) ≥ rank(B_ij-I_b)                 (8)

for every foreign j. The first inequality follows by injecting row(E_i) into
the quotient by row(H); the second follows by restricting columns to donor j.
These are maximum bounds, not sums over overlapping receivers or edges.

Thus a repaired b=5,760 code meeting r≤202 must have every whole-receiver defect
and every foreign block defect of rank at most 202. Every individual foreign block
then has at least 5,558 left-fixed directions. Their spaces may vary, and a
large collection of individually small defects can still have too large a
global canonical quotient rank. The target is the global condition (1).

The quotient matters. As an algebraic native-incidence control, choose the
orthogonal roles0 and1 and two internal coordinates. Put a nilpotent shear on
every block of receiver0 and on the single block(1,0), leaving all other blocks
identity. Its two nonzero defect rows are O_0 in one internal input coordinate
and the coordinate at donor0. Their sum is K_0, an already paid canonical row.
Hence rank E=2 but r(B)=1. All foreign blocks stay invertible and the first
internal row remains fixed. This is a check of the repair invariant; it is not
claimed to be a balanced-network realization of those particular blocks.

## 6. The actual seventy-coordinate family contains maximally defective codes

**Theorem 2.** Retain the downstream specialization provided by the reviewed
seventy-coordinate mixed-flow theorem. Over the same GF(2^30), its affine source
solution spaces contain one actual balanced causal programme such that every
early source map and every foreign block is invertible, all seventy common
rows remain fixed, and

    rank(B_ij-I_5760)=5690

on every one of the 6,470 foreign edges. Such a code has r(B)≥5,690.

### Proof

For donor j the retained theorem has one affine space

    A_j = {F_j : T_j F_j=R_j},

where R_j repeats the first-seventy-coordinate projection at all neighboring
receivers. Its early map E_j has a nonzero determinant polynomial on A_j by the
exact quotient-image lifting lemma. For each foreign receiver i, the mixed
minor gives row-surjectivity of the system imposing a complete B_ij together
with the seventy fixed rows at every other neighbor. Consequently, for any
matrix A with first seventy rows equal to the projection, A_j contains a point
with B_ij=A. That point need not make the early map or other blocks invertible;
it is used only to show a polynomial is nonzero on this same affine space.

Since PB_ij=P throughout A_j, write

    B_ij = [[I_70, 0], [C_ij, D_ij]].

Choose any lambda in GF(2^30) other than0 and1 and prescribe
A=diag(I_70, lambda I_5690). The mixed surjectivity supplies a witness at which
det(D_ij-I_5690) is nonzero. Thus each such defect determinant is a nonzero
polynomial on A_j, as are the retained det(B_ij) and det(E_j).

The product of all these factors on A_j is nonzero and has degree at most

    b + d_j b + d_j(b-70)
       ≤5760+62*5760+62*5690
       =715660 <2^30.

Parameterize A_j by affine coordinates over the same field and apply the
finite-grid nonzero-polynomial lemma. One source choice makes every factor
nonzero. Choose such a source for each actual donor. The retained downstream
code and its invertible early/late phases are unchanged; invertible E_j keeps
the real source restoration valid. No new route, owner or movement is added.

The first seventy defect rows vanish while D_ij-I is invertible, giving the
claimed exact rank5,690. Equation(8) gives r(B)≥5,690. The extra movement is at
least

    (5690/5760)[8] = 7.821036631947954491263568207835175…,

which exceeds the entire limiting room0.278106915125… .

This does not claim that every source solution selected by the earlier theorem
has maximal defect, or that every balanced code is expensive to repair. It
proves that the earlier stated guarantees do not imply proximity to the new
low-rank target, even inside the actual physical construction family. A useful
coefficient search must impose additional correlated identities rather than
merely avoid determinant zeros.

## 7. Verification and open next questions

`check.py --repo REPO --out OUT` authenticates the pinned geometry and theorem
sources, independently recomputes the native rank/injective-restriction facts,
checks quotient rank against exact fibre cardinalities in exhaustive small
binary cases, and checks an all-input repair identity with an invertible late
map. Negative controls reject omission of the new syndrome, failure to apply
the late inverse, and replacing canonical quotient rank by rank(E). It also
produces exact rational moment enclosures and every threshold for r=0..203.

The universal proofs above establish the theorems. The finite controls do not
materialize the 5,760-coordinate global code or replace its inherited existence
proof. In particular, the script does not claim to evaluate a numerical
GF(2^30) coefficient table.

The immediate construction target is now precise: produce a genuine causal
balanced code whose canonical quotient defect rank is at most202 at b=5,760,
or satisfies the scaled strict ratio(6a), preferably with a lower defect and a
more useful finite m. A b=5,760 source with rank203 cannot be fixed by this
ground-only repair at the target exponent. Other
repair destinations and genuinely changed transport networks remain separate
possibilities.

Credit @CubeJerry, the native geometry and balanced-atlas authors, the
seventy-coordinate mixed-flow and canonical-normalization authors, and WorkerB
of this session. Substantial OpenAI assistance was used. This is mathematical
and computational evidence pending independent review, not formal-kernel or
human verification. No complete supplier, foundation discharge or new κ.
