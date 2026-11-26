# Dense bounded-amplitude residuals: an explicit small-modulus corrector

Status: **proved draft; exact finite controls passed; independent physical
review in progress**.
This route permits a dense ordinary residual with small coefficient
amplitudes. It builds the modular convolution algorithm explicitly rather
than charging a free small-field oracle. No fast candidate supplier or
improved complete worst-case multiplier is supplied.

The modular multiplication engine reconstructs the classical Schönhage
radix-three cyclotomic method. It is not a new polynomial-multiplication
algorithm. This note prices the residual-correction interface and states
its amplitude and supplier conditions.

## 1. Correction theorem and the required modulus

Let `A,B` have degree below h and nonnegative b-bit coefficients, and let
the integer candidate C have degree below `D=2h` and coefficients bounded
by Cmax in absolute value. Put

    E=AB-C,  Emax=h 2^(2b)+Cmax,
    tau=ceil(log2(2Emax+2)),  V=D tau.

Suppose a known integer B>=1 satisfies `|E_i|<=B` for every i. Replace
B by `min(B,Emax)` and choose

    a=ceil(log2(2B+1)),       M=2^a>2B.

Reduce each input coefficient and each candidate coefficient modulo M,
and compute `AB` as an ordinary polynomial convolution over `Z/MZ`.
Then `AB-C mod M` has a unique centered lift in `[-B,B]`, namely E.
Add that lift to C and carry to obtain the exact integer product.

**Theorem A1.** Fix alpha>1/2 and a fixed exact multitape integer
multiplier of time `O_alpha(u(1+log2 u)^alpha)` and visited space O(u).
The promised correction above has a deterministic fixed-tape algorithm
of time

    O_alpha(V + h a (1+log2 h)
                    [1+log2 log2(h+2)+(1+log2(a+1))^alpha])   (A1)

and one O(V) bound on cells ever visited. All construction and coefficient
operations are charged. There is no prime search or field extension.

For the usual packed regime `b=Theta(log n)`, candidate coefficient bit
length O(log n), and `h=Theta(n/log n)`, this becomes

    O_alpha(n + n a [log log n+(1+log(a+1))^alpha]).           (A2)

Thus a polynomial-logarithmic amplitude B, giving `a=O(log log n)`,
allows repair in `n(log log n)^O(1)=o(n sqrt(log n))` time. More
generally the displayed cost is below the square-root-logarithmic
target whenever

    a[log log n+(1+log(a+1))^alpha]=o(sqrt(log n)).             (A3)

For example, `a=O((log n)^nu)` with fixed `nu<1/2` satisfies this.
The bound prices correction only, not production of C with this promise.

## 2. Why a direct packed product is not a small-modulus oracle

Packing residues directly into integer digits needs a radix exceeding
`h(M-1)^2`, because an ordinary convolution coefficient can contain h
summands. Its packed bit volume is therefore
`Theta(h(log h+a))`, which is still Theta(n) when b is Theta(log n)
and a is small. A full integer multiplication on that volume does not
automatically give a cheaper correction. The following ring recursion
avoids that hidden guard-bit cost.

## 3. A radix-three polynomial multiplication recursion

Work over the base ring `R=Z/2^a Z`, where 3 is a unit. For each power
of three n, define

    R_n=R[x]/(x^(2n)+x^n+1).

Its elements are represented by 2n base coefficients, each of a bits.
Ordinary polynomial products of input degree below h are embedded by
choosing the least power of three n>=h. The product has degree below
2h-1<=2n-1, so its residue in R_n is its ordinary coefficient list.
The padding factor n/h is below three.

For `n=3^ell`, ell>=2, write

    m=3^ceil(ell/2),   k=3^floor(ell/2),   n=mk.

Split each input into 2k consecutive blocks of m coefficients and write
it as `P(u)=sum_(i<2k) A_i(y) u^i`, with `deg A_i<m`. Calculations
take place over `E=R_m`, and the final substitution is `u=x^m,y=x`.
Let

    omega=y^(m/k) in E,       L=3k.

Then omega is a principal L-th root of unity in E. For any `0<j<L`,
write `j=3^v j0` with 3 not dividing j0, and set `rho=omega^j` and
`t=L/3^(v+1)`. We have `rho^(3t)=1` and `rho^t=y^(m j0)`. Hence

    sum_(i=0)^(L-1) rho^i
       =3^v [sum_(i=0)^(t-1) rho^i](1+rho^t+rho^(2t))=0,

because the last factor is `1+y^m+y^(2m)`, possibly with the last
two terms exchanged. Also omega^L=1. Therefore

    sum_(i=0)^(L-1) omega^(ij)=0,   and L is a unit in E.

The usual DFT matrix and inverse DFT with factor L^-1 are consequently
valid over this ring, despite zero divisors in the base ring.

