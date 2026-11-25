# Outer tape transfer for the variable-arity bounds

Status: **complete source-specific transfer from V7/V8/V17**, with an
explicit common-space wrapper. It closes Route B's outer-source gate V18;
the local variable proofs still require their independent reviews.

Source pin: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`,
November tape `permutations.tex`, `walsh.tex`, `integers.tex` and
`uniformity.tex`. Prior programme pin:
`0607d044d1d09489580da0e5828588820e1a6775`. Local suppliers are E002's
compact execution, rational precision, composite radix, variable space and
variable recurrence notes.

Write `Phi(y)=(y+1)^(2/3)(log_2(y+2))^(1/3)` and
`H(t)=2^(C Phi(log_2(t+2)))`. Increasing the fixed C absorbs fixed
powers of `1+log(t+2)`, fixed multiplicative rescalings of t and fixed
constants. This follows by taking logarithms. H is monotone.

## OT1. Local contracts

Assume an exact fixed-alphabet, fixed-tape interchanger on two complete
U-bit fields and arbitrary complete spectator ranges satisfies

\[
T_I(U,V)\le C V\sqrt{U+1}H(U),\qquad
S_I(U,V)\le C VH(U).                                  \tag{OT1}
\]

V is original bit volume. Encoding, movement and preparation are charged;
space counts visited cells. The output has its original representation
with precisely the requested field swap.

Assume the growing-arity selected-bit Walsh processor on `N=2^k`
numerical records of absolute width `Theta(k)`, with at most
`c_0 k/log(2+k)` selected bits, satisfies

\[
T_W\le C V\sqrt{k+1}H(k),\qquad S_W\le C VH(k).        \tag{OT2}
\]

Gathering/return, paid converters, rational arithmetic and precision are
included. It attains the source's fixed absolute error/input-norm budgets
at absolute O(k) precision above tested guards, retaining a direct fallback.
These are V7/V8 and V17, together with their numerical correctness proof.

## OT2. The source routing wrappers accept this monotone bound

Bulk XOR uses a bounded number of equal-width interchanges of width L
per guarded pass. It does not require the interchanger's bound to be a
power law. Substitute OT1 to obtain

\[
T_{\rm xor}(L,V)\le C V\sqrt{L+1}H(L)(1+\log k)+\operatorname{poly}(k)
\]

and `C VH(L)+poly(k)` visited space. The guard constant stays absolute.
Control, offset and destination computations are fixed integer algorithms
of fixed polynomial degree in k. A target run has at least `2^G`
records to pay its once-per-prefix offset. The exceptional fraction
`80k 2^-G` pays destination calculation and the stable sort. Choose
`G=C_g ceil(log_2(2k))` after those degrees. Widths L<G use at most
G direct bit moves.

Interchanger-template construction is inside OT1; it is not a control
calculation paid anew at every prefix. The numerical address has O(k)
bits and record width Theta(k), so exceptional O(k)-bit tags have constant
proportional cost and are stripped after sorting.

The source's two-involution position decomposition uses a bounded number
of bulk-XOR calls, giving

\[
T_{\rm positions}(k,V)
\le C V\sqrt{k+1}H(k)(1+\log k)+\operatorname{poly}(k).
\]

Controlled small blocks use O(log k) batches and O(log k) Beneš stages,
with one guarded flip batch per stage. Hence

\[
T_{\rm blocks}(k,V)
\le C V\sqrt{k+1}H(k)(1+\log k)^3+\operatorname{poly}(k). \tag{OT3}
\]

Their space is `C VH(k)+poly(k)`; stages/batches reuse regions rather
than multiplying H at each stage. Source CRT tables have O(log k) bits
with fixed width constant. Short-transform blocks use at most seven axes,
each with at most `20 ceil(log_2 k)` bits, hence at most `2^140 k^140`
table entries. Trial division, rotations, switch schedules and phase
preparation have absolute fixed polynomial degrees. Numerical column lists
are polynomial in local m and hence polynomial k with an absolute degree.

This also supplies the routing wrappers inside OT2. Proof order is
interchange, routing, then numerical Walsh: there is no mutual recurrence.

## OT3. Exact integer assembly

For v-bit inputs retain
`b_digit=ceil(log_2 v)`, `h=ceil(v/b_digit)`,
`k=ceil(log_2(4h))`, `N=2^k`. Then `Nk=Theta(v)` and
`k=Theta(1+log v)` with absolute constants for large v. Keep the source
short prime axes. Their tested coprimality/product-size conditions provide
the convolution length; their existence above one absolute prime-gap cutoff
does not depend on local arity. Failed initial shapes use exact fallback.

CRT controls occupy at most `k/2+O(log k)` bits, so OT3 applies with
a fixed positive free fraction at every one of O(log k) depths. Each
synchronized short Fourier transform has O(log k) unitary layers.
Permutation layers use OT3, selected-bit Walsh uses OT2, and phase streams
use the source prefix-tree algorithm. Phase and coordinatewise products
retain the fixed short O(k log k) multiplier with reused marked scratch.
Borrowed occupied coordinates are restored in the source ideal schedule.

The variable Walsh logarithmic gain is k^o(1), and its event count is
polynomial k. One absolute multiple of k bits meets the fixed error budget
at every layer. Retain the actual computed gain/event-count guard before
choosing that format; it eventually passes, and a failed guard selects a
correct direct branch. Other phase and square-root arithmetic uses the
same absolute precision. The source norm/error margins put every desired
convolution coefficient within 1/2 of its exact integer. Rounding and exact
carries recover the full product. No finite-field scalar replaces a
numerical rational coefficient.

Absorb fixed powers of log k into H. With `L(v)=1+log_2 v`, the digit
multiplier has

\[
\tau(v)\le C v\sqrt{L(v)}2^{C\Phi(\log_2 L(v))},\qquad
S(v)\le C v2^{C\Phi(\log_2 L(v))},                    \tag{OT4}
\]

plus the charged sublinear preparation below. Successive layers reuse the
same regions; space is their maximum, not a product or sum over layers.

## OT4. Preparation remains sublinear in digit length

Optional expanded interchanger validation at width U can cost
`2^(U^eta) poly(log(2V))`, for one fixed eta<1. At U of order k,
this is not necessarily `2^(k^o(1))`. Keep the combined honest bound
`2^(O(k^eta'))` for a fixed `eta<eta'<1`; it absorbs all polynomial
factors and the slower Walsh family's `2^(k^o(1))` construction.

There are polynomially many numerical node types: along the width chain,
`sum log m_i=O(log k)`, and local branch lists are polynomial m_i.
Alternatively prepare plans for every integer interchanger/Walsh width up
to a fixed multiple of k. There are O(k) widths. Each interchanger keeps
its common field and deterministic descendant chain. Extra unused widths
add only a polynomial factor; all retained descriptions are compact.
Sequential plan lookup at a call boundary is additive polynomial work,
not an expanded archive scan per record.

Total optional construction/validation is consequently at most
`2^(O(k^eta'))=v^o(1)`, including its visited cells. Discarded archives
are still charged. Compact data and counters fit the same bound. Because
an interchange has two complete active fields, its own construction may
instead be absorbed directly into OT1. Either accounting gives OT4 after
an eventual fixed threshold.

## OT5. One common-space wrapper

Put `x=log_2 L(n)`. Choose h by bit lengths and integer cube-root
comparison so that

\[
h=\Theta((x+1)^{2/3}(\log_2(x+2))^{1/3}).
\]

For example let y=x+O(1) be an integer from successive bit lengths,
`ell=ceil(log_2(y+2))`, and take the least h with
`h^3>=(y+1)^2 ell`. Fix sufficiently large absolute integers C4,C5
and put `r=2^(C4 h+C5)`, `v=ceil(n/r)`. Guard `r<=n`, using exact
fallback otherwise. This is finite integer arithmetic, not an uncharged
real optimizer.

Preserve inputs and mark a fixed number of O(n)-length regions. Allow
construction/preflight at most n/16 actual steps and visited cells. Reuse
the same prepared shape for every v-bit chunk product. The diagonal
positional wrapper performs r^2 products, accumulates them exactly, and
has O(nr) movement/carry cost. Give the candidate one fixed O(n) visited
allowance and a quadratic actual-step cap. Abort before a forbidden head
move; clear visited scratch and use exact schoolbook on any cap/guard
failure. All clock, cleanup and head-return work is charged.

Eventually `log r=O(Phi(x))=o(x)` and
`log v=log n-O(Phi(x))`. The OT4 space coefficient is
`2^(O(Phi(x)))`; choosing C4,C5 large enough makes core space at most
n/4. Construction `2^(O(L(n)^eta'))` is n^o(1) and fits its n/16
cap. Reused input, output, assembly and clock buffers add only a fixed
multiple of n. The marked regions therefore bound the union of visited
cells, including construction and failed attempts.

Since `r^2v<=2rn` eventually, successful time is at most

\[
n r\sqrt{L(n)}2^{C\Phi(x)}+O(nr)+n^{o(1)}
\le n\sqrt{L(n)}2^{C'\Phi(x)}.                        \tag{OT5}
\]

This is n^(1+o(1)), so the quadratic cap eventually does not abort.
Shape and precision guards eventually pass. Exact fallback covers the
remaining finite range. Thus OT1/OT2 and their local suppliers imply one
exact fixed-tape multiplier with

\[
T(n)=O\!\left(n\sqrt{L(n)}
 2^{O(x^{2/3}(\log_2(x+2))^{1/3})}\right),\qquad
\operatorname{visited}(n)=O(n).
\]

This is a mathematical composition from V7/V8/V17, not a full execution,
formal proof, human refereeing, practical-cutoff calculation, or claim of
the exact square-root endpoint. Credits: @CubeJerry, the pinned OpenAI
source and predecessors, E002 component authors, and substantial ChatGPT
multi-agent assistance.
