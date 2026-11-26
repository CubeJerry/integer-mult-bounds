# Independent review of the CRT caller and canonical carry interface

Decision: **accept UC4--UC6's conditional packing/precision transfer and
KC1--KC7's exact carry identities in their stated scopes**. The binary
CRT and carry-time suppliers remain open. This is not a proof of the
desired multiplication bound or a lower bound on alternative CRT methods.

I read the complete `../route-a/unramified-polynomial-crt-caller.md`,
with this review focused on its integer caller, precise local lifting
recurrence and absolute visited-space composition. I also read the
complete `../lead/carry-remainder-interface.md`, first independently
reconstructing the b=2 integer matrix. The separate C review owns the
external finite-field generation/normal-basis imports and full FS1
setup audit. I checked the compact directory clarification in FS1.
Reviewed frozen hashes are recorded in the independent receipt.

## 1. Integer packing and exact output

Let B=ceil(log2(n+2)), h=ceil(n/B), 2h<=q=2^b<4h, and let H be the
least power of two at least 2B+ceil(log2(h+1))+2. Then
b=Theta(log n), H=Theta(log n), qH=Theta(n), and b<=H<=8b eventually.
The finite exceptional range may use the stated correct fallback.

Input digit polynomials have degree at most h-1. Their product has
degree at most 2h-2<q, and every coefficient is below
h(2^B-1)^2<2^H. Therefore reconstruction modulo the ACTUAL monic
product P returns that ordinary product modulo 2^H without polynomial
wraparound. The bound on the nonnegative coefficients then recovers
them exactly. This reasoning does not require P=X^q-X over Z/2^H.

The final integer carry fits the invoice. More precisely, if an incoming
carry is at most h(2^B-1), then adding a coefficient at most
h(2^B-1)^2 and shifting by B preserves that bound. The initial carry
is zero. Thus H+O(1) working bits suffice, and the sequential scan,
reversal and exact 2n-bit output formatting fit O(qH). The inverse
transform must return increasing coefficient order, as explicitly
required in UC.

The two forward transforms, one inverse and small component products
are all separately present in UC2. The proved component products use
only O(b^2)-bit integer calls; monic reversed-polynomial Newton division
uses no inverse of 2. Full product-tree or global CRT constants remain
inside the open transform gate, avoiding a circular n-bit multiplier
call in the proved local part.

## 2. Canonical precision lifting

Put Q=2^t and write every 2t-bit coefficient canonically as F_0+Q F_1.
The actual remainder transform is linear modulo Q^2, so

    E_(2t)(F)=E_t(F_0)+Q[K_t(F_0)+E_t(F_1)] mod Q^2.

The displayed E_t(F_0) is its canonical low-digit representative. This
proves UC5b with two t-bit forward calls and one forward carry map.

For inversion, F_0=E_t^(-1)(Y_0) is canonical. Its image modulo Q^2
has low part Y_0 and high part K_t(F_0). Applying E_t^(-1) to
Y_1-K_t(F_0) supplies F_1. Therefore the SAME forward K_t suffices;
there is no assumed inverse-carry oracle. Arbitrary alternative lifts
would add an unaccounted high digit, so UC's canonical convention is
necessary and correct.

For either direction the actual invoice is

    T(q,2t)<=2T(q,t)+qt D(b,t)+O(qt).

Dividing by 2qt leaves T(q,t)/(qt) plus half the carry/scan allowance.
Iterating yields UC6 up to absolute constants. Its endpoint condition
D(b,t)=O(1+sqrt(t)) has a dyadic sum O(sqrt(H)); when H=Theta(b),
the stated qH sqrt(b) bill follows. A precision-independent
sqrt(b) polylog(b) carry allowance instead incurs the displayed
additional O(log b) depth factor. These are conditional transfer
statements about specified local maps, not supplied algorithms.

