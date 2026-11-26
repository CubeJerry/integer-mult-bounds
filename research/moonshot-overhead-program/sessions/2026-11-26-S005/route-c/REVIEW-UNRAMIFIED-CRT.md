# Independent review: exact lifted CRT caller and factor-stream setup

**Decision: accepted in the stated scope.** UC1–UC6 give a full-input,
volume-preserving exact reduction and a conditional precision recurrence.
FS1 supplies the local binary factor stream within its claimed tape budget.
Neither note supplies the fast forward/inverse CRT or the new-digit carry
map. There is no new unconditional integer-multiplication bound here.

Reviewed final files and SHA-256:

- route-a/unramified-polynomial-crt-caller.md:
  e451b65deb2657176e354e2b3d4ab3da6d1ecba44d75c4d7b44610ac9bb6560b
- route-a/binary-factor-stream-compiler.md:
  13be8001733a677195095abbace706db3fe86f1fcef490531c65f4c49f09be2c

The review independently read the algebra, the physical invoices, and the
primary preprocessing references. The finite checker described below was
written separately and imports no author implementation.

## 1. Full-rate algebra and the ordinary-product guard

Let q=2^b, R=Z/(2^H), and let g_i be the literal binary monic lifts of
all irreducibles over F2 of degree dividing b. The factorization of
x^q-x over F2 gives sum_i degree(g_i)=q. Its derivative is 1, so those
factors are distinct. A modulo-2 Bezout relation lifts to
A g_i+B g_j=1+2C. The polynomial 1+2C is a unit in R[x]: its inverse
is a finite geometric sum, since (2C)^H=0. This argument works over
the nonfield ring and establishes the required pairwise comaximality.

Monicity gives unique representatives of degree below the modulus,
even with zero divisors in R. Hence CRT is an R-linear bijection
between the q independent coefficient words and the factor residues
of total degree q. The representation has exactly qH payload bits
on either side. It does not retain q extension-field elements of
degree b, and it imposes no invariant, symmetry, rank, or phase sector.

The distinction between the literal product P and x^q-x is essential.
Already for b=2, P=x^4+2x^3+2x^2+x, which is not x^4-x modulo 4.
The caller does not need that false equality: its ordinary input
polynomial product has degree below q, so its representative modulo
the actual monic P is unchanged before coefficient reduction.

The integer parameters also pass. With radix D=2^B and h digits,
every ordinary product coefficient is at most h(D-1)^2. The stated
H exceeds the binary length of this bound. After CRT inversion, the
canonical coefficients therefore recover those actual nonnegative
integers. For the final scan, the stronger invariant

    incoming carry <= h(D-1)

is preserved, because

    floor((h(D-1)^2+h(D-1))/D) <= h(D-1).

Thus the added coefficient and carry fit the stated guard. Removing
padding means retaining the required fixed 2n-bit output, including
its zero high bits; it does not change the numerical result.

The power-of-two rounding of H is harmless. As n grows,
B~log2 n, b~log2 n-log2 log2 n, and the rounded H is below
2(2B+ceil(log2(h+1))+2). Hence b<=H<=8b eventually, and qH=Theta(n).
The finite exceptional range can be assigned one direct base program.

## 2. The local product bill is independent of the open transform

For a degree-d quotient, the coefficient packing radix exceeds every
integer convolution coefficient. The packed integer operands have
O(dH) bits when H>=b>=d. The reciprocal of the reversed monic
modulus exists because its constant coefficient is 1. Newton's step
u'=u(2-fu) obeys 1-fu'=(1-fu)^2 over any commutative ring; it does
not require division by 2. This supports monic division modulo 2^H.

The safe per-factor bill O(dH log(dH+2) log(d+2)) includes reciprocal
preparation, multiplication, reduction and scans. Summing d_i=q,
d_i<=b and H<=8b gives the claimed O(qH log^2(b+2)). These UC3
calls have O(b^2)=O(log^2 n) input bits. The cited published integer
multiplier is used only at those local sizes, and its workspace can
be bounded by its local running time and reused. No unproved global
linear-space property of that multiplier is needed.

FS factor construction uses slightly larger local packed operands,
O(b^2 log(b+2)); the revised UC opening correctly states the weaker
O(log^2 n loglog(n+4)) bound for all work outside the open gate.
Both are polylogarithmic, and neither imports n-bit multiplication
into the proved caller.

