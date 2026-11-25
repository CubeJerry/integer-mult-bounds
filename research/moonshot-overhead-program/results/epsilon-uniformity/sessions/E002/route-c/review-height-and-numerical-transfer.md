# Independent C review of the height, numerical and direct-selection components

Reviewer: E002 Route C, a separate agent from the authors. This is written
AI-assisted mathematical review with isolated finite replays. It is not
human refereeing, a formal-kernel proof, or a complete tape implementation.
Snapshot hashes are appended below. Source pin:
`openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`.

## 1. A's height-priced affine streams

**Accepted within its stated fixed-tape scope.** I read
`HEIGHT-PRICED-AFFINE-STREAMS.md` in full, checked each forward/inverse
index identity, and replayed the supplied checker in an isolated directory.

For positive reduced a<Q with gcd(a,Q)=1, the runs beginning at
`ceil(rQ/a)` map to the residue `t_r=(-rQ) mod a`. Their lengths are
q+1 for t_r<s and q otherwise when Q=aq+s. This accounts for both the
ragged final column and the required minus sign. Inverse sorting uses
`-t*(Q mod a)^(-1) mod a`; its arithmetic stays at O(log a) bits, so it
does not introduce the large residue a^(-1) mod Q as a new multiplier.

The sort moves whole equal-padded runs, with only O(log a)-bit headers.
It uses a constant number of tapes; sorting on h bits costs polynomial
h passes, not a parallel a-tape operation. Padding a rows to the next
power of two and q columns to q+1 enlarges payload by less than four.
The short row field is transposed by its h individual bits, retaining
arbitrary prefix/suffix ranges. Known padding positions are removed,
never data-dependent zeros. The inverse restores the same slots.

I checked the proposed setup absorption: initial poly(h+log V) work is
bounded by V poly(h), and each per-run poly(log q+log B) counter/reset bill
is bounded by a fixed constant times qB. The total a runs are therefore
paid by Q B, with polynomial h overhead. Prefix spectators are advanced
amortizedly rather than fully read for every run. Signed/rational units
compose a bounded number of those processors. The lower-triangular
corollary keeps the source descending target order and preserves its
field-permutation invoice for general matrices.

The isolated replay `replay-height/` passed 8,562 forward, 8,562 inverse,
8,562 signed, 4,996 rational and 312 transpose cases, plus 527,486 run
identities. It rejected 7,989 wrong-sign and 8,177 ragged-padding controls.
These are finite permutation tests, not physical machine execution.

## 2. B's rational scaling and on-demand coefficients

**Accepted W1--W2 with the stated aligned-row/spectral-bit interface.**
I checked W1's long-times-short multiplication and restoring long division.
There are h sequential shifted-add passes of O(k+h) bits and O(k+h)
division steps of O(h) work each. All returns to the short remainder tape
are included. Signed floor correction uses the nonzero remainder and has
one extra scan. Consequently exact coefficient use costs O((k+h+1)(h+1))
and introduces less than one last-bit-grid unit of error. It does not
replace arbitrary long multiplication by a cheap primitive.

Against `pairwise-newton-division.md`, I verified that its spectral values
are odd integers and the target is ±1. Only the actual defect set is used,
so every inverted gap is a nonzero even integer. Generalized binomial
recurrence remains integral at negative counts. All counts, truncation
orders and W=O(m) seed roles have polynomial size. The first ell rows of
the Vandermonde restriction have nonzero determinant; the inverse and
transpose inverse produce exactly the two-predictor repair, including
ell=0. Common denominator and minor bounds give polynomial coefficient
and intermediate bit height. Scanning the entire polynomial-sized matrix
for each algebraic access is still a valid fixed-tape polynomial bound.

W2 therefore removes an exponential frequency-table access from execution.
It does not assert that spectral masks are available before the paid
converter. For numerical records their O(k) address examination is paid
by their Theta(k) record width. Coefficients remain rational and are not
reduced into the characteristic-two interchange field.

## 3. B's absolute precision threshold

**Accepted W3 under its explicitly stated finite rational-template bounds.**
The block-diagonal spectral operator has norm equal to the maximum block
norm; its number of possible spectral cases is not a norm multiplier.
Dimensions, partial sums and coefficient heights are polynomial in m, so
the local logarithmic gain is polynomial m. The common-ancestor propagation
argument contributes this amount times O(log k), while completed child
Walsh maps are unitary.

