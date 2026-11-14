# Reversible cut redundancy and masked receiver histories

**Author theorem and exact source premises; independent review pending. No
new kappa.** This package studies simultaneous use of correlated local forms
without losing any original input. It gives a universal linear cut theorem,
an exact obstruction to acquiring all eight coordinate local forms by pure
ascending histories, and a concrete change of representation that escapes
that obstruction. It does not construct a complete eight-packet source.

The native input is
`research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz`,
SHA256 `51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
Source geometry and binary row identities below are rebuilt directly from
these bytes. All geometric subspaces are real; value arithmetic in the
applications is over an arbitrary characteristic-two field.

## 1. General reversible cut theorem

Let a finite chronological linear computation over a field F have independent
inside-born input vector u in F^N and independent outside-born input vector v.
Partition the computation into an inside region and its outside. Every
transfer from inside to outside carries an actual linear signal; concatenate
these signals, in chronological order, into

    z = A u + B v in F^M.

M counts the complete dimensions of all outward transfers, including repeated
crossings and dependent, partially ranked, or identically zero signals. All
independent input born inside is included in u, including arbitrary inputs
initially at a ground chart. Zero-born storage introduces no independent
input. Every outside final public output must be generated from actual
transfers and outside-born inputs. Assume their prescribed joint dependence
on u has column rank N. This is the input-preservation hypothesis; an
invertible endpoint with all original values recoverable is sufficient.

Suppose there are k recipient demand subspaces D_i of the u coefficient
space F^{1 by N}. For each i, all rows in D_i belong to the rowspace of A
restricted to some set I_i of outward scalar-coordinate rows, and the I_i
are pairwise disjoint. The demands may be attained at different times;
simultaneous coexistence is not required. Then

    M - N >= delta(D_1,...,D_k)
            := sum_i dim D_i - dim(D_1+...+D_k).                 (1)

This permits arbitrary outside-to-inside feedback, late outward transfers,
rank-deficient block operations, and unknown v offsets. The disjoint-row
demand condition must still hold for the ACTUAL acquired histories. Granting
an uncounted outside read or allowing a history from one recipient arm to
reach another may invalidate that condition.

### Proof of full cut rank

Open every outward transfer, treating each complete z coordinate as an
independent formal argument. A chronological induction expresses every
outside history, and hence every final outside output, as a linear function
of z and v. An outside-to-inside transfer can affect a later z; this causes
no problem because the later actual z is already one of the opened arguments.
There is no cyclic evaluation: the original execution is finite and causal.
Thus the prescribed output matrix on u factors through A. Its rank is N,
so rank A=N. In particular dim ker(A^T)=M-N. Setting the independent v to
zero for this coefficient argument does not delete its physical carriers or
assume that unknown original Y values vanish during execution.

### Proof of the redundancy bound

For each i choose a linear section taking every d in D_i to a coefficient
vector s_i(d) supported on I_i, with s_i(d) A=d. Such a section exists because
D_i is contained in the indicated rowspace. The space

    R = {(d_1,...,d_k): d_i in D_i, sum_i d_i=0}

has dimension delta. The map R -> ker(A^T) given by the sum of the s_i(d_i)
is injective: disjoint supports imply that a zero sum makes every s_i(d_i)
zero, and hence every d_i zero. Therefore delta <= M-N. This also proves the
bound for arbitrary noncommuting block coefficients after expanding each
whole record into its F coordinates. No full-rank transfer assumption is
used. If all physical records have width V and the baseline has N/V whole
records, at least ceil(delta/V) additional outward records are necessary.

### Exact attainment in an abstract common-chart model

The number delta is sharp when all N inputs may first be linearly encoded
at one common chart and the encoded carriers can use separate recipient
arms and later reunite. Take bases of every D_i, giving sum dim D_i rows of
joint rank d=dim sum D_i, and append N-d rows completing a basis of the input
dual. The resulting (N+delta)-by-N matrix has column rank N. Extend its N
columns to an invertible square matrix and apply this matrix to the N inputs
and delta zero ancillas. Route each demand's rows along its own arm, deposit
the requested values, then reunite all carriers and apply the inverse. The
originals return and all extra carriers are zero. Whole-width implementations
may pad the extra scalar dimensions to complete records.

This is an information-theoretic construction, not a geometry or cost
compiler. It does not assert that the actual BIT roots can reach such an
encoder, that the requested arms exist, or that ordinary work, storage,
restoration, and physical transforms are cheap.

## 2. Geometric conditions giving disjoint arms

Use a downset D of actual chart subspaces: if C belongs to D and C' is a
subspace of C, then C' belongs to D. Original X and Y physical carriers
ascend; persistent packets descend. A descending packet crosses this cut
only inward and cannot supply an outward transfer. Stationary caches start
at zero. Count every extra ascending carrier and every other outward
transfer. Labels do not substitute for following actual carriers.

A demand at facet F is called boundary-local for this cut if its dependence
on inside-born inputs uses only outward transfers whose first outside chart
is contained in F, followed by cochart operations and ascending paths inside
F. This is a sufficient causal condition for its u rowspace to be contained
in the corresponding rows of A. A history with entirely ascending ancestors
satisfies it. Outside-born inputs may contribute arbitrary offsets; these
have zero u coefficient.

In particular, the definition excludes receiving a later result mixed at
Hub, a descending packet reaching F directly from outside D, a lateral
transfer from a different arm, or a nonlocal preloaded cache. Those are
legitimate changed constructions if actually implemented and charged, but
the following pure acquisition corollaries cannot be applied to them. A
descending history that first enters D and then exits through a counted
outward channel is already included in A and does not evade (1).

For two distinct facets F0,F1, let C=F0 intersect F1 and D={C':C' subset C}.
No first outside chart can be contained in both facets, so their eligible
outward-row sets are disjoint. More generally, let D consist of all charts
of dimension at most six. An outside chart contained in a seven-facet is
that facet itself, so all distinct seven-facets have disjoint eligible sets.
These statements cover arbitrary actual real charts, not only named
predecessor IDs or coordinate flags.

## 3. Exact pair and eight-form consequences

For native coordinate indices i=0,...,7, let F_i be its actual terminal
facet, u0=x0+...+x7, K_i the canonical binary fitting row, and

    L_i = K_i + u0.

The preceding programme classified these as the eight nonclass proper
local forms in W0. The present checker independently verifies their actual
supports and ranks; the classification itself is not reproved or promoted
to a stronger statement here.

### Two pure forms require an extra crossing

Take C=F0 intersect F1=span(e2,...,e7). There are28 original X root lines
inside C, including six coordinate lines and22 noncoordinate lines. All111
arbitrary original Y inputs are born at zero inside D. The139 inside-born
original carriers all have final public charts outside D, and each crosses
outward once on an ascending path. If all original X are restored and each
Y is either unchanged or receives a fixed X-linear correction, the endpoint
is injective on all139V inside input coordinates.

Both L0 and L1 restrict on these inputs to the SAME nonzero sum of the22
common noncoordinate x inputs, with zero coefficient on every original y.
For boundary-local pure acquisitions at F0 and F1, D0=D1 has dimension V,
so (1) forces at least V extra outward capacity, or one extra whole-V
crossing. Arbitrary original Y histories cannot be omitted from N when
making this argument. Later outside mixing cannot justify treating the
acquisitions as boundary-local.

The independently developed joint local acquisition word of Worker A is a
matching source-specific upper construction: one additional owned carrier
crosses C->F1 with the common sum, while the original common carrier serves
F0. Every original is restored and the pair is used to complete Y0,Y1. Its
literal word and invoice are a separate package and review obligation; the
cut theorem does not depend on execution of its author checker.

### All eight pure forms require at least four extra crossings

Now use the downset of all charts of dimension at most six. All222 original
X and Y inputs are born inside; all222 final public charts are outside.
Their original monotone paths provide exactly222 whole-V outward crossings.
Pure boundary-local L_i acquisitions at the eight distinct coordinate
facets have disjoint eligible outward rows. Each L_i has rank V, while
the eight binary rows jointly have exact rank4. Binary matrix rank is
unchanged under extension to any characteristic-two field. Thus

    delta(L0 tensor I_V,...,L7 tensor I_V)=8V-4V=4V,

and at least FOUR additional whole-V outward crossings are necessary, even
if the eight pure forms are acquired at different times and consumed
immediately. Each additional crossing requires a positive-rank MOVE in the
stated route model. The independently admitted strict q8 unit-profile
envelope permits at most three extra unit MOVEs at every finite fixed even
multiplicity for k in [.005,.005006]. That specific plan therefore exceeds
its movement envelope before ordinary, storage, and owned costs are added.

This does NOT prove that all eight L_i are necessary for a successful source,
that one must use W0, or that mixed Y histories obey the same redundancy.
The parent programme's new W_c first-entry obstruction is a separate,
stronger result for histories confined to those codes; (1) applies more
generally to any correlated demands meeting its cut hypotheses.

## 4. A changed representation removes the pure-demand obstruction

Let C_i=u0+x_i be the other seven coordinate inputs and define

    H_i=L_i+C_i=K_i+x_i.

Every original-X term in H_i belongs to F_i. Suppose an actual ascending
original Y reaches F_i with value Y_in=y_i+H_i, and a genuine packet arrives
with P_in=K_i. Execute the credited two-ADD receiver exchange:

    Y += P;
    P += Y.

Then Y_out=y_i+x_i is the required public output and
P_out=Y_in=y_i+H_i. Treating the arriving boundary values independently,
P_out depends on Y_in only, so the packet-through block is zero. This is an
invertible two-register transformation; it neither clears unknown y nor
requires a second original y copy. The actual incoming K_i must remain in
the historical kernel coordinates, and the outgoing masked history is not
silently declared pure X. Later processing and final erasure of this packet
remain physical obligations.

This exchange identity and the usefulness of an arbitrary-Y mask were
already exhibited in `bit-y-feedback-normalization/review-b/REVIEW.md` on a
two-target line example. The new point here is its relation to correlated
facet-local L_i demands and their charged acquisition obstruction. The
eight masked demands y_i+H_i are independent because their y_i coefficients
are independent; their cut redundancy is zero. Equation (1) therefore
does not force any extra outward crossing. This is a precise escape from
the pure-demand premise, not a proof of joint physical acquisition.

For the pair, the22-common-input sum can in principle be read by BOTH
original Y0,Y1 while they are at C=span(e2,...,e7), before their paths split.
This suggests a route using their authentic unknown-y records instead of
copying the pure sum into an extra outward record. Worker A is separately
constructing and verifying that literal chronology. No word is inferred
merely from the cut rank being favorable.

## 5. The first masked design still needs new historical directions

The exact source rows satisfy

    rank<K0,...,K7>=4,
    rank<H0,...,H7>=8,
    rank<K0,...,K7,H0,...,H7>=12.

Thus an idealised one-exchange-per-coordinate-packet history has x-space
W_mix of dimension12V, not the old W0 of dimension16V. For a pair the
corresponding historical x-space has dimension4V. This rank statement
assumes no other proper-cell historical coordinates have been introduced.

W_mix admits fitting rows at exactly the eight coordinate ports. For every
noncoordinate port j the checker supplies another actual port j' with the
same four-coordinate real support but nonzero root inner product. Every
coordinate K_i, hence every row of W_mix, has equal coefficients at j,j';
coordinate unit rows are zero at both. Yet a fitting row for receiver j
requires coefficient I at j and zero at the noncontact j'. This is
impossible over every characteristic-two field and every whole width V,
even with arbitrary operator coefficients in W_mix tensor F^V. The
103 explicit pairs certify all remaining native ports.

Consequently, merely acquiring these eight masked forms and running one
exchange on each packet cannot complete the other103 receivers. A viable
continuation must change the packet sources, add genuine lower-chart
history directions through further exchanges, or use another representation.
The masked histories preserve the promising singular-transfer mechanism
while exposing the exact next need: sign-sensitive information within the
four-coordinate support classes.

## 6. Verification and scope

`verify.py` authenticates the native bytes; reconstructs the real lines,
actual facets and canonical contact rows; checks the28/22 pair counts, all
eight proper supports, rank4, rank12, and all103 separating noncontact
pairs. It independently checks the abstract redundancy inequality on
finite field examples with arbitrary scalar row groups, a sharp duplicate
demand example, an invertible-matrix control, and arbitrary-Y two-ADD
exchange identities. Controls reject omitted Y columns, a false claim of
disjoint arms, a dropped source column, a zero-Y substitution, a missing
second exchange ADD, and altered native bytes. Finite tests do not replace
the all-field proof of (1), the cut-opening induction, or the geometric
causality argument.

Dependencies retain the native geometry, the existing W0/local-code
interpretation, the admitted arbitrary-Y historical normalization, and
the separately proved strict unit-profile envelope. All five foundations,
the complete source/compiler and both strict supplier requirements remain.
No new complete multiplication exponent is claimed.

Credit Worker A for the original two-facet cut conjecture and matching pure
pair construction; retain the original BIT/E8 geometry authors and the
prior arbitrary-Y exchange/normalization authors. The general redundancy
argument is elementary linear algebra, with no assertion of literature
priority. The contribution is its source-bound reversible routing use,
the four-extra-crossing consequence, and the explicit changed-history
boundary. Prepared for @CubeJerry with substantial OpenAI assistance.
