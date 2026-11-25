# Independent global review of the variable-arity tape envelope

Gate: **PASS as a complete written mathematical algorithm/profile
composition**, using Route B's amended V1--V20 and the completed outer
source transfer `variable-arity-outer-transfer.md` in this directory.
The separate space review also passes. No remaining blocking obligation
was found after the preparation and precision-guard corrections.

This reviews the whole envelope, not merely the numerical recurrence.
Source pin: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`,
November tape construction. Programme predecessor:
`0607d044d1d09489580da0e5828588820e1a6775`.

## 1. V1--V6: a fully charged interchanger recurrence

Composite specialization uses the complete rational-unit list, not a
field assertion over the composite address ring. The near-root congruence
selector has combined initial padding at most `1+1/(u+1)`. The source
one-leading-digit partition gives

\[
v=\lceil f\log_2 b\rceil\le u/m+2.
\]

The reverse estimate needed by the header-space proof is also valid:
`f log_2 b>=u/(m+2a)-2log_2 b`. With `a<=m/2`,
`log_2 b<=2H+2` and `u>=32m(H+1)`, it is at least `u/(4m)`.
These guards eventually hold for the fixed sufficiently small gamma and
remain actual tests. Child conversion to two binary ranges costs less
than four and is explicitly included in V4; it is not attributed to the
tiny initial padding bound.

Selecting odd `m=Theta(u^gamma)` is effective by integer root comparison
and monotone in u. All source main and reserve children at a spatial
depth have the same raw field width, hence the same next binary width.
The whole deterministic chain can be prepared once. With gamma below
all fixed construction reciprocals, optional preparation is
`2^(U^eta) poly(log(2V))`, eta<1. Since `V>=2^(2U)`, this is O(V)
uniformly in arbitrary spectators: for fixed polynomial degree,
`(log V)^C/V` decreases beyond a fixed threshold, and at the minimal
V its exponentially small ratio absorbs `2^(U^eta)`.

One root field with `s=O(log U)` bits supplies all descendants. Its
explicit F4 generator search is charged once. Neither E coordinates nor
temporary labels are passed through a new embedding at each child.
The local ordinary coefficient is `m^K s^K`. After dividing V5 by
`sqrt(u+1)`, the local term is at most `Cs^K` when `gamma K<1/4`.
The normalized child coefficient is bounded by
`2^(C Phi(log(u+2)))`, since
`sqrt(m)*sqrt(v+1)/sqrt(u+1)=O(1)`.

Above the base, `v<=u^(1-gamma/2)`. Therefore logarithmic widths
decrease geometrically. Their Phi sum is at most a fixed multiple of the
root Phi: bound all logarithmic factors by the root's and sum the
geometric powers `y_i^(2/3)`. Depth, one-time s expansion, and the direct
base `u<K log(s+2)` cost only powers of log U. Thus V7 follows with
an absolute fixed constant, including all local costs and setup.

## 2. V8: the sharper space estimate is necessary and supplied

The companion review `review-variable-interchanger-space.md` checks the
full space proof. Its decisive facts are these. Whole-row keys are
headers paid by complete spatial payloads. Rational run headers fit
because `log Q=Omega(u/m)` dominates coefficient heights. Spectral
roles are moved to the fast position by direct O(log m) binary moves;
one m-label list is appended per B-element block, not per field scalar.
The small spectral matrix is one reused buffer.

The source retains at most `O((1+lambda_m)V)` prepared endpoint copies
and accumulators. The geometry bounds this by the desired Phi envelope.
All `m r_m` low-rank query vectors together occupy at most V by the
exact rank fraction. Consume each rectangle/query sum into these vectors
immediately, rather than storing every sum. This preserves shared endpoint
preparation and the original recursive-call count.

Finite repair has 1/16 child volume. Under the final conservative
binary-entry convention, a grouped spatial main child has at most
`16/N_m<=1/4` when `N_m>=64`. Reserve calls can inflate entry payload
by eight, but park only descriptors; their O(log log U) levels
contribute only a power of log U. Retained compact plans, fixed-field
data, local buffers and parked payload fit the root Phi envelope.
Marked sibling/stage regions are reused, bounding visited rather than
merely live cells. This proves V8; the older polynomial-m space estimate
alone would not have sufficed.

## 3. V9--V14: growing numerical arity and actual tape costs

The prior rational geometry supplies uniformly
`sigma_m/W_m<=C sqrt(m) exp_2(C sqrt(log m log log m))`,
`2m<=A_m<=4m`, and polynomial-m exact power-of-two W_m. These bounds
follow from the displayed even-L, power-of-two-q construction in the
accepted `growing-arity-circuit-candidate.md`; no new search/field
assumption is introduced.

The new slower numerical schedule has `log m=Theta(Phi(y))` at
`y=ceil(log_2(a+2))`. Its even f and direct even remainder preserve
the full normalized transform; the remainder is O(m) bits and belongs
in the polynomial-m local toll. For sufficiently large a, the child
logarithmic width decreases by at least `c Phi(y)`.

Batch divisibility is exact. Since `f_i<=a_i/(2m_i)`, telescoping gives
`sum log m_i<=O(log(a+2))`, and hence the product of W_i is at most
a fixed power of a. Every W_i is a power of two. The original spectator
count `q=2^(k-a)` therefore contains that divisor above a fixed cutoff.
Preflight tests it. Initial selected-position gathering and final return
occur only at the layer root. Internal children have contiguous active
slots and full spectators, so local routing really depends on a rather
than the full k at every recursion level.

Exact rational record scaling has its factor k. Polynomially many column
changes use the completed V7 interchanger and guarded-XOR wrappers.
Their cost is V12, with `m^K sqrt(a)` and the Phi envelope charged.
After `log m=Theta(Phi(y))`, that polynomial coefficient contributes
to the local exponential, not an omitted per-child payload factor.
All metadata is stripped before numerical children.

The path logarithmic numerical gain is at most
`O(log k) 2^(C Phi(log(k+2)))=k^o(1)`. Telescoping also bounds the
product of polynomial-m branch counts by a fixed power of k. This
controls both arithmetic events and intermediate norms. The amended
actual gain/event-count guard makes a fixed absolute O(k) format sound
at every accepted length. Failed guards have the source direct normalized
Walsh fallback. Block-diagonal spectral maps use the maximum block norm,
not their exponential number of possible cases.

## 4. V15--V17: the numerical majorant closes with strict slack

Normalize by `V sqrt(a+1)` and retain the one common fixed power of
`1+log(2+k)`. The local term is at most `2^(C2 Phi(y))`.
The logarithm of the recursive multiplier is at most

\[
C\sqrt{\log m\log\log m}
 =O\bigl(y^{1/3}(\log y)^{2/3}\bigr)=O(\Psi(y)).
\]

For large y, the interval `[y-c Phi(y),y]` lies in `[y/2,y]`.
On it, differentiation gives
`Phi'(t)>=c_1 y^(-1/3)(log y)^(1/3)`. Multiplying by the interval
length proves `Phi(y)-Phi(y-c Phi(y))>=c' Psi(y)`.
Choose B with `B>C2` and `Bc'>C3`. Substitution in V15 yields,
after division by `2^(B Phi(y))`,

