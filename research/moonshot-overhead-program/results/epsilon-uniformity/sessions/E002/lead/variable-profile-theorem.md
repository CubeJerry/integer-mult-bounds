# A complete variable-parameter overhead construction

Status: **admitted complete written unconditional algorithm/profile construction**.
The admission record ADMISSION-V.md identifies the independently reviewed
snapshots and scope. The mathematical proof below is unchanged from the
accepted ccad2873 snapshot; only this status paragraph has changed.

Let L(n)=1+log_2 n, x=log_2 L(n), and
Phi(y)=(y+1)^(2/3)(log_2(y+2))^(1/3). All logarithms below are binary.
The source pin is OpenAI math
3344da59991ed94f9ba711217b29c1d760badfa6. The source model, input/output
conventions, and prior component admissions are those of Theorem P in this
directory. The proposed strengthening is

    T(n)=O(n sqrt(L(n)) 2^{C Phi(x)}),
    cells ever visited=O(n),                              (V*)

for one fixed exact deterministic finite-alphabet multitape machine. C and
the space constant are absolute. In particular every fixed beta>2/3 gives
`T(n)=n sqrt(L(n)) 2^{O(x^beta)}`. The logarithmic factor in Phi is retained;
no log-free beta=2/3, polynomial-x, or constant-overhead endpoint follows.

## 1. Proof order and complete suppliers

This document composes the following arguments, with their physical
interfaces retained. The compact fixed-template primitives are already
part of the admitted P construction; the variable scheduling, space and
outer substitution below require their own reviews.

1. Route B `composite-radix-padding.md` supplies an actual integer-selected
   compatible address radix with near-unit initial padding, together with
   A's and C's independent reviews and A's exact finite replay.
2. Route B `variable-interchanger-space.md` gives one root coefficient
   field, metadata grouping, endpoint incidence storage, and the actual
   depth-first visited-region bound.
3. Route B `variable-arity-transfer.md`, V1--V8, gives exact interchange
   with changing local arity and an explicit time recurrence.
4. A's `VARIABLE-OUTER-SUBSTITUTION.md`, Sections 1--3, and C's
   `variable-arity-outer-transfer.md`, OT1--OT2, prove the guarded routing
   contracts from that completed interchange. No numerical transform is
   assumed while proving the interchanger.
5. Route B's V9--V17, with its independently established polynomial
   rational coefficient and precision supplier, gives numerical Walsh.
6. The remaining sections of both independent outer-transfer notes derive
   exact integer multiplication and one common linear visited-cell cap.

The order is exact interchange, source routing wrappers, numerical Walsh,
then outer integer multiplication. The numerical routine does not enter
its own address-movement proof. The two different arity schedules below
are intentional and use different coefficient domains: exact interchange
uses a characteristic-two field, and numerical Walsh uses its rational
normalized binary template.

## 2. Exact interchange with one field and changing radix

Choose all finite compiler degrees first. Fix an integer M sufficiently
large that gamma=1/M makes every constructor exponent and every local
polynomial-in-m toll subcritical; in particular gamma K<1/4 for the
common enlarged degree K. At active width u use the actual odd integer

    m=2 floor(floor(u^(1/M))/2)+1.

An integer M-th root is obtained by comparisons. Choose the label distance
within an absolute factor of `(log m/log log m)^(1/3)`, restricting to the
source's power-of-two choices. The accepted geometry gives

    D_m(1+lambda_m)<=2^{C Phi(log m)},
    m r_m/N_m<=1,    m<=N_m<=m^5.

The complete finite call mass, including the enlarged predictor window,
all reserve calls, leading padding and binary child conversion, is at most
`C sqrt(m) 2^{C Phi(log m)}`. These are the actual source call lists; a
scalar arithmetic count is not substituted for the physical invoice.

At root width U construct one even-power-of-two-degree field E of degree
s=O(log(U+2)), large enough for every descendant check set. Find a root
of `omega^2+omega+1` explicitly, and retain it. Embed original bits into
s-bit E records once. Internal children keep precisely that representation.
The initial s factor fits the final overhead. No repeated field extension
is charged to, or concealed inside, a child recurrence.

