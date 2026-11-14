# Proper-cover capacity lifts to operator incidence and decomposable quotients

**Author bridge theorem; independent review pending. No new kappa.**

This package uses the separately reviewed scalar proper-cover capacity16.
Every statement below is formulated in the exact capped proper-cover charge
chi. Earlier cardinality17 theorems remain unchanged. The real support
geometry, characteristic-two value field, scalar code C and canonical fitting
K are the same pinned111-port source throughout.

## 1. A generic scalar projection of a common operator quotient vector

Let k be any characteristic-two field, V>=1, C_V=C tensor k^V, and A a
V-by-V block fitting with A_ii=I and the prescribed native zeros. Put

    E=(row(A)+C_V)/C_V,   d=dim E,
    w_i=2-chi_i(supp_foreign(A_i)),   S=sum_i w_i.

Every canonical row has chi=2. Thus a row with w_i>0 deletes a canonical
foreign block. The canonical restriction kernel then proves that

    phi_i:u -> u A_i+C_V

is injective: a kernel vector gives a canonical row K_i u by the own block,
and evaluating it at a deleted contact gives u=0. Its image E_i has
dimension V. Neither scalar operators nor simultaneous triangularization
are assumed.

**Projection lemma.** For any nonzero q in the intersection of E_i over a
set I of positive-saving receivers, their total weight is at most16.

Choose a representative h=(h_j)_j of q, with h_j in k^V. For every i in I
choose the unique nonzero u_i with u_i A_i-h in C_V. Extend scalars to k(t)
and apply the common linear functional

    lambda(x_0,...,x_(V-1))=sum_b t^b x_b.

Every lambda(u_i) is a nonzero polynomial. The scalar rows

    F_i=lambda(u_i A_i)/lambda(u_i)

have own coefficient1, satisfy all native zeros, belong to the same global
one-mode code C_(k(t))+k(t) lambda(h), and have support contained in the
corresponding block row. Fill every other row with its canonical row. Since
chi is support monotone, these scalar rows save at least sum_(i in I) w_i.
The reviewed all-field scalar capacity16 applies over k(t), proving the
lemma. No common-coordinate gluing argument or base-field scalar dominator
is required. Even if lambda(h) were canonical, the scalar theorem still
applies; that case cannot yield positive savings.

The scalar extension is an algebraic proof device for a support comparison.
It supplies no machine operation, available record or change to the costed
value interface of the original fitting.

## 2. Density, weighted intersection and finite-field incidence

If t positive-saving receivers together have weight greater than16, their
quotient images have zero intersection by the projection lemma. For t
V-dimensional subspaces in dimension d, codimension subadditivity gives

    dim intersection E_i >= V-(t-1)(d-V).

Consequently

    d >= V+ceil(V/(t-1)).                              (1)

If S>16, selecting rows until their integer weights first exceed16 uses at
most17 rows. Hence the uniform all-width bound is

    d >= V+ceil(V/16).                                 (2)

If S>=28 and b rows have chi_i=0, select double-saving rows first. For b<=7
one can use b doubles and17-2b singles, giving t=17-b. For b=8 use those
eight doubles and one single; for b>=9 use nine doubles. Therefore

    d >= V+ceil(V/(16-min(b,8))).                       (3)

For a finite value field of order Q, count nonzero quotient vectors with
receiver weights. Each E_i has Q^V-1 such vectors, and each nonzero vector
has weighted incidence at most16 by the projection lemma. Thus

    S (Q^V-1) <= 16 (Q^d-1).                           (4)

These are statements about canonical quotient dimension. If an actual
history W supplies row(A), they also lower-bound dim((W+C_V)/C_V). Only if
C_V is actually contained in W may one add9V and infer
dim W>=10V+ceil(V/16). Neither d nor dim W is automatically a number of
physical packet identities, and arbitrary rank(A) is not asserted to
exceed this canonical-baseline expression.

The factor17/16 in(2) is sharp for the abstract point-incidence premise.
Over GF(32), in E=k^17 take28 hyperplanes with normals
(1,a,...,a^16) at distinct a. A nonzero vector represents a polynomial of
degree at most16, so lies in at most16 hyperplanes. Here V=16,d=17,S=28.
Tensoring with k^s gives V=16s,d=17s. This arrangement is not a native fitting
or physical source; it only prevents strengthening(2) from the pointwise
capacity premise alone. Similarly S=16 does not force d>V abstractly.

## 3. Common invariant filtrations

