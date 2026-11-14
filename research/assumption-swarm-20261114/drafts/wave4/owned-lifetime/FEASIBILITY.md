# Physical protocol for the actual owned1526 lifetime: bounded feasibility

Status at 2026-11-14 04:12 UTC: exact source and ABI comparison completed;
no new graph has been implemented or verified. Base is canonical main
`e54523517d0f03e58352e647c403a5af3e525a57`. No new kappa.

## Exact scope and novelty

The useful delta is the same physical owner across zero production, every
one of its six scientific contacts, retention across unrelated events and
dirty full-field erasure. Existing #7564 section 6 supplies only a primitive
compatibility ledger and explicitly leaves this lifetime and format producer
open. #7567 supplies signed contacts on already live typed fields. Published
B2 now supplies the literal zero producer from an OLD23 context/source.

A complete whole-source execution remains unavailable: external current
donors, receiver installation, and all intervening events must remain explicit
continuations with their own time, history and source correctness contracts.
The proposed graph is a resumable, locally implemented lifetime protocol,
not an assertion that a projected eight-event list executes the 9,582-event
source interval.

## Pinned inputs

| Input | Exact commit | Relevant path |
|---|---|---|
| B2 typed zero from OLD23 | `1ce8a1622b89f925a81815f8158eb8fc95977868` | `research/old-source-owned-zero/zero.py`, proof and inputs |
| B1 typed initializer | `28fc921807f867302b2f43cb0696645f18094307` | `research/selected-owned-gamma-init` |
| Signed ADD/SUB, #7567 | `dcd6352db7e5a5353498203c0c2699334019ba56` | `research/source-bound-signed-home-add/add.py` |
| Actual rank-two MOVE28141, #7564 | `caba500cefa8d1745a187e60198a97b2647e2e90` | `research/literal-owned-rank-two-move/implementation/{rank2.py,adapter.py,PROOF.md,SOURCES.json}` |
| Original fixed B1 graph | `b4fcc9d64971fdabd0b1d82cfb749d8aac920437` | `research/compiler-permanent-home-dispatch/tape_graph.py` |
| Selected source word | `172f4535ce8dcff79f626410af845f757c1563be` | `research/literal-native-quadratic-phase/reference/selected-native.json.gz` |

The archive is 350,722 bytes, SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Canonical word SHA256 is
`91429a6b96729292a8764836e00c87a6f7cd3b76f05159033f4867f69a98d097`.
It has 71,261 events, 1,480 public roles, and the eight owner1526 contacts
below. The archive was re-extracted locally, not inferred from a PR title.

## Chronology that must survive composition

| Event | Literal record | Required contact state |
|---:|---|---|
|28037|`INIT 1526 601`|An inactive granted owner becomes a typed zero in frame601.|
|28041|`ADD 1526 1349 -1 601`|1349's current frame is601; its MOVE28039 from3 occurred after INIT.|
|28129|`ADD 1526 728 -1 601`|728 includes its intervening ADD28127 from1500.|
|28135|`ADD 1526 729 -1 601`|729 includes its intervening ADD28133 from1500.|
|28139|`ADD 1526 730 -1 601`|730 includes its intervening ADD28137 from1500.|
|28141|`MOVE 1526 601 470 true`|Actual fixed rank-two quotient; all numerical prefixes admitted.|
|28159|`ADD 1515 1526 +1 470`|1515 has been initialized at28153 in frame470.|
|37618|`CLEAR 1526 470`|Erase the actual dirty packet; do not assert zero before CLEAR.|

Frames are3=`[]`,601=`[137]`,470=`[75,137,265]`. Following28159,
1515 is scaled by-1/4 at28161 and receives1/4 of402 at28165. These are
external continuation work and cannot disappear into the lifetime projection.
No event in any intervening interval touches1526; checking the full projection
proves that fact, not numerical correctness of the remaining source program.

## Exact ABI match and physical layout seam

All services use positive canonical Gamma6 `(f,r,P,S,w,cutoff)`, packed
lexicographic `[P] x [2^f]^9 x [S]`, with r Gaussian coefficients per address,
real then imaginary and signed MSB-first w-bit components. Write

`V=2PSr2^(9f)w`, `E_gamma=|Gamma6|`, `F=V+E_gamma`.

B2 derives `P=C_rows2^u`, `S=2^(a-u-9f)` from OLD23, with
`V_old=C_rows2^a6r(w+1)` and `V_old/V=3(w+1)/w>3`. It returns
`^ h 0^V | $` with HOME head on its permanent origin. OLD/CONTEXT and40
private heads return to the first cell after their origins. Complete old
component boundaries and width inference are checked. The other services
accept the same binary h/DATA but require their working heads at `^`.

The fixed alphabet renaming is exact:

| B2 hardware | Other services |
|---:|---|
|0|`0`|
|1|`1`|
|2|`^`|
|3|`|`|
|4|`$`|
|6|`_`|

It renames graph labels, never rewrites existing public cells. Physical BASE5
is opaque and unused. After B2, forty paid one-cell moves bring the private
heads to `^`; the reverse moves can restore the B2 return convention at final
retirement. Private bodies are blank, permitting reuse. Rank-two adapter
native origins remain offset2, so their temporary native guard at offset1
cannot overwrite permanent `^` at0.

The real layout seam is that B2 constructs a single HOME ending`|$`, whereas
the supplied B1 wrapper expects one multi-field bank. The prospective fix is
one dedicated permanent HOME1526 (B2 physical tape2), plus a separate fixed
five-field external bank for1349,728,729,730,1515. A new literal gather/scatter
adaptor scans those fields in fixed order and uses the existing two work
ports. It must keep inactive receiver1515's supplied same-F reservation;
only its external INIT continuation makes it live. The protocol does not
claim ownership acquisition or free reservation.

