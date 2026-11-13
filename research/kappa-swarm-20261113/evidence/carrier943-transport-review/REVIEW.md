# Independent review: radius-three transport implication and per-call price

Reviewed `root-public-carrier943-union/PROOF.md`, its frozen RESULT, and the
relevant graph/rank definitions in `worker-a/public-carrier943/import_gate.py`.
I did not rerun the native source census. The review is complementary to the
polynomial-dual replay.

## Finding

The transport implication and price split are sound **for a fixed
instruction/dataflow graph** in which (i) all ordinary scalar processing is
coframed, (ii) every information-carrying cross-frame edge is a separately
charged whole native job, (iii) no sidecar data are piggybacked on an existing
paid carrier or MOVE payload, and (iv) the sidecar service is billed separately
for each of the 17 invocations. The current proof should state these premises
more sharply. Without the fixed-dataflow/control-channel condition, the
common-separator conclusion does not follow from row support alone.

## Graph and rank argument

For each data source that influences the destination B output, choose a
source-to-output path in the fixed dependency graph. For successive frame
changes T_1,...,T_k on that path, Clifford Fourier rank is subadditive under
composition: `r(T_k...T_1) <= sum r(T_i)`. This follows from the support
bound for matrix products; cancellations only reduce support. Monomial/rank-0
steps do not increase the product rank. Co-framed additions, copies, scalar
multiplications, and other fixed local dataflow operations do not change the
frame endpoint. Thus any source used by a network with total new positive
integer rank at most 3 has actual endpoint distance at most 3, even if the
network branches, shares scratch, or uses newly introduced intermediate
frames. Each path's rank sum is bounded by the rank sum of the whole network.

Rank 0 needs an explicit sentence: for these canonical Clifford frame maps,
zero Fourier rank is monomial and corresponds to the same frame span. The
source enumeration pools by exact span key; `bankB = banks[spans[189]]` thus
includes every same-span/rank-0 alias, not only literal frame ID 189. Its
reported two rows are the complete pooled B bank. The 67 nonzero radius-one,
-two, and three source spans are enumerated, with actual Clifford B-rank
checked for each. The proof should say this radius-zero alias coverage
explicitly so it cannot be read as checking only the literal destination ID.

The dual has `R_i*x=delta_i`, `z*x=0`, and `u*x=0`; under
`v(alpha)=e885+e1459-alpha*x`, all 294 pooled rows after the injection tilt
vanish, while target z is 1 and the promise u is 0. Therefore arbitrary
nonlinear or linear processing of values actually available in this pool
cannot recover the target. This conclusion survives fixed-graph fanout,
branching, sharing, and intermediate frames: all accessible input data at
those nodes agree on `v(alpha)` and zero.

## Required control-flow restriction

“Branch and share new scratch” must mean dataflow fanout in a fixed schedule,
or local control that cannot send information to another coframe without a
charged edge. If an unpriced input-dependent branch at a distant source can
select a destination frame, select which B constant to emit, or otherwise
change B-visible control flow, it forms a control channel that is not
represented by the row-support graph. On the separator pair, a branch testing
whether a distant value is zero can select output 0 versus a fixed output 1;
then B-visible outputs differ although every pooled scalar observation is
zero on both inputs. This example is not a full algorithm for arbitrary field
inputs, but it is enough to show that the two-input indistinguishability
argument no longer applies under an unpriced cross-frame control channel.

Accordingly the model should require a fixed instruction/dataflow schedule,
with no input-dependent routing, destination selection, event timing, or
output-label control based on data outside the receiving coframe unless that
control information itself traverses a charged path. Ordinary computation
may be arbitrary on data already coframed; an ordinary frame-changing
algorithm remains outside the model. This restriction should also be carried
into any root-family preparation corollary that invokes the same separator.

## Fixed payload, unavailable input, and scope

The prohibition on appending sidecar data to existing paid MOVE payloads is
essential. If an existing long-rank paid carrier could be reused as a free
sidecar transport, its rank is not part of the “new network” sum and the
radius-three implication fails. The changed original 943 carrier is treated
separately: all resulting strict-history observations are explicitly of form
`R_i + alpha*delta_i*z` and included in the polynomial dual. No additional
original carrier edits, old-payload injection, or use of an original paid
stream as a sidecar are covered.

Demoted initial 1459 unavailability is essential, not implied by paying its
rank-one final target. If the frame-189 initial row `e1459` is granted free,
then under `u=0` the target `z=e885+e943` is already `e1459 +
(e705+e943)` using the original event-40708 row. The separator correctly uses
the unavailable-resource premise; the claimed obstruction must keep it
prominent.

The union and rank argument cover the fixed 17-call template with a fresh
per-invocation sidecar network. They do not bound amortized setup, shared
state, or information carried from an earlier invocation into a later one. If
one network can be executed once and reused across calls, multiplying its
price by 17 is not justified; cross-call reuse requires a separate model and
invoice.

## Price check and optimistic direction

At kappa=.0038, the complete signed invoice moment is about -59.2419338844.
The rank-8 candidate credit less rank-1 target debit is about 6.93703407927
per invocation. This leaves 3.45221443901 units per invocation for all new
services. For nonnegative integer ranks and `0 <= kappa <= 1`, `f(0)=0`,
`f(r)=r^(1-kappa)` is increasing and subadditive. Hence a service network of
total positive integer rank at least 4 costs at least `f(4)`; at .0038,
`f(4)` exceeds the residual. The inherited directed invoice calculation gives
`M+17*(f(8)-f(1)-f(4)) ~= -8.95507795206`, so the arithmetic is consistent.

This is an optimistic upper budget: ordinary computation, storage, and
restoration of already available observations are waived. That waiver cannot
include an uncharged cross-frame transport or information-bearing control
channel. Any target restoration that uses a new cross-frame edge must be
included in the network sum. The proof must retain all original target
requirements; changed final values from the 943 injection are not new
productive credits. No physical supplier or kappa improvement follows.

## Recommended proof edit

Replace the unrestricted “branch and share” wording by: “The new sidecar is a
fixed dataflow graph per invocation. Arbitrary deterministic computation and
fanout are permitted within a coframe. Any input-dependent information,
including control flow, that affects another coframe's data, route, event, or
output must cross a charged whole native edge. All cross-frame edges are
counted, and the old paid payloads are not reused.” Also state rank-zero
same-span pooling and the no-cross-call-amortization premise beside the
17-call multiplier.