\[
2^{-(B-C2)\Phi(y)}+2^{-(Bc'-C3)\Psi(y)}<1
\]

for all sufficiently large y. Enlarge B over the fixed base. This proves
the inductive majorant with actual slack for the additive term; it is not
only a differential heuristic. Rounding y to integer widths is harmless
after decreasing c and enlarging the base.

Local space V13 has coefficient `2^(O(Phi(log(k+2))))`. Numerical
children have volume at most V/2, and finite repair has its stricter
contraction. Parked arrays sum geometrically under the largest root
coefficient. Successive layers/siblings reuse regions. Thus both bounds
in V17 follow, including root gather/return and the fixed polylog factor.

## 5. V18: outer-source gate closed

The complete transfer is written in `variable-arity-outer-transfer.md`
(OT1--OT5). Its proof repeats the source guarded-XOR construction with
the monotone interchanger bound `sqrt(U+1) H(U)` instead of U^rho.
The number of equal-width calls per pass is bounded, so the substitution
is legitimate. Guard arithmetic has an absolute fixed polynomial degree;
interchanger construction is already charged in its own call and is not
a new prefix-control function. Position permutations and controlled
small blocks therefore add only the source fixed powers of log k.

The actual outer CRT tables have absolute fixed-degree size, use a fixed
positive free fraction, and retain the separate short-axis primes and
their tested absolute cutoff. Synchronized short Fourier transforms add
O(log k) unitary layers. Phase streaming and coordinatewise products use
the original fixed O(k log k) short multiplier. With the amended absolute
precision guard, the source exact rounding/carry conclusion applies.
Consequently V18 follows from V7/V8/V17; it need not remain an open gate
once this source-substitution proof is included.

Preparation has been corrected throughout. Walsh-only optional setup is
`2^(k^o(1))`, but top-width interchanger archives may cost
`2^(k^eta)` for fixed eta<1. Polynomially many calls/widths are safely
covered by `2^(k^eta')`, eta<eta'<1, after increasing the cutoff.
This is still sublinear in the digit length. It is not mislabeled as
`2^(k^o(1))` and never becomes a per-record lookup charge.

## 6. V19--V20: actual common-cap machine

The integer cube-root rule selects a power-of-two chunk count with
`log r=Theta(Phi(x))`, `x=log_2 L(n)`. Its fixed coefficient can be
larger than the proved space constant. Then `v=ceil(n/r)` has
`log v=log n-O(Phi(x))`, and the core's
`2^(O(Phi(log L(v)))) v` workspace is at most n/4 eventually.
Construction `2^(L(n)^eta')` is n^o(1), hence passes the marked n/16
preparation cap. Compact plans and each successive chunk use the same
regions. Inputs, output, exact positional assembly and clocks add a
fixed multiple of n.

The r^2 products have `r^2v<=2rn` eventually and
`L(v)<=L(n)`. Their total time, plus O(nr) assembly, is bounded by

\[
n\sqrt{L(n)}\,2^{O(\Phi(x))}.
\]

This is n^(1+o(1)), so the quadratic actual-step cap eventually does
not abort. Every shape and numerical guard eventually passes uniformly.
For any other length, the bounded attempt cleans its visited regions and
uses exact schoolbook. Crossing the fixed O(n) allowance is stopped before
the offending head move. Therefore one fixed machine computes every full
product and has one uniform O(n) bound on all cells ever visited.

The final accepted scale from this composition is

\[
T(n)=O\!\left(n\sqrt{L(n)}
 2^{O(x^{2/3}(\log_2(x+2))^{1/3})}\right),\qquad
\operatorname{visited}(n)=O(n).
\]

It implies a fixed-beta envelope for every beta>2/3. The logarithmic
factor is retained; this is not the pure beta=2/3 expression or the exact
square-root endpoint. The conclusion is a written mathematical algorithm
and source composition, not a full machine execution, human referee
certification or formal build.

Credits: @CubeJerry; pinned OpenAI manuscripts and prior programme
constructions; E002 Routes A/B/C and the lead; substantial ChatGPT
multi-agent assistance.

## Reviewed final snapshots

- Route B `variable-arity-transfer.md`:
  `5c4f71e4596a934c99a22f6a7c34332ef550b6a8a60233144204171a1a542f2a`.
- Route B `variable-interchanger-space.md`:
  `b4a710a1d2160d07ff2aab206bec9be8d3521fa7d5090c8f7cbe138640e6a97c`.
- Route B `composite-radix-padding.md`:
  `011d53c049873648e99a25a1438fd988b08e7d9080340a477c307d6bd31ce6b3`.

Exact copies were retained in `reviewed-snapshots/` while this review was
written, so subsequent author edits do not silently change its scope.
The final amendments include the explicit lower field-width guard, root
omega search, row-payload bit budget, all-width compact preflight cache,
computed precision guard, combined eta' setup bound, and completed A/C
outer suppliers. These amendments have been checked.

The subsequent narrow cache-access amendment is also accepted, at SHA-256
`243849c3349a2ae9e48e5d48e259f510dc63283e24e3d7a4c45a0836615a7d19`.
Global all-width scans occur only at polynomially many external numerical
or address-wrapper invocation boundaries. Spatial descendants carry the
root invocation's unused local chain suffix/current descriptor, whose
size is polynomial in local m and root field degree s; parent dispatch
charges its copying. This explicit realization is audited in
`review-variable-profile-theorem.md`. No other supplier change is inferred.