For each width the compatible radix b and digit count e are selected by
integer root and division operations. They obey the proved near-unit
padding bound. With reserve dimension a=D_m-2, the child digit count
`f=floor((e-1)/(m+2a))` yields binary child width v satisfying

    u/(4m)<=v<=u/m+2.

The lower bound is guarded explicitly. Two raw child fields are padded to
complete binary ranges with less than fourfold total volume. That factor
is in the call invoice at every depth. A b-valued digit is moved by
ordinary binary splitting and merging at cost O(V log b), with constant
space; no polynomial dependence on numeric b is introduced.

The compact processors give local time `C m^K s^K V`. Above guarded
base cases, `v<=u^(1-gamma/2)`. Dividing the full recurrence by sqrt(u+1)
gives a local cost at most a fixed polynomial in s and a recursive factor
at most `2^{C Phi(log(u+2))}`. The logarithmic widths decrease geometrically;
therefore their Phi values have sum at most `C Phi(log(U+2))`. The terminal
direct bit moves, one-time field embedding and depth contribute fixed
powers of log(U+2). This proves

    Time_I(U,V0)<=V0 sqrt(U+1) 2^{C Phi(log(U+2))}.

Here V0 is original binary volume, and all head movement and encoding costs
are included. Optional expanded validation over the deterministic width
chain is at most `2^{U^eta} poly(log(2V0))` for fixed eta<1. The two complete
U-bit fields give `V0>=2^(2U)`, which absorbs that additive bill.

## 3. The refined visited-space bound

A generic polynomial-in-m workspace bound would spoil this argument.
The refined construction instead separates endpoint incidence storage from
ordinary executable metadata.

A complete spatial module row is exponentially longer than its
polynomial-size header under the guard `u>=m^K`. Rational affine runs
have target width Omega(u/m), so even a coefficient of polynomial(m)
bit height leaves long enough complete runs to amortize every header.
Stable row sorting and serialized monomial terms use a constant number
of complete-volume arrays. The inverse affine operation reverses the
short-coefficient map; it does not charge the large modular inverse as a
fresh coefficient.

Finite spectral roles are moved to the fast coordinate by O(log m)
ordinary bit moves. Each grouped block contains B or 32B field symbols,
with B>=2m+1, so one m-entry ternary comparison mask fits the existing
payload. A single reused polynomial-size buffer computes its repair
matrix. Original, output, mask and accumulator arrays have constant total
volume. Every label and grouping header is removed before a paid child.

All prepared endpoint copies and their destination accumulators occupy
`O((1+lambda_m)V)`. All m r_m low-rank vectors together occupy at most
V by the rank guard. This retains the source sharing of endpoint changes
across queries. Serializing queries by recomputing their endpoints would
change the time invoice and is not used.

At binary entry to a spatial node, count both its initial radix padding
and its child's two-field binary padding. Grouped main children then have
fraction at most `16/N_m<=1/4` after enforcing N_m>=64. Finite repair has
its 1/16 contraction inside the current padded layout. Reserve children
can have eightfold entry-volume inflation; the source clears the main
arrays and retains only descriptors before these calls. The spatial depth
is O(log log(U+4)), so even 8^depth is a fixed power of log(U+4).
Every local endpoint coefficient is at most the monotone root envelope
`2^{C Phi(log(U+2))}`. Summing parked arrays, field embedding and compact
plans thus gives

    Space_I(U,V0)<=V0 2^{C Phi(log(U+2))}.

This estimate bounds the union of visited cells: sibling calls, sequential
terms and separate endpoint operations reuse marked work intervals. The
direct base at `u<K log(s+2)` has constant-volume workspace and only a
polylogarithmic root-time coefficient.

## 4. A different schedule for numerical Walsh

The numerical transform calls the completed interchanger for its address
changes. Its local arity therefore cannot be u^gamma without introducing
a fixed power loss in that address bill.

At numerical active width a use integer y=ceil(log(a+2)),
ell=ceil(log(y+2)), the largest h with h^3<=y^2 ell, and m=2^h+1.
Thus log m=Theta(Phi(y)) and m=a^o(1). The rational template has
A=Theta(m), power-of-two batch W<=m^C, and

    sigma/W <= C sqrt(m) 2^{C sqrt(log(m+2) log log(m+4))}.

