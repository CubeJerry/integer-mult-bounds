# Actual nonlinear ordinary controls transported through the source square

**Constructive interface theorem, pending independent review. No complete caller.**

Let the source be A=C_b S, with the exact admitted square A²=C_a C_b R2.
For an arbitrary Boolean table f on four bits define D_f=diag((-1)^f) and
H_f=A^-2 D_f A². Then H_f is a root-four monomial unit if and only if, on
each fixed(c,d) fibre, f is affine in(a,b):

    f(a,b,c,d)=g0(c,d)+a g1(c,d)+b g2(c,d)  over F2.            (1)

There are exactly8^4=4096 such tables. Their ordinary involutions H_f commute,
H_f H_g=H_(f+g), and satisfy the actual source-transport identity

    a² H_f^(tensor V)=D_f^(tensor V) a²                     (2)

for every positive width V, with every phase retained. This family includes
conditional nonlinear address permutations, not only constant Pauli controls.

## Explicit physical monomial

Write R=R2. At z=(a,b,c,d), put epsilon=g0(c,d), r=g1(c,d), s=g2(c,d).
The middle monomial M_f in H_f=R^-1 M_f R has the exact action

    |a,b,c,d> -> (-1)^epsilon i^(r+s) (-1)^(ra+sb)
                 |a xor r,b xor s,c,d>.                   (3)

Indeed C_j^-1 Z_j C_j=Y_j=i X_j Z_j, and r,s do not involve the target bits.
If R maps x to z with phase rho_x and maps x' to the flipped z, the complete
input phase of H_f is rho_x times the phase in(3) times conjugate(rho_x').
This gives a literal16-address table and H_f²=I, without a Gaussian call.

Each two-bit Boolean control has an algebraic normal form with at most four
terms. The two flips therefore use at most2 unconditional X,4 CNOT and2
Toffoli gates. One fixed16-entry root-four phase pass implements the full
phase in(3), before the flips. R and R^-1 each use the retained two coordinate
SWAPs, one Toffoli and one phase pass. A conservative complete H_f recipe is
thus4 coordinate SWAPs,2 X,4 CNOT,4 Toffoli and3 phase passes. All actual
width-dependent scalar/control/tape/precision/compiler costs remain charged.
The inverse uses the same involution recipe. This is a finite paid service,
not a new free oracle.

The phase pass is input-indexed, with exponent

    2 g0(c,d)+g1(c,d)+g2(c,d)
        +2 a g1(c,d)+2 b g2(c,d)  modulo4.                (4)

It is applied before the two conditional flips. On a tensor address
`(x_1,...,x_V)` the phase is the product of the V one-column phases, namely
`i^(sum_j exponent(x_j))`; each R2 wrapper uses the same input-indexed rule
for its own current address. Thus a constant one-column factor i becomes
i^V, and a constant sign becomes(-1)^V. No even-width identification is
used. The controlled-Y core is literally an involution: on an exchanged
pair its two exponents sum to0 modulo4. Conjugation by R2 preserves that
fact, so the identical complete H_f recipe implements both directions.

Per forward **or** inverse H_f application the bound is4 coordinate SWAP,
2 X,4 CNOT,4 Toffoli and3 phase services. A forward/inverse pair therefore
uses at most8,4,8,8,6 of these services respectively. It introduces no ADD,
dyadic denominator, Gaussian query or additional whole-field owner. Each
phase service performs at most one root-four scalar operation at each
stored address, while its descriptor, columnwise exponent calculation,
layout, traversal, tape and precision work remain charged by the retained
fixed-table compiler. Equivalently one may compile the resulting fixed
sixteen-address monomial table as a single service with its complete
retained tariff; the gate list is a constructive upper bound, not a free
implementation of that service. All prefixes have Euclidean and coordinate
maximum-norm bound1, since every gate and phase is a unit-phase monomial.

## Necessity

Fix(c,d). Conjugation by C_a C_b is, up to actual monomial row/column phases,
the two-bit Walsh transform conjugating the four diagonal signs. The resulting
matrix has one nonzero entry per row precisely when those four signs form a
Walsh character, equivalently when f on this fibre is affine. A non-affine
two-bit Boolean function is ab plus an affine function; all four of its Walsh
coefficients are nonzero. Its conjugate has four nonzero entries per row and
cannot be monomial. Since R is monomial and preserves this distinction,
(1) is necessary and sufficient. The checker verifies the sixteen possible
fibre tables exactly, but the Fourier-character argument is the general proof.

At the tensor level, a nonmonomial H_f cannot equal one fixed finite ordinary
tensor-word template at every sufficiently large width: the retained faithful
finite-unitary tensor separation distinguishes H_f from every ordinary
monomial projective class. No claim is made that a width-one linear span test
alone distinguishes them.

## Actual all-width bank routes

For any admitted H_f, its two complementary projectors P±=(I±H_f^tensor V)/2
are actual ordinary operators. Given any pair of scalar bank permutations
(or scalar matrices) B+,B-, define

    Q_H=B+ tensor P+ + B- tensor P-.

If B± are invertible then Q_H^-1=B+^-1 tensor P+ + B-^-1 tensor P-, at every
positive width. In particular conditional bank swaps are involutions. Equation
(2) transports the same route through the source square when the square acts
on each routed bank.

When the two fixed GL3 sector matrices have a common determinant, the retained
cyclic-unit theorem supplies at most108 whole-field ADD,217 fixed-scalar SCALE
and108 H_f monomial services per forward or inverse application, with no new
whole-field owner. The final SCALE can be omitted at common determinant1.
These are conservative upper bounds and every service remains charged.

A conditional bank swap has an explicit much smaller recipe even though its
two sector determinants differ. For the two banks x,y apply chronologically

    x += y;
    y *= -2;
    y += x;
    apply H_f^(tensor V) to y;
    x += y;
    x *= 1/2;
    y *= -1;
    y += x.                                               (5)

It sends `(x,y)` to `(P+ x+P- y,P- x+P+ y)`. Thus each direction of this
involutive route uses exactly4 ADD,3 SCALE and1 H_f service; the third bank
is untouched. The two dyadic scalings are exterior operations, not tensor
powers of the scalars. There is no initialized bank or copied whole field.
The schedule has fixed width-independent amplification constants; a crude
product bound on prefix norms in the coordinate maximum norm is32. A
forward/inverse pair uses8 ADD,6 SCALE and2 H_f services. Other sector
matrices with unequal determinants still owe a separate actual compilation
argument; the inverse formula alone does not provide it.

This provides a larger constructive second-interface family after the new
coherent-diagonal-Q obstruction. It does not show that any member completes
independent(4,2,1), nor that its entire physical invoice is profitable. The next
step is a source-valid Q_H (or noncommuting composition of such units) that
simultaneously preserves the rank-four component and supplies exactly one
rank-two and one rank-one independent endpoint. All five foundations remain.

Credit @CubeJerry and retained source-square, arbitrary-Boolean rank-one
conjugation, cyclic-unit and ordinary-compiler contributors; Worker B with
substantial OpenAI assistance. Universal proof and finite controls are separate
from independent review. No new kappa.
