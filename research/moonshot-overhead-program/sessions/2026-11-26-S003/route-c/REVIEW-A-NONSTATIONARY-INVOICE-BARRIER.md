# Independent review of A's nonstationary invoice barrier

Decision: **accepted as the scoped positive-invoice theorem stated** in `route-a/nonstationary-invoice-barrier.md`. This is not an actual-time lower bound. A and C independently converged on this consequence of the previously accepted Theorem N; their notes are corroborating proofs of one shared result.

I read the complete proof. The following are the consequential checks.

For x=log₂m>=4096, the proposed real J=(1024x/log₂x)^(1/3) is at least64. The relation

    log₂J=(10+log₂x-log₂log₂x)/3 >=(log₂x)/6

holds throughout that range. Theorem N would then require x>=(4/3)x if I<=m^(1/J), a contradiction. The resulting coefficient2^(-10/3) against x^(2/3)(log₂x)^(1/3) is greater than1/16 against F(x), after the stated logarithm comparison. The large-x local conclusion is valid uniformly in nesting depth.

For2<=x<4096, the exact Gram formula gives D>=23 and the exact incidence recursion gives lambda>=27. Therefore log₂I>9, while F(x)<1024. This proves the claimed global coefficient1/128. It uses the actual minimum dimensions of this family rather than an unsupported numerical small-range test.

The ratio F(x)/x is decreasing because ln(x+2)-x/(x+2)>0. Its derivative is x/(x+2)²>=0 and its limit at zero is ln2>0. This supplies both subadditivity and F(cx)>=cF(x) for0<=c<=1. Strict concavity, proved independently in C's note, is a stronger property but is unnecessary for A's argument.

The lower split e_next>=e/(8m) is essential and is explicitly retained. Together with Lambda>=8sqrt(m)I, it yields normalized multiplier at least sqrt(8)I. Since m>=4, each logarithmic drop is at most log₂m+3<=(5/2)log₂m. Telescoping to a terminal width at most E and applying subadditivity therefore gives the stated1/320 coefficient. The normalized base value is correctly bounded by E^(-1/2) when the unnormalized base bill is only at least one.

The scope is precise: B_i is the declared positive charged recurrence, which may overestimate actual execution. No reversal of an algorithmic upper bound is used. Unequal arities, nested distances and arbitrarily uneven admissible drops are permitted. A different actual call count, partition, predictor or width accounting lies outside the theorem and may evade it.

The present full source invoice satisfies the declared lower price because its window/predictor stage budget is at least sqrt(m), its dimension dominates the actual Gram rank, and its positive endpoint and reserve terms are retained. B independently reviews that application. These statements do not assert that each actual tape call is individually necessary.

This acceptance is a written mathematical review. No whole machine, lower-bound kernel proof or human referee certification was performed. C's independent finite discriminant/partition/normalization checker supports the shared consequence but is not counted as a proof of all label ranks or asymptotic cases.

Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance; the source and predecessor attribution in A's note is retained.
