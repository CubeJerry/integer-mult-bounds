# A target-feasible width-two quotient must be completely entangled

**Author theorem, independent review pending. No new kappa.**

This is an algebraic and real-support theorem for the actual 111-port BIT
source. It is not a physical source construction. It uses the classical
Kronecker classification of matrix pencils to obtain a finite architectural
classification, then excludes every class having a regular summand by new
native scalar-capacity and equality arguments.

## 1. Statement and the source facts used

Let k be any field of characteristic two. Let K be the actual native binary
111-by-111 fitting and C its nine-dimensional scalar row code, extended to k.
For each receiver i, J_i is its own index together with the indices of the
native real root lines orthogonal to its root. Let A be any fitting in
two-by-two blocks: A_ii=I_2, and A_ij=0 for j outside J_i. No symmetry,
commutativity, nonsingularity of foreign blocks, or prescribed scalar
reservoir is assumed.

For the foreign whole-block support at receiver i, define chi_i to be zero
if it lies in one proper real subspace of the rank-seven receiver facet,
one if two proper subspaces suffice but one does not, and two otherwise.
Put chi(A)=sum_i chi_i and S(A)=222-chi(A). This is the exact capped
proper-cover charge, not the cardinality charge ell or the quadratic proxy
gamma.

The canonical quotient is

    E = (row(A) + C tensor k^2)/(C tensor k^2)
      <= (k^111/C) tensor k^2.

Its scalar envelope D is the span of all contractions of E against value
functionals. All dimensions here are over the stated value field.

**Theorem.** Suppose dim E<=3 and chi(A)<=194. Then dim E=3, and after
extension to an algebraic closure E contains no nonzero decomposable tensor
h tensor v. Up to a basis of E, a basis of D, and a change of the two value
coordinates, E has exactly one of the following forms, with all displayed
h_j independent modulo C:

1. C3: span{(h0,h1),(h1,h2),(h2,h3)}; dim D=4.
2. C2+C1: span{(h0,h1),(h1,h2),(h3,h4)}; dim D=5.
3. C1+C1+C1: span{(h0,h1),(h2,h3),(h4,h5)}; dim D=6.

Here `(h,g)` abbreviates h tensor e0 + g tensor e1. The three forms are
architectural possibilities, not assertions that a native target fitting
in them exists. The C3 class is the previously studied long chain. The
other two are mixed short chains with shared receiver selectors; they
cannot be billed as independently decoded scalar components.

More quantitatively, every family with a regular summand has chi>=195.
The diagonal repeated-eigenvalue subcase of C1+R2 has chi>=208.
When the scalar envelope is at most three, the inherited stronger
cardinality theorem gives chi>=ell>=197.

### Exact inherited source premises

All native premises are from the programme, not from the external pencil
literature. The finite native input is pinned by SHA256
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.

* `C intersect k^{J_i}=k K_i`, and every canonical foreign degree is at
  least 55. Every canonical foreign support has chi_i=2.
* Every nonzero canonical codeword has weight at least 48. Every nonzero
  word in the forbidden restriction C|J_i^c has weight at least 18.
  These statements hold over every characteristic-two extension field.
* A proper subspace of a receiver facet contains at most 36 native roots.
  Mutually orthogonal nonzero real roots are linearly independent, so
  there are at most eight; seven have at most one further common
  orthogonal native root line.
* Every scalar native fitting in C+k h has S<=14. If equality holds,
  exactly seven receivers save, each saves two, their roots are mutually
  orthogonal, and there is one literal representative g of the projective
  h-coset supported exactly on those seven receivers. The used scalar
  rows are g/g_i. Every coefficient g_i on that support is nonzero.
* If a scalar coset is available at all seven roots of an orthogonal
  seven-set P, the admitted gluing theorem gives a representative
  supported in the intersection of their closed sets J_i. That
  intersection is P together with at most one common orthogonal root.