The event count is polynomial in k and m: branch count m^K and arity at
least m give only a fixed power of k, and base-A pieces add polynomial
factors. Counting all rounded coordinates contributes the explicit 2^(k/2)
Euclidean factor. Coefficient faults from the fixed irrational/source
phases are multiplied by the stated intermediate norm bootstrap. Thus
W6 conservatively bounds every fault propagated to every relevant boundary.

For k>=m^K2 with a sufficiently large absolute K2, the term
`C' m^K4 log(k+2)` is at most k. Choosing fixed p=O(k) therefore controls
absolute output error at every boundary and simultaneously closes the
integer-part norm bootstrap. The polynomial threshold is sufficient;
no claim is made that its exponent or finite cutoff is practical.
Preparation and physical routing remain separate costs, as the note says.

## 4. B's separated-setup transfer

**Accepted as a complete conditional theorem under F/E/N/R.** I checked
`separated-setup-transfer.md` in full. Its physical premises are not
established merely by the transfer proof, and the displayed stronger
multiplication rate is conditional until all components are admitted.

S1 safely absorbs `2^R (1+log n)^v`, v<=R, under its explicit quadratic
log-input guard. S2 overcounts the whole recursion's non-volume setup,
including repeated preparation, by another `2^(m^K)L(n)^(m^K)` term.
The recurrence margins are used only for volume-proportional work.
Visible log-log factors are paid by the available 1/(2J) exponent slack.
Reuse of marked regions and the stated parked-volume contracts are needed
for visited, rather than live-only, space.

The selector uses only integer quantities: the largest dyadic J=2^h with
J^4 h<=q. Maximality gives J=Theta((x/log(x+2))^(1/4)). Its physical family
parameter has log m=O(J^3 log J)=o(x). Therefore even its permitted
additive generation `2^(m^K)L(u)^(m^K)` takes n^o(1) steps for large n and
passes the n/16 cap. The chunk factor r=O(m^K) has log r=o(x), preserving
the sufficient log-input threshold and making the common proportional
workspace fit the marked O(n) regions. All finite failed lengths fall
back to exact schoolbook computation.

The diagonal positional wrapper has r^2 products of size ceil(n/r),
total r^2u<=2rn, and O(nr) movement/carries. This gives
`log H=O(log m)+x/J=O(x^(3/4)(log(x+2))^(1/4))`. The complete successful
bound is eventually below the n^2 clock cap. No weighted-search index
penalty is assumed away: this is a different, directly selected fixed
machine, with charged preparation, sound fallback and common cells cap.

The threshold, branch and workspace hypotheses must be updated if any
actual new processor inflates child payloads or requires an exponential
per-volume scan. The transfer itself correctly rejects those possibilities.

## 5. Composition cautions retained

Temporary comparison labels, row-sort tags and field metadata must be
removed before paid child calls. A polynomial tag factor allowed in local
work is not automatically allowed in the recursive-call coefficient.
Grouping module rows into a prefix call preserves total volume-weighted
calls, but gives the weaker child fraction 2/N_label, not 2/W; the former
still contracts uniformly once N_label>=3. The complete interchanger
invoice states these points explicitly. No gate here establishes a
complete multiplication theorem by itself.

## 6. Reviewed source snapshots

- `e002-route-a/HEIGHT-PRICED-AFFINE-STREAMS.md`: `8c28e7886faf8ede9b6d54f4eec2fe9b260c73996ed8c6b1ccc0e8c052c9c8a3`.
- `e002-route-a/verify_height_streams.py`: `be01035ba5ae04de6aafc224fde24ff79da4ae13c79b0692bc4a3a53c3403299`.
- `e002-route-b/polynomial-walsh-precision.md`: `7dbc8926b2e68840e54f1ce981b5a827f53ab3f29dbe0ea7420ba25093a0ce19`.
- `e002-route-b/separated-setup-transfer.md`: `e2d4aab0a74edf4acac884588728d734524e112a3e4f92ec0eeb62f572aa8ed5`.
- `e002-route-b/verify_rational_walsh.py`: `dee120e42ae4d4ba0637a015e1f2e331df35ac382ea2dbf0d6cfca4ae75db5f7`.
