# A common-basis executor for a Weyl-star pencil

Status: **proved algebraic and tape-composition component; independent review
requested**. This is a positive local batching construction. It is not yet
an executor for the retained Fourier rectangle maps, and it does not prove
RV-W, RV-I, or a stronger global multiplication bound.

The final limitation matters: one batched pencil has a whole-active-width
address bill. Repeating it through Theta(sqrt(m)) predictor stages still
leaves a positive power of m unless its common basis is reused. No such
reuse across all retained rectangles is asserted here.

## 1. Operator family and complete occupancy

Let m>=1 and f>=1. There are m independent complete f-bit query fields
x_1,...,x_m, and two unchanged complete f-bit parameter fields s,xi.
Arbitrary additional spectator fields and independent row indices are
allowed. Let a bound the active address width; initially a=(m+2)f, and
spectators need not be included in that bound when using the established
active-field wrapper. Every address slot carries arbitrary independent
data. There is no zero address coordinate or initialized module row.

For each j define the exact rational signed permutation

    (W_j(s,xi)F)(x_1,...,x_m)
       = (-1)^(xi dot x_j) F(x_1,...,x_j+s,...,x_m),       (WB1)

where addition and the dot product are over F_2. The parameters s,xi
are unchanged. Let B_j be any supplied row matrices independent of the
query fields, with compact polynomial-m descriptions and coefficient
heights. Their row action commutes with every address change below.
The pencil to execute is

    P = B_0 tensor I + sum_(j=1)^m B_j tensor W_j.        (WB2)

Complex coefficients are used only in a constant-rank extension Q(i).
Expanding real and imaginary components gives an exact rational routine
with a factor-two volume cost. All input components can be arbitrary;
the final operator WB2 has rational coefficients and acts separately on
both components.

## 2. One common coset layout

When s=0, every W_j is already diagonal. Suppose s!=0 and choose its
least nonzero bit t. Write

    epsilon_j = (x_j)_t,
    u_j = x_j + epsilon_j s.

Then (u_j)_t=0. The f-1 other bits of u_j, together with epsilon_j,
form a bijective encoding of x_j. Place the epsilon bit last using a
cyclic permutation of the f bit positions; retain the remaining bits
in the same cyclic order. Let C_s be this simultaneous layout change
on every query field. It neither changes s,xi nor discards the zero
coordinate: the latter is omitted and its physical position holds
independent epsilon_j. Thus the full array volume is unchanged.

Put delta=xi dot s. In the new layout

    C_s W_j C_s^(-1)
       = (-1)^(xi dot u_j) Z_j^delta X_j,               (WB3)

where X flips epsilon_j and Z multiplies by (-1)^epsilon_j. Every
u_j is fixed by the operator. This is a one-bit operator, despite the
original f-bit translation.

Let

    H = [[1,1],[1,-1]],
    D_delta = diag(1,i^delta),
    G_delta = D_delta H.

Since D_delta^(-1) Z^delta X D_delta = i^delta X,

    G_delta^(-1) (Z^delta X) G_delta = i^delta Z.        (WB4)

Use G_delta on every epsilon_j. Its inverse is
(1/2) H D_delta^(-1), so all coefficients lie in Z[1/2,i].
Consequently the entire pencil becomes pointwise row mixing with

    B_0 + sum_j (-1)^(xi dot u_j + b_j) i^delta B_j,    (WB5)

where b_j is the transformed epsilon coordinate. The correct application
order is C_s, then G_delta^(-1) on all query bits, then WB5, then
G_delta on all query bits, then C_s^(-1). At s=0 omit all these basis
changes and apply B_0+sum_j(-1)^(xi dot x_j)B_j directly.

This proves the exact algebra for arbitrary independent input rows.
It does not replace an operator sum by a product of permutations.

## 3. Physical implementation of the common layout

Use the pinned OpenAI tape source, commit
3344da59991ed94f9ba711217b29c1d760badfa6, permutations.tex,
“Controlled permutations on small blocks,” with the already completed
E002 active-width and exact-interchange substitution. This supplier
implements parallel small-block value permutations whose unchanged
controls occupy at most a fixed fraction of the active address.
All control tables below are generated in polynomial(a) bit work,
not supplied by an address-word oracle. Its guards, exceptional-record
radix repair, rewinds and occupied workspace remain charged.

First move position t of every x_j to its last position. Compute the
cyclic shift amount f-1-t from s. For each bit of that shift amount,
conditionally apply the corresponding fixed power of the f-position
cycle, simultaneously in every query field. A fixed position permutation
is a product of two involutions, so each such power uses two layers of
disjoint two-bit swaps. Every swap is a two-bit block-value permutation
controlled only by s. There are O(log(f+2)) layers. This does not require
f to be a power of two and does not append dummy positions.