Choose f as the largest even integer at most a/A. Transform Af bits by
the template and the fewer than 2A remaining even bits by direct
four-point butterflies. A single remaining odd bit uses one direct
normalized butterfly. Logarithmic child widths satisfy
`y_child<=y-c Phi(y)` above a fixed threshold.

The product of all batch divisors on a numerical width chain is at most
`(a+2)^C`, since `sum log m_i=O(log(a+2))` telescopes from
`f_i<=a_i/(2m_i)`. Those divisors are powers of two. The source's
q=2^(k-a) spectator rows therefore divide exactly by the whole product
above a fixed threshold. An integer divisibility test is retained.
There is no independent factor-two padding charge at every depth.

The selected-bit gather and its inverse occur once at the layer root.
Every internal child is already a contiguous f-bit active slot. Local
column exchanges and guarded additions use interchanger fields of width
at most a, with all other ranges as spectators. The local bill really is

    V m^K sqrt(a+1) 2^{C Phi(log(a+2))} (1+log(k+2))^K,

and the local visited-space coefficient is
`m^K 2^{C Phi(log(a+2))}`. This includes scalar generation and its
application to Theta(k)-bit numerical records. A small coefficient is not
charged as a constant-time operation on a long tape word.

After normalization by V sqrt(a+1), retain the one common logarithmic
factor in k and set Psi(y)=(y+1)^(1/3)(log(y+2))^(2/3). The recurrence is

    F(y)<=2^{C2 Phi(y)}+2^{C3 Psi(y)} F(y-c Phi(y)).

For large y, differentiation on [y-c Phi(y),y] gives
`Phi(y)-Phi(y-c Phi(y))>=c' Psi(y)`. Choosing B>C2 and Bc'>C3
makes substitution of `F(y)<=2^{B Phi(y)}` a strict inductive majorant;
both normalized terms sum to less than one above an enlarged finite base.
Integer rounding is covered by decreasing c and enlarging that base.
This proves the numerical time bound, including its additive local term.

The logarithmic intermediate norm gain along a path is at most
`O(log k) 2^{C Phi(log(k+2))}=k^o(1)`. The product of polynomial-m
branch counts is polynomial k by the same telescoping identity. The
source common-ancestor error argument therefore needs only an absolute
O(k)-bit signed fixed-point format for its fixed input/error allowances.
The preflight computes upper bounds for both gains and event counts and
tests their allowance against k. A failed test chooses the independently
correct direct normalized Walsh branch. Thus precision is not chosen by
an unknown asymptotic cutoff.

Numerical child volume is exactly V/W, with W>=2. Parked arrays sum
geometrically under the root envelope, and sibling/stage work intervals
are reused. Consequently the complete selected-bit layer, including the
root gather and return, has

    Time_W<=V sqrt(k+1) 2^{C Phi(log(k+2))},
    Space_W<=V 2^{C Phi(log(k+2))}.

Fixed powers of log k have been absorbed by increasing C. The numerical
boundary is a completed unitary transform with the source absolute error
budget. Its internal amplification is not charged again as the norm of a
completed outer layer.

## 5. Outer integer correctness and preparation

Both independent outer-transfer proofs substitute the preceding bounds in
the actual guarded-XOR, position-permutation and controlled-block
operations. They do not insert a variable rho into a fixed-rho theorem.
The guard width remains an absolute multiple of log k because the
controls and exceptions have a fixed polynomial-k degree. Small target
fields use direct bit moves. Complete fibres amortize offset work, and
exceptional O(k)-bit tags fit the Theta(k)-bit numerical records.

For v-bit integers the source digit parameters have N=2^k,
Nk=Theta(v), and k=Theta(1+log v). Its short CRT primes, fixed free
control fraction, synchronized occupied-neighbor identities and tested
prime-shape cutoff are unchanged. The compatible composite address radix
above is a separate object; no rank assertion over a composite ring or
replacement of the outer CRT primes is inferred.

Routing adds only fixed powers of log k. Phase streams and coordinatewise
products retain the source fixed O(k log k) short multiplier. The finite
sequence of completed unitary layers, their absolute precision margins,
and the source final rounding and carry argument recover the exact full
2v-bit product. All borrowed occupied data are restored.

