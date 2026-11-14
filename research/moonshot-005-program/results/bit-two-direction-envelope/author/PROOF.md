# A proper two-direction operator envelope reduces to one scalar direction

**Universal support-domination theorem and native BIT corollary. Independent
review pending. No physical decoder, supplier or new kappa.**

Changing the two scalar patch directions cannot rescue a proper operator
compression of their tensor span. The argument does not assume commuting
coefficients or the fixed supports of the earlier two-patch investigation.

## 1. A rigid scalar reference code

Let k be any field and n,V positive integers. Fix allowed source sets J_i
containing i. Let C<=k^n be a scalar code with rows K_i in C satisfying

    (K_i)_i=1, supp(K_i)=J_i,
    C intersect k^(J_i) = span(K_i).                       (R)

Here k^(J_i) denotes vectors supported on J_i. Thus each receiver has one
local canonical direction. Nonzero foreign entries of K_i need not be1.
A block fitting A has identity diagonal and zero blocks outside J_i. Put

    C_V=C tensor k^V, W=row(A)+C_V, E=W/C_V, d=dim E.

Choose two independent scalar quotient directions h1+C,h2+C and suppose

    E <= D tensor k^V, D=span(h1+C,h2+C), d<2V.            (E)

**Theorem.** Over L=k(t), there is a scalar fitting F and one scalar vector
h outside C_L such that

    row(F) <= C_L+span_L(h), F_ii=1,
    F_ij=0 whenever A_ij=0.                               (S)

Any objective monotone in foreign row-support sets is no larger for F than
for A. The extension is substantive: a three-receiver example below
disproves base-F2 support domination. This algebraic lower-bound reduction
does not claim physical implementation of rational-function coefficients.

## 2. A full scalar line gives subwidth scalarization

First suppose E contains span(h+C) tensor k^V for h outside C. Put
B=C+span(h). The preimage inclusion gives

    row(A)+B_V=W, dim(W/B_V)=d-V<V.

For each i the map u -> u A_i+B_V has a nonzero kernel vector u_i, and the
own block of u_i A_i is u_i. Apply a linear functional taking u_i to1 to
each source block. This gives a row in B, own coefficient1, and zeros at
every zero block of A_i. Independent choices at all rows prove(S), even
over k. This is Worker C's source-free subwidth scalarization argument,
included for self-containment and credited rather than claimed anew.

## 3. Without a full scalar line, each changed row sees both directions

Now assume E contains no whole scalar-line tensor. Define

    P_i={q in D : q has a representative supported on J_i}.

The quotient-row map phi_i:u -> u A_i+C_V has image in
E intersect(P_i tensor k^V). These are linear restriction equations.
Call a row changed when at least one canonical contact j in J_i is erased
as a whole block. If phi_i(u)=0, condition(R) gives
u A_ij=(K_i)_j v. The own block forces v=u. At an erased contact the
nonzero scalar (K_i)_j forces u=0. Hence phi_i is injective with image
dimension V.

If dim P_i=0 this is impossible. If dim P_i=1, the image is the entire
P_i tensor k^V, a full scalar line in E, also impossible. Thus P_i=D for
every changed row. Choose local representatives h1^(i),h2^(i), supported
on J_i, and subtract their own coefficients times K_i so their own
coordinates are zero. They differ from h1,h2 only by canonical rows;
condition(R) makes these normalized representatives unique.

For some V-by-V matrices M1_i,M2_i the fitting has the exact form

    A_ij=(K_i)_j I + h1_j^(i) M1_i + h2_j^(i) M2_i.       (2)

Subtracting the quotient components leaves a local canonical row. Its
identity own block forces the remaining component to be K_i tensor I.
No matrix inverse or commutation is used.

## 4. Erased contacts have one scalar evaluation pattern

At an erased contact j, divide(2) by nonzero (K_i)_j and write

    a=h1_j^(i)/(K_i)_j, b=h2_j^(i)/(K_i)_j.
    a M1_i+b M2_i=-I.                                    (3)

The matrices M1_i,M2_i are scalar-linearly independent. Otherwise both
are scalar multiples of one matrix, and(3) makes that matrix a scalar
multiple of I. Thus M1_i=c1 I,M2_i=c2 I with (c1,c2) nonzero, and the
quotient-row image is the entire scalar line
span(c1 h1+c2 h2+C) tensor k^V. This contradicts the case assumption.

