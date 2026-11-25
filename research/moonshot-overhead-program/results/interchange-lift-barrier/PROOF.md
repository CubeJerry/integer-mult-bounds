# A rank barrier to same-field and p-adic lifts of the published routing

Status: **proved scoped algebraic obstruction; independent review pending**.
This note concerns the specific label identity and rational Gram geometry in
OpenAI's November 24 tape manuscript, pinned at
`3344da59991ed94f9ba711217b29c1d760badfa6`, `build/interchange.tex`,
Sections "A family of labels" and "A shared application of a sum of swaps".
It is not a lower bound for integer multiplication, arbitrary interchange
algorithms, or all possible p-adic correction schemes.

The source deliberately uses different characteristics for scalar transfers
and address geometry. The ordinary-count obstruction in
`../../routes/C/INTERCHANGE-COUNT-OBSTRUCTION.md` shows that merely increasing
the data characteristic cannot import the compact rational predictor. This
note checks two other tempting changes: moving the low-rank transfers to the
rational field, and lifting their exact support to modulus p squared.

## 1. A general same-field lemma

Let F be a field, and let P,G be N-by-N matrices over F. Suppose

    P_ii G_ii != 0,   and   P_ij G_ij = 0 for i != j.       (1)

Then

    rank_F(P) rank_F(G) >= N.                              (2)

Indeed, write P=UV^T and G=XY^T with their respective ranks r,d. Their
entrywise product factors through rd coordinates: at row i use the vector
whose (a,b) entry is U_ia X_ib, and similarly at column j. Thus
rank(P entrywise G)<=rd. By (1) that product is an invertible diagonal
matrix, proving (2).

In particular, if I=P+E and E is supported only where G vanishes, with
G_ii=1, then P entrywise G=I and (2) applies. No symmetry or positive
definiteness is needed. This is the standard entrywise-product rank argument;
the contribution here is its explicit application to the proposed bridge.

## 2. Application to the source labels

Use the source notation: odd prime p, h=2p-1, q a power of two, inner labels
in [q]^h, and outer labels in ([q]^h)^h. Put N=q^(h^2). Inner words are far
when their Hamming distance is p; k(v,w) counts outer coordinates whose
inner words are far. Let P_* have diagonal one and off-diagonal one exactly
when the outer words differ in p coordinates, all of whose inner words are
far. In particular k(v,w)=p on its off-diagonal support.

Let

    G = p J - K,   K_vw=k(v,w).                            (3)

Then G has integer entries and

    P_* entrywise G = p I_N                               (4)

as an exact integer identity. Each summand of K factors through the q^h
inner words of one coordinate, so

    d := rank_Q(G) <= 1 + h q^h.                           (5)

G/p is the source Gram matrix (<x_v,x_w>) obtained by selecting the first
generator at each label. Consequently d is also at most the source quotient
dimension D. Over any field of characteristic other than p where this
factorization is defined, (4) immediately invokes the same-field lemma.
In particular, over Q any exact support-preserving transfer matrix with
nonzero diagonal has rank at least N/d.

The main source invoice includes

    D(1+lambda)(1 + m r/N),                                (6)

where r is the transfer rank and lambda counts rectangle incidences. If
the transfers and Gram matrix are moved into the same field, (2) forces
D m r/N >= m. Therefore (6) cannot certify a sublinear per-pencil bill
under that change. This is a limitation of the displayed sufficient cost
certificate, not a lower bound on the actual minimum cost of every possible
implementation. A different decomposition or physical layout could require
a different analysis.

## 3. Inner rank over a prime-power ring

For R=Z/p^e Z, define the inner rank of an N-by-N matrix M to be the least
r for which M=AB with A of shape N-by-r and B of shape r-by-N over R.
This is a factorization parameter, not the rank of its reduction modulo p.

**Lemma.** For every e>=2, the inner rank of p I_N over R is exactly N.

The upper bound is immediate. For the lower bound, suppose pI_N=AB with
r<N. A matrix over the principal ideal ring R admits Smith reduction by
invertible row and column operations. In particular there is an invertible
N-by-N U for which UA has at most r nonzero rows. One may see this directly
by choosing a nonzero entry of least p-adic valuation, moving it to the
first position, multiplying its unit part away, and clearing its row and
column: its power of p divides every remaining entry. Iterate on the
remaining submatrix. No more than r pivot rows can be obtained.

Thus UAB has a zero row. But UAB=pU, and an invertible matrix modulo p^e
reduces to an invertible matrix modulo p. Every row of U has a unit entry,
whose product with p is nonzero when e>=2. Hence pU has no zero row, a
contradiction. QED.

The same proof shows that tI_N has inner rank N for every nonzero scalar
t in this prime-power ring. It does not hold over arbitrary non-principal
rings without further hypotheses.

## 4. Exact low-rank routing cannot be lifted unchanged beyond p

**Theorem.** For e>=2, let P be any matrix over R=Z/p^e Z with unit diagonal
and with off-diagonal support confined to pairs satisfying k(v,w)=p.
Then its inner rank r satisfies

    r d >= N,   where d=rank_Q(pJ-K).                      (7)