Suppose all block coefficients preserve a common invariant filtration with
nonzero layer dimensions v_1,...,v_s, summing to V, and S>16. Each diagonal
layer is a native block fitting whose whole-block support is contained in
that of A, so its chi saving is at least S. Apply(2) to every layer.

The established rectangular stacked-minor argument for [A;C tensor I]
gives total rank at least the sum of the diagonal-layer ranks. Subtracting
the canonical9V dimensions yields

    d >= sum_j (v_j+ceil(v_j/16)).                      (5)

A complete invariant flag again forces d>=2V. A commuting coefficient
family triangularizes over an algebraic closure; field extension preserves
ranks, and similarity preserves whole-block zeros. Thus the same2V boundary
holds in that case. No characteristic-two Lie-solvability assertion is used.

## 4. Decomposable quotient capacity and the new MDS threshold

Assume V>=2 in this section. Suppose, after a permitted scalar extension,
E has a basis of r pure tensors
h_a tensor v_a. Apply either of the two admitted structural hypotheses:

1. r<=V+1, with no MDS assumption; or
2. V<=r<2V and every V of the value vectors v_a are independent (MDS).

The earlier decomposable-capacity proof establishes, using rank-one matrix
dependence and dual matrix functionals, that every positive-saving row is
support-dominated in at least V indexed scalar codes C+span(h_a). This uses
only the existence of a deleted canonical block and the named structural
hypothesis. The repeated-value-line case in hypothesis1 instead supplies
one scalar code for all saving rows, which is stronger. If r<V there are
no saving rows.

Each indexed scalar code has chi-saving capacity16 by the reviewed scalar
theorem. Charging the receiver weights to those codes therefore gives

    V S <= 16 r.                                      (6)

Coincident scalar codes can occur among the indices. Counting them several
times only weakens this upper bound; it does not supply additional physical
resources. The proof uses support domination, so replacing cardinality by
chi is legitimate here without any comparison between gamma and ell.

Under the necessary target S>=28, an MDS quotient in this range must satisfy

    r >= ceil(7V/4).                                  (7)

The formerly first arithmetic possibility V=3,r=5 is now excluded:
S<=floor(80/3)=26, so chi>=196. The first remaining arithmetic possibility
with r<2V is V=4,r=7, where(6) permits S=28 exactly. No fitting, source or
supplier at that parameter point is claimed. A completely entangled quotient,
such as the protected larger-field chain construction, is not covered by
these pure-tensor hypotheses.

## 5. Other support-dominating bridges and physical compatibility

The admitted two-scalar-direction envelope theorem produces one global
scalar-code dominator when d<2V. Its chi lower bound is therefore206.
The admitted width-two envelope-three theorem, and the four-direction chain
theorem with at most three exceptional conic types, each use at least two
of three global scalar-code dominators. In those respective scopes,
2S<=48 and chi>=198. Their earlier cardinality lower bounds remain separate.

For the retained actual-route model, the existing local source normalization
puts a row's foreign support in its anchor chart plus one proper chart for
each nonanchor occurrence t_i. By the definition of chi, t_i=0 implies
chi_i=0, t_i=1 implies chi_i<=1, and t_i>=2 implies chi_i<=t_i. Thus the same
paid-occurrence accounting gives the necessary chi<=194 target in that
specific retained model. The source interface, full caller costs and all
foundational assumptions are retained; this is no universal multiplication
lower bound or transfer to an unpriced chronology.

The new numerical thresholds are obstructions and design requirements.
No positive target construction, new complete kappa, strict supplier,
precision service, erasure theorem or foundational discharge is obtained.

## 6. Capacity parameter retained for later improvements

The projection argument is independent of the number16. If a future theorem
uniformly bounds one-mode chi saving by an integer L>=1 over all required
scalar extensions, the same proof gives pointwise weighted incidence at
most L, d>=V+ceil(V/L) whenever S>L, and

    S(Q^V-1)<=L(Q^d-1),       V S<=L r

under the respective incidence and decomposable hypotheses above. This is
a conditional parameterized bridge, not an assertion that any L<16 has
been established here. In particular, L=14 would exclude every MDS r<2V
at the target S>=28; the premise must be proved independently before using
that consequence.

Prepared for @CubeJerry with OpenAI assistance. Credit the separately
reviewed scalar proper-cover theorem, prior quotient injection and density
proofs, the invariant-filtration and decomposable-capacity packages, and
Worker A's actual-source geometric charging interface.