The two recursive calls are sequential. At each active descent their
bit volume is half the parent volume, so a fixed number of parked
parent streams has a geometric sum bounded by an absolute multiple
of qH. Siblings reuse their work intervals. FS1 now gives a shared
O(q)-bit compact directory: unary degree 1^d0 followed by d+1 binary
coefficients takes 2d+2<=4d bits per factor, and sum d_i=q. This
fits the binary base supplier's O(q) space convention. Optional
H-bit-expanded factors must instead be charged once as shared qH
storage; they cannot be silently read as a local O(q)-bit list.

## 3. The first carry is quadratic with a lift-dependent linear term

Monic integer division defines the literal integer remainder matrix A.
Let E=A mod2 and D=(A-E)/2 mod2. For Boolean x, each row's low-bit
contributions have ordinary count s. The high bit floor(s/2) mod2 is
binom(s,2) mod2. The 2D contribution is linear. This proves

    K_1(x)=D x+sum_(i<j)(E_i odot E_j)x_i x_j.

No nonnegative-coefficient assumption is used; all high bits refer to
canonical residues modulo 4. Polarization cancels the linear term and
produces the off-diagonal pair sum. The diagonal of
E(u) odot E(v) is exactly E(u odot v), proving KC2.

A supplied XOR circuit lifted to additions computes an integer matrix
C congruent to E modulo2. Its high-bit update is
h_out=h_left+h_right+low_left low_right. Replacing each stored bit by
a fixed two-bit record gives constant physical overhead only when the
original tape schedule is supplied, as KC explicitly requires.

Since A-C is even, its missing high digit is the linear correction
((A-C)/2 mod2)x. The binary matrix E alone does not identify that
correction: A+2R has the same E and changes K_1 by R x. Generation
and physical execution of this particular correction remain paid
obligations. This statement is not a lower bound on their cost.

## 4. Literal four-coordinate reconstruction

I independently divided 1,X,X^2,X^3 by X, X+1 and X^2+X+1 over Z.
In the note's output order this gives exactly

    [[1, 0, 0, 0],
     [1,-1, 1,-1],
     [1, 0,-1, 1],
     [0, 1,-1, 0]].

Its high-coefficient matrix is

    [[0,0,0,0], [0,1,0,1], [0,0,1,0], [0,0,1,0]],

which yields all four KC5 polynomials. F=X and F=1+X distinguish the
actual negative-coefficient remainder from the positive-addition lift
of the same binary XOR map, exactly as claimed.

The separate exact checker covers all 16 Boolean inputs, all 256
polarization pairs and 48 inputs to literal lifted addition circuits
including redundant XOR pairs. It verifies the required correction
for each circuit and rejects the two uncorrected controls. It does
not materialize a large CRT matrix.

## 5. Higher-precision carry identities

For canonical x,y at precision t, put z=(x+y) mod Q and let c_in and
c_out be the ordinary input/output carry vectors in KC6. Both have
entries in {0,1}. On integer representatives,

    x+y=z+Q c_in,
    lift(E_t(x))+lift(E_t(y))=lift(E_t(z))+Q c_out.

Applying A modulo Q^2 and comparing high digits gives

    K_t(z)+E_t(c_in)=K_t(x)+K_t(y)+c_out mod Q.

Here E_t(c_in) is evaluated at full t-bit precision, despite c_in
having Boolean input entries. The cancellation/division by Q is an
integer-representative argument, not inversion of 2 in the residue
ring. At t=1 it recovers KC2 with subtraction equal to addition.

For an integer MATRIX C congruent to A modulo Q, write A-C=Q R.
Their canonical low output digits agree, so
K_t^A(x)=K_t^C(x)+R x mod Q. This is KC7, with the same explicit
generation and execution gate. A merely output-equivalent nonlinear
binary algorithm does not automatically give such a matrix-lift
contract. KC correctly limits its circuit statement.

The higher-precision identities were reviewed algebraically. No broader
high-precision experiment or fast carry construction is claimed.

Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance.
