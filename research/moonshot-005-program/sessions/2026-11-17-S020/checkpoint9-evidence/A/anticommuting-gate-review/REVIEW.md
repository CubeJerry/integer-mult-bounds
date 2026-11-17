# Independent review: the specified C-prime column has envelope rank six

**Accepted with its stated scope.** The particular cancelling last column in
Worker B's changed first interface cannot occur in a complete independent
Gaussian (4,2,1) endpoint factorization in the fixed finite prefix-matrix /
collective root-four tail model. This also excludes invertible ordinary right
basis changes of this column. It does not exclude other columns for C-prime,
arbitrary source interfaces, or broader tail-operation models.

The positive C-prime and Q0 words, their inverses, and their cancellation
identities remain valid. No source word, existing conditional kappa, or
foundational obligation is changed by this review.

## 1. Independent reconstruction and exact evidence

`check.py` imports no author arithmetic, builder, or matrix routines. It pins
the retained source and the three reviewed author files, then reconstructs the
16-letter permutations and phases and all prefix matrices directly using Sympy
exact Gaussian rational arithmetic. Its operation is a tensor-word algebra:

    sum_h c_h tensor h^(tensor W).

The checker groups only exactly identical tail matrices h. It never replaces
distinct tensor words by a linear dependence observed at width one. Thus its
source expansion and cancellations are literal identities for all tail widths,
not numerical or single-width rank evidence.

Starting with the literal rotations, it reconstructs

    Cprime = diag(I,J,I) Rot02(T) Rot12(R) Rot01(S),
    L = [[a,0,0],[I,a,0],[0,0,I]],
    Unative = [[a,-a^2,0],[0,a,0],[0,0,I]],
    p = U(I-S2)/2, z = R H U(I+S2)/2, w = V.

It expands the complete column L Cprime Unative (p,z,w)^T with a separate
formal source degree. The degree-zero and degree-three terms cancel exactly
as tensor words. Every surviving degree-one tail has two nonzeros per row;
every surviving degree-two tail has four. The quadratic column agrees with
the literal path expressions

    f2_0 = a c00 a p + a c01 a z,
    f2_1 = a c10 a p - c00 a^2 z + a c11 a z,
    f2_2 = -c20 a^2 z.

The checker retains and independently verifies the zero middle term, rather
than assuming it away. It also verifies c20 a^2 z = a^2 z. After exact
grouping there are respectively four, four, and two nonzero tail words in
the three output rows.

Writing u=A0^2, the four tail words are

    u, u s2, u s1, u s1 s2,

with the actual ordinary factor K0 on the second output row. K0 is checked
to be a root-four monomial unitary and aJ=KaS is checked exactly, including
the prefix sign. The identity u s2 = SWAP_cd u merges the first two words
into one left ordinary coset. The other three representative pairs have
relative matrices with exactly four nonzero entries in every row. Hence
none is a scalar multiple of any monomial, and the three left ordinary
cosets are distinct even projectively. These are exact support certificates,
not a search over a selected ordinary catalogue.

All four 4-by-4 prefix coefficient matrices for every output row are recorded
in `output/RESULT.json`. Trivial ordinary-tail evaluation gives a 12-by-12
coefficient envelope, separated into the two sigma signs. There are no
cross-sign entries. Each 6-by-6 sign sector has equal consecutive column
pairs and therefore rank at most three. Independent determinant computation
gives the following exact nonzero minors (zero-based indices):

| Sigma sign | Rows | Columns | Determinant |
|---|---|---|---|
| +1 | 0,1,5 | 0,2,4 | i/64 |
| -1 | 0,1,2 | 0,2,4 | (1+i)/128 |

Consequently both sectors have rank exactly three and the complete envelope
has rank exactly six. The explicit minors themselves, as well as their
determinants, are saved in the result.

## 2. Why the endpoint forces a capacity of four

This part is a proof review; finite matrix checks alone would not establish
the endpoint obstruction.

Assume the claimed independent endpoint factorization exists, with an actual
ordinary output unit O and its actual inverse. Let C2 be the four-prefix-
dimensional whole-bank encoder for its quadratic job and D2 the corresponding
decoder. Then D2 C2=I and

    Pi2 = C2 D2 = O diag(0,I,0) O^-1.

