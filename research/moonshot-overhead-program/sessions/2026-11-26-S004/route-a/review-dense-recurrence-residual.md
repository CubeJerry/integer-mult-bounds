# Independent review: dense forward-recurrence residual repair

Verdict: **H1 and H2 pass as the stated promised-class component and scoped
linear-interface obstruction**. No complete multiplier or unrestricted
candidate verifier follows. This review checked the mathematical recovery,
short-data heights, prime construction, block emission and actual common
visited-space composition, not just the finite examples.

Reviewed author snapshot:
`/workspace/scratch/584cf2c0b8ab/route-b-work/dense-recurrence-residual-repair.md`
SHA-256 `85118b0abeddcf5b6cfc94e220ac39f5c5d1a3019a96b47d136d58def174801f`.
The referenced sparse-residual modular stream proof was also reread:
SHA-256 `25b321ea57c5ab387fe7841ad7743007a5586bfe56c5078a3f001e0cd1be7943`.

## 1. Prefix uniqueness and bounded rational reconstruction

The normalized forward-recurrence premise is the right one. Every promised
prefix extends to P/Q with deg P<s, deg Q<=s and Q(0)=1. The difference
of two such series has numerator degree below 2s, so agreement through
coefficient 2s-1 proves identity. Solving only H5 is consequently enough:
any solution extends the observed prefix to another order-at-most-s series,
and the promised true sequence is forced to agree on the entire needed
finite interval. This is not a claim that the prefix certifies the promise.

Selecting independent columns and a nonsingular row minor in H5, setting
other coefficients to zero, gives a consistent solution on every row.
The same selected determinant can clear all denominators. Its order is
at most s and its entries, including the Cramer replacement columns, are
bounded by Emax. The permutation expansion gives bit height at most
O(s(tau+log(s+1))), including the singular/rank-zero consistent cases.
Thus O(s^2) fraction-free entries occupy O(s^3(tau+log(s+1)))=O(K) bits.
Repeated scans and elementary integer operations fit the generous K^6
preparation allowance; no independently formed denominator product is needed.

The prefix product uses one genuine packed multiplication on O(s tau)
bits. Its base exceeds all true prefix convolution coefficients. Signed
candidate subtraction occurs after exact digit decoding, so no signed
carry ambiguity enters the reconstruction.

## 2. The elementary prime bound is adequate and charged

For every prime p, the valuation of binom(L-1,j) is a sum of at most
floor(log_p L) terms in {0,1}. Hence it divides lcm(1,...,L). Taking
one largest binomial coefficient gives lcm>=2^(L-1)/L. The upper bound
lcm<=L^(pi(L)) follows by bounding each maximal prime-power factor by L.
At L=8(B+2)^2, these inequalities give pi(L)>B, using the author's
log_2 L<=2B+5 bound. A B-bit nonzero q_0 cannot contain all those
primes. This proves H7 without a prime-gap or a large-prime oracle.

Even trial division by all smaller integers takes O(B^4 polylog B)
steps over all candidates, with O(B)-bit reusable regions; division of
q_0 by the candidate primes also fits K^6. The q_0=+/-1 case is harmless.
The first prime power M>2Emax has O(tau+log p)=O(tau) bits, since
s<=D and tau>=log_2 D+2b up to the stated rounding. Extended Euclid and
coefficient reductions have polynomial short-data cost. Only q_0 needs
to be a unit; the argument correctly works in Z/MZ rather than assuming
a field.

## 3. H10 emits the right coefficients at the claimed streaming cost

For index js+r in a new s-coefficient block, a degree-s recurrence refers
only to that block's earlier coefficients and to the immediately preceding
block. The high s coefficients of Q times the previous block are exactly
the contribution from those preceding coefficients. Multiplication by
Q^-1 modulo X^s therefore gives the next block. This proves H10 even
when deg Q<s, including order padding and a final partial output block.

