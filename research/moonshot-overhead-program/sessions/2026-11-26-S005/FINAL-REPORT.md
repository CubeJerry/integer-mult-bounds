# S005 — two-hour moonshot report

Requested interval: 26 November 2026, 11:49:41–13:49:41 Australia/Melbourne
(00:49:41–02:49:41 UTC). Observed session timing and completion status
are recorded in [SESSION.json](SESSION.json).

**No new unconditional complete multiplication bound was obtained.**
The main gains are a complete conditional polynomial log-log transfer,
a positive Bell representation with its cost limits exposed, a different
exact CRT caller with affordable factor generation, and stronger
verification of the retained construction and source interfaces.

## Shared frontier

Set L=1+log2(n), x=log2(L), T(n)=O(n sqrt(L) H(n)), G=log2(H).
The retained complete unconditional **written** AQ/V/E003 constructions give

    H(n)=2^{O(x^(2/3)(log2(x+2))^(1/3))},
    G(x)=O(x^(2/3)(log2(x+2))^(1/3)),
    delta(n)=G/x=O((log2(x+2)/x)^(1/3)),
    visited space=O(n).

They remain written constructions with independent agent review, not
complete kernel-checked or human-refereed multiplication theorems.
Fresh scoped audits found no defect in the reconstructed arguments.
The published OpenAI source gives the uniform G=o(x) baseline; this
session does not improve the programme's unconditional rate. The prior
S004 conditional G=O(x^(2/3)) under open JR is preserved separately.

The polynomial target has H=(x+2)^C, G=O(log(x+2)),
delta=O(log(x+2)/x). The endpoint has H=O(1), G=O(1), delta=O(1/x).
Neither is obtained unconditionally. No numerical kappa is assigned,
and no lower-bound hypothesis supplies an upper-bound premise.

## Conditional transfer CT

[CT](route-b/critical-template-transfer.md), with
[independent review](route-c/REVIEW-CRITICAL-TEMPLATE.md), proves

    T(n)=O(n sqrt(L) (x+2)^C*),
    C*=max(p_I+4,p_W+b_CT+1),

under all CT-I and CT-W contracts. Their constants fix a finite absolute
exponent; no numerical value is asserted before they are supplied.
Both local template families remain unconstructed. Here b_CT is the
fixed root-logarithm exponent denoted b in CT; it is unrelated to the
varying field-degree parameter b in the later exact CRT caller.

CT-I requires an exact finite reduction with bounded normalized actual
child-volume mass, polynomial arity work, paid generation and absolute
visited space. CT-W requires a full-rate Walsh identity, bounded normalized
mass and a jointly charged physical delivery schedule, including actual
post-XOR volumes, numerical heights/norms, setup and a common payload cap.
The proof covers child-width guards, adaptive arity, occupied batching,
precision, both recurrences, the actual integer caller and exceptional
small inputs. This is a new complete conditional written reduction in
this session, not a construction or priority claim.

## Representation work: useful local results and explicit stops

[RO](route-a/rowspace-orbit-compiler.md) executes columnwise invertible
binary reindexings locally in supplied rowspace coordinates, under its
complete-fibre and wide-record conventions. It retains every independent
input. Its generic converter incurs a Va term alongside polynomial-
arity work, where a is the active address width.
[RG](lead/rowspace-walsh-rank-gate.md) excludes repairing the Walsh
child's cross-orbit action with a vanishing-rank correction. The exact
[SF decomposition](route-b/spectator-span-fourier-lift.md) keeps all ranks,
ordered frames and the dual-coordinate correction, but retains almost
the entire long quotient width. Two waves left the decisive invoice
unchanged; the current ordinary-orbit implementation is frozen.

[BE](route-a/paired-column-bell-executor.md) changes the representation.
With common even slot width, one admissible pairing and the supplied
orbit layout, square full-rate Bell coordinates close the actual paired GL,
Walsh and quadratic-parity rational repair algebra in polynomial local
work. It covers dependent translations, affine phases, actual table
evaluation and an explicit precision guard. It has no initialized-only
sector or loss of independent input data.

Entry and exit still cost full-volume half-width Walsh calls.
[SU](route-a/square-encoder-support-budget.md) proves that the total
partial-Walsh width is at least a/2 per encoder in the specified square
Walsh/monomial class; Bell attains that budget with one call.
[BO](route-b/bell-outer-boundary.md) shows that the encoded outer
product becomes full XOR convolution; the existing local theorem does
not cover the actual outer phase tables. The standard complete schedule still
pays six half-width transforms. Bell survives as a local executor;
pairing-constant tuning is stopped. A new converter, shared-endpoint
or bilinear implementation must change its actual cost. These are
scoped invoices, not universal time lower bounds.

## A different exact caller and its remaining gate

[UC](route-a/unramified-polynomial-crt-caller.md) uses CRT over
Z/(2^H), with all literal binary lifts of irreducibles whose degrees
divide b, q=2^b. The factor degrees sum to q: both representations
contain exactly qH independent payload bits. The packing gives
qH=Theta(n), H=Theta(b), b=Theta(log n). Product-degree and coefficient
bounds ensure exact integer recovery followed by a linear carry scan.
The actual lifted product P is used; P is not assumed equal to X^q-X.

