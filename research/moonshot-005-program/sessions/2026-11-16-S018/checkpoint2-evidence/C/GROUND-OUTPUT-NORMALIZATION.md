# Actual-ground normalization of output carriers

**Constructive interface lemma; no complete supplier or new κ.** Arbitrary
initial Y columns need not prohibit later original-Y forwarding. A finite
binary word with an invertible homogeneous Y transfer can be normalized at
an actual common ground boundary. The same preparation removes exactly
those X errors that are supplied by actual ground fields. This is standard
boundary linear algebra made into a physical native-word transformation,
not a new lower bound or a claim that any desired correction is available.

## 1. Physical hypotheses and exact statement

Fix the111-root native geometry, a characteristic-two coefficient field and
a positive whole-record width. Every coefficient below is a binary scalar
times the identity on that record. At an actual preparation boundary:

* Every original Y is at ground with its independent initial value y_i.
* All other actual records are independent of y. They may be arbitrary
  specified linear functions of the original x inputs.
* There are named, live, pure-X fields G at ground. Their row matrix is G_x.
  Their acquisition, movements, owners and later retirement belong to the
  word's actual ledger. Abstract membership at a remote chart is insufficient.

Let W be a fixed, finite, legal continuation. It completes every owner's
declared lifetime, places every X at Hub and every Y at its own facet, and
has public endpoint map

    X_final = x,
    Y_final = F x + M y.

In particular, **every final X is already independent of all y columns**.
The continuation may contain original-Y feedback into other original or
owned records; this general variant requires the displayed full endpoint
condition, not merely an X-only replay.

Let D be the desired X-to-Y increment matrix. For a partial construction,
D is the diagonal indicator of its completed targets. There is a ground
preparation using only original-Y ADDs and reads from G, leaving every other
boundary value unchanged, that makes the same W finish as

    X_final = x,
    Y_final = y + D x,

if and only if

    M is invertible,
    row(D-F) is contained in row(G_x).

The preparation adds no MOVE, INIT or CLEAR. Its ADDs and their downstream
ordinary/compiler expense must still be counted. The iff is for this fixed
continuation and this preparation class; additional feedback, source fields,
changed routes or new packets can change the problem.

## 2. Proof and constructive compiler

Choose H with H G_x = D-F. First, at actual ground, perform

    Y <- Y + H G.

The old G fields remain unchanged because they are only read. Next perform

    Y <- M^{-1} Y.

Thus the value substituted for the continuation's original Y input is

    y' = M^{-1}(y + (D-F)x).

Linearity of the fixed word and its complete endpoint map give

    X_final = x,
    Y_final = F x + M y' = y + D x.

The X conclusion uses the zero X-from-Y endpoint block. It remains valid
even if Y affects an X or an owned record temporarily. No cached copy of an
old arbitrary y value is assumed, moved, or discarded. Every original Y is
physically present at ground throughout the preparation.

For necessity, any preparation in this class has the form

    Y <- A y + L G_x x,

where A is the invertible product of its original-Y ADDs. The final y block
is M A, so identity requires M invertible and A=M^{-1}. The final X-to-Y
error equation is M L G_x = D-F, hence row(D-F) is contained in row(G_x).
No invertible Y mixing can manufacture an unknown input direction absent
from the actual ground source.

Binary Gaussian elimination supplies a finite ADD implementation of
M^{-1}. A row swap uses three distinct-source ADDs. For n original outputs,
at most n(n-1)+3(n-1) ADDs suffice for this straightforward elimination;
at most nq ADDs load H G from q actual ground fields. This bound is only a
finite ordinary-work bound, not a supplier tariff. Invertibility over F2
means determinant1, so the same binary inverse works over every
characteristic-two field. Tensoring each ADD with the record identity proves
the same statement at every positive whole-record width. No arbitrary
width-dependent block compiler is inferred from this scalar template.

## 3. Easy grammar and known-column specialization

Suppose the continuation never reads an original Y into a non-Y record.
It may read X/owned records into Ys and may perform arbitrary legal
cocharted original-Y-to-Y ADDs. Then M is exactly the product of the latter
transvections and is automatically invertible. Its inverse is obtained by
taking that Y-to-Y ADD subsequence in reverse order and executing it while
all Ys are still cocharted at ground. Co-location of the original later
operations is still required by W; only their inverse preparation is moved.
X restoration is a separate endpoint obligation.

If actual independent raw fields x_s for s in S have reached ground, then
row(G_x)=span{e_s:s in S}. The source condition becomes simply

    F[:, outside S] = D[:, outside S].

All errors on the known S columns can be corrected together by ground
preparation. This includes errors propagated among completed receivers by
later Y forwarding. It does **not** complete any still-incorrect unknown
column. For direct native-to-ground raw preparation, every one of the |S|
rank-one descents, its owner and its CLEAR must be in the ledger.

