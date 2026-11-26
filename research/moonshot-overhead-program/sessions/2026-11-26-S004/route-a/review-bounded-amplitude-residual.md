# Independent review of the bounded-amplitude residual corrector

Status: **passes algebra, bit-time and fixed-tape visited-space review**, at
the author snapshot identified below. This is a promised correction
component. It supplies neither an unrestricted verifier nor a fast
candidate algorithm satisfying the amplitude promise.

Reviewed author file: `route-b-work/bounded-amplitude-residual-repair.md`.
SHA256: `206372011b3951cfaeef20c60626e0b36efa84597f24919d3c3a6820cddb38b4`.

Physical scheduling supplier: `route-a-work/amplitude-fixed-tape-stack-supplier.md`.
SHA256: `97ac9b9e104bc762854a3aa361faa4d168d643f07e0db6eceb7446ebacd60151`.

The reviewer read the complete current note and independently replayed its
exact checker in `route-a-work/replay-bounded-amplitude/`. The review
includes the ordered coefficient lifting, the principal-root argument over
a ring with zero divisors, actual child dispatch, scalar arithmetic and
the union of visited cells. Finite checks are additional evidence, not
the proof of the unbounded tape estimates.

## 1. Ring identities and the essential child count

Let R=Z/2^a Z and R_n=R[x]/(x^(2n)+x^n+1), with n=mk and m,k powers
of three, m>=k. In E=R_m, omega=y^(m/k) is a principal 3k-th root.
For j=3^v j0 with 3 not dividing j0, the geometric sum contains the
factor 1+y^(m j0)+y^(2m j0), which vanishes because j0 is a unit modulo
three. The length 3k is invertible in R. Therefore the displayed DFT and
inverse DFT work even though R and E need not be fields.

The cyclic idempotent e=(2-u^k-u^(2k))/3 evaluates to zero at precisely
the frequencies j divisible by three and to one at the remaining 2k
frequencies. It is congruent to one modulo u^(2k)+u^k+1. Thus exactly
2k recursive ring products suffice. The proof does not silently charge
3k products or infer vanishing from numerical approximation.

The final coefficient lift has the necessary order. First reduce the
inverse-transformed polynomial in u modulo u^(2k)+u^k+1. Every true
y-coefficient is then a sum of products of original degree-below-m
blocks, so has degree below 2m. Its canonical representative in E is
therefore its actual polynomial coefficient. Only then substitute
u=x^m and y=x and collect overlaps. Substituting y=x directly from E
into R_n would generally be invalid; the current text explicitly avoids
that false homomorphism. This was a material proof detail, now resolved.

## 2. Arithmetic and local movement

Every ring element is a record of 2m coefficients of a bits each.
Addition, subtraction and multiplication by a power of y cost O(ma):
use a zero-extended cyclic shift of 3m coefficients and reduce by the
three-term relation. The argument is valid for every shift exponent,
not just a one-position shift.

Division by three modulo 2^a is linear bit time. For a canonical z,
choose c in {0,1,2} so z+c2^a is divisible by three, and perform exact
fixed-divisor division. Normalizing a radix-three inverse butterfly one
stage at a time therefore has the same linear record bill.

Three monotone partner streams and three reusable output streams implement
each FFT stage with O(kma) movement. Whole-record ternary digit reversal
uses O(log k) stable partition passes. Index work is covered by record
scans because m>=k; this does not assume free arithmetic on an unbounded
word. Hence the complete local term is O(na(1+log k)).

The fixed n=1,3 bases call the stipulated exact a-bit integer multiplier a
constant number of times, with cost O_alpha(a(1+log(a+1))^alpha). Its
uniform linear visited-space hypothesis is explicitly part of A1.

## 3. Recursive head discipline and visited space

A geometric bound on live data alone would not establish the recurrence:
scanning an O(na) parked parent prefix for each of 2k children would be too
expensive. The revised note now uses the explicit suffix-stack supplier.

Each physical tape has a current-frame boundary. Ancestor material lies
below it. Two transformed frequency operands are consumable stacks, read
from their tops in reverse frequency order. A child starts with its two
O(ma)-bit records directly above new boundaries. Its scratch work uses
only current suffixes. A third stack retains the completed parent output
prefix below the child's output boundary. Return clears only child
suffixes, restores the two operand tops, and leaves one canonical result
above the output boundary. Zero frequencies append a zero record without
a recursive call. The tape count and marker alphabet remain fixed.

This costs O(ma) transfer and cleanup per child, hence O(na) altogether.
A single O(na) whole-record order reversal restores inverse-FFT frequency
order. Coefficient bit order inside records is preserved. Full parent
scans occur only in the charged local FFT and reordering passes.

Since m<=n/3 for every nonbase call, maximum rightward extent on each tape
is bounded by a constant times a(n+m+m_next+...), hence O(na). Siblings
reuse suffix regions rather than allocating disjoint new regions. This
bounds all cells ever visited, not merely current live storage. Descriptor
stacks and repeated a descriptions fit this bound. The resulting physical
recurrence is genuinely

    T(n,a)<=2k T(m,a)+O(na(1+log k)).

After division by na, F(ell)<=2F(ceil(ell/2))+O(ell). Ceiling cases
retain the stated O(na log(n+2)[1+log log(n+2)+log^alpha(a+1)]) bill.
The least power-of-three padding is below three. Since a<=tau, the
original input, candidate, residual and modular workspace fit one O(V)
visited-region bound.

## 4. Correction, optional acceptance and limitations

The strict modulus inequality M=2^a>2B gives a unique centered lift of
each residual coefficient in [-B,B]. Candidate reduction, reconstruction,
addition and carries take O(V) scans. This proves A1 under the stated
amplitude promise without any scalar mass computation.

Section 5's optional one-sided test uses least nonnegative residues. Under
the separate structural premise E_i>=0, every E_i-r_i is a nonnegative
multiple of M; equality of total mass is therefore equivalent to absence
of aliasing in every coefficient. The product A(1)B(1) has an explicit
additional cost O_alpha(tau(1+log(tau+1))^alpha). The current note includes
this term. It cannot be hidden in A1 uniformly when h is bounded and b
is arbitrarily large. It is absorbed in the usual growing packed regime.

Without the promise, M X^j aliases to zero. Without one-sidedness, signed
errors may cancel in the mass test. Neither procedure is promoted to a
general verifier. The bilinear Frobenius-norm and ordinary-basis witnesses
are correctly scoped to their specified candidate classes. Classical
Schönhage and Cantor--Kaltofen ancestry is explicitly credited; no new
polynomial-multiplication priority claim is made.

## 5. Independent exact replay

The isolated receipt `replay-bounded-amplitude/bounded-amplitude-verification.json`
reports all controls passed:

* 192 principal-root orthogonality sums and 24 FFT/direct/inverse controls;
* 60 complete cyclotomic products, 405 recursive products with exact 2k
  child invoices, and 1,305 zero-frequency certificates;
* 46 exact division-by-three controls and 2,047 ceiling-recurrence bounds;
* 12 complete ordinary corrections and 12 positive-mass alias controls;
* strict-modulus, unpromised-alias, signed-mass and embedding-degree
  negative controls, plus 60 bilinear amplitude-gate controls.

No fixed-tape implementation was executed. The physical conclusion rests
on the explicit stream, frame and head-movement proof above and in the
supplier note. The two requested corrections have been incorporated in
the reviewed author snapshot, and no remaining blocker was found.

Prepared for @CubeJerry with substantial ChatGPT assistance.
