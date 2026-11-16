# A nonlinear selected-bit gate in the retained compact-control tariff

**Conditional physical specialization, pending independent review. No new kappa.**
This extends the retained compact-control construction from binary row addition
to a simultaneous Toffoli on three complete slots. It uses the same chunk-swap
and record-paid rotation interfaces, an extra reserved front field, and an
explicit exceptional-stream repair. No arbitrary-address gather or zero-valued
payload input is postulated. The source/record hypotheses are retained below.

## 1. Proposition and exact interface

Fix the finite template and a chunk-swap exponent0<tau<1. Let the complete
rectangular address set carry M arbitrary records of R bits, total volume
V=MR. Every complete address and its descriptors have O(A) bits; in
particular every slot/control field has O(A) address bits. The number of
fields is fixed by the template.
Take three disjoint complete slots x,z,y of fK address bits, in any order,
with selected positions j_i=rho+iK,0<=i<f,0<=rho<K. They may have arbitrary
spectators between them. We construct exactly

    y_(j_i) <- y_(j_i) XOR (x_(j_i) AND z_(j_i))

for all i, preserving every other address bit and the payload records.
The operation permutes entire arbitrary records; it does not create a new
independent coordinate or assume a clean temporary record.

For n=f-1>0, reserve three disjoint complete nG-bit front fields u,v,t before
all active slots and one complete nG-bit back field b after them. Each has n
radix-B digits, B=2^G. They have arbitrary contents and must be restored.
The inherited primitives are: arbitrary-width chunk swaps with all spectators
charged, and controlled modular rotations whose offset is independent of the
target and polynomial-time computable from earlier controls/descriptors.
The latter is precisely the retained record-paid rotation lemma; it already
permits nonlinear offset functions. It costs O(V+M A^C) for a fixed C.

Under the same layer regime

    G=4 ceil(log2 p)+6, f<=p, A=O(p), K/log p -> infinity,
    R exceeds every fixed power of p,

the exact Toffoli costs O(V*((f log p)^tau+1)) on a fixed number of tapes.
All temporary fields, field order and arbitrary records are returned. The
constant is independent of f,p,V after the finite template/parameter family
is fixed. A cubic unit-phase pass also costs O(V) in this same regime.
These are conditional consequences of the retained physical interfaces,
not independent proofs of the five multiplication foundations.

## 2. An earlier Boolean-control toggle

Let c_i be ANY Boolean function of front controls, kept unchanged during a
toggle. The retained four-update identity for one target segment Y and dirty
temporary T is

    Y <- Y+2 c T;
    T <- T+(Y mod2);
    Y <- Y+c(1-2T);
    T <- T-((Y mod2) XOR c).

On the guarded integer range, it changes Y to Y+c(1-2a), where a is its
original parity, and restores T. Thus it toggles only that parity by c.
The proof depends on c being a fixed bit during the four updates, not on c
being a linear address function.

Apply it simultaneously to the low n selected segments of y. The two y
rotation offsets are sums of2 c_i t_i 2^j_i and c_i(1-2t_i)2^j_i. Each
temporary update swaps t with b, rotates the back field by the appropriate
packed selected parities of the current y, then swaps back. Controls precede
every rotation target. This costs four compact swaps and four rotations.
Take c_i=(u_i mod2)(v_i mod2); both controls stay fixed within each toggle.

## 3. Four toggles cancel arbitrary dirty controls

Write X_i=x_(j_i), Z_i=z_(j_i). Loading X into u means swapping u with b,
rotating the back field by sum_i X_i B^i, then swapping back. All source
slots precede b even when they follow y. A load uses two compact swaps and
one rotation; its inverse is the same construction with negative offset.
Use this exact chronological sequence:

1. Toggle y using parity products of u,v.
2. Load X into u.
3. Toggle y using parity products of the current u,v.
4. Load Z into v.
5. Toggle y using parity products of the current u,v.
6. Unload X from u.
7. Toggle y using parity products of the current u,v.
8. Unload Z from v.

On the guarded range the original control parities U_i,V_i consequently give

    U_i V_i XOR (U_i XOR X_i)V_i
    XOR (U_i XOR X_i)(V_i XOR Z_i)
    XOR U_i(V_i XOR Z_i) = X_i Z_i.

Each intermediate target toggle preserves its guard and restores t. Both
front loads are reversed, and every swap pair restores the arbitrary back
field. Hence all four temporary fields return exactly. There are **24 compact
swaps and20 record-paid rotations** for the low selected positions, independent
of f. All operations are actual address bijections; offsets are evaluated on
their current controls, including in reverse execution.

## 4. Guards, global bijectivity and exact exceptional repair

Declare an address bad if any digit of its original u,v,t equals B-1, or if
any low target segment, written2g_i+a_i, violates

    2B <= g_i < 2^(K-1)-2B.

On a good address the u and v loads stay within individual digits, so their
parities change exactly by X_i,Z_i. The target four-update identity displaces
each segment by at most2B before restoring its guard. The t load stays within
its digit, too. Induction over the four toggles establishes the desired map
on the good set, for arbitrary control values and source-slot ordering.
The good-set proof is not asserted on overflowing modular digits.

Complete address ranges give the counting bound

    delta <= min(1, n*(3*2^-G +8*2^(G-K))).

Let T be the ideal low-position Toffoli and S the actual44-operation compact
word. T changes only target parities, so it preserves the bad predicate.
S is a bijection on the WHOLE rectangle, because every swap/rotation is a
bijection and every offset is independent of its own target. Since S=T on
the good set, S maps that set bijectively to itself and therefore preserves
its complement as well. Thus T S^-1 is supported on the bad set.

