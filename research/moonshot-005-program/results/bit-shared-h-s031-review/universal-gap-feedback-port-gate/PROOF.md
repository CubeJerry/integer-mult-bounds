# Universal square-zero polynomial-feedback port obstruction

**Exact source-specific obstruction, with a scalar certificate that lifts to
all matrix widths. No new return tariff, complete caller, or kappa.**

At the fixed global-node H263 interface, a shared positive D110 packet is
impossible if **any one** of its three donors uses the nine-gap feedback
family, even when the comparison donor uses an arbitrary matrix polynomial
source of degree at most16. Arbitrary independent GF64-linear whole-bank
input gauges and arbitrary nonlinear H/downstream processing are allowed.
All six ordered reference/comparison donor choices have separate exact
certificates. Binary-linear input gauges outside GF64-linearity and changed
node assignments are outside this result.

## 1. Fixed interface and source hypotheses

Let F0=GF(64), with binary modulus x^6+x+1, and let F/F0 be any finite
extension. H263 has donors0,61,62 and global node c=49. The pinned root
atlas gives33 native receivers seeing H. None is receiver80 and none of
these donors is donor10, so the relevant foreign target blocks are identity
maps. D110 is an actual H exit, seen by the12 native receivers

    5,7,53,54,57,58,74,75,96,97,98,99.

At width k divisible by15 the donor bank is F^(16k), its quotient at each
node has width k, H receives3k symbols, and each of its45 exits has k/15
symbols. A receiver sees15 exits, totaling exactly k. The physical
bank3840 instance has k=240,720 original early owners at H,16 fields in
D110, and240 visible fields at every receiver. The checker reconstructs
these facts from the raw owner routes, including source identity and phase.
For the width3/nine-selected-port component, the same argument applies
whenever those selected ports give the stated tight3-field cuts and D110
has one positive field; no such alternative invoice is inferred here.

Fix a reference donor r among0,61,62. Before its separate whole-bank gauge,
its quotient at node a is

    Q_r(a)=e(a) tensor I_k + h(a)V,
    e(a)=(1,a,...,a^15),       h(a)=a^16+1.

The k-by16k matrix V has arbitrary k-by-k blocks in
G={3,6,7,9,10,11,12,13,15}. We also permit a tenth arbitrary block by
allowing V_5=V_14, with V_0=V_1=V_2=V_4=V_8=0. Thus the theorem includes
all nine-gap feedback and this explicit larger square-zero family. None
of these matrices has to commute with any other matrix.

A comparison donor j != r may have any k-by16k coefficient matrices in a
polynomial Q_j(z) of degree at most16. Its ordinary source cuts must satisfy
the original complete-source contract. In particular it may be any member
of the conditional all16-slot feedback family, with all required small
source matrices invertible. This is a hypothesis on the **comparison**
donor; the reference must retain the stated square-zero support. The third
donor needs only the same linear full-source/tight-cut conditions.
Separate invertible output relabelings do not alter any source fibre and
can be absorbed into the subsequent encoders.

## 2. Reference fibre and its scalar feature space

For the actual receiver parameter v at donor r, put

    L_v(z)=v z^8+v^2 z^16+v^4(z^14+z^5)
           +v^8 z+v^16 z^2+v^32 z^4,
    U_c(v)(z)=(L_v(z)+L_v(c))/(z+c).

The16 coefficients of U are linear combinations of v,v^2,v^4,v^8,v^16,
v^32. On each actual source cut, U_c(v) is v^2 times the monic polynomial
on the fifteen off-H nodes. Let N_c be multiplication by z+c modulo
z^16+1 and B_c(v)=N_c U_c(v). If c_v denotes the lower16 coefficients of
the monic full-source polynomial P_v+1, then

    B_c(v)=v^2 c_v.

The lower coefficient support of c_v is {0,1,2,4,5,8,14}, with equal
coefficients at5 and14. Hence V(c_v tensor I)=0 and V(B_c(v) tensor I)=0.
The full-source view is a Vandermonde times I+(c_v tensor I)V, whose inverse
is itself. This is an exact square-zero identity at every width.

Set A(v)=V(U_c(v) tensor I_k). The coefficients of v^8 and v^16 vanish:
those parts of U are respectively1 and z+c, and V_0=V_1=0. Therefore

    A(v)=v A_1+v^2 A_2+v^4 A_4+v^32 A_32,

for four possibly noncommuting matrices. The whole off-H fibre has basis

    K(v)=U_c(v) tensor I_k
          +(B_c(v) tensor I_k) v^(-2) A(v).

Only a nonzero field scalar is inverted. No matrix inverse is commuted
past A or a gauge. Its H readout is

    Q_r(c)K(v)=d_r(v)I_k,      d_r(v)=v^8+c^4v^4 != 0.

