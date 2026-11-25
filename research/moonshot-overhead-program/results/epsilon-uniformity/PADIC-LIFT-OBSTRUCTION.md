# The literal label matrix loses its small-rank advantage modulo p²

Status: **proved restricted obstruction, independently reviewed by Routes B and C**. This is
a statement about the source's exact zero/one transfer matrix, its rational
reserve geometry, and factorizations over a ring of characteristic `p²`. It is
not a lower bound for interchange or integer multiplication.

## 1. Why consider a lift?

The compact characteristic-zero predictor uses the integer count of negative
query eigenvalues. The count modulo `p` loses parity information on the source
window, as proved in `INTERCHANGE-OBSTRUCTION.md`. One possible response is to
keep extra `p`-adic digits while evaluating integer-valued polynomials, and then
reduce the output modulo `p`. This response needs more than a larger scalar
alphabet: the shared label transfers must also operate at the greater
precision. Here we examine retaining their **literal zero/one matrix and exact
rectangle cancellation identity**.

The source is the tape manuscript at
`openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`,
`build/interchange.tex`, Lemma `lem:interchange-labels`, equations
`eq:interchange-gram` and `eq:interchange-stage-cost`, and
`eq:interchange-contraction`. All label definitions below are those in that
source. The argument uses the elementary character spectrum of Hamming-distance
matrices; the relevant spectral calculation is included in full.

Fix an odd prime `p`, an integer `q>=2` with `p` not dividing `q`, and set

\[
 h=2p-1,\qquad n_0=q^h,\qquad N=q^{h^2}.
\]

An inner word has `h` letters from `[q]`; two inner words are far when their
Hamming distance is `p`. A label is an `h`-tuple of inner words. The integer
matrix `P_*` has a one on the diagonal and on pairs of labels differing in
exactly `p` outer positions, with far inner words at every differing position.
Its other entries are zero.

For a matrix over `R=Z/p²Z`, define its **factor rank** to be the least `r`
for which it can be written `UV`, with `U` having `r` columns and `V` having
`r` rows. This is the number of scalar intermediate streams in a literal
two-factor linear transfer. It is a different notion from rank over `F_p`.

## 2. Quantitative theorem

**Theorem L1.** The literal matrix `P_*` over `Z/p²Z` has factor rank at least

\[
 M=h\binom{h}{p-1}(q-1)^{h^2-p}. \tag{L1}
\]

The rational address Gram matrix of the same labels has rank `D` satisfying

\[
 D\ge 1+(q-1)^h. \tag{L2}
\]

In particular, if `q>=2h²`, the factor-rank fraction obeys

\[
 \frac rN\ge q^{-p}. \tag{L3}
\]

Suppose a retained reserve layout has `a=D-2`, and parameters `m,alpha`
satisfy `0<alpha<=1` and the necessary reserve inequality `2a<m^alpha`.
Then, in this same range of `q`,

\[
 \frac{mr}{N}
 >2^{-p/h}m^{1-\alpha p/h}
 \ge\frac12m^{(p-1)/(2p-1)}
 \ge\frac12m^{2/5}. \tag{L4}
\]

The original characteristic-`p` proof achieves the much smaller fraction
`O_p(q^{-p²})`. Equation (L4) shows that the literal lift cannot retain both
the reserve inequality and a subpolynomial fresh-query factor `mr/N` by
changing `p,q,m` alone. It concerns the specified transfer factorization and
source accounting, not the time of every possible implementation.

### 2.1 A character basis over a suitable extension ring

Identify the letter set with the additive group `Z/qZ`. Choose a finite field
`k` of characteristic `p` containing a primitive `q`th root. Such a field
exists because `p` is invertible modulo `q`. Lift a monic irreducible
polynomial defining `k` to `R`, and form the finite free extension ring `R'`.
Its maximal ideal is `pR'`, its residue field is `k`, and `p²=0`.

A primitive `q`th root in `k` lifts to a root `zeta` in `R'`: from any lift
`z`, one Newton correction

\[
 z-(z^q-1)/(qz^{q-1})
\]

is a root modulo `p²`, since its denominator is a unit. Its order is `q`,
as this is already its order after reduction. For `q` not dividing `j`,
`zeta^j-1` is a unit, so the geometric sum of the corresponding character
vanishes. The character matrix of `(Z/qZ)^h` is therefore invertible over
`R'`, with the usual inverse divided by `q^h`.

Any `r`-stream factorization over `R` remains one over `R'`. A lower bound
after this extension is consequently also a lower bound over `R`.