* The existing width-two envelope-three theorem excludes dim E<=3 and
  dim D<=3 at ell<=194. The existing one-width theorem excludes dim E<=2.

The checker reconstructs the small rank/distance premises from the pinned
native. The previously admitted universal scalar-capacity, equality,
gluing and envelope theorems remain explicit dependencies; replaying their
authors' scripts is not represented as a new independent proof of them.

### Dependency map and extension-field justification

Paths below are relative to `research/moonshot-005-program/`. Their exact
SHA256 pins are emitted by `check.py` into `RESULT.json`.

| Premise | Existing proof and location |
|---|---|
| Scalar capacity14 | `results/bit-scalar-proper-cover-fourteen/author/PROOF.md`, sections1--5 |
| Equality14 and unique short support | `results/bit-scalar-proper-cover-equality/author/PROOF.md`, sections1 and5 |
| Availability gluing | `results/bit-one-extra-coset/author/PROOF.md`, “Exact finite source premises” and “Gluing lemma” |
| Canonical local-kernel and quotient injection | `results/bit-operator-canonical-quotient/author/PROOF.md`, sections1--2 |
| Quotient dimension at most one width | The same proof, section1 theorem and sections3--4 |
| Envelope at most three | `results/bit-three-direction-width-two/author/PROOF.md`, sections1--5 |
| Forbidden distance18 | `results/bit-full-halfclass-width-two-gate/author/PROOF.md`, section3; fresh finite reconstruction here |
| Global distance48 and extension | `results/bit-quotient-direction-savings/author/PROOF.md`, “Sharp algebraic witness and negative control”; fresh reconstruction here |
| Proper real subspace bound36 | `results/bit-monotone-arrival-gate/PROOF.md`, geometric E7 support theorem |

Here is the elementary extension argument for both distance statements.
A vector in a binary code extended to a characteristic-two field uses
only finitely many scalar coefficients. Expand those coefficients in an
F2-basis of their finite F2-linear span. Each nonzero coefficient component
is a binary codeword, and the extended word's support is the union of its
nonzero component supports. The same argument applies to a punctured or
restricted binary code. Thus binary minima48 and18 remain minima after
arbitrary extensions. Binary matrix ranks are likewise invariant.

A chi-saving row necessarily deletes a canonical foreign block: otherwise
its support would be the full canonical support, whose chi is2. More
generally the capped cover charge is support-monotone. This supplies the
contact-deletion premise used in section3 without replacing chi by ell.

## 2. Why a matrix pencil classifies the quotient

Choose a basis of E and write its inclusion as z -> (Pz,Qz), where P,Q
are D-by-3 matrices. The stacked map is injective; im P+im Q is D by the
envelope definition. Thus there is no common right kernel and no common
left kernel. Changes of quotient basis and envelope basis give strict
equivalence of the pencil P+tQ. A value-coordinate change acts by an
invertible linear substitution in its two slices. Applied to A it is a
simultaneous similarity on every block, preserving its own identities,
zero blocks and all whole-block supports.

We use the classical Kronecker theorem: a pencil is a direct sum of
regular square blocks, right singular blocks of size e by (e+1), and left
singular blocks of size (e+1) by e. The common-kernel conditions exclude
the zero-size singular blocks. Every remaining left singular block uses
at least one of the three columns; every right singular block uses at
least two. If a right singular block is present, the remaining at most
one column can contribute at most one left block. Consequently the total
row dimension is at most three. This case is already excluded by the
envelope-three theorem.

For D>=4 only left singular and regular blocks remain. Write C_e for a
left block with e columns and e+1 rows. It gives quotient basis

    (h0,h1), (h1,h2), ..., (h_(e-1),h_e).

Partitioning the three available columns gives exactly the following
six block-size families:

