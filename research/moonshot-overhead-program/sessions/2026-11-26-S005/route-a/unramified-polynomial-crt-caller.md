# A full-rate exact caller through small unramified residue rings

Status: **proved algebraic caller and small-product invoice; fast forward
and inverse CRT remain an open supplier**. This is a different mechanism
from Bell/orbits. The CRT facts are standard; this note gives a precise
volume-preserving alternative interface, not a new multiplication bound.

The only integer multiplication primitive used outside the open gate
has input length O(log^2 n loglog(n+4)), including factor generation;
residue products alone use O(log^2 n) bits. It comes from the
published multitape theorem of
Harvey and van der Hoeven, *Integer multiplication in time O(n log n)*,
Annals of Mathematics 193 (2021), 563--617:
<https://annals.math.princeton.edu/2021/193-2/p04>.
No n-bit multiplication is used as a black box in the proved caller.

## 1. Whole prospective budget before attempting the transform

Let q=2^b and R=Z/2^H Z, with b<=H<=8b for sufficiently large b.
Take all monic irreducibles over F2 whose degrees divide b, and lift
their coefficients literally to 0 or 1 in R. Write them g_i, with
degrees d_i, and put P=product_i g_i. Then

    sum_i d_i=q,  max_i d_i<=b.

The exact forward transform is

    E_(b,H): R[x]_(degree<q) -> product_i R[x]/(g_i),
             F -> (F mod g_i)_i.                       (UC1)

Both sides have exactly qH bits in canonical coefficient encoding.
The complete prospective multiplication invoice is

    3 T_CRT(b,H) + T_generate(b,H)
      + O(qH (1+log(b+2))^2) + O(qH).                 (UC2)

Here T_CRT bounds each direction in the explicitly generated factor
order, including every inverse constant, layout change, read/return
pass and temporary structure. T_generate is actual factor generation.
The hoped-for supplier is

    3 T_CRT+T_generate <= C qH sqrt(b)(1+log(b+2))^c,
    cells ever visited <= C qH.                       (UC-GATE)

Constants must be absolute and effective. Removing the logarithmic
factor gives the corresponding endpoint caller. UC-GATE is **open**;
the note checks that the other bills do not silently defeat it.

## 2. All-input CRT with literal binary factors

**UC1 (full-rate algebra).** The g_i are pairwise comaximal over R[x],
P is monic of degree q, and UC1 is an R-linear isomorphism. It accepts
every independent H-bit coefficient, with no symmetry restriction.

**Proof.** Over F2, x^q-x is squarefree, since its derivative is 1.
Its irreducible factors are exactly the degrees dividing b, proving
the degree sum. Distinct factors have a Bezout identity modulo 2.
Lifting the coefficients gives A g_i+B g_j=1+2C. The finite geometric
sum in -2C inverts 1+2C modulo 2^H, so the ideals remain comaximal.
Polynomial CRT and monicity identify R[x]/P with the product of
quotients. The latter are free R-modules of ranks d_i, hence store
exactly H sum_i d_i=qH bits. QED.

The quotient rings are unramified extensions associated with the
irreducible residue factors. The caller does not build Teichmueller
roots or expand q evaluations into q words of bH bits.

**Lift control.** Generally P is not x^q-x modulo 2^H. For b=2,

    x(x+1)(x^2+x+1)=x^4+2x^3+2x^2+x,

which differs from x^4-x modulo 4. The product-degree guard in UC4
below makes this harmless. A characteristic-two FFT is not thereby
an algorithm for the lifted CRT.

## 3. Independent products use only polylogarithmic integers

Use the published uniform multitape supplier M(t)=O(t log(t+2)).
No global linear-space property of that supplier is needed here:
its local visited-space bound is at most its polylogarithmic-in-n
running time, and the same scratch interval is reused for every call.

**UC3.** Given the factor list and residue streams, their componentwise
products can be formed and reduced in

    O(qH (1+log(b+2))^2) time,
    O(qH)+poly(b,H) cells ever visited.               (UC3)