Pi2 is therefore a specific ordinary operator furnished by the alleged
endpoint. No executable Gaussian-class projection is being granted.

Take the finite group of projective root-four monomials containing all the
ordinary tail words in these finite endpoint expressions and in the source.
At widths W divisible by four, its scalar root-four cocycles disappear, so
collective tensor powers give an ordinary group-algebra representation.
For any fixed finite set of pairwise projectively distinct unitary tail
matrices, the normalized Hilbert--Schmidt Gram matrix of their W-th tensor
powers has diagonal entries one and off-diagonal entries whose absolute
values tend to zero. This follows from strict Cauchy--Schwarz: equality of
the normalized inner product's absolute value with one would imply that
the two matrices were projectively equal. The Gram matrix is consequently
nonsingular at all sufficiently large admissible widths.

This argument applies both to ordinary group words and to the finite union
of source cosets appearing after multiplication. It supplies the required
coefficient faithfulness; an isolated small-width physical rank does not.
Different Gaussian classes have different tail row-support sizes, preserved
by ordinary left and right monomials. They are therefore projectively
distinct. Applying faithful class separation to the actual endpoint identity
gives Pi2 f2=f2 for this column's quadratic part.

Now apply the trivial group representation epsilon(g)=1 to the ordinary
coefficient identities, retaining the four physical prefix coordinates.
Because D2 C2=I is a faithful group-algebra identity,

    epsilon(D2) epsilon(C2) = I4.

Thus epsilon(C2) has rank four, epsilon(D2) has rank four, and
epsilon(Pi2)=epsilon(C2)epsilon(D2) has rank exactly four. The distinct left
source cosets cannot mix under left ordinary multiplication. For each one,
the corresponding 12-by-4 coefficient block F_h must satisfy

    epsilon(Pi2) F_h = F_h.

Their concatenation therefore has column space inside a rank-four image.
The independently verified rank-six envelope contradicts this implication.

If the fixed prefix has further unused identity factors, the source envelope
rank and whole-bank capacity become respectively 6m and 4m. Allowing arbitrary
ordinary mixing on that enlarged fixed prefix does not remove the rank gap.

## 3. Scope and boundary checks

The argument uses the specified column, a finite fixed prefix, a fixed finite
collective root-four tail catalogue, and an actual independent one-whole-bank
endpoint for each of the three indicated Gaussian classes. It permits
ordinary sums and nonlinear tail permutations inside this catalogue, arbitrary
ordinary endpoint units and inverses, arbitrary other columns of the source
completion, and any permissible quadratic endpoint head. The quadratic head
need not be one of the three displayed source representatives: the proof uses
the actual output projector, not a selected head normal form.

For an invertible ordinary right basis change R of this fixed column, class
separation would give Pi2 f2 R=f2 R. Multiplying by the actual ordinary inverse
of R recovers Pi2 f2=f2, so the same contradiction applies. This does not
assert that the displayed numerical envelope itself stays unchanged under R.

The review does not cover a different cancelling column for C-prime,
width-dependent unbounded catalogues, unspecified noncollective tail
operations, or a model lacking the independent whole-bank endpoint. It does
not promote the finite exact determinant checks to a universal interface
classification. Physical separation of the linear and quadratic images is
compatible with this obstruction: the missing condition is containment in an
actual ordinary whole-bank encoder image uniformly in the retained model.

## 4. Reproduction

From the session workspace:

    python workers/A/anticommuting-gate-review/check.py \
      --repo source \
      --author workers/B/anticommuting-column-envelope-gate \
      --out /tmp/anticommuting-gate-independent

Python and Sympy are required. `--out` makes reproduction leave frozen
evidence untouched. The source arithmetic file is authenticated but never
imported; the reviewer reconstructs its monomial definitions independently.
The author proof, checker, and result are pinned before comparison.

Review author: Worker A, S020, 2026-11-17. Credit the retained source authors,
Worker B's construction and gate, root's changed-interface proposal and
source review, and substantial OpenAI assistance.
