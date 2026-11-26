# Generating the binary CRT factor stream within the target budget

Status: **constructive setup lemma; independent review pending**.
This supplies the factor-generation term of the UC caller. It does
not construct the forward/inverse CRT, their global inverse constants,
or the degree-q product polynomial. Those remain inside UC-GATE.

## 1. External primitives and the actual tape claim

Use the deterministic polynomial-time construction of a degree-d
binary field and a normal basis summarized in section 2
of Bshouty--Diab--Kawar--Shahla (2016):
<https://arxiv.org/abs/1602.05032v3>,
<https://www.wseas.org/multimedia/journals/computers/2016/a405805-092.pdf>.
Only polynomial preprocessing is imported. The paper explicitly counts
indexed array operations in its word-enumeration analysis; its delay
bound is not imported as a tape theorem. The schedule below supplies
its own slower, sufficient tape invoice.

Integer multiplication on local words uses the published uniform
O(t log(t+2)) multitape algorithm of Harvey--van der Hoeven (2021),
<https://annals.math.princeton.edu/2021/193-2/p04>.
Its inputs below have O(b^2 log(b+2)) bits. No large integer
multiplication is used to construct the degree-q product P.

**FS1.** For b>=1 and q=2^b, all distinct monic irreducibles over F2
whose degrees divide b can be generated in a fixed deterministic
order on ordinary tapes in

    q b (1+log(b+2))^C + poly(b) steps,               (FS1)

for an absolute C, using poly(b) local visited cells and an output
factor directory of O(q) bits. If coefficients are expanded to H-bit
0/1 words, add O(qH) time and output space. For H=Theta(b), this is
O(qH polylog b), hence eventually below C' qH sqrt(b), with absolute
effective constants after enlarging the initial cutoff.

## 2. Enumeration with physical word movement included

For each d|b, construct K=F2[y]/h_d(y), with h_d monic irreducible,
and a normal basis (alpha,alpha^2,...,alpha^(2^(d-1))). Store its
d polynomial-basis coordinate columns, each d bits. The cited
preprocessing uses polynomially many operations on polynomial-size
data. Even a straightforward fixed-tape simulation remains poly(d),
so summing these finitely many setups remains poly(b).

Use ordinary Duval enumeration of all binary Lyndon words of length
at most d: repeat the current word to length d, remove its trailing
ones and increment the preceding zero, stopping at the terminal word.
The standard procedure generates exactly those Lyndon words once.
Retain only outputs of length d. Implement every symbol/index access
by scanning the O(d)-cell work word; a safe next-word bill is O(d^2),
with an additional polylog(d+2) factor allowed for counters, copy
passes and rewinds. No unit-time random
access is assumed.

There are at most 2^ell/ell Lyndon words of length ell. Splitting
ell<=d/2 and ell>d/2 shows their total for ell<=d is O(2^d/d).
Thus even the discarded shorter words cost only O(2^d d) steps.
Allowing the stated counter factor changes this to O(2^d d polylog d),
which has the same sufficient aggregate bound below.
The length-d word is a primitive cyclic word. Interpreting it as
normal-basis coefficients gives gamma in K with Frobenius orbit
exactly d; rotations are precisely its conjugates. Every such orbit
has one Lyndon representative, giving every irreducible of degree d
exactly once.

## 3. Producing the polynomial in soft-quadratic bit time

Convert the word to gamma in polynomial basis by scanning the stored
normal-basis columns and XORing selected d-bit vectors: O(d^2)
actual steps. Obtain gamma,gamma^2,...,gamma^(2^(d-1)) by squaring
and reducing modulo h_d. Binary polynomial multiplication and monic
division of degree O(d) reduce by ordinary Kronecker packing to
integer multiplication on O(d log(d+2)) bits; reversed-divisor
inversion is precomputed once. Thus all d conjugates cost
O(d^2 polylog(d+2)) steps and O(d^2 polylog(d+2)) local cells at most.

Form the product of the d linear polynomials X-gamma^(2^j) over K
with a balanced product tree. A concrete multiplication of degree<m
polynomials in X, with d-bit field coefficients, is as follows.
Write each coefficient as a binary polynomial in y of degree<d.
Encode X^i y^j at exponent i(2d-1)+j, then pack each binary
coefficient into a digit of ceil(log2(md+1))+1 bits. The product's
y-degree is below 2d-1, so the index encoding does not overlap;
the digit width prevents carries between convolution counts.
One integer multiplication on O(md log(md+2)) bits, parity extraction,
and sequential reduction of each y-coefficient modulo h_d compute
the field-polynomial product in O(md polylog(d+2)) time for m<=d.

At each tree level the aggregate m is O(d), hence work is
O(d^2 polylog(d+2)); O(log(d+2)) levels retain the same soft-quadratic
order. Use two level streams and reuse them, rather than retaining
the entire tree. Local multiplication scratch is bounded by its
polynomial-in-d time and is reused between nodes and factors.

The resulting degree-d polynomial is fixed by Frobenius because its
roots are one complete orbit. Its coefficients are therefore in F2.
Their polynomial-basis representations can be checked/extracted by
scans, and the d+1 binary coefficients are appended to the directory.
Orbit length d makes it irreducible; uniqueness follows from the
Lyndon representative. All work per retained word is d^2 polylog d.

## 4. Summing and the remaining distinction

There are at most 2^d/d degree-d outputs. Therefore the contribution
of this degree is O(2^d d polylog(d+2)), including word enumeration.
All proper divisors of b are at most b/2, so summing over d|b is
O(2^b b polylog(b+2))+poly(b), proving FS1. Binary factors have
total degree q. Encode each degree d by a self-delimiting O(log(d+2))
tag, or simply the unary word 1^d0, followed by its d+1 coefficients.
The latter uses 2d+2<=4d bits per factor, so the directory has O(q)
bits and remains shared even at binary precision. Expanded H-bit
coefficients cost O(qH) bits and time, including these tags.
The constant number of full output streams and reused polynomial-b
work intervals give the asserted visited-space bound.

This removes factor enumeration as an asymptotic obstacle in the
UC invoice. It does not pay for global CRT cofactor inverses, the
large product P, or the forward/inverse remainder maps; assigning
those costs to this local factor compiler would be incorrect.
