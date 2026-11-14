# Independent review: saturated star rigidity and actual BIT blocks

**PASS for the stated theorems and source application.** This is a separate
research-agent mathematical review with a separately written source checker.
It is not independent human review or formal-kernel acceptance.

## Reviewed identities and pins

Worker C author proof:
`bc93c7ef2b853c21f4f20541eda7bbd81ccf51da4a2d7b00ef0dc84ae585befe`.

Credited #7114 THEOREM.md, head
`fc90dc68b54d613a0600e5bddd8e4f557a4b4eda`:
`a2a0b79545a1857aea0bc9ac4beb9f222aa50984c9383053e9163af8e33a4802`.
Its Proposition10/LR and Theorem11 were read directly. The source is an open
PR, not admitted solely because its text was fetched. The LR argument is
independently checked below; none of that source's solver rows, claimed
Petersen value, or characteristic-zero port values is used here.

Actual native:
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
The earlier programme's global fitting proof was read for the point-frame
normalization and binary-anchor propagation. Their premises were separately
reconstructed from this actual native, not imported from its certificate.

## 1. Universal LR and equality review

The independent point frame gives a direct-sum ambient decomposition into its
nV coordinate space and a j-dimensional complement: C_point R_point=I
implies that the image of R_point and kernel of C_point are complementary.
This normalization does not assume symmetry or commutation of block entries.

For a star at point a, row blocks A_e and column blocks B_e have common
middle space of dimension V+j. Prescribed off-diagonal edge zeros give
A_e B_f=0 for e!=f. Thus the full product AB is block diagonal and its rank
is G_a. The rank of the map z->zB on row(A) is exactly G_a; its kernel has
dimension ell-G_a. For each e, every row in row(A_e) already annihilates
every B_f with f!=e. Consequently its kernel under B_e is contained in that
global kernel, with dimensions lambda_e-g_e(a) and ell-G_a. The transposed
argument gives the corresponding inequality for mu_e and rho. This is an
ordinary kernel inclusion; it does not use a positive-definite inner product
or identify a vector space with a commuting algebra.

Sylvester's rank inequality gives ell+rho<=V+j+G_a. The edge diagonal gives
alpha_e(a)=I-gamma_e(b), so lambda_e and mu_e are each at least V-g_e(b).
Combining these exact inequalities yields

    G_a + V <= j + 2(g_e(a)+g_e(b)).

When summed over both orientations of every edge, each g term is counted
four times. The author's coefficient is therefore correct:

    sum_a (degree(a)-4) G_a <= 2|E|(j-V).

At j=V and degree(a)>4, nonnegativity forces every G_a, hence every gamma,
to be zero. Both endpoint products are then -S_e; the diagonal says
(-S_e)+(-S_e)+S_e=I, giving S_e=-I over every field. This remains valid in
characteristic two, where it is S_e=I. No trace/divisibility or hidden
positivity argument is present. The square last factors are therefore units,
and the previously open singular-Schur case is genuinely removed.

The rank-excess inequality also follows: I+S_e=gamma_e(a)+gamma_e(b), so
rank(I+S_e)<=g_e(a)+g_e(b). Summing and dividing by the positive minimum
degree surplus gives the stated stability constant. For the actual seed,
2|E|/(delta-4)=54/2=27; this is an upper bound, not asserted optimal.

## 2. Noncommuting ordered-gauge review

