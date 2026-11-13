# Exact one-extra-coset gluing on the actual111 BIT code

Status: mathematical theorem with exact source certificate, pending independent root review. Scalar values over ANY characteristic-two field. This concerns the restricted historical code C+span(h), not arbitrary rank-ten fittings or arbitrary operator-valued extensions.

## Exact finite source premises

Let K be the canonical111-source fitting and C=rowspan(K), dimension9 over F2. Pick a binary basis of its rows. Let p_j in F2^9 be the evaluation column of that basis at coordinate j, and a_i in F2^9 the coefficient vector expressing K_i in the basis. Then K_ij=a_i dot p_j. All111 a_i are distinct and nonzero. Put Z_i={j:K_ij=0}, T_i={j:K_ij=1}, and S_i=T_i minus{i}. Thus T_i is the closed real-orthogonality neighborhood, with the own coordinate included.

The independent verifier reconstructs K from the authenticated rational roots and certifies:

1. rank{p_j:j in Z_i}=8 for every i.
2. rank{p_l:l in Z_i intersect Z_j}=7 for ALL6105 distinct pairs.
3. |T_i intersect T_j|<=36 for ALL distinct pairs; the actual maximum36 is attained.

The second rank is exactly the full annihilator of independent a_i,a_j. These binary rank certificates hold over every characteristic-two extension field. A zero-restriction codeword on Z_i is therefore a scalar multiple of K_i. A fitting row in C with diagonal one is uniquely K_i.

For a scalar h, define its availability set

    A(h)={i: (h+C) intersects coordinate-span(S_i)}.

The definition depends only on its quotient class. Equivalently, h restricted to Z_i agrees with a codeword and its own coordinate can then be canceled by a multiple of K_i. Closed T_i or open S_i give the same quotient availability because K_i has self coordinate one and support T_i.

## Gluing lemma

For i in A(h), choose local coefficients q_i in F^9 with h_l=q_i dot p_l for all l in Z_i. If i,j are available, their difference annihilates the seven-dimensional pair intersection. Hence

    q_i-q_j belongs span(a_i,a_j).

If the available normals span rank at least three, these pair conditions force one global q with

    q_i=q+lambda_i*a_i for every available i.

Proof: choose three independent a1,a2,a3. Comparing the three pair differences makes the coefficient on a1 agree in q1-q2 and q1-q3. Subtract that multiple of a1 from q1 to obtain q; then q2-q and q3-q are multiples of a2,a3. For any other a, its difference from q lies in each span(a,a1),span(a,a2),span(a,a3). Modulo span(a), at least two of a1,a2,a3 remain independent, so that intersection is just span(a). This includes the cases where a equals a selected normal. All factor order issues disappear because this theorem is scalar.

Put g_l=h_l-q dot p_l. Since a_i dot p_l=0 on Z_i, g vanishes on every Z_i of an available i. Thus

    h+C=g+C,    support(g) subset intersection_(i in A(h)) T_i.

Conversely any g supported in this intersection is available at every listed i: g-g_i K_i has zero self coordinate and is supported in S_i. Consequently, for any index set I whose a_i span rank at least three, the exact intersection identity is

    intersection_(i in I) (C+coordinate-span(S_i))
      =C+coordinate-span(intersection_(i in I) T_i).

This is the requested rigorous availability/intersection lemma, not a random search or numerical rank extrapolation.

## Large availability is exactly a coordinate exception

If |A(h)|>=37, the normals have rank at least three: any two-dimensional span of distinct nonzero binary vectors contains at most three such projective points, even over an extension field (a binary two-by-two unit minor recovers binary coefficients). Apply gluing to obtain g in the same coset, supported in every T_i with i available. If the coset is nonzero, g is nonzero. If g has two different nonzero coordinates j,k, symmetry of K gives

    A(h) subset T_j intersect T_k,

contradicting the exact36 common-neighborhood ceiling. Hence g=c*e_j for one coordinate and c!=0.

Therefore EVERY nonzero coset outside the111 coordinate projective classes has availability at most36. In particular none can be available at52 rows. The bound36 is sharp on this source: the verifier supplies a pair j,k with |T_j intersect T_k|=36 and h=e_j+e_k. Its availability contains those36 rows. The binary code has minimum distance48 (all511 nonzero words are checked), so this coset is nonzero and is not any coordinate coset; the theorem then gives availability exactly36. The zero coset is excluded from the large-availability classification.

## All fittings in the one-extension code

Let scalar fitting A have rowspace inside C+span(h), so A_i=c_i+t_i h. If t_i=0, local injectivity gives A_i=K_i. Every changed row with t_i!=0 makes h available at i. If h is non-coordinate, at most36 rows can change; at least75 rows retain the full canonical foreign support.

If at least37 rows change, glue on their active set and absorb the one global codeword into all c_i. Its coset representative is g=c e_j and it vanishes on every active noncontact set. The exact fitting form is

    A_i=(1-t_i*g_i) K_i+t_i*g.

This follows because the remaining codeword part vanishes on Z_i and is thus a multiple of K_i; the diagonal fixes that multiple. For every i other than j, only foreign column j can change. All those110 rows retain at least54 foreign nonzeros because original degree>=55. Row j may lose its whole foreign support; no stronger claim about it is needed. This handles arbitrary characteristic-two scalar coefficients, not just F2 flips.

## Consequence for the priced monotone target

Use the admitted generalized-scattering normal form and E7 union ceiling52. A row retaining canonical foreign support, or any foreign support of size>=53, requires at least two additional X/packet proper-chart contributions beyond its Y last-proper chart. With111 original X plus q packet paths, there are at most111+q facet visits.

For a non-coordinate h,75 unchanged rows require at least150 visits. For the large-active coordinate exception,110 rows require at least220. Small-active coordinate cases already have at least75 unchanged rows, so150 is a universal lower bound for this entire one-extension code architecture. Canonical h in C is even stronger.

Thus q8 original paths provide119 visits and require at least31 additional upward-local arrivals; q9 paths provide120 and require at least30. Extra copies born from existing cell values are covered by rectangular X blocks; birth at a facet adds no new local remainder support. Each genuinely new proper contribution requires its own positive-rank MOVE. The q8 all-unit target's limiting margin is<4, while q9's optimistic direct-route margin is<12. Neither pays31 or30 extra unit calls. Both strict targets therefore fail in this CODE interface, even with the stated extra upward-local copies.

This closes G=C+span(h) and its vertex-gauge equivalents, not arbitrary rank-ten rowspaces. It supplies no packet-count lower bound beyond the separately proved cut, no new all-width compiler, and no supplier. Arbitrary entangled operator-valued extra rows are not covered. Changed larger global codes, changed route families and all complete original-input endpoint/price obligations remain.

For the vertex-gauge extension, write the code as C D+span(h), with D invertible diagonal. If A fits, then D A D^-1 also fits and has rowspace inside C+span(h D^-1). Its foreign nonzero supports, and the supports of I-A after the same conjugation, are unchanged. Thus the preceding route count applies. No arbitrary dense input transformation is granted.
