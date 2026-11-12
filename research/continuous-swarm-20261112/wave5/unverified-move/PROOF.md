# A complete literal leaf for the actual selected MOVE24472

**Scoped source-composition lemma; no new kappa.** Prepared for Jerry Chen /
@CubeJerry with substantial OpenAI assistance. Canonical base:
`e54523517d0f03e58352e647c403a5af3e525a57`.

## 1. Source operator and credited predecessor boundary

The exact native source is the retained #7000 word
`research/shared-wire-split-composition/data/final.json.gz`, compressed SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Its zero-based event **24472** is `["MOVE",415,3,99,false]`. Write F3 and F99
for its canonical nine-coordinate frame operators. The target one-column
operator is the chronological circuit `F3 adjoint; F99`. This convention is
important: the target is the original source transition, with its absolute
phase and normalization, not merely an equal binary address action.

The authenticated exact lowering retained in RECIPE.json has rank 1. Its
chronological factors are

`right diagonal; G_right; X_1; C on coordinate 0; left diagonal; G_left`.

The global phase of the right monomial is included in its diagonal, once per
tensor column. The left offset and global phase are zero. The matrix rows,
indexed by output coordinate bits, are exactly

| Factor | Binary row masks |
| --- | --- |
| G_right | `(239,129,130,132,136,16,160,192,256)` |
| G_left | `(3,5,9,17,32,65,129,1,256)` |

The right diagonal is the fixed B3 recipe. For
`J={0,1,2,3,5,6}` it is multiplication by `i^q_R(x)`, where

`q_R(x)=1+3 sum_(i in J) x_i+2x_7+2 sum_(i<j in J) x_i x_j (mod 4)`.

The left diagonal has no quadratic terms and is
`q_L(x)=2x_0 (mod 4)`. The positive child is

`C=(1/2) [[1+i,1-i],[1-i,1+i]]`.

Rank 1 selects this child on native coordinate 0. It does not replace the
runtime column width f by 1: the actual child is C tensor f.

The source binder recomputes this lowering and compares all 512 complete
basis columns against the independent original-frame circuit evaluator.
The numerical test oracle independently tensors those original-frame
columns; it imports neither the literal factors nor their factored recipe.
Fixed-source equality of all basis columns, followed by linearity and the
tensor law, applies to arbitrary joint coefficient arrays, not only pure
tensors. The finite source audit pins this one fixed operator; the all-f
implementation statement is proved below.