| Family | Envelope dimension |
|---|---:|
| C3 | 4 |
| C2+R1 | 4 |
| C1+R2 | 4 |
| C2+C1 | 5 |
| C1+C1+R1 | 5 |
| C1+C1+C1 | 6 |

Over an algebraic closure R2 is either two one-dimensional eigenblocks
(equal or different eigenvalues) or one Jordan block. A value-coordinate
change avoids infinite eigenvalues, and the convenient normalizations
used below are legitimate. C_e remains in the same strict-equivalence
class after any invertible value change; its minimal index is unchanged.

This classification is a use of established mathematics, not a new
Kronecker theorem. A primary source for the decomposition is Olivier
Verdier, *Reduction and Normal Forms of Matrix Pencils*, section 8,
especially Theorem 8.5, https://arxiv.org/abs/1205.1138. The connection
between 2-by-m-by-n tensor classification and pencils is developed by
Eric Chitambar, Carl A. Miller and Yaoyun Shi, *Matrix Pencils and
Entanglement Classification*, J. Math. Phys. 51 (2010), 072205,
https://arxiv.org/abs/0911.1803, DOI 10.1063/1.3459069. The new contribution
here is the native source consequence in sections 4--7.

Every nonzero vector of a C_e block has two independent scalar columns:
the first and last nonzero coordinates of its shifted coefficient sequence
prevent proportionality. A nonzero vector in a direct sum of C_e blocks
therefore cannot be decomposable either, since its projection to any
nonzero block would be decomposable. A regular block has an eigenvector
over an algebraic closure, hence supplies a nonzero decomposable quotient
vector. Thus excluding the three regular families proves the theorem's
geometric complete-entanglement assertion.

## 3. A common matrix-functional lemma

Fix a saving receiver i. Its quotient selector U is a 2-by-3 matrix of
rank two. Indeed, if a nonzero output row w killed its quotient, then
w A_i would lie in C tensor k^2. Locality and the own block force it to
equal K_i tensor w. But a saving row must delete a canonical contact,
where this is nonzero. This proves the selector-rank assertion.

Write its block row, using global scalar representatives h_j, as

    A_ij = B_ij + sum_a h_a(j) M_a,

where each scalar entry of B_i is in C. Put

    Phi(z) = sum_a z_a M_a.

Then I_2 belongs to im Phi. To see this, any matrix functional f vanishing
on im Phi makes f(A_i) a local scalar C-row, hence f(I)K_i. Its deleted
canonical contact forces f(I)=0. The annihilator criterion gives the claim.

Choose any identity preimage a with Phi(a)=I. A coefficient vector c gives
a support-dominated scalar fitting in C+k(sum_a c_a h_a) whenever

    c annihilates ker Phi, and c.a != 0.                 (F)

In fact c is f composed with Phi for some matrix functional f; then
f(A_i)/(c.a) is the required row. The own value is one and a zero block
stays zero. The scalar code direction is fixed globally even though f,
a and its normalization may depend on i.

Whenever c is defined using a fresh transcendental t, all original fitting
data and a are taken over the earlier coefficient field. For example
c=e_p+t e_q annihilates ker Phi exactly when both coordinate functionals
do, and c.a is nonzero when (a_p,a_q) is nonzero. Such scalar extensions
are proof devices; they are not an unpriced executable field extension.

If r fixed scalar codes collectively dominate every saving receiver, form
each scalar fitting by using its dominated rows and K elsewhere. Since
whole-block support contains each scalar support, the sum of their scalar
savings is at least S(A). Each such scalar fitting has savings at most14.
Thus S(A)<=14r. At equality every used code saturates14, no positive
saving is counted twice, no domination increases the saving, and the
scalar equality classification applies to each code.

## 4. C1+R2: repeated and Jordan eigenvalues

With a repeated eigenvalue, use a value change to write the three quotient
generators as

    (h0,h1), (h2,0), (h3,0).

Contraction against the second value coordinate has scalar image span(h1).
At every receiver choose an output functional giving own value one. This
produces a support-dominated scalar fitting in C+k h1. Hence S<=14.

