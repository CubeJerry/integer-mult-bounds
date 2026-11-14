# A paid paired relay echo with an actual native compiler rectangle

**Universal linear-algebra interface, source-specific physical construction, and
exact partial-source invoice. Independent review is separate. No new kappa.**

The elementary commutator identity is classical. This package does not claim
novelty for it. The contribution to this programme is its complete paired,
rectangular source interface; exact dirty-value and terminal-location contract;
actual use of two already acquired reverse Gram owners as temporary relays;
and a source-pinned native word with all duties, chronology, endpoints and
costs retained. It supplies a usable local primitive beyond invertible-bank
encoding, not a complete global compiler.

## 1. Exact paired commutator, including arbitrary dirty relay inputs

Let K be any field, V,p,m,k positive integers, and let

    x,b in K^(pV), y,d in K^(mV), r,s in K^(kV)

be arbitrary values. They may be independent; an identity valid for independent
values also permits the physically supplied correlations in Section 5. Let

    P: K^(pV) -> K^(kV),  Q: K^(kV) -> K^(mV)

be arbitrary linear maps. Neither need be square, injective, surjective or
commuting with the other's operator blocks. All transposes are the full
matrix transpose in the chosen field-coordinate bases. Define actual shears

    A_P: r <- r+P x,       b <- b-P^T s;
    B_Q: y <- y+Q r,       s <- s-Q^T d.

Every unlisted bank remains unchanged. In chronological order execute

    A_P, B_Q, A_P^(-1), B_Q^(-1).                         (1)

The exact final state is

    x'=x, d'=d, r'=r, s'=s,
    y'=y+QP x, b'=b-(QP)^T d.                            (2)

**Proof.** After the first two stages,

    r1=r+Px, s1=s-Q^T d,
    y1=y+Q r+QP x, b1=b-P^T s.

The inverse A stage subtracts Px from r1 and adds P^T s1 to b1. Thus r2=r
and b2=b-P^T Q^T d. The inverse B stage subtracts Qr2 from y1 and adds Q^T d
to s1, giving (2). The order of the operator product is retained exactly;
(QP)^T=P^T Q^T is used, never PQ=QP. No unknown dirty input is set to zero.
No auxiliary value is erased. All maps and their inverses are shears, so no
invertibility requirement is imposed on P or Q. This proves the statement for
every field, dimension and input. Finite checks in ALGEBRA.json are controls,
not a substitute for this proof.

For scalar whole-record operations take P=P0 tensor I_V and Q=Q0 tensor I_V.
Then the same literal scalar source applies at every V. The broader operator
statement does not automatically supply a physical implementation or tariff
for arbitrary V-by-V blocks or their transposes.

## 2. Actual chart contract and complete local cost

Suppose C and D are distinct nested charts with rank difference h>0. At C,
the authentic x,b banks remain available throughout both A stages. At D, the
authentic y,d banks remain available throughout both B stages. The r,s banks
start at C. The actual chronology is

    A at C; move r,s C->D; B at D; move r,s D->C;
    A inverse at C; move r,s C->D; B inverse at D.

Every named read is cocharted. The values r,s are restored, but their actual
final chart is D. This **open-route interface** uses exactly 6k whole-record
rank-h transfers: two banks times three crossings. If the caller additionally
requires both banks back at their original chart C, one final D->C passage
of both banks is necessary in this implementation, for 8k transfers total.
Restored values do not imply restored location.

If P0,Q0 use sP,sQ nonzero scalar entries, (1) uses 4(sP+sQ) ADDs. Any nontrivial
coefficient manufacture, precision/storage service, or implementation of a
block operator remains separately charged. Borrowing actual existing owners
creates no new owner by itself, but their old duties, routes, ownership,
lifetimes and final reads must still be satisfied. Additional delivery caches
have their own initialization, storage, reads and retirement.

A fixed expected decoder rank is not a source for P or Q. The source must
really make the original or current x values available at C and original d
values available at D. It must retain them until their inverse-stage reads.
Changing their state between the visits without the appropriate current-row
identity invalidates the macro.

### Minimum stage count within this declared echo grammar

Allow any finite sequence of A_R and B_S stages with arbitrary maps R,S of
the same shapes. Only A stages may read x or change r,b; only B stages may
read d or change y,s. Both relay banks are available at each stage's chart,
and all relay input values must be restored for every x,d,r,s.