For square u_e,v_e with u_e v_e=-I, both are invertible. Under the edge
vertex gauge C_e->u_e^{-1}C_e and R_e->R_e u_e, last factors are I,-I.
An incident-edge zero is A_ea D_fa-I=0. Every endpoint block is invertible,
and a third incident edge permits right cancellation to make the A_ea
independent of e. (The author's degree>=5 supplies more than this step needs.)
Writing that common block A_a, all D_ea=A_a^{-1}.

The ambient basis change multiplies row factors on the right by
diag(A_a^{-1},I), and column factors on the left by its inverse. These
orders make both edge factors canonical. Point vertex gauges restore point
inclusions and projections. None of the calculations swaps two matrix factors.
The resulting statement is vertex gauge of the signed standard star fitting.

The theorem's star graph uses point-point noncontacts, point-edge noncontacts
when nonincident, and incident-edge noncontacts; disjoint edges are permitted
contacts. If a different model imposed additional disjoint-edge zeros, the
derived canonical factors would contradict them rather than silently relax
their mask. The actual seed has exactly the required mask.

## 3. Independent actual-source reconstruction

The separate check.py uses only the authenticated original native. It builds
the contact matrix directly from exact real root orthogonality, with the
identity diagonal. It normalizes the eight designated point roles and forms
the binary Schur residual

    R_ij = K_ij + sum_a K_(i,F_a) K_(F_a,j).

The residual is independently verified to equal the outer product of its
diagonal with itself. This constructs the canonical nine-bit factors without
the author's pivot-based reconstruction. All12321 products are checked.

Exactly27 sparse edge roles appear; their endpoint graph is K8 minus(0,4),
with degrees6,6,7,7,7,7,7,7. Every ordered edge-pair mask constraint is
checked. For each of the remaining76 roles, the checker independently chooses
eight noncontact seed anchors, verifies rank8 and explicitly finds its sole
nonzero annihilator among511 binary vectors. It equals that role's canonical
factor and has self pairing1. Removing an anchor lowers the rank to7.

These binary central-coefficient equations have the same rank over every
characteristic-two field. For arbitrary V by V unknown blocks, they apply
entry by entry without any block products being reordered, so their solution
has C_i=U_i x_i^T and R_i=x_i V_i. The diagonal gives U_i V_i=I; square
matrices over a field are mutual inverses. Thus the global block conclusion
follows exactly as claimed for every V>=1, including nonsymmetric,
noncommuting blocks.

The source has6470 foreign ones, rank(K0)=9 and rank(K0-I)=108. Block diagonal
conjugacy preserves residual rank and foreign-block invertibility, giving
rank(K-I)=108V. This is an algebraic rank, not108V paid physical calls.

## 4. Controls and verification classification

The independent checker rejects a native-byte mutation and all76 seven-anchor
uniqueness controls. It verifies the coordinate-unit K4 fitting with rank5,
four zero Schur diagonals and two unit ones. That example works over every
field by its literal coordinate-unit factorization; it prevents discarding
the degree condition. It says nothing about degree4, which remains open.

An explicit pair of noncommuting2x2 binary matrices checks the ordered inverse
gauge; replacing an inverse by the same-order factor breaks its diagonal.
This is a finite order control, not a proof covering arbitrary blocks. The
universal conclusion rests on the independently reviewed kernel and ordered
algebra arguments in Sections1–3.

No author verifier was imported or executed. The independent command was:

    python -I -B check.py --native BIT-NATIVE-WORD.json.gz --output OUT

It emitted PASS_INDEPENDENT_SATURATED_STAR_SOURCE_REVIEW with27 seed edges,
76 anchors and ranks9,108. RESULT.json contains the reconstruction.

## 5. Downstream consequences and limits

The former arbitrary-block singular-Schur exception at minimum rank9V is
closed. In the programme's declared monotone historical-normalization model,
a completed fitting of rank9V now has full canonical foreign support for
every block width. The already proved E7 arrival obstruction therefore
applies without its former invertible-Schur qualification. In particular,
the nine-packet invertible-through route has no remaining block escape.

For a general completed monotone q8/q9 history in that same model, when the
canonical-support arrival contradiction applies, the conclusion is

    rank(A) > 9V, hence rank(A) >= 9V+1.

It is **not** rank(A)>=10V for arbitrary noncommuting blocks. Together with
rank(A)<=qV+sum nu_C, it gives sum nu_C >= (9-q)V+1 for q=8 or9. The scalar
V=1 consequence is the familiar rank>=10. The stronger rank16 requirement
for the specified class-target historical space is separate and unchanged.

No all-q8 impossibility, changed movement allowance, supplier gain, or
foundational-assumption discharge follows. Higher-rank W0 codes and different
representations remain possible. This is a substantive structural closure
with No new kappa.

Prepared for @CubeJerry by a separate OpenAI research agent. Credit Worker C
for saturation/application, DreamingOfClouds #7114 for LR and its star rank
method, and the retained programme/source authors for the canonical seed,
prior propagation and actual native. No independent human or formal-kernel
approval is implied.
