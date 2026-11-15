# Strengthening the same certificates to a2V slack lower bound

This supersedes the deliberately weaker bound in the first frozen
`PROOF.md`. The original exclusion of dim T≤V remains correct; the exact
same subspace certificates prove the sharper necessary inequality

    dim T≥2V.

No source, information-space or query/depth scope changes. No new empirical
search is used. In particular this strengthening does not transfer the
certificate to a different source or a packed mixture of source spaces.

Use the notation of the main proof. Suppose a slack space T⊂D⊗k^V supplies
both nontrivial virtual demands. For each demand choose a linear section of
the quotient map onto delta_t⊗k^V. This gives a V-dimensional subspace

    F_t⊂T∩(J_t⊗k^V)

whose projection modulo (B+L_t)⊗k^V is injective. Thus

    F_t∩((B+L_t)⊗k^V)=0.

The exact certificate says J_a∩J_b⊂B+L_a (or the corresponding inclusion
for b). Therefore

    F_a∩F_b⊂(J_a∩J_b)⊗k^V⊂(B+L_a)⊗k^V.

The right side is disjoint from F_a, so F_a∩F_b=0. Both spaces lie in T;
consequently dim T≥dim F_a+dim F_b=2V. This holds over every
characteristic-two field and for arbitrary block coding, without requiring
T itself to have dimension V.

The previous one-field proof forced the entire T into each J_t. The improved
argument selects the actual V-dimensional fitting subspaces inside T,
which works at every slack dimension. It is a direct-sum lower bound.

For the fixed augmented source, dim(A/D)=6V. Seven free seed fields can
provide at mostV of D slack, so the q9 two-feedback interface fails. More
generally a changed source with9.5V of acquired W information would leave
1.5V slack in seven free fields, which would also fail **if** this same
pair-intersection certificate were independently re-established on that
changed source. No such transfer is asserted here. The masked block-lane
implementation and any changed-space certificate remain separate obligations.

The checker, `CASES.json` and `CERTIFICATE.json` need no change: they already
verify exactly the intersection inclusion used by this proof. The stronger
statement should be used in future programme dependency maps, with this
versioned explanation retained so the earlier weaker report remains auditable.
