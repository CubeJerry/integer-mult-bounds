# Independent review of the all-slot involutive-feedback extension

**ACCEPT the extension under the large-update involution hypothesis.**

At the pinned H263/D110 interface, the universal polynomial port obstruction
extends from the nine-gap reference to an arbitrary16-slot feedback matrix
V whenever every relevant full-source update

    N_i=(c_i tensor I_k)V

satisfies N_i^2=0. This is a condition on the16k-by16k update. A condition
only on the smaller k-by-k matrix V(c_i tensor I_k) is insufficient for the
two-term inverse used here. The independent controls distinguish those
conditions explicitly.

The existing fixed-node, GF64-linear bank-gauge and tight positive-port
scope is retained. All six possible reference/comparison donor choices are
certified. The comparison donor may still be any degree-at-most16 matrix
polynomial source, including a general conditional-feedback source with
invertible full cuts. Arbitrary nonlinear H and downstream computation is
allowed. Arbitrary binary-linear or nonlinear bank gauges, different node
allocations, and three unrestricted conditional references remain outside
the theorem.

## 1. Algebraic normalization, with all matrix orders retained

Let C_i=c_i tensor I_k. Each C_i has full column rank: the scalar vector
c_i is nonzero: if it vanished, then P_i=z^16+1=(z+1)^16, contradicting
the sixteen distinct allowed roots of P_i. Therefore

    (C_i V)^2=0  if and only if  V C_i V=0.                  (1)

The full source view is A_i(I+C_i V), where A_i is the old Vandermonde
tensor I_k. Under(1) its inverse factor is exactly I+C_i V.
At H263, with c=49 and the reference receiver parameter v,

    U(v)=(L_v(z)+L_v(c))/(z+c),
    B(v)=N_c U(v)=v^2 c_i.

Here N_c is scalar multiplication by z+c modulo z^16+1 and must not be
confused with the source update N_i. Thus the complete off-H fibre is

    K(v)=U(v) tensor I_k + C_i V(U(v) tensor I_k)
        =U(v) tensor I_k +(B(v) tensor I_k)v^(-2)A(v),
    A(v)=V(U(v) tensor I_k).

No support restriction is imposed on V. Consequently A(v) may contain
all six Frobenius powers v,v^2,v^4,v^8,v^16,v^32. The central readout is
still d(v)I_k, where d(v)=v^8+c^4v^4. Indeed Q(c)=e(c) tensor I+h(c)V,
e(c)c_i=h(c), and the remaining term after the two h(c)VU terms cancel is

    h(c) V C_i V(U(v) tensor I_k)=0

by(1). This is the additional cancellation required beyond the old VC=0
family. It does not commute any matrix through another matrix.

After multiplying on the right by the scalar v^2,

    Khat(v)=v^2 U(v) tensor I_k +(B(v) tensor I_k)A(v).      (2)

Every entry of (2) lies in the product span of the six Frobenius powers.
Its exact exponent set is

    E21={1,2,3,4,5,6,8,9,10,12,16,17,18,20,24,32,
         33,34,36,40,48}.

It is E18 enlarged by16,24,32. This observation is entrywise and applies
to every width, arbitrary noncommuting V blocks, and every coefficient
extension. It has no generic-eigenvalue or finite-width premise.

## 2. Independent scalar reconstruction

The new checker reconstructs the actual H263 geometry and source blocks
from raw pinned atlas data. It imports no root or author executable. For
each of the six ordered donor pairs r != j it forms the scalar matrix
whose columns are (m,e), m=0,...,16 and e in E21. Its495 off-H rows are

    C_off[(i,p),(m,e)] = a_p^m v_r(i)^e,

with33 native receivers and15 actual off-H planes of the comparison donor.
Appending the12 central D110 audience rows gives a507-by357 matrix C.
The right side b is zero off H and equals

    tau_i=v_r(i)^2 d_r(v_r(i))

on those central rows. All six orientations give exactly

    rank(C_off)=343,  rank(C)=348,  rank([C | b])=349.      (3)

The initial predicted ranks345/349/350 are not used. The larger off-kernel
has dimension14, not12. Its entire basis is

    v^s(z+c)^epsilon U_c(w),
    s in {0,1,2,4,8,16,32}, epsilon in {0,1},              (4)

where v^0 means the constant1 and w is the comparison donor's actual
binary-linear parameter image. The checker constructs all14 coefficient
vectors, verifies all off-H equations, proves their independence, and
provides a nonzero343-by343 minor. This authenticates (4) exactly.
The central values are therefore

    d_j(w) times span{1,v,v^2,v^4,v^8,v^16,v^32}.

