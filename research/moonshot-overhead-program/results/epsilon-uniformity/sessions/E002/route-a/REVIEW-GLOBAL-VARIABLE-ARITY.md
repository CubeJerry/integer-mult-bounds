# Independent A review of the complete variable-arity composition

Status: **accepted as a complete written source-specific composition** for
B's V20, using the exact suppliers below and the physical details in this
review. The lead controls programme admission. This is an AI-assisted
mathematical audit, not a complete tape implementation, formal verification,
human refereeing or priority certification.

Reviewed SHA256 snapshots:

| Supplier | SHA256 |
|---|---|
| B variable-arity-transfer.md | 5c4f71e4596a934c99a22f6a7c34332ef550b6a8a60233144204171a1a542f2a |
| B variable-interchanger-space.md | b4a710a1d2160d07ff2aab206bec9be8d3521fa7d5090c8f7cbe138640e6a97c |
| B composite-radix-padding.md | 011d53c049873648e99a25a1438fd988b08e7d9080340a477c307d6bd31ce6b3 |
| B polynomial-walsh-precision.md | 7dbc8926b2e68840e54f1ce981b5a827f53ab3f29dbe0ea7420ba25093a0ce19 |
| C polynomial-interchange-invoice.md | 311c0d4987fde89502183bf2fb860c2462675667c6ff8e29ce59769d154aa5d1 |
| A VARIABLE-OUTER-SUBSTITUTION.md | 782ccc6677a2343a7797eaf72c4e27c50b25b722d4ec4fd2207a2ccba0408602 |

The earlier E002 reviews identify the underlying formula, repair, address
and numerical arithmetic bytes. Source pin: OpenAI `math`
`3344da59991ed94f9ba711217b29c1d760badfa6`; programme predecessor
`0607d044d1d09489580da0e5828588820e1a6775`.

Put Phi(y)=(y+1)^(2/3)(log2(y+2))^(1/3), L(n)=1+log2 n. The conclusion
is one fixed exact finite-alphabet multitape full multiplier with

    T(n)<=n sqrt(L(n)) 2^{O(Phi(log2 L(n)))},
    cells ever visited=O(n).

This gives every fixed beta>2/3 in a weaker 2^{O(x^beta)} envelope,
x=log2 L(n). It does not give log-free beta=2/3, polynomial-x overhead,
constant overhead or a general runtime lower bound.

## 1. Rational radix and complete child ranges

The rational dictionary is polynomial m in count, dimension and height.
Its complete product includes every pivot, inverse and required diagonal
unit. The source has no address-ring rank calculation after specialization.
Thus b congruent to 1 modulo this even product is valid modulo all b^f,
including composite b. Scalar F4 and numerical rationals remain separate.
A's composite-radix review and exact replay verify the root choice, tiny
initial padding and polynomial(u,H) preparation. Moving a b-valued coordinate
uses O(log b) binary split/merge moves, with less-than-two temporary padding.
There is no numeric-b work factor or growing physical tape count.

Because e log2 b is between u and u+O(1/u), the child's binary width is
v=ceil(f log2 b)<=u/m+2. Its lower bound also follows from the floor:

    f log2 b >= u/(m+2a)-2log2 b >= u/(4m)

under a<=m/2 and u>=32m(H+1). A rounded integer-power test suffices.
Small fixed gamma makes all such guards automatic at large u for
m=Theta(u^gamma). Remaining failures are explicit direct bases. Every
child's two-field binary padding factor below four remains in the mass;
occupied reserves and genuine-address subsets are restored on return.

## 2. One field and sharpened local storage

Use one root field F_(2^s), with even power-of-two s=O(log U). The ternary
seed count is the least 3^r with (3^r-1)/2>=m and is monotone, so enough
root nodes suffice at every descendant. Irreducibility tests and a search
for a root of T^2+T+1 construct the field and its actual F4 generator in
polynomial(root m) time. Descendants use distinct coordinate strings as
Vandermonde nodes in this field. No field enumeration occurs per coefficient
and no symbol embedding is repeated. The one O(log U) initial factor fits
Phi. Arbitrary root-field inputs satisfy the exact repair identity.

The guards u>=m^K and u>=K log2(s+2) pay fixed polynomial descriptions and
scratch. Module rows retain at least 2^{2u-m^{C0}} payload, at least 2^u
in the guarded range. Their short headers fit. For HS, log Q>=u/(4m)
dominates coefficient height m^C, so every increasing run pays its header.
The transpose grid is at most fourfold and inverse scaling reverses the
same small-coefficient arrangement. Elementary triangular operations reuse
regions. None of these claims infer cheap execution from bit height alone;
they use the explicit HS run-sort algorithm and its long-fibre guard.

