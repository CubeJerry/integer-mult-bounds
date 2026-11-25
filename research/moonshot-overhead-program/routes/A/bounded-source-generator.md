# A bounded constructive route for the original source templates

Status: **accepted for the stated source-extraction contract after independent review**. The finite-generator gate is recorded in `../C/REVIEW-A-BOUNDED-GENERATOR.md`; the physical and end-to-end gates are recorded in `../../verification/S002/lead-review-physical-compiler.md` and `../../verification/S002/lead-review-explicit-extraction.md`. This is an AI-assisted mathematical audit, not a formal build or execution of the complete multiplier.

This route retains the original finite-characteristic construction. It does
not substitute the characteristic-zero count polynomial into interchange.
Source pin: OpenAI `math` `3344da59991ed94f9ba711217b29c1d760badfa6`.

## 1. Directly choose finite parameters, then test exact margins

For target exponent theta_j=1/2+1/(j+2), use
rho_j=1/2+1/(2(j+2)) for both tape recurrences. Choose a prime p between
100(j+2) and 200(j+2), increasing the absolute factor if needed. Trial
division finds it; Bertrand guarantees existence. For Fourier routing take
an even L between 100(j+2) and 202(j+2).

Try m=2^u+1 with u increasing through powers of two. This makes m odd, as
required by the source binary Fourier template. Interchange needs no extra
congruence. For each candidate m:

1. Interchange: take q as the least power of two with q^(p^2)>=C_r m,
   using the explicit C_r in `interchange-label-growth.md`.
2. Fourier: take q as the least power of two with q^(L/2)>=m. At ell=2,
   the direction rank is at most 1+Lq. Charged rectangles number at most
   2^L q^(L/2), and the endpoint incidence is at most
   2(2+log2 q)^L. These follow by the same explicit subset/first-differing-bit
   counts as the source kernel proof.
3. Require also p<=m, the binary prediction degree D_predict<=m, the
   interchange label count N<=m^5, and the Fourier label count q^L<=m^3.
   These are decidable integer guards. They hold in the large-m range
   proved below, so adding them does not change the search bound. They
   ensure that an unexpectedly early successful contraction is not used
   without the stated polynomial-m dimension/height estimates.
4. Build or upper-bound the finite call lists and test exact contractions
   with a fixed relative margin: the complete interchange coefficient
   lambda_I<=m^rho_j/2 and the pre-padding Walsh coefficient
   (sigma/W)<=A^rho_j/4. A possible padding factor at most two then leaves
   a factor-two Walsh contraction margin. The tape Walsh caller actually
   uses exact V/W children after its top-level padding, so this stricter
   test is conservative. Raising to rational-exponent denominators is an
   integer comparison. Only then emit the finite scalar/matrix tables.

The uniform label bounds show that these tests eventually succeed with

    u=O((j+2)^6),  hence m<=2^{O((j+2)^6)}.                (G3)

This deliberately weak sixth-power estimate avoids optimizing constants.
For interchange, the logarithm of the extra label factor is bounded by
O(u/p+p^2 log(u+p)); with p=Theta(j), this is at most a sufficiently small
multiple of u/(j+2) plus O(j^2 log(u+j)). The strict target gap absorbs the
second term at u=O(j^6). For Fourier, its extra logarithm is bounded by
2u/L+O(L log(u+L)); the same argument applies. The universal constants in
the finite stage invoices must be fixed by their explicit instruction lists;
the search itself accepts only verified call counts, so guessing a small
constant cannot make it accept an invalid template.

No asymptotic O_p is used with a growing p here: the needed p-dependence is
provided by the explicit label estimates. The finite scalar repair has
O(sqrt(m log m)) stages with an absolute binary-case constant.

## 2. Coarse rational-address bounds

For the successful family, label counts are polynomial in m once m is large:
interchange N<=m^5, and Fourier q^L<=2^L m^2<=m^3. The remaining bounded
range can be absorbed in an absolute constant. Every initial Gram entry has
polynomial-m numerator/denominator height. Rational elimination, orthogonal
complements and lower-triangular factorizations use polynomially many
operations on polynomial-size matrices. Fraction-free elimination or
determinant-minor formulas keep all resulting rational bit lengths bounded
by a fixed polynomial in m. Numeric numerator/denominator magnitudes are
therefore at most 2^{m^c} for some absolute c.

