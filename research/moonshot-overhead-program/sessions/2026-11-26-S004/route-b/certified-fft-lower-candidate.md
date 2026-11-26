# A deterministic FFT supplier for a dense positive residual

Status: **proved explicit supplier; independently reviewed by Routes A
and C, with exact finite controls replayed**. This is a complete positive bridge to the small-modulus
corrector, but its fixed-point FFT invoice misses the target time. The
FFT, half-angle identities and integer square-root construction are
classical. No new fast multiplication algorithm is claimed.

## 1. Supplier statement and fixed parameters

Let A,B have degree below h, with integer coefficients in `[0,2^b)`,
b>=1. Put U=2^b-1. Let N>=max(4,2h) be the least power of two and
ell=log2 N. Thus N=O(h). Choose an integer

    1<=a<=2b+ell,       M=2^a,
    c=ceil(log2(ell+1)),
    q=2b+3ell+2c-a+20,
    delta=2^(-q),
    w=q+2b+3ell+10=Theta(b+ell),
    V=h(b+ell).

All FFT values use exactly q fractional bits and a fixed w-bit signed
word capacity throughout. Rounding a real component means truncating
downwards to this dyadic grid; the error is below delta. Inputs are
represented exactly. No precision grows from one FFT stage to another.

**Theorem FFT.** Fix alpha>1/2 and the same uniform short integer
multiplier as in the repair notes. There is a deterministic fixed
finite-alphabet multitape algorithm that emits an integer candidate C
of degree below D=2h, with

    0<=(AB)_i-C_i<M   for every i,                         (FFT1)

on every input. Its time is

    O_alpha(h ell w(1+log(w+1))^alpha + ell w^2),          (FFT2)

and all cells ever visited lie in one O(V) region. The candidate's
coefficient bit lengths are O(b+ell). Compute AB modulo M with the
charged modular engine, subtract C modulo M, and take the **least
nonnegative** residues. By (FFT1) those residues are exactly E=AB-C,
so this correction needs no scalar mass product. An optional one-sided
mass test also accepts. Alternatively, centered correction may use
B=M-1 and its own modulus greater than 2B, at most 2M; centered lifting
with the same M would be invalid, for example when M=2 and E_i=1.
Both alternatives retain their explicit modular invoice.

The final integer-product construction is complete. Its time is not an
improvement: in the usual h=Theta(n/log n), b=Theta(log n) regime,
(FFT2) is

    O_alpha(n log n (log log n)^alpha),                   (FFT3)

and the extra modular repair has the smaller cost stated in A1 whenever
a is small. This explicit materialized-word FFT has h*ell full-array
word writes, already Omega(h ell w)=Omega(n log n) in that regime.
That observation concerns this schedule, not every numerical or
nonlinear multiplication architecture.

## 2. Effective roots without a transcendental oracle

