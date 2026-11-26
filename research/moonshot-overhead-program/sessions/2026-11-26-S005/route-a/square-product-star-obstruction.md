# Full-rank row mixing does not rescue a square controlled-star product

Status: **proved scoped mathematical statement; independent review pending**.
This closes the arbitrary-square-row-mixer escape left open by S003's
`route-b/joint-lift-product-handoff.md`. It does **not** lower-bound general
linear circuits, tape time, a computation with initialized scratch and
discarded outputs, or integer multiplication. No complete overhead bound
changes.

Sources: programme starting HEAD
`62d9d8e917379cb2edc17c9761e12e2345bc01f4`; OpenAI math
`3344da59991ed94f9ba711217b29c1d760badfa6`. The actual source Fourier
`kernel.tex`, `binary.tex`, `repair.tex`, and tape `walsh.tex` were read.
The useful predecessor interfaces are E003's
`route-a/ROUTING-STAR-TRANSPOSE-NORMAL-FORM.md`,
`route-b/STAR-SPECTRAL-TEST-SECTOR.md`, and S003's regular lift and product
notes. The spectrum calculations below retain E003's credit; the new
ingredient is the determinant invariant of an arbitrary square product,
its approximation consequence, and its application to the actual seed
family.

## 1. Proposed mechanism and budget before the test

After the shared auxiliary Fourier endpoints, one free-pair middle
operator is a weighted star sum

    S_b = sum_(j=1)^m b_j P_j,

where P_j exchanges complete pair register 0 with register j. Each pair
alphabet has Q=2^(2f) letters. The input consists of arbitrary independent
records at every address, with independent seed rows; no invariance under
register permutations is promised.

The tested proposal was to use existing independent seed rows as a
controlled-query index, repeatedly apply a full-rate controlled register
permutation, and use **arbitrary full-rank scalar row mixing** between
calls. If a subpower-m number of such joint calls replaced m separate
interchanges, it could remove the per-query factor in the local movement
bill. A complete improved numerical supplier would still need rectangle
sharing, the remaining scalar operations, initial/final layouts, precision,
repair and constant visited space. Even removing the numerical bottleneck
alone leaves the admitted exact-interchange two-thirds envelope in the
global theorem. Polynomial-x overhead additionally requires an improved
exact supplier and bounded or polynomial-log normalized child mass.

This note tests the algebraic feasibility of that specific product before
charging its physical realization. All row mixing and controlled
permutations are granted free. An impossibility in this generous product
model invalidates this proposal without implying a runtime lower bound.

## 2. Product model and two actual invariant sectors

Let K=R for the approximation statement and any characteristic-zero field
for the exact statement. Let X=Omega^(m+1), where |Omega|>=2 and m>=2.
The symmetric group on the m+1 register positions permutes the coordinates
of K^X. Fix R>=1 independent row fibres.

Allowed operations on K^R tensor K^X are:

1. A tensor I, with A any square R-by-R scalar matrix. A may depend on all
   finite template parameters and may be dense, singular or ill-conditioned.
2. diag(pi(g_1),...,pi(g_R)), where every g_r is any permutation of the
   m+1 register positions, and pi is its action on X.

The circuit is any finite **product** of these operations, with the same
row dimension R throughout. There are no projections to fewer output
rows, zero-initialized extra rows, additions of different products, or
physical gates outside these register permutations. Individual controlled
star transpositions, controlled leaf rotations and arbitrary products of
them are included. The number of factors is unrestricted.

Choose two different letters a,b in Omega. The m+1 words having one a
and otherwise b form a permutation-invariant physical subspace E. Let
e_i denote the word whose a occurs at position i, for 0<=i<=m. Inside E,

    E = E_triv direct-sum E_std,
    E_triv = span(sum_i e_i),
    E_std = {sum_i x_i e_i : sum_i x_i=0}.

These are orthogonal real subspaces of dimensions 1 and m. Every register
permutation is the identity on E_triv and an orthogonal map on E_std.
Every scalar row map preserves both row-extended sectors. These sectors
exist in the actual complete pair-register array for every f>=1; this is
not an abstract replacement by a stronger oracle representation.

## 3. Determinant conservation across sectors

**Theorem SP1.** Let O be any allowed product. Write O_0 and O_1 for its
restrictions to K^R tensor E_triv and K^R tensor E_std. Then

    det(O_1)^2 = det(O_0)^(2m).                         (SP1)

Over R, equivalently |det O_1|=|det O_0|^m. This is valid even when some
row map is singular.

