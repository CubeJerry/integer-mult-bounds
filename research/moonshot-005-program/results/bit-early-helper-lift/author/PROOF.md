# Incidence-class meet funnels with early pivot repair

**Constructive interface theorem; independent review pending. No new kappa.**
Concrete native words are constructed separately by Worker A.

## 1. Exact model

Fix any characteristic-two field and positive whole-record width V. The native
has n=111 source lines L_j in an eight-dimensional rational chart space,
receiver facets F_i, and independent original records X_j=x_j and Y_j=y_j.
Original X moves upward from L_j to Hub, Y upward from zero to F_i, and owned
records downward. ADD requires live cocharted records. Chart ranks over Q
are distinct from binary payload-code ranks.

The canonical row is K_i=x_i+sum_{L_j subset F_i}x_j. Its code K has dimension
c=9. The source line is not contained in its own facet. A basis of K must be
physically acquired; naming the row code does not supply a source.

For a nonempty selected receiver set I, q=|I|, define

    S_j={i in I : L_j subset F_i}, J_S={j:S_j=S},
    r_S=rank_Q(normals i in S), r=rank_Q(normals i in I),
    C_S=intersection_{i in S}F_i, M=intersection_{i in I}F_i.

Thus dim(M)=8-r and dim(C_S)=8-r_S. For each nonempty singleton class J_{i},
choose one original pivot p_i. Let k count these classes and let p be the
canonical evaluation rank on the k pivot roots. Put Delta=k-p. Mixed classes
are nonempty J_S with |S|>=2; let m count them. For a nonempty class, r_S<=7
because every L_j in the class is contained in C_S. Omit zero-distance MOVEs
and use [0]=0.

## 2. Cross-chart acquisition and restoration

For each mixed class S, initialize one owned A_S at C_S. Every X_j in J_S
follows L_j -> C_S -> Hub, contributes once to A_S, and is unchanged. After
all captures, A_S holds sum_{j in J_S}x_j and descends C_S -> M. Since M is
contained in C_S this is a legitimate downward path. Incomparable acquisition
charts do not create an access fiction: the caches actually meet at M.

For singleton J_i, move every original to F_i and add each nonpivot once into
X_{p_i}. Keep that pivot at F_i; all other members proceed to Hub. Its value
is d_i=sum_{j in J_i}x_j. Empty-incidence originals move directly to Hub.
The resulting source map on all original X records is invertible, with actual
cut H direct-sum D: H is the Hub row space and D the k held pivot coordinates.
The inverse column of d_i is exactly the original coordinate x_{p_i}, so the
held projection of K has rank p. Each pivot marginal has rank one since the
native canonical evaluation column is nonzero.

Before these operations, capture Delta selected pivot originals at their
actual initial lines into owned records and descend them to zero. Section 3
constructs the precise canonical source from these early helpers and the
actual late held pivots. All source operations occur once; no reset is assumed.

Once the canonical basis is at ground, each selected Y_i reads K_i there,
ascends to M, reads each A_S with i in S, ascends to F_i, and reads d_i if its
singleton class is nonempty. Its value is exactly

    y_i+K_i+sum_{S contains i}sum_{j in J_S}x_j = y_i+x_i.

Unselected receivers move to their facets unchanged. Every held pivot moves
F_i -> Hub, where adding all other members of its singleton class again
restores it. Mixed captures never altered X. Retire every owned field, retaining
the programme's explicit owned-erasure premise for dirty retirements.

This constructs the partial direct-sum endpoint for I. It is a complete native
only when I contains all111 roles. The fixed finite binary word tensors with
I_V for every positive width; it uses neither masked lanes nor a scalar oracle.

## 3. Source-aware early lift theorem