Indeed e(c)U=d_r, e(c)B=v^2 h(c), V B=0, and the two h(c)A terms cancel.
Multiplying the fibre basis on the right by the scalar v^2 gives

    Khat(v)=v^2 U_c(v) tensor I_k + (B_c(v) tensor I_k) A(v).       (1)

Every scalar entry of Khat is in the18-dimensional function space

    E=span_F {v^e : e in E18},
    E18={1,2,3,4,5,6,8,9,10,12,17,18,20,33,34,36,40,48}.          (2)

To see this, multiply the six Frobenius powers occurring in U and B by
one of v,v^2,v^4,v^32. Their exponent sums give exactly E18, using v^64=v.
The v^2 U term is already included. The33 actual reference parameters
have evaluation rank18 for each of the three choices of r. Matrix entries
and products can be arbitrary: (2) is an entrywise scalar span statement.

## 3. Exact scalar equations and certificates

For an ordered pair r,j, let v_i be receiver i's parameter at r and w_i
its parameter at j. For each of the33 receivers and each of the15 actual
off-H planes p at j, impose a scalar equation on coefficients x_(m,e):

    sum_(m=0..16,e in E18) a_p^m v_i^e x_(m,e)=0.                (3)

There are495 rows and306 columns. Call this matrix C_off. Its rank is298.
Its entire eight-dimensional kernel is the coefficient space of

    v^s (z+c)^epsilon U_c(w),  s in {1,2,4,32}, epsilon in {0,1}. (4)

These expressions are functions on the33 actual paired parameters.
The exact binary parameter map w=Jv is reconstructed from those pairs.
It makes every coefficient in (4) belong to E. The checker verifies the
eight independent coefficient vectors and all495 annihilation equations,
then supplies a nonzero298-by298 minor. Thus (4) is an exact description
of the kernel; no untested genericity claim is involved.

At z=c the epsilon=1 terms vanish. Consequently all possible central
value vectors of (3) are

    d_j(w_i) times span_F {v_i,v_i^2,v_i^4,v_i^32}.               (5)

For the12 D110 audience receivers, append the central rows a_p=c to
C_off and call the507-by306 matrix C. Define b by zero on the495 off-H
rows and by

    b_i=tau_i=v_i^2 d_r(v_i)

on the12 central rows. For **each of the six ordered pairs** r != j,

    rank(C_off)=298,       rank(C)=302,       rank([C | b])=303. (6)

The literal output includes a scalar vector lambda with507 entries such
that

    lambda^t C=0,          lambda^t b=1.                        (7)

It also includes nonzero minors and a five-receiver central witness:
the five columns [d_j(w)v,d_j(w)v^2,d_j(w)v^4,d_j(w)v^32,tau]
have a nonzero5-by5 minor. The support count of lambda is a certificate
size, not a claim of minimum support. Row order is increasing receiver,
then increasing companion plane, then increasing D110 audience; column
order is z-degree followed by the listed feature exponent.

Equations (7), rather than a floating-point rank report, are the direct
certificate used below. They hold in F0 and remain valid over every field
extension. They apply separately to every entry of any matrix-valued
polynomial in the allowed scalar feature space.

## 4. From a hypothetical completion to the forbidden equations

Write the separate field-linear bank gauges as G_l. The physical source
input at donor l is G_l x_l. Fix a receiver i. Its fifteen off-H source
observations leave a k-dimensional affine uncertainty at each donor.
Their identity-target sum has dimension at least k. The visible H packet
has exactly k symbols, so exact decoding forces the three residual linear
spaces in target coordinates to be equal. Otherwise their sum would have
more than |F|^k values. In the reference coordinates this common space has
basis K(v_i).

For a comparison donor j define the matrix polynomial

    F_j(z)=Q_j(z) G_j G_r^(-1).

Its degree remains at most16, and its coefficients are otherwise arbitrary.
Alignment of the entire off-H fibres gives

    F_j(a_p) K(v_i)=0

for every off-H companion plane p. Its central matrix
Z_j(i)=F_j(c)K(v_i) is invertible because the companion's complete16-node
source view is invertible. Let y_l be the actual H input from donor l.
The required aggregate, in the common residual-fibre coordinates, is

    d_r(v_i)^(-1) y_r + Z_j(i)^(-1)y_j + Z_l(i)^(-1)y_l.        (8)

As the three source uncertainties vary, the same whole H-input domain
F^(3k) is obtained for every fixed side-information choice. Exact capacity
makes the visible H tuple a bijective function of (8): each aggregate has
at least one tuple, there are |F|^k aggregates, and only |F|^k possible
tuples. Hence every individual visible exit is a function of (8), has
its full alphabet, and is independent of the choice within its kernel.
The H encoder is fixed, so this statement holds on the same full domain
for every receiver seeing that exit. Arbitrary nonlinear H encoding is
permitted in this argument.

