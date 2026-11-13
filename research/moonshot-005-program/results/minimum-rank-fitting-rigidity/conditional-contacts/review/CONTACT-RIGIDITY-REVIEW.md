# Independent review of block fitting rigidity with invertible contacts

**Classification: proved in the stated scope. No new κ.** Root independently
reviewed the author's argument and rebuilt the finite source premises directly
from the pinned native word. This is not a rerun of the author's verifier.

The reviewed proof has SHA256
`fb8b348dd0d82ac3c0c117dc04ee7ad6688096806a173830514f645d3365dbb1`.
All four reviewed author-file hashes, including the frozen manifest, are in
`CONTACT-RIGIDITY-REVIEW.json`. The source gzip is
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.

## Proposition and exact logical scope

Let G be the fixed dyadic normalized Gram matrix of the actual 96 hosted roots,
and B=(5,56,69,100,65,77,96,103). Over any field of characteristic other than 2,
for any integer V≥1, suppose K has V×V blocks, diagonal I, zeros wherever G has
zeros, scalar rank 8V, and invertible K(i,b), K(b,i) for every allowed B contact.
Then K(i,j)=G(i,j) T_i T_j⁻¹ for invertible T_i. The converse also holds.

The field statement refers to specialization of a matrix over Z[1/2]. The
9-coordinate realization used to check it over Q has a normalization by 18;
division by 18 is not performed in characteristic 3. All identities needed by
the theorem are dyadic identities with allowed values ±1/2 or 1, and specialize
validly in every characteristic other than 2.

The contact-invertibility premise is explicit and unproved in general. This
review neither asserts that all fitting matrices satisfy it nor excludes a
singular-contact, larger-rank, different-source or characteristic-two code.

## Independent algebra check

1. K(B,B)=I_(8V) and rank(K)=8V imply the Schur complement is zero. Thus
   K=C R with C=K(:,B) and R=K(B,:), without a symmetry or positivity premise.
2. Write C(i,p)=g_ip X_ip and R(p,i)=g_ip Y_pi on the allowed contacts. For an
   orthogonal source pair with support intersection {p,q}, the dyadic signs
   cancel and give X_iq⁻¹ X_ip = Y_qj Y_pj⁻¹. The complete bipartite graph for
   each pair has exactly the two sign components used by the proof.
3. If σ=g_ip/g_iq and τ=g_iq/g_ir, the row triangle is
   λ_qr^τ λ_pq^σ=λ_pr^(στ), whereas the column triangle is
   λ_qr^(−τ) λ_pq^(−σ)=λ_pr^(−στ). An actual second source row with both
   ratios reversed has the same ordered left side as the column identity and
   the opposite right-side sign. This proves λ_pr^+=λ_pr^- without commuting
   any operators. Independent witnesses exist for every one of the 28 pairs.
4. Every coordinate triple occurs in an actual source row, so the common
   ratios satisfy λ_qr λ_pq=λ_pr. Put D_0=I and D_p=λ_p0. Then
   λ_pq=D_q⁻¹ D_p. Accordingly X_ip=T_i D_p and Y_pi=D_p⁻¹ P_i. For B rows
   take T_bp=D_p⁻¹ and P_bp=D_p. Direct substitution yields
   K(i,j)=G(i,j) T_i P_j, and its diagonal forces P_i=T_i⁻¹.
5. The converse is block-diagonal conjugation of G⊗I_V, which preserves rank,
   zeros, identity diagonal and the required contact invertibility.

Every inverse used here is justified by a displayed premise or an established
product of invertible matrices. In particular, rank 8V alone is not used to
infer invertibility of any individual contact.

## Finite source verification and controls

The independent checker reconstructs 96 actual roots as integer vectors in Q⁹,
checks all 9,216 Gram entries and their factorization through B, and extracts
the 14 support quads. It uses union/find over all source edges to check the 28
pair graphs, rather than importing the author's graph algorithm or trusting
its spanning trees. It independently searches all rows and middle coordinates
for all 28 sign-collapse witnesses, and checks all 56 triple supports.

Noncommuting 2×2 unipotent matrices satisfy every correctly ordered cocycle
identity. Reversing the order fails. Removing the graph constraints leaves
isolated vertices and cannot justify the contact-ratio gluing. Both checks
guard genuine logical premises; neither is offered as a universal search over
arbitrary fitting matrices. The checker passes both ordinary and optimized
Python, because acceptance does not rely on assertions.

Reproduce from an installed package directory:

```sh
python3 -I -B review/review_contact_rigidity.py --repo REPO --author PACKAGE --output OUT.json
python3 -I -B -O review/review_contact_rigidity.py --repo REPO --author PACKAGE --output OUT-OPT.json
```

## Consequences and limits

The row code is row(G⊗I_V) followed by invertible coordinatewise block maps.
Hence every whole-coordinate support and every shortened-code dimension is
preserved. Over characteristic zero, the programme's separately proved hosted
Gram minimum distance 42 transfers: a nonzero vector-valued word has a nonzero
scalar component of support at least 42, and a scalar minimum word in one
component attains 42. Invertible coordinatewise maps preserve those supports.

This statement alone supplies no physical operation and no price reduction.
Implementing arbitrary T_i, restoring original endpoints, collecting input
rows, routing fields and satisfying precision/compiler/uniformity interfaces
remain obligations. A transport lower bound transfers only when all of that
bound's additional access premises hold. The result is a source-specific
classification useful to the ongoing joint forward/reverse construction.

Credit: author worker B; independent mathematical and source review by root,
with AI assistance under the @CubeJerry persistent programme. The predecessor
source and distance theorem retain their original credit.
