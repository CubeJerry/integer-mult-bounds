# A weighted formation and delivery obstruction from the actual current cuts

**Proved scoped continuation obstruction; independent mathematical review is
still required.** At the exact 9b remaining-receiver descent floor, none of
the current scalar, two-copy F4, or three-copy F8 sources can fit its residual
movement budget using at most one exterior descent to a chart of rank at most
four. Arbitrary recoding, arbitrary record width, joint bank operations, paid
owned ascents, and unrestricted exterior descents to charts of rank at least
five are included. No unrestricted formation price or new supplier is claimed.

For the two-copy source the required extra movement is at least
43.75132983573329 per copy, exceeding its 42.94339242695855 room by more than
0.80793740877474. The three-copy source has a slightly weaker bound but is
still excluded by more than 0.48405408893826 per copy. Thus a continuation that
meets the current budget must use either more than 9b remaining-downset
descents or at least two exterior descents to rank at most four.

## 1. Actual source, information, and cost conventions

Let

    T={14,17,19,20,96,99,101,102},
    U={8,...,110}\T,   |U|=95,
    D_U=union_(i in U) {B:B is a subspace of F_i}.

An exterior chart is a chart outside D_U. An exterior descent is a future
owned downward MOVE whose destination is exterior. Ground lies in D_U, so
an exterior chart has positive rank. A low exterior descent has destination
rank at most four. This definition concerns the destination; its origin can
have any larger rank.

The three authenticated source cuts have 222,444,666 original columns and
410,812,1218 live fields, respectively. The prior independent replay packages
check every original column and live field. The present checker authenticates
those exact full-row cut files and their source words, independently rechecks
the whole source movement invoice and every cut chart, and examines every
remaining-input coefficient of every field. After conditioning all inputs
outside U, its new exact conclusion is

    support_U(field at B) subset {i in U:R_i lies in B}.       (1)

This includes the proper half reservoirs, raised Ys, every native copy,
public original record, and Hub field. There are no geometric U-support
leaks in any source. The resulting all-field witnesses are retained in
ALL-FIELD-LOCALITY.json. Some unconditioned half payloads have support outside
their chart; (1) is the audited conditional statement that is actually used.

For a real chart B, let L_B be the vector space of linear input forms whose
U-support is contained in {i:R_i lies in B}. Then the initial field at B is
in L_B. Local linear gates and upward moves preserve this form of locality.
Downward moves need not preserve it; they are charged explicitly below.

Let each whole record have width V over a characteristic-two field k and
let b be the number of separately paid copies. Set d=bV. A movement across
a positive integer rank gap g costs [g]=g^t, with 0<t<=1. The numerical
comparison uses t=199/200 and the current complete source invoices. The
source's retained closing suffix contains no owned movement that could
already pay the future owned movements counted here. Splitting its required
public ascents cannot reduce their invoice, by subadditivity of x^t.

The private-region theorem independently requires at least 8b future positive
owned MOVE arrivals into the four private regions. Such arrivals may ascend
or descend. Their destinations have rank six or seven and lie outside D_U.
They are disjoint from D_U descent events and from low exterior descents.
Consequently at least 8b unit movement cost may always be added without
charging any movement twice.

## 2. The equality code and its geometric shortenings

Cut every future downward MOVE whose destination lies in D_U, replacing
the record after the move by an independent formal width-V variable. The
actual initial side-information audit and the chronological open-network
construction give a fitting factorization K=A C on U. If there are exactly
9b such events, K has rank 9d, and the 9bV rows of C are independent. Each event
payload block C_e has full row rank V; the entire collection is independent.

The induced95 rigidity theorem makes its row space Ccal a vertex-gauged
canonical code of dimension 9d. We use only these consequences of the exact
support classification:

1. Ccal intersects L_B trivially whenever rank B<=6.
2. For rank B=7, the intersection is either zero or a single scalar canonical
   direction lambda tensored with k^d, with its fixed invertible vertex
   gauges. There are exactly 25 possible proper directions lambda, and their
   real rank-seven support hyperplanes are distinct.
3. Any three distinct proper binary directions are linearly independent.
   The checker verifies all 2,300 triples. Equivalently, every proper mask has
   odd binary weight, so no three distinct proper masks can sum to zero.
4. Every D_U descent destination has rank at most one. Its nonzero-line
   possibilities are the 25 lines already classified by the equality theorem.