This is complementary to root's contemporaneous known-offset reset. It
extends the no-Y-source condition to actual Y-to-Y forwarding, and the
general endpoint-block version permits wider feedback when its stated
full endpoint tests hold. It does not automatically compose incompatible
source cuts: all Ys and every advertised donor must actually be at the
preparation boundary with the stated values.

## 4. Concrete native physical control

`ground_output_normalization.py` builds a complete111-role test from the
pinned early-paid46 source geometry. Its source word pin is
`27dc6c36eec067acd2fe4679a81c95ea9db8fd6377784a0bbfc060ca52a121fd`;
its authenticated native root source pin is
`8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`.

Each of the46 completed input coordinates is copied at its own native
line into a separately owned record and physically moved to ground. All
Ys are still raw at ground after this preparation. No old proper source
history is inherited.

The later forwarding pattern uses original Y2,Y3,Y4. Their actual facets
contain the coordinate lines L0 and L1. All three first ascend to L0;
Y2 reads actual raw X0, then Y2 adds into Y3 and Y3 adds into Y4. Y2 and Y3
subsequently ascend to the real two-dimensional span(L0,L1). Actual raw X1
ascends there, adds into Y3, and Y3 adds into Y2. Every X eventually reaches
Hub unchanged and every Y reaches its own facet.

Before normalization, the three affected output values are

    Y2 = y3 + x1,
    Y3 = y2 + y3 + x0 + x1,
    Y4 = y2 + y3 + y4 + x0.

This is a nonidentity invertible Y transfer with genuine forwarding at two
proper charts, not a wholly ground calculation. Its X error depends only
on actual ground-known columns. The compiled preparation uses50 source
ADDs and five inverse ADDs. The final word restores all111 X originals,
preserves all111 arbitrary initial Y columns and supplies exactly the46
declared completed increments.

The normalized word pin is
`83ce8c4cdab17ceccc977c17b8b7d9c0ae655e9ee1dcd9d7a477e70b63a5dd52`.
Its complete ledger is46 INIT,106 ADD,274 MOVE,46 dirty CLEAR, peak46 owners.
The movement profile is

    52[1] + 2[5] + 2[6] + 218[7],

with exact directed moment enclosure beginning
`1585.0375262138081275866073412074841...` at exponent199/200. Normalization
changes no movement, birth or retirement relative to this actual forwarding
control. This partial control is not claimed as an improvement over the
direct46 boundary benchmark: its purpose is to test the extension physically.

## 5. Checks and separate failure controls

The author checker reconstructs every native line and annihilating facet
from the pinned rational source, checks every actual co-location and
monotone MOVE, computes all222 independent endpoint columns, and checks all
owner lifetimes. A second endpoint replay is provided by C's separate
earlier native-word interpreter; no A or root construction code is used.
The binary final row identities are also explicitly tensor-extended to two
independent lanes. The proof, rather than a finite width check, establishes
the all-width statement.

Seven controls reject: the unnormalized word; omitted inverse preparation;
omitted actual known-column correction; a donor read before its ground
arrival; a singular homogeneous Y map; an unknown-column error outside the
actual ground source span; and uncorrected arbitrary-y contamination of an
original X. The singular example uses an actual zero-born ground owner to
copy and cancel one Y, then clears that owner. Its failure is information
loss, not a numerical matrix accident. The unavailable-column example uses
a legal actual read of raw X5 by Y0 at L5, but the advertised ground source
has no x5 direction, so the compiler correctly refuses to normalize it.

The control word and complete results are in
`normalization-control/{WORD,UNNORMALIZED-WORD,RESULT}.json`. Independent
review of this newly authored theorem/control is still requested.

## 6. Predecessor overlap and limits

The admitted `bit-y-feedback-normalization/author/PROOF.md` already permits
arbitrary Y feedback in the historical locality and fitting bounds. Its
arbitrary y terms are explicitly symbolic nuisances, never remote reads.
This lemma provides an actual boundary preparation; it does not weaken
those necessary bounds or supply the unknown historical directions.

`bit-code-decoder-robustness/author/PROOF.md` likewise requires the final
homogeneous Y map to be identity and allows public receiver coding. The
present preparation establishes that identity when its real source and
invertibility premises hold. Its last-incoming-record and suffix-chain
support restrictions continue to apply within their declared source class.

The earlier physical mixed-Y constructions in
`bit-y-feedback-normalization/review-b` and
`bit-joint-multicast/mixed-author` already acquire and transfer mixed y/x
values with real packet operations. No such packet or owner may be deleted
merely because boundary preconditioning is possible: any x duties it
performs remain. The older `bit-allpoint-retention` preconditioner prepares
X-dependent output increments using its actual source fields; it is not a
claimed arbitrary invertible-Y boundary normalization result.

The exact inverse preparation is therefore a constructive search interface,
with substantial predecessor overlap, not an unqualified novelty claim.
All unfinished increments, both strict suppliers, full recursion and the
five foundations remain open: native_all_columns, owned_erasure, compiler,
precision_tape and analytic_recovery. Credit @CubeJerry, the cited native
and feedback predecessors, root's reset construction and OpenAI assistance.