At an invertible actual cut H direct-sum D, let desired K have dimension c,
held image P of dimension p, and D'=direct-sum_a pi_a(P). Choose a chart-supported
basis B of D'. Choose Delta members E of B whose classes form a basis of D'/P.
Then D'=P direct-sum span(E). Suppose an actual earlier source has delivered
to ground fields Q(e), e in E, with held projection e. Their Hub components
may be nonzero, but must be paid for in the principal seeds.

Choose a lift L:P->H for K, modulo K intersection H. For b in B outside E,
write b=p_b+e_b. Seed a principal field with actual Hub value

    L(p_b)+pi_H Q(e_b),

query b at its one held chart, then at ground subtract Q(e_b). The resulting
value is L(p_b)+p_b. Along with a Hub-only basis of K intersection H these
are exactly c independent canonical fields. There are Delta early helpers.
Their independent classes modulo K prove that the first-arrival span is
c+Delta. This changes helper routes, not the old arrival-span theorem or peak
storage, full history, or retirement costs.

For the singleton pivot above, use Q(e_i)=x_{p_i}, acquired at L_{p_i}. In the
late coordinates,

    x_{p_i}=d_i+sum_{j in J_i minus {p_i}}x_j.

The second summand is an actual Hub combination. Gaussian elimination on P
selects E. Exactly p principal fields query held facets, taking Hub -> F_i ->
zero; c-p fields descend directly from Hub; Delta early helpers descend from
their native lines. All early copies, adjusted Hub reads, late pivot reads
and ground corrections are real emitted ADDs.

The movement module is therefore

    (c-p)[8]+p[7]+k[1].

The late-held-chart module would be (c-p)[8]+k[7]+p[1]. Its extra cost is
Delta*([7]-[1]). Earlier source access changes that premise; it does not
contradict fixed-cut optimality or make any noncanonical helper canonical.

## 4. Full partial-word invoice

Write [a]=a^t for 0<t<1. Let n_0=|J_empty| and n_1 be the number of originals
in singleton classes. The entire constructed word has movement

    Q_I = n_0[7]+n_1([6]+[1])
        + sum_mixed_S |J_S|([7-r_S]+[r_S])
        + sum_mixed_S [r-r_S]
        + (111-q)[7]+q([8-r]+[r-1])
        + (9-p)[8]+p[7]+k[1].

The source terms include held pivots' eventual returns to Hub. The next term
counts actual cache descent. Both completed and unfinished Y movements are
included. The final terms are the proved early-helper canonical module. For
b separately paid copies all source/native/caller terms scale by b.

There are m+9+Delta owner lifetimes. ADDs comprise mixed captures; n_1-k
singleton aggregations and the same number of inverses; Delta early reads;
actual Hub seeds; p late queries; actual ground helper repairs; actual
canonical preloads; sum_mixed |S| cache deliveries; and k singleton deliveries.
Concrete words must give exact read lists and integer totals. Favorable
movement is not complete ordinary/precision/compiler/recursive admission.

## 5. Canonical quotient can remove a real cache

More generally retain any subset B of mixed cache classes. An exact sufficient
and necessary algebraic condition for the unchanged funnel delivery interface
is, for each i in I,

    e_i in K + span{z_S:S in B} + span{d_i},
    z_S=sum_{j in J_S}e_j,

with d_i=0 if no singleton class exists. The condition means a new ground
canonical preload, arbitrary actual retained-cache reads at M, and an optional
singleton read at F_i exist. Sufficiency follows by emitting those linear
coefficients. Necessity follows because these are all permitted X-bearing
sources on Y_i's unchanged route. Source originals in dropped mixed classes
can go directly to Hub. This criterion alone is not a new source word; actual
canonical availability and the unchanged cut must still be checked.

For the fixed A3 six-set I={1,3,73,76,77,80}, the four triangle classes obey
the exact native binary relation

    z_{3,76,80}+z_{3,73,77}+z_{1,76,77}+z_{1,73,80}
      =K_1+K_3=K_73+K_76=K_77+K_80.