## 3. Precision lifting: exact identity and explicitly conditional cost

The family of factors is independent of coefficient precision. For
the canonical low-digit representative F0, define K_t(F0) as the
high t digits of E_(b,2t)(F0). Reduction of those values modulo 2^t
is exactly E_(b,t)(F0). Linearity then proves the forward formula

    E_(2t)(F0+2^t F1)
      = lift(E_t(F0))+2^t(K_t(F0)+E_t(F1)) mod 2^(2t).

For inverse lifting, E_t^-1(Y0) is precisely the low coefficient
representative F0. Subtracting K_t(F0) from Y1 and applying E_t^-1
recovers F1. The subtraction and canonical-lift convention are
necessary. A binary CRT circuit alone does not supply K_t.

For H a power of two, two children at precision H/2 plus one local
new-digit gate give the stated normalized recurrence. There are H
binary leaves, producing qH B(b), rather than only one binary call.
At each nonbase level, total child coefficient volume is qH, so its
local charge contributes one D(b,t) term after normalization. This
explains the sum over dyadic t in UC6 without suppressing multiplicity.

The common visited-space argument is conditional on the stated
uniform local contracts. Only one child runs at a time. Parent
payloads occupy a constant multiple of their volume; active volumes
decrease by halves, so their sum is below 2qH. Reused sibling regions,
one shared O(q)-bit binary factor directory, and paid split/merge
scans preserve an absolute O(qH) visited-cell cap. Counting only
simultaneously live data without region reuse would not suffice;
the note explicitly calls for reuse.

For the proposed endpoint supplier, sum over dyadic sqrt(t) is
O(sqrt(H)), while the added depth O(log H) is smaller. With H=Theta(b),
the total normalized bill is O(sqrt(b)). The broader supplier adds
the displayed logarithmic depth. These implications are valid;
the binary and carry suppliers are both still unproved.

## 4. FS1: actual factor-stream work and its preprocessing import

The primary Bshouty–Diab–Kawar–Shahla PDF, section 2, explicitly
states deterministic polynomial-time construction of a degree-d
field and a normal basis for fixed base field F2. The formulas there
remain polynomial when both q and p are 2. Its enumeration procedure
uses indexed operations; the review does not import its stated delay
as a multitape theorem. Only once-per-degree polynomial preprocessing
is imported. Slowing that preprocessing by a polynomial to simulate
its data on a fixed number of tapes remains harmless.

The following separate accounting supports FS1's stronger per-output
bound without a generic polynomial RAM simulation of each output:

1. Ordinary Duval updates use O(d) symbolic operations on an O(d)-bit
   word. Scanning for each access permits O(d^2 polylog(d+2)) actual
   steps. The total number of generated Lyndon words of all lengths
   at most d is O(2^d/d), including discarded shorter words. The
   enumeration bill is consequently O(2^d d polylog(d+2)).
2. A retained length-d primitive word specifies one element in normal
   coordinates. Converting it once by scanned basis columns costs
   O(d^2). Generating the remaining conjugates by d sequential
   Frobenius squarings and fast monic reductions costs
   O(d^2 polylog(d+2)). Recomputing every conjugate independently by
   a dense basis conversion would instead introduce an unnecessary
   factor d; the note uses the cheaper sequence explicitly.
3. For two degree-bounded polynomials over the d-bit binary field,
   the index map (i,j) -> i(2d-1)+j separates the outer degree from
   the field-polynomial degree after multiplication. A digit width
   above log2(md) prevents integer convolution carries. Parity
   extraction and sequential monic reduction yield the exact field
   coefficients. The operands have O(md log(md+2)) bits, and for
   m<=d this gives O(md polylog(d+2)) tape work, including scans.
4. At a balanced root-product level, the sum of the outer size m is
   O(d). Summing its levels gives O(d^2 polylog(d+2)) per polynomial.
   Two sequential level streams and local multiplier scratch are
   reused. No global list of extension-field roots is retained.
5. Frobenius permutes the complete d-element root orbit, so every
   coefficient of its product is Frobenius-fixed and therefore lies
   in F2. The polynomial-basis coordinates are exactly literal 0 or
   1, not approximate constants or an assumed field embedding. The
   primitive orbit proves degree-d irreducibility, and the unique
   Lyndon representative proves uniqueness and completeness.

