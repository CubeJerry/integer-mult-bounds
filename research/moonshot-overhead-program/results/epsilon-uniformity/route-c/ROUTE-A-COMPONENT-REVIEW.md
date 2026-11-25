# Independent review of the compact binary kernel and repair compiler

Status: **review passed within the stated local scope**. This review does not
certify a complete multiplication overhead bound. Reviewed on 2026-11-25 by
Route C, independently of the author of the two Route A notes.

## Material inspected

- `../route-a/explicit-binary-kernel.md`, SHA-256
  `2ccc3b19fc28e4b50f9cb225816c22a308f6034bec27242f37f47802b6ce8e87`.
- `../route-a/repair-table-compiler.md`, SHA-256
  `d1a664423c38eddb9a7100595dd0d1813cf4d679ecbb6eccf86b540ea07d2912`.
- OpenAI `math` commit `3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier
  manuscript `build/kernel.tex`, `build/binary.tex`, and the proof of
  `lem:hermite-repair` in `build/repair.tex`.
- S002 `routes/A/compact-complex-predictor.md` at programme checkpoint
  `bbfd1086b7e629375f9891998e4602270d8801cd`, including its actual window,
  finite-field seed construction, real factorization, and precision estimate.
- `../route-a/verify_route_a.py`, replayed with `python3 -I -B`.

The review checked the dependencies rather than treating the source's
fixed-parameter big-O assertions as uniform in growing parameters.

## 1. Binary kernel estimate

The parameter choices satisfy the source's congruence: `m=2^z-1` is odd.
The diagonal of the binary Gram matrix is one, so its rank `g` is at least
one. Expanding it as a constant matrix plus `2t` equality matrices gives
`g<=1+2tq`; no hidden dependence on the growing label length is used in
this bound. This implies `2m<=A<=4m` for the displayed choices.

The free-incidence count has no omitted orientation factor. Once a source
letter is fixed, a first differing bit determines its bit orientation and
the preceding common prefix. There is one equality choice and at most `r`
unequal choices per coordinate. Restricting the products to odd Hamming
distance only decreases the number. Each of the two endpoints is charged,
giving `4g(1+r)^(2t)`. Charged rectangles use a complete common kernel with
`2g` calls, rather than two additional complete kernels. Their total is
bounded by `2g m 2^(2t)q^(-t)` per independent input row. Thus the coefficient
six in the pencil estimate is conservative.

The S002 seed rows remain independent even when their shifts coincide.
The compact predictor has `D` stages; four predictor applications in
binary Hermite repair therefore use `4D` stages. The spectral table really
converts `2s` rows in each direction. At `A` calls per complete conversion,
the repair contribution is at most `4sA/M<=2A/m^3`. No extra independent
input rows are created by these work arrays.

The strict margin follows from the displayed integer inequalities. A useful
explicit check of the only abbreviated comparison is

\[
 (2t-1)\log_2(16t)-12.5-1.5\log_2t>0\qquad(t\ge8),
\]

which proves the prefactor logarithm is at most `6t log_2(16t)` after using
`1+r<=(16t)^2`. The choice of `r` supplies much more slack than this needs.
The exact ceiling identities for the seed field and seed count hold for
the stated `z>=3`, and the formula `log_2 W=6z^2+6z` follows.

Normalization is compatible with the compact replacement. The source's
common binary query kernel uses `2g` normalized axis calls, whose scalar
product is `2^(-gf)`. The two shared partial transforms together use those
same axes. A full spectral conjugation cancels its forward and inverse
normalizations. The product of the queries is already the normalized
target up to signs and a permutation. Replacing the source predictor by
real affine factors introduces a finite real algebraic coefficient set,
not an uncharged width-dependent scalar. The note explicitly avoids
claiming those coefficients are dyadic.

## 2. Repair-table identity and heights

Let `V` be the square Vandermonde matrix on the selected exceptional nodes.
Its inverse orientation in the note is correct: rows are indexed by
nodes and columns by powers. For an error vector supported on `J`, the
first `j` checks give `V e_J`. With

\[
 K=V^{-\mathsf T}\operatorname{diag}(D_z(p_i))V^{-1},
\]

the lifted correction satisfies
`V^T K V e_J=diag(D_z(p_i))e_J`. The remaining rows need not have zero
lifted correction, because multiplication by `p_i-z` annihilates them.
This verifies both the block signs in the table and the source's final
output `g(P)X-PZ+FZ`. Overmarking a correct row in `J` is harmless.

The integer-binomial bound covers negative arguments. All factors in the
falling factorial have magnitude at most `2m`, so
`|binom(c-u,h)|<=(2m)^h`; the stated geometric estimate for `P(c)` follows.
The sum of absolute coefficients of a Lagrange numerator is at most
`(M+1)^(j-1)`. Together with the common denominator, these facts prove the
claimed absolute polynomial bit-height bound and the explicit safe `B_*`.

There is a harmless possible improvement. In fact

\[
 |w_i|\mid(\nu_i-1)!(M-\nu_i)!\mid(M-1)!,
\]

since each side consists of a subset of the corresponding distinct
differences and the second divisibility is a binomial-coefficient identity.
Thus `2F_M^2` would already be a universal denominator. The note's
`2F_M^4` remains valid and does not change its asymptotic result.

## 3. Compiler and conditioning scope

The on-demand algorithm does have finite loops and explicitly bounded
integer operands. Constructing the shifts by the cited bounded-independence
family, evaluating one pattern, multiplying the product polynomials,
performing exact integer divisions, and assembling the table are all
polynomial in `M,m` with an absolute degree. The common denominator avoids
an unbounded rational-arithmetic primitive. No loop over all sign patterns
is needed. Binary long division gives the stated cost per coefficient per
precision bit.

The table-application bit bound presupposes that the incoming entries'
integer parts also fit in `O(P+B_*)` bits. The subsequent wrapper precision
choice, which includes the input exponent `I`, supplies this condition.
Reading the standalone application statement with arbitrary, unbounded
input magnitudes would not be justified. This is an expositional
qualification, not a failure of the compiler or height theorem.

The wrapper's conditioning estimate is valid when query pencils and full
spectral conversions are atomic operations with the advertised accuracy.
Each partial real-factor predictor product has norm at most `2m^D`.
Only a constant number of complete predictor paths, checks, lifts and
tables occur in binary Hermite repair. Dot-product partial sums are bounded
by absolute row sums, so their contribution is polynomial in row count
times the proved coefficient bound; one need not multiply a condition
bound once per scalar addition. This yields the asserted logarithmic gain
bound. The note correctly leaves internal query-routing amplification,
physical alignment, recursive precision, and uniform linear space open.

## 4. Replay evidence and its limits

The checked script completed with exit status zero under isolated Python:

```
python3 -I -B research/moonshot-overhead-program/results/epsilon-uniformity/route-a/verify_route_a.py
```

Its output reported 1,252 exact rational repair cases, including overmarked
exceptions; 40,329 integer-count predictor cases; ten integer-parameter
boundary cases; and five modular-obstruction checks. These finite checks
support the identities and integer arithmetic. They do not prove the
universal inequalities, a full fixed-tape compiler, or an endpoint bound.

No substantive blocker was found in these two component notes. They give a
quantitative binary-kernel call count and a local repair-table compiler,
with exactly the remaining obligations stated in their scope sections.
