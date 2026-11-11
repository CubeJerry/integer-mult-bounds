# Selector lifting on the current BIT native: exact defect and paid repair

**No new κ.** We prove a source-bound selector-lift identity, compute its
actual main-only endpoint, construct an explicit paid endpoint repair, and
show that this particular fully billed family fails the raw moment test at
κ=1/200. This does not exclude other shared cores or cheaper repairs.

Frozen source: CrocSwap/integer-mult-bounds main
e54523517d0f03e58352e647c403a5af3e525a57.
The exact source pins are in SOURCES.json. The selected certificate is unchanged.

## Selector invariant without averaging

Fix an integer m>=2 independently of the input size. Partition the source
word into 222 main fields and its public-helper/owned core. The audited
complete endpoint is E on the mains, independently of all arbitrary helper
inputs, and identity on the public helpers.
Duplicate the main fields m times, retain the core once, duplicate main-main
operations, broadcast each main<-core ADD to every copy, and let core<-main ADD
read only copy 1. Core-core operations run once. Main MOVEs and within-main
SWAPs are duplicated; core MOVEs and owned lifetimes run once. The actual source
contains no main/core SWAP. No half scalar or division by m is used.

In coordinates z=x_1 and d_i=x_i-x_1, z plus the core executes the original
word, while every d_i executes the main-only word M0. Thus if E is the desired
main endpoint, passive copy i ends at M0 x_i +(E-M0)x_1. In particular, zero
repair works iff M0=E. The relation is an exact linear invariant over F2 (and
over any field for the stated operations). All copied fields have independent
arbitrary inputs. Sharing a core is not justified merely by identifying labels.

The exact canonical BIT source has M0=I, whereas E sends each of 111 Y fields
to Y+X and preserves 111 X fields. The unrepaired lift therefore misses
111(m-1) independent Y shears. The original 659-public-field endpoint was
replayed with zero coefficient mismatches, and all 222 main-only rows equal
identity. This is a finite scalar-source statement, not a new all-column
physical admission.

## Literal paid endpoint repair

At the complete endpoint, each X field is in its full dimension-8 frame and
its corresponding Y is in a dimension-7 body frame. Copied X fields of one
port have exactly the same frame. For passive copy i and each port, allocate
owned zero Z in the X frame, add X_i and X_1 into Z, execute one paid rank-1
nested MOVE to the Y frame, add Z into Y_i, and clear Z. This supplies the
missing normalized X_i-X_1 term (minus equals plus in F2).

The repair has six literal events, one rank-1 paid job, and one owned lifetime
per port/passive copy. A single extra owned label can be reused after each
complete CLEAR. Clearing a nonzero owned value retains the canonical owned
erasure assumption; this note does not discharge it. All original source
MOVEs are charged, including public MOVEs. Every added MOVE is charged.

The checker constructs and replays this lift+repair for m=2,4,6:

|m|Public fields|Owned labels|Events|Added rank-1 calls|
|---:|---:|---:|---:|---:|
|2|881|238|57757|111|
|4|1325|238|104997|333|
|6|1769|238|152237|555|

All new public scalar endpoints and all final frames pass. No full native word
was written to disk. The source grammar and its original native realization
remain inherited; no updated physical all-width, precision or tape audit ran.

## Complete target invoice and the scoped obstruction

Let t=199/200. The current paired E-free BIT caller has complete signed moment
M2< -444. Decompose source paid jobs by physical owner: P_main is the222-main
bill and P_core the helper/owned bill; H0 is the 437-helper productive profile.
The exact root-envelope checker independently proves D=(P_core-H0)_t<88.

The new block's helper profile is H0 and paid profile is
m P_main + P_core +111(m-1) rank-1 jobs. Insert it at the 18 body stages and take
m/2 copies of the paired E-free root (even m). Root target/query/idle terms are
all retained. Its complete signed target moment is exactly

```
M_lift(m)=(m/2)M2+18(m-1)(D-111)
         < -222m-414(m-1) <0.
```

The numerical inequality is true for every integer m>=2; caller assembly uses
even m. Therefore this particular selector lift with this displayed paid
repair cannot satisfy the existing strict-moment compiler at kappa=1/200.
It does NOT prove that every shared-core construction, every repair schedule,
cross-plane batch, bus itinerary or changed computational representation fails.
No optimality of the 111-per-passive-copy repair bill is claimed.

The target root terms used are the canonical paired caller formulas:

```
T_total=18 H_m +111m H127+222m sum(j=1..9)H_(1+7j);
P_total=18 P_m +222m H1+222m sum(j=1..8)H_(7j).
```
They come from research/paired-query-only-bit/PROOF.md, including every
nonempty root target, thin query, idle and native call. Source helper and
paid histograms are independently recomputed from the frozen native.

The native has 222m+437 arbitrary public fields and 238 owned labels. Its
literal event count is 34137+23620(m-1): 22954 copied main events and 666
repair events per extra plane. Every scalar ADD, MOVE, initialization and
erasure remains in this count; all existing source charts are retained, and
the repair introduces only its specified nested rank-1 moves. A fresh finite
ordinary/tape allowance is required for every changed word; no old constant
is reused. The obstruction already holds when all additional ordinary work
is optimistically free, since its complete recursive paid moment is negative.
Charging those nonnegative costs cannot repair this failed moment gate.

## Exact verification

The standalone Node checker authenticates the compressed source SHA256,
replays all 434281 original public scalar coefficients, verifies M0=I,
constructs three finite repaired lifts, checks every actual chart at ADD and
MOVE boundaries, and compares all paid counts with the closed formula.
It certifies the two moment bounds by exact integer 200th-root
intervals at scale2^128. Adjacent integer powers certify each enclosure;
no floating-point acceptance test is used.

Run from the repository root:

```sh
node research/bit-selector-lift-price/verify.js
```

Expected marker: `PASS_BIT_SELECTOR_LIFT_PAID_REPAIR`. The saved RESULT.json
is compared exactly. The omitted-repair negative control has a positive
four-plane target moment; putting back every repair reverses the sign.
The zero-repair endpoint has 111(m-1) incorrect rows, and an unpaid same-chart
output ADD is rejected by the actual dimension-8/dimension-7 boundary.
The universal theorem follows from the written selector invariant and
counting argument; the m=2,4,6 checks do not establish an unbounded claim
by extrapolation. No all-column physical admission is inferred.

The five foundational assumptions are unchanged: native_all_columns,
owned_erasure, compiler, precision_tape, analytic_recovery. This result discharges none. Credit the retained BIT native/caller authors, DreamingOfClouds,
zxv, @CubeJerry and their source notices. The selector invariant, repair construction
and exact-root price check were developed with substantial OpenAI
assistance. Prepared for @CubeJerry. No independent human review is claimed.

## Open next question

Can an alternate shared-core word or a cheaper admissible correction produce
the required main endpoint while avoiding this particular full repair bill?
A same-chart claim must respect the actual dimension-8/dimension-7 boundary,
and any new batching, role mixing, queries, storage and erasure must be paid.