Consider any common F-linear row ell=(ell_r,ell_j,ell_l) in the row spaces
of (8) for all12 receivers seeing D110. Equating its three block
coefficients implies

    ell_j F_j(c)K(v_i)=d_r(v_i) ell_r                     (9)

for every audience receiver. Also ell_j F_j(a_p)K(v_i)=0 on every off-H
companion node, for all33 receivers. Multiply these equations on the right
by the scalar v_i^2 and use (1). Each entry of

    ell_j F_j(z)Khat(v_i)

is a polynomial in z of degree at most16 with its coefficients in E18.
Therefore, for every coordinate t of the row ell_r, its scalar coefficient
vector x_t satisfies exactly

    C x_t=b (ell_r)_t.

Apply (7). Its left side becomes zero and its right side becomes
(ell_r)_t. Thus ell_r=0. Equation (9) and invertibility of Z_j(i) then
give ell_j=0; the third block of (8) similarly gives ell_l=0. The common
row-space intersection is zero.

A function of every linear aggregate (8) is invariant under every one of
their kernels, hence under the sum of those kernels. The annihilator of
that sum is the intersection of the row spaces, now zero, so the sum of
kernels is F^(3k). The shared D110 packet must therefore be constant.
This contradicts its full alphabet |F|^(k/15)>1. This proves the theorem.

This argument uses no common amplitude ansatz and no simultaneous
triangularization. It never rewrites T^(-1) A T as A. The reference basis
has the scalar normalization (1); all noncommuting coefficients on the
comparison side are simply unrestricted unknowns in the scalar relaxation.
The contradiction is consequently uniform over all positive admissible k,
all reference feedback choices, and all comparison coefficient matrices.

## 5. Extensions, controls, and precise boundaries

Arbitrary GF64-linear whole-bank gauges over a finite coefficient extension
are covered by restriction of scalars: width k over F becomes width
k[F:F0] over F0. Every geometric coefficient is in F0; the reference
feedback, comparison polynomial, and bank gauges become matrices over F0.
Equations (1)--(9) apply without any scalar-action assumption beyond
GF64-linearity. They do not establish the result for merely F2-linear
input gauges or arbitrary nonlinear bank bijections. In particular, this
package does not reuse the earlier gap15 nonlinear affine-reduction lemma
for the present nonadditive reference-fibre diagram.

The source hypothesis is asymmetric, but the finite certificate covers
all six orientations. It excludes having **any** donor in the stated
square-zero family when either comparison donor has the degree16
polynomial form. It therefore excludes three arbitrary nine-gap donors,
and also mixtures with one nine-gap donor and conditional all16-slot
companions. It does not exclude three conditional all16-slot reference
sources. Such a reference has a genuinely matrix-valued inverse in its
fibre basis, and the E18 normalization used here need not hold.

The allowed node coordinates are the pinned global assignment, common to
the donors. Independent donor-specific relabelings, degree-greater-than16
comparison maps, changed demand/route interfaces, and additional paid
informative channels require separate analysis. No quantitative excess
return or minimum repair price follows from the zero-intersection result.

The checker supplies three classes of controls. For each reference donor,
comparison with that same donor has the explicit solution
F(z,v)=v^2 U_c(v)(z), showing that the cross-donor geometry is essential.
Changing one nonzero coefficient in each dual certificate makes its
annihilation equation fail. A genuine width3 noncommuting reference with
V_3 a cycle, V_6=E00 and V_5=V_14=E12 passes all63 square-zero source
inverse identities and the full off-H/readout checks. In contrast, a lone
unsupported V_14=I makes the v=1 full-source matrix have rank45 instead
of48. These finite controls authenticate the implementation; the all-width
proof is the square-zero algebra and scalar tensor lifting above.

## Replay and provenance

    OPENBLAS_NUM_THREADS=1 python -I -B research/moonshot-005-program/results/bit-shared-h-s031-review/universal-gap-feedback-port-gate/check.py --repo REPO --out FRESH

Expected receipt:

    PASS_ALL_ORIENTATIONS_UNIVERSAL_GAP_PORT_GATE 6 298 302 303 110

The checker imports no predecessor executable. It reconstructs actual
roots and incidences, uses polynomial-basis finite-field arithmetic, and
checks exact minors and annihilator identities. The polynomial/source and
atlas proofs are credited and pinned as inputs. Credit @CubeJerry and the
retained S030 geometric-node, global-allocation, polynomial-feedback and
tight-cut authors. S031 worker C derived the scalar polynomial relaxation,
its exact central kernel and the all-width port contradiction. Substantial
OpenAI assistance. Programme admission requires independent review.
