# The remaining query factor in numerical address work

Status: **proved source-operation audit and explicit local obstruction;
submitted for independent review**. This sharpens NW's coarse local physical
toll, but does not establish the separated numerical supplier SN. The
unconditional AQ theorem is unchanged. Concurrent S004's
`joint-rectangle-two-scale-transfer.md` gives a different conditional route
under JR by improving the binary rectangle family itself; this audit does
not assert that SN is necessary for every conditional improvement.

Source pin: OpenAI math `3344da59991ed94f9ba711217b29c1d760badfa6`.
Read and used here: Fourier `build/kernel.tex`, subsections "The product of
queries", "Sharing the queries of a pencil", "The endpoint Fourier
transforms" and "The finite saving and recursion"; Fourier `build/binary.tex`,
Proposition `prop:binary-template`; tape `build/walsh.tex`, "A recursive call
on tapes"; tape `build/permutations.tex`, `lem:packed-xor`. The quantitative
predictor is `routes/B/pairwise-newton-division.md`, B1--B3 and section 5.
The physical arithmetic/space dependencies are CW and NW in this directory.

All logarithms are base two. A **field move** means one complete width-f
slot exchange or packed-XOR addition, including its paid spectator ranges.
It does not mean a unit-cost address-word operation.

## 1. A sharper, separated local bound

Use the binary family and rational predictor of NW. Put

    D = D_F,  A = 2(m+D-1),  f <= a/A,
    lambda <= (1+log q_F)^L_F + 2^L_F,
    d_pred <= 7 sqrt(m),
    E_addr = (D+1)^2 (1+lambda).

The inequality for lambda counts either endpoint incidence, including the
charged rectangles. In particular

    log E_addr = O(sqrt(log(m+2) log log(m+4))).          (SN-A1)

Let J(u) be the physical per-volume price of an exact completed width-u
interchanger, with an absolute linear visited-space coefficient. Assume
J is increasing and J(u)>=1. The source packed-XOR construction then costs
`C V(1+J(f))(1+log(k+2))` for a width-f addition on a complete array of
actual encoded volume V. Its third slot is a paid, restored spectator.
Narrow slots use direct bit operations; the global fixed guard and its
absolute polynomial setup degree are the same as NW6.

**Proposition SN-A.** The actual NW local template admits the bound

    time <= C V [m^K + J(a)
                 + d_pred m E_addr (1+J(f))]
                 (1+log(k+2))^b + poly(m,k),            (SN-A2)
    visited cells <= C V + poly(m,k),

for absolute effective C,K,b. The recursive call count remains NW4. This
bound includes finite repair unrolling, preparation, physical scans and
returns. No recursive Fourier call is treated as ordinary work.

### Kernel address count

For a fixed query j, every common-coordinate and coset-representative map
acts only on its distinguished slot and the D-1 auxiliary slots in each
half. The remaining m-1 distinguished slots are spectators, exactly as
specified in `kernel.tex`. Thus the relevant binary matrix has dimension
at most 2D, even though the complete array has A axes. Gaussian elimination
uses at most C(D+1)^2 exchanges/additions. Its finite construction and
stored description are polynomial(m); this is a small support statement,
not an uncharged random-access implementation.

Process rectangles sequentially, retaining the NW constant-array schedule.
For a free rectangle the first and last auxiliary basis preparations are
performed once at each incident endpoint. Their field-move volume is at
most C(D+1)^2 lambda V per pencil. Between these endpoints, **each j** has
its own representative changes at incident sources and destinations.
Copy a current source, perform its small-support map, sum into a common
row, and add the mapped result to the current destination accumulator.
Restore or release the scratch before proceeding. Summed over all
incidences this has field-move volume at most

    C m (D+1)^2 lambda V.                              (SN-A3)

The row matrix is pointwise in the spatial address. Even a dense row
matrix is executed by polynomially many ordinary row scans; it is not
another spatial field move. For the Newton pencils the query coefficients
are in fact diagonal across seed rows, although this refinement is not
needed for SN-A2.