Next, for every non-pivot position of every query field, flip its bit
conditionally on the product of that query's epsilon_j and the matching
bit of s in the rotated order. This is a single family of one-bit block
permutations. The unchanged controls consist of the f bits of s and the
m epsilon bits. For f>=2 they occupy at most half of (m+2)f, because

    f+m <= ((m+2)f)/2.

The two-bit permutation layers have still fewer external controls.
Thus one fixed free-fraction guard applies. The controlled-block supplier
handles all these flips together, including the shared controls. They
are not executed as m separate f-field XORs. Reverse the flips and
position layers for C_s^(-1). Handle f=1 directly, where no coset shear
or position permutation remains.

If the supplied exact interchanger has time
V sqrt(u+1) E_I(u), with monotone E_I, the complete C_s and inverse cost

    O(V sqrt(a+1) E_I(a) polylog(k)),                  (WB6)

with fixed log degree, where k is the retained outer precision/address
parameter. Their workspace is the supplier's O(V E_I(a)) envelope plus
compact polynomial descriptors. Preparation is separately charged under
the same root/local descriptor contract as E002 V. Narrow guarded widths
use the existing direct branch and are absorbed by the displayed fixed
logarithmic allowance.

The m one-bit transforms and their inverses use O(m) ordinary full-volume
passes. A single specified address bit can be moved to the adjacent-pair
position and restored in O(V) tape steps, with actual counter scans and
rewinds. Condition on s!=0 when mixing that pair. All other address bits
are restored. Applying the diagonal phases and WB5 takes polynomial-m
ordinary arithmetic per volume under the declared row-matrix supplier.
The m dot products xi dot u_j together scan only mf address bits, within
one O(k)-bit numerical record/counter allowance. Extra row buffers follow
the supplied row-mixing invoice; none is free.

Therefore the complete local bound is

    Time_P <= V [m^K + sqrt(a+1) E_I(a) polylog(k)]
              + separately charged compact preparation,       (WB7)

for one fixed K covering the row matrices and arithmetic. Visited space
is the inherited interchange envelope plus the declared polynomial-m row
buffers. The layout itself adds only O(V) payload space. This theorem
does not strengthen an unspecified row-mixing space supplier.

## 4. Precision and repeated pencils

No numerical square root is needed: H and its rational inverse suffice.
The product of m one-bit changes has logarithmic operator-norm growth
O(m), and the scalar phases have absolute value one. Together with the
polynomial-m row-matrix heights, the local norm and precision invoice is
of the type already allowed in the numerical compiler. A full global
error budget still requires the usual path and event-count guard; this
local algebra is not that global precision proof.

If an entire sequence of pencils uses exactly this same W_j family,
with row matrices that change by stage but still act only on row indices,
the same C_s and G_delta diagonalize every stage. Apply them once at
entry, perform all stage row matrices pointwise, and undo once at exit.
The expensive address bill WB6 is then paid once for the sequence,
while ordinary arithmetic grows by the number of stages. This is a
proved reuse property of this operator family.

It does not apply merely because two individual rectangles each admit
a Weyl-star representation. Different rectangles may require different
bases and their sum need not share either basis. The retained predictor
is a polynomial of the complete pencil, not the sum of independently
evaluated rectangle polynomials. Distributing that polynomial over its
rectangle terms would be incorrect.

## 5. Applicability limits and current result

The construction gives an explicit example where m nontrivial query maps
can share physical work, so a separated-query map-volume count alone is
not a physical lower bound. It is compatible with the earlier scoped
obstruction: C_s changes query coordinates and uses a genuine common
basis rather than phases and auxiliary-only reindexing.

For one pencil, WB7 replaces m separate f-field map costs of order
m V sqrt(f) E_I(f) by a whole-active-width cost of order
V sqrt(mf) E_I(mf), up to logarithms and ordinary arithmetic. This saves
a square-root-m factor in that explicitly specified subfamily.

If the common basis is rebuilt at each of Theta(sqrt(m)) predictor stages,
its total expensive bill is instead of order
sqrt(m) V sqrt(a) E_I(a) polylog(k). This still has a positive power of m
after square-root-a normalization. It does not establish the numerical
address gate NI5. Reusing the basis across the complete retained pencil
would remove that extra factor, but is not established here.

Actual free-rectangle representatives also contain query/auxiliary
exchange patterns. The family of swaps of one shared auxiliary register
with query j is noncommutative for different j. Such a family cannot be
simultaneously diagonalized, so WB4 cannot be applied to it simply by
renaming its registers. Neither an exact classification of all source
middle maps nor a replacement of those swaps has been supplied here.

The admitted global bound remains E002 Theorem V. This component is a
positive construction with explicit interfaces and a reusable test target,
not a new endpoint result or a lower bound on other physical executors.

Credits: @CubeJerry; the pinned controlled-block tape processor; E002's
active-width exact interchanger; standard finite Weyl/Pauli algebra;
and substantial ChatGPT multi-agent assistance. No priority, full-machine
execution or formal refinement is claimed.