Move the B or 32B role coordinate to the fast position by short-coordinate
moves. Each (module,address) block has B field values and pays one list of
m ternary labels. A single reused polynomial(m,s) buffer emits and applies
the selected small matrix. Labels and matrices are not retained per scalar.
Restore role order and remove metadata before every child.

Prepared endpoint arrays occupy O((1+lambda)V), where
lambda<=2^{C Phi(log m)}. All m queries' low-rank vectors together occupy
`(m r/N)V<=V`. Consume each rectangle/query sum immediately into its direct
and basis-row contributions, then release that sum. Keep prepared source
copies and destination accumulators through all queries. This preserves
source endpoint sharing without storing all rectangle-query sums or
repeating endpoint conversions per query. Factors use serial terms and
ping-pong arrays.

## 3. Spatial time and the visited-region stack

The final VS snapshot has a consistent binary-entry convention: a node's
initial padding is at most two; main-child fraction is at most 16/N with
N>=64; reserve-path growth is at most 8^d. Finite repair has 1/16 volume
inside its padded node. Main descendants are contractive. Reserve descendants
clear the other payload first and park only descriptors. Spatial depth is
d=O(log log U), so 8^d and the number of ancestors are polynomial in log U.
Their product with the largest endpoint factor still fits the Phi envelope.
Finite-repair ancestors form geometric volume series at each spatial scale.
Siblings reuse marked intervals, bounding all visited cells.