### 2.2 The inner spectrum

Let `A` be the inner far-pair adjacency matrix. A character with exactly
`t` nontrivial coordinates has eigenvalue

\[
 \lambda_t=
 \sum_{j=0}^{p}(-1)^j(q-1)^{p-j}
       \binom tj\binom{h-t}{p-j}. \tag{L5}
\]

There are `binom(h,t)(q-1)^t` such characters. Indeed, the generating
function for distances contributing to a character is

\[
 (1-z)^t(1+(q-1)z)^{h-t};
\]

its coefficient of `z^p` is (L5).

Write `c=binom(2p-1,p)` and `beta=binom(2p-2,p-1)`. Two facts will be
used:

\[
 \lambda_h=-c\equiv-1\pmod{p^2},\qquad
 1+\lambda_{p-1}\equiv q^p\not\equiv0\pmod p. \tag{L6}
\]

For the first, in `R` we have

\[
 c=\prod_{a=1}^{p-1}(1+p/a)
   \equiv1+p\sum_{a=1}^{p-1}a^{-1}\equiv1\pmod{p^2}.
\]

The last sum is zero modulo `p`, by pairing `a` and `p-a`.
Furthermore

\[
 \beta=\frac{pc}{2p-1}, \tag{L7}
\]

so `beta` is divisible by `p` but not by `p²`.

For the second fact in (L6), the matrix `I+A` has entries
`1-d^(p-1)` modulo `p`, where `d` is the inner Hamming distance.
Expand `d^(p-1)` as a power of a sum of coordinate inequality indicators.
On a character with exactly `p-1` nontrivial positions, a term survives
only if it uses every one of those positions. Since the total degree is
`p-1`, each is used once, with coefficient `(p-1)!`. Its character sum
is `(-1)^(p-1)q^(h-p+1)`. The constant part contributes zero. Wilson's
identity `(p-1)!=-1 mod p` now gives `1+lambda_(p-1)=q^p mod p`.
Wilson's identity here follows by pairing each nonzero residue with its
inverse; the only self-inverse residues are `1,-1`.

### 2.3 A large eigenblock with valuation exactly one

On a tensor product of inner character spaces with inner eigenvalues
`a_1,...,a_h`, the label matrix has eigenvalue

\[
 1+e_p(a_1,\ldots,a_h), \tag{L8}
\]

where `e_p` is the elementary symmetric polynomial of degree `p`. This
is exactly the choice of the `p` far outer coordinates in the definition
of `P_*`.

Take one inner character of weight `p-1` and all the other `h-1` inner
characters of weight `h`. Put `a=lambda_(p-1)`. By (L6), the eigenvalue
in (L8), modulo `p²`, is

\[
 1-\binom{h-1}{p}+a\binom{h-1}{p-1}
   =1-c+(a+1)\beta
   \equiv(a+1)\beta. \tag{L9}
\]

This is `p` times a unit, by (L6)--(L7). More explicitly, division of
(L9) by `p` and reduction modulo `p` gives `-q^p`, which is nonzero.

There are `h` choices for the distinguished outer coordinate. The
multiplicity is therefore

\[
 h\binom{h}{p-1}(q-1)^{p-1}(q-1)^{h(h-1)}
   =h\binom{h}{p-1}(q-1)^{h^2-p}=M.
\]

The invertible character transform makes these an `M` by `M` diagonal
block whose diagonal entries are `p` times units.

### 2.4 Why this block requires at least M intermediate streams

We use an elementary fact about a ring with maximal ideal `(p)`, residue
field `k`, and `p²=0`: a diagonal `M` by `M` matrix with diagonal entries
`p` times units cannot factor through fewer than `M` columns.

To prove it, suppose `UV` is such a diagonal matrix and `U` has `r`
columns. Use unit row and column pivots to reduce `U` to a block with
an `a` by `a` identity and a remaining block `pC`, where
`a=rank(U mod p)`. These operations are invertible and can be absorbed
into the other factor or the output. Because `UV=0 mod p`, the first
`a` rows of the transformed `V` are divisible by `p`. Divide the
product by `p` and reduce modulo `p`. Its first block has rank at
most `a`, and the remaining block has rank at most `r-a`. Its total
rank is at most `r`. But the transformed diagonal product divided by
`p` has rank `M` over `k`. Thus `r>=M`.

Selecting the eigenblock from any factorization of `P_*` proves (L1).
This argument is needed: ordinary rank after reduction modulo `p`
would see this whole block as zero.

### 2.5 Rational reserves and the cost inequality