Their restriction to the D110 audience has rank5, and adjoining tau gives
rank6. The same six receivers give a nonzero central minor for every pair:

    5,7,53,54,57,74.

The selected columns are d_j(w) times1,v,v^2,v^4,v^8, followed by tau.
For ordered pairs(0,61),(0,62),(61,0),(61,62),(62,0),(62,61), their
6-by6 determinants are respectively33,1,26,14,17,56.

Each case also supplies a literal507-entry dual vector lambda with

    lambda^t C=0,    lambda^t b=1.                       (5)

The supports have193 or196 nonzero entries. These are valid certificate
sizes, with no minimality claim. Exact nonzero minors and explicit kernel
vectors certify the dimensions in(3); (5) directly certifies the
inconsistency needed by the all-width proof.

## 3. Why the scalar identity excludes a nonlinear shared packet

The tight-cut argument is unchanged, but its connection to(2) is stated
here to fix the quantifiers. With complete linear source views and
identity target contributions, each receiver's three residual spaces have
dimension k. Their sum must fit in the visible k-symbol H tuple, forcing
all three residual spaces to coincide. Use the reference physical source
coordinates as the common frame. After arbitrary field-linear input
gauges, the comparison observation is still a matrix polynomial F_j(z)
of degree at most16. It annihilates K(v_i) at every companion off-H node.
Its central value Z_j(i)=F_j(c)K(v_i) is invertible.

A common linear row ell=(ell_r,ell_j,ell_l) in every required H-aggregate
row space for the D110 audience must satisfy

    ell_j F_j(c)K(v_i)=d_r(v_i)ell_r.

The corresponding off-H expressions vanish. Multiply by the scalar v_i^2.
Every coordinate of ell_j F_j(z)Khat(v_i) has exactly the coefficient
form used in C. For each coordinate t of ell_r this yields

    C x_t=b(ell_r)_t.

Applying(5) forces ell_r=0, and invertibility of the other central maps
forces the other blocks to vanish. Thus the common row-space intersection
is zero for every positive width and every allowed parameter assignment.

At exact capacity each visible exit is a full-alphabet function of the
required aggregate, on the same whole H-input domain. A function of all
these linear aggregates is invariant under their kernels and hence their
sum. The zero row-space intersection makes that sum the whole domain,
forcing the D110 packet constant. Its required positive alphabet gives
the contradiction. This step permits arbitrary nonlinear H and subsequent
processing; the field-linearity restriction applies to the source/bank
coordinate maps, not to the packet encoder.

Restriction of scalars from a finite extension F to GF64 enlarges the
matrix width and preserves all geometric coefficients and equations.
Consequently arbitrary GF64-linear whole-bank mixing of extension
coordinates is included. F2-linear mixing that does not preserve the
GF64 scalar action is not included.

## 4. Controls that test the enlarged hypothesis

A concrete width3 reference sets V_0=E01 and V_3=E20, all other slots zero.
These blocks do not commute: V_0 V_3=0 while V_3 V_0=E21. All63 large
source updates satisfy N_i^2=0 and have the stated two-term inverse.
In contrast to the old square-zero-support family, V C_i is nonzero in
all63 views. The v^8 and v^16 amplitude coefficients are both nonzero.
All36 whole off-H fibres and central readouts are verified.

A second control replaces V_3 by E10. For every one of the63 source views,
the smaller matrix V C_i still squares to zero, but the larger update
C_i V does not. Its correct inverse is I+N_i+N_i^2. Using the invalid
two-term formula breaks the central readout at35 of the36 actual H
parameters. Thus the check rejects precisely the tempting but incorrect
weakening of(1). This control is a valid conditional source outside the
reviewed hypothesis; it is not an H construction or an obstruction to
that remaining class.

The three same-donor comparison controls retain the explicit solution
v^2 U_c(v)(z), and perturbing a nonzero coefficient of any dual witness
breaks its annihilator identity. These controls supplement the symbolic
argument; they do not replace its all-width tensor lifting.

## Replay and attribution

    OPENBLAS_NUM_THREADS=1 python -I -B research/moonshot-005-program/results/bit-shared-h-s031-review/involutive-feedback-extension/check.py --repo REPO --out FRESH

Receipt:

    PASS_ALL_SLOT_INVOLUTIVE_FEEDBACK_EXTENSION 6 343 348 349 110

The package leaves the accepted E18 proof and evidence unchanged. Root
proposed and first computed the all-slot involutive extension; worker C
independently verified its algebraic scope, rebuilt all six scalar systems,
proved the14-dimensional kernel description and supplied the strict
large-versus-small involution controls. The retained geometry, source and
tight-cut authors are credited. Substantial OpenAI assistance. No new
return tariff, complete global word, caller invoice or kappa is claimed.
