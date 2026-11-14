# The full halfclass reservoir requires more than three width-two quotient dimensions

**Proposed all-field source-specific theorem; exact source certification and
independent review pending. No new kappa.**

## 1. Statement and the actual quotient

Let C be the canonical rank9 scalar code on the actual111 BIT ports over
an arbitrary characteristic-two field k. Partition the roots into36
halfclasses: equal coordinate support and equal sign parity after
normalizing the first nonzero sign. Eight groups are coordinate
singletons; the other28 have sizes2,3 or4. Let u_g be the group indicators
and U their span. The source certificate gives

    dim(U)=36, dim(C+U)=39, R=C intersect U of dimension6.

Identify D=(C+U)/C with U/R. Every quotient below lives in D, retaining
the six indicator relations.

Let E be any subspace of D tensor k^2 with dimension at most3.
Let A be any width2 native fitting with identity own blocks, prescribed
forbidden zeros, and canonical row quotient contained in E.

For each real foreign whole-block support, let chi_i be0 if one proper
facet subspace covers it,1 if two suffice but one does not, and2 otherwise.
Put S=sum_i(2-chi_i).

**Theorem.** S<=26, equivalently chi(A)>=196.

This misses the retained chi<=194 target. The family permits arbitrary
overlapping halfclass combinations and arbitrary block operators. There
is no decomposable-tensor exclusion, triangularizability assumption or
chain shape restriction. Larger quotient dimension, other scalar
reservoirs and different source histories remain outside scope. No
physical supplier or complete kappa is obtained.

## 2. Exact local source structure

Let T_i be the closed canonical support of K_i. Let G_i be the halfclasses
wholly contained in T_i, and L_i their indicator span. The complete binary
rank check proves

    (C+U) intersect k^(T_i) = k K_i + L_i.              (1)

For noncoordinate i the sum is direct. For coordinate i, K_i belongs to
L_i and the right side is simply L_i. Binary ranks and kernel dimensions
are unchanged under scalar extension, so(1) is an all-field identity.

Every noncoordinate block row therefore has the unique form

    A_ij = K_ij M_i + sum_(g in G_i) (u_g)_j N_ig.     (2)

On canonical contacts outside all local groups the block is exactly M_i.

At all103 noncoordinate receivers these forced roots have quadratic-lift
span27 in Sym^2(F_i). Their unique vanishing quadratic is, up to scale,

    Q_i(x)=sum_(a in support(root_i)) x_a^2
           -sum_(a outside support(root_i)) x_a^2,

restricted to F_i=root_i-perpendicular. Its real signature is(3,4), so
its symmetric matrix has rank7. Two proper subspaces would be contained
in two hyperplanes, whose product gives a nonzero vanishing quadratic
with symmetric rank at most2. Uniqueness rules this out. Thus these
forced contacts have chi=2 despite quadratic rank27.

Every positive-saving noncoordinate row consequently has M_i=0 and lies
in L_i tensor k^2. Coordinate rows already lie in L_i by(1). This step
requires exact chi; the weaker quadratic-rank proxy gamma does not suffice.

The canonical code has minimum distance48. Noncoordinate local supports
have at most20 actual source ports; the maximum union of two is34, checked
over all5253 pairs. Therefore their projection into D is injective, and

    image(L_i) intersect image(L_j)=image(L_i intersect L_j).    (3)

Indeed two representatives differ by a C-word supported on at most34
ports, which must be zero. The same argument works after any field
extension: expand the finitely many coefficients in a binary basis, so
every nonzero extended codeword contains the support of a nonzero binary
component. No free change of quotient representative is used.

## 3. The small common reservoir W

There are exactly two size-two halfclasses, {9,11} and{46,50}. Let W_0 be
the literal indicator span of those two groups and the eight coordinate
singletons. Its actual support is

    X={0,1,2,3,4,5,6,7,9,11,46,50}.

Write W for its image in D. Projection is injective because |X|=12<48.
Every canonical foreign support outside X has quadratic span28, certified
for all111 receivers. The canonical forbidden restriction C|Z_i has
minimum nonzero weight at least18 at every i, another exact source fact.

**Small-support lemma.** A positive-saving row at i outside X has its
two-dimensional quotient row plane E_i disjoint from W tensor k^2.

To prove it, suppose q is a nonzero common vector. Write q=u A_i modulo
C tensor k^2 and choose its literal W_0-supported representative h. The
row coefficient u is nonzero. Over k(t), choose the value functional
v=(1,t)^T so u v!=0. Then

    f_j=(u A_ij v)/(u v)

is a scalar fitting row in C+k(t)(h v), with support contained in A_i.
Its extra word is supported on X and vanishes at i. On forbidden
coordinates, its canonical part has support at most12<18, hence vanishes.
Canonical rigidity and the own coefficient force that part to be K_i.
All canonical contacts outside X survive, so chi_i(f)=2. This contradicts
positive saving and support containment. This argument also covers the
case h v is the zero coset; that would give the canonical row directly.