For charged rectangles, source and destination changes have the same
incidence bound and query factor. Their common kernel uses its separately
billed 2D recursive calls. All other common-kernel monomial maps act on
the same 2D slots, so the field-move bill is bounded by (SN-A3), with an
additional absolute constant. The number of common work rows divided by
the full batch is no larger than the charged endpoint incidence count.
This is deliberately conservative but contains no additional power of m.

Both predictor evaluations use at most 2d_pred pencils. Their Newton
updates, signs and rational divisions are pointwise. This proves the
third term of SN-A2 before finite contraction.

### Check, lift, boundaries and finite contraction

The fixed Vandermonde check H, transpose lift H^T and spectral repair
tables combine numerical rows at a fixed spatial address. On-demand key
evaluation and rational coefficient preparation are CW's ordinary
polynomial(m) work. Extracting, restoring and rewinding a selected coarse
row role takes complete tape scans; enumerating all roles is absorbed in
m^K V. These operations make no uncharged spatial reindexing.

The monomial equivalence between the query product and the target Walsh
has one exchange of the two full address halves, of width at most a/2,
plus pointwise signs. It costs C V J(a); it should not be decomposed into
m separate width-f swaps. The finite contraction calls have the same a,f
but actual volumes V/8 in each of two phases. Consequently their total
normalized nonrecursive bill is multiplied by

    sum_(h>=0) 2^h 8^(-h) = 4/3.

The terminal direct A-axis conversions are precisely the recursive calls
already included in the finite invoice. Their aligned row setup is
ordinary work. The bounded remainder outside Af is handled by direct
one-/two-bit butterflies and costs polynomial(m) V log(k+2).

Every addressed work row includes its entire f-bit source, target and
auxiliary ranges and every inactive spatial spectator. The leading seed,
label and contraction roles are selected by complete scans and restored.
Only a constant number of full payload arrays are kept at once. The
contraction stack shrinks by 1/8 and the numerical children shrink by the
exact power-of-two W_m factor. This preserves NW's absolute visited-space
coefficient and spectator divisibility; it does not borrow zero-filled
productive coordinates. All descriptor/scalar work has fixed polynomial
degree. These observations complete SN-A2.

## 2. What the square-root cancellation actually removes

For a useful regular price write

    J(u) = sqrt(1+u) L(u),   L increasing.

When f>=2 and A>=2m,

    d_pred J(f)
      <= 7 sqrt(m) sqrt(3f/2) L(a)
      <= 7 sqrt(3/4) J(a).                            (SN-A4)

Thus the refined executed upper bound becomes

    C V [m^K + (1+m E_addr) J(a)] log(k+2)^b
      + poly(m,k).                                    (SN-A5)

This is a real improvement over charging arbitrary polynomial(m) binary
elimination on width a. However, the cancellation removes the predictor
degree sqrt(m), **not the m distinct queries inside each pencil**. The
remaining m cannot be absorbed into the subpower E_addr. Substituting
SN-A5 into the unchanged binary recurrence retains the positive-majorant
gate in the lead's `numerical-toll-gate.md`; its local exponent is still
Theta(log m), regardless of the better absolute polynomial exponent.

The next section gives an exact free-endpoint example showing why the
query factor is not merely an accidental dense elimination count.

## 3. A two-dimensional free endpoint forces a query-dependent map

Work over the binary dot-product space of dimension two. Let

    d_v=e_1,  d_w=e_2,  H=<e_2>,  H^perp=<e_1>.

These are unit vectors with pairing zero. They occur in the source binary
Gram quotient already for q=2,L=2: the two parity classes give its two unit
directions. A singleton orthogonal source/destination pair is a valid free
rectangle. This tiny example is a test of the endpoint identity, not a
parameter family claimed to give the large-m saving.

