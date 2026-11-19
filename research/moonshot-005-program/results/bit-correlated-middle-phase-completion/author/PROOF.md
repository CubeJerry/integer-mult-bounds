# Paid phase completion with correlated proper early and late values

**Proved local interface extension, conditional on its supplied row spaces.
No complete supplier and no new kappa.** This extends S027's
`bit-paid-middle-phase-completion`, whose proper inputs were assumed to range
over a full product. The actual early owners remain independent. The proper
contributions on incoming late Y owners may be correlated with them and with
one another. Arbitrary original Y baselines remain independent physical
inputs and are preserved by a bijective late phase.

## 1. Fixed interface and quantifiers

Let F be a finite field and let x range over F^b. Fix matrices
E:F^b->F^nE of rank nE and V:F^b->F^nL. The genuine early X owners have
values u=Ex. On the proper slice the genuine incoming late Y owners have
values v=Vx; on arbitrary inputs they have values y+Vx, with y arbitrary.
There are s genuine X closures and exactly s genuine Y births, so

    aE=nE-s,       aL=nL+s,       0<=s<=nE.

The early phase is a bijection on its nE actual X owners. Its aE continuing
slots are observable messages and its s remaining slots use the actual
closure routes. The late phase can read a paid retained snapshot of u and
is a bijection on all aL actual incoming/born Y owners for every fixed u.
Born Y values are zero only on the proper slice, not on arbitrary inputs.
No outside source information is available at this local step.

Each receiver i observes a specified subset A_i of the continuing early
and late slots and must recover T_i x, where rank T_i=|A_i|. Assume
row(T_i) is contained in R=row[E;V]. There is no uncharged receiver side
information in this statement. Let d be the maximum number of receivers
seeing any one slot. Put

    W=row E,  rho=dim R-nE,
    pi:R -> R/W,
    Q_a=W intersect (intersection of row T_i over audiences i), early a;
    Q_a=R intersect (intersection of row T_i over audiences i), late a.

For an empty audience the intersection is R. Thus Q_a<=R always.
The quantity rho, between zero and nL, is the rank of V restricted to
ker E. It counts fresh proper late information, not actual late owners.

## 2. The exact three conditions

The following are necessary even for arbitrary deterministic nonlinear
encoders obeying the stated phase bijections and exact saturated targets:

H: For each receiver i and S subset A_i,
   dim(sum_(a in S) Q_a) >= |S|.

E: For each subset S of continuing early slots,
   dim(sum_(a in S) Q_a) >= |S|.

L: For each subset S of late slots,
   dim(sum_(a in S) pi Q_a) + (nL-rho) + s >= |S|.

Conversely, if these three conditions hold and |F|>d+1, one simultaneous
linear assignment meets all targets and both phase bijections. It uses
exactly the genuine owners, closures, births and movements in the stated
interface, together with the charged stationary early snapshot below.
The field-size condition is sufficient; it is not claimed necessary.

The new allowance nL-rho comes from dependencies of proper late values
modulo early information. It is not an additional birth, a discarded Y
baseline, or a free source dimension. If (u,v) ranges over a full product,
rho=nL and this is exactly the previously proved condition.

## 3. Necessity, including nonlinear codes

A saturated receiver tuple has exactly |F|^rank(T_i) possible values and
recovers every T_i x, so it is a bijective relabeling of that target. A
slot shared by several receivers is therefore a common function of their
linear targets and of its available linear input. Translation by each
observation kernel leaves the slot unchanged; hence it factors through
the intersection Q_a of the corresponding row spaces. This is the
previously proved saturated common-information argument.

Every subtuple of a saturated receiver has its full product range. This
proves H. Since E has full row rank and the complete early map is a
bijection, every subtuple of its continuing outputs has its full product
range on x. This proves E.

For L, set Ex=0. The proper incoming late values Vx range over a linear
space of dimension rho inside F^nL. Together with born Y=0 they give
|F|^rho inputs to the actual late bijection. Its outputs remain distinct.
Projection onto a subset S has fibres of size at most
|F|^(aL-|S|), so the projected proper range has size at least
|F|^(rho-aL+|S|). Its entries are functions of Q_a restricted to ker E.
The row space of those restrictions has dimension
dim(sum_(a in S) pi Q_a), since restriction kills exactly W in R.
Comparing range sizes proves L. If its right-hand bound is nonpositive,
the same inequality is simply vacuous. This proof does not linearize the
encoders or assume independent proper late values.

## 4. Lifting proper rows to independent Y-baseline rows

Define tau:F^nL -> R/W by tau(beta)=pi(beta V). It is surjective and
dim ker tau=nL-rho. A desired proper row q in Q_a can be written

    q=alpha E+beta V.

