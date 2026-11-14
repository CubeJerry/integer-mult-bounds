# One zero-restored carrier streams a paired rank factorization

**Proved universal source interface and actual native two-factor construction.
Independent review is separate. No new complete kappa.**

This extends the paid paired-relay bridge through a single evolving carrier
and one cumulative output cache bank. It shares the final adjoint cleanup
across factors. The source transmits two independent forward modes and two
independent reverse modes on one actual carrier, while paying every passage.
The mechanism supplies an exact chronological compiler primitive; it does not
complete the programme's global complex supplier.

## 1. Statement with all dimensions and actual source premises

Let K be any field and V,p,m,r positive integers. Let

    P: K^(pV) -> K^(rV), Q: K^(rV) -> K^(mV),
    L: K^(mV) -> K^(rV), with LQ=I_(rV).

Partition P into V-row blocks P_i, Q into V-column blocks Q_i, and L into
V-row blocks L_i for1<=i<=r. Then L_i Q_j=delta_ij I_V. No block commutativity
is assumed. Q is injective; P may be singular or rectangular.

Two distinct nested charts C<D have rank difference h>0. Authentic arbitrary
input banks x,b in K^(pV) remain at C. Authentic arbitrary input d in K^(mV)
remains unchanged at D. A real m-field output cache bank z at D is initialized
to zero and stays there. One real V-coordinate carrier u is initialized to
zero at C. No initially available cross-station information about x,d is
assumed for the communication-minimum statement below. All named local maps,
transposes, scalar primitives and coefficient-production costs must actually
be available; an abstract factorization does not establish that service.

There is a literal linear schedule with the endpoints

    x'=x, d'=d, z'=QP x, b'=b-P^T Q^T d, u'=0 at D,          (1)

using exactly2r+1 C/D passages of this one whole-V carrier. Every original
input survives. The output cache is a genuinely zero-born bank, not an
arbitrary original Y bank silently treated as zero. Later actual recipients
may add its contents to their original Y values on paid compatible routes.
The carrier ends at D, not its birth chart C. Its zero retirement at D is
part of the specified interface.

## 2. Inductive chronology and cleanup proof

Set Q_0=0. Before factor i, maintain the following exact boundary invariant:

    u=Q_(i-1)^T d at C,
    z=sum_(j<i) Q_j P_j x at D,
    b=b0-sum_(j<i) P_j^T Q_j^T d at C.                      (2)

The initial state satisfies (2). Perform these actual local stages:

1. At C add P_i x into u, then move this same carrier to D.
2. At D subtract Q_(i-1)^T d using the authentic still-present d bank.
   Its current value is now exactly P_i x.
3. At D add Q_i u into the cumulative output cache z.
4. At D subtract L_i z from u. By L_i Q_j=delta_ij I_V,

       L_i z = L_i sum_(j<=i) Q_j P_j x = P_i x,

   so this actual carrier is zero. Earlier output components do not
   contaminate the cleanup.
5. At D add Q_i^T d into this zero carrier, then move it back to C.
6. At C subtract P_i^T u from the actual current b bank.

This gives (2) for the next factor. In particular, the b bank is never assumed
to equal its original input after the first factor; the update is applied to
its actual accumulated current row. After r factors it has the desired b
endpoint, while the carrier holds Q_r^T d at C. Make one final actual C->D
passage and subtract Q_r^T d there. The carrier is zero at D, proving (1).

All forward/adjoint source cancellation is performed at its stated station.
No inverse stage reads departed original d, no erased carrier is restarted,
and no earlier forward cache is overwritten. All factors share the same
physical input residence interval, the same m output caches, and one owner
lifetime. The whole argument holds for noncommuting V-by-V blocks because
only the stated matrix products and the order-correct transpose identity
(QP)^T=P^T Q^T are used.

An arbitrary original y at D cannot replace the zero cache. If z initially
contains y, step4 leaves -L_i y in the carrier. This changes later adjoint
loads and B outputs. That missing premise has an explicit negative control.

## 3. Exact local price and minimum within the isolated one-carrier interface

There are r passages C->D carrying a new primal contribution, r passages
D->C carrying the acquired adjoints, and the final C->D zero-cleanup passage.
Thus the whole-record movement moment is

    (2r+1) h^t,             0<t<=1.                       (3)

Returning the final zero carrier to C would add another h^t. Initializing
one new carrier and eventually clearing it are still charged operations.
The m stationary output caches retain their own initialization, storage,
real later reads and retirement. Zero transport is not zero ownership cost.

For scalar whole-record matrices let sP,sQ,sL be the numbers of nonzero
entries in P,Q,L. The exact ADD count of the streaming macro is

    2sP + 3sQ + sL.                                        (4)

