# UNVERIFIED recovery: BIT selector lift and its paid repair

Status: exact finite checks and a scoped written algebraic argument; independent
scientific review was NOT completed. Do not publish this as a verified research
contribution or a new kappa. Workspace access failed before integration.

Frozen source: CrocSwap/integer-mult-bounds main
e54523517d0f03e58352e647c403a5af3e525a57.
The source pins are in SOURCES.json. No new branch, selected certificate or
upstream pull request is part of this recovery subtree.

## Selector invariant without averaging

Partition the source word into 222 main fields and its public-helper/owned core.
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

The exact canonical BIT source has M0=I, whereas E sends each of111 Y fields
to Y+X and preserves111 X fields. The unrepaired lift therefore misses
111(m-1) independent Y shears. The original659-public-field endpoint was
replayed with zero coefficient mismatches, and all222 main-only rows equal
identity. This is a finite scalar-source statement, not a new all-column
physical admission.

## Literal paid endpoint repair

At the complete endpoint, each X field is in its full dimension8 frame and
its corresponding Y is in a dimension7 body frame. Copied X fields of one
port have exactly the same frame. For passive copy i and each port, allocate
owned zero Z in the X frame, add X_i and X_1 into Z, execute one paid rank1
nested MOVE to the Y frame, add Z into Y_i, and clear Z. This supplies the
missing normalized X_i-X_1 term (minus equals plus in F2).

The repair has six literal events, one rank1 paid job, and one owned lifetime
per port/passive copy. A single extra owned label can be reused after each
complete CLEAR. Clearing a nonzero owned value retains the canonical owned
erasure assumption; this note does not discharge it. All original source
MOVEs are charged, including public MOVEs. Every added MOVE is charged.

The checker constructs and replays this lift+repair for m=2,4,6, obtaining:
- m2:881 public fields,238 owned labels,57757 events,111 added rank1 calls;
- m4:1325 public fields,238 owned labels,104997 events,333 added rank1 calls;
- m6:1769 public fields,238 owned labels,152237 events,555 added rank1 calls.
All new public scalar endpoints and all final frames pass. No full native word
was written to disk. The source grammar and its original native realization
remain inherited; no updated physical all-width, precision or tape audit ran.

## Complete target invoice and the scoped obstruction

Let t=199/200. The current paired E-free BIT caller has complete signed moment
M2< -444. Decompose source paid jobs by physical owner: P_main is the222-main
bill and P_core the helper/owned bill; H0 is the437-helper productive profile.
The exact root-envelope checker independently proves D=(P_core-H0)_t<88.

The new block's helper profile is H0 and paid profile is
m P_main + P_core +111(m-1) rank1 jobs. Insert it at the18 body stages and take
m/2 copies of the paired E-free root (even m). Root target/query/idle terms are
all retained. Its complete signed target moment is exactly

M_lift(m)=(m/2)M2+18(m-1)(D-111)
         < -222m-414(m-1) <0.

The numerical inequality is true for every integer m>=2; caller assembly uses
even m. Therefore this particular selector lift with this displayed paid
repair cannot satisfy the existing strict-moment compiler at kappa=1/200.
It does NOT prove that every shared-core construction, every repair schedule,
cross-plane batch, bus itinerary or changed computational representation fails.
No optimality of the111-per-passive-copy repair bill is claimed.

The target root terms used are the canonical paired caller formulas:
T_total=18 H_m +111m H127+222m sum(j=1..9)H_(1+7j);
P_total=18 P_m +222m H1+222m sum(j=1..8)H_(7j).
They come from research/paired-query-only-bit/PROOF.md, including every
nonempty root target, thin query, idle and native call. Source helper and
paid histograms are independently recomputed from the frozen native.

## Execution and limitations

The exact verifyWord function in verify.js was executed in the surviving
functions V8 runtime against cached canonical source bytes. Initial recovery
used a hand-written JavaScript gzip decoder, checking111747 compressed bytes,
745029 decompressed bytes, gzip CRC32=764150836. Those same compressed bytes
had already passed SHA256 authentication before workspace loss. The verifier's
ordinary Node fs/crypto/zlib CLI wrapper has NOT been executed in this session.

The core function replays all434281 original public scalar coefficients,
verifies M0=I, constructs three finite repaired lifts, and proves the moment
bounds by exact integer200th-root intervals at scale2^128. Adjacent integer
powers authenticate every root enclosure. No floating-point acceptance is used.

Reproduce after workspace recovery:
  node verify.js PATH/TO/BIT-NATIVE-WORD.json.gz
The CLI first authenticates SHA256 and then compares the exact RESULT.json.
Expected status: PASS_FINITE_SOURCE_REPLAY_AND_SCOPED_COST_SCREEN.
Independent review remains NOT_COMPLETED.

The five foundational assumptions are unchanged: native_all_columns,
owned_erasure, compiler, precision_tape, analytic_recovery. This recovery work
discharges none. Credit the retained BIT native/caller authors, DreamingOfClouds,
zxv, @CubeJerry and their source notices. The selector invariant, repair screen
and independent exact-root price check were developed with substantial OpenAI
assistance. Prepared for @CubeJerry. No independent human review is claimed.

## Open next question

Can an alternate shared-core word or a cheaper admissible correction produce
the required main endpoint while avoiding this particular full repair bill?
A same-chart claim must respect the actual dimension8/dimension7 boundary,
and any new batching, role mixing, queries, storage and erasure must be paid.