Local residue products cost O(qH log^2(b+2)) using O(bH)-bit integers.
[FS](route-a/binary-factor-stream-compiler.md) generates the factors
in q b polylog(b)+poly(b) tape steps: scanned Lyndon enumeration,
one normal-basis conversion per orbit, sequential conjugates and
explicitly packed small products. The compact directory has O(q) bits;
repeated setup products have O(b^2 log(b+2))-bit operands. The cited
deterministic preprocessing is polynomial in the small degree parameter.
These costs fit the prospective endpoint budget after a fixed cutoff.

**Fast forward/inverse CRT remains open.** Classical product/remainder
trees have a safe O(qH b^2) product/remainder-stage invoice, before
separately pricing global inverse constants and a common-space schedule.
They include full-size upper-level integer products. Paying those
products with the desired theorem would be circular.

UC identifies K_t, the new high t remainder bits on canonical t-bit
input. Both transform directions at precision 2t use two half-precision
calls, the same K_t and linear scans. If binary CRT costs qB(b) and
K_t costs qtD(b,t), the normalized bill is

    T_CRT(q,H)/(qH)<=C B(b)+C sum_(dyadic t<H)(1+D(b,t)).

B(b)=O(sqrt(b)), D(b,t)=O(1+sqrt(t)), and the stated absolute local
space contracts would give the endpoint. Both fast suppliers are open.
The broader explicit contracts give a polynomial log-log target.

[KC](lead/carry-remainder-interface.md) isolates the first carry:
over F2: for actual integer remainder matrix A, E=A mod2, D=(A-E)/2 mod2,

    K_1(x)=D x+sum_(i<j)(E_i odot E_j)x_i x_j.

A lifted binary XOR circuit computes its own integer matrix C. It
needs the linear correction ((A-C)/2 mod2)x to produce the actual
carry. Construction and execution of that correction must be paid.
The canonical identities extend to higher precision. This gives the
next concrete question: a fast binary circuit with a cheap actual-lift
correction. [Independent UC/FS review](route-c/REVIEW-UNRAMIFIED-CRT.md)
and [KC/precision review](route-b/REVIEW-CRT-CALLER-AND-CARRY.md) keep
these limits explicit.

## Verification and formal scope

[Fresh algebra reconstruction](lead/FINITE-ALGEBRA-AUDIT.md) and
[independent review](route-b/REVIEW-FINITE-ALGEBRA-CHAIN.md) cover
Boolean-to-F4 substitution, whole-module cyclic identities, input-grade
orientation, compact checks, field packing and order-three words.
An audit sentence was corrected: C squared is one allowed query power;
the local factor two comes from two predictor evaluations. The inherited
invoice was already correct.

The source already supplies arbitrary fare and floor clocks. The
[AS bridge](lead/adaptive-source-interface.md) separates local time
from payload/descriptor space using the exact command closure. Its
concrete adaptive dispatcher and physical body contract remain open.

Five pure-Std Lean files were read and independently rebuilt with Lean
4.35.0: arena reuse, pathwise batching, copied formula size/degree,
whole-word Boolean count semantics and resource potential arithmetic.
Receipts give hashes, commands and standard kernel axioms. No sorry,
new axiom or weakened multiplier target was used. These proofs do not
formalize the complete multiplier, cyclic factorization or AS's actual
OAI instantiation. Upstream requires Lean4.34.1; its complete closure
and comparator were not rebuilt.

Separate exact implementations test Bell/table algebra, outer phases,
CRT module inverses, ordinary integer recovery, precision lifts,
complete small irreducible lists and packed products. Finite controls
include zero polynomials, noncommuting internal factors and independent
extension-field payloads. SF's lead replay uses the author's checker
and is labelled accordingly. Dense small CRTs and brute-force field
searches are checking oracles, not fast suppliers. No human referee
check or exhaustive priority audit is claimed.

## Source state, publication and handoff

Canonical main e54523517d0f03e58352e647c403a5af3e525a57 and OpenAI math
3344da59991ed94f9ba711217b29c1d760badfa6 were refreshed unchanged at
02:20:40 UTC. Prompt/strategy pins are in SESSION.json. The
[literature note](lead/LITERATURE-REFRESH.md) scopes the 25 November
tape-sorting revision and subspace-convolution lead; neither closes
the present converter.

The existing branch `research/moonshot-overhead-program` contains the
work, preserving concurrent S004/E003 completions. Confirmed checkpoints
before final publication include 78273a08ea35dee9997a5d4cfdecb0a1fb787687,
6cc559980c3005e5550ed9c97d6073be51491091 and
d0600416df65f62a935fccf100f3feec5ab363c8. Git history and final chat
identify the commit containing the completed report; no self-referential
hash is embedded. No upstream PR or canonical result was changed.

Next session: prioritize the actual binary CRT/carry compiler; retain
CT as the precise contract for bounded-mass delivery; formalize a real
AS physical body. Do not restart ordinary-orbit or Bell constant tuning
without a supplier that changes the paid global inequality.

## Credits

Jerry Chen (@CubeJerry); pinned OpenAI manuscripts/formalization;
preserved S002/S003/AQ, E002/V, E003 and S004 work; the cited
matrix-factorization and Fourier/Clifford predecessors; Harvey–van der
Hoeven's multiplier; Bshouty–Diab–Kawar–Shahla preprocessing and its
predecessors; Perles–Weinstein and Tal for scoped literature leads.
Substantial ChatGPT multi-agent discovery, derivation, coding and
independent review assisted this session. Standard algebra and earlier
authors' results retain their provenance.