**Proof.** For degree<d polynomials, pack H-bit coefficients in radix
2^w, w=2H+ceil(log2(d+1))+2. Coefficients of their integer polynomial
product are below d 2^(2H), so no packed digits overlap. The integer
operands have O(d(H+log(d+1)))=O(dH) bits; unpack and reduce modulo
2^H. For monic division reverse g_i, whose constant coefficient is
one. Newton power-series inversion u<-u(2-fu) doubles the correct
coefficient prefix over any commutative ring; it never divides by 2.
There are O(log(d+2)) stages and each uses products of at most O(dH)
bits. This safe invoice is O(dH log(dH+2) log(d+2)), including inverse
preparation, reduction, scans and return passes.

Since d_i<=b, H<=8b, and sum_i d_i=q, sum these bills to get UC3.
All integer calls have size O(bH)=O(b^2). Retain a constant number
of complete qH-bit input/output streams and reuse local factor,
inverse, product and multiplier work regions. Their maximum size
is polynomial in b,H and is eventually absorbed by qH. QED.

Thus at b=Theta(log n), the product bill is
O(n(1+loglog n)^2), smaller than n sqrt(log n). There is no call on
an n-bit integer hidden in this claim. The large polynomial P and
CRT inverse constants are not assumed precomputed by UC3.

## 4. Integer packing, coefficient guard and output

For n-bit inputs let B=ceil(log2(n+2)), h=ceil(n/B), and choose
q=2^b with 2h<=q<4h. Choose

    H=least power of two >=2B+ceil(log2(h+1))+2.       (UC4a)

For all sufficiently large n, b<=H<=8b and qH=Theta(n).
Use direct multiplication for the fixed exceptional initial range.
Expand the inputs as X(2^B),Y(2^B), where X,Y have degree<h and
integer coefficients in [0,2^B). Pad their coefficient streams to q
positions, with H bits per coefficient. All writes and counters
cost O(qH) steps and an absolute O(qH) visited-space coefficient.

The ordinary polynomial product Z=XY has degree<2h-1<q, and

    0<=Z_j<=h(2^B-1)^2<2^(2B+ceil(log2(h+1)))<2^H.   (UC4b)

Apply UC1 to X,Y, multiply the residues by UC3, and invert UC1.
Because deg Z<q, its representative modulo actual P is precisely Z
modulo 2^H. UC4b makes its canonical residues the exact nonnegative
integer coefficients. In increasing j order, add the incoming carry,
emit the low B bits and shift the remaining carry by B. The carry is
bounded by a constant multiple of h 2^B, so H+O(1) working bits
suffice. This final scan costs O(qH); remove leading zero output
padding and return the required 2n-bit product format in O(n) time.

The inverse supplier must return this coefficient order. A result in
factor order, random-access memory, or a redundant field evaluation
format is not the UC-GATE interface. Two forward calls, one inverse,
factor generation, small products and every read/write pass are exactly
the terms in UC2. Fixed supplier tapes and constant complete arrays,
plus reused local work, yield absolute O(n) visited cells if UC-GATE
holds. Therefore UC-GATE implies the stated polynomial-loglog
multiplication target; its version with c=0 implies the endpoint.

## 5. Generation and the classical product/remainder-tree invoice

The factor stream is not an oracle. A completely explicit fallback
enumerates candidate monic binary polynomials of the required degrees,
tests irreducibility by modular Frobenius/gcd calculations, and writes
accepted 0/1 factors. This gives q poly(b) time and polynomial local
workspace, but its polynomial factor is not certified below UC-GATE.
The actual generation cost remains an explicit term in that gate.

A relevant primary lead is Bshouty--Diab--Kawar--Shahla, *Enumerating
all the Irreducible Polynomials over Finite Field* (2016), section 2:
<https://arxiv.org/abs/1602.05032v3> and
<https://www.wseas.org/multimedia/journals/computers/2016/a405805-092.pdf>.
It gives deterministic polynomial preprocessing and soft-O(d^2)
delay by Lyndon words, normal bases and products of conjugates. With
O(2^d/d) degree-d factors, this suggests soft-O(qb) total arithmetic
work. The companion `binary-factor-stream-compiler.md` now proves
a sufficient actual tape schedule: it imports only polynomial-size
field/normal-basis preprocessing, uses slower scanned Duval words,
and explicitly packs the small products of conjugates. Its FS1 bill
is q b polylog b+poly(b), with reused local workspace. Since
H=Theta(b), this is affordable even at the endpoint after enlarging
the fixed cutoff. Its independent review is recorded separately;
no q-element list of full bH-bit field values is introduced.