Then a nonzero paired source action needs at least two nonzero A stages and
two nonzero B stages after merging consecutive stages of the same family.
Indeed r_out=r+(sum R)x and s_out=s-(sum S)^T d. Restoration requires each
sum to vanish. If only one A stage occurs its R is zero, and if only one B
stage occurs its S is zero; either makes the cross action trivial. Consecutive
A stages merge by addition, as do consecutive B stages. Therefore a nontrivial
restored macro needs at least four alternating stages. The four stages in
(1) attain the minimum when QP != 0. In the two-station co-moving-bank
interface this entails at least three interstation passages per relay bank.

This is not a lower bound for arbitrary physical circuits, borrowed originals,
independently routed banks, endpoint changes, or other dirty-memory grammars.
It is precisely the grammar just stated.

## 3. Separate cheaper interfaces when zero initialization is available

The dirty-compatible echo must not be advertised as the cheapest way to use
fresh zero owners. Initialize a new r=0 at C and new s=0 at D. At C acquire
r=Px and send it to D. At D do y+=Qr and acquire s=Q^T d, then send s to C.
At C do b-=P^T s. This realizes (2) on x,b,y,d with only 2k transfers and
2(sP+sQ) ADDs, but r=Px at D and s=Q^T d at C remain dirty. Their retirement
uses the retained owned-erasure service. Their source-dependence and the
preservation of x,d show logical public information is retained; this is not
a physical erasure theorem.

Alternatively return r to C and subtract Px, and return s to D and subtract
Q^T d. This **clean roundtrip interface** uses 4k transfers and 3(sP+sQ) ADDs.
Both owners are now zero at their respective birth charts and can be retired
with their actual zero values recorded. All moves and CLEAR operations remain
charged. This does not discharge the programme's owned_erasure foundation:
other source owners and delivery caches still use the inherited contract.

If fresh zero r,s are both initialized at C, the original four-stage echo also
works, with 6k transfers and zero values at D. It is a valid but dominated
control for this particular interface. It is retained to prevent comparing a
dirty-compatible theorem against an unpriced zero initialization premise.

### Zero-born output caches reduce cleanup to three transfers

There is a sharper clean interface when the forward destination is a genuinely
zero-born stationary output bank z at D, and Q has full column rank. After the
two-transfer construction, z=QPx and r=Px. Choose a left inverse L with LQ=I.
At D execute r<-r-Lz, so r becomes zero using the actual retained output.
Return s from C to D and subtract Q^T d, so s also becomes zero. This uses
3k transfers, leaves both scratch owners zero at D, and preserves z=QP x.
The forward owner is not returned to its birth chart C; its actual retirement
at D is part of this interface. Returning it to C would restore the four-
transfer bill. A rank factorization always permits full-column-rank Q, but
its exact coefficient/precision cost and actual local output availability
must still be supplied.

The extra ordinary cleanup is nnz(L)+nnz(Q), so the scalar ADD count is
2sP+3sQ+nnz(L). The native instance uses Q0=-1 and one actual cache to perform
r+=z0. This reduces one new whole-record rank1 MOVE relative to the clean
roundtrip source. It is invalid with arbitrary original y in place of z:
then L(y+QPx) contains Ly and the proposed cleanup leaves -Ly. An explicit
dirty-output counterexample accompanies the finite controls.

### Exact two-way communication minimum in the isolated bridge interface

For completeness, suppose the two stations have free local linear arithmetic
and fixed linear communication schedules. Initially x,b are at C and y,d at
D, along with any independent local dirty memory. No pre-existing cross-station
side information about x,d is granted. A correct implementation of

    y'=y+F x, b'=b-F^T d, x'=x, d'=d

must transmit at least rank(F) scalar dimensions in each direction. To prove
the C->D assertion, fix all D-side initial inputs and all other nuisance inputs
to zero and vary x. Every current D-side row then lies in the span of actual
C->D message rows previously received, by induction on the chronology. Since
the final y block is Fx, the total incoming dimension is at least rank(F).
Fixing the C-side initial inputs to zero and varying d proves the transpose
bound in the other direction. Interaction and arbitrary dirty memory do not
break these inductions. The two-transfer rank-factorization construction
attains the sum2 rank(F), subject to its explicit fresh-zero/retirement
contract. For F=F0 tensor I_V and r=rank(F0), at least r whole-V messages are
needed in each direction, and a rank factorization attains2r transfers.

This is the usual linear communication cut argument applied to the paired
source interface, not a new general lower-bound technique. Native pre-existing
Gram modes or other cross-station side information require their actual
quotient cut; this bound is not applied blindly to the borrowed-owner example.
The local optimality says nothing about sharing acquisition or communications
between different chart pairs.

