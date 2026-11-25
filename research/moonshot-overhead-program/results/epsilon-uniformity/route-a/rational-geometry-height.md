# A sharper height bound for the rational address geometry

Status: **proved refinement, independently reviewed by Route C**; see
`../route-c/RATIONAL-GEOMETRY-REVIEW.md`. This replaces the
deliberately coarse bit-length-doubling estimate in Section 2.3 of the tower
extraction. It does not improve the final envelope while the literal scalar
matrix-root dimension remains triple exponential. The argument uses standard
determinant bounds and an explicitly chosen rational representation.

Source: OpenAI `math`, `3344da59991ed94f9ba711217b29c1d760badfa6`, November
tape `build/interchange.tex`, `eq:interchange-gram`, endpoint preparation and
delivery by low rank; September tape `build/sections/04-swap.tex`,
`lem:lower-lower`. Only the address geometry is bounded here; the scalar
Clifford and Hermite rows remain separately charged.

Concurrent S002 already establishes polynomial rational bit heights by a
fixed-depth minors chain in `routes/A/rational-address-and-generator-bounds.md`
at `96028cba1342c02bdca1f537ae9a80485087bdf3`. The proof below independently
spells out quotient and complement choices; it corroborates that result
and sharpens our earlier coarse invoice, without a priority claim.

## 1. Statement

For the interchange parameters in `elementary-tower-extraction.md`, let
`m=q^(p^2)` and `N=q^((2p-1)^2)<=m^4`. There is a deterministic choice of
all rational quotient coordinates, orthogonal-complement bases, rectangle
complements, endpoint layouts, layout conversions, and triangular factors
such that:

1. the complete list has `poly(m)` entries;
2. every numerator and denominator has `poly(m)` bits;
3. the product `B` of all nonzero numerators and denominators has
   `poly(m)` bits;
4. a literal determinant-based tape generator takes `2^(poly(m))` steps
   and visited cells. Faster elimination is unnecessary for this claim.

All polynomial degrees are absolute. With `log m=O(Z)`, address values,
their product, and generation cost are therefore at most `E_2(O(Z))`.
The common radix remains bounded by `max(W,E_2(O(Z)))` up to an absolute
factor; expanded scalar width `W` still has the old `E_3(O(Z))` bound.

## 2. Quotient coordinates of controlled height

Write `G` for the symmetric rational `2N` by `2N` Gram matrix. Its blocks
are

