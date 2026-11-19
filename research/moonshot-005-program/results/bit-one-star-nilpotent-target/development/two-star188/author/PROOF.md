# A native near-minimum fitting with no nonzero flat gauge subsystem

**Status: explicit algebraic construction, not a balanced physical source code.**
The construction has binary coefficients, works over every field of
characteristic two, keeps all 6,470 foreign blocks invertible, and has
`rank(I+B)=9b+188` at `b=5760`. Its retained-canonical repair rank is also188.
Nevertheless it has no nonzero flat vertex-gauge subsystem. Thus a small
additive fitting-rank excess does not force a large canonical input subsystem
on the native111-role graph. This does not establish a new multiplication
exponent or supply either missing recursive caller.

## 1. Pinned native facts and the meaning of flatness

Use the authenticated111 native roots in
`sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json`. Two distinct roles are
foreign when their roots are orthogonal. Let O be this adjacency matrix and
K=I+O. Over the binary field K has rank nine; tensoring with a b-dimensional
identity gives the canonical return space H of dimension9b. Every rank fact
below persists over a characteristic-two field extension.

Choose native receivers a=80 and b0=42, and a common foreign neighbor c=8.
The use of b0 for a vertex distinguishes it from the bank width b. The exact
native census gives

* a and b0 are foreign, with degrees62 and61 respectively;
* c is foreign to both;
* the restriction of K to columns outside N(a) union N(b0) has rank seven;
* its restriction to columns outside {a,b0} has rank nine.

Consequently the canonical row code supported on N(a) union N(b0) is
exactly span(K_a,K_b0). Those rows are independent and supported there,
since a and b0 are adjacent. Also the canonical column code contains no
nonzero vector supported on {a,b0}. The separate exact checker reconstructs
these statements from the integer roots, without accepting a supplied graph.

A flat vertex-gauge subsystem of dimension d means injective linear maps

    Z_i : F^d -> F^b,       B_ij Z_j = Z_i

for every foreign ordered pair(i,j). The injectivity is required at every
role, as it would be for a canonical direct subsystem transported by local
changes of coordinates. This definition permits different embeddings at
different vertices and does not assume a common coordinate subspace.

## 2. Two square-zero receiver stars

Put

    w_a=ceil(b/62),       w_b0=ceil(b/61).

For b=5760 these are93 and95. Choose disjoint coordinate subspaces U_a and
U_b0 of those dimensions. Regard U_a and U_b0 also as the corresponding
injective coordinate matrices. Their columns occupy the final188 internal
coordinates, so the first5572 coordinates are untouched by both images.

For every j in N(a) except b0 choose a w_a-by-b matrix V_a,j satisfying

    V_a,j U_a=0,          intersection_j ker V_a,j = U_a.

Choose V_b0,j analogously, excluding a from the second star. There are enough
slots: (deg(a)-1)w_a >= b-w_a and
(deg(b0)-1)w_b0 >= b-w_b0. Row selectors therefore suffice; no existence
argument over a large field is needed.

At c use especially simple selectors. V_a,c selects the first93 coordinates
of U_b0. V_b0,c selects all93 coordinates of U_a and two coordinates outside
U_a+U_b0. These188 selector rows are linearly independent. Allocate every
remaining coordinate outside the relevant U among the other neighbors,
padding unused rows by zero. This gives the required intersections of
kernels. The full b=5760 allocation is saved in SELECTORS.json.

Set B_ij=I on every foreign block except

    B_a,j  = I + U_a V_a,j,       j in N(a) except b0;
    B_b0,j = I + U_b0 V_b0,j,     j in N(b0) except a.

In particular B_a,b0=B_b0,a=I. Set all diagonal and nonforeign blocks to
zero. Let Delta=B-O tensor I_b. Each modified block is invertible, because
(U_i V_i,j)^2=0 and in characteristic two its inverse is itself. This checks
the whole native fitting mask, not merely a selected source fragment.

The two shears at c do not commute. On the first93 paired coordinates of
U_a and U_b0 they map in opposite directions. Their additive commutator has
rank186. Noncommutativity is an actual feature of the construction, not an
unrestricted-block permission that the example leaves unused.

## 3. Exact rank and repair cost

Write Delta=U V, where U has188 columns supported at the two receiver roles,
and V stacks the two horizontal collections of selector matrices. U is
injective. The column block of V at c has row rank188, so V is surjective.
Thus rank Delta=188.

