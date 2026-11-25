# Independent review of S002's characteristic-two count formula

Reviewer: E001 Route C, 2026-11-25. **PASS for the finite algebra,
copied-formula size, syntactic degree, full-row identity and actual
single-exponential generator interface.** This is a written review;
no additional numerical tests or full multiplier execution were run.
The physical/global synthesis is reviewed separately by the lead and
Route A.

## Pinned material read

Repository `CubeJerry/integer-mult-bounds`, commit
`848fbf1d7a5e192aa352d79b4d3e36fa06be21ee`; paths below are relative to
`research/moonshot-overhead-program/`:

- `routes/A/characteristic-two-count-formula.md`, blob
  `7620fb1eb7848d3b6aa48e31fdd07ce275659d1a`, read B1--B11 in full.
- `routes/C/CHAR2-COUNT-BIT-FORMULA.md`, blob
  `76c932ea0845536bbe066f5d5766949c28ab4b75`, read in full.
- `routes/B/review-characteristic-two-count-formula.md`, blob
  `a44f303fdb41f5885daf867036a30c0b9fcc5898`, read in full.

## 1. The polynomial formula size is paid

On Boolean values in characteristic two,
`c_(i+1)=x_i y_i+(x_i+y_i)c_i` is the correct ordinary binary carry.
The preceding carry occurs once, while both operand-bit expressions
occur twice. Counting each copied occurrence gives
`|c_(i+1)|<=|c_i|+4S_i+4`. Including the output sum bit gives the
factor-eight cumulative bound used in B2.

Iterating cumulative summation over the balanced input tree gives
`S_(r,k)<=8^r binom(r+k,k)<=2^(4r+k)`, not a circuit-reuse bound.
Here `r=ceil(log_2 m)` and all retained bit positions are `O(log m)`.
The added constant residue of `-u` costs one more such level.
For `D<=m`, the final copied predictor expression, including every
selected-bit product and every summand, is polynomial in `m`; the
loose B9 bound is sufficient. A literal traversal prints these trees
in polynomial work and space. No reference opcode is needed.

## 2. Degree, negative offsets and the spectral phase

Assign position `i` budget `2^i`. Both carry products have degree at
most `2^(i+1)`, and the output bit has degree at most `2^i`.
The ternary high-bit indicator is actually affine, so assigning it
budget two is safe. Degree is measured in the permitted individual
query powers `C_j` and `C_j^2`; both are allowed atoms of a pencil.

Modulo `T^(2^t)` in characteristic two, `(1+T)^(2^t)=1`.
Since `1+T` is a unit, the residue identity also holds for negative
integer exponents. Binary expansion of that exponent's residue then
proves B7 without division. The product selecting the bits of `h`
has syntactic degree at most `sum 2^k=h`. Thus the entire predictor
has degree at most `D` before any Boolean quotient simplification.

For `0<=c-u<=D`, the truncated binomial sum is `omega^(c-u)`.
Multiplication by `omega^(u-sum beta)` gives
`omega^(c-sum beta)=omega^(sum k_j)`, including the shift wraparound.
The formula agrees with the known predictor also outside the window.
The indicators are Boolean at every allowed spectral tuple. Since
`X^3-1` splits over F4 with distinct roots and unit differences, these
pointwise identities imply the exact commuting-query operator identity,
also after the stated coefficient-algebra extension.

## 3. Full rows and the characteristic-two cyclic sum

The cyclic compiler applies to the actual formal, possibly
nonmultilinear formula. It produces a scalar identity on the whole
grade, not a designated output with zero-filled auxiliary rows.
Scalar coefficients do not add stages; all shifts retain the same
shape. The final degree can be padded to `D` by identities.

For clarity, even factor lengths do not require nonexistent primitive
even-order roots in characteristic two. Write `d=2^a e` with `e` odd
and use a primitive `e`-th phase in the graded sum. The ordinary
root-of-unity identity gives `(U+V)^e=U^e+V^e`; the two terms on the
right commute. Raising to `2^a` in characteristic two yields
`(U+V)^d=U^d+V^d`. The phase also has `d`-th power one, so total-grade
restriction gives all cyclic products with the stated rank `d ab`.
Consequently polynomial formula size gives width `D^poly(m)` and
exactly `O(sqrt m)` active pencil stages for the chosen window.

All `3^m` shifts have equal multiplicity. The window
`B=3 ceil(sqrt m)` has outside fraction at most `2 exp(-9/2)<1/32`.
Fixed duplication makes the containing defect budget integral without
changing its fraction. Every matrix coordinate remains independent data.

## 4. A bounded actual coefficient constructor

The common conductor `M=M0*tau` is odd, includes every needed odd-part
root order, and has numeric value `2^(poly(m))`. The monic cyclotomic
quotient is finite free over F4. Characteristic two does not divide
`M`, so its root-order relations and the power-of-three check nodes
specialize correctly. Their difference inverses follow from the
explicit cyclotomic product equal to three, which is one in F4.
The base-field `omega` need not be identified with a conductor power.

Divisor enumeration, exact monic cyclotomic division, coordinate
arithmetic, expanded matrices, all frequency tables and even exhaustive
spectral validation each cost `2^(poly(m))` actual bit work and space.
No full alphabet truth table is introduced. The directly checked
`D<=m` guard and a valid total small-parameter baseline make this an
actual constructor rather than an eventual existence assertion.

## 5. Scope and provenance

This establishes the specified fixed-field representation IP4. It
does not establish the all-odd-characteristic dyadic MR/IP hypothesis.
The numerical rational Walsh component is separate; no homomorphism
from `Z[1/2]` into characteristic two is asserted here.

The formulas use nonmultilinear intermediates and agree with the count
function on Boolean spectral inputs. Therefore neither E001's nor
S002's matching lower bound for the literal **formal multilinear**
compiler applies. For example the extra repeated-variable terms in
S002 B's four-input carry formula vanish on Boolean inputs in
characteristic two while remaining nonzero as formal polynomials.
This is a substantive change of representation, not an exception to
the lower bound's hypotheses.

Credit for this new count construction and its stronger fixed-field
extraction remains with the concurrent S002 derivation and its named
source dependencies. E001's earlier construction and scoped barriers
retain their separate provenance. The common constant-overhead
endpoint and the all-odd-characteristic representation remain open.
