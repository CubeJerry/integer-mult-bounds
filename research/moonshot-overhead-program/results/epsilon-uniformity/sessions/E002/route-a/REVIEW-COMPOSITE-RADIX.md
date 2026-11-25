# Independent A review of the composite-radix padding component

Status: **accepted arithmetic and source-specialization component**. This
review does not claim a variable-arity recursion or a new global bound.

Reviewed B file `composite-radix-padding.md`, SHA256
`afbef1f7f68361c9d0c865fdef95acf1f5eaad78bc5cec35c9eb43d9ad7404c6`.
Source pin: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`,
November tape `build/interchange.tex`. In this pass I reread its initial
tape-operations/specialization discussion, address geometry interface and
complete recursive implementation. The inherited polynomial count/height
of the complete unit list is in programme
`routes/A/rational-address-and-generator-bounds.md`, AG1.

## 1. Composite specialization is valid in this exact interface

The source chooses its address radix after fixing every rational matrix,
factorization and inverse, avoiding all needed denominator and diagonal
numerator primes. Subsequent identities are finite identities in that
localization of the rational integers. The source uses the prime p of its
scalar field separately. No rank calculation or basis choice is performed
over the ring of addresses modulo b^f.

Consequently every b coprime to the complete compatibility product Q gives
the same specialization argument. Each supplied triangular diagonal is a
unit; its supplied inverse specializes correctly; permutations are ring
independent. Compositions remain equal by the ring homomorphism. This
proves CR1 for composite b as well as primes. It would not justify using
an arbitrary modular field theorem over a composite ring, and B does not
do that.

AG1 bounds the complete rational dictionary polynomially in m in count and
height. Its finite product Q therefore has polynomial bit length. The
scalar module's exponentially many rows do not enter that product: its
coefficients belong to the separate data field, not the address ring.
The product must still include all retained pivots, inverse scalings and
inverse maps, exactly as B requires.

## 2. The root-and-congruence selector is exact

For H and e in CR1, u>=2H gives e>=2 and

    2^H <= R=2^(u/e) <= 2^(2H).

The integer ceil-root B and least b>=B congruent to 1 modulo Q obey
`R<=B<=b<R+Q+1`. Since Q is positive even, b is odd and gcd(b,Q)=1.
The bit-length definition gives

    2^H > 16 Q W (u+1)^2.

Using Q+1<=2Q yields
`(b-R)/R<1/[8 W (u+1)^2]`. Exponentiation and the elementary
`exp(z)<=1+2z` bound on the stated interval give exactly the first CR3
inequality, with its extra 1/W saving. The batch ratio is less than
`1+W/b<1+1/[16(u+1)^2]`. The upper bound on b gives the claimed
`2H+2` bit length.

The combined bound needs no unstated asymptotic approximation. Put s=u+1.
Then

    (1+1/(4s))^2 (1+1/(16s^2))
      =1+1/(2s)+1/(8s^2)+1/(32s^3)+1/(256s^4)
      <=1+1/s

for every s>=1. Thus the stated two-field and batch inflation follows
throughout the admissible range, without changing a small-width constant.
The theorem's allowance to increase a constant is harmless but unnecessary.

Binary search uses O(H) exact comparisons because the root search interval
has O(H) bits. Repeated squaring with an overflow cap at 2^u keeps all
intermediates O(u+H) bits, and schoolbook arithmetic gives a fixed polynomial
number of actual bit operations. Its cost and workspace are paid by the
at least 2^(2u) complete two-field volume; no fast multiplication premise
or prime-gap theorem has been introduced.

## 3. Fixed-tape movement of an arbitrary radix coordinate

The O(V log b) assertion is correct for *moving a coordinate*, even when
numeric b is huge. Here is an explicit physical version of the argument.

Let an array have shape `[P] x [b] x [G] x [B]` and volume V=P b G B.
To move `[b]` to the other side of `[G]`, set h=ceil(log2 b) and
A=2^h. Pad only that coordinate from b to A. The volume is less than 2V.
It now has shape `[P] x [2]^h x [G] x [B]`.

Move the least significant remaining binary digit across `[G]`, then the
next remaining digit, until all h digits have moved. After j moves the
shape is

    [P] x [2^(h-j)] x [G] x [2^j] x [B].

A single step is the operation `[P'] x [2] x [G] x [B']` to
`[P'] x [G] x [2] x [B']`. For each prefix, write the two contiguous
`G B'` runs to two work tapes and merge corresponding B'-blocks to the
output tape. Its inverse splits alternate B'-blocks and concatenates the
two runs. Both cost O(volume), including head returns and amortized range
counters. The number of tapes is fixed. Prefixes are processed serially,
and scratch regions are reused.

Finally discard indices b<=digit<A from the now-transposed coordinate.
Padding and its removal are linear-volume known-range scans. The result
is exact on all genuine entries, with O(V log b) time and O(V) visited
payload cells plus O(log V) descriptors. Temporary padding is removed
before recursive calls. Reversing the operations implements the inverse.
A digit exchange is a bounded number of such coordinate moves, including
moving a digit across arbitrary intervening spectators; it does not require
b or b^2 physical tapes.

This argument concerns coordinate movement, not an arbitrary externally
supplied permutation of b digit *values*. Such a value permutation would
need its own evaluator or a charged table. B only requires coordinate
moves and the separate HS/HA rational maps.

## 4. Finite independent evidence

Command:

    python3 route-a/verify_composite_radix.py

The isolated checker passed:

* 894 exact root/congruence choices, including admissibility boundaries;
* 894 exact combined-padding inequalities;
* 894 negative controls rejecting the previous congruence candidate;
* 260 selected radices with an explicitly found proper small divisor;
* 16 forward/inverse rational-matrix specializations modulo powers of
  explicitly composite radices 29^2, 41^2, 71^2 and 139^2;
* 1,728 forward/inverse short-coordinate padding/transposition cases.

The receipt is `composite-radix-verification.json`. The checker uses exact
integer and rational operations. Its random-access lists are only a finite
permutation oracle; they are not an execution of the fixed-tape algorithm
or an asymptotic complexity proof. The displayed physical proof carries
that separate obligation.

## 5. Variable recursion remains a separate gate

The new radix has polynomial bit height but possibly superpolynomial numeric
value in m. The short-coordinate proof above and HS/HA avoid paying numeric
b. The allocation condition `e>=m+2a+1` and all height-dependent local costs
must still be satisfied by a proposed m(u).

Most importantly, converting a child radix field to a binary complete range
can cost a factor below four in child volume. CR3 does not eliminate that
factor. It must remain in the time recurrence and the parked-space ratio.
Likewise the already proved polynomial-m workspace does not by itself give
a sufficiently small *uniform* space coefficient in a variable-arity global
scheme. B states these limits accurately.

A useful next gate is to prove a constant-copy streaming implementation with
short headers amortized by the long child fibres, and to reuse one data-field
encoding throughout each interchange call. These are additional lemmas,
not conclusions of CR1--CR3. A fixed numerical caller with k-bit payload
records may allow field coordinates to pack existing record bits without
any polynomial-m padding of their physical volume.

Credits: Jerry Chen (@CubeJerry), the pinned source specialization and stream
primitives, B's congruence selector, A's height-priced streams, and substantial
AI-assisted independent review.