Ordinary balanced product/remainder trees do not supply UC-GATE.
At a level of polynomial degree scale D, total polynomial coefficient
volume is O(qH). Kronecker multiplication of one pair of D-degree
polynomials costs an actual M(O(D(H+log D))) bit operation bill.
Here log D<=b<=H, so the scalar bit size is O(DH). With the published
M(t)=O(t log(t+2)), a complete level is billed at
O(qH log(DH+2)); summing O(b) degree levels gives the familiar safe
O(qH b^2) product/remainder bill, before separately verifying inverse
constants and the retained-space schedule. Keeping every tree level
would itself use O(qH b) cells and is not allowed by UC-GATE.

In particular the upper levels include multiplications on Theta(qH)
bits. They cannot be supplied for free, and substituting the desired
n-bit multiplication theorem there would be circular. This note's
proved UC3 has no such calls. Any full-size product P, Bezout constants,
reciprocal trees, regenerated nodes and conversions needed by a new
transform belong to T_CRT+T_generate.

The O(qH b^2) figure is an invoice for the classical implementation,
not a lower bound on the structured CRT. Its factors have special
binary residue algebra that a different compiler may exploit.

## 6. A precision-local gate: only the new remainder digits

For t-bit canonical input coefficients F_0, define K_t(F_0) to be
the high t bits of E_(b,2t)(F_0) in each residue coefficient:

    E_(b,2t)(F_0)=lift(E_(b,t)(F_0))+2^t K_t(F_0).   (UC5a)

K_t has qt input and qt output bits. Its input coefficients lie in
[0,2^t); its output is only the newly revealed remainder digits.
The factors are the same literal binary g_i at every precision.
This is a concrete carry-remainder map, not a same-size integer
multiplication request.

**UC5 (forward and inverse precision lifting).** Forward and inverse
CRT at precision t, together with K_t, compute either direction at
precision 2t using two t-bit transforms, one K_t application, and
O(qt) scans/additions. No inverse-carry oracle is required.

**Proof.** For F=F_0+2^t F_1 compute A_0=E_t(F_0), A_1=E_t(F_1).
Output low digits A_0 and high digits

    K_t(F_0)+A_1 mod 2^t.                            (UC5b)

For inversion write Y=Y_0+2^t Y_1. First set F_0=E_t^(-1)(Y_0),
whose forward image has low digits Y_0 and high digits K_t(F_0).
Then set

    F_1=E_t^(-1)(Y_1-K_t(F_0)),
    F=F_0+2^t F_1.                                  (UC5c)

Linearity verifies E_(2t)(F)=Y. All lifts are canonical nonnegative
coefficient representatives; arbitrary lifts without compensating
their high digits would invalidate UC5c. QED.

Let binary forward/inverse suppliers cost q B(b), and K_t cost
qt D(b,t), in the fixed coefficient/factor order. Require absolute
O(q) and O(qt) visited cells, including physical movements and actual
factor/setup access. Doubling gives the positive invoice

    T(q,H)/(qH) <= C B(b)
       + C sum_(t=1,2,4,...,H/2) [1+D(b,t)].          (UC6)

Only half the parent bit volume recurses at a time. Park a constant
multiple of the parent volume and reuse regions; active precision
volumes sum to at most 2qH. Share the factor directory and charge its
generation once. The stated local gates therefore give absolute
O(qH) visited cells.

Two prospective, **unproved**, supplier contracts are explicit:

- B(b)<=C sqrt(b)(1+log(b+2))^c and
  D(b,t)<=C sqrt(b)(1+log(b+2))^c imply polynomial-loglog overhead,
  with one extra O(log b) factor from precision depth.
- B(b)<=C sqrt(b) and D(b,t)<=C(1+sqrt(t)) imply the endpoint:
  H=Theta(b), and sum over dyadic sqrt(t) is O(sqrt(b)).

Both must also pay factor generation. These are gates for binary
remainders and new precision digits, not an import of a characteristic-
two additive FFT. Already modulo 4, the high digit of a sum includes
pairwise carry products; replacing XOR by addition in a binary circuit
does not establish the correct ring homomorphism. The next concrete
test is a compiler for K_t or a joint binary-and-carry schedule, with
all input coefficients retained.
