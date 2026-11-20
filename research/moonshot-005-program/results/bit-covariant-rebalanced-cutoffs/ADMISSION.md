# Two mixed-grade cutoff schedules for the proposed 0.005 source

The rebalanced-tail method used in [upstream #7831](https://github.com/CrocSwap/integer-mult-bounds/pull/7831) transfers to the m=870 target histogram with newly selected cutoffs. At raw price 0.0050000005, 88 product factors suffice with uniform logarithmic power 234. A separate 194-factor schedule lowers that power to 36. Both support the conditional uniform price 0.0050000004. The earlier 2^42-factor witness used a single productive grade. Both the physical source and the ordinary/outer contracts still have to be met.

[Exact arithmetic and proof](author/PROOF.md) · [Independent price check](review/REVIEW.md). Credit Dugongue, Ali Romman, Clear1nsight and @CubeJerry. Substantial OpenAI assistance. No new complete κ.

The [nine-bank ceiling and finite multiplicity thresholds](ideal/PROOF.md) price the same caller under the best possible one-way return. At m=870 its ideal raw crossing is between 0.00504096857045 and 0.00504096857046. A hypothetical physical fitting with 64 excess fields would require m=86 to cross 0.005, compared with 870 at 128 excess fields.
