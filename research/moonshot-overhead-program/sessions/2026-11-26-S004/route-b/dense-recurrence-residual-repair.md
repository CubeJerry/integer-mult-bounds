# Dense residual correction from a short forward recurrence

Status: **proved component construction and supplier obstruction, pending
independent review**. This changes the ordinary-error model from sparse
support to a short linear recurrence. The residual may be dense. The
construction charges rational reconstruction, small-prime selection,
coefficient reduction, and emission on fixed tapes. It does not provide
a fast candidate supplier or a general product verifier.

## 1. Exact promise and quantitative theorem

Let `A,B` have degree below `h`, with nonnegative `b`-bit coefficients.
Let `D=2h`, and let the integer candidate `C` have degree below `D` and
`|C_i|<=Cmax`. Write

\[
 E_i=(AB)_i-C_i,\qquad Emax=h2^{2b}+Cmax,\qquad
 \tau=\lceil\log_2(2Emax+2)\rceil.
\]

Thus `|E_i|<=Emax` and `tau` is at least a constant multiple of
`b+log(D+1)`. A length-D sequence has **forward recurrence order at most
s** if some rational coefficients `c_1,...,c_s` satisfy

\[
 E_i+\sum_{j=1}^s c_j E_{i-j}=0\qquad(s\le i<D).             \tag{H1}
\]

The coefficient on `E_i` is normalized to one. A smaller-order recurrence
can be padded with zero coefficients. The zero sequence has order zero.
The coefficients may depend on the input. Let `1<=s<=D/2` be a promised
upper bound, and set

\[
 V=D\tau,\qquad
 K=(s+1)^3\bigl(\tau+\lceil\log_2(s+2)\rceil+1\bigr).        \tag{H2}
\]

**Theorem H1.** Fix `alpha>1/2` and a fixed exact finite-alphabet
multitape multiplier of time `O_alpha(u(1+log_2 u)^alpha)` and space
`O(u)` measured in cells ever visited. Under promise (H1), the exact
ordinary residual, all coefficients of `AB`, and the carried integer
product can be recovered in

\[
 O_\alpha\bigl(V(1+\log_2(K+1))^\alpha+K^6\bigr)             \tag{H3}
\]

time and one `O(V)` bound on cells ever visited. The tape count, alphabet,
and program are fixed; constants are independent of the input parameters.

For packed integer inputs with `b=Theta(log n)` and candidate coefficient
bit lengths `O(log n)`, `V=Theta(n)`. If `s` is polynomial in `log n`,
the repair costs `O(n(log log n)^alpha)+poly(log n)`. More generally, if
`s<=2^((log n)^nu)` for a fixed `0<nu<1`, choose a fixed
`alpha=(1+nu)/(4nu)>1/2`. Then (H3) is

\[
 O_\nu\bigl(n(\log n)^{(1+\nu)/4}+n^{o(1)}\bigr)
                         =o(n\sqrt{\log n}).                 \tag{H4}
\]

This is the cost of correcting a candidate satisfying the explicit
promise. It is not the cost of constructing that candidate.

## 2. The first 2s coefficients determine a promised sequence

Two length-D sequences of forward recurrence order at most s that agree
on their first `2s` coefficients agree everywhere. To see this, regard
each sequence as the prefix of its rational generating series
`P_i(X)/Q_i(X)`, with `deg P_i<s`, `deg Q_i<=s`, and `Q_i(0)=1`.
The numerator of the difference has degree below `2s`. If its first
`2s` series coefficients are zero, that numerator is zero. This argument
also applies directly modulo `X^D` and requires no infinite output.

Compute the first `2s` coefficients of `AB` by multiplying the first
`min(h,2s)` coefficients of each operand and retaining the needed prefix.
Packed radix greater than `4Emax` prevents carries between coefficients.
This is one short multiplication on `O(s tau)` bits, followed by
subtraction of the candidate prefix. All data are actual integer values.

Solve the s equations

\[
 e_i+\sum_{j=1}^s c_j e_{i-j}=0\qquad(s\le i<2s)             \tag{H5}
\]

over the rationals. A solution exists under the promise. Set free
variables to zero after selecting a nonsingular rank minor, and use
Cramer's rule on that minor. Clearing its single determinant gives
integers `q_0,...,q_s`, with `q_0!=0`, such that `c_j=q_j/q_0`.
The entries of all relevant determinants have absolute value at most
`Emax`, so Hadamard's bound or the permutation expansion gives

\[
 \operatorname{bits}(q_j)=O\bigl(s(\tau+\log(s+1))\bigr).     \tag{H6}
\]