For a deliberately loose common envelope, the detailed height proof in
`rational-address-and-generator-bounds.md` permits the fixed absolute
choice C0=100000. Put

    Rhat(m)=2^{2^{m^C0}}.                                 (G4)

The scalar program in `scalar-template-growth.md` fits a fixed power of
Rhat. All rational-address numeric magnitudes, not merely their bit lengths,
also fit Rhat. Choosing the address radix prime above both the total batch
width and every nonzero numerator/denominator, including factor inverses,
pivots and required diagonal units, is sufficient for compatibility.
Bertrand supplies such a prime below twice that maximum. Enumeration and
trial division up to that bound cost a fixed power of Rhat.

## 3. An actual finite construction, not an unbounded search oracle

All successful finite data can now be constructed by explicit finite loops:
labels and rectangles; rational elimination; scalar Clifford matrices;
cyclotomic Lagrange inverses and Hermite tables; basis expansion; compatible
radix selection; exact call-list checks. Each loop dimension, coefficient bit
length and retained array is bounded by a fixed power of Rhat. Schoolbook
arithmetic therefore gives finite generation time and workspace

    g_j,d_j <= Rhat(m_j)^C                               (G5)

for an absolute C, provided the listed matrix/primitive constructions are
indeed used. Failed trials with smaller u are covered by the largest envelope
and there are only O(log(j+2)) trials before (G3), after enlarging constants.

This does not follow from output size alone. It follows from the specified
construction and the explicit ring inverse formula. A different generator
with arbitrary delays does not inherit (G5).

## 4. Intended physical compilation budget

The source primitive ledger suggests the following conservative targets:

    a_j,c_j <= Rhat(m_j)^C,
    U_j <= max{U_abs,2^{Rhat(m_j)^C}},                     (G6)

where U_abs is the fixed source prime-shape/geometry cutoff (no numerical
value is asserted), a_j is the interpreted digit-time coefficient, c_j its proportional
space coefficient, and U_j its valid-input threshold. Fixed code remains
in d_j. Reasons: coordinate scalings and radix padding have numeric factors
at most a fixed power of Rhat; there are at most that many one-level streams
and instructions; numerical coefficient *bit heights* and log gains have
the same bound; threshold k>=Rhat^C makes their contribution fit a fixed
record precision and absorbs polynomial setup. Strict recurrence margins
are at least 1/2 by construction.

This compiler contract is now established by the separately reviewed physical ledger.
Its audited requirements are concrete: bound every variable-length primitive by a
common polynomial in the finite data and k, show its guard/sort costs retain
the source log^4 k factor, and verify the stream/descriptor serialization
without changing recursive volume coefficients. An unspecified 'poly(k)'
must not conceal dependence in its degree or an extra full-array scan.

## 5. Envelope that would follow after completing that audit

If (G3)--(G6) are established, A10 gives candidate prefactors and thresholds
with

    log2(prefactor_j), log2 L(N_j) <= 2^{2^{O((j+2)^6)}}.

The dyadic candidate subsequence suffices. Taking a sufficiently small
constant multiple of (log2 log2 s)^(1/6) for j gives the explicit envelope

    H(n) <= 2^{O(s/(log2 log2 s)^(1/6))},  s=log2 L(n),    (G7)

for sufficiently large n. Indeed the double-exponential candidate overhead
can then be made s^{o(1)}, while the exponent-excess contribution is O(s/j).
This is much slower than 2^{O(s^beta)} for beta<1, but it is an explicit
subpower envelope. It would be a quantitative extraction from the published
construction, not evidence that it improves the published unspecified o(1).
The physical compilation and uniform assembly audits are now accepted; (G7) is an admitted quantitative extraction for this programme.

The complete profile-to-envelope assembly is in `explicit-extraction-theorem.md`.

Next questions: sharpen this deliberately coarse profile and compare it with any quantitative rate already extracted elsewhere. The completed review gates are linked above. Credits:
the OpenAI source constructions and predecessors, @CubeJerry, AI assistance.
