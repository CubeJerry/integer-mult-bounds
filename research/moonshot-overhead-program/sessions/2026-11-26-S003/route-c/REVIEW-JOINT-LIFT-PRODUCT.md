# Independent review of low-rank mixers in the joint star lift

Status: **accepted in the explicitly restricted product architecture**. Reviewed B's `../route-b/joint-lift-product-handoff.md`, the preceding regular-lift note and the actual moment checker. The acceptance uses real scalar row maps, as in the written eigenvalue argument. It does not cover arbitrary full-rank mixing, arbitrary physical operations between lifted calls, or all algorithms for a weighted star sum.

## 1. Actual representation and moments

An alphabet of size at least m+1 permits a tuple with all m+1 entries distinct. Its orbit under coordinate permutations has exactly M=(m+1)! elements and trivial stabilizer. Restricting all star permutations to this invariant orbit therefore gives the regular representation, whose normalized trace detects exactly the identity group element. This is an actual occupied part of the physical address space, not replacement by independent oracle variables.

Each star is a real symmetric involution. The only cancelling length-four words are i,i,j,j and i,j,j,i, with the all-equal word double counted. Their weighted contributions give the stated exact fourth moment 2Q²-sum a_j⁴. The normalized second moment is Q. Cauchy--Schwarz on nonzero eigenvalues gives rank at least M/2 whenever Q>0.

For A-cI, odd trace moments vanish by permutation parity. The fourth moment is M(2Q²-sum a_j⁴+6c²Q+c⁴), bounded by 3M(Q+c²)², while its second moment is M(Q+c²). This proves the M/3 rank bound. Applying the elementary second-moment tail inequality to squared eigenvalues yields the M/12 and M/8 high-singular-value counts used in LP6. The scale is sqrt((Q+c²)/2) or sqrt(Q/2), respectively; it is not a bound on an unnormalized trace.

## 2. Products, exact rank and approximation

Telescoping the q+1 row maps against c_t I gives a sum of q+1 perturbations, each with rank at most M rank(E_t). Left and right multiplication cannot increase rank, even if a factor is singular. Therefore LP4 is valid without invertibility or bounded-norm assumptions on the intermediate row maps. The baseline is c B^q, with c the product of the c_t; B²=I makes its parity dependence explicit.

For even q, every target-minus-baseline block is S_b-cI and has rank at least M/3. For odd q, block j is S_b-cS_j; at most one of its star coefficients can be cancelled, and the remaining m-1 are nonzero. It has rank at least M/2. Thus r(q+1)>=m/3 is necessary for exact realization. The divided form assumes r>0; if r=0, exact realization in this model is impossible.

The numerical version also follows. Every block has at least M/12 singular values at least b_min sqrt((m-1)/2). A map of smaller rank than the combined high-singular-value subspace has a kernel intersecting that subspace nontrivially. On such a vector the difference from the target has norm at least the threshold. Consequently an operator-norm error strictly below that threshold requires r(q+1)>=m/12. This argument places no norm bound on the low-rank perturbations themselves.

The same proof permits row-dependent nonzero real weights b_(row,j), by applying the corresponding block moment estimate separately and taking the minimum absolute weight over all rows and queries. This covers nonzero diagonal seed coefficients; it does not extend the conclusion to arbitrary dense target row matrices without an additional argument. B added this clarification and the real-scalar quantifier during review.

## 3. Physical invoice and scope

Each lifted B call touches all m independent row fibres, so its queried physical volume equals the original full batch volume. The conjugating controlled rotations can be granted zero cost without weakening the rank argument. In the actual separated-half layout the central/leaf pair swap takes two width-f field exchanges; a factor of two is immaterial to the lower invoice.

For fixed positive r and sufficiently large m, the exact and approximation bounds force Omega(m) such call mass. This rejects this fixed-r reflection/product supplier as a way to replace the retained m factor by a subpower factor. The subsequent recurrence is a positive call invoice for this supplier. It is not a lower bound on the fastest tape algorithm for the weighted star sum. Allowing rank-r to grow, composing many rank-one changes into one interval, or using arbitrary full-rank mixing changes the model and is explicitly outside this rejection.

## 4. Independent replay

Copied the checker to `replays/joint-lift-moments/` and ran `python3 -I -B`. It passed 30,912 short-word moment evaluations, 21 weighted cases, 231 scalar-shift cases, and seven alternating-word controls. The source hash is `9e760ae35d37c332a57ad7a9803b05df3745ab24055e220aaafa524c43b885de`; the replay receipt is preserved there.

The checker tests moment identities and inequalities, not an exhaustive search over product algorithms or numerical approximation matrices. The telescoping, rank and high-singular-subspace implications are supplied by the written proof above. This is an AI-assisted independent review, not a formal-kernel or human-referee certificate.