These statements apply to arbitrary characteristic-two extension fields
and noncommuting vertex gauges. The gauge matrices preserve whether a whole
role block is zero. In particular they preserve support containment in B.
For a proper direction lambda, its shortening has dimension d, not V; this
distinction is essential in the joint-bank argument below.

Every collection

    D_e=C_e-sum_(f<e) B_ef C_f                              (2)

obtained by subtracting arbitrary linear combinations of earlier cut blocks
still lies in Ccal and is jointly independent, since the change from the
chronological C_e blocks is block triangular with identity diagonal. This
will justify innovation claims without assuming that a payload was born at
Hub or that its earlier formation had no recoding.

## 3. Threshold gate when no low exterior descent occurs

Suppose no exterior downward destination has rank below r. Let event e have
pre-descent chart B of rank less than r. In the network where all D_U descents
are cut, no uncut downward move can reach B: every exterior downward
destination has rank at least r, and reaching B afterwards would require
another downward move to rank below r. Thus every uncut initial contribution
to this event follows only local and upward paths. By (1), that contribution
belongs to L_B. All other contributions are earlier formal cut variables.
After substituting their actual values, the payload has

    C_e=L_e+sum_(f<e) B_ef C_f,    L_e in L_B.

The residual D_e=L_e is in Ccal and has rank V by (2). If rank B<=6 this
contradicts Ccal intersect L_B=0. Therefore every event origin has rank at
least min(r,7). Since its destination has rank at most one, its movement
gap is at least min(r,7)-1, in addition to being positive.

In particular, if there is no low exterior descent, take r=5. The 9b event
movements cost at least 9b[4]. Adding the direction-neutral private arrivals
gives

    additional movement >=9b[4]+8b.                         (3)

Allowing arbitrary exterior descents to ranks five through seven does not
change this bound. The stricter no-exterior-descent submodel gives 9b[6]+8b.
This stricter submodel is not vacuous merely because private arrivals are
required: those arrivals may be upward MOVEs from earlier arrivals below.

## 4. One low exterior descent: the quotient argument

Suppose there is exactly one low exterior descent, denoted z. Write A for
its destination, a=rank A in {1,2,3,4}, S for its source, s=rank S>a, and Z
for its full U-projected payload. All other exterior downward destinations
have rank at least five. Let m count the D_U events whose origins B_e have
rank at most four. Other D_U events already cost at least [4].

Cut both the D_U events and event z. For each low-origin event e, an uncut
initial path to B_e must again be local and upward. Any contribution from z
requires A subset B_e. Its exact payload equation is

    D_e=L_e+T_e Z,    L_e in L_(B_e),                       (4)

where D_e has the chronological form (2), and T_e is V-by-V. Every such
event occurs after z; otherwise T_e=0 contradicts Ccal intersect L_(B_e)=0.

Each T_e is invertible. If a nonzero row vector u satisfied uT_e=0, then
uD_e=uL_e would belong to both Ccal and L_(B_e), hence would vanish. This
contradicts the full row rank of D_e. Normalize

    F_e=T_e^-1 D_e=Z+L'_e,    L'_e in L_(B_e).              (5)

The m normalized blocks F_e remain jointly independent. For two distinct
events their difference has rank V, lies in Ccal, and is supported inside
B_e+B_f. Both charts contain A, so

    rank(B_e+B_f)<=rank B_e+rank B_f-a<=8-a<=7.

The nonzero canonical difference requires rank at least seven. Therefore,
whenever m>=2,

    a=1,   rank B_e=4 for every low-origin event e,
    rank(B_e+B_f)=7 for every distinct pair.                (6)

Each difference F_e-F_f consequently belongs to one proper shortening
lambda_ef tensor k^d. Its V-by-d coefficient matrix has full row rank V.
For three events the identity

    (F_e-F_f)+(F_f-F_g)=F_e-F_g

forces all three proper directions to be equal. If the directions were all
distinct, their verified binary independence over k would force every
coefficient matrix to vanish. If precisely two directions coincided, the
coefficient of the remaining direction would vanish. Either contradicts
the rank-V difference. It follows that all pair differences occupy one
common d-dimensional proper shortening. For m=2 this is immediate.

Thus all m blocks lie in the sum of the V-dimensional row space of F_1 and
one d-dimensional shortening. Their independent rows give

    mV<=V+d,   hence m<=b+1.                               (7)