**Proof.** A scalar row map A tensor I restricts to A on the first sector
and A tensor I_m on the second, whose determinants are det A and
(det A)^m. A controlled permutation restricts to I_R on the first and to
a block diagonal matrix of m-dimensional orthogonal permutation
representations on the second. Its determinant is therefore +1 or -1.
Multiply determinants through the product and square to remove the
sign. No inverse, commutation, rank bound or condition-number bound on A
is used. QED.

An immediate equivalent gate is useful: if O_0 is invertible then every
row factor A is invertible, so O is invertible on every invariant sector.
Conversely, if any row factor is singular then every nonzero-dimensional
physical invariant sector has a singular restricted product.

The same proof works for a finite group with a trivial sector and any
d-dimensional orthogonal sector, replacing m by d. Register permutations
are used here to connect the invariant to the actual source star core.

## 4. Uniform approximation obstruction for an unweighted star

Write S=sum_j P_j. Let alpha>=0, and suppose O is intended to implement

    F = I_R tensor (alpha I+S)

on arbitrary full-rate inputs.

**Theorem SP2.** In the real Euclidean operator norm,

    ||O-F|| >= 1/2.                                    (SP2)

In normalized form, no allowed product approximates
I_R tensor (alpha I+S)/(alpha+m) to error smaller than
1/[2(alpha+m)]. The assertion holds for every finite number of controlled
queries and every R, including arbitrary full-rank row mixing.

**Proof.** On E_triv, S=m. On E_std its eigenvalues are m-1, with
multiplicity m-1, and -1, once. One can see this directly: leaf differences
e_i-e_j have eigenvalue m-1, and
m e_0-sum_(j=1)^m e_j has eigenvalue -1. Thus F_0=(alpha+m)I_R and
||F_1||=alpha+m-1 for m>=2 and alpha>=0.

Suppose ||O-F||<=epsilon<1/2. Restriction cannot enlarge this error.
Every singular value of O_0 is at least alpha+m-epsilon>0, so

    |det O_0|^(1/R) >= alpha+m-epsilon.

Every singular value of O_1 is at most alpha+m-1+epsilon, so

    |det O_1|^(1/(Rm)) <= alpha+m-1+epsilon.

SP1 says the two displayed geometric means are equal. Therefore
alpha+m-epsilon <= alpha+m-1+epsilon, or epsilon>=1/2, a contradiction.
For a normalized target use the identical argument with its trivial
singular value 1 and standard norm 1-1/(alpha+m). QED.

The lower bound does not claim to be optimal. Its importance is that
arbitrarily accurate approximation is unavailable, so exact rejection is
not merely a zero-eigenvalue accident. The programme's exponentially
small numerical tolerances cannot overcome this fixed product-model gate.

## 5. The actual pairwise-independent seed signs

The retained rational predictor includes m=2^r-1, r>=2, with leaves
indexed by all nonzero vectors a_j in F2^r and independent seed rows
t in F2^r. Let b_j(t)=(-1)^(a_j dot t). Its middle target is

    F_seed = direct-sum_t S_(b(t)).

This has R=2^r rows; any fixed positive number of independent copies is
also permitted. It includes both the zero and nonzero seed cases.

**Theorem SP3.** No allowed square product computes F_seed exactly, even
with arbitrary scalar mixing across all seeds and arbitrarily many calls.

**Proof.** At seed 0 the sum of signs is m. At every nonzero seed it is
-1. Hence the complete trivial-sector target is invertible. On a nonzero
seed there are 2^(r-1) negative leaves. Choose two such leaves i!=j. The
vector e_i-e_j lies in E_std. From the elementary signed-star action,

    (S_b x)_0=sum_j b_j x_j,
    (S_b x)_j=b_j x_0+(B-b_j)x_j, B=sum_j b_j,

this nonzero vector is killed when B=-1 and b_i=b_j=-1. Thus the complete
standard-sector target is singular. SP1, or the invertibility consequence
after it, rules this out. The argument remains valid if row mixers mix
different seeds: they are unrestricted in SP1. QED.

This uses the kernel already visible in E003's signed-sector spectrum;
that earlier note used the quadratic eigenvalues for a coefficient-field
test, and did not impose SP1 on arbitrary square mixed products.
SP3 concerns the extracted pure signed-star batch. It does not
automatically apply to every affine Newton update A_0+sum_j B_j P_j:
its scalar shift may change sector invertibility. SP2 separately treats
the stated nonnegative shifts of an unweighted star, not all signed
affine pencils.

**Corollary SP3f (exact field scope).** The exact SP3 statement holds
over every field whose characteristic does not divide m, including
characteristic two. For this extension use the one-dimensional line of
the actual all-equal address: every register permutation fixes that
single basis vector. The target on its independent row fibres is still
diag(m,-1,...,-1), hence invertible. Every square row factor must be
invertible, forcing the full physical product to be invertible. The
same negative-leaf difference is a nonzero kernel vector over any field,
a contradiction. No characteristic-zero decomposition or determinant
root is needed. This is an algebraic statement about the specified star
family, not permission to specialize the rational numerical predictor
through its noninvertible denominators.