Walsh-only optional finite preparation is `2^{k^o(1)}`. Exact interchange
may instead have `2^{k^eta}` preparation for one fixed eta<1. The honest
combined bound, including polynomially many invocations or precomputed
widths, is `2^{k^eta'}` for a fixed eta<eta'<1 above a fixed cutoff.
The latter term must not be renamed `2^{k^o(1)}`. Both its time and
visited workspace are sublinear in v. Compact executable plans are
retained and any expanded validation archives are discarded after charging
their construction and erasure.

A concrete preflight can prepare every integer interchange or numerical
width up to a fixed multiple of k. Each entry contains its compact chain
or an explicit direct base branch. Charged sequential lookup occurs only at external numerical/address-wrapper
invocation boundaries, whose total count is polynomial k. Internal spatial
descendants retain their root invocation's local deterministic width chain
and current compact descriptor. They do not scan the global cache at each
small child. Local descriptor access/copying is paid by that guarded
node's payload; direct bases use only the opaque record/range descriptor.
No global lookup occurs once per input record. All equal-width chunk
products reuse these plans. The resulting digit machine has

    tau(v)<=v sqrt(L(v)) 2^{C Phi(log L(v))},
    visited(v)<=v 2^{C Phi(log L(v))},

including the absorbed additive preparation above its tested guards.

## 6. One fixed common-cap machine

Choose integer y=x+O(1) from successive input-length bit lengths and
ell=ceil(log(y+2)). The least h with `h^3>=(y+1)^2 ell` is
Theta(Phi(x)) and is computed by integer comparisons. Fix sufficiently
large absolute integers C4,C5, set `r=2^(C4 h+C5)`, and take
`v=ceil(n/r)`. If r>n use exact schoolbook. Otherwise retain the original
inputs and mark one fixed collection of linear-size tape regions.

Give preflight at most n/16 actual steps and visited cells. Give the
candidate one fixed O(n) visited allowance and a quadratic actual-step
cap. Stop before any offending head move, clear scratch and invoke exact
schoolbook on a failed guard or cap. Clock, cleanup, head returns, input,
output, descriptors and accumulators are all charged within these regions.
The r^2 exact chunk products use the source positional assembly with
O(nr) movement and carry work; sibling products reuse their work areas.

Eventually `log r=O(Phi(x))=o(x)` and
`log v=log n-O(Phi(x))`. Choose C4,C5 larger than the proved space
coefficient: the core then visits at most n/4 cells. The combined setup
`2^{L(n)^eta'}` is n^o(1) and fits the n/16 cap. All actual shape,
precision and compatibility guards eventually pass. Since
`r^2 v<=2rn`, total successful time is

    n r sqrt(L(n)) 2^{C Phi(x)} + O(nr) + n^o(1)
       <= n sqrt(L(n)) 2^{C' Phi(x)}.

This is n^(1+o(1)), so the quadratic cap eventually does not abort.
The finite remaining lengths use a bounded attempt followed by exact
schoolbook. Increasing the absolute bound over that finite range proves
V* for all positive lengths. The fixed marked regions bound all cells
ever visited, including setup, abandoned attempts and fallback. No
unbounded compiler, nonuniform choice of index, or free minimization
is part of this machine.

## 7. Review and evidentiary scope

This is a composition of mathematical algorithm descriptions in the pinned
model. It is not a full executed multiplier, formal refinement, independent
human refereeing, evaluated practical cutoff or literature-priority claim.
The finite exact grouped-role replay in `grouped-role-replay/` passed
108 layouts and 56,889 repaired vectors, with padding, mask-budget,
occupied-zero and wrong-order controls. The earlier independent component
replays and source audits remain inputs; finite tests do not establish an
asymptotic theorem by themselves.

The companion `variable-invoice-barrier.md` is not used as a premise here.
It lower-bounds only a specified product of sufficient literal majorants.
It must not be reported as an algorithmic lower bound or as evidence
against the exact square-root endpoint.

Credits: Jerry Chen (@CubeJerry), the pinned OpenAI manuscripts and cited
prior work, earlier programme constructions, E002 Routes A/B/C and lead,
concurrent S003's separately admitted same-scale predecessor, and
substantial ChatGPT multi-agent mathematical assistance.