For each half, v's distinguished coordinate is e_1 and its auxiliary
coordinate is e_2. At w their roles reverse. Use one auxiliary slot in
each half, denoted X_0,Z_0, and query j's distinguished slots X_j,Z_j.
All four slots have width f. On one column write the input as
`(x_j,x_0,z_j,z_0)`. The common-kernel output coordinates are
`s=(s_0,s_j), t=(t_0,t_j)`, because the destination frame is reversed.
The exact normalized one-column block from source v to destination w is

    K_j(s,t;x,z)=1/4 (-1)^[(x_j+s_0)(t_0+z_j)
                            +(x_0+s_j)(t_j+z_0)].      (SN-A6)

Let H_aux apply normalized Walsh to both auxiliary slots. Let D_aux be
the sign `(-1)^(sum_c x_(0,c)z_(0,c))`, and D_j the corresponding sign on
query j's two slots. Both H_aux and D_aux are independent of j. Define
the shared source and destination endpoints

    E_source = H_aux D_aux,
    E_dest   = D_aux H_aux.

Then the exact free-endpoint factorization is

    K_j = E_dest M_j E_source,
    M_j = D_j P_j D_j,                                (SN-A7)

where P_j is the address permutation

    X_j <-> Z_0,        Z_j <-> X_0,                   (SN-A8)

with every other slot untouched. In particular the middle phase can be
evaluated pointwise, but its permutation is two actual width-f exchanges.

**Proof.** Let H_all be normalized Walsh on these four slots. Expanding
SN-A6 gives the diagonal phases D_j D_aux on both sides, and the cross
Walsh kernel P_j H_all. The permutation P_j exchanges the set of main
slots with the set of auxiliary slots, so

    H_aux P_j = P_j H_main,
    H_main H_aux = H_all.

D_j commutes with H_aux and D_aux. Substitution in SN-A7 therefore gives
`D_j D_aux P_j H_all D_j D_aux`, exactly SN-A6. Tensoring the one-column
identity proves it for every f. Other query slots are complete spectators.
QED.

For distinct j and l the permutations P_j and P_l are different: an input
address supported only in X_j is sent to Z_0 by P_j and is unchanged by
P_l. Therefore no single common spatial permutation followed and preceded
only by invertible diagonal phases can represent all M_j. Diagonal phases
cannot change the support permutation of a monomial matrix. With m
queries the literal source schedule makes 2m width-f exchanges for this
middle block per pencil. Reusing the two Fourier endpoints does not reduce
that field-move count.

This is a **supplier obstruction**, not a lower bound for the sum of the
queries on a tape machine. A joint algorithm can act on their sum without
materializing every M_j. Nor does one small rectangle prove an Omega(m)
lower bound on the complete large-family normalized invoice. The example
rules out the proposed generic argument that all j dependence remaining
after the shared endpoints is pointwise, or that the existing operation
list has only d_pred poly(D,lambda) field moves.

## 4. A precise replacement lemma worth trying

The simplest unresolved core already has the operator

    Z = sum_(j=1)^m b_j D_j P_j D_j X,                 (SN-A9)

on complete arrays with m distinguished pairs and one auxiliary pair of
width-f fields. Coefficients b_j may depend on the polynomial-size seed
row role but not on the spatial address. All other ranges remain paid
spectators. More general source rectangles add small-support linear
coordinate frames and parity signs of the same type.

A sufficient new supplier would evaluate these joint middle operations,
for the actual source incidence family and both predictor evaluations,
in `V E_addr J(a) log(k+2)^b + V poly(m) log(k+2)^b`, with an absolute
linear payload coefficient, preserved shared recursive call invoice and
effective polynomial-size descriptors. It must aggregate across j before
paying independent full-field movement. Merely enumerating j and applying
P_j reproduces SN-A3. Merely moving the full m-coordinate address at every
query is more expensive. Row arithmetic and scalar preparation alone do
not implement the distinct support permutations in SN-A8.

This isolates the missing joint-address executor without asserting its
impossibility. The finite verifier checks SN-A6--SN-A8 exactly over the
rationals, checks distinct support permutations with all spectator fields
present, and includes omitted-swap/phase negative controls. It does not
certify such a joint executor or a new multiplication envelope.
