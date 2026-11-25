# A small compatible radix and a multidigit batching prefix

Status: proved component; independent review pending. This note does not
claim an improved multiplication envelope. It removes two particular
exponential constants from the literal source implementation and states
what still has to be paid.

Source pin: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`build/interchange.tex`, especially the paragraphs before and within the
proof of Theorem `thm:interchange`. Predecessor parameter bounds are
`routes/A/rational-address-and-generator-bounds.md`, Sections 1--2, at
programme start `0607d044d1d09489580da0e5828588820e1a6775`.

## 1. A compatible odd prime of polynomial bit-height cost

**Lemma R1.** Let `a_1,...,a_k` be nonzero integers given in binary, and
let `B` be the binary length of `M=2 product_i |a_i|`. There is an odd prime
`b <= 32(B+1)^2` dividing none of the `a_i`. A fixed deterministic binary
multitape machine can find such a b using time and space polynomial in
the total input bit length. No factorization oracle is used.

**Proof.** Let N be the least power of two at least `16(B+1)^2`. Then
`N<32(B+1)^2` and N is even. Put `P_N=product_(p<=N, p prime) p` and
`Q_N=lcm(1,...,N)`. The exponent of each prime p in the central binomial
coefficient `binom(N,N/2)` is

    sum_(r>=1) (floor(N/p^r)-2 floor((N/2)/p^r)).

Every summand is zero or one, and there are at most `floor(log_p N)`
nonzero summands. Hence that binomial coefficient divides Q_N. Since
there are N+1 binomial coefficients in row N and the central one is
largest,

    log2 Q_N >= N-log2(N+1).

Every exponent in Q_N is at most log2 N, so

    log2 P_N >= [N-log2(N+1)]/log2 N.

For B>=1, `log2 N < 5+2log2(B+1) <= 4(B+1)`, while
`log2(N+1)/log2 N<2`. Consequently

    log2 P_N > 4(B+1)-2 > B > log2 M.

Thus P_N cannot divide M. Some prime p<=N does not divide M; call it b.
Because 2 divides M, b is odd. Enumerate integers through N, test
primality by trial division, and compute M mod b by ordinary binary
long division. N is polynomial in B, and B is at most one plus the sum
of the supplied integer bit lengths. Even schoolbook operations give
polynomial total time and space. QED.

The exponent and constants above are deliberately loose. No analytic
prime-number theorem or unproved quantitative prime hypothesis is needed.

**Application R2.** Suppose the exact rational address constructor emits
polynomially many rational entries of polynomial bit height in m. Collect
all nonzero numerators and denominators required for invertible diagonal
scalings, pivots and inverses; include every coefficient actually used by
the factorization. Apply R1 to this complete list. The chosen radix b is
polynomial in m, although individual address integers can have numeric
size `2^(poly(m))`. They specialize correctly modulo every `b^f`.

This does not make a scaling by a large integer cheap. Its *execution*
still requires a height-priced address primitive. R2 only removes the
need to choose b above the largest numeric coefficient.

The source's rational label geometry is independent of its exponentially
wide scalar module. Under its accepted guards `N<=m^5`, the number of
label pairs, rectangles, endpoint maps, pivots and matrix entries is
polynomial in m. The existing height proof bounds each listed height by
`m^10000`; hence its complete address compatibility product has polynomial
bit length. This is the exact scope in which R2 applies. It is not a claim
about all scalars of the full predictor or numerical Walsh program.

## 2. Replacing the one-digit split by a block of digits

The source asks for `b>W`, where W is the completed number of independent
rows in a finite main-swap program. This is sufficient for its one-digit
split but is not necessary for the batching argument.

Fix an integer radix b>=2, row width W>=3 and `0<eta<=1`. Set

    ell = ceil(log_b(W/eta)),  A=b^ell,
    q=ceil(A/W).

Equivalently ell can be found by repeated multiplication of b until
`b^ell >= W/eta`; use a rational eta for exact finite computation. Then

    A>=W/eta,   qW/A <= 1+W/A <=1+eta.                 (R3)

At a width-e interchange node, take the first ell digits of the earlier
chunk as a leading range of A values. Batch these values into q groups
of W, with zero padding only in the final group. Keep the group index as
a spectator. A fixed number of tapes can split the row-major array by
that leading range, retaining the W row coordinates in one concatenated
stream; the physical executor must consume that declared representation.
Every row has the same remaining address ranges. There is no need to
transpose an unbounded outer-prefix range past the row index: process
successive outer-prefix/group batches serially, preserving their existing
order. Within each batch its W rows are contiguous. All address maps
leave these spectators fixed, so the same finite row program applies to
each batch independently. The descriptor of the repeated spatial shape
is prepared once; the outer prefix/group index is only advanced, not
redecoded for each datum. Summing child volumes over all batches gives
at most `(1+eta)V/W` per finite row-program call. Each individual child
also has volume at most this amount. The complete finite row program
acts identically and exactly on each independent row, so discarding the
padding and restoring the leading range preserves every genuine entry.

