# Necessary retained-memory injection at a proper-chart cut

**Proved under the declared chronological interface; independent review requested.
No new κ.** This extends the preceding no-side-memory obstruction to actual
retained side information and gives a source-specific canonical overhead.

## 1. General theorem with arbitrary retained memory

Fix any payload field k, positive width V, independent original input blocks
at nonzero real lines L_j, and final facets F_j=L_j-perp in a positive-definite
real space. Permit an invertible X subsystem z=P x formed by arbitrary
cocharted X-to-X block transformations and monotone upward X moves. Before
a cut, X information may also be copied into retained side records, including
original Y, owned caches or other memories. Such copies do not alter the X
subsystem. Let S be the matrix of ALL actual retained side-state X coefficients
at the cut, with original independent Y set to zero only for the obstruction
argument. This is a relaxation of arbitrary-Y completion, not a source shortcut.

Grant the row space of S globally, and grant any fixed global space generated
by cut-Hub X rows. After the cut the only additional propagation of X information
is through cocharted linear operations and upward moves. Fresh downward
nonlocal information or later enlargement of the fixed globals is excluded.

Take h current original X banks all at the same proper chart C. Write W_A
for their hV inverse columns in P^(-1). Then complete identity delivery at
all original target facets NECESSARILY requires

    rank(S W_A)=hV.                                      (1)

Proof. Inverse-column locality holds despite one-way side copies: every
original line supporting W_A lies in C. If (1) fails, choose a nonzero
hV-vector v in its kernel. The original perturbation w=W_A v is nonzero,
whereas every cut-Hub X row and every side state has zero perturbation.
All initially nonzero current-X records are at the SAME C. Every later local
nonzero perturbation therefore remains at a chart containing C. For any
nonzero original block w_j, L_j lies in C, so C is not contained in F_j by
positive definiteness. Its required nonzero output cannot be reached.
The arbitrary block proof uses no commuting coefficient or scalar assumption.

Co-chartedness is essential to this statement. Separate held charts can
interact with different receiver sets; summing their individual lower bounds
without a joint argument is invalid. The result also does not turn access to
side rows into a free physical global service. It grants that service only
to derive a necessary condition. Passing (1) does not establish any schedule.

## 2. Actual four-copy MDS prefix

Root independently recomputes the entire444-by444 inverse matrix at each cut
by augmented elimination, instead of C's incremental inverse-column updates.
At the chart-aggregate cut,440 X banks are at Hub. Four held banks form two
cocharted pairs: X1_2,X1_3 at C2 and X2_2,X2_3 at C3. Their inverse-column
hex masks are respectively90,e0,d00,600, with supports on original roots1
and2. The exact proper-chart inclusions are independently checked by rational
augmented rank.

Although some original Y already contains X information, its restriction
S W_A has rank ZERO for EACH two-bank group. Thus the earlier Y copies do
not repair the frozen-global completion obstruction at this cut. The theorem
applies with those actual Y rows included. Any completion retaining this cut
must acquire new side information, form further globals or otherwise change
the permitted propagation. It does not invalidate the local foreign correction
or its paid late-K completion, which already use a changed continuation.

Two actual stationary copies of the two held pivot values at each chart give
identity restriction and pass this necessary test. They cost real INIT/ADD
and later retirement; their dissemination is still missing. Dropping one
copy gives rank1 instead of2 and fails. These exact controls show that an
unrelated earlier Y copy cannot be counted as acquisition of a missing mode.

## 3. Exact canonical overhead for importing the four actual held rows

Let H be the440-dimensional cut-Hub row space and D the4-dimensional row
space of the actual held X values, so H direct-sum D is the full444-dimensional
input row space. Let C_can be the fixed canonical36-dimensional code across
four binary copies. The exact current source has

    dim(C_can intersect H)=32,
    dim(C_can intersect D)=0,
    dim(C_can+D)=40.                                     (2)

Suppose the four actual D rows are granted globally and B is a subspace of H
such that C_can is contained in B+D. Projection along D gives

    projection_H(C_can) subset B,
    dim B >= dim C_can - dim(C_can intersect D)=36.       (3)

Equality is algebraically attained by B=projection_H(C_can). Therefore this
particular actual-held-row import requires40 total global modes, including
at least36 from Hub. Merely observing32 canonical dimensions at Hub and four
missing dimensions does NOT prove a36-mode acquisition scheme: the actual
held rows add nuisance directions outside the canonical code. Choosing other
actual proper sources may change this quotient; their acquisition must be shown.

Equations (2) are exact binary matrix statements. For this fixed source word
their tensor extension gives ranks32V,36V and40V over every characteristic-two
field and original width V. No arbitrary-block source optimization is inferred.
This is an actual-source application of elementary projection/quotient algebra,
not a claim that that linear-algebra fact itself is new.

Reproduce check.py --repo REPO --source SHARED_FACET_AUTHOR --out OUT.
The independent receipt contains all three chronological cuts, inverse columns,
actual side-row restrictions and changed-cache controls. Credit @CubeJerry,
C's inverse-column theorem, root's retained-memory extension and source-specific
quotient computation, and all retained native/code predecessors; OpenAI assistance.