Independence means(3) has at most one pair(a,b). Every erased contact of
row i therefore has the same nonzero normalized evaluation pair(a_i,b_i).
This replaces the fixed five/five/one-region argument of the earlier
two-patch example and works for arbitrary scalar directions.

## 5. One generic scalar direction dominates all changed rows

In L=k(t), choose the single global quotient direction h=h1+t h2.
Every a_i+t b_i is nonzero. Define at a changed row

    F_i=K_i-(h1^(i)+t h2^(i))/(a_i+t b_i).                (4)

This belongs to C_L+span(h), has own coefficient1, and remains zero
outside J_i. At each A-erased canonical contact its numerator is precisely
(K_i)_j(a_i+t b_i), so F_ij=0. Its support is contained in the block support
of A_i. At an unchanged row use F_i=K_i; all its canonical blocks survive
in A_i, so containment holds there too. This proves(S), with one global
scalar direction and permitted row-dependent normalizations.

An infinite extension also permits choosing a direction outside the finite
union of row annihilator lines. The rational-function choice avoids a
finite-field cardinality hypothesis. Line-freeness itself survives extension:
the space of h with h tensor k^V <= E is a kernel of a finite linear map,
whose rank is unchanged after extension. No nonlinear descent is assumed.

## 6. Native BIT consequence and strict boundary

For the actual111-port BIT source, C has dimension9 and every forbidden
restriction has rank8, so(R) holds for the binary canonical fitting.
The independently reviewed scalar one-direction theorem, valid over every
characteristic-two field, gives

    sum_i ell_i(F)>=205,
    ell_i=1[foreign support>36]+1[foreign support>52].

Apply it over k(t). Support containment implies ell(A)>=205. Therefore:

**Native corollary.** A fitting with ell(A)<=194 and d<2V must have scalar
quotient envelope dimension at least3. No choice of two scalar directions,
and no proper entangled or noncommuting subspace of their tensor span,
can meet the retained target. This covers every two-direction envelope,
not only the frozen two patches.

The scalar envelope is the span of all channel contractions of E into
k^111/C; it is independent of value-space basis. Any envelope of dimension
at most2 lies in a two-direction space. The native ambient quotient allows
extending a smaller envelope to dimension2.

The strict inequality d<2V matters. The already admitted scalar two-patch
fitting has ell193 and quotient dimension2; its identity tensor lift has
d=2V and beats205. This is an algebraic control, not a decoder. The theorem
does not bound arbitrary fitting rank or physical packet count. Actual
acquisition, access, endpoints and complete costs remain separate.

## 7. Base-field domination can fail

Take k=F2,n=3,V=2,C=span(1,1,1), K_i=(1,1,1), and h1=e0,h2=e1.
With I the two-by-two identity, use the block fitting

    [ I,               0,               [[1,0],[1,1]] ]
    [ [[0,0],[1,0]],   I,               0             ]
    [ 0,               [[1,1],[0,1]],   I             ].

Its canonical quotient has dimension3<4 in the two-direction tensor
envelope, with no whole scalar-line tensor. Its erased foreign contacts
are(0,1),(1,2),(2,0). Scalar fitting rows in C+span(h) with those zeros
would force h0,h1,h2 pairwise distinct, impossible over F2. Over F4 choose
h=(1,alpha,0), alpha neither0 nor1, and formula(4) supplies the fitting.
The native corollary is unaffected because its scalar205 theorem already
holds over every characteristic-two extension field.

The verifier checks this example, every normalized block-row choice in its
fixed five-dimensional total code, the full-line kernel test, the F2
failure, F4 domination, and the pinned native strict-boundary control.
These finite controls corroborate the universal proof.

## Dependencies and status

Native gzip SHA256:
51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78.
Scalar205 proof SHA256:
8e83d29e18e78e1b6f8e30a154b9cc84ad089c5283b2c04c807e048ffee5229b.
Programme baseline:880a5ad38f77b15a1e5c7f889a0233b8c83a7ca0.

Credit native/canonical and scalar-savings predecessors; Worker C's
subwidth reduction and fixed two-patch investigation; root's generic
two-direction reduction and finite-field control; @CubeJerry and OpenAI
assistance. Both strict suppliers, the complete kappa target and all five
foundations remain open. Independent review is separate.
