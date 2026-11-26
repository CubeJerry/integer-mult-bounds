# Independent review of B's signed-star spectral test

Disposition: **accepted invariant-sector calculation and coefficient-field
obstruction**. Reviewer: E003 routing A. The complete note
`../route-b/STAR-SPECTRAL-TEST-SECTOR.md` was read and its algebra checked
directly. No extra numerical spectrum or full-array diagonalization was run.

Reviewed SHA-256 values:

* Sector note: `bb96bb7063a32387c9fcf8eb2a8115647ffc505953fa4699e97fb6da6761bff6`.
* Family comparison: `cc4fd8c1479352f399490ae68f348d3ccf648f2d6136bb2f64671f994e3d4d78`.

The one-exceptional-letter sector is invariant under every register
permutation, and the star query acts on it as the corresponding ordinary
transposition. The coordinate formula T1 is therefore exact. Positive-leaf
and negative-leaf zero-sum spaces give eigenvalues B-1 and B+1. The stated
three-dimensional quotient in the basis e_0,u_+,u_- is correct. Its row
sums are B, and direct determinant expansion gives
`(lambda-B)(lambda^2-B lambda-(m+1))`. Together these invariant summands
have the full sector dimension m+1 and establish T4 over Q.

For the full nonzero binary column family, a nonzero seed has B=-1.
The radicand 1+2^(r+2) is nonsquare for r>=2: an integer square would
force two powers of two differing by two to be z-1,z+1, hence z=3 and
r=1. Consequently the sector supplies real irrational eigenvalues that
cannot belong to Q(i). The entire operator inherits those eigenvalues,
even if a proposed basis mixes the sector with other coordinates.

The conclusion correctly concerns scalar diagonalization over Q(i),
not rational block forms or larger extensions. Nonzero rational scaling
and rational scalar shifts preserve the irrationality obstruction.
The two-by-two rational-block escape is explicitly retained, as is the
possibility of a newly priced basis for one weighted sum.

B's accompanying `WEYL-STAR-COMPARISON.md` was also read. The star-family
commutator and relative-product tests are correct: ordinary conjugation
fails for m>=2, and two-sided simultaneous diagonalization fails for
m>=3 because P_1 P_2 and P_1 P_3 do not commute. This review does not
claim an independent complete audit of the separate E002 positive Weyl
executor. The distinction between diagonalizing a family and diagonalizing
one symmetric weighted sum is necessary and is stated correctly.

This is independent AI-assisted written review. It does not certify a
tape lower bound, practical compiler, formal-kernel proof or human review.