There are at most 2^d/d degree-d outputs. Summing over d dividing b
therefore gives q b polylog(b+2)+poly(b), because every proper divisor
is at most b/2. The absolute polynomial preprocessing term is
eventually absorbed by qH. For H=Theta(b), the main setup bill is
qH polylog(b+2), below qH sqrt(b) after a fixed cutoff.

The revised directory format is suitable for the binary leaf's space
contract. A unary degree tag 1^d0 followed by d+1 literal bits costs
at most 4d bits for d>=1. Since total degree is q, the directory is
O(q) bits. It is emitted in the specified degree/Lyndon order and
needs no q-by-b record sort. Expanded H-bit coefficients are a
separate O(qH) stream. Current-degree basis data, roots, level
streams and arithmetic scratch use only polynomial-in-b local
space, reused before the next factor.

This is a constructive written tape schedule, not an executable
verified tape compiler. Its imported algebraic preprocessing theorem
and published integer multiplication theorem remain external results.

## 5. The unsupplied gate remains the first asymptotic obstacle

The total actual caller has two forward transforms and one inverse,
plus factor generation, quotient products and output carry scans.
The inverse must return coefficient order. Setup for a large P,
global CRT cofactors, inverse constants, reordering and return passes
is inside the open transform bill; FS1 does not pay for them.

For a classical balanced product/remainder tree, a degree-D stage
has coefficient volume O(qH). With actual published multiplication
at that degree scale, its safe time invoice is O(qH log(DH+2)).
Across O(b) degree levels, this yields O(qH b^2). The top levels
make integer calls of size Theta(qH), so treating them as free or
using the hoped-for multiplication theorem there would be circular.
Keeping every tree level would additionally cost O(qH b) visited
cells; a common-cap schedule must be proved separately. This is an
upper invoice for that implementation, not a lower bound on CRT.

Thus the review admits a more concrete alternative target: binary
CRT plus the precise canonical carry-remainder map K_t, both at
their stated time and space contracts. It does not admit a fast
lift merely from characteristic-two algebra, a fast arbitrary-basis
field evaluation transform, or an unconditional endpoint.

## 6. Independent finite replay and adverse controls

Run from the worktree with:

    python3 -I -B research/moonshot-overhead-program/sessions/2026-11-26-S005/route-c/verify_crt_independent.py

The receipt is crt-independent-verification.json. The checker uses
brute force irreducibility tests and dense modular matrix inverses
only as finite oracles. Those algorithms are deliberately excluded
from every fast-supplier and physical-compiler claim.

The successful independent replay covers:

| Check | Count |
| --- | ---: |
| Full CRT module inverse identities, b=1 through 5 and H=1,2,3,4,8 | 25 |
| Arbitrary full coefficient round trips | 200 |
| Packed products and Newton monic remainders over Z/(2^H) | 345 |
| Forward and inverse canonical precision lifts | 180 |
| Exact ordinary integer products with carry invariant | 80 |
| Complete Duval lists of all Lyndon lengths through d, d=1 through 8 | 8 |
| Normal-basis orbit products, matching all irreducibles of degrees 1 through 8 | 71 |
| Explicit two-dimensional packed field-polynomial products | 545 |
| First-carry polarization and its quadratic coordinate formula | 150 |

Omitting K_t fails on 149 tested inputs, and the literal b=2 lift
differs from x^q-x modulo 4. These controls reject the two shortcuts
most likely to make the proposed lifted transform appear supplied.
Finite replay supports the algebraic reading; it is not a proof of
asymptotic complexity, uniform tape compilation or the open gate.

The separate note BINARY-CARRY-POLARIZATION.md proves the first carry's
quadratic refinement identity. Its 150 additional comparisons include
125 controls where omitting the overlapping-support correction fails.
The identity identifies the missing linear lift data; it does not
provide that data or the required physical compiler.

## Sources consulted

- Bshouty, Diab, Kawar and Shahla, Enumerating all the Irreducible
  Polynomials over Finite Field, section 2 and the ordinary Duval
  discussion: https://arxiv.org/pdf/1602.05032 and
  https://www.wseas.org/multimedia/journals/computers/2016/a405805-092.pdf.
  The review checked the deterministic preprocessing statements in
  the primary PDF, rather than relying on the author's summary.
- Harvey and van der Hoeven, Integer multiplication in time O(n log n),
  Annals of Mathematics 193 (2021), 563–617:
  https://annals.math.princeton.edu/2021/193-2/p04.
  Its published model is multitape Turing machines with binary integers.