The common denominator is one minor, not the product of independently
formed denominators. A rank-zero consistent system uses `q_0=1` and
all other `q_j=0`. The candidate recurrence together with the first s
terms matches all `2s` observed terms; by the uniqueness argument it
continues to the true residual throughout `[0,D)`.

Fraction-free elimination and determinant computation can be carried out
with `O(s^2)` entries of `O(s(tau+log(s+1)))` bits. Their full stored
volume is `O(K)`. Repeated scans to select or update entries, and naive
integer arithmetic, fit the coarse `O(K^6)` preparation allowance.

## 3. A small modulus with an invertible denominator

Direct rational recurrence evaluation can create large intermediate
fractions. Instead compute modulo an explicitly constructed prime power.
Let `B>=1` bound the bit length of the nonzero integer `q_0` in (H6).
There is a prime

\[
             p\le 8(B+2)^2\quad\hbox{with }p\nmid q_0.       \tag{H7}
\]

Here is an elementary bounded search proof. For each `L>=2`, every
binomial coefficient `binom(L-1,j)` divides `lcm(1,...,L)`: the
prime-valuation formula is a sum of at most `floor(log_p L)` zeroes
and ones. Therefore

\[
 2^{L-1}/L\le\operatorname{lcm}(1,\ldots,L)\le L^{\pi(L)}.
\]

With `L=8(B+2)^2`, this gives `pi(L)>B`, using
`log_2 L<=2B+5`. A nonzero B-bit integer has at most B distinct prime
divisors, so at least one of these primes does not divide `q_0`.
Enumerate the integers up to L, test primality by trial division, and
test divisibility of `q_0`. This uses polynomial time in B and `O(B)`
work cells. Even the naive all-divisors implementation fits `O(K^6)`;
it does not search through integers of size comparable to `Emax`.

Choose the least `e>=1` with

\[
                   M=p^e>2Emax.                             \tag{H8}
\]

The modulus has `O(tau+log p)=O(tau)` bits because `s<=D` and
`tau=Omega(log D)`. Compute `q_0^-1 mod M` by the extended Euclidean
algorithm and reduce every `q_j` modulo M. No field extension, root of
unity, unproved prime-gap estimate, or large-prime construction is used.
The ring `Z/MZ` suffices because `q_0` is a unit.

## 4. Emit the dense recurrence in short blocks

Let `Q(X)=sum_(j=0)^s q_j X^j` over `Z/MZ`. Precompute

\[
                   W(X)=Q(X)^{-1}\pmod{X^s}.                \tag{H9}
\]

The constant term is invertible, so schoolbook coefficient recursion
prepares W in polynomial time in K and `O(K)` space. Store the first
s error coefficients modulo M as the initial block.

Suppose the previous block is
`A_j(X)=sum_(r=0)^(s-1) E_(js+r) X^r`. For the next block, take

\[
 B_j(X)=-[X^s,\ldots,X^{2s-1}]\bigl(Q(X)A_j(X)\bigr),
 \qquad A_{j+1}(X)=W(X)B_j(X)\pmod{X^s}.                    \tag{H10}
\]

The bracket means extract those s coefficients and renumber their
exponents starting at zero. Since Q has degree at most s, only the
immediately previous block contributes from earlier positions. Within
the new block the recurrence is exactly `Q A_(j+1)=B_j mod X^s`.
Thus (H10) advances the recurrence correctly. A final partial block is
computed in the same way and only the needed coefficients are emitted.

Each block costs two polynomial products of O(s) coefficients modulo M.
Use packed nonnegative representatives and a power-of-two radix exceeding
`4(s+1)M^2`; the digit width is `O(tau)`. Each polynomial product is
therefore one `O(s tau)`-bit exact integer multiplication. Decode its
coefficients, reduce them modulo M, and repack. Individual reductions
are charged using a precomputed Barrett reciprocal and a fixed number
of `O(tau)`-bit multiplications, as proved in the sparse-residual note.
They are not treated as constant-time word operations. This gives total
block emission cost

\[
 O_\alpha\bigl(D\tau(1+\log_2(s\tau+1))^\alpha\bigr),       \tag{H11}
\]

including the coefficient reductions. Because the true coefficients
are integers in `[-Emax,Emax]` and M exceeds `2Emax`, their centered
representatives recover the exact signed values, not only residues.

The previous block, Q, W, the multiplication regions, and the modular
reciprocal are reused at every step. Input and output scans have O(V)
bit volume; the additional retained work occupies O(K) cells. If `K<=V`,
this is one O(V) visited-space bound. If `K>V`, skip the reconstruction
and use packed schoolbook multiplication in `O(V^2)<=O(K^6)` time and
O(V) visited cells. This branch also covers a supplied `s>D/2` by
direct multiplication. The alphabet and tape count never depend on s.

## 5. What is and is not certified

