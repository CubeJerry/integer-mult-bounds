# An eight-evaluation lower bound in odd characteristic

Take the authenticated 111 primitive native roots v_i. Divide the eight coordinate roots by two before use. All entries then lie in {−1,0,1}, every proper foreign pair has integer inner product zero, and every squared norm is 1 or 4.

Let A be a finite abelian group. Consider the native output T_i(x)=x_i+Σ f_ij(x_j), with f_ij(0)=0 and f_ij(−x)=−f_ij(x) on all proper cells. Evaluate this same map eight times on the original input, using x_j^(t)=v_jt x_j. Then

    Σ_t v_it T_i(x^(t)) = ||v_i||² x_i + Σ_{j foreign to i} (v_i · v_j) f_ij(x_j)
                          = ||v_i||² x_i.

The eight outputs allow the joint recovery of all eight coordinate-role inputs and the multiples 4x_i at every other role. Consequently |im T|⁸ ≥ |A|⁸ |4A|¹⁰³ without any invertibility assumptions. For odd-order A this gives |im T|⁸ ≥ |A|¹¹¹. Edge maps can be nonlinear when they commute with negation.

For arbitrary odd-characteristic fields with b-dimensional blocks one has 8 rank M≥111b, including infinite fields. Indeed the direct sum of eight copies of M, precomposed with the eight native sign encodings and postcomposed with the signed readout, has block diagonal (||v_i||² I_b)_i and rank 111b. At b=3,840 the return rank is at least 53,280, exceeding the 34,688 target. The argument allows arbitrary singular proper cells and does not require the certified tree. Its premises differ from those of the finite-alphabet rigidity result for arbitrary edge functions.

The rank-product calculation is the complement form of the fractional Haemers bound. The signed, nonadditive extension follows directly from the eight equations above. Credit @CubeJerry and the native root atlas. No new κ.