## 4. Native source and exact rectangle

The predecessor is the admitted omitted-line Gram seed, whose complete
400-input normalized map is

    X=a, Y=y+Cw G a, B=b-G_HH d, D=d.

H is the set of96 hosted ports, Cw is1 on hosted receivers and1/2 on coupled
receivers, and all eight coupled a entries retain their original precondition.
The seed's full proofs and exact remaining compiler slot are in the programme's
`results/complex-omitted-line-gram`. We preserve its current map and every
remaining duty; no old parity-layer gain is added.

Exact source pins:

- Native source gzip: `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
- Seed gzip: `6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc`.
- Complete caller: `d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7`.
- Starting programme SHA: `a22f6932c7a57328f92bcf7a6f373c1433ec52f8`.

Use the hosted donor and receiver roles

    J=(32,48,85,98), T=(0,7,87,92),
    P=(1/2,-1/2,1/2,1/2), Q=(-1,1,-1,1)^T.

Directly from the native real root rows, QP=-G[T,J]. Every entry is nonzero.
The actual binary chart bases are

    C=[426,74,25,7]       (dimension4),
    D=[384,74,42,25,7]    (dimension5).

Every donor source line lies in C, and C is a strict subspace of D. The
receiver class chart C3=[42,25,7] lies strictly in D, and D lies strictly in
each receiver's native facet. Thus the direct source can acquire P at C,
interact with original D receivers at D, and later deliver the correction
through each actual C3->D->facet receiver chain. These are exact source
containments, not inferred from algebraic rank.

The optional finite search found this rectangle within its declared C4/D5
class family. The proof and builder require only this explicit instance. No
search maximum is promoted to a universal compiler or geometry obstruction.

## 5. Actual reuse of two dirty reverse Gram owners

The seed has already assembled eight real reverse records at omitted-root
lines before its X/B slot. Their values are

    R_l = sum_(h in H) g_l(h) d_h.

Choose the real R0 and R1 owners, whose initial mode lines are generated by7
and25. Both lines lie in C. These are generally nonzero, unknown combinations
of independent original d inputs; they are not fresh zero helpers. They will
still be consumed by the seed's original reverse procedure after this macro.

Retain original D_h for h in T at D after their genuine C3 restoration, instead
of sending them immediately to their final facets. Route the four original X
and their four genuine B companions to C. No fake companion is introduced at
a coupled port. All other X/B fields may complete their original direct route.

Move R0,R1 from their actual lines to C, use them as the r,s banks in (1), and
create one stationary correction cache at D for each h in T as its y bank.
Each cache starts at zero and ends at exactly

    cache_h = -sum_(j in J) G_hj a_j.

The full echo cancels every dirty reverse-Gram contribution to these caches
and to the changed B outputs. It leaves R0,R1 at D with precisely their
original Gram values. Their original later rank8 ascents are replaced by
D->Hub rank4 calls. At Hub their old reverse reads and original retirements
are unchanged. Thus the complete route for each borrowed owner is

    line1 -> C4 -> D5 -> C4 -> D5 -> Hub9,
    ranks 3,1,1,1,4.

The original source used one rank8 line-to-Hub call. Both old duties are
preserved; a funded leg is counted once, and the two downward rank1 turns
are explicit. The owners do not return to their birth lines, and no such
claim is made. Their actual caller requires them at Hub, which they reach.

The selected original D fields then continue D->facet with unchanged values.
The original X/B donors continue C->Hub; all X retain their authentic a.
After the unchanged forward Gram reception and inverse-transpose Y decoder,
each selected Y makes C3->D, reads its genuine cache, clears it at D, and
continues D->facet. This timing avoids any requirement that future forward
Gram modes exist before the X donors reach Hub.

The resulting full partial map differs from the seed only by

    Y_T += QP a_J,       B_J -= (QP)^T d_T.

Sixteen real offdiagonal coefficients disappear on each side. All400 original
input directions remain, every original D is preserved, and the hosted
R+L_HH^T relation remains exactly zero. No entire new target row is completed.
The current-a forward debt is4992-16=4976; the expanded original-coordinate
forward debt is5360; the reverse residual rank remains96. These are honest
partial-source diagnostics, not an improved complete supplier.

## 6. Complete movement and ordinary invoices

The common raw profile of all five literal variants is

    {1:112, 2:120, 3:104, 5:200, 8:192}, rank mass3200.

The eight selected X/B paths change8 to3+5. The four selected D and four Y
paths change5 to2+3. Every new receiver stop is included.

| Actual variant | Complete owned profile | Total ops | ADD | MOVE | INIT/CLEAR each | Peak owners |
|---|---|---:|---:|---:|---:|---:|
| Borrowed dirty Gram echo | {1:14,3:2,4:2,8:14} |3224|2156|760|28|12|
| Fresh zero roundtrip | {1:12,8:16} |3216|2148|756|30|14|
| Fresh zero with actual output cleanup | {1:11,8:16} |3212|2145|755|30|14|
| Fresh zero, inherited dirty erasure | {1:10,8:16} |3206|2140|754|30|14|
| Fresh zero four-stage echo control | {1:14,8:16} |3226|2156|758|30|14|

All variants retain252 SCALE operations; every new scalar is dyadic. The four
stationary correction caches remain real owner lifetimes even when their
transport is zero. Their storage, ADDs and CLEARs are counted. The dirty
variant adds no relay lifetime because its two owners already exist.

Use the seed's exact fixed-m substitution with the same full caller profiles:

    P_m=m(Pcaller-18N)+18N+18(m-1)Qsource,
    T_m=mTcaller-18(m-1)Hhelpers.

At t=199/200, the actual signed movement margin divided by18(m-1) is

    R_m = R_infinity - 31.5397783670854.../(m-1).

Directed200th-root bounds in each PRICE.json give:

| Variant | New-minus-seed movement moment | R_infinity | First certified positive fixed m |
|---|---:|---:|---:|
| Borrowed dirty Gram echo |4.421039538464972...|4.422479424557809...|9|
| Fresh zero roundtrip |4.343674090618734...|4.499844872404047...|9|
| Fresh zero with actual output cleanup |3.343674090618734...|5.499844872404047...|7|
| Fresh zero, retained dirty erasure |2.343674090618734...|6.499844872404047...|6|
| Fresh zero echo control |6.343674090618734...|2.499844872404047...|14|

These positive values price the actual partial source, including the previously
paid seed, complete caller terms and every new route. They do not price a
completed global compiler. The dirty-compatible mechanism is not the cheapest
choice when fresh zero owners and inherited erasure are permitted. Two fresh
zero roundtrips, or repeated rectangles on new routes, may exhaust the room;
no unconstructed composition is credited.

## 7. Verification, negative controls and limitations

The exact rational author replay checks all400 independent input columns,
every public endpoint chart, all genuine donor restorations, the actual
post-echo borrowed-owner rows, all9216 paired coefficients and every ownership
lifetime. It checks zero states and birth-chart restoration only for variants
that actually provide them. In particular, merely deleting an inverse stage
can leave public endpoints unchanged while destroying a claimed zero owner;
the intermediate owner-state check rejects that false claim.

Controls reject omitted source feedback, wrong paired signs, omitted relay
restoration, and premature departure of an original D source. The general
algebra checker separately covers singular/rectangular maps, noncommuting
blocks, arbitrary dirty independent inputs and too-short echo words. Exact
introduced MOVE maps are lowered and signed/global phases checked with the
credited retained engines, including a wrong-phase control. These reused
engines provide reproduction, not independent-agent mathematical review.

This mechanism does not discharge native_all_columns, owned_erasure, compiler,
precision_tape or analytic_recovery. It supplies no new complete kappa. The
actual finite construction, its coordinatewise all-V algebra and its movement
invoice remain distinct from uniform physical scalar/source admission.

## Open next questions

Can a coherent collection of such actual rectangular bridges share acquisition,
receiver storage or paid reverse owners enough to complete a substantial
residual block inside the whole-source budget? The next proof must address
joint source chronology and owner reuse before repeating local gains. A useful
alternative is a larger low-rank rectangular block at one real pair of charts,
with a factorization whose complete source and adjoint reads are both available.
No algebraic factorization makes those inputs cocharted for free.

## Attribution and prior mathematics

This is @CubeJerry's persistent programme, with substantial OpenAI assistance.
Credit the native source authors, the omitted-line Gram seed and paired
primal/dual source predecessors, and the retained replay, full-caller moment,
and signed-Pauli/global-phase engine authors. The bare identity is an elementary
matrix/Steinberg commutator relation; see Charles Weibel, *The K-book*, Chapter
III, sections1 and5, available from the author's
[book page](https://sites.math.rutgers.edu/~weibel/Kbook.html), and John Milnor,
*Introduction to Algebraic K-Theory*, section5,
[publisher archive](https://www.jstor.org/stable/j.ctt1b9x0xv.8).
The programme-specific application and its physical price are the result here.