\[
 (1-k(v,w)/p)I_2+(k(v,w)/p)
 \begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

Thus `A=pG` is integral with entries of absolute value at most `2p`.
Let `D=rank G`, and choose a set `J` of `D` independent columns of `G`.
Then `G[J,J]` is invertible: their coordinate vectors span the quotient by
the radical, on which the induced form is nondegenerate. Any vector in
their span orthogonal to that span is orthogonal to the entire quotient,
hence zero. Let `M=A[J,J]` and `Delta=det M!=0`.

Use the images of the original generators indexed by `J` as a quotient
basis. The coordinate column of generator `t` is

\[
 v_t=M^{-1}A[J,t].
\]

Cramer's rule expresses every coordinate over the *same* denominator
`Delta`. Every numerator and `Delta` is a determinant of order at most
`D` with entries bounded by `2p`. The Leibniz formula gives absolute bound
`D!(2p)^D<=(2pD)^D`, so all these integers have

\[
 H_0=O(D\log(2pD))
\]

bits. The bilinear form in this basis is `K=M/p`. The vectors `x_v,y_v`
retain Gram block `I_2`, exactly as in the source. No square roots or
diagonalization by algebraic numbers are introduced.

A basis and the correct rank can be selected without a unit-cost linear
algebra assumption: enumerate principal minors and take one of largest
nonzero order. A symmetric matrix of rank `D` has such a principal minor
by the argument above. Computing all minors by their Leibniz formulas
takes `2^(poly(N))` bit work with polynomial-length integer entries.
This very wasteful but explicit method suffices for the height claim.

## 3. Complement and endpoint bases

For an orthonormal pair `x,y`, the projection onto its complement is

\[
 \Pi_{x,y}=I-x(x^{\mathsf T}K)-y(y^{\mathsf T}K).
\]

Choose independent columns of this projection as the source basis of
`D_v`. Its rank is `D-2`. Each entry has denominator dividing
`p Delta^2` and polynomial bit length in `(D,H_0,log p)`. Column selection
uses rank tests; it does not form a potentially tall sequence of newly
normalized basis vectors.

For a rectangle, form the differences `u_i-u_0,z_i-z_0` and choose a
maximal independent subset as a basis of `E`. Adjoin `u_0,z_0` to give a
basis of `U`. Choose the complement `C` by appending standard coordinate
vectors greedily until a quotient basis is obtained. Thus the vectors of
`C` have entries zero or one; the chosen `E` vectors are differences of
the already bounded columns.

The endpoint lift of `c in C` is

\[
 c-\langle c,u_i\rangle u_i-\langle c,z_i\rangle z_i.
\]

It again has denominator dividing `p Delta^2` and polynomial bit length.
These lifts and the fixed `E` basis give the source's complement basis;
the source orthogonality argument proves independence. Each full endpoint
layout matrix therefore has polynomial bit length. Its inverse, and the
change between any two such layouts, have polynomial bit length by
Cramer's rule and a matrix product of polynomial dimension. Permuting or
adjoining unchanged spare fields adds only zeros and ones.

The depth of these rational constructions is bounded independently of the
number of labels: each rectangle's data are built directly from the common
quotient columns. A layout is not defined by multiplying through a chain
of all previously constructed layouts.

## 4. Triangular factors and all bad prime divisors

Apply the predecessor's `lem:lower-lower` elimination to a rational layout
matrix of dimension `d=poly(m)` and entry height `H=poly(m)`. Clear a
common denominator first; its bit length is at most `d^2 H`. Every active
Schur-complement entry in pivoted elimination is a ratio of minors of
this cleared matrix. The determinant bound gives polynomial bit lengths
for all pivots and elimination multipliers, regardless of which allowed
nonzero pivot is chosen.

There are `O(d^2)` elementary lower-triangular operations. Their factors
and inverses have polynomial bit length, and so do their products. One
direct bound represents each elementary matrix over its one common
denominator, multiplies those denominators, and bounds the numerator
matrix product by the product of absolute row sums. Its logarithm is the
sum of polynomially many polynomial-height terms. This prices the
triangular factors and their inverses without an exponential recurrence
for unreduced fractions.

There are at most `N^2` nonempty disjoint directed rectangles and at most
`2N^3` endpoint incidences. Every endpoint, singleton and low-rank layout
conversion has polynomial dimension; query positions can add at most a
factor `m` to the list. Hence there are `poly(m)` rational entries in
the whole address table. Multiplying all nonzero numerators and
denominators gives a value `B` of polynomial bit length. Including
numerators of invertible diagonal factors is therefore harmless.

All basis/rank tests and determinants can be evaluated by explicit finite
enumeration in `2^(poly(m))` time. Matrix products of the displayed sizes
and lengths remain within that budget on tapes, even with full sequential
array scans. This proves the statement.

## 5. Consequence and scope

This refinement removes the address geometry as an independent source of
a third exponential in the finite-data bound. It does not remove the
large radix: the source chooses it also above the expanded scalar width
`W`. Improving the full-rate scalar representation while preserving its
odd-characteristic applicability would therefore remain the main change
needed to lower the complete tower height.

No lower bound or novelty claim is attached to this determinant estimate.
It refines a conservative invoice for the pinned construction. Standard
rational linear algebra could improve the generator's time further, but
that improvement is not assumed here.

Credits: @CubeJerry; the pinned OpenAI constructions and their matrix
factorization predecessors; the concurrent S002 source-generator work;
GPT-6 Astra Pro assistance.
