# Input-dependent composite radix with charged height and tiny padding

Status: **proved arithmetic/source-specialization component, independently
reviewed by Routes A and C**. Their reviews are
`../route-a/REVIEW-COMPOSITE-RADIX.md` and
`../route-c/review-composite-and-outer-transfer.md`. This strengthens
the earlier E001 input-dependent
radix preparation by removing prime search and its analytic prime-gap
premise. It does not by itself establish a variable-arity tape algorithm.

Pins: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`build/interchange.tex`, especially the rational-coordinate specialization
and final binary-range padding; programme predecessor
`0607d044d1d09489580da0e5828588820e1a6775`, focused E001
`route-c/INPUT-DEPENDENT-RADIX.md`. The earlier note already proves the
concept of input-dependent small-loss padding using compatible primes.
The new ingredient here is a simple congruence choice, and its compatibility
with E002's height-priced address operations.

## 1. Primality is unnecessary for this address interface

Let Q be a positive even integer divisible by every nonzero numerator and
denominator that must be a unit in the finite rational address programme.
Include the diagonal units of the fixed triangular/Bruhat factorizations
and every inverse matrix actually used. Zero coefficients need not be units.

**Lemma CR1.** Every integer b>=2 with gcd(b,Q)=1 is a valid address radix
for those specified rational operations modulo b^f, for every f>=1.

**Proof.** Each required denominator and diagonal numerator is coprime to
b, hence to b^f. The canonical homomorphism from the localization of Z at
these units to Z/b^fZ specializes every finite rational matrix identity.
An invertible triangular factor remains invertible because its diagonal
entries remain units; its supplied rational inverse specializes too. A
permutation factor is invertible over every ring. Thus all endpoint maps
and their paired inverses remain genuine bijections on complete digit
ranges. Identities obtained by adding/multiplying these matrices remain
valid. No vector-space rank assertion over Z/b^fZ is needed: all bases and
factorizations were fixed over Q before specialization.

The data field in the interchange proof is separate from the address
radix. Its characteristic-two row arithmetic, spectral order-three
identities and check matrices do not require b to be prime. Splitting
complete radix ranges, comparisons, rotations, digit moves and reserve
restoration are combinatorial operations valid for every b>=2. These are
all uses of b in the cited interchange proof. ∎

This lemma does not claim that an arbitrary proof over a prime field can
be specialized to a composite modulus. It applies only to the stated
rational address maps and finite identities with all required units listed.

## 2. An explicit integer choice

Let u>=1 be a binary field width, W>=1 a required leading batch width,
and let Q be as in CR1. Write `ell(z)=floor(log_2 z)+1` for positive
integer z and define

\[
H=\ell(Q)+\ell(W)+2\ell(u+1)+4,
\qquad e=\lfloor u/H\rfloor.                         \tag{CR1}
\]

Assume u>=2H; bounded failing cases are left to the caller's direct base
algorithm. Compute exactly

\[
B=\min\{a\in\mathbb N:a^e\ge2^u\},\qquad
b=1+Q\left\lceil{B-1\over Q}\right\rceil.             \tag{CR2}
\]

**Theorem CR2.** The resulting radix is odd, coprime to Q and greater
than W. It has bit length at most 2H+2. Moreover

\[
1\le {b^e\over2^u}\le1+{1\over4(u+1)},\qquad
1\le {W\lceil b/W\rceil\over b}
 <1+{1\over16(u+1)^2}.                               \tag{CR3}
\]

Thus two-field padding followed by the source's leading batch padding
has volume inflation at most `1+1/(u+1)` for every admissible width.
All quantities are
computed by finite integer arithmetic; no prime theorem or prime search
is used.

**Proof.** Put R=2^(u/e). Since e<=u/H, R>=2^H. Since
e=floor(u/H)>=u/(2H), R<=2^(2H). Integer ceiling and the congruence
choice give

\[
R\le B\le b<B+Q<R+Q+1.
\]

The definition of H gives
`2^H>16 QW(u+1)^2`, and `Q+1<=2Q`. Therefore

\[
0\le {b-R\over R}<{1\over8W(u+1)^2}.
\]

