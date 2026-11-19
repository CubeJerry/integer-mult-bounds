# A noncommuting covariant source with every native view and the actual early phase

**Proved source-existence theorem from exact finite certificates. Physical
source compilation retains the existing compiler and erasure assumptions.
Shared H/D/K transport and a complete supplier are open. No new kappa.**

The previous arbitrary-row two-evaluation source theorem did not imply
that a locally Clifford-covariant source exists. This package establishes
that missing source property in a 64-parameter family per donor-plane
incidence. It uses one exact foreign-view witness, an explicit complete
orthogonal-pair orbit, 111 exact early-phase witnesses, and a simultaneous
polynomial argument. The witnesses are not a claim that a random finite
experiment proves an asymptotic multiplication bound.

## 1. Source family and theorem

Use the pinned binary Clifford representation on S=F^16 of the native
eight-dimensional quadratic space. For an A2 plane H, let A_H=Cl(H)
inside End(S); it is a copy of M_2(F). Its commuting algebra is M_8(F).
The source bank for the basic construction is End(S), dimension 256.

For each native donor j and each H containing j, choose independently
four vectors u_(j,H,A) in S, one for every A in a fixed basis of A_H, and
put

    F_(j,H)(X) = sum_(A in basis A_H) A X u_(j,H,A).       (1)

The 64 scalar coefficients of these four vectors are donor-specific.
For every L commuting with A_H,

    F_(j,H)(L X) = L F_(j,H)(X).                         (2)

In particular this holds for L=gamma(i) whenever receiver i is
perpendicular to H. This is a structured family of maps 256 to 16; the
space of all such linear maps would have dimension 4,096.

**Theorem.** Over F=GF(512), one can choose all maps (1), actual early
output frames, and all extra early rows so that:

1. For each of the 6,470 native foreign ordered pairs (i,j), the map
   from X to the sixteen F_(j,H)(X) for H containing j and perpendicular
   to i is invertible from F^256 to F^256.
2. At each of the 111 native donors, the actual normalized early source
   rows form an invertible 256-by-256 map. A type-8 incidence emits eight
   independent rows of its quotient early and its complementary eight
   rows late; a type-16 incidence emits all sixteen early; a type-24
   incidence emits all sixteen quotient rows and eight additional early
   rows. The latter eight are real owned values, not omitted symbols.
3. In the common original matrix-column coordinates, two coefficient
   matrices of one selected source map do not commute. Thus the selected
   family can explicitly avoid the globally commuting coefficient class.
4. Every abstract quotient still satisfies (2). The source output frames
   may depend on the donor and H, and their inverses are explicit finite
   linear maps. No phase-by-phase equivariance is asserted.

The same result repeats on r independent End(S) copies, with source bank
b=256r and quotient width 16r. To fit the literal bank-480 atlas one takes
r=15a, hence b=3840a. At a=1 these are fifteen matrix copies, or 240
spinor copies. Downstream operations may mix those copies; none are
declared free auxiliary inputs.

## 2. Why this is the full covariant family, and why parameters have rank eight

For two roots j,k spanning H, put N=gamma(j)+I and M=gamma(k)+I.
Then N^2=M^2=0 and NM+MN=I. As in the explicit adapted-basis lemma,
choose a basis of im N and append its M-images. This identifies

    S = F^2 tensor F^8,
    N = E_01 tensor I_8,       M = E_10 tensor I_8.

Thus A_H=M_2(F) tensor I_8 and its commutant is I_2 tensor M_8(F).
As a module under that commutant, End(S) is a sum of 32 copies of F^8
and S is a sum of two copies. Its equivariant Hom space has dimension
2 times 32=64. The 64 maps

    X |-> C_ab X e_t,     a,b in {0,1}, 0<=t<16,       (3)

where C_00=NM, C_01=N, C_10=M, C_11=MN, are independent and span that
space. Indeed, after the displayed change of basis, they independently
select one of the 32 input multiplicity coordinates and place it in one
of the two output multiplicity coordinates. Each C_ab has rank eight,
so each coefficient map (3) has rank eight. This statement uses the
ordinary original vector basis e_t; changing the input-column basis is
an invertible scalar reparametrization.

The equivalent partial-trace form used to discover the finite witnesses is

    F(X) = sum_(C in basis A_H) tau_H(C X) v_C,
    tau_H(X) = [gamma(j),[gamma(k),X]].                  (4)

In the adapted basis, tau_H is the two-by-two matrix trace onto the
commuting M_8 algebra: tau_H(X)=I_2 tensor(X_00+X_11). Consequently (4)
is another set of 64 coordinates on the same equivariant Hom space.
Equivalently, expanding the two commutators expresses it directly in
the form (1). The certificate checker reconstructs maps from this latter
expansion and does not trust reported ranks in the discovery log.

## 3. One exact foreign view transports to all native foreign views