The two P terms are acquisition and B consumption. Q is used for output
accumulation, loading adjoints, and subtracting every adjoint exactly once
at the next arrival or final cleanup. L supplies local output cleanup.
No new SCALE is required by this ADD-based realization once its coefficients
are admitted. Coefficient generation, physical precision and operator-block
implementation remain separately charged obligations.

For scalar rank-r F, one may choose P as r independent actual rows of F.
Then F=QP with Q equal to the identity on those pivot rows, and L can be the
corresponding row selector. This eliminates nontrivial cleanup coefficients,
but Q itself may still have non-dyadic entries. Every concrete construction
must record them; they are not free scalar primitives. The native example
below has Q=L=I2 and all new coefficients in{0,+/-1,+/-1/2}.

### Sharp passage count for a specified isolated interface

Assume rank(QP)=rV, the two stations initially have no cross-station side
information about x,d, communication is solely this one persistent V-field
carrier, its schedule is fixed and linear, and it starts at C and ends at D.
Then any correct realization of (1), even with arbitrary independent local
dirty memory, requires at least2r+1 carrier passages.

Fix all D-side original inputs and all nuisance inputs to zero, and vary x.
By induction on chronological messages, every D-side row lies in the span
of actual received C->D rows. The final z=QP x has rankrV, so at least r
whole-V messages must arrive from C. Fixing the C-side inputs to zero and
varying d analogously requires at least r messages D->C, because the B
correction has rankrV. A single carrier starting at C and ending at D has
one more C->D passage than D->C passages. Therefore at least r+1 and r,
respectively, are needed. Equation(3) attains this bound while also cleaning
the carrier. This is a linear communication cut plus location parity, not
a general lower bound for native compilers with other channels, side
information, multiple owners, reinitialization or different endpoints.

The actual forward crossing values are Q_(i-1)^T d+P_i x; the backward
crossing values are Q_i^T d; the last crossing repeats Q_r^T d. If P has full
row rankrV, their combined row-space rank is exactly2rV, despite one carrier
holding only V coordinates at a time. This statement concerns **transported
boundary modes**. Local intermediate ADD prefixes can have a larger history
span, and are not silently omitted from any broader historical-mode theorem.
Every boundary change here has its paid chronology.

## 4. Exact native two-factor source

