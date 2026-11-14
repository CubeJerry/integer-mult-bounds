# Three scalar directions cannot supply a width-two fractional target

**Proposed theorem, awaiting independent review. No new kappa.**

Author: root, for @CubeJerry, with OpenAI assistance. This continues the admitted canonical-quotient programme. Baseline: `880a5ad38f77b15a1e5c7f889a0233b8c83a7ca0`.

## 1. Statement and inherited native facts

Let k be any characteristic-two field. Let K be the pinned native 111-by-111 canonical fitting, C its nine-dimensional row code, and J_i the allowed positions for receiver i, including i. We use precisely:

1. K_ii=1, supp(K_i) is contained in J_i, and C intersect k^{J_i}=span(K_i).
2. Every scalar fitting with rows in C+span(h), for any scalar h over any characteristic-two extension field, has charge at least205.
3. K has charge222. A row with s foreign nonzero positions has charge1[s>36]+1[s>52]. Each scalar one-direction code thus carries at most17 saving units.

These are inherited facts. Native word SHA256: `51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`. Scalar205 proof: `bit-quotient-direction-savings/author/PROOF.md`, SHA256 `8e83d29e18e78e1b6f8e30a154b9cc84ad089c5283b2c04c807e048ffee5229b`. Subwidth scalarization and the two-direction-envelope theorem are additional dependencies.

Let A be any native fitting with arbitrary two-by-two blocks, identity diagonal and zero outside J_i. Put

    E=(row(A)+C tensor k^2)/(C tensor k^2),   d=dim E.

Regard E inside (k^111/C) tensor k^2. Its scalar envelope D spans every contraction of E against a value-space linear functional. This is independent of bases and representatives.

**Theorem.** If d<=3 and dim D<=3, then ell(A)>=197. Thus a width-two fitting with ell<=194 and d<=3 needs scalar envelope at least four. No commutativity, invertibility of foreign blocks, binary restriction, or pure-tensor basis is assumed.

Ranks, zero blocks, identity blocks and charges persist under field extension. We may use an algebraic closure and independent transcendentals without asserting that scalar dominators descend to k. The prior two-direction control shows this distinction is necessary.

## 2. Earlier reductions

If d<=2, the admitted one-width theorem gives ell>=205. If dim D<=2 and d<4, the two-direction-envelope theorem gives the same. If E contains a whole scalar-line tensor L tensor k^2, enlarge the scalar base to B=C+L. Its tensor lies inside row(A)+C tensor k^2. The remaining quotient has dimension d-2<2, so subwidth scalarization gives a support-dominated scalar B fitting and ell>=205. These statements hold after extension.

It remains that d=dim D=3, with E containing no whole scalar-line tensor over an algebraic closure. This excludes a complete two-dimensional line tensor, not an individual decomposable tensor.

## 3. A singular square pencil forces a whole line tensor

Choose bases and write the inclusion as z |-> (H_0 z,H_1 z), with three-by-three matrices H_0,H_1. The stack is injective, and im H_0+im H_1=D by the envelope definition. There is neither a common right kernel vector nor a common left kernel vector.

Suppose det(H_0+tH_1) is identically zero. Its rank over k(t) is two: rank at most one makes both H_0,H_1 have rank at most one, by constant and leading coefficients of their two-minors, contradicting the three-dimensional sum of images.

The adjugate of P(t)=H_0+tH_1 is nonzero, rank one over k(t), and has entry degree at most two. Choose primitive polynomial right/left kernel vectors p,q, with coordinate gcd one. Then adj P=f p q^T for a nonzero polynomial f. To justify polynomial rather than rational factors, each column is a rational multiple of p; a Bezout combination of primitive p coordinates makes that multiple polynomial. Apply the same argument to the resulting polynomial row and primitive q.

Neither p nor q is constant, since that would give a common right or left kernel. The maximal entry degree of f p q^T equals deg f+deg p+deg q: choose maximal-degree coordinates of p and q. Therefore both p and q have degree one and f is constant.

Write p=u+t v. Primitivity and degree one force u,v independent; otherwise their coordinates share a nonconstant factor. Comparing coefficients gives H_0u=0, H_1v=0 and H_0v=-H_1u. Set w=H_1u, which is nonzero by absence of a common right kernel. Then E contains (0,w) and (-w,0), hence the whole span(w) tensor k^2, contradiction.

The pencil is therefore regular. Over an infinite extension a nonzero value projection E->D is invertible. Change value coordinates to make it the first projection and change the E basis, obtaining

    E={(z,Tz):z in D}.

The value change acts on fitting blocks by simultaneous similarity, preserving zero blocks and identity diagonal. Over an algebraic closure a scalar-basis change puts T in Jordan form.

## 4. A row and a scalar functional

Let h_1,h_2,h_3 represent the Jordan basis of D. The graph basis is q_a=h_a tensor e_1+(T h_a) tensor e_2. A receiver's two quotient rows have a two-by-three coefficient matrix U, with columns u_a. The matrix multiplying scalar h_b in its block row is

    M_b=u_b e_1^T+(sum_a T_ba u_a)e_2^T.

The remaining part lies in C tensor Mat_2; it need not be a multiple of K_i.

A row deleting a canonical contact has injective quotient map. Otherwise a nonzero row vector u gives uA_i in C tensor k^2, supported in J_i, with own block u. Rigidity forces K_i tensor u, contradicting the deleted contact. Thus U has rank two.

Also I_2 belongs to span(M_b). For any functional f on Mat_2 annihilating every M_b, the scalar row f(A_i) is in C and supported in J_i. The deleted canonical contact forces it to be zero, so f(I_2)=0. The annihilator criterion gives the claim.

