# Review of the sharper rational-geometry bound

Status: **review passed**. Independently reviewed
`../route-a/rational-geometry-height.md` on 2026-11-25 against the pinned
source Gram and endpoint definitions already inspected for the tower audit.

The first principal-minor claim is valid for **any** set of `D` independent
columns of the symmetric rank-`D` Gram matrix. Their original generator
classes are linearly independent in the quotient by the radical and hence
form a basis of that quotient. The induced pairing is nondegenerate on the
whole quotient, so its matrix in this basis, the corresponding principal
submatrix, is invertible. No positive-definiteness assumption is needed.

The coordinate formula `M^-1 A[J,t]` follows by pairing the original
generator with that quotient basis. Its common denominator is the one
nonzero determinant. The stated Leibniz determinant bound supplies
`O(D log(2pD))` bits for numerator and denominator.

The projection-column complement basis is also sound in an indefinite
pairing. The two distinguished vectors have Gram matrix `I_2`, so
`I-x(x^T K)-y(y^T K)` projects onto their orthogonal complement and
has rank `D-2`. Its entries have denominator dividing `p Delta^2`.
Selecting columns preserves that bound and avoids a long sequence of
normalized vectors. Rectangle difference vectors already use the common
quotient coordinates. Appending coordinate vectors gives the required
complement, and the source's lifted vectors stay at the same polynomial
height. The source orthogonality argument gives their independence.

For lower-lower factorization, one may analyze the chosen pivot order by
reordering the active rows and columns in the determinant formulas without
implementing those reorderings physically. The remaining entries are
Schur complements and hence ratios of minors of the original cleared
matrix. Pivots and elimination multipliers therefore have polynomial
bit lengths. Products of polynomially many elementary factors, and their
inverses, have polynomial bit lengths by the product-of-row-sums bound.
The requirement that the implemented factors are lower triangular does
not invalidate this height argument.

There are at most `N^2` nonempty disjoint rectangles, at most polynomially
many endpoint incidences, and at most an additional factor `m` from
query placement. Since `N<=m^4` and `p,D` are polynomially bounded in
`m`, both the total number of entries and their bit lengths are
polynomial in `m` with absolute degrees. Thus the product of the absolute
values of their nonzero numerators and denominators also has polynomial
bit length. Taking absolute values makes the bad-prime product positive.

Enumerating all minors and evaluating them by Leibniz expansion takes at
most `2^(poly(m))` bit work. Ordinary sequential storage and array scans
do not exceed that budget. This is enough to establish the double
exponential address-generation and value bound in the parameter `Z`.
It leaves the separate scalar matrix-root row count as the dominant
triple-exponential contribution, exactly as the note states.

No numerical test is needed to validate this refinement: its remaining
claims are finite-dimensional determinant identities and explicit
dimension/height bounds. It introduces no new complete endpoint claim.