The first `2s` coefficients uniquely identify the residual **within the
promised class**. They do not certify that an arbitrary residual belongs
to that class. For example, the zero prefix and an error `X^(2s)` agree
on all observed coefficients but require different answers when `D>2s`.
That example lies outside the recurrence promise.

Adding finitely many modular fingerprints does not by itself turn this
into an unrestricted verifier: a nonzero integer polynomial with an
initial `2s`-zero prefix can be multiplied by the tested fold polynomials
to evade those fingerprints, when degree and height budgets allow. A
general certificate needs additional hypotheses or additional work.

Likewise, a single small **finite Hankel-matrix rank** is not the same
as (H1). The length-D vector `(0,...,0,1)` has rank at most one in every
rectangular Hankel matrix whose indices stay below D, yet its normalized
forward recurrence order is D. Boundary degeneracy prevents recovery
from a short initial prefix. The theorem uses (H1), not an unproved
identification with an arbitrary finite Hankel-rank convention.

## 6. A rank obstruction to supplying this structure at the linear interface

**Theorem H2.** Let V be a linear subspace of length-D sequences over any
field. If every vector of V has normalized forward recurrence order at
most s, with its own input-dependent recurrence coefficients, then

\[
                         \dim V\le s.                       \tag{H12}
\]

Indeed, restrict the linear map from V to its first s coordinates. Any
vector in its kernel has s initial zeroes. Its own recurrence then makes
every subsequent coefficient zero by induction. The restriction map is
injective, so `dim V<=s`. The difference of two vectors belongs to V;
this is why the argument is stronger than counting all nonlinear
recurrence descriptions.

For W output rows of length N, if every output row of every vector in a
linear image has recurrence order at most s, the same proof using the
first s coordinates of every row gives

\[
                 \operatorname{rank}(R)\le Ws.               \tag{H13}
\]

Thus the spectral matrix-prediction rank bounds in the companion notes
have a direct consequence. A full-rate independent-input transform error
of rank at least `delta WN` cannot have recurrence order below
`delta N` on every output row for every input. The recurrence may depend
arbitrarily on the input; linear-image closure still proves the bound.

To instantiate the rank premise from an abstract uniform spectral average,
use the regular representation, or separately verify the actual spectral
multiplicities. Unequal multiplicities in a physical payload do not give
the same normalized rank merely because every spectral value is present.
The algebraic statement (H13) applies to the actual error map and does
not suppress this representation check.

The same injection proof applies if field coordinates are first encoded
as integers by a fixed coordinatewise map that sends zero to zero and
no nonzero field element to zero, and every encoded output sequence has
its own rational forward recurrence of order at most s. A field vector
in the prefix kernel has an integer-encoded zero prefix; its rational
recurrence forces the entire encoded sequence to vanish, hence the field
vector vanishes. The prefix projection and dimension count remain over
the original field. No reduction of rational recurrence denominators
into that field is needed. This encoding extension was pointed out by
the session lead.

These are statements about the declared sequence order and coordinate
encoding. A serialized-bit stream, a changed ordering, or a later
nonlinear candidate residual needs its own explicit mapping before
the dimension conclusion can be used.

This rules out inserting this corrector at that linear transform interface
while assuming a uniformly tiny recurrence order. It does not prove that
the final integer-product residual after arbitrary nonlinear or later
composition has high recurrence order. Such a new supplier needs its own
proof. No general multiplication lower bound follows.

The construction uses classical rational-generating-series and block
polynomial arithmetic ideas, written out here to price the exact tape
application. No priority claim is made for those underlying methods.

## 7. Prior-art and read-scope record

Alin Bostan and Ryuhei Mori, *A Simple and Fast Algorithm for Computing
the N-th Term of a Linearly Recurrent Sequence*, SOSA 2021, pp. 118--132,
DOI <https://doi.org/10.1137/1.9781611976496.14>, provides a primary
reference for the classical rational generating-function characterization
and fast polynomial-arithmetic treatment of recurrences. The author PDF
<https://mathexp.eu/bostan/publications/BoMo21.pdf> was retrieved; Section
2.1, Lemma 1 and Algorithms 1--2, and Section 3.1's slice formulation and
Algorithms 5--7 were read. Their selected-term and slice algorithms are
prior art, rather than claimed here as new. This note uses its own
explicit consecutive-block identity (H10), so it does not import their
unread implementation details as tape primitives. The full paper and
its cited predecessors, including Fiduccia's original proof, were not
audited in this session. A publisher abstract was inspected for Fiduccia,
*An Efficient Formula for Linear Recurrences* (1985), DOI
<https://doi.org/10.1137/0214007>; no full-text read is claimed.

Prepared for @CubeJerry with substantial ChatGPT assistance.