Define Phi(gamma)=sum_b gamma_b M_b. Its two columns show

    ker Phi=ker U intersect (T^T)^(-1)(ker U).

Since ker U is a line, ker Phi is zero or a T^T eigenline.

Choose a with Phi(a)=I_2. A fixed scalar coefficient vector c admits a functional f with f(M_b)=c_b exactly when c annihilates ker Phi. If also c.a!=0, then f(A_i)/(c.a) is a scalar fitting row in C+span(sum_b c_b h_b), with support contained in A_i. The value c.a is well defined despite a nonunique a. This functional criterion avoids assuming separately localized scalar representatives.

Every charge-saving row deletes a canonical contact, since all K rows have charge two. Set s_i=2-ell_i(A), in {0,1,2}. If each saving row is dominated by at least r of N fixed one-direction scalar codes, fill other rows of each code with K_i. Each full scalar fitting carries at most17 saving units. Thus r sum_i s_i<=17N. The scalar direction is fixed across receivers; row coefficients and matrix functionals may vary.

## 5. Jordan cases

### 5.1 Three distinct eigenvalues

Here M_b=u_b v_b, v_b=(1,lambda_b), with distinct projective row lines. Nonzero active M_b are independent. A minimal size-two dependence would equate rank-one matrices with distinct row lines. A size-three dependence has a two-by-three left matrix times a three-by-two value matrix of rank two equal to zero, forcing left span at most one. Its matrix span could not contain I_2. Both are impossible.

Representing I_2 uses at least two nonzero active coefficients. Dual functionals therefore let at least two of the fixed codes C+span(h_b) dominate each saving row. Consequently2 sum_i s_i<=51, giving sum_i s_i<=25 and ell>=197.

### 5.2 Diagonalizable, at most two eigenvalues

Choose an eigenvalue lambda of multiplicity at least two. The value projection (second coordinate minus lambda times first) of E has scalar image dimension at most one. Apply this fixed nonzero value functional to each source block; for each receiver choose an output functional making its diagonal one. The resulting support-dominated scalar rows all lie in the same C+span(h). Thus ell>=205. A zero scalar image needs no h.

### 5.3 A size-three Jordan block

Write v=(1,lambda), w=(0,1). Then

    M_1=u_1 v+u_2 w,  M_2=u_2 v+u_3 w,  M_3=u_3 v.

The only T^T eigenline is span(e_3). Therefore c=(1,t,0), with t transcendental over the data, annihilates ker Phi. In I_2=Phi(a), the pair(a_1,a_2) is nonzero because M_3 has rank at most one. Hence a_1+t a_2!=0. The single fixed code C+span(h_1+t h_2) dominates all saving rows, giving ell>=205.

### 5.4 A size-two block and the same eigenvalue

Now M_1=u_1 v+u_2 w, M_2=u_2 v, M_3=u_3 v. Every T^T eigenvector has first coordinate zero, so c=e_1 annihilates ker Phi. The identity

    I_2=(sum_b a_b u_b)v+a_1 u_2 w

forces a_1!=0, since otherwise its rank is at most one. The fixed code C+span(h_1) dominates all saving rows, giving ell>=205.

### 5.5 A size-two block and a different eigenvalue

Let v=(1,lambda), v'=(1,mu), lambda!=mu. Then

    M_1=u_1 v+u_2 w,  M_2=u_2 v,  M_3=u_3 v'.

Use three fixed codes with coefficient vectors

    c_0=(1,0,0),  c_12=(1,t,0),  c_13=(1,0,s),

where t,s are independent transcendentals. If ker Phi=0, both c_12 and c_13 work: neither (a_1,a_2) nor (a_1,a_3) can vanish, or I_2 is a multiple of rank-one M_3 or M_2. If ker Phi=span(e_2), M_2=0 and u_2=0; M_1,M_3 have rank at most one, so a_1,a_3 are nonzero and c_0,c_13 work. If ker Phi=span(e_3), M_3=0 and a_1 must be nonzero because M_2 has rank at most one; c_0,c_12 work. These exhaust the eigenlines of T^T.

Every saving row is therefore dominated by at least two of the same three scalar codes. Again2 sum_i s_i<=51 and ell>=197. The Jordan forms are exhausted, proving the theorem.

## 6. First remaining envelope geometry

A natural abstract shape outside this theorem uses four independent scalar directions:

    q_1=h_1 tensor e_1+h_2 tensor e_2,
    q_2=h_2 tensor e_1+h_3 tensor e_2,
    q_3=h_3 tensor e_1+h_4 tensor e_2.

A nonzero combination has scalar-coordinate columns(a,b,c,0)^T and(0,a,b,c)^T. They cannot be proportional over any extension, by the first and last nonzero coordinates. Thus this three-dimensional subspace has no nonzero decomposable tensor even after extension and has scalar envelope four. It is only an abstract candidate: no native fitting, charge, source access, movement invoice or completion is asserted.

A finite search may impose this shape but must not assume arbitrary GL_3 quotient basis changes preserve it. Failed finite search is not an all-field impossibility theorem. Physical acquisition and the actual source construction remain separate obligations.

## 7. Limits and credit

The theorem excludes only d<=3 with envelope<=3 at width two. It does not exclude envelopes4,5,6, larger widths, d>=4 or a different physical architecture. The197 bound is not claimed sharp. Native scalar205 and canonical rigidity are retained premises. No strict supplier or foundation is discharged; no complete kappa improves.

Credit the native/canonical predecessors, Worker C's decomposable capacity and Jordan3 observations, root's two-direction theorem, and @CubeJerry. OpenAI assistance is disclosed. No human or formal-kernel review is claimed.
