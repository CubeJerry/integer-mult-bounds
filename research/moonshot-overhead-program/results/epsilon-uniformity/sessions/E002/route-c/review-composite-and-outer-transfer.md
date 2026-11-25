# Composite radix and the outer tape layers: independent review

Status: **independent source audit and proved local refinements**. This
accepts the composite-radix component under its complete-unit-list
contract. It does not assert a complete multiplication bound by itself.

Source pin: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`,
`preprints/The-logarithmic-exponent-of-integer-multiplication-on-tapes-November-24-2026/build/`
files `interchange.tex`, `permutations.tex`, `walsh.tex`, `integers.tex`.
Programme predecessor: `0607d044d1d09489580da0e5828588820e1a6775`.
Reviewed E002 Route B files: `composite-radix-padding.md`,
`polynomial-walsh-precision.md`, and `separated-setup-transfer.md`.

## 1. Which primes are actually needed?

The interchange proof has two independent arithmetic objects. Its data
field has characteristic two and uses order-three spectral data. Its
address fields are `Z/b^f Z`. Rational address changes are factored over
Q and only then specialized to this address ring.

Let Q be a positive even integer divisible by every nonzero numerator and
denominator that must be invertible in the **supplied** rational factors,
inverse factors and diagonal pivots. If `gcd(b,Q)=1`, all these numbers
are units modulo `b^f`, for every f. The map from their localization of
Z to `Z/b^f Z` preserves the supplied matrix identities. In particular,
supplied triangular inverses remain inverses. Field permutations and
ordinary digit splitting remain bijections on complete radix ranges.

This is exactly what the address part of `interchange.tex` uses. No new
Gaussian elimination or rank assertion is made over `Z/b^f Z`; all bases
and factorizations were fixed over Q. Comparisons, rotations and reserve
restoration are combinatorial operations on integer representatives.
Therefore **address-radix primality can be replaced by this coprimality
condition**. Route B's CR1 is accepted, with its full unit list remaining
a constructor obligation.

The outer `integers.tex` uses distinct primes `a_i` in short intervals to
obtain pairwise-coprime cyclic axes with a constant occupied fraction.
These primes are unrelated to b and remain unchanged. Their existence
uses the source's fixed prime-gap result; enumeration/trial division has
fixed polynomial cost in the outer address width k. The eventual cutoff
is absolute, independent of the template. The source tests size and
coprimality and keeps an exact direct fallback. This separate prime-gap
premise is not removed.

## 2. Exact near-root congruence selector

Write `ell(z)=floor(log_2 z)+1`. Route B sets

\[
H=\ell(Q)+\ell(W)+2\ell(u+1)+4,\quad e=\lfloor u/H\rfloor,
\quad B=\min\{a:a^e\ge2^u\},\quad
b=1+Q\lceil(B-1)/Q\rceil,
\]

assuming `u>=2H`. Put `R=2^(u/e)`. Then
`2^H<=R<=2^(2H)`, `R<=B<=b<R+Q+1`, and
`2^H>16QW(u+1)^2`. Hence

\[
0\le(b-R)/R<1/[8W(u+1)^2].
\]

Since `e<=u`, the elementary bound `(1+t)^e<=exp(et)` gives

\[
1\le b^e/2^u\le1+1/[4W(u+1)]\le1+1/[4(u+1)].
\]

Also `b>16QW(u+1)^2`, so

\[
1\le W\lceil b/W\rceil/b<1+1/[16(u+1)^2].
\]

Combined two-field and leading-batch inflation is at most `1+1/(u+1)`
without another asymptotic qualification: for `z=1/(u+1)<=1/2`,

\[
(1+z/4)^2(1+z^2/16)
=1+z/2+z^2/8+z^3/32+z^4/256\le1+z.
\]

The congruence rounding also covers `B=1 mod Q`. Since Q is even, b is
odd, coprime to Q, and greater than W. It has `O(H)` bits. Exact binary
search for B takes `O(H)` power comparisons. Capped schoolbook integer
arithmetic gives fixed polynomial preparation in u and H on fixed tapes.
This accepts CR2 and its preparation estimate. A child-field conversion
from radix b to binary still has a separate factor less than four for two
fields and must remain in the variable-template child invoice.

## 3. A direct radix move costs bit height

**Lemma O1.** A complete field of size b can move past an arbitrary
adjacent complete spectator range in `O(V(1+log b))` actual fixed-tape
steps and `O(V)` reusable payload space. Leading and trailing ranges are
arbitrary. Descriptors retain their additive polynomial bit-length cost.

**Proof.** Pad the b-valued field to size `2^t`,
`t=ceil(log_2 b)`, at less than twice the volume. Move its t binary
positions, in their original order, past the spectator range using the
elementary bit move. Each move is a two-stream split/merge of linear
volume, including rewinds and cleanup. After all positions move, each
field has its original value; delete values at least b by a scan. Reverse
the steps for the inverse. Only a fixed number of streams is used, and
the spectator range need not be a power of two. ∎

For exchanging two separated b-valued fields, an equivalent implementation
pads both to `2^t` (less than fourfold volume), exchanges their t
corresponding binary positions, then removes padding. Padding must be
removed **after the full field exchange**: a partial bit exchange need
not preserve the subset below b. An ell-digit field can be treated as
one range of size `b^ell`, giving `O(V(1+ell log b))` work. Thus
polynomially many direct remainder/reserve moves have polynomial height
cost when `log b=poly(m)`. No recursive encoding is declared volume free.

## 4. Interchange precedes Walsh, with an active-width toll

Suppose exact interchange has cost
`m^K V(1+v^rho)+Setup(m,k)` on two binary fields of width v, and
`m^K V+SetupSpace(m,k)` visited space. The source first uses it for
bulk XOR, position permutations and controlled small-block permutations.
The guard/sparse-repair proof is unchanged. Address/control computations
have a fixed polynomial degree in k, including polynomial-m coefficients
once `k>=m^C`. Fixing the guard constant after those degrees leaves
`O(log k)` guard classes. Hence the source bounds acquire polynomial-m
prefactors:

\[
\begin{aligned}
\mathrm{Xor}(v,V)&\le m^{K'}V(1+v^\rho)(1+\log k)+\mathrm{Setup}',\\
\mathrm{Positions}(k,V)&\le m^{K'}V(1+k^\rho)(1+\log k)+\mathrm{Setup}',\\
\mathrm{Blocks}(k,V)&\le m^{K'}V(1+k^\rho)(1+\log k)^3+\mathrm{Setup}'.
\end{aligned}
\]

Sparse destination tags have `O(k)` bits per exceptional numerical
record, whose untagged width is already `Theta(k)`, and are stripped
after sorting. Temporary tags/direct padding do not change later child
volumes.

At a Walsh node of active width a, binary column elimination uses
polynomially many slot exchanges/additions on slots of width `a/A`.
Its nonrecursive toll is therefore

\[
m^{K''}V(1+a^\rho)(1+\log k)^{C_0}+\mathrm{Setup}'',       \tag{O1}
\]

with fixed C0. It is not just `m^{K''}V polylog(k)`. Route B has
amended E/S2 to allow (O1), after this review identified the distinction.
The complete profile draft independently states this toll in P6.

Write `q=sigma/W` and assume `q/A^rho<=1/2`. Dividing time by
volume gives

\[
T(a)\le m^{K''}(1+a^\rho)(1+\log k)^{C_0}+qT(a/A).
\]

Divide by `a^rho`. The local term is at most
`2m^{K''}(1+log k)^{C_0}`, and every later level has ratio at most
one half. This proves `T(a)<=m^{O(1)}a^rho(1+log k)^{C_0}`.
There is no circular dependency: prove interchange first, binary routing
second, numerical Walsh third. An internal Walsh child designates one
complete contiguous active slot with full spectators; it does not repeat
the top-level arbitrary selected-position permutation on the entire
k-bit address at every internal child.

## 5. Leading-row padding and outer costs

The numerical batch has `A>=m`, `W<=m^K`, and polynomial branch
count. At recursion depth J, `W^J<=(1+s)^K` after enlarging an
absolute K. The top selected-bit layer has at least `2^(k/2)` spectator
rows for large k. Rounding their count to a multiple of `W^J` costs at
most a constant factor after an absolute or polynomial-m guard. It does
not hide a W factor per child. Each child receives one of W work streams;
the polynomially many row roles can be serialized on fixed tapes.

The outer integer construction uses a fixed number of transforms and
`O(log k)` unitary layers per transform. Local tables occupy blocks of
`O(log k)` address bits, so their preparation has fixed polynomial degree
in k. The short record multiplier costs `O(k log k)` with marked reusable
regions. Once Route B's absolute `O(k)` precision theorem applies, no
new template-dependent record-width factor appears. Final rounding and
carry propagation use the source's fixed norm/error margins.

These outer layers add polynomial-m coefficients and fixed powers of
`1+log k`. They do not force an expanded per-record table scan or a
template-dependent prime-gap threshold. Variable-template child
re-encoding, shape and common visited-space composition still need their
own proof.

## 6. Evidence boundary

These are written proofs and a source audit, not a full machine execution
or formal verification. The independent rational replay in
`replay-rational/rational-walsh-verification.json` checked 203949 signed
scalings, 611847 signed same-grid roundings, 1440 full repair-basis cases,
and the recorded zero-gap/wrong-transpose controls. Those finite tests
support the separately reviewed numerical component only.

Credits: @CubeJerry; the pinned OpenAI tape construction and cited
predecessors; E001's input-dependent radix idea; E002 Route A's
height-priced streams and Route B's selector/precision work; substantial
ChatGPT multi-agent assistance.