The pinned layout contains all 120 nonsingular vectors of the binary
plus quadratic space and all 1,120 anisotropic A2 planes. The checker
verifies that this A2 list is complete: every nonorthogonal pair of
distinct nonsingular vectors has its unique third vector in the listed
plane. No native source is added by using this complete symmetry set.

For every nonsingular vector u, conjugation by gamma(u) sends

    gamma(v) |-> gamma(u) gamma(v) gamma(u)
              = gamma(v + beta(u,v)u).                (5)

The induced binary orthogonal transvection permutes all 120 roots and
all A2 planes. `ORBIT.json.gz` gives a rooted spanning tree, starting at
(5,77), using those 120 transvections. The exact reconstructed orbit
contains all 7,560 ordered orthogonal pairs in the full 120-root geometry.
All 6,470 native foreign pairs are explicitly included. This finite
certificate replaces any need to assume an unproved transitivity theorem.

`PAIR-WITNESS.json` lists the sixteen actual H planes at (5,77) and all
four GF(16) vectors v_C for each H in (4). The field has polynomial
t^4+t+1. Direct expansion of its 256-by-256 map into a 1,024-by-1,024
binary matrix has rank 1,024.

If a product P of the binary gamma(u) matrices carries (i,j) to (i',j'),
it permutes the sixteen visible source planes. It transports a source by

    F'_(j',H')(X) = P F_(j,H)(P^(-1) X P).             (6)

This belongs to the covariant family for H', because conjugation sends
A_H to A_H'. The input conjugation and each output P are invertible,
so its visible determinant stays nonzero. Every individual native
foreign-view determinant is therefore a nonzero polynomial in its
donor-specific source parameters.

These transported choices need not agree for different receivers. They
are certificates of nonzero individual polynomials. Section 5 selects
one common assignment satisfying all of them simultaneously.

## 4. Exact actual-quota early witnesses

The authenticated source routes contain 53,280 original early departures
at bank 480. For bank 256 normalize the actual per-incidence counts
15,30,45 to 8,16,24. There are respectively

    2,675 type-8 incidences,
      422 type-16 incidences,
       11 type-24 incidences.

Every donor's early quotas sum to 256. At a type-8 incidence choose an
8-by-16 matrix L_(j,H) and take L_(j,H) F_(j,H)(X) early. At a type-16
or type-24 incidence choose a 16-by-16 L and take all its quotient rows.
At each type-24 incidence also choose eight explicit arbitrary rows on
the original End(S) bank. These are additional early owners with their
own information; they are not restricted to the abstract quotient and
are never dropped from the physical source word.

`EARLY-WITNESSES.json.gz` gives a GF(16) assignment of the four vectors
in (4), all L matrices, and every additional row, separately for all
111 donors. The checker expands each actual 256-by-256 early map into
binary coordinates and checks rank 1,024. The native quota list is
reconstructed from the authenticated routes rather than supplied by the
witness. Thus every donor's early determinant is a nonzero polynomial
in the same source variables, early-frame variables and extra-row
variables that will be used in the simultaneous selection.

The witnesses have different assignments from the individual foreign
view. They establish nonzero polynomial factors, not a simultaneous
GF(16) implementation. No finite search over arbitrary larger sizes is
used to infer the theorem.

## 5. One simultaneous assignment over a fixed nine-bit field

Use the rank-eight parameter basis (3) for every donor-plane source,
independent variables for every entry of L, and independent variables
for all additional rows. All determinant polynomials have coefficients
in F_2. The exact GF(16) witnesses in sections 3-4 prove that each is
formally nonzero over F_2. Their product is nonzero in the polynomial
ring, which is an integral domain.

A source parameter occurs in at most 36 foreign-view determinants:
the complete geometry has 36 roots perpendicular to H, and deleting
nonnative roots only decreases that number. In each such determinant
its coefficient matrix has rank at most eight, by (3), so its individual
degree is at most eight. The standard bound follows by multilinearity:
a term of degree greater than the update rank would require more
independent columns from that update than it has. The same bound holds
in the donor's one early determinant, even with variable L, since left
multiplication cannot increase the update rank. Therefore its degree in
the total determinant product is at most

    8(36+1)=296.                                      (7)

Each early-frame entry occurs in one row of one early determinant, so
its degree is at most one. Each additional-row entry has the same bound.

To ensure a genuinely noncommuting source, fix H=263 and donor 0. In
the original sixteen-column input coordinates, write its quotient as
F(X)=sum_t B_t X e_t, with B_t in A_H. Multiply the determinant product
by the polynomial giving the (0,0) entry of [B_0,B_1]. This polynomial
is nonzero: take B_0=N and B_1=M for the two actual H generators, whose
commutator is I. It adds at most two to any individual source-parameter
degree. Thus the full product has individual degrees at most 298.

