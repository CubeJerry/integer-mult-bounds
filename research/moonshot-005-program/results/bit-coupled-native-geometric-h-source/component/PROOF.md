# Geometric fibres with a quadratic-annihilator H word

**Local component theorem; pending independent review. No new kappa.**

The exact GF64 certificate constructs three genuine source stars at
H263={0,61,62}, with quotient width3 and source dimension48 per component.
All actual geometric foreign cuts are invertible, all three genuine early
bases have rank96, and one invertible9-by9 H word gives equal invertible
readouts on every whole H inverse fibre. Its nine exits are actual native
D charts, with a changed allocation relative to the inherited marking.
The remaining36 exits, physical expansion, and full invoice are separate
obligations addressed by a subsequent extension, not asserted here.

## 1. Actual geometry and the changed port set

Work in F=GF(64), represented by the binary polynomial x^6+x+1. Define
q(z)=z^9+z^18+z^36. The checker reconstructs an explicit binary isometry
from H263-perpendicular to this six-dimensional minus quadratic space.
Its28 zeros label the28 source planes, with the centre labelled0.
Every off-centre plane has a nonzero label t. Its source quotient is

    Q_t = (1,t,...,t^15) tensor I_3.

The parameter file gives an explicit basis identifying the same space
with F4^3, where q(r)=r_1^3+r_2^3+r_3^3. The nine singular F4 lines are
actual D radicals, namely

    110,132,720,810,1509,1735,1994,2621,2836.

For each port choose a nonzero singular representative u, and put the
corresponding row of E1 equal to (u_1^2,u_2^2,u_3^2). The row of E2 is
the six quadratic monomials in that E1 row. Their ranks are3 and6.
For each of the36 actual receivers perpendicular to H263, E1*r vanishes
at exactly its three visible ports. This incidence statement is checked
against the native owner geometry, not inferred from abstract counts.

## 2. The quadratic-annihilator construction

Choose nonzero port weights a,b,a+b, using the exact arrays in PARAMETERS.
Let W_c be a three-row basis of the left annihilator of diag(c)*E2, and set

    T = [ W_(a+b) ; W_b ; W_a ],       H = T^(-1).

For a receiver r, define

    A0(r)=diag(E1*r) diag(a) E1,
    A1(r)=diag(E1*r) diag(b) E1,
    A(r)=[A0(r),A1(r)].

Every entry of diag(E1*r)*E1 is a linear combination of the six quadratic
evaluation columns. Hence W_c diag(c) diag(E1*r) E1=0 identically, giving

    T A(r) = [ D0(r) D0(r) ; D1(r) 0 ; 0 D2(r) ],

where D0=W_(a+b)A0, D1=W_b A0, D2=W_a A1. Each D_j is a3-by3 pencil
linear in r. The finite certificate verifies rank(T)=9, rank(D_j(r))=3
for every receiver and donor, and rank(A(r))=6 on exactly the six unseen
coordinates. If H_(i,j) is the visible3-by3 block of H for donor j, the
zero visible rows of A imply

    H_(i,0)D0(r)=H_(i,1)D1(r)=H_(i,2)D2(r).

The common matrix is invertible. To see this without a determinant guess,
the six-dimensional image of A is the complete unseen-coordinate space.
Therefore the visible rows of H annihilate exactly the image of T A.
Since all D_j are invertible, the three-dimensional annihilator of that
image is the graph of the three inverse pencils. Its projection onto
each donor block is an isomorphism. The checker also evaluates all these
equalities and ranks directly.

## 3. Realizing the pencils by literal source quotients

For receiver i, let K_i be the48-by3 kernel of its fifteen visible off-H
quotients. Distinct evaluation nodes give rank45 and exactly this kernel.
Scale K_i by v_i^2, where v_i is the nonzero GF64 label of the receiver in
H-perpendicular. The36 scaled fibres jointly span dimension18.

The construction selects a deterministic basis S of that span and solves
for three3-by48 matrices C_j whose restrictions satisfy

    C_j (v_i^2 K_i) = D_j(r_i), for every i.

All these simultaneous equations are explicitly checked. Thus no unproved
claim about extension of a linear pencil is needed for the finite result.
The geometric explanation is the six-dimensional scalar fibre identity
developed independently in the same session: after scaling, the degree15
kernel polynomial is binary-linear in the receiver vector. The three
coordinates of r are binary-linear as well. This explanatory identity
is not a dependency on an unreviewed external implementation.

An arbitrary recorded3-by30 tail in the annihilator of S is added to each
C_j. This preserves every common inverse fibre while permitting the
actual early source bases to be invertible. The source at donor j uses
C_j at H263 and Q_t at each other source plane. If a receiver does not
see H263, its sixteen distinct evaluation nodes give a full-rank cut.
If it sees H263, the fifteen ordinary quotients have kernel K_i, and
C_j is injective on that kernel because D_j is invertible. The actual
early basis is checked using the frozen source ownership/phase rule,
with early seed0 for each donor.

All three sources also have an explicit sixteen-plane observation of
rank47 instead of48. Consequently they are not Reed-Solomon source
systems up to arbitrary whole-input bijections and separate output
bijections: the number of distinguishable values of that observation is
different. A source gauge alone cannot turn these sources into old RS
information systems.

## 4. Scope, negative controls, and replay

This is a local canonical foreign-identity H construction. H263 contains
neither donor10 nor receiver80's proper star, but that fact does not prove
the S028 perturbed global target. Nothing here constructs common D, K or
facet maps, a complete return, or either strict supplier. All five
foundational assumptions remain.

Deleting a real source quotient loses three ranks. Changing one central
control breaks common readout equality. Equal port weights a=b make the
first annihilator nine-dimensional and invalidate the3+3+3 construction.
These controls check source information, fibre compatibility, and the
essential polynomial construction separately.

Replay with:

    python -B research/moonshot-005-program/results/bit-coupled-native-geometric-h-source/component/check.py --repo REPO --out FRESH

An optional --rank-library may name the unchanged field_rank C accelerator;
default NumPy and accelerated receipts must agree.

## Open next questions

Complete the complementary36-port component and literal original-owner
source/H cost; then move the existing fibres while adjoining a shared
centre. Global port allocation and the D/K/facet compatibility remain
independent constraints. The new quadratic mechanism makes the H provider
adapt to geometric fibres, rather than fixing its previous Vandermonde
coefficients; it gives no automatic connected-centre extension.

Credit @CubeJerry and the pinned native geometry, source ownership and
spread-source authors. S030 root derived the geometric field identity and
the quadratic-annihilator mechanism; Worker A constructed and checked its
literal source and native port realization. Substantial OpenAI assistance.
Independent review is recorded separately.
