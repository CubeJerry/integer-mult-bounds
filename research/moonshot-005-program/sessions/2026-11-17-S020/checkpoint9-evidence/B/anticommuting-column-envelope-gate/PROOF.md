# The first cancelling C-prime column has too large an ordinary quadratic envelope

**Scoped endpoint obstruction.** The ordinary interface C-prime, its exact
inverse, paid column completion and cancellation of the ordinary/cubic terms
remain valid. The particular last column in the preceding positive package
cannot belong to a complete independent (4,2,1) endpoint factorization.
This is not an obstruction to C-prime with a different last column.

## 1. Scope and the actual endpoint implication

Use exactly the fixed finite prefix-matrix / collective root-four tail
catalogue of `prefix-anticommuting-first-interface/PROOF.md`. The prefix has
two active bits sigma,tau; identities on unused fixed prefix bits can be
included throughout. The tail width W varies. Coefficients and catalogue
words are fixed independently of W. We restrict the proof to arbitrarily
large W divisible by four, so scalar root-four phases of tail words disappear.
The physical prefix remains unchanged.

Suppose an actual ordinary endpoint unit O and its ordinary inverse factor
the full source as O diag(F4,F2,F1) I, with one independent whole bank for each
indicated Gaussian class. Let

    Pi2 = O diag(0,I,0) O^-1.

This is the **actual ordinary output projector** of the quadratic bank.
Uniform class separation implies Pi2 f2=f2 for the quadratic part f2 of
every source column. This implication does not posit an executable
Gaussian-class projection. It follows from the claimed encoder and decoder.

Let G contain the finite ordinary tail catalogue of these endpoints and all
ordinary tail words in the source. It is a subgroup of the finite projective
root-four monomial group on sixteen letters. At sufficiently large widths
4k, distinct projective matrices in any of the finitely many source cosets
have linearly independent tensor powers. One proof uses their normalized
Hilbert--Schmidt Gram matrix: every off-diagonal magnitude is strictly below
one, and its 4k-th power tends to zero. The same argument gives faithful
ordinary group-algebra identities.

Therefore Pi2 f2=f2 holds coefficientwise in each distinct left ordinary
coset. Apply the trivial representation epsilon:G->1, retaining all four
prefix coordinates. The matrix epsilon(Pi2) has rank exactly four: the
actual encoder and decoder satisfy D2 C2=I, and
epsilon(Pi2)=epsilon(C2)epsilon(D2). Consequently the concatenated ordinary
coefficient envelope of f2 in this representation must have rank at most
four. We will exhibit rank six.

This argument permits arbitrary ordinary sums, nonlinear tail permutations,
arbitrary endpoint units/inverses, arbitrary other columns of the intermediate
unit, and any rank-two Gaussian endpoint head. It does not apply to
width-dependent catalogues of unbounded size or unspecified noncollective
tail operations. Enlarging the fixed prefix by unused identity factors
multiplies both ranks by the same factor and leaves the contradiction.

## 2. Literal source and the specified column

Retain the preceding package's notation

    P=(I+Z_tau)/2, N=I-P, U=(I+X_tau)/2, V=I-U,
    S=Z_sigma tensor SWAP_cd^W,
    S1=a^-1 S a, S2=a^-2 S a^2,
    J=I_prefix tensor (R2^-1 SWAP_ab R2)^W,
    K=a J S a^-1,
    H=c(Z_tau+X_tau), c=(1+i)/2.

K is ordinary, with prefix factor Z_sigma. The actual first interface is

    C-prime=diag(I,J,I) Rot02(Z_tau) Rot12(X_tau) Rot01(S).

The fixed last column is

    p=U (I-S2)/2, z=X_tau H U (I+S2)/2, w=V.          (1)

Write B=X_tau H U, D0=P-NV, D1=P+NV. The exact source identity aJ=K aS
and the proved cancellation of c00 a^2 z and c10 a^2 z give

    f2_0 = (D0 a^2(p+S1 z)+D1 a^2(S1 p-z))/2,
    f2_1 = K U a^2(-(I-S1)p+(I+S1)z)/2,
    f2_2 = -a^2 z.                                   (2)

The checker independently reconstructs the literal source matrices and
verifies this complete quadratic column. The proof uses the exact identity,
not a numerical estimate of its physical rank.

## 3. Three distinct ordinary source cosets

Put u=A^2, s1=SWAP_ad and s2=SWAP_ab on one tail block. The four right
words in (2) are u, u s2, u s1, u s1 s2. The first two belong to the same
left ordinary coset, because u s2=SWAP_cd u. The other two represent distinct
cosets, both from the first and from each other. This is certified directly
by the three relative matrices: none is monomial. Left multiplication by
the ordinary K tail factor changes no coset.

Denote the three representatives by u, u s1, u s1 s2. After trivial tail
evaluation, the coefficient matrices split into sigma signs r=+1 and r=-1.
On the two tau coordinates use

    U = [[1,1],[1,1]]/2,
    B = c [[0,0],[1,1]],
    D0 = [[1,0],[1/2,-1/2]],
    D1 = [[1,0],[-1/2,1/2]].

For sign r the six-row, six-column envelope is the following 3 by 3 matrix
of 2 by 2 blocks, with one block column per source coset:

    M_r = [ ((1-r)D0 U-(1+r)D1 B)/4,
             r(D0 B+D1 U)/4, (D0 B-D1 U)/4;
             r U(-(1-r)U+(1+r)B)/4,
             U(U+B)/4, r U(B-U)/4;
             -(1+r)B/2, 0, 0 ].                    (3)

All entries are exact dyadic Gaussian rationals. Consecutive column pairs
are equal, so each M_r has rank at most three. With zero-based indices:

* M_+ rows (0,1,5), columns (0,2,4) have determinant i/64.
* M_- rows (0,1,2), columns (0,2,4) have determinant (1+i)/128.

Thus each rank is exactly three. Sigma signs are independent direct summands,
so the complete four-prefix-dimensional envelope has rank six. This exceeds
the rank-four image of the actual ordinary quadratic endpoint projector.
The supposed endpoint factorization cannot exist.

## 4. What survives and what changes next

The preceding paid C-prime and Q0 words, all inverses, all source kernels,
the third-row right inverse and the positive cancellation identity remain
unchanged. The fixed column (1) is now excluded from a complete independent
(4,2,1) endpoint, even if its ordinary completion and both endpoint units are
changed. A right ordinary basis change of this last column is also excluded:
it can be absorbed into the ordinary input endpoint, or removed by multiplying
the column equation by its ordinary inverse.

Actual separation of the physical images of f1 and f2 is compatible with this
theorem. The obstruction is the larger whole-bank **ordinary encoder** image
forced by uniform source-coset separation. Further construction must change
the last column, the first interface, or the stated ordinary representation
class. No supplier, improved kappa, or foundational discharge is claimed.

Credit @CubeJerry, the retained source and previous interface authors,
root's C-prime proposal, independent root verification of the positive
interface, and substantial OpenAI assistance.