Restrict the source Gram matrix to labels in which just one inner word
varies over all `q^h` possibilities. Changing the two vector coordinates
to their sum and difference gives blocks proportional to

\[
 J_{q^h}\quad\hbox{and}\quad J_{q^h}-(2/p)A.
\]

Over the complex numbers, characters of inner weight `h` are nonconstant,
so the second block has eigenvalue `2c/p`, which is nonzero, on a space
of dimension `(q-1)^h`. The first block has rank one. Rank over the
complex numbers equals rational rank for this rational matrix, proving
(L2).

If `q>=2h²`, Bernoulli's inequality gives

\[
 (1-1/q)^{h^2-p}\ge1/2,\qquad
 (1-1/q)^h\ge1/2.
\]

Dividing (L1) by `N` proves (L3), since
`h binom(h,p-1)/2>=1`. Also `(q-1)^h>=2`, so the reserve condition gives

\[
 m^\alpha>2((q-1)^h-1)\ge(q-1)^h\ge q^h/2.
\]

Combine `q^h<2m^alpha` with (L3) to obtain the first inequality in
(L4). The remaining inequalities use `alpha<=1`, `p/h<1`, and
`(p-1)/(2p-1)>=2/5` for `p>=3`. This completes the proof. ∎

## 3. A polynomial version of the same loss

**Lemma L2.** A polynomial over `Z/p²Z` whose values on
`0,1,...,2p-1` are one at `0,p` and zero elsewhere has degree at least
`2p-2`. This bound is attained by `(1-X^(p-1))²`.

For a unit residue represented by `a in {1,...,p-1}`, the polynomial
vanishes at both `a` and `a+p`. Taylor expansion modulo `p²` gives
`f(a+p)=f(a)+pf'(a)`, so its reduction has a double root at every
nonzero residue. The reduction is nonzero at zero. It must therefore
be divisible by `(X^(p-1)-1)²`, proving the lower degree. The displayed
polynomial has the required values: its inner factor is divisible by
`p` at every unit, and `p^(p-1)` is divisible by `p²` for odd `p`.

This degree statement alone would not imply a matrix-rank lower bound;
Theorem L1 supplies that missing spectral argument directly.

## 4. Scope and the resulting research choice

Theorem L1 applies to the literal integer `P_*`, not every possible lift
of its reduction modulo `p`. Lifting a small factorization instead can
keep its small factor width, but changes the entries by multiples of `p`.
The exact rectangle cancellation then leaves extra transfers to be
computed. The theorem does not rule out a new economical correction for
those transfers, nor new labels, nonlinear data operations, division-based
protocols, or higher-count-digit representations with a different layout.

Keeping higher `p`-adic precision also does not by itself make an ordinary
scalar polynomial in the count a parity predictor. For counts differing
by `p`, every such polynomial has equal outputs modulo `p`; the desired
signs differ by `2` modulo `p`. This remains true over `Z/p^sZ` for every
`s>=1`. A successful divided-power approach would need genuinely charged
division by nonunits or additional query information.

The quantitative obstruction directs the next attempt toward a new
transfer/correction mechanism, rather than a literal lift of the existing
low-rank label matrix. It neither invalidates the published characteristic-
`p` construction nor supplies a lower bound on its actual running time.

Prepared for @CubeJerry with substantial OpenAI AI assistance. The source
label construction and the standard character/finite-ring tools are
credited above. Novelty relative to all literature has not been established;
the claim here is a proved source-specific consequence with explicit scope.

## 5. Independent review and complementary concurrent result

Independent reviews appear in `route-b/independent-reviews.md` and
`route-c/PADIC-LIFT-REVIEW.md`. The exact root verifier is
`verify_padic_lift.py`; Route C also made a separate finite checker.
These support the written proof without materializing the full outer matrix.

Concurrent S002 checkpoint `96028cba1342c02bdca1f537ae9a80485087bdf3`
contains `../interchange-lift-barrier/PROOF.md`. Root read that proof.
Its entrywise-product identity `P entrywise (pJ-K)=p diag(P)` proves
`r rank_Q(pJ-K)>=N` for every support-preserving unit-diagonal lift over
`Z/p^eZ`, `e>=2`. It also proves the literal matrix nonsingular over Q
for power-of-two q. These are broader support/modulus statements.
Theorem L1 here gives a stronger explicit large-q factor-rank fraction
for the literal matrix modulo p². The two proofs have complementary
scope and separate provenance; neither is claimed as an unrestricted
computational lower bound or a priority result.