Construct the primitive N-th root by repeated positive half-angle steps,
starting from the exact pair `(cos(pi/2),sin(pi/2))=(0,1)` at N=4.
For each doubling use

    c'=sqrt((1+c)/2),        s'=s/(2c').                    (FFT4)

Round each operation to the q-bit fractional grid and clamp each
component to [0,1]. Clamping cannot increase its distance to the true
component. If the stored cosine is C*delta, compute its next numerator
exactly as

    C'=isqrt((2^q+C) 2^(q-1)).                            (FFT5)

This is the correctly downward-rounded square root in (FFT4).
The sine numerator is the integer quotient
`floor(S 2^(q-1)/C')`, followed by clamping. Integer restoring square
root and ordinary long division take O(q^2) bit steps and O(q) visited
cells: each has O(q) digit steps, each scanning O(q) bits. There are
ell-2 half-angle steps, so root construction costs O(ell w^2).

Here are explicit error bounds. Let e_c,e_s be the current component
errors. Since the cosine square-root argument lies in [1/2,1],

    e_c'<=e_c/2+delta.

Every stored c' is at least 1/2, because q>=20. The exact c' is also
at least 1/2, so the division in (FFT4), then rounding, gives

    e_s'<=e_s+2e_c'+delta.

Starting from zero error, e_c<=2delta and e_s<=5ell delta. Hence the
computed primitive root differs from the exact root by at most
`epsilon=7ell delta` in complex modulus.

Generate its N powers by successive fixed-point complex multiplication,
rounding each component after every product. The extra complex rounding
error is at most 2delta. If e_j is the error in power j,

    e_(j+1)<=(1+epsilon)e_j+epsilon+2delta.

Our parameters give N epsilon<1/2, so `(1+epsilon)^N<2` and
`e_j<=16N ell delta` for j<=N. We retain the more generous bound

    eta=32N ell delta                                     (FFT6)

for every twiddle, including its conjugate. Its stored magnitude is at
most 1+eta. The same parameters give `eta ell<=2^(-17)<1/16`
and delta<=eta.
These follow directly from a<=2b+ell, hence
q>=2ell+2c+20. All roots are effective dyadic numbers; no exact complex
root, analytic-function routine or hidden field construction is assumed.

## 3. Uniform numerical error through both transforms

Zero-pad A,B to length N and use the usual radix-two FFT with positive
root powers. The DFT convolution identity gives their cyclic product;
N>=2h ensures that it is the ordinary product, since its degree is
below N. Exact stage-j values have modulus at most 2^j U. A
butterfly combines u and omega*v. Complex multiplication is rounded
once in each component; addition and subtraction of fixed-grid values
are exact. If e_j bounds the stage error, then

    e_(j+1)<=(2+eta)e_j+eta 2^j U+2delta.

Divide by 2^(j+1) and sum the resulting geometric factors. Since
eta ell<=1/16 and U>=1, a safe uniform forward bound is

    e_ell<=4eta ell N U.                                  (FFT7)

In particular e_ell<=NU/4. The exact transform values have modulus
at most NU. Each rounded pointwise product therefore has error at most

    2NU e_ell+e_ell^2+2delta
       <=14eta ell N^2 U^2.                               (FFT8)

Apply the conjugate-root FFT to these pointwise products. Its exact
initial values have modulus at most N^2 U^2. The same recurrence,
now with the error (FFT8) as initial error, and exact division by N at
the end, bounds the final coefficient error by

    64eta ell N^2 U^2
       =2048 delta ell^2 N^3 U^2
       <=M/512<M/8.                                      (FFT9)

The generous factor 64 includes an additional q-grid rounding after
the final binary division. For detail, normalization by 2^j bounds
the inverse error by twice its initial error plus
`2j eta N^2 U^2`; after j=ell and division by N this is at most
`30eta ell N^2 U^2`. One further component rounding is absorbed by 64.
The last inequality in (FFT9) uses U<2^b and ell^2<=2^(2c), together
with the fixed q specified in Section 1.

All exact inverse intermediate values are bounded by N^3 U^2, and
the error bounds make their approximate magnitudes at most twice that.
The w-bit capacity includes q fractional bits plus 2b+3ell+10 integer,
sign and guard bits. No overflow occurs. A complex product temporarily
uses at most a constant multiple of w bits before truncation, charged
by the short integer multiplier and its O(w) workspace.

Let z_i be the real part of the resulting approximate coefficient.
Define the integer output

    C_i=floor(z_i-M/8).                                  (FFT10)

The true coefficient c_i is an integer and (FFT9) gives
`|z_i-c_i|<M/8`. Thus C_i<=c_i and

    0<=c_i-C_i< M/4+1<=M,

since M>=2. This proves (FFT1), including the padded final zero
coefficient. The possible negative C_i near a zero true coefficient
is allowed by the repair theorem. Also `|C_i|<=hU^2+M/4+1`, whose bit
length is O(b+ell), because M<=2^(2b+ell). For very small M the same
precision even permits direct exact rounding; the repair stage is not
claimed to be essential in that regime.

## 4. Fixed-tape movement and complete charge

Complex products use a constant number of w-bit integer products and
O(w) scans. Additions, subtractions, clamping, shifts, floors and grid
truncation cost O(w). The root table needs N such short products after
the O(ell w^2) half-angle construction. Two forward FFTs, N pointwise
products and one inverse FFT use O(N ell) complex operations. This
proves the arithmetic term of (FFT2).

Reserve a separate fixed set of tapes for the fixed short integer
multiplier and O(w)-bit local arithmetic buffers. Copy only the current
operand records into that workspace, execute the short multiplication,
copy back its result, and reset that O(w) region. The large FFT streams'
heads remain at their current records. A call therefore does not cross
an O(Nw) parent prefix. Adding this constant set of tapes preserves a
fixed tape count and costs O(w) movement per arithmetic call.

All arrays have O(Nw) bits and use a fixed number of tapes. Implement
each radix-two butterfly stage with two monotone partner input streams
and two reusable output streams, then merge their records. Every head
traverses O(Nw) cells per stage. Initial binary digit reversal uses ell
stable two-way whole-record partition passes, also O(Nw ell) time.
Counters have O(ell) bits, dominated by w; no unit-cost unbounded index
arithmetic is assumed.

Twiddles are not random-access lookups. At a stage with groups of size
2^j, scan the full root table once to select its required stride pattern,
then repeat that pattern sequentially to form the stage's twiddle stream.
The selection scan and the total repeated-pattern scans each cost O(Nw).
Conjugation merely negates the imaginary component. Stage arrays, root
patterns and twiddle streams are reused and erased within fixed marked
regions. The root construction uses O(w) temporary cells. Thus the
union of all visited cells is O(Nw)=O(V), not only the live storage at
one stage. The tape count, alphabet and program are fixed.

Producing the integer candidate and its optional scalar mass data takes
the separately charged scans or mass-product term from the repair note.
To obtain the full exact product by least nonnegative lifting, add

    O_alpha(V+h a(1+log h)
                 [1+log log(h+2)+(1+log(a+1))^alpha])

to (FFT2), using the explicit triadic modular engine. The optional
scalar mass test has its separate O_alpha(w(1+log(w+1))^alpha) charge;
it is unnecessary for this proved supplier. A centered alternative
increases a by at most one and has the same asymptotic invoice. The
space stays O(V) by sequential workspace reuse.
In the packed regime (FFT3), that root-setup term ell*w^2 and the scalar
mass product are only polynomial in log n and are absorbed. No such
absorption is silently asserted for bounded h and arbitrarily large b.

## 5. Why the bridge does not reach the target

The construction provides the required all-input positive residual,
using signed internal arithmetic and a deterministic precision margin.
It therefore escapes the nonnegative bilinear factorization gate, and
its global FFT decoding is not the missing-coordinate local interface.
The cost remains high because the supplier scans full words at every
FFT stage. For small a, q and the integer-part width are both
Theta(b+log h); the small final error amplitude does not make those
intermediate words short. The explicit supplier plus repair recurrence
is complete, but is weaker than the published baseline and the current
programme bound. A faster supplier must change this charged architecture
or supply a different representation and proof.

## 6. Exact finite controls

The self-contained checker uses integer `isqrt`, exact integer division,
and integer pairs for every fixed-point complex value. It uses no
floating-point operations or transcendental library. It passes 217
complete candidate-plus-modular-correction cases, including all 16
binary two-digit input pairs, with 2,542 certified residual coefficients
and the final zero padding coefficient included. It checks 309
half-angle square-root/division steps, 3,952 root-power norm enclosures,
37,148 exact complex rounding operations, and 2,229 fixed-precision
FFT stages. Every checked complex output lies within the M/512 margin,
and all final recorded arrays fit the stated fixed word capacity.
Uncertified modular aliasing and negative-floor conventions have explicit
negative controls. The finite checks supplement the unbounded numerical
and tape arguments; they do not constitute a timing simulation.

The separate integration checker runs the actual dyadic supplier and
the actual triadic modular engine in succession, rather than supplying
the latter's residues from the verification oracle. All 34 complete
integration cases and 568 corrected coefficients pass, including 16
all-maximum-digit products at both extreme allowed precision budgets.
It also checks exact mass and the final base-2^b integer carry identity.
Its JSON records both component checker hashes. The original supplier
checker remains self-contained and unchanged by this integration test.

## 7. Primary-source attribution and actual read scope

James W. Cooley and John W. Tukey, *An algorithm for the machine
calculation of complex Fourier series*, Mathematics of Computation 19
(1965), 297--301, DOI
<https://doi.org/10.1090/S0025-5718-1965-0178586-1>, is a classical
reference for the radix FFT. The primary indexed text of p. 297,
including the DFT definition, factorized-index setup and stated
N log N arithmetic count, was read from the primary PDF mirror
<https://home.cis.rit.edu/~cnspci/references/cooley1965.pdf>. The publisher
PDF returned access denied; the complete article was not claimed read.
The present error margins, half-angle bit construction and sequential
tape charges are derived explicitly here rather than imported from
that arithmetic-operation statement.

The elementary radix-two identity used here splits the DFT sum into
even and odd input indices. If E_j and O_j are their length-N/2 DFTs
at omega^2, then output j is E_j+omega^j O_j, while output j+N/2 is
E_j-omega^j O_j because omega^(N/2)=-1. Recursing gives ell butterfly
stages and the stated bit reversal. Orthogonality of exact roots gives
the inverse and convolution identities. These exact algebraic facts
specify the reference values used in the numerical proof; only the
charged dyadic approximations are ever constructed by the algorithm.

Prepared for @CubeJerry with substantial ChatGPT assistance.
