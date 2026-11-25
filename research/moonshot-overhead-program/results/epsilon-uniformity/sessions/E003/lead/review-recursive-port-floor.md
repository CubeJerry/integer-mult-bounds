# Lead review of the recursive port invoice

Disposition: **R1 and R2 accepted within their explicit recursive-invoice
model**. This does not establish a lower bound for physical interchange or
integer multiplication. Reviewed: `../route-c/RECURSIVE-PORT-COST-FLOOR.md`.

The lead independently checked the following proof steps.

- The central-binomial induction is correct: after clearing denominators,
  its induction-step difference is exactly the nonnegative integer `v`.
  The weaker uniform mode bound `sqrt(2/(3m))` covers both parities.
- The centered-tail deficit is at most `(t+1) M_m/2`, with the larger
  parity endpoint included. Consequently the displayed lower bound
  `delta_m(t)>=1/2-(t+1)/sqrt(6m)` is valid, even when its right side
  is negative.
- For `A=6/5`, the proposed potential satisfies
  `t+4A sqrt(m) delta_m(t)>=A sqrt(m)` for every integer `t>=0`,
  `m>=4096`. The exact last comparison reduces to `151321/25600<6`.
  The `t>=A sqrt(m)` case is separate, so no negative tail lower bound
  is used incorrectly at large degree.
- Finite-tree induction applies to arbitrary node-dependent degrees and
  port dimensions. All four target/inverse uses are charged. A leaf
  without ports must have degree at least `m` by the positive rank
  obstruction for every smaller degree. The potential scales with its
  independent row count, not the number of simultaneously stored rows.
- For fixed `q>2`, uniform central-limit convergence on a compact interval
  yields the stated asymptotic subsolution. The continuous positive gap
  on `[0,A]` is justified when `A<Lambda_q`, including the endpoint
  `c=0` because `q/2>1`. The derivative and unique-minimum equations
  in R8 are correct. No decimal approximation enters either theorem.

The crucial pricing assumptions remain visible: a counted depth-t node
pays at least `Wt` row-stages, and each port dimension pays `q` complete
recursive same-target transforms. Those are defined invoice rules. The
source's upper-bound shared-pencil formula is not evidence of a minimum
tape cost per stage. In particular, R1 does not prove that the actual
machine must lose a factor 6/5 at every spatial level, and it does not
exclude changing the converter word or sharing work across levels.

The new obstruction is useful because it identifies such a converter
change as a meaningful next experiment. It gives no new upper-bound
hypothesis and no unrestricted lower-bound claim. AI-assisted written
review is distinct from formal-kernel or human verification.