A change of the *finite row-index fields* inside a batch may still be
needed to expose a chosen label/module order. Their total width is
O(log W). Direct binary-field moves, or stable bit partitions of the
row coordinate, cost a fixed polynomial in log W per volume on a fixed
number of tapes. The latter may attach only the row-index bits to encoded
symbols; no long spatial address is appended. Inverting each known field
move uses the reverse split/merge scans and the same range descriptors.
This finite row-layout cost is part of C_m below. It does not sort on an
unbounded prefix, gap, or spatial address.

The number W need not be the number of machine tapes. Representing its
rows on W separate tapes would be inadmissible when W varies. This lemma
uses only the arithmetic batching and a concatenated representation; all
later scalar-row operations still need their own fixed-tape execution
proof.

Let a be the number of occupied reserve fields at either end and let m
be the number of main field pairs. For `e>=ell+m+2a` put

    f=floor((e-ell)/(m+2a)).                            (R4)

Partition both chunks into: the ell leading digits, a reserve fields,
m main fields, a reserve fields, and the remaining fewer than m+2a
digits. The batch extractor uses only the leading range of the earlier
chunk; the leading range of the later chunk remains a spectator. Run the
same main program on width-f fields and restore reserves as in the source.
Finally swap the 2a reserve pairs recursively and interchange the two
leading blocks and the bounded remainder by individual digit moves.
There are at most `ell+m+2a` such direct digit exchanges. Since b varies,
serialize the b (or b squared) digit classes by repeated scans on a fixed
number of tapes; each direct digit exchange costs polynomial b times V,
not a b-independent O(V). All fields and
spectators have their source positions restored.

For `e<ell+m+2a`, use the same direct digit procedure on all e digits.
It costs `poly(b) (ell+m+2a)V` and visits polynomial-b times V cells,
with a fixed number of
tapes and the source digit-splitting scans.

If the main program makes sigma recursive calls per W independent rows,
the resulting recurrence is

    T(e) <= C_m + ((1+eta)sigma/W+2a) T(f),
    f<=e/m,                                           (R5)

where C_m includes actual scalar work, the batching/merge representation,
and `poly(b) (ell+m+2a)` for direct moves. In particular if

    (1+eta)sigma/W+2a <= kappa m^rho,  0<kappa<1,

then induction or a geometric series gives, for `1/2<rho<1`,

    T(e)<=C'_m max(1,e^rho),
    C'_m=O(C_m/(1-kappa)+poly(b)*(ell+m+2a)^(1-rho)).             (R6)

For the bounded base range, the direct digit bill includes poly(b) and
uses `e<=max(1,ell+m+2a)^(1-rho) e^rho`.

## 3. Quantitative effect and limitations

For the power-of-two formula refinement, `log2 W=poly(m)`. With constant
eta, `ell=poly(m)` even when `W=2^(poly(m))`. By R2, b can also be
polynomial in m. Thus the binary-to-radix range padding factor `<b^2`,
the leading-block length, the direct digit base procedure, and prime
preparation have polynomial m cost. None requires a multiplicative W
factor or numeric-height-sized radix.

This eliminates the *literal radix/batch-width* obstruction to a
polynomial proportional compiler. It leaves the genuine issues separate:

* row pencils and repairs must run on concatenated independent rows in
  polynomial m work per input symbol, without W scans;
* address scalings need actual height-priced tape algorithms;
* spectral case lookup cannot scan an exponential table per datum;
* the numerical Walsh, precision, preparation and whole-input common-space
  contracts must compose.

The conclusion is a source-specific constructive component, not an
integer-multiplication runtime bound or a lower bound. Credits: the
OpenAI source interchange and source rational label construction; the
predecessor programme height analysis; elementary binomial/divisibility
arguments; Jerry Chen (@CubeJerry); AI-assisted E002 Route C analysis.

## 4. Finite support

`verify_small_radix.py` passed 3,375 compatibility lists, seven exact
binomial/lcm divisibility cases, 1,940 padding/occupancy cases, 960 full
digit partitions, and 12,000 contractive recurrences. There were 1,868
negative controls where the one-digit split cannot supply W rows. The
receipt is `small-radix-verification.json`. These checks do not execute
a tape machine or establish the asymptotic proof.