Each polynomial operand has O(s) canonical residues below M. Its ordinary
integer product coefficients are less than (s+1)M^2. The packed base in
H10 consequently prevents inter-digit carries, and its digit width is
O(tau), because log s=O(tau). Two O(s tau)-bit integer products suffice
per emitted block. Their number is O(D/s), giving the main H11 bill.

The modular coefficient reductions are also charged correctly. To make
explicit the constant in the cited stream lemma: Emax>=D/2 and s<=D/2,
while M>2Emax, so s+1<=M. A raw product coefficient is therefore less
than M^3. If k is the bit length of M, it has at most three k-bit blocks.
The cited Barrett/Horner processor reduces those blocks with at most
three applications of its u<2^(2k) primitive. Each application uses a
fixed number of O(k)-bit multiplications and physical scans. Thus a
coefficient really costs O_alpha(tau(1+log(tau+1))^alpha), and all O(D)
reductions fit H11. No O(tau)-bit word reduction is treated as constant
cost, and no oversized numerator is inserted into the two-block Barrett
formula without splitting it.

Centered representatives are unique because M>2Emax. Adding the aligned
candidate stream yields the actual nonnegative convolution coefficients.
Emission, final signed correction and base-2^b carry propagation use O(V)
scans and O(tau)-bit running registers. The fixed short multiplier's own
visited-space bound applies to the O(s tau)-bit regions reused at every
block.

## 4. One visited cap and the stated n-scale consequence

When K<=V, input, candidate, output, previous block, Q, W, reciprocal and
short multiplication scratch fit O(V) visited cells on a fixed number of
tapes. Sibling blocks start at the same marked origins and reuse regions.
When K>V, the direct packed schoolbook branch uses O(V^2) time and O(V)
visited cells; V^2<=K^6 absorbs it. Subtracting C in that branch also
returns the residual if requested. This bounds all visited cells, not only
peak live values.

For b=Theta(log n) and the stated candidate height, V=Theta(n). If
s<=2^((log n)^nu), log K=O((log n)^nu) and K^6=n^o(1). The fixed
choice alpha=(1+nu)/(4nu)>1/2 gives alpha nu=(1+nu)/4<1/2, exactly
as claimed. This is a conditional correction cost and supplies no fast
way to generate C.

## 5. H2 and the scope boundary

On a linear sequence space V, the prefix-s projection is injective:
a vector with s initial zeroes and its own normalized order-at-most-s
recurrence must be zero by induction. Thus dim V<=s. Applying the same
projection to each of W output rows proves the rank<=Ws version.
Input-dependent recurrence coefficients do not evade this argument.

The stated coordinatewise integer encoding extension also works: the
prefix projection and its kernel remain linear over the original field;
zero-preserving, nonzero-detecting encoding converts a kernel vector to
an integer zero prefix, and its rational recurrence forces it to vanish.
No invalid reduction of rational coefficients into that field is used.
Actual spectral multiplicities and the declared sequence ordering remain
necessary to apply the rank premise. The note properly keeps those
conditions visible.

The finite Hankel boundary example and the zero-prefix counterexample
correctly distinguish H1 from both unrestricted verification and a weak
finite Hankel-rank definition. No general multiplication lower bound is
claimed or obtained.

## 6. Isolated finite replay

Read and copied the author's checker into `replay-dense-recurrence/` before
running it. The isolated replay passed 36 complete integer recoveries,
37 rational reconstructions, 697 packed polynomial products, 330 emitted
blocks, 80 prime-count bounds, 72 linear-prefix controls, 10 finite-Hankel
boundary controls, and the explicit rejected unrestricted-verifier claim.
The three nonunit-prime controls passed too. Its JSON receipt is retained
in that replay directory. This is exact algebra/packing evidence; it is
not a finite-tape time simulation or a formal proof.

No blocking correction is required. The three-block reduction explanation
above makes an already-cited stream argument explicit and does not add a
new premise to the accepted theorem.
