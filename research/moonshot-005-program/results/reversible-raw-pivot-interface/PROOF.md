# Reversible raw pivots for distributed aggregate collection

## Status and computational contract

This is an exact field-linear interface lemma, proposed for independent review
in S007. It explains the mechanism of the source-specific three-receiver word
and the systematic eight-receiver cohort under construction. It does not prove
that all required source rows admit a compatible global schedule, a uniform
supplier, or a new multiplication exponent.

Use the programme's retained normalized-coordinate chart transport contract.
A raw field at chart L may move to a nested chart C through the corresponding
complete recursive operation; in normalized coordinates it remains the same
field value. A rank-r MOVE is charged r^t in the native moment, with 0 < t <= 1.
All ordinary field operations, coefficient services, storage, precision,
ownership and erasure remain charged through their separate contracts. Exact
chart maps and arbitrary-volume physical realization are premises, not proved
by this algebraic statement.

Let F be any field and V any positive integer. Let 1 <= m <= p. Let q_1,...,q_p be arbitrary,
independently variable vectors in F^V, in existing raw carriers whose initial charts L_j
are subspaces of a common chart C. All carriers eventually terminate at a hub
H containing C. A receiver i needs a specified row (Aq)_i at a chart F_i with
C contained in F_i contained in H. The m rows of A are indexed by distinct
delivery duties; their receiver charts need not be distinct. No raw carrier
has an intervening use requiring its original q value during this construction.

## Theorem 1: exact preservation and acquisition interface

Choose m distinct pivot indices I and write J for the other p-m indices. The
following in-place transformation preserves all p raw input fields if and
only if the square matrix A_I is invertible:

    q'_I = A_I q_I + A_J q_J = Aq,     q'_J = q_J.

When A_I is invertible, it can be implemented using only cochart ADD and
nonzero SCALE operations on the existing carriers at C. Route pivot i through
F_i and then to H, and route every nonpivot from C to H. Copy the pivot value
to a real stationary receiver or owned accumulator while it is at F_i. Once
all these carriers have reached H, the local inverse

    q_I = A_I^{-1}(q'_I - A_J q'_J),   q_J = q'_J

restores every original raw value before its next use. No extra owned MOVE is
needed for this acquisition-and-restoration interface. Every newly introduced
raw stop, owned accumulator, ordinary operation and retirement is still owed.

Consequently some pivot choice works if and only if rank(A)=m. Full row rank
alone does not justify an arbitrary pivot choice: the selected minor must be
checked. If the m requested rows are dependent, this one-carrier-per-row
interface cannot replace m raw values and preserve all p inputs without
additional retained information or a different delivery scheme.

### Proof

Order the raw coordinates as (I,J). The emitted linear map is the block matrix

    M = [[A_I, A_J], [0, I_(p-m)]].

It has determinant det(A_I). If that determinant is nonzero, Gaussian
elimination expresses A_I as a product of elementary row additions, nonzero
scalings and swaps. A swap is realizable in place with three additions and
one multiplication by -1, also in characteristic two. Apply these elementary
operations on the pivot carriers at C, then add the A_J contributions from
unchanged nonpivot carriers. Every operand is physically at C.

The nested routes transport the actual pivot values to F_i. A stationary
zero-initialized field there can receive the value by ADD and later supply it
to the receiver at its actual visit. The pivot continues to H. Once all
nonpivots and pivots are at H, the displayed inverse is cocharted and valid
on all V coefficient positions. It recovers the original q exactly; it does
not infer q from an independently assumed duplicate.

Conversely, fixing q_J leaves the pivot outputs with rank rank(A_I) on q_I.
The kernel has dimension m-rank(A_I), so full recovery is impossible from
these emitted values alone if A_I is singular. A rank-m matrix has an
invertible m-column minor, and a rank-smaller matrix has none. This proves
the pivot existence criterion and the stated necessity.

More generally, the output information rank is p-m+rank(A_I) per coordinate.
Additional linear records must contribute at least m-rank(A_I) independent
dimensions on its kernel. That algebraic minimum is attained by completing
the row basis with coordinate records; acquiring and transporting those
records is a separate physical obligation. This is a specialization of the
programme's retained-record accounting, not a waiver of it.

## Theorem 2: exact changed raw-route invoice