Proof. The integer matrix G admits an integer factorization through d
coordinates, by integer Smith normal form. Reducing this factorization
modulo p^e gives an R-factorization of G of width d. The entrywise-product
factorization used in Section 1 is valid over a commutative ring, so the
inner rank of P entrywise G is at most rd. The latter is p times an
invertible diagonal matrix. By the preceding lemma its inner rank is N.
This proves (7). QED.

This applies to the exact original 0/1 matrix P_* at every modulus p^e,
e>=2. At modulus p the right side of (4) is zero, so there is no
contradiction with the source's much smaller finite-field rank.

A low-rank lift with new nonzero entries outside the allowed support is
not excluded by this theorem. Those entries no longer cancel using the
source's free rectangles. Their correction must be supplied and charged.
Likewise, a graded or nonlinear digit algorithm which does not factor this
same transfer matrix is outside the theorem. The result rules out a
specific unpaid lift; it does not rule out p-adic research generally.

## 5. The exact source transfer matrix is nonsingular over Q

There is an even stronger fact for the original matrix (not every matrix
with its support): for every odd prime p and every power of two q,

    rank_Q(P_*) = N.                                      (8)

Identify the q letters with the additive group F_2^t, q=2^t. Equality,
Hamming distance, and the two-level far-pair relation are translation
invariant, so P_* is a convolution matrix on F_2^(t h^2). Its off-diagonal
degree is

    Delta = binom(h,p)^(p+1) (q-1)^(p^2).                 (9)

The integer binom(2p-1,p) is even for every odd p>1. To check this without
an external divisibility theorem, let 2^a, a>=1, be the least nonzero bit
of p above its units bit. Then p has bit a equal to one, while 2p-1 has
bit a equal to zero. In F_2[x], the factorization
(1+x)^n=product_(bits b of n equal to 1)(1+x^(2^b)) shows that the
coefficient of x^p in (1+x)^(2p-1) is zero.

Consequently Delta is even. In characteristic two, squaring any convolution
kernel on an elementary abelian two-group cancels every cross term, and
every group element squares to the identity. Its square is therefore the
kernel's total coefficient sum times the identity. The coefficient sum
of P_* is 1+Delta, which is odd. Hence

    P_*^2 = I_N modulo 2.                                 (10)

P_* is invertible modulo two and its integer determinant is odd and
nonzero. It is therefore invertible over Q, proving (8). The same argument
works for every odd integer p>1 in this definition of h and the labels;
primality is needed for the source finite-field construction, not for (8).

## 6. Exact spectral checks without constructing N-by-N matrices

For q a power of two, the inner distance-p adjacency matrix has character
eigenvalues

    kappa(t)=sum_j (-1)^j (q-1)^(p-j) binom(t,j) binom(h-t,p-j),
    multiplicity mu(t)=binom(h,t)(q-1)^t,   0<=t<=h.       (11)

For the outer convolution, a type tuple (t_1,...,t_h) has eigenvalue

    Lambda=1+e_p(kappa(t_1),...,kappa(t_h))                 (12)

and multiplicity product_i mu(t_i), where e_p is the elementary symmetric
polynomial. The character matrix is invertible over every Z/p^e Z because
q is a power of two and p is odd. Thus the inner rank modulo p^e equals
the sum of these multiplicities for which Lambda is nonzero modulo p^e.
Smith reduction of a diagonal matrix verifies this last assertion.

The accompanying verifier will compare (11)-(12) with directly materialized
small convolution matrices, check (4) and (10), and compute exact spectral
rank strata for p=3 and several q. These checks are finite corroboration,
not the proof of (7) or (8). No full outer matrix of size q^(h^2) is needed.

## Consequence for the programme

The rational small-batch predictor remains a candidate for faster arithmetic
Walsh circuits. It does not obtain a tape caller by simply moving the source
interchange transfers to Q or by preserving their low rank modulo p squared.
The next bridge must change the representation, the cancellation geometry,
the repair of lift errors, or the physical algorithm. This is an exact
reason to pivot rather than repeatedly modify scalar coefficients.

Credits: the label construction and its cost certificate are from the pinned
OpenAI tape manuscript and its cited predecessors. The entrywise-product
rank bound, Smith reduction and elementary two-group convolution identities
are standard algebra. Their application here was developed in this
AI-assisted programme for @CubeJerry; broader literature novelty has not
been established. Independent review and replay status will be recorded
separately rather than assumed.

## Independent review and concurrent comparison

Route C accepted Sections 1--6 and replayed the exact verifier; see `../../routes/C/REVIEW-INTERCHANGE-LIFT-BARRIER.md`. Concurrent E001 `../epsilon-uniformity/PADIC-LIFT-OBSTRUCTION.md` gives a stronger large-q lower bound for the literal matrix modulo p squared. The present proof covers arbitrary supported unit-diagonal lifts, all e>=2 and no large-q restriction. These complementary scopes retain independent provenance; no priority claim is made.