This is a joint-bank rank bound. It does not multiply a scalar cover number
or assume that a width-V event fills a d=bV shortening.

### The low exterior movement itself has gap at least three when m>=2

By (6), A is a line and all low origins have rank four. If s<=3, then before
event z its source S can receive no other low exterior descent, and no high
exterior descent can reach it without a cut D_U event. Its payload is

    Z=L_S+sum_(f<z) H_f C_f,    L_S in L_S.

Subtract this earlier canonical contribution from (5). The resulting block
is still a full-rank chronological canonical innovation, but is supported
in S+B_e, whose rank is at most s+4-1<=6. This is impossible. Hence s>=4,
and z has gap s-1>=3. Every low-origin D_U event also has gap at least three,
by (6) and its destination rank at most one.

Therefore, when m>=2, the joint price of the m low-origin events and their
single low exterior entry is at least (m+1)[3]. All remaining D_U events
cost [4]. The private arrivals are a disjoint additional 8b, giving

    additional movement >=(9b-m)[4]+(m+1)[3]+8b,
    2<=m<=b+1.                                             (8)

### A single low-origin event cannot improve the threshold bill

Let m=1, r=rank B_e<=4, and d_e=rank(destination e)<=1. Both B_e and S
contain A. If s>=5, the two rank gaps have sum

    (s-a)+(r-d_e)>=5-d_e>=4.

If s<=4, the preceding local expansion for Z applies. After subtracting
earlier canonical contributions, a nonzero canonical block is supported
inside S+B_e. Thus s+r-a>=7, and the two gaps sum to at least7-d_e>=6.
In both cases subadditivity gives

    [s-a]+[r-d_e]>=4^t.

The low exterior movement and its one low-origin event together cost at
least the ordinary[4] threshold price. If m=0, the exterior event is simply
an extra positive movement. Consequently (3) still holds whenever m<=1.

## 5. The weighted theorem and exact budget consequences

Combining the preceding cases, at most one low exterior descent implies

    additional movement >=
      9b[4]+8b+min(0,(b+2)[3]-(b+1)[4]).                   (9)

The minimum in (8) occurs at its largest permitted m because[4]>[3]. For
b=1 or b=2 the correction term is nonnegative for every 0<t<=1:
3[3]>=2[4] and4[3]>=3[4]. For b=3 at t=199/200, the best lower profile is
23[4]+5[3]+24, or 43.42744651589682 per copy. This still exceeds the current
three-copy room.

All numerical intervals are outward rational certificates at t=199/200.
The optimistic per-copy caller ceiling is 1621.7508802111523552...; it is
used only as the existing necessary source-budget ceiling, not as a completed
batched caller construction.

| Source | Copies | Current per-copy room | Lower bill with at most one low exterior descent | Strict deficit per copy |
|---|---:|---:|---:|---:|
| Scalar pair source | 1 | 30.95377265821791 | 43.75132983573329 | 12.79755717751537 |
| Two-copy F4 source | 2 | 42.94339242695855 | 43.75132983573329 | 0.80793740877474 |
| Three-copy F8 source | 3 | 42.94339242695855 | 43.42744651589682 | 0.48405408893826 |

The proof charges only the 9b D_U movements, the 8b compulsory private-region
arrivals, and, when used, the distinct low exterior movement. Every other
paid ascent or descent is optimistically omitted. There is no double charge
between these three categories. Neither support rank nor equality rigidity
is used as an unsupported Hub-birth claim.

## 6. Scope and verification

The two explicit escapes are material: a continuation may use more than 9b
D_U descent events, or may use at least two low exterior descents. This
package neither prices those cases fully nor proves that either escape is
feasible. Nonlinear encoders do not inherit the canonical equality theorem
and are outside the weighted theorem's scope. The previously proved nonlinear
17b/2 information bound remains separate.

Run

    python -B check.py --repo REPO --workers WORKERS --out OUTPUT

The checker authenticates the finite geometric dependencies, source word and
full coefficient cut; rechecks all cut charts and complete movement profiles;
checks every current field's U-root support containment; verifies all 2,300
proper-direction triples and the distinct proper hyperplanes; and evaluates
the source room and lower bills with outward integer-root intervals. The
chronological quotient proof above is the mathematical component; a passing
finite checker alone is not a substitute for reviewing it.