The relation has58-root support. It is checked directly on all111 columns,
hence holds at every width and characteristic-two field. Any ONE triangle
cache can be omitted. Each receiver in that omitted triangle changes its
canonical preload by K_1+K_3 and toggles its reads of the three remaining
triangle caches. Other source values and exact endpoints are unchanged.

An omitted triangle of size a has r_S=2 while r=3, so its exact saving is

    [1]+a([5]+[2]-[7]).

Two triangle cohorts have a=16, providing the largest such saving within this
fixed four-choice deletion. Exhaustive subset linear algebra finds7 of8
mixed caches necessary and sufficient in the stated cache-subset interface;
the four-receiver set {0,3,76,80} requires all5 of its mixed caches. These are
exact finite-source classifications, not universal lower bounds on all coding.

## 6. Complete flat-funnel obstruction and next direction

For all111 receivers the native has111 distinct incidence classes, each source
facet intersection is exactly its own source line, and there are no singleton
classes. The literal construction has M=zero and

    Q_literal=222[7]+111[1]+9[8].

These geometric statements are checked from the pinned finite native table.
Even a more generous flat-ground continuation fails. Suppose all X originals
reach Hub before Y moves, and every later X-dependent contribution to Y is
obtained from information delivered at ground. There is no new proper-chart
source or retained original after this cut. All111 endpoints require111
independent X directions in the joint actual ground-arrival span. Each
source-bearing record-width arrival costs at least one positive integer-rank
MOVE, hence at least [1]. Every original X and Y trajectory costs at least
[7], by sum a_j^t >= (sum a_j)^t. Thus

    Q_flat >= 222[7]+111[1].

This even allows the canonical bank to be omitted, arbitrary earlier LINEAR
source coding in the declared field/whole-record model, and owner reuse. The
rank argument makes no claim about arbitrary nonlinear encodings. The
inequality exceeds the exact retained B_infinity at
t=199/200. It is a scoped no-go for the all-information-at-ground continuation,
not a lower bound for general multiplication or new proper-chart deliveries.

A scalable extension must deliver receiver information above ground, retain
originals through successive proper cuts, or introduce joint histories outside
this premise. Hierarchical funnels are a concrete next question: hold caches
at receiver-subset meets, let Y read nested meets, and move only paid residual
combinations across incompatible branches. No complete hierarchy is claimed.

### Economic control: interface novelty is not a partial-price improvement

A simpler one-copy partial word captures q selected input originals directly
at their native lines into q owned point helpers, descends each helper to
ground, copies x_i into its selected Y_i, and sends every original to its
usual endpoint. Even retaining an otherwise unused complete canonical bank,
its movement is `222[7]+9[8]+q[1]`. This control is cheaper than the current
four- and six-receiver funnel examples. Omitting that unneeded bank makes the
control cheaper still, while changing its downstream interface.

The new contribution is actual cross-chart shared acquisition, early repair
of a nonseparable held projection, and a reusable canonical cache relation.
It is not a lower partial price or a complete supplier advance. More completed
receiver counts alone are not an adequate reason to extend an uneconomical
flat funnel. A subsequent hierarchy must demonstrate shared information above
ground and a complete invoice that survives this direct-point control.

## 7. Verification and provenance

Baseline4743ad65eff2ce1a63bf8572e4e2bf0751b0426d. Native table:
research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json,
SHA2568cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e.
The checker independently reconstructs finite source incidence/ranks, early
lift controls, exact cache-subset classification and directed budget intervals.
Universal scope is justified by the written proofs, not the finite checks.
Worker A's separate word requires independent full-column/route replay.

Credit @CubeJerry, Worker C's incidence-funnel/source-aware bridge and canonical
cache-quotient identity, Worker A's independent funnel construction and early
point repair realization, retained canonical/MDS/query-repair predecessors;
OpenAI assistance. All five foundations and strict supplier/outer obligations
remain. **No new kappa.**