Use the pinned omitted-line Gram seed. Its native gzip is
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`, seed gzip
`6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc`, and full
caller JSON `d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7`.
Starting programme head is `a22f6932c7a57328f92bcf7a6f373c1433ec52f8`.

The two receiver roles are T=(0,7), and the15 hosted donors are

    J=(1,6,32,33,48,49,50,73,74,75,82,83,84,85,98).

Use the actual binary chart bases

    C=[263,135,71,32,19,13]             (dimension6),
    D=[256,128,64,32,19,10,7]           (dimension7).

Every donor line lies in C; C<D; the receivers' common seed chart C3 lies
in D; D lies in both final receiver facets. These containments are checked
against the exact native frames, with no reliance on chart-number equality.
Let P=-G[T,J], Q=L=I2. Both P rows have15 nonzero entries, each +/-1/2.
They are independent: on donors1 and32 their two-by-two minor has determinant
-1/2, up to the displayed row/column ordering. Thus this exact target block
has rank2 and cannot be supplied by one static rank-one factor at this same
interface. It is not globally superior to every other target subset.

The source keeps the two genuine original D fields at D after their actual
C3 restoration. It routes the15 genuine X fields and15 genuine hosted B
companions to C. The new carrier is actually zero-initialized at C, and the
two correction caches are actually zero-initialized at D. In the first cycle
it sends P_1 a, leaves that value in cache0, zeros itself from that cache,
returns with d0, and updates the current B bank. In the second cycle it
sends d0+P_2 a, cancels d0 using the actual source at D, stores cache7, zeros
itself from cache7, returns with d7, and applies the second B update. Its
fifth passage returns d7 to D for genuine zero cleanup and retirement.

No original X or D changes. The B fields continue to Hub with their actual
paired corrections. All the seed's reverse Gram records and forward Gram
sources are otherwise unchanged. The two original Y fields follow the
seed's unchanged forward reception and inverse-transpose decode, then move
C3->D, read their real correction cache, clear it at D, and continue to their
native facets. The original d sources are not reused after departure.

The normalized map therefore differs from the seed by

    Y_T += P a_J,    B_J -= P^T d_T.

Thirty genuine current-a offdiagonal coefficients disappear on each side.
All400 input directions and every original final chart are preserved. The
hosted R+L_HH^T identity holds on all9216 entries. The carrier's transported
boundary-mode rank is4, from two independent primal rows and d0,d7; the
coordinatewise statement is4V. Its five physical crossings are all billed.

The current-a forward debt is4962, the expanded original-coordinate debt
is5346, and reverse residual rank remains96. No new whole receiver target
is completed. No complete supplier or kappa improvement follows from this
partial word.

## 5. Actual independent-factor comparison and full caller invoice

For comparison, the builder also emits a literal independent-factor source
on exactly the same C,D banks and raw source routes. Each factor uses the
previous clean three-transfer bridge, with fresh zero forward and reverse
owners, genuine output cleanup, and reverse-owner return. Both factors share
the same authentic X/B/D residence intervals and the two output caches.
Their source coefficients, endpoints and corrections equal the stream.
Only the relay chronology differs. This is an actual compatible baseline,
not a sum of incompatible local prices.

Both words have the complete raw profile

    {1:116,2:112,3:118,4:4,5:226,8:170}, rank mass3200.

The30 selected X/B routes change8 to5+3. The two original D and two Y routes
change5 to4+1. Every extra stop is counted. The unchanged eight coupled
entry calls and16 rank8 Gram-mode calls remain in the complete owned invoice.

| Literal source | Total ops | ADD | MOVE | INIT/CLEAR each | SCALE | Peak owners | New moving lifetimes |
|---|---:|---:|---:|---:|---:|---:|---:|
| Single stream |3271|2190|775|27|252|11|1|
| Independent clean factors |3278|2190|776|30|252|12|4|

The streaming owned profile is{1:13,8:16}; the independent profile is
{1:14,8:16}. The exact source improvement is one rank1 MOVE and three owner
lifetimes, with the same true endpoint map. It changes no source cost convention.
All new and inherited scalar denominators in these actual words are1 or2.

With the same source-pinned complete fixed-m substitution as the seed,

    P_m=m(Pcaller-18N)+18N+18(m-1)Qsource,
    T_m=mTcaller-18(m-1)Hhelpers,

at t=199/200 the signed margin divided by18(m-1) has the form

    R_m=R_infinity-31.5397783670854.../(m-1).

Directed200th-root arithmetic verifies:

| Actual source | Added movement moment vs seed | R_infinity | First certified positive fixed m |
|---|---:|---:|---:|
| Single stream |5.836925502926034...|3.006593460096747...|12|
| Independent clean factors |6.836925502926034...|2.006593460096747...|17|

The shared raw-stop charge is0.836925502926034...; it was included before
construction. The source screen did not equate the five carrier passages
with the complete incremental price. Other finite candidates were screened
with the same accounting. A rank3 C5/D6 candidate had a positive complete
partial-source screen but removed only12 coefficients; it was not promoted
as the useful native construction. Search failure or a finite optimum is
not a universal theorem.

## 6. Global preflight: separated bridges cannot complete this fixed seed

The local primitive must be screened against the entire missing endpoint map.
This section deliberately reuses existing rank results. The tight-frame
identity and rank 104 already occur in `two-direction-terminal-completion`
Section 2, crediting `eight-packet-prefix/review-algebra/CORRECTION-STRUCTURE.md`.
The omitted-line Gram seed already established hosted residual rank 96.
The new use here is a precise bridge-budget consequence for this actual
coupled interface, not a claim that these source ranks were newly discovered.

### The actual required correction

The seed's actual preconditioned rows are a_h=x_h on the 96 hosted ports and
a_u=x_u-y_u on the eight coupled ports. This is an invertible change of
coordinates when the original Y bank is also retained. The seed and target
first-Y banks are, respectively,

    y+C G a,                 y+C a,

with C diagonal 1 on hosted ports and 1/2 on coupled ports. Consequently
the complete missing forward correction is exactly

    F=C(I_104-G),                                            (5)

on the actual a bank. Replacing a by original x or silently dropping C
gives a wrong source formula. `preflight.py` checks every actual Y row and
both coupled-interface negative controls against the pinned 400-column word.

Let A be the 8-by-104 omitted-frame coefficient matrix. Direct exact source
arithmetic gives AA^T=13 I_8, G=A^T A, and hence

    G^2=13G,         (I-G)^(-1)=I-G/12.

Thus F has rank 104 over the characteristic-zero source field, and rank
104V on whole-field volume V. Its determinant is

    det(F)=2^(-8)(-12)^8=6^8=1679616.

The hosted block has the separate exact small-matrix certificate

    det(I_8-A_H A_H^T)=415068771/2 != 0.

The block determinant identity det(I-A_H^T A_H)=det(I-A_H A_H^T) therefore
gives rank(I_96-G_HH)=96. This agrees with direct exact replay of the actual
reverse residual. Rank(G)=8 alone would not imply invertibility of I-G;
the tight-frame eigenvalue 13 is essential. A projection provides an
explicit negative control to that invalid inference.

### Precisely delimited movement exclusion

Fix this seed, its coupled preconditioning and all its already paid mode
calls. Suppose completion changes the hosted paired correction only by
additive rectangular bridge matrices F_j, each of rank at most r_j V on
the independent source inputs. The family supplies no other uncharged
local correction, prior acquired cancellation mode or correction side
information. Assume its actual source ledger charges at least 2 r_j new
positive-rank whole-field movements for factor j, with no movement counted
twice across factors. This tariff holds for the isolated forward/adjoint
bridges considered here before charging their cleanup, and for disjoint
groups of factors after each actual shared stream is counted as one group.
All original-route changes in this restricted family are refinements of
the retained routes; no old call is removed and no unrelated refund is
claimed.

Rank subadditivity then implies

    96V = rank((I_96-G_HH) tensor I_V)
         <= sum_j rank(F_j) <= V sum_j r_j.

Therefore sum_j r_j>=96. Every positive integer rank h obeys h^t>=1, so
the new paired movement moment alone is at least 192. Raw route refinements
cannot offset this charge for 0<t<=1, because replacing a rank a+b by
successive ranks a,b costs a^t+b^t>=(a+b)^t. The complete retained seed has
limiting room below 9 at t=199/200, and finite-m room is smaller. This
declared additive separated-bridge architecture cannot complete the seed.

The 104 forward rank does not silently give 208 paired transfers: the eight
coupled ports have no hosted B/D companions, so such a stronger paired
tariff would require an additional interface theorem. Hosted rank 96 and
the 192 floor already suffice. Likewise, sharing source histories or
previous transmissions can invalidate the assumed disjoint factor tariff;
they must be analyzed from their actual chronology rather than charged
twice by this proof.

Even the optimistic bridge budget permits total paired rank at most 4
with two transfers per rank, or at most 3 for one clean 2r+1 stream,
before any raw stops. The actual two-factor source still has reverse
residual rank 96. Removing 30 coefficients has not removed this global
rank obstacle. Further small rectangles cannot be promoted to a credible
wholesale completion by summing favorable local margins.

This is not a lower bound for all complex suppliers. Changing original
raw-route encoders, replacing or reusing already paid Gram histories,
creating genuine cocharted correction channels, or changing the source
interface lies outside the restricted family. A bridge can still be a
useful final correction after such a mechanism reduces the actual missing
rank sufficiently. That structural reduction is the next construction
obligation; a nested 38-coefficient patch has not been built or claimed.

## 7. Evidence, scope and next step

Author evidence includes exact400-column replay, all original X/D restorations,
the actual current B prefix invariant, every true carrier primal and adjoint
row, actual zero cleanup at D, all endpoint charts, complete owner lifetimes,
and all9216 paired coefficients. The transported-mode rank is separately
computed from real MOVE values. Introduced chart maps have exact signed and
global-phase lowering, using the retained credited engines and a wrong-phase
control. These engines are reused reproduction, not independent-agent review.

Controls reject missing previous-adjoint subtraction, wrong B consumption,
missing cumulative-output cleanup, omitted final zero cleanup and a false
retirement at C. General exact controls cover60 cases over Q and GF(2,3,5,7),
including singular P and noncommuting blocks, and reject a dirty output cache
or a cleanup row that does not annihilate preceding modes. They support the
universal induction without replacing it.

The next constructive question is whether actual original-route encoders or
already paid source histories can remove most of the full-rank correction
before this bridge is used. The present theorem shares one real C/D bridge.
It does not grant free passage between unrelated acquisition charts or
infer that a factorization can be acquired at another source location.
Any such global composition requires its own actual source word and bill.

All five foundations remain: native_all_columns, owned_erasure, compiler,
precision_tape and analytic_recovery. The moving carrier retires zero, but
the genuine forward caches and other seed owners still use the retained
owned-erasure contract. Uniform strict complex/BIT suppliers, ordinary and
precision admission, and the complete global target remain open.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the native
source and paired-code authors, the omitted-line Gram seed, the paid paired-
relay predecessor, and the retained replay, complete-caller interval and exact
signed-phase engine authors. Linear rank factorization, transpose composition,
and communication cut arguments are classical; this package's result is the
actual cumulative-output chronology, its source contracts and its fully paid
native realization. Apache-2.0. No claim of general literature priority.