The plane E_i has dimension2 by the admitted canonical contact-deletion
injection. Indeed chi_i<2 implies at most52 contacts, below every canonical
degree, so a canonical block is deleted. The own identity then makes the
quotient map on the two output rows injective.

## 4. All saving noncoordinate receivers must share one family

The fourteen four-coordinate root supports form seven complementary
pairs {P,P^c}. Call each pair a family. Each noncoordinate receiver lies
in one family. Over all4543 cross-family receiver pairs, the exact local
group census gives

    L_i intersect L_j subset W_0.

Together with(3), this is a statement about the actual quotient as well.
Let E_W=E intersect(W tensor k^2).

Suppose S>24. At least one positive-saving receiver i lies outside X,
because X has only twelve ports. This i is noncoordinate. If dim(E_W)>=2,
every2-plane E_j in the at-most3-dimensional E meets E_W nontrivially,
contradicting the small-support lemma at i. Thus dim(E_W)<=1.

For any positive-saving noncoordinate j in a different family, the
2-planes E_i,E_j intersect nontrivially. Their intersection lies in
W tensor k^2 by the cross-family source fact, again contradicting the
small-support lemma at i. Therefore ALL positive-saving noncoordinate
receivers lie in one family F. This includes the four noncoordinate
members of X; none is omitted from the subsequent count.

Let B_F be the literal indicator span generated by W_0 and the four
halfclasses in F. Its source support X_F has, for the seven families in
lexicographic order, sizes

    26,27,28,27,28,23,24.

Each L_j for a noncoordinate j in F is contained in B_F. Since every
|X_F|<48, the quotient projection is injective on B_F as well.

## 5. Coordinate canonical terms over one family remain expensive

For each of the seven F and eight coordinate receivers j, the exact
subcode computation gives

    {r in R : r vanishes on Z_j outside X_F}=k K_j.      (4)

There are64 binary R-words; the only nonzero permitted one is K_j in
each of these56 checks. The dimension-one kernel statement extends to
every characteristic-two field.

The forced contact set supp_foreign(K_j) minus X_F has chi=2 in all56
cases. Fifty-four have quadratic span27, with the unique split-norm
quadratic sum_(a in P)x_a^2-sum_(a in P^c)x_a^2 restricted to x_j=0.
Its symmetric rank is7. The other two cases are family P={0,1,2,3} at
receivers0 and3, with quadratic span26. In free facet coordinates y0..y6,
their quadratic kernels are respectively spanned by

    Q0=y0*y1-y3*y6+y4*y5,   or Q0=y1*y2-y3*y6+y4*y5,
    Q1=-y0^2-y1^2-y2^2+y3^2+y4^2+y5^2+y6^2.

For the doubled symmetric matrix pencil M0+z M1, two specified3-by3
minors are p(z)=1-4z^2 and q(z)=8z^3. They satisfy the exact identity

    (1+4z^2)p(z)+2z q(z)=1.

Thus no finite pencil member has rank at most2; the infinity member M1
has rank7. No nonzero vanishing quadratic factors into two linear forms,
so the forced support cannot be covered by two proper subspaces. All
kernel coefficients, minor positions and polynomial identities are in
the certificate. This is an all-real-parameter argument, not a sample
of candidate quadrics. The pencil and identity are over Q and R; they
are not reduced into the unrelated characteristic-two coefficient field k.

## 6. Distinct noncoordinate row planes force a small clique

Suppose two positive-saving noncoordinate receivers have different
quotient planes. Both lie in image(B_F) tensor k^2. Their2-planes span
the entire at-most3-dimensional E, so E has a unique literal lift H
inside B_F tensor k^2. Write every fitting row as a selector times H
plus its canonical part.

A positive noncoordinate row lies in L_i tensor k^2, hence in B_F tensor
k^2. Its canonical difference is supported on X_F, smaller than48, and
is therefore zero. For a coordinate receiver, (1) puts the row in U;
its canonical difference lies in R tensor k^2. Fitting zeros outside
X_F and(4) force that difference to be K_i M_i. If M_i is nonzero, the
forced chi2 support of section5 survives in the block row. Thus positive
saving again forces the canonical difference to be zero.

Every positive row is consequently U_i H with U_i of rank2. The own
identity at any other positive receiver j implies the3-by2 block H_j
has rank2. Sylvester's inequality gives rank(U_i H_j)>=1. Hence every
positive receiver has every other positive receiver in its source support,
and the native fitting zeros force their real roots to be mutually
orthogonal. There are at most8 such roots. If there are8, each row
contains the other seven independent roots, so each saves at most1.
If there are at most7, the total saving is at most14. This case therefore
has S<=14, incompatible with the standing assumption S>24.

## 7. A common noncoordinate plane also prevents the target

