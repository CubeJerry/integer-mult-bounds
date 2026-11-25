# Independent review: embedded subfields and low-bit coefficient packing

Reviewer: E002 Route C. Status: **PASS for the stated optional components**.
Neither component changes the admitted unconditional envelope by itself.

Reviewed Route A artifacts:

- `EMBEDDED-SUBFIELD-ENUMERATION.md`, SHA-256
  `9cc550a9850b021cfc73b92170cc0d72b43f868dd6db7c8239cd6f76c381b600`.
- `LOW-BIT-COEFFICIENT-PACKING.md`, SHA-256
  `0d231ce8e872f577cfee1eca3074a4f418fbfd2e6d8db05b2f99ec3ad41bfa89`.

## 1. Embedded local fields

The binary matrix of `x -> x^(2^r)+x` is constructible by at most `rS`
root-field squarings plus additions. Root-field arithmetic, dense binary
elimination and even sequential searches for matrix positions have fixed
polynomial cost in S. Thus no enumeration of the root field is hidden in
the subfield construction.

When `r|S`, the polynomial `T^(2^r)-T` divides `T^(2^S)-T`. The latter
splits into the distinct linear factors indexed by E; both derivatives
are one. The former therefore has exactly `2^r` roots in E. Closure under
addition, multiplication and inversion proves that the kernel is the
embedded field, and its binary dimension is r. Enumerating all binary
linear combinations of the computed basis is injective and requires an
r-bit counter and an S-bit accumulator after the basis is stored.

Taking root and local degrees to be powers of two makes the divisibility
an actual invariant. The least suitable local degree satisfies
`B<=2^r<4B^2`, including the small B cases. Since `r>=2` is even, its field
contains the same supplied order-three root omega as the root field.
Vandermonde matrices on distinct local nodes remain nonsingular over E.
No arbitrary E-valued payload is truncated to the local field.

The coefficient-extraction identity is accepted for the index range
`0<=i<s`, which is the range explicitly stated in the supplying lead
`streamed-lagrange-coefficients.md`, Lemma SL1. For `deg L_j<=s-1<q-2`,
the exponent differences lie strictly between `-(q-1)` and `q-1`.
Multiplicative character orthogonality leaves just the coefficient with
matching exponent, with sum `q-1=1` in characteristic two. If read as an
identity for arbitrary i, the displayed formula would alias exponents;
the local note should repeat `0<=i<s` for clarity. This is a scope
clarification of its cited SL1, not a new assumption.

The optional component correctly leaves comparison/count alignment,
field preparation, endpoint payload storage and removal of metadata to
their separate suppliers. Polynomial(S) local descriptor storage does
not become a separate matrix at every spatial input location.

## 2. Full-rate low-bit packing

In the layout

`[P][X_H][X_L][G][Y_H][Y_L][B]`,

the complete `Y_L` coordinate has d values, exactly the number of binary
coordinates in one E element. Moving it past B and grouping those d bits
therefore produces `V/d` arbitrary E elements and still exactly V binary
coordinates. There is no zero embedding. The assumption that the high
interchanger accepts arbitrary E input is essential and is explicitly
present.

The high interchanger treats `[X_L][G]` as its gap and swaps only X_H
with Y_H, leaving coefficient positions fixed. Unpacking then gives

`[P][Y_H][X_L][G][X_H][Y_L][B]`.

The final low-field swap gives

`[P][Y_H][Y_L][G][X_H][X_L][B]`,

which is the required full-coordinate permutation. This checks arbitrary
independent basis bits, including nonzero coordinates of every E element.
Each packing or low-coordinate move is a composition of O(t) complete
binary-coordinate rotations, each of which uses O(V) sequential movement
on a fixed number of reusable tapes. Hence the wrapper adds O(tV) time
and O(V) visited payload cells. Its space statement does not incorrectly
replace the high routine's separate space invoice.

With a polynomial root-node requirement, the chosen degree is
`d=O(log(U+2))` and `t=O(log log(U+4))`. The finite guard covers small U,
and the exponential input-volume lower bound absorbs separately charged
polynomial-U field preparation eventually. The text correctly avoids
reinvoking the public zero-embedding wrapper inside this full-rate
composition.

The note preserves E003's provenance for the general scalar-descent
principle and attributes only the low-address-block specialization to
the E002 proposal. This review makes no priority claim.

## 3. Independent finite replay

Copied checkers and their notes were run in the isolated
`replay-optional-packing` subdirectory; no Route A files were changed.

- Embedded fields: nine kernels, 306 emitted elements, 66,108 closure
  pairs and 1,200 coefficient checks passed. The replay also observed
  628 wrong-exponent failures, five nondivisibility failures and five
  degree-alias negative controls.
- Low-bit packing: 360 complete layouts and 835,488 position checks
  passed, including 270 nontrivial packings. Omission of the low swap
  and reversal of the coefficient basis failed in all 270 applicable
  negative controls each.

These finite checks support the exact algebraic/layout identities.
The all-width and fixed-tape bounds rely on the written primitive
composition; neither checker simulates a full asymptotic machine.

Credits: @CubeJerry; the standard Frobenius and scalar-descent facts;
Route A's constructive notes, E002 lead's optional specializations and
the explicitly credited E003 predecessor; substantial ChatGPT
multi-agent assistance.
