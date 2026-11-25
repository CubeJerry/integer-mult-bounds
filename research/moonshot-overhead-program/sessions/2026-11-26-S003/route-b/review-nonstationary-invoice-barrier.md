# Independent review of the nonstationary literal-invoice barrier

Reviewer: S003 Route B. Status: **accepted in its explicitly declared positive-invoice scope**. Reviewed C's `NONSTATIONARY-LITERAL-INVOICE-BARRIER.md` in full, including NI1--NI9, its application to B's exact AI recurrence, and the fast-descent countermodel. A's nested-label theorem has its own independent C review; this review imports that theorem and checks the new deduction rather than claiming another independent derivation of its suppliers.

## Local inversion and accumulation

The large-x split at b=x^(3/4), J=x/b is valid: in the second branch J>=64, so Theorem N applies. Cubing and substituting J gives b^3>=x^2 log2(x)/512. In the other branch log2(x)<=x^(1/4) gives the claimed weaker constant. The finite x range is genuinely covered by the absolute b>=1 bound, so the resulting local coefficient is uniform over arity and nesting depth.

I independently differentiated f=x^(2/3)ln(x+2)^(1/3). Multiplying f''/f by 9x^2(x+2)^2 ln(x+2)^2 yields exactly

    -2(x+2)^2 L^2+x(x+8)L-2x^2.

Its discriminant is -3x^3(5x+16)<0. Therefore strict concavity and the stated subadditivity are valid on the whole positive range, not just asymptotically. Concavity with f(0)=0 gives each summand at least its proportional share of f(total), so the arbitrary nonstationary arity accumulation follows.

The normalization hypothesis is necessary and correctly separated from the raw product bound. Merely bounding logarithmic width drop by O(log m) does not preserve the sqrt(m) call factor after normalization. The supplied m^2 fast-descent counterexample distinguishes those claims.

## Application to the actual AI price

AI can enlarge its one fixed threshold to ensure ell<=e/4, A=m+2a<=3m and e/A>=4. Then

    floor((e-ell)/A)>=3e/(4A)-1>=e/(2A)>=e/(6m).

This proves the application's lower split directly; it does not follow only from AI's looser e^(1-delta)/8 display.

The predictor is the declared power-of-two window architecture. In `routes/B/structured-shift-check-refinement.md`, b=5ceil(sqrt(m)), T is the least power of two at least 2b+1, and the actual billed stage budget Dp=T-1 is at least 2b, hence at least sqrt(m). This is a lower bound on that retained budget, not a claim that every equivalent predictor has that minimum degree or cost.

B's enlarged geometric dimension Dg=2(2+hq^h) exceeds the exact underlying rational Gram dimension D=2+h(q^h-1). Its rank fraction is the actual scalar rank or an upper bound for it. Thus Rpen>=Cg I(m), and the retained positive term 8Dp Rpen in Qm pays at least 8Cg sqrt(m)I(m). Leading padding beta>=1 only increases this price. The coefficient exceeds sqrt(6), so the normalized multiplicative invoice retains at least one whole I(m) per spatial descent. NI-P therefore applies to this literal certificate.

This acceptance does not assert that the physical implementation really needs all billed operations. A sharper analysis, a sharing compiler or another representation may leave the price model. In particular the result is not a time lower bound matching AI, and not a lower bound for integer multiplication. The note maintains these distinctions throughout.

## Isolated evidence

An unmodified copied checker was replayed under `replays/c-nonstationary-invoice/`: 2,048 exact concavity discriminants, 489 cubic contraposition cases, 160 exact normalized-price cases, 160 Decimal partition diagnostics and three negative controls passed. The exact checker SHA-256 is `4ed6f2cd516c3732d4685894dda95e3f4e7930c4484b36804eb67303491c4c1b`; proof/checker snapshots are in the replay receipt. Decimal diagnostics are not interval proofs and do not replace the calculus argument.

Prepared for Jerry Chen (@CubeJerry), with substantial OpenAI AI assistance. No formal kernel certification or complete machine run is claimed.