Only 2k pointwise products are necessary. In `E[u]/(u^(3k)-1)`, put

    e(u)=(2-u^k-u^(2k))/3.

This idempotent is zero at omega^j when 3 divides j, and is one at the
other 2k evaluation points. It is also congruent to one modulo
`u^(2k)+u^k+1`. Embed P and Q as eP and eQ modulo `u^(3k)-1`, transform
both, multiply at the 2k nonzero frequency positions, and invert the
transform with zeroes in the remaining k positions. Reducing the answer
modulo `u^(2k)+u^k+1` gives exactly PQ in that quotient.

Each pointwise product is a multiplication in R_m and is computed by
the same algorithm recursively. After inverse transformation, first
reduce in u modulo `u^(2k)+u^k+1`. The true coefficient polynomials in y
are then sums of products of the original A_i and B_i, so have degree
below 2m. Take the canonical degree-below-2m lift of each E coefficient;
it is exactly that true polynomial, since reduction modulo
`y^(2m)+y^m+1` has lost no coefficient information. Only after this
lifting step substitute u=x^m and y=x, add adjacent-block overlaps,
and reduce modulo
`x^(2n)+x^n+1`. This reconstructs the exact desired ring product.
In particular, the proof does not assert a homomorphism from E to R_n
sending y to x; that map need not exist. The ordered lift is essential.

The cases n=1 and n=3 use a fixed number of a-bit coefficient products
and ordinary scans. Their time is `O_alpha(a(1+log(a+1))^alpha)`.

## 4. Actual tape invoice and uniform space

A length-3k radix-three FFT has O(log k) stages, each with O(k) ring
additions and multiplications by powers of y. A multiplication by y^j
is a cyclic shift in a zero-extended 3m-coefficient array followed by
the relation `y^(2m)=-y^m-1`; it costs O(ma) bit steps. Each ring addition
also costs O(ma). Scalar division by three modulo `2^a` costs O(a):
choose `c in {0,1,2}` for which `z+c 2^a` is divisible by three and
perform ordinary bitwise division by the fixed integer three. Inverse
FFT normalization can divide by three at each stage, so it has the same
cost. The idempotent embedding needs only shifted additions and one
such division per coefficient.

These are sequential tape operations. At a butterfly stage, retain a
fixed number of copies of the array on fixed tapes. Three monotone input
heads read the three partner blocks within each butterfly group, skipping
unused sections monotonically between groups. They write the three
result streams onto three reusable tapes, then merge corresponding
blocks into the next array. Every head traverses O(kma) cells per stage.
Twiddle shifts are done within the reusable O(ma) record regions. No
random-access field operation, variable tape count, or free global
permutation is used. Counters and powers of three have logarithmic
descriptions; their preparation and advancement are covered by the scan
invoice, with constant-size base cases handling the smallest inputs.
An initial or final ternary digit reversal, if needed by the chosen FFT
ordering, uses O(log k) stable three-way partition passes on whole ring
records. This costs O(kma log k), within the transform invoice. Since
m>=k, O(log k)-bit index work per record is covered by its O(ma) scan.

If T(n,a) is the full bit cost for R_n multiplication, the actual
recursive bound is

    T(n,a)<=2k T(m,a)+O(n a(1+log k)),                        (A4)

with the base cost just stated. The essential factor is **2k**: the
idempotent makes the other k Fourier products identically zero.
Charging all 3k children would give a different, weaker recurrence.

For `F(ell)=T(3^ell,a)/(3^ell a)`, (A4) becomes

    F(ell)<=2 F(ceil(ell/2))+O(ell),
    F(0)+F(1)=O_alpha((1+log(a+1))^alpha).

By grouping recursion levels until ell halves, this yields

    T(n,a)=O_alpha(n a(1+log n)
                  [1+log log(n+2)+(1+log(a+1))^alpha]),       (A5)

including the ceiling cases. At each level only one pointwise child is
active; parents park a fixed number of full arrays. To avoid traversing
these parked prefixes for every child, keep the two transformed frequency
streams as consumable stacks and process frequency indices in reverse
order. The next child's two input records are at their respective stack
tops. Copy those O(ma)-bit records into child work suffixes above marked
frame boundaries, run the child, and append its result to a third output
stack. Erase/reset only the child's suffixes when it returns. Fixed tapes
may hold a constant number of these disjoint marked stack streams; no
parent prefix is crossed per child. The total child transfer and cleanup
cost is O(ma) per child, already within the O(na) level invoice. One
O(na) reversal/copy after the last child places the result frequency
stream in the order required by the inverse FFT. All sibling boundaries
remain inside the parent's O(na) frame ranges. The child volume
is at most one third of the parent volume for ell>=2. The retained
volumes form a geometric series, so one fixed O(na) region bound covers
all cells ever visited. FFT stages and siblings reuse their marked
regions. The original input/candidate stream is O(V), and a<=tau, so
the correction algorithm has O(V) visited space. Input reductions,
centered lifting, addition to C, and final carries cost O(V), proving A1.

