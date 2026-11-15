# Exact bank expansion realizes finite lane circuits as multicopy native words

**Proved finite-word translation; source admission requires the expanded
literal word and its full counts. No complete supplier or new κ.**
This changes the representation and productive multiplicity. It does not
implement a lane mask for free inside one retained physical array.

## 1. Translation theorem

Fix an integer b>=1 before the tensor-column multiplicity or input size varies.
Let a finite source program have finitely many named records, each represented
algebraically by b banks. All banks of a record have the same chart. Permitted
operations are full-record scalar ADD/SCALE, zero INIT, CLEAR, MOVE between
declared charts acting identically on each bank, and bank operations

    ADD_BANK(source,a,target,c): target[c] += source[a]

with fixed bank indices. Distinct source/target bank identities are required
for an invertible elementary ADD. Suppose the formal program is an identity
on arbitrary independent original bank values with its declared outputs,
source restoration and owned handoff. Each bank transform is the same native
all-column transform assigned to its chart; this is a declared b-copy source
interface, not a hidden decomposition of one array.

Replace each record R by b separately named ordinary records R_0,...,R_(b-1).
Each original bank is an independent original input. Each owned bank is a
separately zero-born owner. Translate INIT, CLEAR and MOVE into b chronological
operations, one on each bank. Translate a full ADD or SCALE into b ordinary
operations. Translate ADD_BANK into the one ordinary ADD between its named
bank records. A whole-bank permutation is an explicit fixed role permutation,
or its stated counted ADD implementation.

Every translated operation belongs to the existing full-record alphabet.
Full-record operations on different banks commute, so any fixed ordering
implements the original simultaneous bank operation. A bank ADD is cocharted
because its source and target records inherit the same actual chart from the
verified bank program. Induction over operations identifies every translated
record value with its corresponding formal bank after each original step.
Thus the original identities, arbitrary-input domain, restoration, output
independence and final ownership states all hold in the expanded word.

The argument works for every positive column multiplicity and every field
admitted by the source scalar grammar. No new coefficient, selector, inverse,
clean field or within-array permutation is used. A fixed b enlarges the finite
role catalogue and its constants; it is not allowed to grow with input size.

## 2. Exact accounting

For a b-bank program with F full ADDs, L bank ADDs, M whole-record MOVEs and O
owned lifetimes, the translation has

    bF+L ordinary ADDs,  bM MOVEs,  bO owned lifetimes.

Every rank-r MOVE appears b times, so its complete movement profile and moment
multiply by b. Every INIT/CLEAR remains present; dirty/zero status is checked
per physical bank and cannot be inferred merely from whole-record nonzeroness.
Any whole SCALE or separately specified role route is charged according to its
translation. Counts for all productive originals and unfinished receiver
ascents likewise multiply by b. There is no reuse of an owned bank between
simultaneously live formal banks.

For the present two-lane cohort candidate, b=2,F=674,L=778,M=495,O=200.
The predicted expanded counts are2126 ordinary ADDs,990 MOVEs and400 owned
lifetimes. Its movement profile is twice

    183[1]+12[2]+119[3]+71[4]+110[7].

These predictions must be confirmed from the actual expanded operation word.
The two-copy source has444 independent original X/Y columns. It acquires
19 dimensions of W30 from D80, with11 remaining W quotient dimensions. It
completes only the two actual copies of Y0. No full fitting decoder is claimed.

## 3. Complete caller homogeneity

Let the retained scalar-unit invoice be N,H,P2,T2,Q and, for an admissible m,

    P_m=(m/2)P2-18(m-1)N+18(m-1)Q,
    T_m=(m/2)T2-18(m-1)H.

Use b independent copies of the complete caller, including its native bodies,
productive jobs, all boundary terms and restoration. Replace the corresponding
b source occurrences jointly by the expanded bank word only when that word
supplies their full required interface. The new invoice is

    (N',H',P2',T2',Q')=b(N,H,P2,T2,Q).

Therefore P'_m=bP_m and T'_m=bT_m. The limiting source threshold is also
B'_infinity=bB_infinity; the sign of the movement feasibility inequality and
its finite-m margin are unchanged after division by b. The mixed-unit moment
root is unchanged because both paid and productive sums scale by b.

### Bounded batching and chronology

This is a new finite unit with b times the original productive inventory,
not a promise that an arbitrary running single caller has another matching
task available for free. Its inputs explicitly contain b independent copies
of the original unit's arbitrary input arrays. For each corresponding source
occurrence, execute each copy's prefix up to that occurrence and suspend it.
The copies have identical parameters and corresponding charts, so all b source
interfaces are now available. Execute the joint source word, which must return
the direct sum of those b interfaces. Resume the b prefixes to the next matched
occurrence and repeat. Operations on different copies commute before and after
the joint replacement, so this finite schedule preserves each copy's semantics.

Every suspended copy retains its own complete originals, owned fields and
child state. The live inventory is bounded by the sum of the b original
inventories and the joint source's explicitly counted owners. Work is the sum
of executed operations; no concurrent execution is credited as cheaper time.
The source word's completed endpoint is required before either copy resumes.
This is the arbitrary-independent-array, finite-program category in the
retained compiler. Its admitted supplier may have a larger fixed productive
multiplicity. No padding of an unpaired single task or uncharged auxiliary
productive input is assumed.

This calculation grants no partial decoder. Until all required outputs are
constructed, it is only an optimistic necessary whole-system budget. It also
does not erase ordinary costs: the finite compiler must use the expanded
operation, role, storage, adapter and precision constants. A repeated source
word is not credited as b jobs without b independent arbitrary inputs and the
full corresponding completed outputs.

## 4. Why this is compatible with the retained category

The retained finite-precompilation contract explicitly allows arbitrary
independent productive arrays, complete spectators, finite scalar/routing
passes and a finite owned inventory. Its native requirement is all-column
correctness and declared endpoint restoration. The translated source consists
only of existing ADD/INIT/CLEAR/MOVE operations on actual separate owners;
there is no request to enlarge that grammar by a coordinate-dependent mask.
Whole-job adapters and every child remain attached to the actual copy whose
job is invoked. The complete caller's finite replication is a permitted
finite composition; coupling copies by cocharted ordinary ADDs does not change
the type of any operation. Exact source identities, rather than operation
membership alone, must establish the resulting completed endpoints.

The scalar word is fixed before multiplicity varies. For each native chart
C, both bank records carry the same all-column transform T_C, so cocharted
cross-bank ADDs commute with it by linearity. This avoids the false inference
that a diagonal lane projector alone licenses an off-diagonal bank transfer.
No large packed memory layout, masked streaming access or new lane compiler
premise is needed for the separately owned representation.

The protected distinction remains: the exact block-capacity theorem concerns
all widths within its abstract run interface; this finite two-copy word
physically realizes its V=2 coefficient pattern and tensors by arbitrary
whole-record multiplicity. Odd abstract widths can use a separate scalar
copy if needed, with every resulting job counted. The two-copy construction
already gives the normalized9.5 acquisition needed for the current test.

Dependencies: the exact cohort-capacity theorem and bank word; native geometry
SHA2568cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e;
retained FINITE-PRECOMPILATION SHA2564cb32f6b8e388ecf6ed41b5bbdeeb4539cb40c8424f194974afea58f7e0921e8;
retained SPECIALIZATION SHA25670430114f744108223bc1d44b98bc25b696c4b408b7b044c2a8bbdfdb434ac5c.
All five foundational assumptions remain. Credit @CubeJerry, native/compiler
predecessors, Worker C's capacity and lane word, and root's multicopy
translation and complete invoice reduction. OpenAI assistance.