We need both row and column separation from K tensor I_b. Column separation
follows from the native rank-nine restriction outside {a,b0}: no nonzero
canonical column vector can be supported only at those two roles.

For row separation, suppose v lies in row(V) and in the canonical row space.
It is supported on N(a) union N(b0), so the rank-seven native restriction
implies

    v = K_a tensor alpha + K_b0 tensor beta

for two b-dimensional row vectors alpha,beta. The donor column blocks a and
b0 of V are zero: the cross-star perturbations were deliberately omitted.
Since K has ones in all four positions of this2-by-2 native block, this
forces alpha=beta. At the common neighbor c the canonical expression is
then zero. But V's column block at c has full row rank188, so a row
combination of V that vanishes there has all its coefficients zero. Hence
v=0. Therefore row(Delta) intersects H trivially.

For completeness, if M has rank k, Delta=U V has rank r, col(U) intersects
col(M) trivially and row(V) intersects row(M) trivially, then

    rank(M+U V)=k+r.

Indeed V restricted to ker(M) is surjective; otherwise a nonzero combination
of V's rows would belong to row(M). Thus the image of M+UV contains col(U),
and consequently also col(M). Their direct sum has dimension k+r and is
the whole image. Applying this lemma yields

    rank(I+B) = 9b+188 = 52028,
    rank([H;I+B])-9b = 188.

The return-bank replacement theorem therefore assigns excess h=188, and
the retained-canonical repair theorem assigns the same r=188. This example
does not distinguish their costs; its purpose is to test a proposed
near-minimum rigidity implication.

Every row covector annihilating U_a+U_b0 is fixed on the left by all foreign
blocks. There are5572 such independent covectors. Thus the construction
preserves the first70 common correct rows, and in fact5572, while its input
flatness behaves very differently.

## 4. No positive-dimensional flat subsystem

Suppose a flat family(Z_i) exists. The unmodified two cross blocks imply
Z_a=Z_b0. For j in N(a) except b0, receiver j has its block from donor a
equal to I, so Z_j=Z_a. The reverse equation is

    (I+U_a V_a,j) Z_j = Z_a,

and therefore V_a,j Z_a=0. Intersecting these kernels gives
im(Z_a) contained in U_a. The same argument at b0 gives
im(Z_b0) contained in U_b0. Their embeddings are equal and the two spaces
are disjoint, so Z_a=0. Injectivity forces d=0.

This proof permits arbitrary local changes of basis and arbitrary
non-coordinate embeddings of the candidate subsystem. It does not claim
the absence of common left quotients: Section3 explicitly constructs a
5572-dimensional one. Nor does it say anything about invariant subspaces
of a larger physical realization with additional owners. The statement
concerns the native foreign transfer maps specified here.

## 5. Movement screen and the remaining construction

Conditional on realizing this exact B with the retained balanced proper
stages and an invertible late self-map G, either paid return protocol adds
188 field records at gap eight. The authenticated exact interval budget
then gives

    Q = (4451/8)[1] + (7213/16)[2] +24[4]+(9+188/5760)[8],
    [j]=j^(199/200).

The limiting retained movement room is between
0.01969656595059440726206041677207780408520749 and
0.01969656595059440726206041677207780408588911.
The first successful even paired multiplicity is m=628; m=626 fails the
same strict movement comparison. These are inherited exact movement
screens, not a full ordinary-operation or recursive-caller invoice.

There is no claim that the balanced original-donor H source system realizes
these blocks. The source overlap, early-to-late causality, finite compiler,
precision, erasure, both strict suppliers and complete caller obligations
remain. The matrix construction isolates a concrete algebraic target with
a quantified repair budget and rules out the shortcut of deducing a large
flat canonical subsystem solely from small positive rank excess.

## 6. Verification and credit

Run `python3 -B author/check.py --repo <repo> --out <output>`. The checker
rebuilds all native adjacencies, checks the decisive restricted ranks,
verifies the full5760-coordinate selector coverage and nilpotence, and
computes complete fitting/repair ranks at b=2,3,4,8,62. At b=2,3,4 it also
solves every native gauge equation jointly and obtains zero solution
dimension. The b=62 case checks unequal star widths. Independent random
all-original-X/Y algebraic endpoint controls use the explicit canonical
and correction sums; they are not a physical-network implementation.

Credit the authenticated native/atlas authors and @CubeJerry; the retained
repair and replacement-bank bridges developed by S026 Workers B and C;
and the reviewed saturated-star work for the equality-case distinction.
This construction and proof were developed by S026 root with substantial
OpenAI assistance.