## 5. A sound one-sided budget test

If the candidate construction independently guarantees `E_i>=0`, the
same modular convolution yields a sound acceptance test without an
amplitude promise. Choose M=2^a with `1<=a<=tau` and let `r_i` be the **least
nonnegative** residue of `(AB-C)_i mod M`. Compute

    T=E(1)=A(1)B(1)-C(1).

Every difference `E_i-r_i` is a nonnegative multiple of M. Therefore

    sum_i r_i=T  if and only if  E_i=r_i for every i.          (A6)

Equality certifies the complete correction. Failure permits an exact
fallback or a larger budget. A bound `0<=E_i<M` guarantees fast
acceptance; a guessed amplitude cannot silently cause acceptance of
aliased positive errors. The scalar sums fit O(V) scanning time, while
the product A(1)B(1) involves O(tau)-bit integers and costs
`O_alpha(tau(1+log(tau+1))^alpha)`. Thus this one-sided test has the
time in (A1) **plus that explicit scalar-product term**. Its space is
still O(V). In the usual packed regime of (A2), the additional term is
absorbed by O(V), but that absorption is not asserted for constant h
and arbitrarily large b. The promised corrector A1 itself does not need
the scalar product or this extra charge. One-sidedness remains a
structural premise, and is not inferred merely from nonnegative candidate
digits.

The mass identity itself holds for any power-of-two modulus. For the
stated O(V) space invoice, cap a at tau: `2^tau>2Emax` already resolves
every residual allowed by the input/candidate height bound. Capping a
larger requested budget therefore preserves acceptance and avoids
allocating an unbounded-width modular record.

Without an amplitude or one-sided premise the modular residues are not
a verifier: the nonzero error `M X^j` aliases to zero modulo M. Signed
errors can also cancel in the mass test. These limitations are explicit.

## 6. Supplier precision gates

The following are scoped obstructions to two studied candidate classes,
not lower bounds for arbitrary multiplication algorithms.

First, in the regular ordinary basis of a product of commuting shift
queries, a support-degree-t linear predictor with t<m has zero coefficient
at the target full shift. On an input with a single nonzero entry U,
the corresponding target output is U and the predicted output is zero.
Thus any uniform ordinary absolute-error budget must satisfy B>=U.
This is the basis-vector witness already proved in the spectral-rank
note, now read as an amplitude constraint. For record digits of b bits,
U can be `2^b-1`; hence the modulus bit length a cannot be substantially
smaller than b at that linear interface. A later nonlinear product
composition is a separate mapping and is not covered automatically.

Second, for a fixed real bilinear ordinary-product candidate
`Q_i(a,b)=a^T G_i b`, write the exact form as `a^T H_i b` and
`F_i=a^T(H_i-G_i)b`. If `|F_i|<=B` on every input in `{0,U}^h`,
the independent-sign expansion from the bilinear supplier note gives

    B^2>=E[F_i^2]>=U^4 ||H_i-G_i||_F^2/16,
    ||H_i-G_i||_F<=4B/U^2.                                  (A7)

In particular, reducing the matrix rank of any individual convolution
form forces `||H_i-G_i||_F>=1`, hence B>=U^2/4. Omitting a unit
coefficient outright gives the stronger B>=U^2 on the corresponding
one-hot pair. A modulus with very small a therefore requires high
absolute accuracy in every output form, rather than merely low average
spectral rank error. Shared bilinear implementations and exact low-cost
forms are not excluded by this statement.

The corrector is fast under a real dense-amplitude guarantee. Neither
rare spectral errors nor the low-degree predictors examined so far
supply that guarantee on arbitrary full-rate inputs. A genuinely new
approximate supplier remains the missing step toward a complete bound.

## 7. Prior-art and actual read scope

Arnold Schönhage, *Schnelle Multiplikation von Polynomen über Körpern
der Charakteristik 2*, Acta Informatica 7 (1977), pp. 395--398, DOI
<https://doi.org/10.1007/BF00289470>, is the original triadic reference.
Its publisher abstract and author bibliography were read; the
subscription full text was not accessed.

David G. Cantor and Erich Kaltofen, *On Fast Multiplication of Polynomials
over Arbitrary Algebras*, Acta Informatica 28 (1991), pp. 693--701,
author PDF <https://kaltofen.math.ncsu.edu/bibliography/91/CaKa91.pdf>,
was read through Sections 1--2 and the initial cyclotomic split of
Section 3. These primary sections credit Schönhage's triadic construction
and develop Fourier/cyclotomic arithmetic. The present proof over Z/2^a
supplies its own unit-root, coefficient-lifting, tape-movement, and
visited-space arguments. An algebraic operation count is not imported
as a free tape routine. No priority claim is made for the modular engine.

Prepared for @CubeJerry with substantial ChatGPT assistance.
