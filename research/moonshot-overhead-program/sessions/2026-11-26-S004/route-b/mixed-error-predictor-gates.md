# Direct gates for dense small errors with adaptive sparse outliers

Status: **proved scoped supplier gates; independent review and finite
controls pending**. These conclusions are derived from the mixed promise
itself. They do not infer a mixed-error obstruction by separately applying
pure sparsity and pure amplitude statements. Outlier positions may depend
arbitrarily on the input. Neither result is a general multiplication
lower bound.

## 1. Missing-input gate, including coordinatewise nonlinear decoding

Let N independent input variables range over {0,U}, with U>0. The target
output is a permutation of those N variables. For output i let j(i) be
its required input coordinate. Suppose the proposed output C_i, including
any rounding or nonlinear coordinatewise decoding, is independent of
input j(i) when all other inputs are fixed. Its other input dependences
may be arbitrary.

Fix a budget M with `0<M<=U`. Call output i good if

    |target_i-C_i|<M/2.                                    (Mix1)

For every fixing of the other N-1 inputs, the two possible targets are
0 and U, while C_i is unchanged. The two open intervals of acceptable
candidate values are disjoint because their centers are separated by
U>=M. At most one of the two choices is good. Therefore, under uniform
independent input bits,

    Pr[output i is an outlier]>=1/2,
    E[number of outliers]>=N/2.                            (Mix2)

Some input consequently has at least ceil(N/2) outliers. Thus an
all-input mixed promise with at most S outliers requires S>=ceil(N/2).
There is no assumption that outliers have fixed positions or independent
events across output rows.

The same conclusion holds for the one-sided good interval
`0<=target_i-C_i<M`, again when M<=U: the acceptable intervals have
width M and are half-open, so do not intersect even at M=U. If a decoder
has access to other computed rows or to the missing raw input coordinate,
the independence premise must be checked anew; it is not free.

### Application to the regular low-support-degree interface

In the regular monomial representation of commuting cyclic shifts,
the full target shift is a permutation. A matrix polynomial predictor
of support degree t<m omits the monomial containing every one of the m
target shifts. Hence, in each target output row, the coefficient of its
designated input coordinate is zero. This remains true with arbitrary
constant W-by-W coefficient matrices. A decoder that sees only that
predicted output coordinate is independent of the designated input, so
(Mix2) applies with N equal to the full regular payload dimension times W.

When the same ordinary interface accepts independent b-bit digits, one
may choose U=2^b-1. For a multi-component record this requires that the
entire locally decoded output record be independent of the corresponding
input record; an isolated missing bit does not establish that claim.
Any change of alphabet, digit serialization or numeric encoding must
retain the stated two-value independence premise. Under that premise a
small modulus M=2^a<=U cannot turn the interface into a candidate having dense small
errors and o(N) exceptional outputs. This is stronger than a single
large-error witness for the mixed promise. It does not automatically
describe a final integer-product residual after arbitrary later
composition, nor the ordinary basis of every unequal physical spectrum.

## 2. Fixed bilinear candidates with varying outlier sets

Let a,b independently range over {0,U}^h. Let exact convolution output i
have bilinear matrix H_i, let the unrounded candidate be a^T G_i b, and
write

    F_i=a^T(H_i-G_i)b,    Delta_i=H_i-G_i.

Allow a final coordinatewise rounding step with absolute rounding error
at most delta, so the actual integer residual E_i satisfies
`|E_i-F_i|<=delta`. Ordinary nearest-integer rounding has delta=1/2.
Assume every input has at most S outputs for which `|E_i|>=B`, for
some B>0. Put R=B+delta. Whenever `|F_i|>R`, that output is an outlier.

The independently proved two-block sign moment calculation gives

    mu_i=E[F_i^2]>=U^4 ||Delta_i||_F^2/16,
    E[F_i^4]<=9 mu_i^2.                                   (Mix3)

For completeness, substitute `a_j=U(1+x_j)/2` and likewise for b.
The coefficient of x_j y_k is U^2 Delta_(i,j,k)/4, so orthogonality of
the independent sign monomials proves the first inequality. For an
affine sign form Z=c+sum d_j x_j, direct expansion gives E[Z^4]<=
3(E[Z^2])^2. Apply this conditionally in one sign block, then the
Cauchy--Schwarz inequality to the squares of its affine coefficient
forms in the other block, and apply the same one-block bound there.
This gives the factor 3*3=9, including constant and linear terms.

Let p_i=Pr[|F_i|>R]. If mu_i>R^2, splitting the second moment gives

    mu_i <= R^2 + sqrt(E[F_i^4] p_i),
    p_i >= (1-R^2/mu_i)^2/9.                              (Mix4)

Because there are at most S outliers on every input, summing these
probabilities yields the quantitative energy invoice

    sum_(i:mu_i>R^2) (1-R^2/mu_i)^2 <= 9S.                (Mix5)

No independence between different output errors is needed. In particular
there are at most 16S indices with mu_i>=4R^2, and hence at most 16S
indices with

    ||Delta_i||_F >= 8R/U^2.                              (Mix6)

This conclusion permits an input-dependent exceptional-output set; it
is a necessary condition on the fixed candidate's coefficient matrices.

### Rank-deficient output forms

Each convolution H_i is a partial permutation matrix, with all its
nonzero singular values equal to one. If rank(G_i)<rank(H_i), choose a
unit vector in the intersection of ker(G_i) with the active column
space of H_i. This intersection is nonzero by dimension counting, and
H_i acts isometrically there. It follows directly that
`||H_i-G_i||_F>=1`. Hence if R<U^2/4, the number D_rank of these
rank-deficient forms satisfies

    D_rank <= 9S / (1-16R^2/U^4)^2.                        (Mix7)

For R<=U^2/8 this is at most 16S. Thus small dense error plus few
arbitrary outliers cannot be supplied by reducing the individual rank
of most convolution forms in a fixed bilinear candidate. The statement
does not lower-bound the total shared bilinear rank or its tape cost:
one product may contribute to many full-rank output matrices. Algorithms
with nonlinear, input-dependent coefficient matrices are also outside
this model.

For the signed hybrid corrector take B=M/2. For the one-sided version,
an actual residual E_i>=0 is an outlier at E_i>=M, so take B=M.
The corresponding mixed promise gives exactly the all-input hypothesis
above, including rounded candidates if their rounding error is bounded.

## 3. Provenance

The first argument extends the already recorded missing-coordinate
ordinary-error witness by testing an interval of width M, and therefore
addresses the mixed promise directly. The second is the two-block
fourth-moment calculation from the reviewed bilinear supplier note,
applied to the outlier threshold with its rounding guard. Both proofs
are included here to make their additional hypotheses and their limits
explicit. No new anti-concentration theorem, general arithmetic lower
bound or complete multiplier is claimed.

Prepared for @CubeJerry with substantial ChatGPT assistance.