**Corollary SP3a (numerical robustness).** Over R, every allowed product
has

    ||O-F_seed|| >= 1/(54 m^3).                         (SP3a)

For the target F_seed/m, the corresponding bound is 1/(54 m^4).

**Proof.** The trivial-sector target has minimum singular value 1. The
standard-sector target has norm at most m, by the triangle inequality for
m orthogonal permutations. Each of its m nonzero seed blocks has a
negative-leaf difference kernel of dimension (m-1)/2. Thus its nullity is
at least h=m(m-1)/2 inside dimension D=m(m+1), and h/D>=1/4 for m>=3.

Suppose the error epsilon is below 1/2; otherwise the stated bound holds.
The geometric mean of the singular values of O_0 is at least 1-epsilon.
At least h singular values of O_1 are at most epsilon, and all are at
most m+epsilon. SP1 consequently implies

    1/2 <= 1-epsilon
        <= epsilon^(h/D) (m+epsilon)^(1-h/D)
        <= epsilon^(1/4) (m+epsilon)^(3/4).

Raising to the fourth power and using m+epsilon<=3m/2 gives
epsilon>=1/[16(3m/2)^3]=1/(54m^3). For a fixed number of independent
copies the nullity ratio and the same argument are unchanged. Scaling
the target by 1/m scales the distance bound; scalar multiplication is
an allowed row factor, so the product class is closed under scaling.
QED.

## 6. Scope, escape routes, and research decision

The verdict is to **stop the same-width controlled-permutation product**
as a replacement for the full-rate star sum. Dropping S003's rank-r
restriction on row mixers does not repair it. This is a specific global
mechanism decision, not another optimization of the retained invoice.

Several material escape routes remain, and this theorem must not be
quoted against them:

- A computation with initialized workspace, rectangular encoders and
  decoders, or discarded output rows need not preserve the determinant
  ratio. One regular lifted call already computes S_b on one embedded
  input; its independent-row and volume cost is the separate SL issue.
- Adding separate products is outside the product model. The direct sum
  of m individual star actions computes S_b and violates no assertion.
- Dense physical transforms or physical maps that do not preserve E_triv
  and E_std can change the ratio. Their preparation and tape movement
  require their own full-rate proof.
- Address-dependent diagonal scalings are not generally scalar row maps.
  For example, unequal weights on the one-special-letter addresses send
  the all-ones vector outside E_triv. Such pointwise source operations
  can break SP1; this is explicitly not a theorem about arbitrary
  pointwise operations or the entire source pencil.
- A direct executor on full permutation orbits, with a genuinely priced
  conversion from lexicographic layout, is not an allowed product merely
  because its target belongs to the group algebra.
- An algorithm for the whole source pencil may exploit signed cancellation
  across rectangles and may never expose this individual-pair cut.

The protected positive alternative is now a direct orbit-layout executor.
It would need to move arbitrary data into orbit blocks, apply every
required operation there with O(V poly(m)) work and constant payload space,
and amortize or avoid the layout changes across the complete pencil.
Sorting by the multiset of coordinate values is not free. Ordinary tape
sorting gives an excessive address-length factor, and the present note
does not assert a faster converter or a new complete H.

## 7. Verification and open next questions

The accompanying exact checker tests SP1 on finite arbitrary square
products, including dense/singular row matrices; independently reconstructs
the signed-star kernel and all-positive sector spectrum; checks the exact
determinant mismatch; and exercises rectangular-compression and sum-of-
products controls outside the hypotheses. The unbounded proofs above,
not finite tests, establish SP1--SP3. No Lean or full tape execution is
claimed here. Independent review and its actual scope will be recorded
separately.

Open next questions:

1. Can an actual orbit-layout conversion be charged once across a complete
   pencil and its repair, rather than once per rectangle or Newton stage?
2. Can constant-factor initialized scratch support an explicit useful
   cancellation identity with sublinear queried volume? SP1 deliberately
   does not rule this out, while SL controls only a sum of single-call
   scalar compressions.
3. Which whole-pencil operations preserve an orbit layout, and what is
   the exact cost of those that break it? This is the next decisive test
   for the protected discovery route.

Credits: Jerry Chen (@CubeJerry); OpenAI's November 24 Fourier and tape
constructions; S002 pairwise/Newton rational predictor; S003 regular-lift
and low-rank product investigations; E003 exact star normal form and signed
invariant-sector spectrum; substantial ChatGPT multi-agent assistance.
