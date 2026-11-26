# An exact spectral test for a common basis of the signed star pencil

Status: **proved invariant-sector calculation and restricted coefficient
field test; independent review pending**. It goes beyond the query-family
commutator in `WEYL-STAR-COMPARISON.md`, but does not exclude rational
block forms, larger algebraic fields, or a newly priced compact basis.

## 1. An invariant sector in every complete array

Let P_j exchange registers 0 and j and let `S=sum_j b_j P_j`, with
`b_j in {+1,-1}`. Choose two register letters a!=b. The m+1 words
containing exactly one a and otherwise b form an invariant sector.
If e_i is the word whose exceptional letter is at position i, P_j
acts exactly as the ordinary transposition (0,j). Thus this sector is
present for every alphabet of size at least two, including pair registers.

Let p,n count positive and negative weights, m=p+n, B=p-n, and assume
p,n>=1. On the sector,

```
(Sx)_0=sum_j b_j x_j,
(Sx)_j=b_j x_0+(B-b_j)x_j.                            (T1)
```

This small sector has an O(m)-arithmetic implementation with one weighted
leaf sum and a broadcast of x_0. It is not claimed to dominate the full
array; it is a necessary spectral test for a basis of the whole operator.

## 2. Complete exact sector spectrum

The positive-leaf zero-sum space has dimension p-1 and eigenvalue B-1.
The negative-leaf zero-sum space has dimension n-1 and eigenvalue B+1.
Their complementary three-dimensional space has basis e_0,u_+,u_-,
where u_+ and u_- sum the positive and negative leaf vectors. Its matrix is

```
K = [[ 0,   p,    -n ],
     [ 1,  B-1,    0 ],
     [-1,   0,   B+1 ]].                             (T2)
```

The all-ones vector has eigenvalue B. Direct determinant expansion gives

```
det(lambda I-K)=(lambda-B)[lambda^2-B lambda-(m+1)].   (T3)
```

These spaces form a direct sum over Q. The complete sector
characteristic polynomial is consequently

```
(lambda-(B-1))^(p-1) (lambda-(B+1))^(n-1)
   (lambda-B)[lambda^2-B lambda-(m+1)].               (T4)
```

The last two eigenvalues are
`(B +/- sqrt(B^2+4(m+1)))/2`. This is an exact invariant-subspace
identity, not an inference from floating numerical eigenvalues.

## 3. A concrete binary shift-family test

Take m=2^r-1, r>=2, index queries by every nonzero vector a_j in F2^r,
and use the standard seed signs `b_j=(-1)^(a_j dot t)`. For every
nonzero seed t, there are `2^(r-1)-1` positive and `2^(r-1)` negative
weights. Thus B=-1 and the two exceptional eigenvalues are

```
(-1 +/- sqrt(1+4(m+1)))/2.                            (T5)
```

The radicand `1+2^(r+2)` is nonsquare for r>=2. If an odd integer z
satisfied `z^2-1=2^(r+2)`, both z-1 and z+1 would be powers of two
differing by two. They must be 2 and 4, giving z=3,r=1, outside this
range. Already m=3 forces `(-1 +/- sqrt(17))/2`.

This smallest example is a test member, not a claim that the recursive
compiler admits its smallest parameter without a guard. Arbitrarily
large admissible m of the same form have the identical field issue.

## 4. Precise applicability limits

There is no exact **scalar diagonalization over Q(i)** of these signed
star operators at nonzero seeds. The whole operator has the eigenvalues
T5 because the sector is invariant. A diagonal matrix over Q(i) cannot
have a real irrational eigenvalue, because the real elements of Q(i)
are exactly Q. Similarity preserves the spectrum even if the basis
mixes this sector with other coordinates. Nonzero rational scaling and
a rational scalar shift preserve the obstruction.

This distinguishes a basis for one weighted sum from E002's particular
constant-rank Q(i) one-bit diagonalizer. It does not invalidate E002's
positive batching for its commuting Weyl family. Nor does it prohibit
retaining nontrivial row matrices: rational two-by-two blocks can already
realize the quadratic in T3. A larger row interface or rational block
form remains possible and needs separate cost/full-rate accounting.

Adjoining the displayed square root also removes this test-sector field
obstruction. It does not diagonalize the rest of the star representation,
construct its basis, or bound its tape application. Generic diagonalization
of an array-sized matrix is not a compact template supplier.

There is a limited positive reduction: sign patterns with the same p,n
are conjugate by leaf-register permutations. For the full nonzero binary
column family, only two types occur: the all-positive zero seed and the
balanced nonzero seeds. The conditional leaf permutations and any ensuing
common basis still require their physical invoice; no free routing follows.

## 5. Evidence and next target

`verify_star_spectral_sector.py` checks invariant spaces, quotient action,
the determinant polynomial, seed counts and nonsquare controls exactly.
It does not enumerate a basis for the full representation.

A useful next construction would give a compact rational block form or
a priced algebraic basis for the balanced signed-star family, then show
how it composes with full rectangles and successive predictor stages.
The sector above is a concrete test for such a proposal.

Credits: @CubeJerry; E003 A's exposed star kernel; the retained binary
pairwise-shift family; E002 Weyl batching as comparison; substantial
ChatGPT assistance. No general circuit lower bound, full multiplier,
formal-kernel or human review is claimed.