Write D=dim(H), c=dim(C), ell_j=dim(L_j) and f_i=dim(F_i). Set 0^t=0, meaning
that an equal-chart segment emits no MOVE. Relative to direct L_j-to-H raw
routes, the added recursive moment of the routes in Theorem 1 is exactly

    sum_j [(c-ell_j)^t + (D-c)^t - (D-ell_j)^t]
      + sum_i [(f_i-c)^t + (D-f_i)^t - (D-c)^t].

This counts every carrier once in acquisition and replaces the pivot's
direct C-to-H segment by its two delivery segments. The expression is
nonnegative by subadditivity of x^t for 0<t<=1. Rank mass is unchanged because
all paths remain nested and monotone. The expression is not zero merely
because no new owned packet is used.

For the native's line-to-nine-dimensional-hub geometry and facet deliveries,
ell_j=1, D=9 and f_i=8. The expression simplifies to

    p*((c-1)^t + (9-c)^t - 8^t)
      + m*((8-c)^t + 1 - (9-c)^t).

At t=1 this transport-rank increment vanishes, while the ordinary acquisition,
decoding and restoration operations remain. At t<1, splitting an ascent has
a real price. If a construction begins from already split routes, compare the
actual old and new histograms instead of applying the direct-route baseline
twice.

### Proof

Each nonpivot uses ranks c-ell_j and D-c. Pivot i uses c-ell_i, f_i-c and D-f_i.
Subtract the original rank D-ell_j moment per carrier. Regrouping gives the
formula. The two inequalities a^t+b^t >= (a+b)^t prove nonnegativity and the
telescoping sum of dimensions proves rank-mass conservation.

## Ordinary operations and live records

One concrete Gaussian-elimination implementation of A_I uses at most
m(m-1)+3(m-1) ADDs and 2m-1 nonzero SCALEs, including at most m-1 swaps.
Adding A_J costs at most m(p-m) further ADDs. The inverse uses the same bounds.
Thus acquisition plus restoration can be implemented with at most
2m(p-1)+6(m-1) ADDs and 4m-2 nonzero SCALEs. These are generous existence
bounds; a source word should report its actual sparse operations and exact
coefficients. No scalar multiplication is assumed free.

If all deliveries need delayed owned records, each adds one INIT, one ADD to
the record, one ADD at consumption, and one CLEAR. At most m such records are
live for this one group. The receiver's visit and the permitted retirement
must be real. Reusing a persistent accumulator across groups can reduce
lifetimes but needs a compatible chronology and a fresh peak-storage audit.

The interface assumes the q inputs have already been formed. It does not
remove input difference formation or final private/common recoupling from a
complete word's invoice.

## Composition gate

Disjoint donor groups satisfying the theorem may be processed with separate
local maps, provided all delivery visits and receiver accumulations coexist
and all originals are restored before their later uses. Their block-diagonal
raw map is invertible and their actual route/ordinary costs add.

For overlapping groups, local invertibility alone preserves total information
but does not prove that a later operation computes its intended row of the
original q. If the current global raw matrix is M, a cocharted set S contains
rows M_S. Using only those raw fields, a desired original-input aggregate a q is
obtainable there only if a lies in row(M_S). If cocharted owned records or
other declared observations are also available, append their current
original-input rows to the availability matrix before applying this test.
Its actual coefficients must be solved against that complete current matrix. A fresh invertible local row operation gives another global
invertible map; the final inverse is the reverse chronological product.

This gives an explicit algebraic test for a coded continuation, not automatic
route compatibility. Once a carrier has reached H, returning it to a lower
cochart is a paid detour. Independent eight-receiver cohort prices cannot be
summed while granting every cohort a fresh set of original source routes.

## Required negative controls

1. A full-rank A with a singular chosen minor must fail raw recovery.
2. Dependent requested rows cannot overwrite one carrier per row without the
   corresponding retained information.
3. Inverting overlapping group maps in the wrong order must be rejected.
4. A recipient facet not containing C is not a monotone delivery route.
5. Omitting acquisition or the final pivot leg must alter the paid histogram.

The universal claims follow from the arguments above. Finite source matrices,
word interpreters and exact chart checks can certify applications, but they
cannot by themselves supply the unbounded physical foundations.