The possible beta vectors, as q ranges over Q_a, are exactly
P_a=tau^(-1)(pi Q_a). Indeed membership means beta V differs from a row
of Q_a by a row of E, and the full row rank of E supplies alpha.
For every nonempty set S,

    sum_(a in S) P_a = tau^(-1)(sum_(a in S) pi Q_a),
    dim(sum_(a in S) P_a)=nL-rho+dim(sum_(a in S) pi Q_a).

The first identity follows by choosing preimages of each summand and
putting the residual kernel vector into any one nonempty summand. The
empty set is handled separately and requires no such identity.

The s genuine born-Y coefficients gamma are unrestricted. Consequently
the allowed pure-late row space for slot a is P_a direct-sum F^s.
The independent-representatives criterion for an invertible aL-by-aL
pure-late matrix is precisely L for every nonempty subset. This is the
physical significance of the dependency allowance.

## 5. Simultaneous construction and field size

For each early slot choose independent variables for a row q_a in Q_a.
For each late slot use independent coordinates in the linear space of
pairs (alpha,beta) satisfying alpha E+beta V in Q_a, and free gamma
coordinates on the born-Y columns. Each desired q_a has such a lift.
Also give each genuine early closure an arbitrary row of W.

H and linear independent representatives show that each receiver
determinant is a nonzero polynomial. E gives independent continuing
early rows, which extend by the s free closure rows to a nonsingular
nE-by-nE early matrix. The preceding lifting lemma and L make the
aL-by-aL pure-late determinant a nonzero polynomial.

Multiply these polynomials. Every slot variable occurs linearly in at
most d receiver determinants and in one phase determinant. Closure and
born-Y variables have no higher individual degree. Thus the product is
nonzero and every variable has degree at most d+1. A polynomial with
individual degrees less than |F| cannot vanish on all of F^N: induction
on N, using the univariate root bound, proves this finite-grid fact.
Therefore |F|>d+1 supplies a simultaneous assignment.

Retain u before applying the early invertible map. Apply the constructed
pure-late matrix to the actual vector (y+Vx,y_born), then add alpha u
from the snapshot. On the proper slice its values are q_a x. On arbitrary
Y inputs its linear Y coefficient matrix is invertible. The dependence
between E and V does not modify or remove any actual Y baseline.

## 6. Fully paid finite binary invoice

For F=GF(2^w), put M=w*nE and N=w*aL and expand in a fixed binary basis.
The identical local invoice from the full-product theorem applies:

    ADD <= 2(M^2+3M)+2(N^2+3N)+MN+M;
    INIT = charged dirty CLEAR = M;
    extra stationary owned peak = M; additional MOVE = 0.

It includes the snapshot, dense cross additions, the invertible early
and late maps, and their assigned Hub/ground inverses. Those inverse
placements remain conditional on the retained whole-word restoration
and preload composition. This is one local bill, not the full supplier.
Actual births and closures are the public originals already present.
The choice of row spaces and a uniform coefficient selector still need
their own construction; nothing here makes selection or field arithmetic
free. For native audience d<=3, GF16 or GF32 satisfies the size condition.

## 7. Separating examples and limits

Let nE=2,s=0,nL=1, E x=(x1,x2), Vx=x1. Keep both early fields and ask a
separate one-slot late receiver for x2. Here rho=0. The allowed proper
late row Q=span(x2) has zero image in R/W, but L holds because nL-rho=1.
The actual incoming Y is z+x1; adding cached x1+x2 gives z+x2. Its
pure-Y map is the identity on every arbitrary z. The old full-product
formula would reject this correlated interface if applied without its
premise. We do not describe that premise violation as a flaw in the old
theorem.

Change Vx to an independent x3 while keeping the target x2 and s=0.
Then rho=1, L fails, and no invertible one-Y map can give a proper message
depending only on x2. A genuine birth s=1 can absorb one such lost proper
dimension, but it also changes the actual early/late owner counts and
must be supplied by the atlas. Conditioning on x is not permission to
erase arbitrary z.

The theorem does not ensure compatible H input quotients, shared K
delivery, all foreign blocks, a low value of rank(I+B), the strict BIT or
complex supplier, or complete recursive accounting. It removes a false
independence restriction when testing an actual local proper boundary.

## Verification and provenance

`check.py` checks the quotient/preimage identity and exact independent
representative feasibility on finite binary spaces, tests correlated and
independent-boundary controls, and replays the positive proper/arbitrary-Y
word. These finite checks support the displayed all-dimension proof.
Independent review is recorded separately before admission.

Credit @CubeJerry, the native atlas and source-compiler authors, the
balanced-source Rado construction, and S027 Worker B's saturated-message
and full-product paid phase theorems. Root developed this correlated
boundary extension with substantial OpenAI assistance. The five retained
foundations remain explicit and unresolved. No new kappa.