For time, choose m=Theta(u^gamma) with gamma K<1/4 and gamma smaller than
all preparation/height guards require. The actual one-level mass is
`C sqrt(m) 2^{C Phi(log m)}`, including initial, child and reserve padding.
Normalize I_s(u) by sqrt(u+1). The local term is at most Cs^K because
m^K/sqrt(u+1)<=C. The recursive factor is bounded by

    C sqrt(m) sqrt((u/m+3)/(u+1)) 2^{C Phi(log m)}
      <=2^{C' Phi(log(u+2))}.

Widths decrease by u_next<=u^{1-gamma/2}. Their logarithms therefore
decrease geometrically, and the sum of their Phi values is bounded by a
constant times Phi(log(U+2)). Expand the recurrence: products of recursive
factors have that envelope; the number of terms, s^K and terminal direct
cost are polynomial in log U. The root-field base u<K log(s+2) has only
polylog(U) width. All other failed guards occur below a fixed cutoff.
This proves V7 and the refined stack proves V8.

Generation can be as large as 2^{U^eta} poly(log(2V)), eta<1 fixed.
It is still O(V) when V>=2^{2U}: for large U, 2^{U^eta}<=sqrt(V), while
any fixed power of log V is at most a constant times sqrt(V). The finite
width chain is prepared once and retains compact plans. Optional expanded
archives are erased and their visited region remains charged.

## 4. Numerical arity, exact batching and local routing

The numerical family must grow more slowly than polynomial active width.
Its integer cube-root rule gives log m=Theta(Phi(y)), y=ceil(log2(a+2)).
For large a, A=Theta(m) and even f<=a/A produce
`y_child<=y-c Phi(y)`. The remainder has fewer than 2A bits and is handled
by direct small butterflies; its polynomial-m toll is already local.
No approximate root or noncomputable parameter choice is needed.

The numerical batch W_m is a power of two: the binary pairwise seed count,
binary label count q^L and replication factor 8^h are all powers of two.
This is explicit in the predecessor growing-arity construction. Along a
chain, f_i<=a_i/(2m_i) gives sum log m_i<=log a_0+O(1), so
product W_i<=(a_0+2)^C. The initial q=2^{k-a_0} spectator rows eventually
exceed that product, and both are powers of two. Hence exact divisibility
holds at every child, whose volume is precisely V/W_i. Preflight tests this;
there is no repeated leading-padding multiplier.

The initial selected-bit gather and final undo act once at full k width.
Every internal child already has one contiguous f-bit slot. Local column
and position changes use only its active a bits: split that field into
three subchunks as in the source two-involution proof. Guards remain
O(log k), while every interchanger width is O(a). For a shorter than the
guard, direct bits cost O(V log k). This gives the required local
sqrt(a+1)*2^{O(Phi(log(a+2)))} toll, with fixed log k factors, as proved
in VO6 of A's outer substitution. No global sqrt(k) gather is repeated
at each numerical node.

## 5. Numerical recurrence, precision and its physical space

Polynomial(m) local maps and short-rational scalings add only
2^{O(Phi(y))} to the local toll. Recursive mass after sqrt(a+1)
normalization is 2^{O(Psi(y))}, where
Psi(y)=(y+1)^(1/3)(log2(y+2))^(2/3). Thus V15 is the actual physical
recurrence, not the predecessor arithmetic-only recurrence.

For large y the interval [y-c Phi(y),y] lies in [y/2,y]. On it,
Phi'(t)>=c0 y^(-1/3)(log2 y)^(1/3). Integrating over length c Phi(y)
gives `Phi(y)-Phi(y-c Phi(y))>=c' Psi(y)`. Integer rounding is absorbed
by reducing c and increasing the fixed base. Choose B>C2 and Bc'>C3
with strict slack. The recursive term in V15 is at most
2^{B Phi(y)-(Bc'-C3)Psi(y)}; the additive term is 2^{C2 Phi(y)}.
For large y each is at most half the claimed majorant after increasing
B and the fixed base constant. This is a valid inductive solution of V15.

Local logarithmic norm gain is polynomial m. Its sum along a path is at
most O(log k)*2^{C Phi(log(k+2))}=k^{o(1)}. Branching is polynomial m,
and sum log m_i=O(log k), so the entire numerical recursion has only a
fixed polynomial number of arithmetic node types/events. The common-ancestor
argument propagates each fault through at most this sublinear logarithmic
gain. A block-diagonal spectral map uses its largest block norm. Absolute
O(k) signed and fractional precision therefore covers all intermediate
norms, the number of errors and the fixed source accuracy target.

The final plan computes a numerical upper bound for gain and event count
and checks it against a fixed fraction of k. Failure uses direct normalized
Walsh at the independently sufficient absolute precision. Thus every length
has a correct format, and the fast branch succeeds uniformly at sufficiently
large k. W1 applies a short exact rational to a long record with the required
k factor; full k-bit products still use the source O(k log k) multiplier.

Numerical local arrays cost V*m^K*2^{C Phi(log(a+2))}, with
m^K=2^{O(Phi(y))}. Children have exact volume V/W_m<=V/2, and finite
repair keeps its 1/8 ratio. The maximum local coefficient times the geometric
parked-volume series bounds numerical visited space. A called interchanger
returns the original numerical record format before a Fourier child begins;
its temporary field encoding is not inherited as that child's payload.
This proves V17, including its physical space statement.

## 6. Outer transfer, setup and actual plan access

A's separate VO1--VO6 proof rereads the entire actual permutations/integers
source. Guarded XOR, position involutions, Beneš blocks, balanced CRT and
synchronized short transforms preserve only fixed log k powers. They fit
the Phi envelope. Phase streaming writes fewer than 2N products and retains
the source short multiplier. The numerical allowance supplies the exact
source 13k norm/50k error budgets; rounding and carries give the full exact
2v-bit product. This establishes V18 after V7/V8/V17.

The corrected setup bound is 2^{k^{eta'}}, with one fixed eta'<1.
The numerical family alone permits the stronger 2^{k^{o(1)}}; optional
exact-interchanger checks at U approximately k need only satisfy the weaker
fixed-power bound. Polynomial counts of preparations fit a slightly larger
eta'. This is 2^{o(k)}, so it is absorbed in the 2^k-record volume and is
n^{o(1)} for final chunk preparation. No proportional archive lookup is
hidden in that additive bound.

For the final all-width cache, use its charged sequential lookup at the
external numerical/address-wrapper invocation boundaries; their total count
is polynomial k. Internal spatial descendants retain their root invocation's
local width chain and current compact descriptor. They do not scan the
entire all-width cache for every small child or payload record. Child-plan
copies are priced by the guarded node's payload and compact local grammar;
direct bases only need the opaque record/range descriptor. This is the
concrete implementation of the declared once-prepared width chains and
avoids multiplying a global polynomial-k lookup into the spatial recurrence.

## 7. Final integer caps, correctness and common visited cells

After the ordinary O(n) input-length scan, compute the integer cube-root
scale for Phi(log2 L(n)). Choose r as a power of two with exponent a fixed
large multiple of that scale, and v=ceil(n/r). The fixed constant is chosen
to dominate V18's space coefficient and the factor eight. If an early length
cannot fit the computed parameter or preparation, the marked cap stops
before an out-of-range visit and invokes exact schoolbook multiplication.
The input-length scan itself is ordinary wrapper work, not part of the
sublinear n/16 finite-construction allowance.

Eventually log r=O(Phi(log2 L(n)))=o(log2 L(n)), r<=n, and
log2 v=log2 n-O(Phi(log2 L(n))). Monotonicity of the Phi space majorant
then gives `space(v)<=n/8+o(n)` with the chosen r. Combined preparation
has size at most 2^{L(n)^{eta'}}=n^{o(1)} and passes its n/16 budget.
All root and descendant shape/precision guards are eventually satisfied;
the separate absolute prime-shape cutoff is eventually passed as well.
Its numerical value is not needed by the machine.

There are r^2 exact chunk products, each of the same length and using the
same prepared descriptions. Their core regions are reused. The actual
positional wrapper has O(nr) movement/carry work and r^2v<=2rn, giving

    time <=n r sqrt(L(n)) 2^{C Phi(log2 L(n))}+n^{o(1)}
          <=n sqrt(L(n)) 2^{O(Phi(log2 L(n)))}.

This is eventually below the n^2 body cap. Every shorter input also halts
correctly by the capped attempt and exact fallback. Input, output, wrapper,
constructor, numeric and stack regions are a fixed set of marked O(n)
intervals. Reuse across calls, failed attempts, cleanup and fallback bounds
the union of visited cells by one absolute O(n), rather than by a varying
candidate-space constant.

## 8. Audit result and limits

The final B snapshots incorporate the two requested corrections: fixed-eta
combined preparation and binary-entry padding constants 16/N, N>=64, 8^d.
The local-width gather distinction and exact precision guard are explicit.
With the actual call-boundary/cache interpretation above, no remaining
unproved proportional-cost premise is needed for the stated complete
written theorem. The separate proposed streamed-Lagrange optimization is
not a premise and is not used to hide its physical layout obligations.

Finite arithmetic and permutation replays support their component identities
only. This global proof does not execute a complete astronomical multiplier,
claim a practical cutoff or a proof-assistant refinement. It compares the
programme's explicit upper envelopes, not an unspecified published o(1).

Open next questions: improve the label/endpoint mechanism or its complete
call invoice to beat the Phi scale; refine the optional low-storage repair;
or implement a substantially smaller complete physical example. None is
required for the accepted written bound above.

Credits: Jerry Chen (@CubeJerry), pinned OpenAI source and cited prior work,
predecessor programme constructions, E002 component authors and substantial
AI-assisted independent derivation and review.

## 9. Lead theorem review

I read the complete `lead/variable-profile-theorem.md` draft at SHA256
`bb61c3970877fde81d88f45a0ba0a5a956b0f796def9fd3e916165cc61f291e5`,
then inspected its sole cache-access clarification. The resulting SHA256
`ccad2873bfa36755382495a24c488d1cdfd622f562fb1c8b3cd7712b6a4b9cb4`
is **accepted in full** as the complete written theorem V*.

The lead statement preserves the proof order, the two arity schedules,
fixed-field interpretation, binary-entry padding constants, explicit
gain/precision checks, fixed-eta setup and actual integer common cap.
Its Section 5 now limits the all-width cache scan to external invocation
boundaries and retains local chains inside spatial recursion, exactly as
specified in this review. Its final Section 6 uses an integer ceiling
cube-root and an added absolute C5 to cover constants in the common-space
factor. I found no further mathematical correction needed for these bytes.

The root statement also explicitly credits concurrent S003's separately
admitted same-scale predecessor. Acceptance here is a source-specific
independent construction/review, not a claim of priority over that work.

## 10. Narrow B cache amendment

Inspected B's replacement cache paragraph and verified resulting SHA256
`243849c3349a2ae9e48e5d48e259f510dc63283e24e3d7a4c45a0836615a7d19`.
**Accepted:** this is the concrete external-boundary-only lookup already
required and justified in Section 6 above. Internal spatial descendants
retain the local tail chain/current compact descriptor; its size and copying
fit polynomial(local m,s) dispatch. The VS snapshot remains
`b4a710a1d2160d07ff2aab206bec9be8d3521fa7d5090c8f7cbe138640e6a97c`.
No other mathematical premise or target changes. The whole acceptance now
applies to this amended B snapshot and lead theorem `ccad2873...`.