For the Jordan case use

    (h0,h1), (h2,0), (h3,h2).

Writing U=[u v w], with column vectors u,v,w, the coefficient map is

    Phi(z) = [z0 u+z2 v+z3 w, z1 u+z2 w].              (J)

If u,w are independent, Phi is invertible: after quotienting both output
columns by span(u), the contributions of z2 and z3 are independent.
If u!=0 and w=t0 u, rank U=2 forces v independent of u and the kernel
is span((t0,0,0,1)). In both cases e1 and e2 annihilate ker Phi, and an
identity preimage has (a1,a2)!=0 because its second column is nonzero.
Thus the generic scalar code h1+t h2 dominates every saving row with
u!=0. If u=0, rank U=2 makes v,w independent, the kernel is precisely
the unused z0,z1 coordinates, and an identity preimage must have a2!=0.
The scalar code h2 dominates every such row. These two fixed codes give
S<=28.

If S=28, equality gives disjoint seven-sets P for h2 and Q for h1+t h2.
The representative of h1+t h2 supported on Q implies separately that
h1,h2 belong to C+k^Q: pass to the quotient by the k-defined subspace
C+k^Q and use the linear independence of 1,t. Hence h2 has representatives
supported both on P and on Q. Their difference is a C-word supported
on at most fourteen ports, below distance48, so the representatives are
equal. Since P and Q are disjoint, that common representative is zero,
contrary to the independence of h2 modulo C. Therefore S<=27.

This case distinction is essential. When u=0 the generic h1+t h2
functional does not annihilate the unused z1 kernel; a one-code proof
would be false. The finite controls retain an explicit such selector.

## 5. C1 plus two different regular eigenvalues

Normalize the independent regular value lines to obtain

    (h0,h1), (h2,0), (0,h3).

Then

    Phi(z) = [z0 u+z2 v, z1 u+z3 w].                   (D)

Let ker U be spanned by (a,b,c). A kernel element of Phi has its two
three-coordinate columns in that line. If b,c are nonzero, Phi is
invertible. If b=0,c!=0, its kernel is span((0,a,0,c)); identity requires
the coefficient a2!=0, so h2 dominates. If b!=0,c=0 the symmetric
argument gives h3. If b=c=0, u=0 and v,w are independent, and both h2
and h3 dominate. In the invertible case an identity preimage cannot
have a2=a3=0, since the resulting matrix has image in span(u). Thus the
two fixed scalar codes h2,h3 cover every saving receiver and S<=28.

Suppose S=28. Equality gives disjoint orthogonal seven-sets P2,P3 and
representatives g2,g3 of h2,h3 supported on them respectively. All fourteen
used block rows have chi_i=0. At every one of these rows u!=0: otherwise
both scalar codes dominate, contrary to equality's no-double-counting.

For i in P2, take an output functional nonzero on u and inspect the first
value coordinate of A_i. It shows that h0 is available modulo C at i,
because h2 has the literal local representative g2. Applying scalar
gluing to all seven i in P2 gives a representative f0 of h0 supported
on P2 plus at most one common orthogonal root. Similarly h1 has a
representative f1 supported on P3 plus at most one root. All four scalar
representatives f0,f1,g2,g3 therefore lie in a set X of at most16 ports.

Use these representatives to write any of the fourteen saving rows as
its canonical part plus U times the same three literal quotient rows.
On forbidden positions outside X the canonical part is zero. Its
forbidden restriction has support at most16, below the source distance18,
so it vanishes entirely. Canonical local rigidity makes that part K_i M_i
for a constant 2-by-2 matrix M_i. If M_i!=0, at least55-16>36 foreign
canonical contacts outside X survive, impossible for chi_i=0. Hence
M_i=0 at all fourteen rows.