[#6974](https://github.com/CrocSwap/integer-mult-bounds/pull/6974) already proves
protected whole-MOVE composition for an older current-coded occurrence, with
numerical-provider premises and stronger named-failure retirement. Its proof
explicitly leaves the complete literal lifecycle export open. Its protected
staging mechanism and source factorization are credited. #3091 and its lineage
supply the Gaussian identities, tensor grid reserve and physical direct tariff.
This result supplies one complete fixed transition graph on a different exact
source/packed boundary, joining the separately lowered literal factors.

## 2. Supplied packed ABI and exact theorem

Supply six positive integers `f,r,P,S,w,t` consecutively as canonical Elias
Gamma codes on HEADER. Gamma(n) consists of `ell(n)-1` zeroes followed by its
ell(n) ordinary binary digits. Let E be the length of all six codes. The graph
checks `w>=2` and `f<=t`. The threshold t stays binary; its numerical magnitude
is not charged as unary work. Arbitrary opaque header data may follow the sixth
code, and every factor that reads only the first five preserves the entire tail.

DATA is the complete lexicographic array

`[P] x [2^f]^9 x [S]`,

with a0 slowest and a8 fastest among the nine active coordinates. There are r
Gaussian coefficients at every address. Each coefficient is w signed MSB-first
real bits followed by w signed MSB-first imaginary bits, in two's complement
on one arbitrary fixed common grid. Set

`Q=2^(9f)`, `N=P Q S r`, `V=2Nw`.

The field consists of exactly V binary cells followed by a physical blank.
Cells after this blank, cells before the field, and header exteriors are opaque.
The original HEADER and DATA heads start at their respective origins. The
**171 fixed owners** are distinct; origin choices may differ and may be negative.
On each of 169 private roles the interval from origin minus one through
origin plus `V+E+2` is supplied blank. Smaller role-specific reservations are
possible from the component proofs, but this simple common cap is sufficient.
This is an explicit whole-window blankness/ownership premise, not inferred
from two local probes. All previously allocated source, opaque and blank
storage is included in actual entry backing K0.

For an active tuple a and column j, native bit i is
`x_(j,i)=(a_i >> j)&1`. The desired operation applies the original source
transition independently to each of these f nine-bit columns, preserving
prefix, spectator and coefficient indices. Denote this lifted operator U_f.

**Theorem.** `compile_move()` emits one fixed **84,280-location** program on
171 tapes, alphabet `{blank,0,1,|}`, containing only local scanned-symbol
reads, one-cell writes, unit moves, fixed jumps and halt. It has no runtime
shape, recipe, owner index, source callback, decoded address or compiler call.
On the supplied complete ABI with `w>=2` and `f<=t`, every successful execution
replaces the original DATA field by exactly U_f applied to its coefficients,
preserves HEADER and every opaque exterior, restores all heads to their entry
origins, and erases all private bodies and guards. It writes exactly V bits
to the original DATA owner, once in its final commit.

Its exact numerical acceptance domain is the conjunction of the component
guards in their stated order: the right Gaussian rotations must fit w bits;
every actually executed low-bit-first C prefix must be integral and fit w bits;
and the left Gaussian rotations must fit w bits. Permutations add no numerical
guard. Equivalently, on a well-formed admitted geometry it accepts precisely
when all these finite-width operations are valid. Endpoint integrality alone
does not imply this prefix condition.

A useful explicit sufficient domain is: every input component is divisible by
`2^ceil(f/2)`, has magnitude at most M, and

`2^ceil(f/2) M <= 2^(w-1)-1`.

On this domain every guard succeeds. On any numerical guard failure, HEADER
contents and the entire original DATA contents/owner remain unchanged, including
their exteriors. Private cleanup and head return after rejection, interruption
recovery and immediate rejected-call reuse are not claimed. Header/cardinality
rejections discovered before the factors also precede every original DATA write.

The complete instruction count on success, and up to a numerical rejection on
a legal complete packet, obeys

`T <= 2^24 (fV+E+1)`.

For actual pre-entry historical backing K0, a sufficient all-owner envelope is

`K_final <= K0+512(V+E+1)`.

These are direct-leaf O(fV+E) and retained-history bounds. They do not imply an
unrestricted-f O(V) supplier, a nonleaf recurrence improvement, or a new complete
multiplication exponent.

## 3. Fixed linking and exact entry geometry

The wrapper uses the frozen C4 literal Gamma, binary cutoff, generated geometry,
clone, return and commit helpers. It first installs the 27 fixed master guards,
reads all six codes, returns HEADER using an erased trace, compares f and t
without expanding t, and checks two width marks. The generated initial C shape is

`A0=P 2^(f-1)`, `U0=S r 2^(8f)`.

Its identity `2 A0 U0=N` makes the width-guided clone read precisely V bits.
The clone checks a blank after the field, returns original DATA with its erased
trace, and returns the shadow head. It does not modify DATA. The parameter and
geometry guides are erased before entering the factors; the shadow and master
guards remain. All factors receive HEADER at the same origin and this complete
shadow field at the same origin. The shadow's guard is an opaque public-prefix
cell to each factor, which never reads or alters it.

The fixed tape allocation is as follows; all ranges are inclusive.

| Stage | Private roles | Locations |
| --- | --- | ---: |
| Master wrapper, including shadow role 2 | 2--28 | 1,532 |
| Right diagonal | 29--49 | 8,211 |
| Right G | 50--74 | 24,451 |
| Right X1 | 75--97 | 1,878 |
| Positive C tensor f | 98--124 | 6,826 |
| Left diagonal | 125--145 | 7,251 |
| Left G | 146--170 | 34,131 |

For each component, input tape 0 becomes original HEADER, input tape 1 becomes
shadow role 2, and its private tape IDs become its disjoint fixed cohort. Every
program counter target is shifted by the constant start location. Each successful
halt becomes one fixed jump to the next stage, retaining its one-instruction
price. Rejection branches remain rejection branches. No other opcode or branch
is changed. `audit_link` compares all **82,748** included instructions with this
rule; the mathematical correspondence is pointwise, not a runtime call service.

Consequently the component's normal theorem transfers by induction on its
local instructions. All component private bodies are initially blank, guards
are private, and previously used cohorts are disjoint. Normal completion
restores HEADER, shadow and every cohort head and erases that cohort. Its output
has exactly the same V-bit raw common-grid layout required by the next factor.
Neither head transport nor a changed coordinate packing is hidden at a join.

## 4. The missing left phase and all-column source composition

The retained phase graph constructor accepts a fixed linear vector, symmetric
quadratic rows and constant in addition to its selected default. The left call
uses `(2,0,0,0,0,0,0,0,0)`, nine zero rows and constant zero. These satisfy the
constructor's dimension, symmetry and diagonal-parity constraints. This is a
fixed graph specialization, not a runtime recipe loader.

For clarity, its new left-source consequence does not follow merely by naming
the right-specific theorem. Initially every coordinate counter is zero and its
four-state phase is `f*0=0`. Flipping bit x in coordinate 0 changes the phase by
`2(1-2x)=2 (mod 4)`; flips in any other coordinate change it by zero. There are
no quadratic-neighbor reads contributing a value. The inherited synchronized
counter invariant therefore becomes

`Phi_L(a)=2 sum_(j=0)^(f-1) bit_j(a0)=2 popcount(a0) (mod 4)`.

The Gaussian action is exactly `(-1)^popcount(a0)` on every coefficient at that
address. Counter wrap and repetition preserve this formula. It is applied
before G_left, in agreement with the source constructor; using a phase of the
post-G coordinates would in general be wrong. The same literal negation and
signed-minimum guard apply, with the same or smaller complete phase cost.

The right phase includes its constant 1 on each of f columns, hence a scalar
`i^f`, not a single i and not a missing unit. It is evaluated in input coordinates
before G_right. G_right's fixed CNOT word maps native bits by the rows in Section
1 for every column. The next translation flips output coordinate 0 across all
f columns: `a0 -> a0 XOR (2^f-1)`. Its descriptor producer and complete-record
reversal pay for the whole suffix; bit zero in the native chart is not confused
with the fastest packed coordinate. The positive leaf then applies C on every
bit of a0. The left sign and G_left finish the actual source factorization.

All six operations preserve the stated spectator, coefficient and common-grid
interfaces. Equality to U_f follows from the exact one-column source equality
and distributivity of tensor products over composition. No factor of the
exterior native compiler or old coded-format conversion is inferred from this
local equality.

## 5. Numerical admission and whole-public atomicity

Gaussian unit rotations and the two binary affine permutations preserve the
component magnitude bound and divisibility. Thus the right entrance leaves the
sufficient input reserve unchanged. For a C tensor prefix of k columns, the
credited exact tensor kernel has denominator dividing `2^ceil(k/2)` and real
component row norm at most `2^ceil(k/2)`. Since k<=f, the sufficient divisibility
condition makes every prefix integral and its component magnitude is at most
`2^ceil(f/2)M`. The upper bound `2^(w-1)-1` is symmetric; it also excludes the
one signed endpoint that a later negation cannot represent. Every C guard and
the left-sign guard therefore succeeds. This uses the inherited exact prefix
reserve, not an endpoint-only or floating-point argument.

On general inputs outside that sufficient domain, the exact component guards
still define the wider legitimate acceptance set. In particular C may succeed
at its most-negative endpoint and the subsequent left sign may reject. The
author late-left witness has w=3 and an exact C output -4 on a0=1. Its reachable
pre-C pair is `(-2-2i,-2+2i)` and its supplied source input is the inverse of the
actual right monomial applied to that pair. C succeeds; the left sign attempts
+4 and rejects. This witnesses a genuine need for protection across the entire
join rather than child-local public preservation.

Original DATA is only read by the outer clone. Every component treats the
private shadow as its public DATA. A failure at any component therefore cannot
alter original DATA, even if earlier components have completely committed to
the shadow. Static inspection shows the only two original-DATA write locations
are the two bit branches of the final master commit. That commit is entered
only after all six successes. At that point the source shadow is a complete
valid V-bit result, so no arithmetic or cardinality rejection remains during
commit. The commit erases the shadow as it writes original DATA, traces and
returns the original head, returns the shadow head, and erases every master
guard. Other private cohorts are already blank and restored.

The failure promise concerns the program's explicit guard rejections under
its entry premises. It does not promise transactional behavior under physical
interruption in the final overwrite, or under a corrupted factor falsely
reporting success. No failed private cohort is relabelled clean for a later call.

## 6. Complete instruction bill

All five opcode kinds have unit price. Component relabeling changes no
instruction price, and each halt-to-jump substitution costs exactly one.
Every predecessor tariff includes its own header reads, geometry generation,
source clone, data moves, copy/return, all tensor columns and normal retirement.
Those costs are retained even when several stages repeat a header scan or stage
the same shadow field. There is no cancellation of separate helper bills.

For fixed m=9, the phase predecessor bounds a complete phase or its numerical
failure prefix by `65536 B`, where

`B=E5+10f+r+P+S+w+100 P Q+V+1`.

Here E5<=E; f,r,P,S,w<=V; and `P Q<=V/4` because w>=2 and r,S>=1. Therefore
`B<=E+40V+1<=40(V+E+1)`. The left graph has fewer fixed neighbor operations,
and the same bound holds by its invariant and unchanged per-operation census.
The two phases together cost at most `5,242,880(V+E+1)`.

Each of the two fixed matrix graphs and the positive C graph costs at most
`65536(fV+E+1)`. The selected X1 graph costs at most `4096(V+E+1)`. Their
tables include full field movement and all input/header return, not just the
algebraic CNOT or rotation work.

The outer front is the literal C4 six-field header/guard, initial geometry and
source-clone front; the outer back is its literal commit/retirement pattern.
Its guide clearings are the same scans, executed before the components rather
than after the numerical axes. It omits the numerical loop, MODE selection and
several axis-end returns. The separately proved front/back bounds, together
with all 27 master guard pairs and fixed jumps, fit `32768(V+E+1)`. This includes
the additional whole protected field, all copying, original-source access and
return, and final erasure. Threshold t contributes only O(E) binary work.

Because f>=1, summing these six complete factor bills and the outer bill gives
at most `5,476,352(fV+E+1)`, below the stated `2^24(fV+E+1)`. The same finite
loop bounds apply before a numerical rejection: the failed scan is a prefix
of its bounded component work and no final commit is needed. These constants
come from the literal helper proofs and exact instruction linkage, not from
fitting finite timing or count data.

## 7. History, blank tails and repeated calls

Each private role remains within its own guard and a body/frontier cap at most
`V+E+2`. This follows directly from the retained cap lists: the phase counters
are length f and its fields length V; the translation's unary suffix and
temporary conversion lengths are <=V; the matrix's pre-halving geometry and
all split/merge banks are <=V; the C component uses w+2 numerator bits and
whole/suffix banks bounded by V. Cutoff bits/length and header traces are <=E.
The master uses the same caps as its C4 geometry/clone/commit helpers.

The sum of the 169 possible new private intervals is at most
`169(V+E+4)`. The two public scan intervals add at most `V+E+2`. Their sum is
below `512(V+E+1)` on this positive complete ABI. Adding these visited intervals
to actual prior historical backing gives the stated bound; overlap with old
backing can only reduce the increment. Initially supplied inputs, opaque
sentinels and preallocated blank tails stay in K0. The test interpreters' head
span observations do not assert that other supplied backing is free.

All actually used body cells and guards are erased on success. Hence every
older tail remains blank. A subsequent smaller clean call scans only its new
guides and fields; none of the loop stopping rules consults historical capacity.
Its time bound depends on its current geometry, while its storage bill retains
the whole previous history. At fixed role origins repeated calls keep the sum
of the individual rolewise maximum intervals, not a single maximum aggregate
volume that forgets which owner reached it. If origins change, the correct
quantity is the union of absolute intervals on each role, including paid
transport corridors. Reinitializing a Python object is not a storage proof.

The supplied creation/re-encoding of a later HEADER or DATA field and any
transport to new origins are outside this adapter. The repeated-call evidence
changes those public inputs externally and preserves the exact private owners,
histories and clean heads between successful calls. No analogous reuse claim
is made after a rejecting execution.

## 8. Remaining obligations and review scope

This supplies one complete selected local leaf, not the whole native J or
compiler. The old current-coded interface uses three physical bits per virtual
symbol, LSB-oriented components and a 23-value descriptor. A caller must still
produce this exact six-Gamma MSB packed field with paid source access, codec and
layout conversion, matching common grid, cutoff, headroom, owner identity and
blank work. Arbitrary strided packing or generic gathers are not supplied here.
The true enclosing occurrence and source-control emission remain separate.

The leaf still requires f<=cutoff. Substituting its O(fV) route into unrestricted
nonleaf work would change the recurrence and needs a new complete budget. The
global precision/cutoff choices, whole-caller stock, analytic recovery and all
five selected foundational assumptions remain conditional. No selected
certificate is changed and no new complete kappa is claimed.

The fixed graph, direct original-source tensor oracle, actual complete m9
packets, late-failure controls, same-owner history and semantic graph mutations
are executable evidence supporting these universal loop/interface arguments.
Finite executions do not prove all widths. Author, separate CPU and independent
review scopes are recorded separately in REVIEW.md and the structured receipts;
human or proof-kernel acceptance is not claimed.