Extract the bad records from the stream after S, retaining marked holes.
For each extracted address q, evaluate S^-1 using reverse order and CURRENT
inverse controls, then compute T(S^-1 q). The fixed44-operation descriptor
computation has polynomial cost O(A^C) per record (C=3 suffices with ordinary
schoolbook descriptor arithmetic). Stable binary radix passes sort the
extracted records by their destination keys. Reinsert them into the holes.
Keys are distinct and occupy exactly the bad holes by the bijection argument.
This is exact deterministic repair, not discarding a small erroneous set.

The rotation/repair cost is

    O(V+M A^3+delta M A(R+A)).

No growing descriptor is scanned per payload bit. Work tapes, extraction,
rewinds and clearing are the same fixed-tape primitives already charged in
the retained proof. If eventually K>=G+4 ceil(log2 p)+10, then

    delta <= 7/(128 p^3),
    A^3/R=o(1), delta A(1+A/R)=O(p^-2).

Hence all repair/rotation work is O(V) per call. The24 swaps each have width
nG and cost O(V*((nG)^tau+1)); their constant count proves the claimed tariff.

The omitted highest selected bit is handled separately and exactly. If its
target is not last among the three chosen address bits, swap it with the
last one using a width-one chunk swap. Both controls now precede the target.
One controlled rotation of that one-bit target by their Boolean product
performs the Toffoli; undo the swap. At most two width-one swaps and one
rotation cost O(V), with all intervening coordinates restored. This also
handles f=1. Repair the low-position word before this final operation.

## 5. Reservations survive the complete recursive layout

Use the retained layer's global p,d,K and H=dG at every recursive node. Keep
its row reservation q0 and back reservation q_B=ceil(H/K), and replace the
front reservation by q_F=ceil(3H/K). Process these axes individually as in
the retained layout. The front region supplies three complete H-bit fields;
carve nG bits from each for the current call, leaving unused bits as spectators.
The back region supplies the fourth field. No address coordinates are added.

The row index uses only the separate first q0 chunks. Whole-row padding and
the W-way split preserve complete u,v,t,b ranges in every child, exactly as
in the pinned layout. Each role receives1/W of its parent's current volume.
Controls finish and are restored before a scalar gate, child or returned
result uses them. The fixed-tape scheduler charges parked streams by their
own volumes and does not allocate one tape per selected position.

Now q_F+q_B<=4dG/K+2, versus the old3dG/K+2. Eventually K>=d^c/2, giving
at most8d^(1-c)G+2. The full reservation cost still is

    O(V*(log(2d)+d^max(1-c,0) log p+1)).

If D<=q0+q_F+q_B, use the same individual-kernel fallback. Reserved axes are
within the original D and never exceed d. Ideal Toffoli and fixed recipes
built from it act as identity on reserved coordinates, commuting with the
earlier individual kernels there. Restored row order returns every original
row separately; padded zero rows stay zero at completion.

Node overhead remains O(G^tau e^tau+1). Hence the retained volume-weighted
recurrence, stopped-depth bound and strict outer inequalities keep their
form with larger fixed constants. Repair is charged at EVERY node; an old
global exceptional-stream bound is not reused. These added permutations
introduce no coefficient arithmetic or height. Any completed source/compiler
must still recompute actual counts, ownership, precision constants and endpoints.

## 6. Cubic phases and finite nonlinear monomial recipes

A fixed phase on f selected columns has the form

    i^(a*f+sum_i q(x_i,z_i,y_i)),

where q is a fixed table in Z/4. CCZ uses q=2xzy. Compute the residue from
address/descriptors once per complete record in polynomial O(A^C) setup,
then apply its sign change and/or real/imaginary exchange to the full
coefficient encoding. This costs O(V+M A^C)=O(V) in the retained record regime.
All spectator records are included. The absolute phase a*f and the sum are
retained exactly; no scalar is incorrectly moved outside a tensor power.
These unit phases add no coefficient height and have norm one.

A fixed finite recipe of affine selected-bit gates, the constructed Toffoli
gates and these phase passes, with its actual inverse, therefore has tariff
O(V*((f log p)^tau+1)). Its constant and descriptor code grow with the fixed
recipe, not f or input length. This does not assert a cheap arbitrary RAM
permutation. It supplies actual primitive decompositions for nonlinear head
adapters in the programme's next complex source.

Here the f-column source lift acts on the f designated bits at one fixed rho
inside each fK-bit physical slot. The other K-1 positions in each chunk are
spectators and are restored. This is exactly the retained selected-axis
embedding, not a claim to perform all K choices of rho for one tariff. A
caller requiring several choices must charge each invocation unless it
separately proves and invoices a simultaneous implementation.

## 7. Verification, remaining premises and credit

The new argument is the exact algebra, chronology, guard counting, deterministic
repair and changed reservation count. The inherited chunk-swap tariff and
complete physical/record domain remain explicit. No foundation is discharged
and no parameter range is silently extended. A profitable complex caller,
complete BIT source, strict suppliers and target theorem remain open.

Independent finite evidence checks the literal modular word and its inverse
on complete small address rectangles, plus boundary/multidigit cases, and
checks bad-set preservation and exact repair. Omitted stages and missing
repair fail controls. These computations supplement the all-parameter proof.
Root's parameter/linkage checker separately pins the retained sources, checks
the exact finite-difference identity, reservation/guard inequalities and
literal highest-bit lowering. Independent review is a separate artifact.

Credit Douglas Colkitt and the original compact-control, chunk-swap,
ordered-affine streaming, dirty-control repair and recursive-layout authors;
exact canonical pins/copies are in DEPENDENCIES.json. New nonlinear
specialization developed in @CubeJerry's persistent programme with OpenAI
assistance. Independent review pending. **No new kappa.**
