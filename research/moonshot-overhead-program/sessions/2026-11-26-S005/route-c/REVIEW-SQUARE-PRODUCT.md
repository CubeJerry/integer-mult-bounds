# Independent review of square-product star obstruction

**Verdict: SP1--SP3a and SP3f accepted within the stated square-product model.**
No tape-time, whole-pencil or multiplication lower bound follows.

Reviewed source: ../route-a/square-product-star-obstruction.md.
Final reviewed proof hash: bd4749fef46737e2196f70091d3e9e18fc9176c4e054378aa771571b2438a28c.
The affine-Newton scope clarification and SP3f extension were read and accepted; the
independent replay was refreshed against these exact bytes.

## Actual physical sectors

The words with exactly one distinguished letter form a literal invariant
$(m+1)$-coordinate subspace in every complete register array with alphabet
size at least two. Its trivial and zero-sum sectors have dimensions $1,m$.
Both scalar row maps and row-controlled register permutations preserve them.
Use orthonormal real bases for norm claims; a rational coordinate basis in
a determinant checker is not necessarily orthonormal.

The connection to the source was checked against E003's star normal form,
its signed spectrum, and the actual Fourier kernel.tex endpoint subsection.
For a fixed free pair the star sum is the exact middle operator after
query-independent auxiliary endpoints, on arbitrary full-rate inputs.
Those endpoint transforms and general pointwise phases need not preserve
the sectors, so the conclusion is confined to the exposed middle cut.

## SP1: arbitrary square row mixing

A row factor has determinants $\det A$ and $(\det A)^m$ on the two sectors.
A controlled register permutation has determinants $1$ and $\pm1$.
Multiplicativity and squaring give
$$
\det(O_1)^2=\det(O_0)^{2m}.
$$
No inverse, commuting-mixer assumption, conditioning bound or low-rank
hypothesis is used. Singular mixers make both sides zero. If the trivial
target is invertible, every row factor was invertible, forcing every
positive-dimensional invariant restriction of the product invertible too.
The characteristic-zero exact version is algebraic; orthogonality is only
needed for the real analytic consequences.

## SP2: unweighted approximation

The unweighted star has standard-sector eigenvalues $m-1$ (multiplicity
$m-1$) and $-1$ (once). Hence for $m\ge2,\alpha\ge0$,
$$
F_0=(\alpha+m)I_R,\qquad \|F_1\|=\alpha+m-1.
$$
If the error is $\varepsilon<1/2$, every trivial singular value is at least
$\alpha+m-\varepsilon$, while every standard singular value is at most
$\alpha+m-1+\varepsilon$. SP1 equates their geometric means, contradicting
$\varepsilon<1/2$. The normalized lower bound
$1/[2(\alpha+m)]$ is correct. Nonnormal products and ill-conditioned
intermediates do not escape the argument. The excluded case $m=1$ is
genuinely different: one star is itself a permissible permutation.

## SP3 and SP3a: signed seed batch

For $m=2^r-1$, $r\ge2$, seed zero has sum $m$ and every other seed has sum
$-1$, making the full trivial restriction invertible. Each nonzero seed
has $(m+1)/2$ negative leaves. Differences of their coordinates have zero
center contribution and leaf coefficient $B-b_j=0$, yielding a standard
kernel of dimension $(m-1)/2$ per nonzero seed. This contradicts SP1 even
if mixers couple all seeds.

The total standard dimension is $D=m(m+1)$, with nullity at least
$h=m(m-1)/2$, so $h/D\ge1/4$. At error $\varepsilon<1/2$, singular-value
perturbation gives at least $h$ standard singular values at most
$\varepsilon$ and all at most $m+\varepsilon$. SP1 implies
$$
\frac12\le1-\varepsilon
 \le\varepsilon^{h/D}(m+\varepsilon)^{1-h/D}
 \le\varepsilon^{1/4}(m+\varepsilon)^{3/4}.
$$
The last inequality is correctly directed since
$\varepsilon/(m+\varepsilon)<1$. Taking fourth powers and
$m+\varepsilon\le3m/2$ yields $\varepsilon\ge1/(54m^3)$.
Independent copies preserve this ratio. Scalar closure of the product class
gives $1/(54m^4)$ for target divided by $m$.

SP3 concerns the pure signed-star batch. It does not automatically concern
a shifted affine Newton update, a whole predictor, or cancellation across
rectangles. SP2 only supplies its stated nonnegative shifts of the unweighted
star, not every row-dependent signed shift.

## SP3f: the exact characteristic extension

The all-equal physical address supplies a one-dimensional invariant line
over every field, without dividing by \(m+1\) or decomposing the natural
permutation module into trivial and standard summands. Each controlled
register permutation fixes that basis vector. On the independent seed rows,
the target is \(\operatorname{diag}(m,-1,\ldots,-1)\), which is invertible
when the characteristic does not divide \(m\). Consequently every square
scalar row factor is invertible, and so is the entire physical product.

For any nonzero seed there are at least two negative leaves. The
difference of their one-special-letter basis vectors is nonzero over
every field, including characteristic two; direct signed-star action
annihilates it. The exact target is therefore singular on the full space,
contradicting the preceding conclusion. This proves SP3f without applying
the characteristic-zero determinant argument in a field where its sector
decomposition may fail. If the characteristic divides \(m\), the fixed-line
target is singular and this argument no longer applies; that exclusion is
real. The extension does not make rational predictor denominators invertible.


## Scope controls and decision

A physical diagonal phase that is minus one on the distinguished-center
word and plus one on the other one-special-letter words sends the all-ones
vector outside the trivial line. This is a concrete address-dependent source
operation breaking the determinant hypotheses.

Initialized scratch, rectangular encoders/decoders, discarded outputs,
addition of products, sector-mixing physical maps and whole-pencil
cancellation remain outside the theorem. An orbit executor is not excluded
merely because its target belongs to the group algebra.

The result justifies stopping the proposed same-row-dimension product of
scalar mixers and controlled register permutations, including full-rank
mixers and unlimited calls. It does not justify stopping all joint
movement or full-rate star algorithms.

## Independent exact replay

Command: python3 -I -B verify_square_product_independent.py

A new SymPy checker, without imports from the author's checker, constructs
physical one-special-letter orbits and dense/singular products before
changing basis. Passed: 166 physical actions, 18 exact mixed products,
six positive spectra, 56 signed seed kernel blocks and six address-phase
scope controls. It also checks the nullity ratio and rational constant.
The characteristic extension adds 265 exact finite-field kernel checks,
19 invertible fixed-line cases, and five excluded-characteristic controls.
Receipt: square-product-independent-verification.json.

These are finite algebra checks. The analytic and unbounded proofs above
carry the theorem; no tape execution or Lean SP proof is claimed.

Credits: Jerry Chen (@CubeJerry), pinned OpenAI Fourier/tape sources,
E003's normal form and spectrum, S003's low-rank-mixer predecessor, S005
discovery's determinant argument, and substantial ChatGPT assistance.