B2 ports0..42 suffice for old input, context, owned HOME and reused service
work; one new external bank port43 gives a prospective44-tape program.
Map the existing service ports1..34 to physical3..36. Existing rank-two
native HEADER/DATA/private ports and ADD unary guides then reuse disjoint
blank working windows after each successful return. This count is a design
feasibility result; exact generated states and all interfaces must still be
checked before it becomes an implementation claim.

## Numerical and continuation contracts

Each ADD contact requires identical geometry/header, current frame, common
quantum and signed final component range. Header equality alone does not
verify current frame or quantum. Actual exterior coefficients remain-1/-1/
-1/-1/+1 for every f. Rank-two MOVE requires `2f<=cutoff`, both complete
phase actions to fit, and every one of its actual2f C-prefix outputs to be
integral and signed-range bounded. No endpoint-only shortcut is admissible.

One simple sufficient, deliberately stronger numerical domain is: each of
the four actual donor vectors at its contact has components divisible by
`2^f` and bounded by M; the supplied receiver is bounded by M; and
`(1+4*2^f)M <= 2^(w-1)-1`. Partial negative sums are bounded by4M;
the right monomial preserves their divisibility and magnitude; each central
prefix has denominator at most2^f and component amplification at most2^f;
the final consumer is bounded by the displayed reserve. This uses #7564's
credited prefix theorem. A sharper correlated selected common-root domain
can be a separate caller proof and is not required for local feasibility.

At each chronological gap the protocol exports one fixed continuation port
and resumes only at its corresponding fixed return port. The extension must
preserve owner1526, its HOME/head, the blank required scratch and old input,
provide correct current donor/receiver values in their actual homes, and
pay its complete time `tau_j` and historical increment `eta_j`. A literal
composition theorem can use these ports without providing those extensions.
Any finite demonstration that uses a simpler literal extension must identify
it as a protocol fixture, never the full selected source execution. No host
write of a nonzero donor at a pause counts as a literal extension.

## Optimistic complete local budget before implementation

The credited primitive bounds are:

* B2 INIT: `2^20(V_old+E_old+1)`; history `64(V_old+E_old+3)`.
* Five scalar contacts: `5*4096(F+1)`; history `5*8(F+2)`.
* Rank-two packed adapter: `128(F+1)+2^24(fV+E_gamma+1)`;
  history `1088(F+1)`.
* B2 full CLEAR: `16(F+1)`; original owner/history retained.
* Head-convention joins:80 unit moves for40 private heads, plus fixed jumps.

A conservative pre-implementation reserve is `8192(F+1)` for all six
transactions' fixed-five-bank delivery, source preservation, work-copy
retirement and complete head returns. A simple scan argument should make
this ample; it is not yet a checked bound for emitted code. Thus the target
whole local bill is

`T_local <= 2^20(V_old+E_old+1) + 2^24(fV+E_gamma+1) + 32768(F+1)+128`.

Add `sum_j tau_j` for the actual external continuations and all caller
source/window production. Target historical increment:

`DeltaK_local <=64(V_old+E_old+3)+2048(F+2)`.

Add the actual external bank/source entry history and `sum_j eta_j`;
erasure never refunds prior backing. There is no nonleaf accelerated tariff
or multiplication exponent improvement. At a fixed admitted cutoff2f<=q,
the local lifetime work is `O_q(V_old+E_old+1)`, with a separately charged
possibly very long encoded cutoff.

## Verification, stopping rule and overlap limits

Before claiming the protocol implemented: authenticate every retained source;
check every graph-label/port translation; prove two-arena delivery by scans;
execute one full nonzero admitted packet with literal continuations and no
host mutation after start; verify all eight event boundaries, immutable HOME
identity, source preservation, all heads/private bodies, final full erase,
opaque exteriors and historical unions. The oracle must use unlowered source
frame action and ordinary exact integers outside the runtime.

Controls should reject a short inactive target, alias, unequal header,
`f<=cutoff<2f`, true signed overflow, incorrect event resume, and changed
absolute phase. A no-C or wrong fixed sign mutation must be detected by
independent output checks. The continuation contract must reject resuming
the first SUB with1349 still in frame3. Failure cleanup remains outside scope.

Stop before implementation if current-source overlap duplicates the same
physical lifetime, or if parent requires a complete actual intervening-source
implementation rather than the explicit continuation theorem. In the latter
case the exact missing object is a chronological physical producer and
same-owner return for the gap segments, especially28039's nonzero frame3-to-
601 transformation and receiver INIT28153; these cannot be replaced by host
packet injection.

Live #7564/#7567 heads and full relevant proofs were read. #7564 already
credits the separate six-contact ledger; B2 removes only its zero-producer
gap. Targeted GitHub searches for quoted bank1526/28141/formatted-zero gave
no results even though known #7564 contains28141, so search index silence
does not establish novelty. Parent's current PR/claim sweep must supplement
that bounded, explicitly incomplete search. Fixed-recipe closure #7559,
all-rank semantics #7561 and concurrent S011 source work are excluded.

Prepared for @CubeJerry with substantial OpenAI assistance. Predecessor
authors retain their credit. This feasibility checkpoint is unverified
research planning, not a publication package or proved new theorem.

Independent feasibility cross-check by the `owned_recursion` agent found no
B2 scratch/CLEAR mismatch: all40 private bodies are blank at first-body
heads, the left shift reaches the existing permanent guards, native offset1
guards stay separate, and B2 CLEAR accepts arbitrary dirty F-bit bodies with
unchanged`|$`. The reviewer requires the reverse head shifts for a final B2
return convention and explicit external-bank entry/history accounting.
This was an ABI review only; no prospective new graph was checked or run.