A nonzero multivariate polynomial whose individual degrees are all
less than |F| does not vanish on all F^n. Induct on the number of
variables using the univariate root bound. Apply this to F=GF(512).
One explicit field is F_2[z]/(z^9+z^4+1); the checker verifies the
irreducibility criterion x^(2^9)=x and
gcd(x^(2^3)-x,z^9+z^4+1)=1. Because the polynomials have binary
coefficients, GF(512) need not contain the GF(16) witness field.

The resulting assignment makes every source view and every early map
invertible, and makes the chosen coefficient commutator nonzero. At a
type-8 incidence, the eight L rows are independent; complete them to an
invertible 16-by-16 frame and use its other eight quotient rows late.
At type 16 or 24, L is invertible already. These completions preserve
the abstract equivariant quotient F and require no new source data.
They may be undone later by a paid local linear operation, if the
downstream causal interfaces permit it.

Lexicographic enumeration of the finite GF(512) coefficient arrays and
exact determinant checks is a terminating selector. A complete common
coefficient file has not yet been emitted, and no practical selection
time bound is claimed. This is a source-existence theorem, not a
completed native word.

## 6. Literal source invoice and architecture compatibility

Repeat the basic maps on r matrix copies, with b=256r. Take r=15a to
fit the literal bank-480 routes, repeated 8a times. The 11 type-24 flags
retain 88r additional early field values. The 2,675 type-8 flags require
21,400r late field values. The other flags need no late source values.

At each donor, before the original X owners depart, compute all required
late parities into initialized stationary caches. Apply the chosen
invertible early source map to the actual original X owners. When the
genuine late Y owners visit that donor, add the cached parities into
them and pay dirty CLEAR for every cache. Original X values are restored
by the early inverse at Hub, or as part of the complete pure-early
inverse once downstream maps are provided. A departed X owner is never
read for free; Y baselines are arbitrary and are preserved by addition.

Expand the field in its nine-bit basis. Put

    M = 9b = 2304r,
    L_total = 9*21400r = 192600r.

The retained dense binary source compiler gives the finite upper bounds

    ADD <= 222(M^2+3M) + M L_total + L_total,
    INIT = charged dirty CLEAR = L_total,
    extra stationary ownership peak <= L_total,
    additional MOVE = 0.

At r=15, M=34,560 and L_total=2,889,000. The ADD bound is
365,025,125,160. The source map and its inverse are both included; all
late injections, snapshots and erasures in this source module are paid.
Finite coefficient selection is a separate fixed setup computation,
whose practical cost is not established. These bounds do not absorb any
new H/D/K transport, return-bank, decoder or recursive expense.

At the minimum bank, each ordinary H quotient is fifteen S copies
(dimension 240). A fully native H therefore has 45 spinor inputs and
45 spinor-width port packets. A D input or output boundary consists of
16 spinor flags, dimension 256, naturally the size of End(S). This is
the concrete matrix-module layout suggested by the covariant target.
The abstract source maps commute with gamma(i) on a visible receiver's
left action, as required by that target's receiver-wise covariance.

That common action is only an interface opportunity. No common H lifts,
shared D target spaces, causal early/late D implementation, or complete
K donor-rank realization follows from the source theorem. In particular,
the exact K saturation gate still requires full per-donor K ranks at
every native K. The output-frame inverses may mix early and late quotient
coordinates; their causal use must be proved downstream. The earlier
fixed-column commuting-source obstruction is not bypassed by calling a
source covariant: it is the explicit noncommuting coefficient condition
that removes that hypothesis.

The covariant irreducible endpoint has h/b=1/30 and positive retained
movement room, but is not physically realized by this source alone.
Strict covered-BIT and ordinary BIT prices, the compatible uniform
complex supplier, complete recursion and all five foundational
assumptions remain open. No complete new kappa is asserted.

## 7. Verification, controls and credit

`search.py` records bounded discovery of exact witnesses. `check.py`
reconstructs the native geometry, actual quotas and coefficient maps,
checks the full transvection orbit, expands all 112 witness matrices to
binary matrices, and verifies the parameter-rank and field claims.
Removing one complete source quotient destroys the foreign-view rank;
zeroing an actual early group destroys early invertibility. These
controls detect omitted source information and omitted original owners.
The checker also verifies a nonzero local coefficient commutator.

Source geometry, routes, Clifford basis, witness bytes, code and earlier
source compiler are pinned. Independent review is recorded separately;
rerunning this author checker alone is not independent mathematical
verification. The universal repeated-bank and fixed-field conclusions
follow from the written covariance, orbit transport and nonzero-polynomial
arguments, supported by exact finite certificates at the native geometry.

Credit @CubeJerry; the prior native atlas, balanced source compiler,
Clifford one- and two-evaluation packages, and the S027 covariant target.
The full covariant-family direction was suggested by the S027
orchestrator; Worker C constructed the witnesses and proof, with
substantial OpenAI assistance. This is a continuation of the same
permanent proof programme.
