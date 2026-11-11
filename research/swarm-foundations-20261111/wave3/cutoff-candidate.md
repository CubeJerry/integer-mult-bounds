# Source-bound feasibility of generating the selected stopping cutoff

Status: proposal and written budget; not independently reviewed, no new
implementation, no publication request. The earlier selected-rank-control
package remains frozen. Prepared for @CubeJerry with OpenAI assistance.

Base: `e54523517d0f03e58352e647c403a5af3e525a57`.

## 1. Findings that change the task

The retained source already supplies both ingredients needed for an ordinary
cutoff computation: a canonical binary root descriptor containing d, and an
explicit exact rational-power comparison procedure with polynomial setup
cost. A generic integer-root algorithm would repeat existing work and should
not be packaged as a new research result.

There is also an important notation distinction in the actual selected
parameters. In `research/shared-wire-split-composition/interval_gate.py`,
`be=1-3*g` is an outer exponent. The complex stopping exponent is the separate
variable `stop=g`, as witnessed by the retained layer formulas

    internal = tau + (1-stop)*max(sig-tau,0)
    leaf = sig + stop*(1-sig).

The selected `FULL-RESULT.json` records

    claim = 363005817/100000000000
    tested = 363005817007/100000000000000
    compiler_gap = (tested-claim)/7 = 1/100000000000000.

Consequently the selected complex stopping cutoff is

    L = ceil(d^(1/Q)), Q = 100000000000000,

not ceil(d^(1-3/Q)). The batched-complex note's generic beta denotes this
stopping exponent when instantiated by the gate. No selected parameter is
changed. The previous controller theorem was parameterized by supplied L and
did not choose either exponent.

## 2. Actual input and caller pins

`upstream/build/sections/02-streams.tex`, integer-descriptor-code, specifies

    b_v = floor(log_2(v))+1,
    Gamma(v) = 0^(b_v-1) bin_(b_v)(v), |Gamma(v)|=2b_v-1.

`upstream/build/sections/05-layers.tex`, the formal simultaneous-layer
proposition, supplies the descriptor header on a tape:

    E = Gamma(p) Gamma(d) Gamma(r) Gamma(D) Gamma(P) Gamma(S)
        Gamma(K) Gamma(rho+1) Gamma(w).

It has length at most C_desc*p, with 1<=D<=d, d=Theta(p^epsilon),
epsilon<1, w>=p+2, and a nonempty complete array of logical volume
V=2*M*r*w. Thus V>=2(p+2), even without using the much stronger growing
polynomial-record lower bound. The input header is valid by the retained
interface promise, not established by this investigation.

The selected application review section 5 retains that root boundary and
processes Q0 reserved axes first. In the recursive branch the remaining
active width is e=D_total-Q0, with 1<=e<=d. In the other branch the source
already processes the layer individually. The batched-complex note gives
the row/compact reservation procedure and uses global d throughout stopping.

The existing selected controller already receives unary e. A cutoff-only
prefix can read this stream, count it into binary, and restore it; it does
not require a second external binary e input. Alternatively, a full root
prefix can consume the binary e produced by the retained reservation step.
This investigation does not implement Q0 construction, row grants, the
actual final template or the array's complete physical root producer.

At the outermost input, `08-assembly.tex` counts n from the promised string
x#y in O(n), then generates p and d internally. Its scalar setup paragraph
explicitly uses binary search and fixed integer powers for rational powers,
including d itself, and says these lengths are not advice. The selected
review changes fixed parameters and eventual thresholds while retaining this
input/setup framework. Thus d is present at the actual admitted layer call;
inventing a new caller-supplied d would be unnecessary.

## 3. Exact capped-cutoff implication

Candidate claim: from the admitted header E and the existing marked unary
root WIDTH stream of length e, construct a marked unary cutoff

    C = min(ceil(d^(1/Q)), e+1)

on a private work tape, restore the E and WIDTH inputs and their heads, and
leave the new cutoff head at its first unary symbol. Retain C through the
completed controller run, then clear it and return that head locally.

All descendant widths x satisfy 1<=x<=e. If L<=e+1 then C=L. If L>e+1,
both x<L and x<C hold for every such x. Therefore

    x < max(N,L)  iff  x < max(N,C)

for every descendant, including equality at L and the additional fixed
cutoff N. The controller's entire call shape and remainder hooks are
unchanged. This caps the new unary cutoff backing at e+1 even when the
global d is much larger than the current active width. It is an elementary
saturation fact, claimed only as a source-specific interface reduction.

Compute C by binary search with upper sentinel e+1, treating that sentinel
as accepted, and testing interior integers t by

    t^Q >= d.

The search returns the first accepted interior t, or e+1 if none exists;
these are exactly the two cases in the formula for C. The strict stopping
test is x^Q<d. Using <= instead would change perfect-power boundaries.

Power comparisons need no huge Q-fold array. Use binary exponentiation
with saturation at d+1 after each multiplication. For positive operands,

    min(min(a,d+1)*min(b,d+1),d+1) = min(a*b,d+1).

Thus the saturated exponent is exact for comparison with d, including
equality. There are O(log Q) schoolbook multiplications on O(log(d+1))-bit
operands per test. Q is fixed by the selected gate; no exponent-dependent
input advice or growing tape family is introduced.