It remains that all positive-saving noncoordinate receivers have the
same quotient2-plane E0. Choose its literal lift H0 from the two rows
at one such receiver. It lies in B_F tensor k^2. Every other positive
noncoordinate row has the same quotient row space and lies in B_F;
minimum distance48 therefore makes its canonical difference zero.
It is an invertible2-by2 left multiple of H0.

The own identity shows H0 has an invertible2-by2 evaluation at every
positive noncoordinate receiver. Hence each such row has nonzero blocks
at all other such receivers. Their roots are mutually orthogonal.

If there are at most five positive noncoordinate receivers, their saving
is at most10. The eight coordinate receivers add at most16, giving S<=26.
This count includes all noncoordinate members of X.

Suppose instead there are at least six. The exact finite census checks
all501 orthogonal six-subsets of noncoordinate receivers within one
family. In every case their common literal local indicator span consists
of precisely two halfclasses g,h, one on each complementary coordinate
support. The six receivers lie in g union h, meeting both groups. As
H0 is supported in every used L_i, it lies in span(u_g,u_h) tensor k^2.

At a positive receiver in each group, the own identity makes the two
evaluation maps E0 -> k^2 at g and h isomorphisms. Thus every nonzero
q in E0 has nonzero values on both halfclasses. For any coordinate
receiver j, one of g,h is wholly forbidden: its four-coordinate support
contains that coordinate. The other group is wholly orthogonal to j.

If such a q were available at j modulo C tensor k^2, its forbidden
restriction would be canceled by a canonical codeword. That restriction
is supported on at most four ports, the forbidden halfclass. The source
restricted distance18 forces it to be zero in each value component,
contradicting the nonzero evaluation just proved. Consequently E0 has
zero intersection with the available quotient space at every coordinate
receiver.

Any positive coordinate receiver would supply a2-plane E_j in E, which
must intersect E0 because dim(E)<=3. This is impossible. There are no
positive coordinate receivers in this six-or-more case. All positive
receivers are the mutually orthogonal noncoordinate ones, whose total
saving is at most14 by the final argument of section6.

Together the alternatives prove S<=26. The proof does not use absence
of rank-one tensors, even after scalar extension. That stronger-looking
hypothesis from the initial research outline is unnecessary.

## 8. Four quotient dimensions attain the algebraic target

The quotient-dimension threshold for chi<=194 is exact in this reservoir.
Take the two disjoint native seven-cliques

    S1={54,56,57,59,61,63,64},
    S2={52,53,55,58,60,62,65}.

Their indicators h1,h2 are unions of full halfclasses. Use A_i=h1 I2
on S1, A_i=h2 I2 on S2, and A_i=K_i I2 elsewhere. All fitting zeros and
own identities hold. Each changed row has six independent foreign roots,
so chi_i=0; every other row is canonical with chi_i=2. Thus chi=194.

The two disjoint weight-seven scalar directions are independent modulo C:
every nonzero combination has support at most14<48. Their full width2
tensor therefore has dimension4, and the used rows attain all four
quotient directions. The exact binary rank check confirms canonical
quotient dimension4. This credits and reuses the two-seven-class boundary
from the class-reservoir geometric bridge; it is not a new physical word.

Consequently the least canonical quotient dimension for a width2 fitting
inside this full halfclass reservoir to meet chi<=194 is exactly4.
Achievability concerns the algebraic fitting and real support covers;
acquisition, cost, ownership and complete source realization remain open.

## 9. Exact verification and remaining scope

The accompanying checker authenticates the native word, all111 local
rank identities, C and restricted-code distances, the full64-word R code,
all5253 local support unions,4543 cross-family intersections,501 common
six-subset spans and56 coordinate/family subcodes. Exact modular minors
certify the103 noncoordinate quadratic ranks,111 outside-X ranks and56
coordinate/family ranks. Explicit nonzero quadratic kernels prove the
upper ranks; the two exceptional pencils use the displayed polynomial
identity. No finite numerical sample replaces the universal pencil proof.

Binary code rank identities and distance bounds extend to every
characteristic-two field. The real chart geometry is kept separate from
that coefficient field. The argument controls canonical quotient
dimension, not arbitrary fitting rank or a physical packet count. An
actual history may add9V only when it truly contains the canonical tensor
code. No acquisition, ownership, erasure, recursive supplier, precision,
compiler or foundational-assumption contract is weakened.

The theorem explains why a search using only linear/quadratic rank cuts
can admit false geometric candidates: most forced obstructions here have
quadratic rank27 and an irreducible rank7 vanishing form. A separate
bounded five-type GF4 chain search is preserved with its original
necessary-relaxation scope; it is not evidence for this theorem.

Prepared for @CubeJerry with OpenAI assistance. Credit the native scalar
code and source geometry, canonical quotient injection, scalarization,
restricted-distance and halfclass predecessors. Exact pins and
reproduction commands accompany the package. Independent review remains
separate. No new kappa.