They now factor through the same three-dimensional literal row space.
For any two of these receivers i,j, write A_ij=U_i H_j, with U_i of size
2-by-3 and H_j of size3-by-2. The own identities imply both factors have
rank2. Sylvester gives rank(A_ij)>=1. Thus all fourteen roots would be
pairwise orthogonal, contradicting the ambient real dimension8.
Equality is impossible: S<=27 and chi>=195.

## 6. C2+R1

Normalize the regular generator and write

    (h0,h1), (h1,h2), (h3,0),
    Phi(z)=[z0 u+z1 v+z3 w, z1 u+z2 v].                (C)

Let ker U=span(a,b,c). If c=0, then u,v are dependent. The only part of
Phi with output image outside span(u,v) is z3 w, so every identity
preimage has a3!=0. Also z3 vanishes on ker Phi; thus h3 dominates.
If c!=0 and b!=0, Phi is invertible. If c!=0 and b=0, its kernel is
span((a,0,0,c)). In both latter cases the functionals e1,e2 annihilate
the kernel, and an identity preimage has (a1,a2)!=0 because its second
column is nonzero. Therefore the generic code h1+t h2 dominates.
The two fixed codes h3 and h1+t h2 give S<=28.

If S=28, the generic code has equality support P of seven orthogonal
ports; the h3 code has a disjoint equality support Q of seven ports.
Since h1+t h2 belongs to C+k(t)^P, and C and the coordinate subspace
k^P are defined over the earlier field, linear independence of 1,t in
the quotient by C+k^P implies separately

    h1,h2 belong to C+k^P.

Choose representatives f1,f2 supported on P. At any i in Q, the second
column of its block row is now a canonical vector row plus u f1+v f2.
The canonical forbidden restriction is supported on at most seven ports;
distance18 makes it zero, so it is K_i b_i for some two-vector b_i.
If b_i!=0, at least55-7>36 foreign contacts survive in that column,
contradicting chi_i=0. Thus b_i=0. But i is outside P, so the second
column of A_ii is zero, contradicting A_ii=I_2. Again S<=27.

## 7. C1+C1+R1

Write

    (h0,h1), (h2,h3), (h4,0),
    Phi(z)=[z0 u+z2 v+z4 w, z1 u+z3 v].               (M)

If ker U=span(a,b,c) has c=0, then u,v are dependent and an identity
preimage must have a4!=0; h4 dominates. If c!=0, ker Phi is the line
span((a,0,b,0,c)). Hence e1,e3 annihilate it and the nonzero second
column of identity gives (a1,a3)!=0. The generic code h1+t h3 dominates.
The same two-code argument gives S<=28.

Equality would place representatives of h1 and h3 on one seven-set P,
by the same transcendental coefficient separation. The other regular
code would attain equality on a disjoint seven-set Q. At i in Q the
second column involves only those two P-supported representatives and
an entrywise canonical term. The distance18 and support36 argument of
section6 again forces that column's canonical term to vanish, making
its own coefficient zero. Therefore S<=27.

## 8. Scope, status, and next decisive construction

Sections4--7 give new all-field native exclusions for every regular
family. Combined with section2 and the inherited envelope-three gate,
they prove the complete-entanglement theorem. The universal argument is
independent of finite field size and of the native scalar envelope's
particular root/class reservoir. Its independent review remains pending.

After the regular-family closure, the two new constructive targets are
the C2+C1 and C1+C1+C1 quotients. Their coefficient kernels have genuinely
shared selectors. A valid target must provide a complete native fitting,
real support covers, actual chronological acquisition and receiver
access, all original restorations, and the full movement/ordinary/owned/
precision/compiler/recursive invoice. Algebraic possibilities do not
establish those services. Both strict suppliers and all five foundations
remain open; no new complete kappa follows.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the
native, scalar-gluing, sharp14/equality, source-distance and envelope-three
programme predecessors, and the cited classical pencil/tensor literature.
