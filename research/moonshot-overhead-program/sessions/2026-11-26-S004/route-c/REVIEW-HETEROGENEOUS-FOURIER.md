# Independent review: heterogeneous Fourier invoice

Reviewer: S004 Route C. Verdict: **accepted as a restricted positive-invoice
lower bound**. It does not lower-bound actual Fourier or multiplication
time, and does not contradict the JR construction, which changes its
literal incidence premise.

Reviewed Route A's `heterogeneous-fourier-invoice-barrier.md` in full.
The full pinned Fourier kernel was read during the preceding JR review.

HF1's marginal-space proof is exact over F2. Marginal tuples have common
sum F, dimension sum(q_i)-L+1, and are all attainable by coordinate-line
assignments plus a reference value. A zero Gram image forces constant
marginals; even q_i then force F=0, leaving an L-1 dimensional kernel.
Thus D=2+sum(q_i-2), including the all-binary rank-two case. In particular
D is at least the largest alphabet, so a coarse-rank improvement does
not make a large alphabet logarithmically cheap in this invoice.

HF5 is a separate rational calculation. The top binomial coefficient is
2^-r. On each tensor space with exactly r zero-sum factors, every smaller
equality cylinder vanishes and only the matching r-cylinder survives.
Its eigenvalue is nonzero. These mutually independent spaces give
rank(P)>=e_r(q_i-1), and choosing the largest r alphabets yields
rho/N>=2^(-T0-r). No rank over Q is substituted for rank over F2.

The free incidence is exactly the odd-subset sum of products t_i. All
weights at odd distances are nonzero. Its selected largest-factor term,
the count of odd subsets, the binary dimension and charged-rank bound
give each of HF9's four inequalities. With b<x/4 they imply T0>=x/2;
the three ranges of r then prove the claimed constant 1/8 at x>=256.
This argument genuinely allows heterogeneous alphabets and does not
assume the usual hard charged-rank guard. The old homogeneous upper
construction supplies the matching order for this specified expression.

Arbitrary correlated free rectangles, cancellation/endpoint execution
improvements, or replacing the charged matrix leave the stated model.
The note correctly keeps those mechanisms open. The isolated copied
checker and helper reside in `replay-heterogeneous-fourier/`; its receipt
is arithmetic evidence, not a tape implementation or proof of asymptotic
optimality beyond the written invoice theorem.

The isolated replay passed all 13 matrix families (101,200 entries),
exact first-difference incidences and 1,452 integer invoice profiles.
Its field-mixing and lower-degree-zero controls were exercised as stated.
