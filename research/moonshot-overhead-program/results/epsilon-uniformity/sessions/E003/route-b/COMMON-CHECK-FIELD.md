# A single check field across changing interchange templates

Status: **proved source-specific representation lemma; independent review
pending**. This closes a compatibility detail for the nonstationary
interchanger. It does not replace the physical executor audit.

Predecessor pin: `a2d9c4b00c02dadf7bdc970acf9190dfabf9ec32`.
Relevant constructions are S002's characteristic-two count formulas,
cyclic factorization and order-three repair, and E002's shift-only
Vandermonde check refinement and on-demand spectral repair. They use
predictor coefficients and order-three spectral values in `F4`. A
finite extension is used only to obtain enough distinct check nodes.

## Statement

Let a finite menu have arities `m<=M`. Suppose its largest number of
shift rows is `B_max<=C M^c`, for fixed absolute `C,c`. For every menu
entry, the predictor cyclic factors have coefficients in `F4`; the
spectral exceptions are identified from order-three eigenvalues in
`F4`; the check matrices are Vandermonde matrices at pairwise distinct
nodes. Their exact repair identities use field arithmetic and division
only by nonzero node gaps and nonzero predictor defects.

**Lemma F.** Every template in the menu can use one common field

```
E = F4[T]/(g),  deg g = q=ceil(log_4(max(4,B_max))).
```

The field can be constructed by one fixed binary multitape algorithm
in `poly(M)` time and space. One element has `2q=O(log(M+2))` bits;
addition, multiplication and inversion have polynomial bit cost in
`log(M+2)`. Every recursive call can preserve this exact encoding.
The completed target remains the componentwise permutation of the
independent input records.

## Proof

There is a monic irreducible degree-q polynomial over `F4`. Enumerate
all `4^q` monic degree-q polynomials and test reducibility by trial
division by all monic polynomials of positive degree at most `q/2`.
A reducible polynomial has a factor in that degree range. Ordinary
polynomial long division on binary-encoded `F4` coefficients costs
`poly(q)` actual fixed-tape steps. The total enumeration is bounded by
`4^(3q/2+O(1)) poly(q)=poly(B_max+1)=poly(M)`. This deliberately loose
method avoids an uncharged factorization oracle.

The quotient by a found irreducible polynomial is a field with `4^q`
elements. Its fixed coefficient-basis representation supplies at least
`B_max` distinct nodes; for each template take the required initial
segment of the same explicit enumeration. Arithmetic by polynomial
addition, multiplication/reduction and extended Euclid has polynomial
bit cost in q. The concrete base `F4` embeds as constant polynomials.

The characteristic-two cyclic factorization identities are polynomial
identities over `F4`, so scalar extension preserves them. The three
spectral values and all finite shift comparisons remain the same.
Every relevant Vandermonde determinant is a product of nonzero node
differences and is invertible in E. The repair proof uses precisely
these inverses and the explicitly nonzero predictor gaps, so the
same identity holds for the new distinct nodes. It does not require
the field to have the smallest possible degree.

The completed operation is an ordinary swap product, whose matrix
entries are zero or one. Applied over E, it permutes all E-valued
records. In the fixed binary basis it therefore applies the same
permutation to each bit component. Thus data initially encoded as
the elements zero and one returns as zero and one, and general
independent field records are also accepted. Intermediate operations
need not act componentwise; their completed target does.

Keep E fixed at the binary root. A smaller child template uses a
subset of the same nodes and operates on the same encoded payload;
there is no extension tower or repeated per-depth representation
expansion. Initial embedding and final decoding cost `O(qV)` for
an original V-bit payload. Its proportional space factor is q,
explicitly retained in the two-scale theorem's polynomial-logarithmic
space bill and paid by the final chunk wrapper. ∎

## Scope

This uses the proved shift-only check structure. It would not justify
changing a construction which required additional template-specific
roots of unity or a spectral transform over the entire growing field.
The power-of-two cyclic factors here have characteristic-two twist one,
and the order-three eigenvalues already lie in F4. Rational Walsh
coefficients are a separate numerical construction and are never
reduced into E.

Next: verify the one fixed dispatcher invokes all field arithmetic and
coefficient access within its local polynomial bill, without carrying
temporary tags into spatial children. Credits: @CubeJerry; the source
and S002/E002 finite identities; standard finite-field existence and
elementary polynomial arithmetic; substantial ChatGPT multi-agent
assistance. No formal or human verification is claimed.