## 4. Complete optimistic budget and physical boundary

Let h=|E| and b=ceil(log_2(d+1)). Standard fixed-tape binary arithmetic gives
the following complete bound for the proposed prefix and final retirement:

    O(h + e + (log Q)*b^3 + C)

time, with additional historical backing

    O(e+b)

beyond existing input/history K0. These are asymptotic bills for an explicitly
describable ordinary tape routine, not counts for an emitted instruction table.

The accounting is:

1. Parse Gamma(p), Gamma(d) and any needed surrounding header fields in a
   sequential prefix pass; copy d to a local register. Count the number of
   input positions traversed and rewind over that same prefix to restore the
   entry head. Charge O(h), with the header unchanged. No outer ancestor
   prefix is entered and no descriptor is rescanned for each output symbol.
2. If binary e is not already present, count the supplied unary WIDTH with
   a least-significant-end binary counter and rewind WIDTH. The retained
   elementary-counter analysis includes carry excursions and returns in
   O(e+b). This also pays the local copy used by the search.
3. Perform at most O(b) binary-search tests. A saturated power needs
   O(log Q) schoolbook multiplications; each multiplication, comparison,
   clipping, copying and head return costs O(b^2) on a fixed number of tapes.
   Intermediate products have at most 2b+O(1) bits. This gives the displayed
   O((log Q)b^3) term and O(b) reusable arithmetic backing.
4. Emit C unary symbols using a local binary countdown, then rewind the
   cutoff head. The elementary-counter bound includes all carry returns in
   O(C+b). Arithmetic tapes are erased and returned; after controller
   completion the cutoff is erased and returned in O(C). Erasure does not
   subtract previously visited cells from retained backing.

Since h=O(p), e<=d=O(p^epsilon), epsilon<1, C<=e+1 and b=O(log p), this is
O_Q(p) time after enlarging a fixed constant. The elementary inequality
(log p)^3=O(p) suffices; no superpolynomial record or new supplier rate is
needed. As V>=2(p+2), the whole root preparation/retirement costs O_Q(V).
Input access, work copies, physical returns and erasures have all been included.

For repeated layer calls, restore then reuse the same fixed work origins.
Historical allocation is bounded by the maximum prefix written, not the sum
of cutoff lengths across completed calls. For a call already inside a larger
stack, this argument uses a private local top-of-stack interval or fixed
descriptor bank with its entry extent charged; it does not permit scanning
an arbitrarily distant global origin through suspended ancestors.

## 5. Novelty screen and proposed disposition

Nearest work inspected:

- #6719, head `e4e52d6ba2c805fa78bb57778c3b7bbc064edba5`, and review #6739,
  head `d4f7d625b2a5fa71f2c9c276b9ea503c28dcee4b`: richer natural-root
  H/A/R production from supplied binary T/R_body/w and unary depth; no
  claim to produce this selected complex stopping cutoff.
- #5515, head `a3be1f66a44e1e6d7fc798b238fea8470edd0a63`: root-dependent
  historical QQ16 threshold max(73,ceil(d^(1/1000))), parking envelope and
  exact division depth. It preserves supplied root descriptors and does not
  implement this header-to-cutoff prefix. Its root-dependence theorem is not
  repeated here.
- #2310 and #2386: older BIT controller work with charged local controls
  and polynomial preparation absorption. They retain credit for that general
  method; no new polynomial-absorption principle is claimed.
- The retained 02/08 source already provides exact rational-power comparison
  and counter construction. An elementary root implementation alone is
  superseded as a proposed research objective.

Metadata searched all canonical research-directory names. Focused PR queries
included cutoff/binary, root/producer, stopping/comparison, unary/cutoff,
rational/stopping and root-dependent. `unary cutoff` returned zero;
`root-dependent` returned seven, including #5515. Broad result pages were
bounded and are not exhaustive coverage of historical diffs/unpublished work.
The parent supplied the latest recent-PR delta through #7270.

Recommended disposition: treat the arithmetic cutoff obligation as already
covered at the retained algorithmic level, with the precise selected-parameter
and capped-prefix connection above as a useful source-bound reduction. Do not
open a generic integer-root PR. If this implication passes independent review,
the remaining narrow implementation obligation is an emitted tape prefix
linked to the existing controller with the actual E/root-reservation entry
contract. This does not implement the entire selected root/payload dispatcher.

No previous frozen artifact was changed. No new kappa or full foundational
assumption discharge is claimed. All five selected assumptions remain inherited.

## 6. Verification plan before any implementation

First independently check the mapping `stop=g` versus outer `be`, the
selected exact gap, the Gamma header and the O(p)<=O(V) bill. Then test
perfect-power boundaries with small analogous fixed Q, saturation at d+1,
cap cases L>e+1, L=e+1 and L<=e, root fallback e<N, translated private origins,
arbitrary ancestor bytes, full restoration and historical tails. Mutations
must reject exponent substitution, <= at a strict boundary, failure to rewind
the borrowed header, forgotten cutoff retirement and a falsely zero setup
invoice. Finite tests cannot by themselves prove the all-input tape routine.
