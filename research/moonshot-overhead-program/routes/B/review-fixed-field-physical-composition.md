# Independent review of the fixed-field physical composition

Result: **PASS for Q1--Q13 and the stated substitution into the separately
accepted source compiler/common-cap gates**. Read
`../A/fixed-field-extraction-theorem.md` in full during S002, with targeted
rereads of B's actual component proofs. No missing factor was found.

## 1. Complete call invoices Q3 and Q5

The O3 recurrence has four children of row fraction 1/16 and total mass
1/4. Its final three-transform word costs

    sigma_Q/W <= 8 D_pred R_pencil + 3m 4^(-a).

The new factorization supplies D_pred stages, replacing the old padded
b_pred. Using D_pred<=12sqrt(m), R_pencil<=64D_I(1+lambda_I), and
a=ceil(log2(m)/4), the main coefficient is at most 6144; the leaf term
is at most 3sqrt(m). Thus 8192 is safe. Doubling for leading-row batching
and adding 2(D_I-2) occupied-reserve calls is safely below Q3's 32768.
Both query powers share one swap pencil, with the two diagonal masks
handled by charged comparison/row scans. No factor of two is missing.

The pairwise Newton predictor uses at most 7sqrt(m) active pencils and
two evaluations. Its two V/8 phases have total mass 1/4. With the exact
source pencil cost 5D_F lambda_F and A<=4m, the complete bound is

    sigma_F/W <= (280/3)sqrt(m)D_F lambda_F+4sqrt(m),

so Q5's 128 is safe. The parked Newton accumulator is charged as space
and ordinary work, not incorrectly transformed with every active pencil.
Shared endpoint scheduling is retained; only ordinary scalar work is
overcounted in the auxiliary audit.

## 2. Parameter inequality Q4--Q7

For the interchange loss, d in [100J,200J) gives
`3x/d<=0.03x/J` and `10d^2 log2(4x)<400000J^2 log2(4x)`.
At x0=2^40 J^3 log2 J, J>=3, the bound
`log2(4x0)<32log2 J` holds, and the displayed 400002 coefficient costs
less than x0/(4J). The ratio log2(4x)/x decreases beyond that point.
Thus all constants, leading padding and reserves fit a strict margin
below x/(2J). The Fourier loss `2x/L+O(L log x)` is smaller and fits the
quarter pre-padding margin. The stated finite label guards also hold.

The actual power-of-two exponent trials overshoot this sufficient x by
at most a fixed factor. Every trial constructor terminates, so Q7 is a
generation bound rather than advice or an unbounded initial search.

## 3. Finite data Q8

The count formula, full-rate module, common finite algebra and all
polynomial/exception tables have the proved actual `2^{m^C}` construction
bound. Contraction adds at most 16m to the batch and polynomially many
description nodes. The completed swap has F2 coefficients; basis descent
preserves independent occupancy and the call ratio. Intermediate F4
transforms are not claimed to act componentwise over F2.

The rational Walsh component has polynomial-m row widths and coefficient
bit heights plus explicitly generated `2^{O(m)}poly(m)` tables. Rational
address dimensions/heights are polynomial under the accepted guards;
their numeric magnitudes, compatibility lists and actual radix are charged
separately. All fit one P_m<=2^{m^C}. No full-alphabet truth table is used.

## 4. Rational numerical preparation and Q9

A stored a/b coefficient is divided once during setup at the chosen
p=O(k) precision, in polynomial(P_m,k) bit work. Above k>=P_m^K, its
prepared dyadic representation has O(k) bits. Every record still uses
the fixed O(k log k) short multiplier. There is neither per-record
schoolbook division nor an uncharged k-squared multiplier.

Finite coefficient heights and update counts give a polynomial(P_m)
logarithmic local norm bound. The source recursion argument makes total
logarithmic amplification polynomial(P_m)*log(2+k). The same cutoff
absorbs this gain, event counts and setup into absolute O(k) precision
and the exponential record volume. Coefficient-rounding errors are
included in that operator/error calculation.

The exact characteristic-two interchanger acts on coordinate-encoded
symbols. Numerical Walsh invokes its completed permutation on encoded
records; rational coefficients are never reduced modulo two. All address
movement, comparisons, endpoint scans and dense coordinate arithmetic are
charged by the finite-template compiler. V/16 and V/8 repair descents and
the existing spatial descent each retain geometric parked volumes. The
substitution adds no uncharged space-depth factor or profile exponential.

## 5. Complete profile and eligibility Q10--Q13

The common-cap/restart wrapper retains generator time, retained workspace,
failed attempts, cleanup and one absolute physical cell cap. Its displayed
threshold includes U_abs. Q7--Q9 give logarithmic prefactors and
`log2 L(N_j)<=2^{O(J^3 log J)}`. The sparse candidate selected in Q11
makes that at most sqrt(s), which proves n>=N_j. The term s/J dominates
sqrt(s) and yields exactly the stated Q13 overhead.

This is an independent mathematical invoice/profile review, not execution
of the entire tape machine. Credits: the source proofs; A's composition;
B's component proofs; Jerry Chen (@CubeJerry); AI-assisted audit.
