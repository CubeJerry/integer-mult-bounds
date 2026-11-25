# Independent review of shift-only checks and the small repair field

Reviewer: Route A, S002, 2026-11-25.

**PASS for SC1--SC2, the exact paid check fractions, the degree-compatible
predictor and the logarithmic-degree repair field** in
`../B/structured-shift-check-refinement.md`. This review does not establish
a succinct physical tensor executor or improve the accepted global rate.

The completed predictor is scalar on every internal module coordinate in
one shift block. Therefore its containing exceptional row set has the
product form J_shift times the module index. Restricting H0 tensor I to
that set gives (H0 restricted to J_shift) tensor I. The left inverse and
transpose right inverse tensor identically, so both error recovery and
lift in the existing repair proof remain exact on arbitrary independent
module-row inputs. No zero workspace occupancy is counted as data.

The projective F3 shift vectors are pairwise linearly independent, and
including a basis makes the seed map injective. A fixed frequency shift
preserves their uniform pairwise distribution. Each digit has mean one
and variance 2/3, giving the exact count variance 2m/3. Chebyshev with
radius 5ceil(sqrt m) bounds the exceptional proportion by 2/75<1/32
at every frequency. This is a deterministic guarantee over the whole
chosen seed family, not a randomized success claim.

The least admissible projective dimension gives
2m+1<=3^r<6m+3. Selecting the basis first and then unused normalized
projective representatives is an explicit polynomial-m constructor.
The power-of-two-minus-one window contains the symmetric tail window
and remains O(sqrt m); for m>=4096 it has D<=m. All additions in A's
carry formulas and factored Lucas expression admit power-of-two budgets,
so the base-F4 cyclic construction is valid. The final odd-length product
requires concatenation only.

The rounding inequality is correct: B>=219 implies
B(1/32-2/75)>=1, and therefore floor(B/32)>=(2/75)B.
After the paid module duplication v=32w, R=Bv and S=R/32 are integers.
The actual tensor check has floor(B/32)*v<=S rows. Appending the remaining
zero *check* rows adds charged internal transform inputs, not independent
parent rows. Thus each two-array phase contains exactly 2S=R/16 rows;
the four-child total fraction stays 1/4.

Only B distinct Vandermonde nodes are needed, rather than Bv. A degree
ceil(log4 B) field over F4 supplies them, and bounded monic irreducible
enumeration plus trial polynomial division costs polynomial B. All
node differences are units. Shift-space matrices and their inverses have
polynomial-m dimensions and coordinate cost; their tensor identity factor
does not require new nodes. The full 3^m frequency table remains an
explicit exponential setup option, correctly retained in B's note.

The claimed interface boundary is accurate. The module width can still
be exponential, and neither sparsity nor a small coefficient field by
itself proves inexpensive fixed-tape row-index permutations, aligned data
movement, or numerical preparation. The existing Q theorem and its
numerical invoice constants are preserved. This is an optional finite
structural refinement for a future physical execution proof.

Independent exact check: `verify_shift_check_refinement.py` passed 1,147
moment/tail cases, 144 exact check-budget cases, and 176 tensor left/right
inverse basis cases over F5, with a negative control rejecting proportional
ternary shift vectors. Results are in
`shift-check-refinement-verification.json`. This checks the finite algebra
and accounting, not a physical executor.
