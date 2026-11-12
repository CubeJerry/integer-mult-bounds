# Independent review of the actual four-contact reciprocal star

**Pass in its stated finite-source scope. No new κ.** The reviewer independently
reconstructed the complete77,814-instruction word from the frozen parent and
source geometry. It did not import or execute `build_feedback_star.py`, its
verifier, or the retained parent interpreter. The separate `engine.py` replays
all1880 original input columns at the common-entry boundary and type-walks the
entire source word. The original author and predecessor credit are unchanged.

## Exact object reviewed

Source compressed SHA256:
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Parent paired-word compressed SHA256:
`bd5c598c9ac30bffdcdd85a4cb059376ceb83846144fa9cfa28a347a9ea2ef17`.
Star compressed SHA256:
`a312df6c1ea30b8779dbf9f77ceccf2734aa73703f3cccffd7804a5661e5efd7`.
Star decompressed payload SHA256:
`02b86b2096a7b9ebbf4529821e7675e94101019efd1cde0634fd32435b9c318e`.
The exact builder pin and independent receipts are in REVIEW.json.

## Mathematical review

The eight source-frame roots B form an orthonormal basis in the rational
nine-coordinate zero-sum representation, after dividing their inner products
by2. This review derives their products using that Q^9 representation, rather
than the author's integer-eight-coordinate formula. Receiver t=0 has four
contacts c=(+1/2,-1/2,-1/2,+1/2) on roles5,56,69,100. In particular c^T c=1.
Every involved first-X and X2/Y2 role is genuinely hosted and independent;
none is one of the eight coupled aliases.

Order the96 hosted reverse coordinates as the8 frame entries B followed by
K, the88 others. Direct extraction from independently interpreted parent rows
verifies its complete residual matrix is

    D_old = [[I8, 0], [C, I88]],       C_(h,b)=<r_h,r_b>/2.

The new word supplies only the four reverse entries from d_t into the frame
X2 carriers. Its residual is

    D_new = [[I8, c e_t^T], [C, I88]].

Block elimination gives Schur complement S=I88-(C c)e_t^T. Its vector
u=Cc satisfies e_t^T u=c^T c=1, so S is a rank87 projection: its kernel is
exactly span(u), and it fixes the87-dimensional kernel of e_t^T. Therefore
rank(D_new)=8+87=95. An exact right-kernel vector is (-c,u). The review extracts
and checks every coefficient of this vector against the96 actual source rows.
It does not infer a physical low-rank return implementation from the algebra.
Each residual diagonal remains1; no new complete reverse pair is claimed.

The new forward correction subtracts the four specified basis terms at raw
receiver112. It cancels four inherited residual coefficients. The frame first-X
carriers remain unchanged. The reverse changes are additions of unchanged d_t
to four X2 fields, and the first-Y change is a combination of preserved frame
inputs. These give an explicit algebraic inverse on the true input fields.
This inverse establishes information preservation; it grants no free local
access to separated final values and no physical reverse execution.

## Source and ownership review

All nine rerouted carriers have exactly one original direct source ascent in
the parent, and that ascent is in the prefix. Four first-X and four independent
X2 carriers each replace their rank8 route by real rank7 and rank1 legs through
the actual receiver facet. The ninth carrier d_t retains its original empty-
chart-to-facet route and is only retimed. Original routes are consumed once.
All eight nonzero donors have the required exact binary subspace containment.
The receiver's actual facet arrival determines consumption of the stationary
collector; its INIT, one lifetime, use and CLEAR are all present.

The independent prefix replay finds precisely the declared five changed rows:
receiver112 and four hosted X2 fields. Every other live field, including every
common input and surviving owned record, matches the parent. Every changed row
has no later use except its prescribed final common recoupling. The common
suffix is literally unchanged, so the admitted parent's arbitrary-input common
restoration result composes. All final source charts and the full typed owner
lifecycle agree. Peak owned storage remains43.

There are four newly introduced distinct ordered chart maps, even though eight
raw paths are split: some pairs coincide or already existed in the parent.
All four have exact recipes verified using the pinned Clifford lowering and
separately implemented signed-Pauli/global-phase engine. An altered global phase
is rejected. This uses established source engines; it is not a new universal
physical compiler proof.

## Complete price and adversarial controls

The independently counted increment is8 MOVE,9 ADD,1 INIT and1 CLEAR. The raw
histogram change is +8 rank1,+8 rank7,-8 rank8, hence constant rank mass and
added moment8(1+7^t-8^t). Adding18 copies of the exact raw delta to the parent's
complete caller histogram agrees with the author's P_partial. All eight rank9
packets remain charged. Independent integer-root bounds at denominator2^120
agree with the decimal-denominator certificate and place the remaining
per-native moment at40.897367207217805... for t=199/200.

Deleting one feedback contact makes the actual96-by96 residual full rank96;
its reduced scalar is1/4. Adding a second nonorthogonal feedback receiver also
makes the actual residual rank96; the two-dimensional Schur determinant is
-1/4. These are exact matrix negative controls, not only unchecked scalar
claims. They show that arbitrary additional stars need not monotonically
reduce residual rank. Orthogonal completion and changed global schedules are
separate constructions requiring their own source and price verification.

## Reproduction

Run:

    python3 -I -B check_star.py --repo REPO --author STAR_PACKAGE --output OUT

`STAR_PACKAGE` contains build_feedback_star.py and output/WORD.json.gz plus its
RESULT.json. The expected terminal result is
`PASS_INDEPENDENT_FEEDBACK_STAR_REVIEW 77814 instructions; 4 new maps; rank 95`.
The proof, independently reconstructed source identity, tariff and meaningful
negative controls support the finite result. Every supplier, recursive,
precision, compiler, owned-erasure and foundational obligation remains.