Using `e<=u` and `(1+t)^e<=exp(et)`,

\[
{b^e\over2^u}<\exp\!\left({1\over8W(u+1)}\right)
\le1+{1\over4W(u+1)}\le1+{1\over4(u+1)}.
\]

Here `exp(z)<=1+2z` for `0<=z<=1/8`, for example by its power
series and a geometric bound. Also `b>=R>16QW(u+1)^2`, so
`W ceil(b/W)/b<1+W/b<1+1/[16(u+1)^2]`.
Multiplying the two squared-range factors and this leading factor proves
the displayed combined bound. Finally b is 1 modulo the even Q,
so it is odd and coprime to Q. The upper bound
`b<2^(2H)+Q+1<2^(2H+1)` gives the bit-height claim. ∎

## 3. Actual preparation and fixed-tape use

Binary search computes B with O(H) candidate comparisons. Repeated
squaring, truncated once a product exceeds 2^u, compares a^e to 2^u
using a fixed polynomial number of bit operations in u and H. All
intermediate stored integers can be capped at O(u+H) bits. Ordinary
schoolbook arithmetic suffices. One integer division then computes b.
Thus preparation takes polynomial(u,H) actual steps and workspace on a
fixed number of tapes, including reading Q and W. Their bit lengths are
already at most H. No near-root multiplication routine is invoked.

For an interchange input with two complete u-bit fields, volume is at
least 2^(2u). Under u>=2H, every such fixed polynomial setup is absorbed
by O(V), including arbitrary spectator ranges. Forming the supplied Q
from its matrix/unit list remains charged to template construction.

The numeric value b can be exponential in a polynomial of the template
parameter. E002's height-priced affine lemma acts modulo b^f using
coefficient heights and complete fibres, not a number of streams equal
to b. A direct move of one radix digit across an arbitrary range also has
cost O(V log b): pad that single digit to the next power of two, perform
its binary digit moves, then discard the known padding. Its temporary
volume is less than twice V, and there is no recursive call. The inverse
reverses the same moves. Repeating polynomially many such direct moves
therefore has polynomial height cost, not polynomial numeric-b cost.

These statements explain why the congruence choice is useful now: before
height-priced scaling, a huge numeric radix could have restored the cost
that the small padding removed.

## 4. Explicit variable-template requirements

For a family with `log Q,log W<=m^C` and m=Theta(u^gamma), taking a
sufficiently small fixed gamma gives H=o(u) and e=Omega(u/H). To allocate
the source's m main and polynomially many reserved fields, the stronger
test `e>=m+2a+1` is still required. It follows when
`H(m+2a+1)=o(u)`, after increasing the fixed base threshold.

Recursive calls have fields of size b^f. Padding those fields to binary
ranges before a child chooses a new radix has a factor less than four.
That factor must appear in every child invoice. It is not covered by CR3
and is not declared summably small. Repeated field encodings, row metadata,
and proportional workspace likewise need their own recursion accounting.

CR2 is therefore a proved padding/preparation component. A complete
variable-arity bound needs the charged recurrence, child conversions,
literal fixed-alphabet executor and common visited-space normalization.

Open next questions: verify the complete unit list in the actual endpoint
plans; audit the integer selection against tiny/boundary cases; compose
the variable-radix child interface and determine whether its remaining
padding/space losses fit the desired recurrence.

## 5. Independent finite check

Route A's exact checker was replayed in this directory as
`verify_composite_radix_replay.py`. It passed 894 radix selections and
combined-padding inequalities, rejected all 894 immediately preceding
congruence candidates, specialized 16 rational inverse identities at
explicit composite moduli, and checked 1,728 short-digit moves and
their inverses. Of the selected radices, 260 had a detected small
proper divisor, so those cases do not merely retest prime moduli.
The receipt is `composite-radix-verification.json`. The copied checker
is the author's implementation, not an independently coded tape machine.
These finite checks do not prove the asymptotic physical cost.

Credits: @CubeJerry; the pinned OpenAI address construction; E001's prior
input-dependent-radix idea and proof; E002's height-priced affine streams;
substantial ChatGPT multi-agent assistance. No full multiplier execution,
human refereeing or Lean verification is claimed.
