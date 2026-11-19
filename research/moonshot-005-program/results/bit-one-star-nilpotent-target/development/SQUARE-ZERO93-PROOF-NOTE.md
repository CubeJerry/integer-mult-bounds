# Two square-zero receiver stars with 93 excess dimensions

**Algebraic construction only.** This alternative preserves square-zero
perturbations at every foreign block. Root's one-star construction gives the
same excess with a simpler receiver support and higher nilpotency. The
following construction is not a physical balanced-source realization.

Use the native adjacent pair a=80, b=42, with degrees 62 and 61 and common
neighbor c=8. At internal width n=5760, let S and W be complementary
coordinate spaces of dimensions 5642 and 118. Choose U_a inside W of
dimension 91 and U_b inside S of dimension 2. Their coordinate images can
occupy the final 93 positions, preserving the first 5667 left coordinates.

Across all 62 neighbors of a, distribute every coordinate covector of S
once into the 62*91=5642 rows of V_a,j. Their common kernel is W. Across all
61 neighbors of b, distribute every coordinate covector of W into the
61*2=122 rows of V_b,j, padding four rows with zero. Their common kernel
is S. Both families annihilate their own image spaces.

At c, choose the first two rows of V_a,c to read U_b and map into the first
two U_a coordinates; use 89 additional S coordinates for its other rows.
Choose V_b,c to read those first two U_a coordinates. At the cross edge
choose V_a,b as 91 distinct S covectors and V_b,a as two distinct W
covectors, using unused coordinates. Fill the remaining slots with the
remaining coordinates. The available slot counts make this literal.

Set B_i,j=I+U_i V_i,j at those two receiver stars and identity at every
other native foreign block, with the native zero mask elsewhere. Every
perturbation squares to zero; every foreign block is therefore invertible
in characteristic two. At c the two nilpotent parts have an additive
commutator of rank four.

The horizontal V at c has row rank 93 because its selector rows belong to
the disjoint coordinate sets S and W. Thus Delta=B-O has rank 93. Native
restriction outside {a,b} has canonical rank nine, giving column separation.
Native restriction outside N(a) union N(b) has canonical rank seven, so a
canonical row supported there is K_a tensor alpha + K_b tensor beta.
Its donor-column blocks at a and b are equal. A row combination of V has
those two blocks in row(V_b,a) and row(V_a,b), which are disjoint W and S
coordinate spaces. Equality makes both zero; each cross block has full row
rank, so both coefficient vectors vanish. This proves row separation.
Consequently rank(I+B)=9n+93=51933 and retained-canonical repair rank is 93.

For a flat family B_i,j Z_j=Z_i, the unmodified receiver row at c gives
Z_a=Z_b. Every other reverse star edge is unmodified, so the star equations
place this common embedding in every kernel of both selector families. It
lies in W intersect S={0}. Thus there is no positive-dimensional flat
vertex-gauge subsystem, despite 5667 literal common correct left rows.

There is a sharp lower bound on the **total fixed-image width** in this
two-star family. A constant flat vector survives in the common kernel of
all V_i,j. Eliminating it requires rank at least n in their vertical stack,
whose rank is at most 62 dim(U_a)+61 dim(U_b), hence at most 62t when
t=dim(U_a)+dim(U_b). Therefore t>=ceil(5760/62)=93, attained here. This is
not a lower bound on fitting excess for arbitrary perturbations, or for
constructions in which row/column separation fails and t differs from that
excess.

The native restriction facts were independently checked in the separate
two-star review. This note has not yet received a standalone full selector
replay. It is preserved as a secondary exact construction while the positive
source-module review takes priority. No new multiplication exponent follows.
