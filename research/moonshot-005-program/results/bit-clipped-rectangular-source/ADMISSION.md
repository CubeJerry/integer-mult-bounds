# Admission: clipped rectangular source filtration

**Proved for the stated source factorization over every field and block width. No new κ.**

The [author proof](author-root/PROOF.md), [disjoint-cohort extension](author-root/DISJOINT-COHORTS.md), and [independent review](independent-a/REVIEW.md) preserve their exact source pins. Frozen author manifests precede the review; this admission records the reviewed status.

For target cohorts of sizes n_i, source-channel counts m_i, total n and m, source-local U and zero-own-cohort acquisition P with each channel reading at most d other cohorts, every cohort order π gives

    rank(I−UP) ≥ V Σ_i max(0,n_i−m_i+g_i(π)).

The right side retains the per-cohort clipping lost in the earlier rectangular relaxation. If m≤λn, random priorities and conditional convexity yield

    rank(I−UP) ≥ V ceil(n I_d(λ)),
    I_d(λ)=integral_0^1 (1−λ+λu^d)_+ du.

For λ>1, with α=(1−1/λ)^(1/d),

    I_d(λ)=1−dλ/(d+1)+d(λ−1)α/(d+1).

At λ2,d3, I=(3/4)2^(−1/3)−1/2>119/1250. The rational comparison follows by integrating only over [4/5,1], so the consequence does not rely on floating arithmetic.

For n=111b native input blocks, up to all original X and Y channels m≤222b, and one actual E6 chart per source-local channel followed only by containing receiver facets, transposing I=G+DE gives

    rank(G) ≥ V ceil(13209b/1250) > 9bV.

Thus extra original Y couriers alone cannot supply canonical9b within this exact model. Arbitrary uneven allocation, noncommuting block maps and singular within-cohort maps are allowed. The same argument covers fixed disjoint multi-root cohorts that recode at one common chart before exit; enlarging such fixed cohorts does not remove the obstruction.

The claim does not cover overlapping or successively interacting cohorts, nonlocal retained histories, additional acquisition supports, or altered global information. It is not a multiplication lower bound. The root checker supplies144 exact finite controls and four scope-breaking examples; the independent checker supplies128 cases and separate controls. These supplement the universal proof rather than establish it by finite extrapolation.

Credit @CubeJerry, the retained cohort-filtration and native-geometry predecessors, root's clipped integral extension and Worker A's independent proof review, with OpenAI assistance.
